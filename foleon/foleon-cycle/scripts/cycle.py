#!/usr/bin/env python3
"""Mechanics for the cycle doc — the deterministic half of `foleon-cycle`.

Governed by docs/stds/CYCLE_DOC.md (CYC-1…CYC-13). The split is deliberate:
this script owns everything with a pass/fail answer (skeleton shape, hill
values, task placement, banned log patterns, close preflight). Everything that
needs judgement — is this topic shaped, is this scope name the maintainer's own
word, does this log line pass a gate — stays with the model, because a script
that guessed at those would be confidently wrong.

The model edits the markdown directly; `validate` is the backstop that runs
after. That is why there is no `topic`/`scope`/`task` subcommand: markdown is
already the interface, and a second one would drift from it.

Usage:
  cycle.py new --id ID [--start YYYY-MM-DD] [--end YYYY-MM-DD]
  cycle.py active
  cycle.py validate [--id ID]
  cycle.py status [--id ID]
  cycle.py log --repo R --scope S --text "..." --gate state|decision|surprise [--date D]
  cycle.py render [--json] [--id ID]
  cycle.py tickets [--json] [--id ID]
  cycle.py snapshot --why "..." [--id ID]
  cycle.py close [--id ID]

The cycle directory keeps a local-only git history (no remote, never pushed),
authorised by the maintainer for that directory alone. `new`, `log` and `close`
commit on their own; `snapshot` records a hand-edit.
"""

import argparse
import datetime
import glob
import os
import re
import sys

HILLS = ('uphill', 'top', 'downhill', 'done')
DEV_WEEKS = 6          # the bet window: everything shaped must fit here
COOLDOWN_WEEKS = 2     # bug-fixing / research, deliberately NOT tracked in the doc
SELF_RE = re.compile(r'^self\s*:\s*(.+)$', re.I)   # a task for the maintainer, never a Jira ticket
GATES = ('state', 'decision', 'surprise')

# CYC-8: a log line states an outcome, not an activity. These openers describe
# activity, and every one of them is a line git already tells you.
BANNED_LOG = (
    'worked on', 'working on', 'continued', 'continuing', 'wip', 'some progress',
    'progress on', 'more work on', 'started looking', 'kept going', 'touched',
    'various fixes', 'misc',
)
PCT = re.compile(r'\b\d{1,3}\s?%')
TOPIC_RE = re.compile(r'^## ((?:\[[a-z0-9._-]+\])+)\s+(.+?)\s*$')
SCOPE_RE = re.compile(r'^### scope:\s*(.+?)\s+[—-]\s*([a-z]+)\s*$')
TASK_RE = re.compile(r'^- \[([ xX])\]\s*(~\s*)?(.+?)\s*$')
LOG_RE = re.compile(r'^- (\d{4}-\d{2}-\d{2})\s+\[([a-z0-9._-]+)\]\s+(.+?)\s+(?:→|->)\s+(.+?)\s*$')
FIELDS = ('Outcome:', 'Appetite:', 'No-gos:', 'Done when:')


DEFAULT_HOME = '~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES'


def cycle_home():
    """The maintainer's own cycle directory — never a code repo (CYC-1).

    Resolved from FOLEON_CYCLE_HOME or the default, and never from the cwd: a
    cwd-relative location is exactly how a cycle doc ends up committed to
    whichever repo you happened to be standing in. It deliberately does not live
    beside this script either — skills-tinky is a skills repo, shared between
    professional and personal work and pushed to GitHub, so work product does
    not belong in it (CYC-1, v1.1.0).
    """
    d = os.path.abspath(os.path.expanduser(os.environ.get('FOLEON_CYCLE_HOME') or DEFAULT_HOME))
    # Fail closed if the directory sits inside someone else's git work tree: that
    # would put cycle docs under a repo's version control by accident, which is
    # the mistake v1.1.0 of the standard exists to prevent. The cycle directory
    # being its own repo is fine — that is the opt-in local history.
    probe = d
    while True:
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
        if os.path.isdir(os.path.join(probe, '.git')):
            die(f'cycle directory {d} is inside the git repo at {probe} (CYC-1). '
                f'Set FOLEON_CYCLE_HOME to a directory outside it.')
    os.makedirs(d, exist_ok=True)
    return d


def state_dir():
    return cycle_home()


def git(home, *args):
    """Run one git command inside the cycle directory. Returns (ok, output)."""
    import subprocess
    try:
        r = subprocess.run(('git', '-C', home) + args, capture_output=True, text=True, timeout=15)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, str(e)


def snapshot(home, message):
    """Commit the cycle directory — local history, no remote, ever.

    The maintainer authorised this explicitly for THIS directory only
    ("SHAPEUP-CYCLES may auto-commit", 2026-08-19), as a narrow carve-out from
    their standing rule that nothing commits without per-message consent. Narrow
    by construction: this only ever runs inside the cycle directory, only stages
    that directory, and never configures a remote or pushes — there is nowhere
    for this history to go, which is the point.

    Commits carry a Co-Authored-By trailer for Claude, at the maintainer's request
    and for this history only (2026-08-19) — the plans and log lines here are
    written collaboratively, so the history says so.

    A failed commit must never cost the write that preceded it, so every error is
    a warning, not an exception: the markdown is already on disk.
    """
    if not os.path.isdir(os.path.join(home, '.git')):
        ok, out = git(home, 'init', '-q')
        if not ok:
            print('cycle.py: note - git init failed, continuing without history (%s)' % out,
                  file=sys.stderr)
            return
        gi = os.path.join(home, '.gitignore')
        if not os.path.exists(gi):
            with open(gi, 'w', encoding='utf-8') as fh:
                fh.write('# Hook runtime state - never versioned.\n.state/\n')
        print('cycle.py: initialised local history in %s (no remote - nothing is ever pushed)' % home)

    ok, out = git(home, 'remote')
    if ok and out:
        print('cycle.py: refusing to commit - %s has a remote (%s). This history is meant to stay '
              'on the laptop.' % (home, out), file=sys.stderr)
        return

    # Trailer on the cycle history only. It is scoped by construction: this is the
    # one place cycle.py commits, and it commits nothing but the cycle directory.
    # Nothing global changes, and no other repo is touched.
    message = message + '\n\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>'

    git(home, 'add', '-A', '.')
    clean, _ = git(home, 'diff', '--cached', '--quiet')
    if clean:
        return  # nothing staged -> nothing to record
    ok, out = git(home, 'commit', '-q', '-m', message)
    if not ok:
        first = out.splitlines()[0] if out else '?'
        print('cycle.py: note - commit failed, the file is still saved (%s)' % first,
              file=sys.stderr)


def doc_path(cycle_id):
    return os.path.join(state_dir(), f'{cycle_id}.md')


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def find_active():
    hits = []
    for p in sorted(glob.glob(os.path.join(state_dir(), '*.md'))):
        head = read(p).split('\n', 3)[:3]
        if any('Status: active' in ln for ln in head):
            hits.append(p)
    return hits


def resolve(cycle_id):
    if cycle_id:
        p = doc_path(cycle_id)
        if not os.path.isfile(p):
            die(f'no cycle doc at {p}')
        return p
    hits = find_active()
    if not hits:
        die('no active cycle doc. Create one: cycle.py new --id <cycle-id>')
    if len(hits) > 1:
        die('more than one active cycle doc (CYC-1 allows one at a time):\n  ' +
            '\n  '.join(os.path.basename(h) for h in hits))
    return hits[0]


def die(msg, code=2):
    print(f'cycle.py: {msg}', file=sys.stderr)
    sys.exit(code)


class Doc:
    """Parsed view of a cycle doc. Only the skeleton CYC-2 fixes is understood."""

    def __init__(self, path):
        self.path = path
        self.lines = read(path).split('\n')
        self.cycle_id = None
        self.status = None
        self.topics = []        # {repos, name, fields{}, scopes[], line}
        self.log = []           # (lineno, raw, match|None)
        self.problems = []
        self._parse()

    def _parse(self):
        m = re.match(r'^# Cycle\s+(.+?)\s*$', self.lines[0] if self.lines else '')
        if m:
            self.cycle_id = m.group(1)
        else:
            self.problems.append('CYC-2: line 1 must be "# Cycle <cycle-id>"')
        for ln in self.lines[:4]:
            s = re.search(r'Status:\s*(\w+)', ln)
            if s:
                self.status = s.group(1)
                break
        if self.status not in ('active', 'closed'):
            self.problems.append('CYC-2: header must carry "Status: active" or "Status: closed"')

        in_log = False
        topic = None
        scope = None
        for i, raw in enumerate(self.lines, start=1):
            if raw.strip() == '## Dev log':
                in_log, topic, scope = True, None, None
                continue
            if in_log:
                if raw.strip().startswith('- '):
                    self.log.append((i, raw, LOG_RE.match(raw)))
                elif raw.strip().startswith('#'):
                    self.problems.append(f'line {i}: CYC-2 — nothing may follow the dev log')
                continue

            t = TOPIC_RE.match(raw)
            if t:
                topic = {
                    'repos': re.findall(r'\[([a-z0-9._-]+)\]', t.group(1)),
                    'name': t.group(2), 'fields': {}, 'scopes': [], 'line': i,
                }
                self.topics.append(topic)
                scope = None
                continue

            s = SCOPE_RE.match(raw)
            if s:
                if topic is None:
                    self.problems.append(f'line {i}: CYC-7 — scope outside any topic')
                    continue
                scope = {'name': s.group(1), 'hill': s.group(2), 'tasks': [], 'line': i}
                topic['scopes'].append(scope)
                continue

            k = TASK_RE.match(raw)
            if k:
                if scope is None:
                    self.problems.append(
                        f'line {i}: CYC-7 — a task must sit under a scope, not directly under a topic')
                    continue
                text = k.group(3)
                m_self = SELF_RE.match(text)
                scope['tasks'].append({
                    'done': k.group(1).lower() == 'x', 'nice': bool(k.group(2)),
                    'text': m_self.group(1) if m_self else text,
                    'kind': 'self' if m_self else 'jira', 'line': i,
                })
                continue

            if topic is not None and scope is None:
                for f in FIELDS + ('Open questions:', 'Shipped:', 'Cut:'):
                    if raw.startswith(f):
                        topic['fields'][f] = raw[len(f):].strip()

    # ---- rule checks -------------------------------------------------------

    def check(self):
        p = list(self.problems)
        body = '\n'.join(self.lines)

        if '## Dev log' not in body:
            p.append('CYC-2: the doc must carry exactly one "## Dev log" section')
        elif body.count('\n## Dev log') > 1:
            p.append('CYC-2: more than one "## Dev log" section')

        for m in PCT.finditer(body):
            ln = body[:m.start()].count('\n') + 1
            p.append(f'line {ln}: CYC-6 — no completion percentages ({m.group(0)!r}); '
                     f'the hill carries status')

        for t in self.topics:
            where = f'topic "{t["name"]}" (line {t["line"]})'
            if not t['repos']:
                p.append(f'{where}: CYC-9 — needs a repo tag, e.g. "## [fio] {t["name"]}"')
            for f in FIELDS:
                if f not in t['fields'] or not t['fields'][f]:
                    p.append(f'{where}: CYC-3 — missing "{f}"')
            ap = t['fields'].get('Appetite:', '')
            if ap and '(fixed)' not in ap:
                p.append(f'{where}: CYC-4 — appetite must be marked "(fixed)"')
            if ap:
                weeks = re.search(r'(\d+(?:\.\d+)?)\s*w', ap, re.I)
                days = re.search(r'(\d+(?:\.\d+)?)\s*d', ap, re.I)
                if weeks and float(weeks.group(1)) > DEV_WEEKS:
                    p.append(f'{where}: CYC-4 — appetite {weeks.group(1)}w exceeds the '
                             f'{DEV_WEEKS}-week dev window; hammer the scope or split the topic')
                elif days and float(days.group(1)) > DEV_WEEKS * 5:
                    p.append(f'{where}: CYC-4 — appetite {days.group(1)}d exceeds the '
                             f'{DEV_WEEKS}-week dev window ({DEV_WEEKS * 5} working days)')
            if ap and 'first cut' not in ap.lower():
                p.append(f'{where}: CYC-4 — no first cut named; add "· First cut: <what goes first>"')
            for s in t['scopes']:
                if s['hill'] not in HILLS:
                    p.append(f'scope "{s["name"]}" (line {s["line"]}): CYC-2 — hill must be one of '
                             f'{", ".join(HILLS)}, got {s["hill"]!r}')
                if s['hill'] == 'done':
                    open_must = [k for k in s['tasks'] if not k['done'] and not k['nice']]
                    if open_must:
                        p.append(f'scope "{s["name"]}" (line {s["line"]}): CYC-7 — marked done with '
                                 f'{len(open_must)} must-have task(s) open (a "~" nice-to-have may '
                                 f'stay open, a must-have may not)')

        for lineno, raw, m in self.log:
            if not m:
                p.append(f'line {lineno}: CYC-8 — log line must read '
                         f'"- <date> [<repo>] <scope> → <what changed>"')
                continue
            low = m.group(4).lower()
            for b in BANNED_LOG:
                if low.startswith(b) or f' {b} ' in f' {low} ':
                    p.append(f'line {lineno}: CYC-8 — {b!r} narrates activity; state the outcome '
                             f'(what changed, what was decided, what surprised you)')
                    break
        return p


def cmd_new(a):
    if not re.match(r'^[A-Za-z0-9][A-Za-z0-9._-]*$', a.id):
        die('cycle id must be filename-safe (letters, digits, dot, dash, underscore)')
    path = doc_path(a.id)
    if os.path.exists(path):
        die(f'{path} already exists — one doc per cycle (CYC-1)')
    for other in find_active():
        die(f'{os.path.basename(other)} is still active. Close it first '
            f'(cycle.py close) — CYC-1 allows one active cycle.')
    start = a.start or datetime.date.today().isoformat()
    # An 8-week cycle: 6 weeks of dev, then 2 of cooldown. The doc covers the dev
    # window only — cooldown is bug-fixing and research, which has no appetite, no
    # no-gos and nothing to put on a hill, so forcing it through intake would be
    # wrong (maintainer's call, 2026-08-19).
    try:
        d0 = datetime.date.fromisoformat(start)
        dev_end = (d0 + datetime.timedelta(weeks=DEV_WEEKS)).isoformat()
        cool_end = (d0 + datetime.timedelta(weeks=DEV_WEEKS + COOLDOWN_WEEKS)).isoformat()
    except ValueError:
        die(f'--start must be YYYY-MM-DD, got {start!r}')
    end = a.end or dev_end
    if a.end and a.end != dev_end:
        print(f'cycle.py: note — dev window from {start} is {DEV_WEEKS} weeks, ending {dev_end}; '
              f'using your {a.end}', file=sys.stderr)
    dates = f'Dates: {start} → {end} · Cooldown: → {cool_end}'
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(f'# Cycle {a.id}\n{dates} · Status: active\n\n## Dev log\n')
    snapshot(state_dir(), '%s: cycle opened' % a.id)
    print(path)
    print('Topics go above "## Dev log" — one "## [repo] name" section each, '
          'shaped per CYC-3 before any scope exists.')


def cmd_active(a):
    hits = find_active()
    if not hits:
        print('no active cycle')
        return 1
    for h in hits:
        print(f'{os.path.splitext(os.path.basename(h))[0]}\t{h}')
    return 0 if len(hits) == 1 else 1


def cmd_validate(a):
    d = Doc(resolve(a.id))
    probs = d.check()
    if not probs:
        print(f'{os.path.basename(d.path)}: conforming — {len(d.topics)} topic(s), '
              f'{sum(len(t["scopes"]) for t in d.topics)} scope(s), {len(d.log)} log line(s)')
        return 0
    print(f'{os.path.basename(d.path)}: {len(probs)} problem(s)')
    for x in probs:
        print(f'  - {x}')
    return 1


def week_of(d):
    """Which week of the dev window today falls in, or the cooldown."""
    m = re.search(r'Dates:\s*(\d{4}-\d{2}-\d{2})', '\n'.join(d.lines[:3]))
    if not m:
        return ''
    try:
        start = datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return ''
    days = (datetime.date.today() - start).days
    if days < 0:
        return 'not started yet'
    wk = days // 7 + 1
    if wk <= DEV_WEEKS:
        return f'week {wk} of {DEV_WEEKS}, dev'
    if wk <= DEV_WEEKS + COOLDOWN_WEEKS:
        return f'cooldown, week {wk - DEV_WEEKS} of {COOLDOWN_WEEKS} (not tracked here)'
    return 'past the cycle end'


def cmd_status(a):
    d = Doc(resolve(a.id))
    where = week_of(d)
    print(f'# Cycle {d.cycle_id} ({d.status})' + (f' — {where}' if where else ''))
    for t in d.topics:
        tags = ''.join(f'[{r}]' for r in t['repos'])
        print(f'\n{tags} {t["name"]}')
        ap = t['fields'].get('Appetite:', '(no appetite)')
        print(f'  appetite: {ap}')
        if not t['scopes']:
            print('  no scopes yet — shape it, then factor into scopes (CYC-5)')
        for s in t['scopes']:
            must = [k for k in s['tasks'] if not k['nice']]
            done = [k for k in must if k['done']]
            nice = [k for k in s['tasks'] if k['nice'] and not k['done']]
            bits = f'{len(done)}/{len(must)} must-have' if must else 'no tasks yet'
            if nice:
                bits += f', {len(nice)} nice-to-have open'
            print(f'  {s["hill"]:<9} {s["name"]}  ({bits})')
        oq = t['fields'].get('Open questions:')
        if oq:
            print(f'  open: {oq}')
    stuck = [(t, s) for t in d.topics for s in t['scopes'] if s['hill'] in ('uphill', 'top')]
    if stuck:
        print(f'\n{len(stuck)} scope(s) not yet downhill — that is where the unknowns are:')
        for t, s in stuck:
            print(f'  {s["hill"]:<9} {t["name"]} › {s["name"]}')
    return 0


def cmd_log(a):
    if a.gate not in GATES:
        die(f'--gate must be one of {", ".join(GATES)} (CYC-8)')
    d = Doc(resolve(a.id))
    if d.status != 'active':
        die(f'cycle {d.cycle_id} is {d.status} — closed docs take no new log lines (CYC-13)')
    text = a.text.strip()
    low = text.lower()
    for b in BANNED_LOG:
        if low.startswith(b):
            die(f'{b!r} narrates activity (CYC-8). State the outcome instead: what changed, '
                f'what was decided, or what surprised you.')
    if PCT.search(text):
        die('no percentages (CYC-6) — move the scope on the hill instead')
    date = a.date or datetime.date.today().isoformat()
    line = f'- {date} [{a.repo}] {a.scope} → {text}'
    if line in d.lines:
        die('that exact line is already in the log')
    scopes = [s['name'] for t in d.topics for s in t['scopes']]
    if scopes and a.scope not in scopes:
        print(f'cycle.py: warning — no scope named {a.scope!r} in this doc '
              f'(have: {", ".join(scopes)})', file=sys.stderr)
    body = '\n'.join(d.lines).rstrip('\n')
    with open(d.path, 'w', encoding='utf-8') as fh:
        fh.write(body + '\n' + line + '\n')
    snapshot(state_dir(), '%s: %s -> %s' % (d.cycle_id, a.scope, text[:60]))
    print(line)
    return 0


def cmd_close(a):
    d = Doc(resolve(a.id))
    if d.status == 'closed':
        die(f'cycle {d.cycle_id} is already closed')
    probs = d.check()
    if probs:
        print('cannot close — the doc has open conformance problems:')
        for x in probs:
            print(f'  - {x}')
        return 1
    missing = [t['name'] for t in d.topics
               if 'Shipped:' not in t['fields'] or 'Cut:' not in t['fields']]
    if missing:
        print('cannot close — CYC-13 needs "Shipped:" and "Cut:" on every topic. Missing on:')
        for m in missing:
            print(f'  - {m}')
        return 1
    signal = [(t, s) for t in d.topics for s in t['scopes'] if s['hill'] in ('uphill', 'top')]
    body = '\n'.join(d.lines).replace('Status: active', 'Status: closed', 1)
    with open(d.path, 'w', encoding='utf-8') as fh:
        fh.write(body)
    shipped = sum(1 for t in d.topics if (t['fields'].get('Shipped:') or '').strip()
                  and 'nothing' not in t['fields']['Shipped:'].lower())
    snapshot(state_dir(), '%s: cycle closed - %d/%d topic(s) shipped'
             % (d.cycle_id, shipped, len(d.topics)))
    print(f'cycle {d.cycle_id} closed — the doc is now read-only (CYC-13)')
    if signal:
        print(f'\nshaping signal: {len(signal)} scope(s) never reached downhill. Not a personal '
              f'failure — it means these were under-shaped at intake (CYC-13):')
        for t, s in signal:
            print(f'  {s["hill"]:<9} {t["name"]} › {s["name"]}')
        print('Carry that into the next intake: these are the topics whose rabbit holes were missed.')
    print('\nNext: hand this closed doc to the sprint-review skill for the retro (CYC-13).')
    return 0


def cmd_snapshot(a):
    d = Doc(resolve(a.id))
    probs = d.check()
    if probs:
        print('not committing a non-conforming doc - fix these first:')
        for x in probs:
            print('  - %s' % x)
        return 1
    snapshot(state_dir(), '%s: %s' % (d.cycle_id, a.why))
    print('committed: %s: %s' % (d.cycle_id, a.why))
    return 0


def cmd_render(a):
    """Render the Notion mirror: body markdown + the derived properties (CYC-10).

    Deterministic on purpose. The model rendering this by hand each time is how
    the body drifts — the first hand-render duplicated Dates/Status in the body
    when the row's properties already carry them.
    """
    d = Doc(resolve(a.id))
    probs = d.check()
    if probs:
        print('not rendering a non-conforming doc - fix these first:')
        for x in probs:
            print('  - %s' % x)
        return 1

    repos = []
    for t in d.topics:
        for r in t['repos']:
            if r not in repos:
                repos.append(r)
    repos.sort()

    out = []
    for repo in repos:
        out.append('## %s' % repo)
        out.append('')
        for t in d.topics:
            if repo not in t['repos']:
                continue
            out.append('### %s' % t['name'])
            out.append('')
            for f in FIELDS + ('Open questions:', 'Shipped:', 'Cut:'):
                if t['fields'].get(f):
                    out.append('%s %s' % (f, t['fields'][f]))
            out.append('')
            for sc in t['scopes']:
                must = [k for k in sc['tasks'] if not k['nice']]
                done = [k for k in must if k['done']]
                nice = [k for k in sc['tasks'] if k['nice'] and not k['done']]
                bits = '%d/%d must-have' % (len(done), len(must)) if must else 'no tasks yet'
                if nice:
                    bits += ', %d nice-to-have open' % len(nice)
                out.append('- **%s** — `%s` (%s)' % (sc['name'], sc['hill'], bits))
            out.append('')
    out.append('## Dev log')
    out.append('')
    out += [raw for _, raw, _ in d.log]
    body = '\n'.join(out).rstrip() + '\n'

    # The header line is deliberately NOT in the body: Dates and Status are row
    # properties, and writing them twice creates two truths in one page (CYC-10).
    dates = re.search(r'Dates:\s*(\S+)\s*(?:→|->)\s*(\S+)', '\n'.join(d.lines[:3]))
    props = {'Name': d.cycle_id,
             'Status': 'In progress' if d.status == 'active' else 'Done'}
    if dates and dates.group(1) not in ('?', ''):
        props['date:Dates:start'] = dates.group(1)
        if dates.group(2) not in ('?', ''):
            props['date:Dates:end'] = dates.group(2)
    props['Repos'] = repos

    if a.json:
        import json as _json
        print(_json.dumps({'properties': props, 'body': body}, ensure_ascii=False, indent=2))
    else:
        print(body)
        print('--- properties (derived, regenerated every mirror) ---')
        for k, v in props.items():
            print('%s: %s' % (k, ', '.join(v) if isinstance(v, list) else v))
        print('\nRepos options must already exist in the database, or Notion rejects the value.')
        print('If it is rejected: skip Repos, tell the maintainer which option to add, mirror the rest.')
    return 0


def cmd_tickets(a):
    """Propose a prioritised work list: Jira-bound tickets and personal tasks.

    Two kinds, because only one belongs in a tracker (maintainer's distinction,
    2026-08-19): implementation work becomes a Jira ticket, while "I need to
    figure this out first" is a task for the maintainer whose outcome is usually
    *producing* the tickets. A research task closing and adding new tasks to its
    scope is normal, not scope creep.

    Ordering is unknowns-first: a task under an `uphill` scope outranks a
    must-have under a `downhill` one, because attacking the unresolved part early
    is what leaves time to react to what it reveals. Nice-to-haves come last.

    The acceptance criteria emitted here are a SCAFFOLD from the topic's outcome
    and done signal. They are meant to be sharpened against the actual code —
    a criterion invented from a topic title is fiction (see SKILL.md, plan flow).
    """
    d = Doc(resolve(a.id))
    rank = {'uphill': 0, 'top': 1, 'downhill': 2, 'done': 3}
    rows = []
    for t in d.topics:
        for sc in t['scopes']:
            for k in sc['tasks']:
                if k['done']:
                    continue
                rows.append({
                    'kind': k['kind'], 'summary': k['text'], 'nice': k['nice'],
                    'topic': t['name'], 'repos': t['repos'], 'scope': sc['name'],
                    'hill': sc['hill'],
                    'outcome': t['fields'].get('Outcome:', ''),
                    'done_when': t['fields'].get('Done when:', ''),
                    'sort': (1 if k['nice'] else 0, rank.get(sc['hill'], 9)),
                })
    rows.sort(key=lambda r: r['sort'])
    for i, r in enumerate(rows, start=1):
        r['priority'] = ('P3' if r['nice'] else
                         'P1' if r['hill'] in ('uphill', 'top') else 'P2')
        r['order'] = i

    if a.json:
        import json as _json
        print(_json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    jira = [r for r in rows if r['kind'] == 'jira']
    mine = [r for r in rows if r['kind'] == 'self']

    if mine:
        print('## Your tasks — not Jira\n')
        for r in mine:
            tags = ''.join('[%s]' % x for x in r['repos'])
            print('%d. %s %s  (%s · scope: %s · %s)' %
                  (r['order'], tags, r['summary'], r['priority'], r['scope'], r['hill']))
            if r['hill'] in ('uphill', 'top'):
                print('   outcome: resolve the unknown, then add the tickets it reveals')
        print()

    print('## Jira tickets — proposed, in this order\n')
    for r in jira:
        tags = ' '.join('[%s]' % x for x in r['repos'])
        print('### %d. %s %s' % (r['order'], tags, r['summary']))
        print('Epic: %s · scope: %s (%s) · %s%s'
              % (r['topic'], r['scope'], r['hill'], r['priority'],
                 ' · nice-to-have' if r['nice'] else ''))
        if r['outcome']:
            print('Why: %s' % r['outcome'])
        if r['done_when']:
            print('Topic done signal: %s' % r['done_when'])
        # Deliberately a placeholder, not a generated criterion. Pasting the topic
        # outcome into every ticket produces text that reads like acceptance
        # criteria and tests nothing — worse than an honest blank, because it
        # looks finished. The model fills these in after reading the code.
        print('Acceptance criteria: TODO — one or two testable statements about THIS change,')
        print('  written after looking at the code. Do not restate the topic outcome.')
        print()

    print('--- %d Jira ticket(s), %d personal task(s). Unknowns first: a task under an uphill scope '
          'outranks a must-have under a downhill one. ---' % (len(jira), len(mine)))
    if not rows:
        print('Nothing open — every task is done, or no tasks exist yet.')
    return 0


def main():
    ap = argparse.ArgumentParser(prog='cycle.py', description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    n = sub.add_parser('new', help='create a cycle doc skeleton')
    n.add_argument('--id', required=True)
    n.add_argument('--start')
    n.add_argument('--end')
    n.set_defaults(fn=cmd_new)

    v = sub.add_parser('active', help='print the active cycle')
    v.set_defaults(fn=cmd_active, id=None)

    c = sub.add_parser('validate', help='check the doc against CYC-2/3/4/6/7/8/9')
    c.add_argument('--id')
    c.set_defaults(fn=cmd_validate)

    s = sub.add_parser('status', help='where every scope sits on the hill')
    s.add_argument('--id')
    s.set_defaults(fn=cmd_status)

    g = sub.add_parser('log', help='append one dev-log line')
    g.add_argument('--repo', required=True)
    g.add_argument('--scope', required=True)
    g.add_argument('--text', required=True)
    g.add_argument('--gate', required=True, choices=GATES,
                   help='which CYC-8 gate this line passes — name it before writing')
    g.add_argument('--date')
    g.add_argument('--id')
    g.set_defaults(fn=cmd_log)

    n2 = sub.add_parser('snapshot', help='commit the doc after a hand-edit (intake, scopes, tasks)')
    n2.add_argument('--why', required=True, help='short reason, becomes the commit message')
    n2.add_argument('--id')
    n2.set_defaults(fn=cmd_snapshot)

    r = sub.add_parser('render', help='render the Notion mirror body + derived properties')
    r.add_argument('--json', action='store_true', help='machine-readable output')
    r.add_argument('--id')
    r.set_defaults(fn=cmd_render)

    k = sub.add_parser('tickets', help='propose a prioritised ticket + task list')
    k.add_argument('--json', action='store_true')
    k.add_argument('--id')
    k.set_defaults(fn=cmd_tickets)

    z = sub.add_parser('close', help='close preflight, then flip status')
    z.add_argument('--id')
    z.set_defaults(fn=cmd_close)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == '__main__':
    main()
