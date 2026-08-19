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
  cycle.py questions [--id ID]
  cycle.py mirrored [--id ID]
  cycle.py reconcile --from <fetched.md> [--id ID]
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
TOPIC_RE = re.compile(r'^## ((?:\[[a-z0-9._-]+\])+)\s+(.+?)(?:\s+[—-]\s*(shaping|shaped))?\s*$')
STATES = ('shaping', 'shaped')
SCOPE_RE = re.compile(r'^### scope:\s*(.+?)\s+[—-]\s*([a-z]+)\s*$')
TASK_RE = re.compile(r'^- \[([ xX])\]\s*(~\s*)?(.+?)\s*$')
LOG_RE = re.compile(r'^- (\d{4}-\d{2}-\d{2})\s+\[([a-z0-9._-]+)\]\s+(.+?)\s+(?:→|->)\s+(.+?)\s*$')
FIELDS = ('Outcome:', 'Appetite:', 'No-gos:', 'Done when:')
EXTRA_FIELDS = ('Open questions:', 'Assumptions:', 'Shipped:', 'Cut:')


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


INTERROGATIVES = ('do', 'does', 'did', 'is', 'are', 'was', 'were', 'will', 'would', 'can',
                  'could', 'should', 'shall', 'who', 'whom', 'whose', 'what', 'which', 'when',
                  'where', 'why', 'how', 'if', 'any', 'has', 'have')


def asks_something(entry):
    """Does this open-question entry actually ask a question?

    A real question often carries its "why this matters" in a trailing clause, so
    the '?' is mid-string or absent: "is Mixpanel still the destination — nothing
    in either repo says where these land". Requiring a trailing '?' rejected six
    good questions and one bad one on first contact with a real doc, so the test
    is instead: a question mark anywhere, or a clause that OPENS with an
    interrogative. Position matters — "This is my assumption" contains "is" but
    starts with "This", and it is exactly the kind of entry this check exists to
    catch.
    """
    if '?' in entry:
        return True
    for clause in re.split(r'[—;.]|,\s+(?=and\b|or\b)', entry):
        words = re.findall(r"[a-zA-Z']+", clause)
        if words and words[0].lower() in INTERROGATIVES:
            return True
    return False


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
                    'name': t.group(2), 'state': t.group(3), 'fields': {},
                    'scopes': [], 'line': i,
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
                for f in FIELDS + EXTRA_FIELDS:
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
            state = t['state']
            if state not in STATES:
                p.append(f'{where}: CYC-3 — topic must declare its state: '
                         f'"## [repo] {t["name"]} — shaping" or "— shaped"')
            ap = t['fields'].get('Appetite:', '')

            if state == 'shaping':
                # A shaping topic is one nobody can spec yet. It needs the budget
                # and the open questions, and NOTHING that requires knowing the
                # answer — demanding an outcome here is what produced a guessed
                # `Outcome: TBD`, the exact untrustworthy file CYC-3 exists to
                # prevent (v1.6.0).
                if not ap:
                    p.append(f'{where}: CYC-3 — a shaping topic still needs an appetite '
                             f'(the budget is a decision, the spec is not)')
                if not t['fields'].get('Open questions:'):
                    p.append(f'{where}: CYC-3 — a shaping topic must carry at least one open '
                             f'question; that is what makes it shaping rather than unstarted')
                for sc in t['scopes']:
                    if sc['hill'] != 'uphill':
                        p.append(f'scope "{sc["name"]}" (line {sc["line"]}): CYC-7 — a shaping '
                                 f'topic\'s scopes are all uphill by definition, got {sc["hill"]!r}')
                    for k in sc['tasks']:
                        if k['kind'] != 'self':
                            p.append(f'line {k["line"]}: CYC-7 — a shaping topic holds only '
                                     f'"self:" research tasks; implementation work needs a shaped '
                                     f'topic (run the shape flow first)')
            else:
                for f in FIELDS:
                    if f not in t['fields'] or not t['fields'][f]:
                        p.append(f'{where}: CYC-3 — missing "{f}"')
                if ap and 'first cut' not in ap.lower():
                    p.append(f'{where}: CYC-4 — no first cut named; add '
                             f'"· First cut: <what goes first>"')
            oq = t['fields'].get('Open questions:', '')
            for q in [x.strip() for x in oq.split('·') if x.strip()]:
                if not asks_something(q):
                    p.append(f'{where}: CYC-3 — open question does not ask anything: {q[:60]!r}. '
                             f'An assumption or a caveat belongs on "Assumptions:"; if it needs an '
                             f'answer, phrase it as the question that would settle it')
            if ap and '(fixed)' not in ap and '(provisional)' not in ap:
                p.append(f'{where}: CYC-4 — appetite must be marked "(fixed)", or '
                         f'"(provisional)" while the topic is still shaping')
            if ap:
                weeks = re.search(r'(\d+(?:\.\d+)?)\s*w', ap, re.I)
                days = re.search(r'(\d+(?:\.\d+)?)\s*d', ap, re.I)
                if weeks and float(weeks.group(1)) > DEV_WEEKS:
                    p.append(f'{where}: CYC-4 — appetite {weeks.group(1)}w exceeds the '
                             f'{DEV_WEEKS}-week dev window; hammer the scope or split the topic')
                elif days and float(days.group(1)) > DEV_WEEKS * 5:
                    p.append(f'{where}: CYC-4 — appetite {days.group(1)}d exceeds the '
                             f'{DEV_WEEKS}-week dev window ({DEV_WEEKS * 5} working days)')
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


def shaping_overrun(d, appetite):
    """Shape Up's circuit breaker, applied to shaping.

    Three weeks of research is not a three-week bet. Past roughly a quarter of the
    appetite with the topic still unshaped, the useful move is to escalate to
    whoever can answer, not to keep researching (v1.6.0).
    """
    m = re.search(r'Dates:\s*(\d{4}-\d{2}-\d{2})', '\n'.join(d.lines[:3]))
    wk = re.search(r'(\d+(?:\.\d+)?)\s*w', appetite or '', re.I)
    dy = re.search(r'(\d+(?:\.\d+)?)\s*d', appetite or '', re.I)
    if not m or not (wk or dy):
        return ''
    try:
        start = datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return ''
    budget = float(wk.group(1)) * 7 if wk else float(dy.group(1)) * 1.4
    spent = (datetime.date.today() - start).days
    if budget and spent > budget * 0.25:
        return ('still shaping after %d of ~%d days of its appetite — escalate to whoever can '
                'answer the open questions rather than researching further' % (spent, int(budget)))
    return ''


def cmd_status(a):
    d = Doc(resolve(a.id))
    where = week_of(d)
    print(f'# Cycle {d.cycle_id} ({d.status})' + (f' — {where}' if where else ''))
    for t in d.topics:
        tags = ''.join(f'[{r}]' for r in t['repos'])
        print(f'\n{tags} {t["name"]}')
        ap = t['fields'].get('Appetite:', '(no appetite)')
        print(f'  state:    {t["state"] or "UNDECLARED"}')
        print(f'  appetite: {ap}')
        if t['state'] == 'shaping':
            warn = shaping_overrun(d, ap)
            if warn:
                print(f'  ⚠ {warn}')
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
    booked = 0.0
    for t in d.topics:
        ap = t['fields'].get('Appetite:', '')
        wk = re.search(r'(\d+(?:\.\d+)?)\s*w', ap or '', re.I)
        dy = re.search(r'(\d+(?:\.\d+)?)\s*d', ap or '', re.I)
        booked += float(wk.group(1)) if wk else (float(dy.group(1)) / 5 if dy else 0)
    if booked:
        left = DEV_WEEKS - booked
        note = ('%.1fw unbooked' % left if left > 0 else
                'OVER-BOOKED by %.1fw — hammer a scope or drop a topic' % -left)
        print('\nbooked: %.1fw of %dw dev window · %s' % (booked, DEV_WEEKS, note))

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
    never_shaped = [t['name'] for t in d.topics if t['state'] == 'shaping']
    signal = [(t, s) for t in d.topics for s in t['scopes'] if s['hill'] in ('uphill', 'top')]
    body = '\n'.join(d.lines).replace('Status: active', 'Status: closed', 1)
    with open(d.path, 'w', encoding='utf-8') as fh:
        fh.write(body)
    shipped = sum(1 for t in d.topics if (t['fields'].get('Shipped:') or '').strip()
                  and 'nothing' not in t['fields']['Shipped:'].lower())
    snapshot(state_dir(), '%s: cycle closed - %d/%d topic(s) shipped'
             % (d.cycle_id, shipped, len(d.topics)))
    print(f'cycle {d.cycle_id} closed — the doc is now read-only (CYC-13)')
    if never_shaped:
        print('\nnever shaped, the whole window: %s' % ', '.join(never_shaped))
        print('This is the strongest shaping signal the system produces — the topic was bet on '
              'before anyone could say what done looked like. Take it to whoever sets the topics.')
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
    return cmd_render_for(Doc(resolve(a.id)), a)


def cmd_render_for(d, a):
    """Render the Notion mirror: body markdown + the derived properties (CYC-10).

    Deterministic on purpose. The model rendering this by hand each time is how
    the body drifts — the first hand-render duplicated Dates/Status in the body
    when the row's properties already carry them.
    """
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

    STATE_ICON = {'shaping': '🔍', 'shaped': '🎯'}
    n_shaping = sum(1 for t in d.topics if t['state'] == 'shaping')
    n_shaped = sum(1 for t in d.topics if t['state'] == 'shaped')
    where = week_of(d)

    # A callout at the top: the two things a human wants on opening the page —
    # where the cycle is, and which parts of this page they may edit.
    out = ['<callout icon="🔁" color="gray_bg">']
    # The id may already say "Cycle" (the maintainer named one "Cycle-11"), and
    # "Cycle Cycle-11" reads like a bug on a page they look at every day.
    label = d.cycle_id if d.cycle_id.lower().startswith('cycle') else 'Cycle %s' % d.cycle_id
    out.append('\t**%s**%s · %d shaping · %d shaped'
               % (label, ' · ' + where if where else '', n_shaping, n_shaped))
    out.append('\tTick tasks here and they sync back. Everything else — fields, appetite, '
               'hill positions, the dev log — is edited locally.')
    out.append('</callout>')
    out.append('')

    for repo in repos:
        out.append('---')
        out.append('')
        out.append('## %s' % repo)
        out.append('')
        for t in d.topics:
            if repo not in t['repos']:
                continue
            icon = STATE_ICON.get(t['state'], '')
            out.append('### %s %s — %s' % (icon, t['name'], t['state'] or 'state undeclared'))
            out.append('')

            # Fields as bold labels rather than "Label:" prose — same information,
            # scannable instead of read line by line.
            for f in FIELDS:
                v = t['fields'].get(f)
                if not v:
                    continue
                if f == 'Appetite:' and '·' in v:
                    # "3w (fixed) · First cut: X" reads better as two labels than as
                    # one line with a lowercase field name buried inside it.
                    head, rest = v.split('·', 1)
                    out.append('**Appetite** %s' % head.strip())
                    cut = rest.strip()
                    if cut.lower().startswith('first cut:'):
                        cut = cut.split(':', 1)[1].strip()
                    out.append('**First cut** %s' % cut)
                else:
                    out.append('**%s** %s' % (f.rstrip(':'), v))
            for f in ('Shipped:', 'Cut:'):
                if t['fields'].get(f):
                    out.append('**%s** %s' % (f.rstrip(':'), t['fields'][f]))
            if t['fields'].get('Assumptions:'):
                out.append('')
                out.append('<callout icon="⚠️" color="yellow_bg">')
                out.append('\t**Assumed, not confirmed** — %s' % t['fields']['Assumptions:'])
                out.append('</callout>')
            out.append('')

            # Open questions were the worst part of the first render: one run-on
            # line joined by "·", which is fine in a parseable file and unreadable
            # on a page. They are the content that matters while a topic is
            # shaping, so they get a real list and a count.
            oq = [x.strip() for x in (t['fields'].get('Open questions:') or '').split('·')
                  if x.strip()]
            if oq:
                out.append('**Open questions** (%d)' % len(oq))
                for q in oq:
                    out.append('- %s' % q)
                out.append('')

            for sc in t['scopes']:
                # Scope as a heading-4: better looking in Notion than a bold line,
                # and unambiguous to parse back (a "**bold** — word" field line
                # could collide, a "#### " prefix cannot).
                out.append('#### %s — `%s`' % (sc['name'], sc['hill']))
                if not sc['tasks']:
                    out.append('*no tasks yet*')
                for k in sc['tasks']:
                    mark = 'x' if k['done'] else ' '
                    pre = '~ ' if k['nice'] else ''
                    kind = 'self: ' if k['kind'] == 'self' else ''
                    out.append('- [%s] %s%s%s' % (mark, pre, kind, k['text']))
                out.append('')

    out.append('---')
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
    shaping = [t['name'] for t in d.topics if t['state'] == 'shaping']
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

    if shaping:
        print('Still shaping: %s — no Jira tickets from these until the topic is shaped. Their '
              'research tasks are above; that IS the work right now.' % ', '.join(shaping))
    print('--- %d Jira ticket(s), %d personal task(s). Unknowns first: a task under an uphill scope '
          'outranks a must-have under a downhill one. ---' % (len(jira), len(mine)))
    if not rows:
        print('Nothing open — every task is done, or no tasks exist yet.')
    return 0


def mirror_snapshot_path(cycle_id):
    d = os.path.join(cycle_home(), '.state')
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, '%s.mirror.md' % cycle_id)


def render_body(d):
    """The mirror body for a doc — same text `render` prints, reused by the snapshot."""
    import io as _io
    import contextlib
    buf = _io.StringIO()

    class _A:
        json = False
        id = None
    with contextlib.redirect_stdout(buf):
        cmd_render_for(d, _A())
    return buf.getvalue().split('--- properties')[0].rstrip() + '\n'


def cmd_mirrored(a):
    """Record what was just written to Notion. Run ONLY after a successful write.

    The snapshot is what makes a later reconcile a 3-way merge instead of a guess:
    without it, a task that is unticked in Notion is indistinguishable from a task
    that was never ticked, and one side silently wins.
    """
    d = Doc(resolve(a.id))
    path = mirror_snapshot_path(d.cycle_id)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(render_body(d))
    print('snapshot recorded: %s' % path)
    return 0


def parse_mirror_tasks(text):
    """{scope: [ {text, done, nice, kind} ]} from a rendered/fetched mirror body."""
    # h4 ONLY. Topic headings are h3 and now end with "— shaping"/"— shaped",
    # so a looser pattern would read a topic as a scope named after it.
    scope_re = re.compile(r'^####\s+(.+?)\s+[—-]\s*`?(\w+)`?\s*$')
    out, cur = {}, None
    for raw in text.split('\n'):
        # Notion escapes brackets on the way out (\[fio\]); undo before matching.
        ln = raw.replace('\\[', '[').replace('\\]', ']').rstrip()
        m = scope_re.match(ln)
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
            continue
        k = TASK_RE.match(ln)
        if k and cur is not None:
            body = k.group(3)
            m_self = SELF_RE.match(body)
            out[cur].append({
                'done': k.group(1).lower() == 'x', 'nice': bool(k.group(2)),
                'kind': 'self' if m_self else 'jira',
                'text': m_self.group(1) if m_self else body,
            })
    return out


def cmd_reconcile(a):
    """Apply the maintainer's Notion-side task edits back into the local doc.

    Three-way: their side (fetched page) and ours (local doc) are each compared
    against the snapshot of what was last mirrored. A change on one side applies; a
    change on both sides of the same task stops for a decision. Nothing about a
    field, an appetite, a hill position or the dev log is ever taken from Notion —
    those need gates or human judgement a text box cannot enforce (CYC-10 v2.0.0).
    """
    import difflib
    d = Doc(resolve(a.id))
    snap_path = mirror_snapshot_path(d.cycle_id)
    if not os.path.isfile(snap_path):
        die(f'no mirror snapshot for {d.cycle_id} — nothing has been mirrored yet, so there is '
            f'nothing to reconcile against. Mirror first, then `mirrored` to record it.')
    theirs = parse_mirror_tasks(read(a.source))
    snap = parse_mirror_tasks(read(snap_path))

    applied, conflicts, ignored, added = [], [], [], []
    lines = list(d.lines)

    def local_tasks(scope_name):
        for t in d.topics:
            for sc in t['scopes']:
                if sc['name'] == scope_name:
                    return sc
        return None

    for scope_name, their_list in theirs.items():
        sc = local_tasks(scope_name)
        if sc is None:
            ignored.append(f'scope {scope_name!r} exists in Notion but not locally — scopes are '
                           f'local-only; add it with the plan flow')
            continue
        snap_list = snap.get(scope_name, [])
        snap_by_text = {k['text']: k for k in snap_list}
        retitled_from = set()   # snapshot texts a retitle consumed — not disappearances
        local_by_text = {k['text']: k for k in sc['tasks']}

        for th in their_list:
            was = snap_by_text.get(th['text'])
            if was is None:
                near = difflib.get_close_matches(th['text'], list(snap_by_text), 1, 0.8)
                if near and near[0] not in {x['text'] for x in their_list}:
                    old = near[0]
                    loc = local_by_text.get(old)
                    if loc is None:
                        # They retitled it in Notion and it was also retitled (or
                        # removed) locally. This is the ONLY real conflict this
                        # reconcile can hit — see the note on booleans below.
                        conflicts.append(f'{scope_name}: {old!r} was retitled to {th["text"]!r} in '
                                         f'Notion but no longer exists under that name locally; '
                                         f'resolve by hand')
                        continue
                    if loc:
                        lines[loc['line'] - 1] = lines[loc['line'] - 1].replace(old, th['text'])
                        retitled_from.add(old)
                        applied.append(f'{scope_name}: retitled {old!r} → {th["text"]!r}')
                        continue
                if th['text'] not in local_by_text:
                    mark = 'x' if th['done'] else ' '
                    pre = '~ ' if th['nice'] else ''
                    kind = 'self: ' if th['kind'] == 'self' else ''
                    insert_at = (sc['tasks'][-1]['line'] if sc['tasks'] else sc['line'])
                    lines.insert(insert_at, '- [%s] %s%s%s' % (mark, pre, kind, th['text']))
                    for t2 in d.topics:
                        for s2 in t2['scopes']:
                            for k2 in s2['tasks']:
                                if k2['line'] > insert_at:
                                    k2['line'] += 1
                    added.append(f'{scope_name}: added {th["text"]!r}')
                continue

            loc = local_by_text.get(th['text'])
            if loc is None:
                ignored.append(f'{scope_name}: {th["text"]!r} was removed locally; not restored')
                continue
            if th['done'] == was['done']:
                continue                      # they didn't change it
            if loc['done'] != was['done']:
                # Both sides moved this checkbox. With a boolean that cannot
                # diverge: if each side changed it away from the snapshot value,
                # both changed it to the same value, so there is nothing to
                # resolve and nothing to write. A done-state conflict is
                # unreachable by construction — conflicts only exist for renames.
                continue
            ln = lines[loc['line'] - 1]
            lines[loc['line'] - 1] = (ln.replace('- [ ]', '- [x]', 1) if th['done']
                                      else ln.replace('- [x]', '- [ ]', 1))
            applied.append(f'{scope_name}: {th["text"]!r} → '
                           f'{"done" if th["done"] else "reopened"}')

        for was_text in snap_by_text:
            if was_text in retitled_from:
                continue
            if was_text not in {x['text'] for x in their_list}:
                ignored.append(f'{scope_name}: {was_text!r} disappeared from Notion; left in place '
                               f'locally (deleting work is never automatic)')

    if conflicts:
        print('CONFLICTS — nothing written. Resolve these first:')
        for c in conflicts:
            print('  ! %s' % c)
        print('\nDecide per task, then re-run. The doc is untouched.')
        return 1

    if not (applied or added):
        print('nothing to reconcile — Notion matches the local doc')
        for i in ignored:
            print('  · %s' % i)
        return 0

    with open(d.path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines).rstrip('\n') + '\n')
    for x in applied + added:
        print('  ✓ %s' % x)
    for i in ignored:
        print('  · %s' % i)

    d2 = Doc(d.path)
    probs = d2.check()
    if probs:
        print('\nWARNING — the reconciled doc no longer validates:')
        for x in probs:
            print('  - %s' % x)
        print('Fix locally; not committed.')
        return 1
    snapshot(cycle_home(), '%s: reconciled from Notion (%d change(s))'
             % (d.cycle_id, len(applied) + len(added)))
    return 0


def cmd_questions(a):
    """Number every open question so answers can be referred to, not re-pasted.

    Stable numbering matters for the shape flow: the maintainer comes back from a
    call able to say "1, 4 and 7 are settled" instead of restating nine questions.
    """
    d = Doc(resolve(a.id))
    total = 0
    for t in d.topics:
        oq = [x.strip() for x in (t['fields'].get('Open questions:') or '').split('·') if x.strip()]
        if not oq and t['state'] != 'shaping':
            continue
        tags = ''.join('[%s]' % r for r in t['repos'])
        print('\n%s %s — %s (%s)' % (tags, t['name'], t['state'] or '?',
                                     t['fields'].get('Appetite:', 'no appetite')))
        if t['fields'].get('Assumptions:'):
            print('  assumed: %s' % t['fields']['Assumptions:'])
        for i, q in enumerate(oq, start=1):
            total += 1
            print('  %d. %s' % (i, q))
        if not oq:
            print('  (none left — this topic may be ready to shape)')
    if total:
        print('\n%d open question(s). Which are answered? Say the numbers per topic; anything '
              'still open stays recorded.' % total)
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

    mk = sub.add_parser('mirrored', help='record the snapshot after a successful Notion write')
    mk.add_argument('--id')
    mk.set_defaults(fn=cmd_mirrored)

    rc = sub.add_parser('reconcile', help='apply Notion-side task edits back into the local doc')
    rc.add_argument('--from', dest='source', required=True,
                    help='file holding the fetched Notion page body')
    rc.add_argument('--id')
    rc.set_defaults(fn=cmd_reconcile)

    q = sub.add_parser('questions', help='list open questions, numbered per topic')
    q.add_argument('--id')
    q.set_defaults(fn=cmd_questions)

    z = sub.add_parser('close', help='close preflight, then flip status')
    z.add_argument('--id')
    z.set_defaults(fn=cmd_close)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == '__main__':
    main()
