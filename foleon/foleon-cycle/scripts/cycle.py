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
import json
import os
import re
import sys

HILLS = ('uphill', 'top', 'downhill', 'done')
DEV_WEEKS = 6          # the bet window: everything shaped must fit here
COOLDOWN_WEEKS = 2     # bug-fixing / research, deliberately NOT tracked in the doc
SELF_RE = re.compile(r'^self\s*:\s*(.+)$', re.I)   # a task for the maintainer, never a Jira ticket

# CYC-15b: a task's kind is carried by the group it sits in, not by a prefix on
# every line. These label lines open each group in the mirror. They are the only
# place the kind is visible, and they are deliberately NOT parsed as content —
# which is what lets them carry a colour the task line never may (CYC-15).
KIND_LABEL = {
    'self': '**Mine — research & decisions, never a ticket**',
    'jira': '**Ticket work — becomes a Jira ticket**',
}
# NST-3's mapping: research is an unknown (orange), ticket work is execution (blue).
KIND_COLOR = {'self': 'orange', 'jira': 'blue'}
# Matched on the leading word rather than the whole label, so rewording a label
# does not orphan every task under it on a page mirrored before the change.
KIND_LABEL_RE = re.compile(r'^\s*\*{0,2}(Mine|Ticket work)\b', re.I)
KIND_ORDER = ('self', 'jira')   # research before execution, as CYC-14 orders the work list
SELF_PREFIX_RE = re.compile(r'^- \[[ xX]\]\s*(?:~\s*)?self\s*:', re.I)
SHAPE_HEAD_RE = re.compile(r'^## .*\bShape \d+: ')
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
EXTRA_FIELDS = ('Open questions:', 'Assumptions:', 'Annex:', 'Shipped:', 'Cut:')

def parse_annexes(raw):
    """Splits an `Annex:` field into (label, url) pairs.

    Written `Annex: <label> → <url> · <label> → <url>`. A malformed entry is
    skipped rather than raising: an annex is a convenience link, and losing one
    must never be able to stop a mirror.
    """
    out = []
    for chunk in (raw or '').split('·'):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = re.split(r'\s+(?:→|->)\s+', chunk, maxsplit=1)
        if len(parts) != 2 or not parts[1].startswith('http'):
            continue
        out.append((parts[0].strip(), parts[1].strip()))
    return out




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
                # CYC-15b: the mirror renders task kind as a group label rather than
                # a `self:` prefix on every line, and the round-trip check compares
                # task ORDER. So the groups have to already be in order here: all
                # research tasks, then all ticket tasks. Reordering at render time
                # instead would make the rendered body stop parsing back to this
                # file, which is the one failure CYC-15 refuses to write through.
                seq = []
                for k in s['tasks']:
                    if not seq or seq[-1] != k['kind']:
                        seq.append(k['kind'])
                if len(seq) != len(set(seq)):
                    p.append(f'scope "{s["name"]}" (line {s["line"]}): CYC-15b — tasks of one kind '
                             f'must be contiguous; the "self:" and Jira tasks are interleaved. '
                             f'Group them: "self:" tasks first, then the rest')
                elif seq and [x for x in KIND_ORDER if x in seq] != seq:
                    p.append(f'scope "{s["name"]}" (line {s["line"]}): CYC-15b — "self:" research '
                             f'tasks come before Jira-bound ones (unknowns first, as CYC-14 orders '
                             f'the work list)')

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

        # CYC-16: an annex is generated from a local sidecar, so a topic whose
        # ticket list has moved on from its annex is a non-conforming doc, not a
        # cosmetic mismatch. Structure only here — the write-up itself is
        # demanded at publish time, so adding a ticket never blocks an unrelated
        # local snapshot.
        p.extend(annex_problems(self))
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
    booked = booked_weeks(d)
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


HILL_BG = {'uphill': 'orange_bg', 'top': 'purple_bg', 'downhill': 'blue_bg', 'done': 'green_bg'}
STATE_ICON = {'shaping': '🔍', 'shaped': '🎯'}
STATE_BG = {'shaping': 'orange_bg', 'shaped': 'blue_bg'}

# The hill as a position on its own track, which is what Shape Up draws: a dot
# somewhere on a curve. Deliberately NOT a fill bar — `▓▓░░` for `top` reads as
# "half done", and the hill measures knowledge, not output (CYC-6). A track shows
# an ordinal position and claims nothing about how much is finished.
HILL_TRACK = {
    'uphill':   '◉ ─ ○ ─ ○ ─ ○',
    'top':      '○ ─ ◉ ─ ○ ─ ○',
    'downhill': '○ ─ ○ ─ ◉ ─ ○',
    'done':     '○ ─ ○ ─ ○ ─ ◉',
}


def bar(weeks, of=None, cells_per_week=2):
    """A proportional bar for an appetite.

    Only ever used for **time**, never for task completion. An appetite is a
    quantity of weeks the maintainer bet, so drawing it to scale is honest. A bar
    over must-haves-done would be the percentage CYC-6 bans wearing a costume:
    it implies the remaining work is known, which is the one thing an uphill
    scope guarantees it is not.
    """
    of = DEV_WEEKS if of is None else of
    full = int(round(weeks * cells_per_week))
    total = int(round(of * cells_per_week))
    full = max(0, min(full, total))
    return '█' * full + '░' * (total - full)


def appetite_weeks(field):
    """One topic's appetite in weeks. A day is a fifth of a week — a five-day week."""
    wk = re.search(r'(\d+(?:\.\d+)?)\s*w', field or '', re.I)
    dy = re.search(r'(\d+(?:\.\d+)?)\s*d', field or '', re.I)
    return float(wk.group(1)) if wk else (float(dy.group(1)) / 5 if dy else 0.0)


def booked_weeks(d):
    """Appetite booked across every topic, in weeks."""
    return sum(appetite_weeks(t['fields'].get('Appetite:', '')) for t in d.topics)


def must_have_line(scope):
    """CYC-10's required must-have completion state, as a count — never a percentage (CYC-6)."""
    must = [k for k in scope['tasks'] if not k['nice']]
    done = [k for k in must if k['done']]
    nice_open = [k for k in scope['tasks'] if k['nice'] and not k['done']]
    if not scope['tasks']:
        return 'no tasks yet — the steps are not discovered'
    bits = '**%d of %d** must-haves' % (len(done), len(must)) if must else 'no must-haves'
    if nice_open:
        bits += ' · %d nice-to-have open' % len(nice_open)
    return bits


def cell(s):
    """Table cells take rich text only; the angle brackets are what would break the XML."""
    return (s or '').replace('<', '\\<').replace('>', '\\>')


def roundtrip_problems(d, body):
    """CYC-15's enforcement: does the rendered body parse back to the local doc?

    The mirror is a writable surface (CYC-10 v2.0.0), so `reconcile` reads scope
    headings and task lines straight back out of it and a task's text wins. Any
    styling that leaks into one of those lines therefore *rewrites the doc* on the
    next reconcile. Checking it here rather than in a test is deliberate: render
    is the only write path, so a body that fails this can never reach Notion.
    """
    parsed = parse_mirror_tasks(body)
    probs = []
    for t in d.topics:
        for s in t['scopes']:
            if s['name'] not in parsed:
                probs.append('scope %r does not parse back out of the render — every task under it '
                             'would be reported as missing from Notion' % s['name'])
                continue
            mine = [(k['text'], k['done'], k['nice'], k['kind']) for k in s['tasks']]
            theirs = [(k['text'], k['done'], k['nice'], k['kind']) for k in parsed[s['name']]]
            if mine == theirs:
                continue
            for a, b in zip(mine, theirs):
                if a != b:
                    probs.append('task under %r round-trips as %r, not %r' % (s['name'], b[0], a[0]))
            if len(mine) != len(theirs):
                probs.append('scope %r has %d task(s) locally and %d in the render'
                             % (s['name'], len(mine), len(theirs)))
    return probs


def layout_problems(body, repos, n_topic_headings):
    """CYC-15a's enforcement: does the rendered body have the page shape the standard fixes?

    Same fail-closed contract as `roundtrip_problems`: checked in the write path,
    not in a test, because `render` is the only way a body reaches Notion. The
    checks are structural on purpose — a heading level or a missing orientation
    line is exactly the kind of regression that survives review by looking fine.
    """
    lines = body.split('\n')
    probs = []

    first = next((l for l in lines if l.strip()), '')
    if first != '# Preview':
        probs.append('the page must open with "# Preview" (CYC-15a), got %r' % first[:40])

    want = ['# Preview'] + ['# %s' % r for r in repos] + ['# Dev log']
    got = [l for l in lines if l.startswith('# ')]
    if got != want:
        probs.append('page sections are %r, expected %r (CYC-15a)' % (got, want))

    for i, l in enumerate(lines, start=1):
        if l.startswith('### ') and not l.startswith('#### '):
            probs.append('line %d: "###" is unused on this page — scopes are "####" and topics '
                         '"##" (CYC-15a): %r' % (i, l[:40]))
        if SELF_PREFIX_RE.match(l):
            probs.append('line %d: a task line renders a "self:" prefix; kind is a group label '
                         '(CYC-15b): %r' % (i, l[:60]))

    n = sum(1 for l in lines if SHAPE_HEAD_RE.match(l))
    if n != n_topic_headings:
        probs.append('%d "## <icon> Shape N: <name>" headings, expected %d (CYC-15a)'
                     % (n, n_topic_headings))

    # Every page section states what it is before its first block (NST-11). A
    # callout counts — for Preview the header callout IS the orientation, and a
    # grey line under it would say the same thing twice.
    for i, l in enumerate(lines):
        if not l.startswith('# '):
            continue
        after = [x for x in lines[i + 1:i + 4] if x.strip()]
        if not after or not (after[0].startswith('<callout')
                             or after[0].rstrip().endswith('{color="gray"}')):
            probs.append('section %r has no orientation line under it (CYC-15a, NST-11)' % l[:40])
    return probs


def cmd_render_for(d, a):
    """Render the Notion mirror: body markdown + the derived properties (CYC-10).

    Deterministic on purpose. The model rendering this by hand each time is how
    the body drifts — the first hand-render duplicated Dates/Status in the body
    when the row's properties already carry them.

    The visual contract is CYC-15: the four questions the doc answers must be
    answerable without scrolling, so the hill board comes first, the outcome is
    the loudest thing in a topic, and the constraints recede into grey. Two
    CYC-15a fixes the page's sections (`#` Preview / project / Dev log, topics as
    `## <icon> Shape N: <name>`) and CYC-15b moves task kind onto a group label,
    both asserted before the write by `layout_problems`. Two
    things are deliberately NOT styled — the scope h4 and the task lines — since
    both are parsed back out of Notion by `reconcile` (a `{color=}` swallowed
    into a task's text would rewrite the task, and task text is authoritative
    from Notion).
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

    n_shaping = sum(1 for t in d.topics if t['state'] == 'shaping')
    n_shaped = sum(1 for t in d.topics if t['state'] == 'shaped')
    where = week_of(d)

    # A callout at the top: where the cycle is, how much of the window is bet,
    # and which parts of this page the maintainer may edit. Purple because it is
    # the maintainer's own accent and this is the one block that is about them
    # rather than about the work.
    # Page-level sections at `#` (CYC-15a): Preview, one per project, Dev log.
    # Before this the top half of the page was three unframed blocks and the
    # reader had to infer the page's shape from its contents.
    out = ['# Preview', '']
    out.append('<callout icon="🔁" color="purple_bg">')
    # The id may already say "Cycle" (the maintainer named one "Cycle-11"), and
    # "Cycle Cycle-11" reads like a bug on a page they look at every day.
    label = d.cycle_id if d.cycle_id.lower().startswith('cycle') else 'Cycle %s' % d.cycle_id
    out.append('\t**%s**%s · %d shaped · %d shaping'
               % (label, ' · ' + where if where else '', n_shaped, n_shaping))
    booked = booked_weeks(d)
    if booked:
        left = DEV_WEEKS - booked
        note = ('%.1fw unbooked' % left if left > 0
                else '**over-booked by %.1fw** — hammer a scope or drop a topic' % -left)
        out.append('\t`%s`  **%.1fw** of %dw dev window booked · %s'
                   % (bar(booked), booked, DEV_WEEKS, note))
    out.append('\tTick tasks here and they sync back. Everything else — fields, appetite, '
               'hill positions, the dev log — is edited locally.')
    out.append('</callout>')
    out.append('')

    # The hill board. The whole reason the hill exists is to answer "where are the
    # unknowns" at a glance, and it could not do that when it rendered as an
    # inline code chip three screens down. One table, every scope, colour and a
    # position track — this is the first thing on the page after the header.
    board = [(t, s) for t in d.topics for s in t['scopes']]
    if board:
        out.append('## Where the work stands')
        out.append('')
        out.append('<table fit-page-width="true" header-row="true">')
        out.append('\t<tr><td>**Scope**</td><td>**Topic**</td><td>**Hill**</td>'
                   '<td>**uphill → done**</td><td>**Must-haves**</td></tr>')
        for t, s in board:
            must = [k for k in s['tasks'] if not k['nice']]
            done = [k for k in must if k['done']]
            tally = '%d of %d' % (len(done), len(must)) if must else '—'
            out.append('\t<tr><td>%s</td><td>%s</td><td color="%s">**%s**</td>'
                       '<td color="%s">`%s`</td><td>%s</td></tr>'
                       % (cell(s['name']), cell(t['name']),
                          HILL_BG.get(s['hill'], 'gray_bg'), s['hill'],
                          HILL_BG.get(s['hill'], 'gray_bg'),
                          HILL_TRACK.get(s['hill'], '?'), tally))
        out.append('</table>')
        out.append('')
        stuck = [x for x in board if x[1]['hill'] in ('uphill', 'top')]
        if stuck:
            out.append('%d of %d scopes are not yet downhill — that is where the unknowns are, and '
                       'that is what to attack first. {color="gray"}' % (len(stuck), len(board)))
            out.append('')

    # The bet, to scale. "How much time is it worth" is one of the four questions
    # and it was only ever answerable by reading three topics and adding up. A
    # bar over *time* is honest in a way a bar over task completion would not be
    # — see `bar()`.
    if d.topics:
        out.append('## The bet')
        out.append('')
        out.append('<table fit-page-width="true" header-row="true">')
        out.append('\t<tr><td>**Topic**</td><td>**Appetite**</td>'
                   '<td>**against the %dw window**</td><td>**State**</td></tr>' % DEV_WEEKS)
        for t in d.topics:
            ap = t['fields'].get('Appetite:', '') or ''
            head = ap.split('·', 1)[0].strip()
            wks = appetite_weeks(ap)
            out.append('\t<tr><td>%s</td><td>%s</td><td>`%s`</td><td color="%s">%s %s</td></tr>'
                       % (cell(t['name']), cell(head) or '—', bar(wks),
                          STATE_BG.get(t['state'], 'gray_bg'),
                          STATE_ICON.get(t['state'], ''), t['state'] or 'undeclared'))
        left = DEV_WEEKS - booked
        if left > 0:
            out.append('\t<tr><td>*unbooked*</td><td>*%.1fw*</td><td>`%s`</td><td>—</td></tr>'
                       % (left, bar(left)))
        out.append('</table>')
        out.append('')

        # Notion renders mermaid natively in a code block. Only the appetite is
        # charted, because it is the one quantity in this doc that IS a quantity —
        # the hill is four ordinal stops and any chart of it needs a second axis
        # nobody stated, which is inference (CYC-6).
        if booked:
            out.append('```mermaid')
            out.append('xychart-beta')
            out.append('    title "Appetite against the %dw dev window"' % DEV_WEEKS)
            labels, values = [], []
            for t in d.topics:
                nm = t['name'].replace('"', '')
                labels.append('"%s"' % (nm if len(nm) <= 22 else nm[:21].rstrip() + '…'))
                values.append('%g' % appetite_weeks(t['fields'].get('Appetite:', '')))
            if left > 0:
                labels.append('"unbooked"')
                values.append('%g' % left)
            out.append('    x-axis [%s]' % ', '.join(labels))
            out.append('    y-axis "weeks" 0 --> %d' % DEV_WEEKS)
            out.append('    bar [%s]' % ', '.join(values))
            out.append('```')
            out.append('')

    # A shape's number is its position in the doc, counted across the whole cycle
    # so "Shape 2" is unambiguous on a multi-project page. Derived only: it
    # renumbers the moment a topic is added or split, which is why CYC-15a forbids
    # using it as an identifier anywhere outside this page.
    shape_no = {id(t): n for n, t in enumerate(d.topics, start=1)}
    n_topic_headings = sum(1 for r in repos for t in d.topics if r in t['repos'])

    for repo in repos:
        mine = [t for t in d.topics if repo in t['repos']]
        scopes = [sc for t in mine for sc in t['scopes']]
        stuck_here = [sc for sc in scopes if sc['hill'] in ('uphill', 'top')]
        weeks = sum(appetite_weeks(t['fields'].get('Appetite:', '')) for t in mine)
        out.append('---')
        out.append('')
        out.append('# %s' % repo)
        out.append('')
        # Derived counts only. A sentence about what the repo *is* would have to be
        # composed here, and an invented gloss reads like a fact (CYC-15a) — if one
        # is ever wanted it gets quoted from that repo's project-context skill.
        out.append('%d shape%s · %d scope%s, %d not yet downhill · %.1fw of the %dw window '
                   '{color="gray"}'
                   % (len(mine), '' if len(mine) == 1 else 's',
                      len(scopes), '' if len(scopes) == 1 else 's',
                      len(stuck_here), weeks, DEV_WEEKS))
        out.append('')
        for t in mine:
            icon = STATE_ICON.get(t['state'], '')
            # Numbered, because three shapes rendered as three bare titles read as
            # one column. Colon-separated, not em-dash: topic names contain em
            # dashes already ("GTM analytics — plumbing") and "Shape 1 — GTM
            # analytics — plumbing" is unreadable (CYC-15a).
            out.append('## %s Shape %d: %s' % (icon, shape_no[id(t)], t['name']))
            out.append('')

            oq = [x.strip() for x in (t['fields'].get('Open questions:') or '').split('·')
                  if x.strip()]

            if t['state'] == 'shaped':
                # The outcome is the one sentence that decides whether everything
                # under it is the right work, so it gets the loudest block on the
                # page. Done-when rides with it: same question, other end.
                out.append('<callout icon="🎯" color="blue_bg">')
                if t['fields'].get('Outcome:'):
                    out.append('\t**Outcome** — %s' % t['fields']['Outcome:'])
                if t['fields'].get('Done when:'):
                    out.append('\t**Done when** — %s' % t['fields']['Done when:'])
                out.append('</callout>')
                out.append('')
            else:
                out.append('<callout icon="🔍" color="orange_bg">')
                out.append('\t**Still shaping** — %s. No outcome or done signal yet, on purpose '
                           '(CYC-3).'
                           % ('%d open question%s' % (len(oq), '' if len(oq) == 1 else 's')
                              if oq else 'the questions are not written down yet'))
                warn = shaping_overrun(d, t['fields'].get('Appetite:', ''))
                if warn:
                    out.append('\t⚠️ %s' % warn)
                out.append('</callout>')
                out.append('')

            # Constraints recede: same information, grey, below the outcome. What
            # the topic IS should outrank what it is not.
            ap = t['fields'].get('Appetite:') or ''
            cut = ''
            if '·' in ap:
                ap, rest = [x.strip() for x in ap.split('·', 1)]
                cut = rest.split(':', 1)[1].strip() if rest.lower().startswith('first cut:') else rest
            if ap:
                out.append('**Appetite** %s · %s {color="gray"}' % (ap, t['state'] or 'state undeclared'))
            if cut:
                out.append('**First cut** %s {color="gray"}' % cut)
            for f in ('No-gos:', 'Shipped:', 'Cut:'):
                if t['fields'].get(f):
                    out.append('**%s** %s {color="gray"}' % (f.rstrip(':'), t['fields'][f]))
            out.append('')

            if t['fields'].get('Assumptions:'):
                out.append('<callout icon="⚠️" color="yellow_bg">')
                out.append('\t**Assumed, not confirmed** — %s' % t['fields']['Assumptions:'])
                out.append('</callout>')
                out.append('')

            # Open questions are the content of a shaping topic, so they stay
            # expanded — but numbered, to match `cycle.py questions`. That makes
            # "3 and 5 are settled" a sentence the maintainer can say straight off
            # this page.
            if oq:
                out.append('**Open questions** (%d)' % len(oq))
                for n, q in enumerate(oq, start=1):
                    out.append('%d. %s' % (n, q))
                out.append('')

            for sc in t['scopes']:
                # Scope as a heading-4: better looking in Notion than a bold line,
                # and unambiguous to parse back (a "**bold** — word" field line
                # could collide, a "#### " prefix cannot). Left uncoloured on
                # purpose — this line is `reconcile`'s scope key, and an attribute
                # list on it is one more thing the round-trip can mangle. The hill
                # gets its colour in the board above instead.
                out.append('#### %s — `%s`' % (sc['name'], sc['hill']))
                out.append('%s {color="gray"}' % must_have_line(sc))
                # CYC-15b: the kind is a group, not a prefix. `self:` on forty
                # consecutive lines spent forty lines conveying a grouping the eye
                # can read for free — and the obvious fix, a colour on the
                # checkbox, is the one thing CYC-15 forbids, because that
                # attribute becomes the task's text on the next read. The label
                # line takes the colour instead: nothing parses it back. Groups
                # are emitted in file order (validate guarantees they are already
                # contiguous and research-first) so the round-trip stays exact.
                last = None
                for k in sc['tasks']:
                    if k['kind'] != last:
                        out.append('')
                        out.append('%s {color="%s"}'
                                   % (KIND_LABEL.get(k['kind'], KIND_LABEL['jira']),
                                      KIND_COLOR.get(k['kind'], 'blue')))
                        last = k['kind']
                    mark = 'x' if k['done'] else ' '
                    pre = '~ ' if k['nice'] else ''
                    # Deliberately unstyled: this line comes back from Notion and
                    # its text wins, so anything appended here would become part
                    # of the task on the next reconcile.
                    out.append('- [%s] %s%s' % (mark, pre, k['text']))
                out.append('')

            # Annexes render once per topic, directly under its last scope's
            # tasks — the point in the page where the reader has just seen the
            # ticket lines and wants the write-up behind them. Grey and plain:
            # `reconcile` reads scope headings and task lines, so a link line
            # sitting between them must not look like either.
            for label, url in parse_annexes(t['fields'].get('Annex:')):
                out.append('📎 **Annex** — [%s](%s) {color="gray"}' % (label, url))
            if t['fields'].get('Annex:'):
                out.append('')

    out.append('---')
    out.append('')
    out.append('# Dev log')
    out.append('')
    dates = sorted(m.group(1) for _, _, m in d.log if m)
    span = ''
    if dates:
        span = ' · %s' % dates[0] if dates[0] == dates[-1] else ' · %s → %s' % (dates[0], dates[-1])
    out.append('%d entr%s%s {color="gray"}'
               % (len(d.log), 'y' if len(d.log) == 1 else 'ies', span))
    out.append('')
    if d.log:
        # A flat bullet list was fine at four lines and unreadable at forty. The
        # date and the scope are what you scan by, so they get their own columns.
        out.append('<table fit-page-width="true" header-row="true">')
        out.append('\t<tr><td>**When**</td><td>**Scope**</td><td>**What changed**</td></tr>')
        for _, raw, m in d.log:
            if m:
                out.append('\t<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
                           % (m.group(1), cell('%s › %s' % (m.group(2), m.group(3))),
                              cell(m.group(4))))
            else:
                out.append('\t<tr><td>—</td><td>—</td><td>%s</td></tr>'
                           % cell(raw.strip().lstrip('- ')))
        out.append('</table>')
    else:
        out.append('*nothing logged yet*')
    body = '\n'.join(out).rstrip() + '\n'

    lay = layout_problems(body, repos, n_topic_headings)
    if lay:
        print('render aborted — the page layout does not conform (CYC-15a/CYC-15b):')
        for x in lay:
            print('  - %s' % x)
        return 1

    rt = roundtrip_problems(d, body)
    if rt:
        print('render aborted — the body does not parse back to the local doc (CYC-15).')
        print('Writing it would let the next reconcile rewrite the doc from a mangled read:')
        for x in rt:
            print('  - %s' % x)
        return 1

    # The header line is deliberately NOT in the body: Dates and Status are row
    # properties, and writing them twice creates two truths in one page (CYC-10).
    hdr = re.search(r'Dates:\s*(\S+)\s*(?:→|->)\s*(\S+)', '\n'.join(d.lines[:3]))
    props = {'Name': d.cycle_id,
             'Status': 'In progress' if d.status == 'active' else 'Done'}
    if hdr and hdr.group(1) not in ('?', ''):
        props['date:Dates:start'] = hdr.group(1)
        if hdr.group(2) not in ('?', ''):
            props['date:Dates:end'] = hdr.group(2)
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
    # An annex is generated output and is never read back, so its snapshot is
    # not a merge base — it is the record of what the page currently says, which
    # is what makes "the annex is stale" answerable without fetching Notion.
    for t in d.topics:
        for label, url, apath, ax in topic_annexes(d, t):
            if ax is None or annex_problems(d, strict=True):
                continue
            sp = annex_snapshot_path(d.cycle_id, label)
            with open(sp, 'w', encoding='utf-8') as fh:
                fh.write(render_annex(d, t, label, url, ax))
            print('snapshot recorded: %s' % sp)
    return 0


# Notion silently autolinks anything that looks like a domain, so a task
# mentioning `docs/observability/gtm.md` comes back as
# `docs/observability/[gtm.md](http://gtm.md)`. Left alone that reads as a
# retitle (difflib matches it at >0.8) and the autolink gets written into the
# local doc as the task's new text. Only unwrap where the URL is the link text
# with a scheme bolted on — that is the autolink signature, and it leaves a
# link the maintainer actually typed untouched.
AUTOLINK_RE = re.compile(r'\[([^\]]+)\]\(https?://(?:www\.)?([^)]+)\)')


def unautolink(s):
    return AUTOLINK_RE.sub(lambda m: m.group(1) if m.group(2).rstrip('/') == m.group(1) else m.group(0), s)


def parse_mirror_tasks(text):
    """{scope: [ {text, done, nice, kind} ]} from a rendered/fetched mirror body."""
    # h4 ONLY. Topic headings are h3, so a looser pattern would read a topic as a
    # scope named after it. A trailing attribute list is tolerated in case a
    # future render or Notion's round-trip puts one here — CYC-15 forbids the
    # renderer from doing it, and this is the belt to that braces.
    scope_re = re.compile(r'^####\s+(.+?)\s+[—-]\s*`?(\w+)`?(?:\s*\{[^}]*\})?\s*$')
    out, cur, kind = {}, None, None
    for raw in text.split('\n'):
        # Notion escapes brackets on the way out (\[fio\]); undo before matching.
        ln = unautolink(raw.replace('\\[', '[').replace('\\]', ']')).rstrip()
        m = scope_re.match(ln)
        if m:
            cur = m.group(1)
            kind = None      # a group label never carries across a scope boundary
            out.setdefault(cur, [])
            continue
        lb = KIND_LABEL_RE.match(ln)
        if lb and cur is not None:
            # CYC-15b: the kind lives on the group label now. A task the
            # maintainer types under a label inherits that label's kind, which is
            # the behaviour they'd expect from where they put it.
            kind = 'self' if lb.group(1).lower().startswith('mine') else 'jira'
            continue
        k = TASK_RE.match(ln)
        if k and cur is not None:
            body = k.group(3)
            # An inline `self:` is still honoured: it is the local file's syntax
            # (CYC-7) and the maintainer may well type it into Notion by hand. A
            # task above any label falls back to CYC-7's default, Jira-bound.
            m_self = SELF_RE.match(body)
            out[cur].append({
                'done': k.group(1).lower() == 'x', 'nice': bool(k.group(2)),
                'kind': 'self' if m_self else (kind or 'jira'),
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
                    # Land it at the end of its OWN kind group, not the end of the
                    # scope. CYC-15b requires the kinds to stay contiguous, and the
                    # re-validate below would otherwise reject the maintainer's own
                    # added task — a task typed into Notion must never be the thing
                    # that makes the doc non-conforming.
                    same = [k for k in sc['tasks'] if k['kind'] == th['kind']]
                    if same:
                        insert_at = same[-1]['line']
                    elif th['kind'] == 'self' and sc['tasks']:
                        insert_at = sc['tasks'][0]['line'] - 1   # research group goes first
                    else:
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



# ---------------------------------------------------------------------------
# Annexes (CYC-16)
# ---------------------------------------------------------------------------
#
# An annex is a supporting document for one topic — a ticket write-up, a list of
# questions for a call. Until v3.0.0 of the standard it was hand-authored
# straight into Notion and merely linked from the cycle doc, which meant it went
# stale the moment a ticket was added and nothing could tell: the maintainer hit
# exactly that, an annex still saying "Three tickets" over a topic that had four.
#
# So an annex is now generated output like the cycle page itself. Its content
# lives in a local sidecar file beside the cycle doc, one section per Jira-bound
# task, and `validate` fails while the doc and the sidecar disagree about which
# tickets exist. The prose is still written by a human or an agent reading the
# code — CYC-14 forbids generating acceptance criteria, and a generated write-up
# would be exactly the filler that rule exists to prevent. What is enforced is
# the structure, the coverage and the links; never the words.

ANNEX_HEAD_RE = re.compile(r'^# Annex:\s*(.+?)\s*$')
ANNEX_META_RE = re.compile(r'^Cycle:\s*(\S+)\s*·\s*Topic:\s*(.+?)\s*$')
ANNEX_SECTION_RE = re.compile(r'^##\s+(.+?)\s*$')
ANNEX_TASK_RE = re.compile(r'^Task:\s*(.+?)\s*$')
# The Jira summary to paste into the tracker. The section heading is written for
# a reader of this page; a Jira ticket is read in a list of forty, out of context,
# so it gets its own line rather than reusing the heading.
ANNEX_JIRA_RE = re.compile(r'^###\s*Jira ticket name:\s*(.*?)\s*$', re.I)
ANNEX_JIRA_TODO = 'TODO — a short imperative summary, readable out of context in a Jira list'

# CYC-17: a ticket write-up is a fixed set of slots, in a fixed order.
#
# Before this, a section was free prose and every ticket invented its own shape.
# The maintainer pasted the first one into Jira and deleted most of it: a bullet
# list of "what to build" that stated implementation steps without saying why
# any of them were there, which reads as noise to whoever picks the ticket up.
# So the slots are the ones a ticket is actually read for — what it must achieve,
# what it must respect, when it is done, and what proves it — and the checklist
# of steps is gone, because the annex is not a design document.
#
# Required slots are required because a ticket missing one cannot be worked:
# no outcome is no ticket, no criteria is unfalsifiable, and unstated testing is
# how "expected testing: none" gets decided silently by whoever is in a hurry.
# The rest are conditional and simply omitted when they do not apply — an empty
# slot header is worse than an absent one, for CYC-14's reason.
ANNEX_SLOTS = [
    ('Expected outcome', True),
    ('Environment', False),
    ('Parameters', False),
    ('Open questions', False),
    ('Done when', True),
    ('Criteria', True),
    ('Lives under', False),
    ('Expected testing', True),
]
# Slots whose content is a bullet list rather than inline prose. `Parameters` is
# a set of independent constraints, and running them together behind `·` makes
# the reader do the separating that punctuation should have done for them.
ANNEX_LIST_SLOTS = {'Parameters'}
ANNEX_SLOT_NAMES = [n for n, _ in ANNEX_SLOTS]
ANNEX_SLOT_REQUIRED = [n for n, r in ANNEX_SLOTS if r]
ANNEX_SLOT_RE = re.compile(r'^\*\*(%s)\*\*\s*(.*)$' % '|'.join(
    re.escape(n) for n in ANNEX_SLOT_NAMES))
# `Done when` and `Criteria` are two slots, not two lines inside one. They answer
# different questions — "how do I know I am finished" and "what would fail if I
# were not" — and nesting the second inside the first buried it.

# The one marker a stub must lose before the annex may be published. Deliberately
# not subtle: it has to be obvious in the file that nobody wrote this.
ANNEX_STUB_MARK = 'TODO — write this from the code'
ANNEX_STUB = '\n'.join([
    '**Expected outcome** — %s (references/tickets.md): what this ticket must achieve, observable from outside.' % ANNEX_STUB_MARK,
    '**Done when** — %s: the one-sentence signal that it is finished.' % ANNEX_STUB_MARK,
    '**Criteria** — %s: testable statements about THIS change, never the topic outcome (CYC-14).' % ANNEX_STUB_MARK,
    '**Expected testing** — %s: which tests, at which level, or "none" if none.' % ANNEX_STUB_MARK,
])
ANNEX_STUB_JIRA = '### Jira ticket name: ' + ANNEX_JIRA_TODO


def slot_problems(section):
    """CYC-17 conformance for one ticket-bound section: the required slots are
    present, non-empty, unduplicated and in the standard's order, and the ones
    that are lists are written as lists.

    Order is enforced rather than merely recommended because the value of a
    fixed shape is that a reader finds the same thing in the same place across
    forty tickets; a section that carries every slot in its own order defeats
    exactly that.
    """
    p = []
    seen = []
    for raw in section['body']:
        m = ANNEX_SLOT_RE.match(raw.strip())
        if not m:
            continue
        name, rest = m.group(1), m.group(2).strip(' —-·')
        if name in [x[0] for x in seen]:
            p.append('slot "%s" appears twice' % name)
            continue
        seen.append((name, rest.strip()))
    have = [n for n, _ in seen]
    for name in ANNEX_SLOT_REQUIRED:
        if name not in have:
            p.append('no "**%s**" slot' % name)
    order = [ANNEX_SLOT_NAMES.index(n) for n in have if n in ANNEX_SLOT_NAMES]
    if order != sorted(order):
        p.append('slots are out of order — the standard\'s order is: %s'
                 % ' · '.join(ANNEX_SLOT_NAMES))

    def content_after(name):
        """The lines belonging to a slot: everything up to the next slot header."""
        run = []
        hit = False
        for raw in section['body']:
            m = ANNEX_SLOT_RE.match(raw.strip())
            if m:
                if m.group(1) == name:
                    hit = True
                    continue
                if hit:
                    break
                continue
            if hit:
                run.append(raw)
        return run

    for name, rest in seen:
        run = [x for x in content_after(name) if x.strip()]
        if name in ANNEX_LIST_SLOTS:
            if rest:
                p.append('slot "%s" is a list — put its items on "- " lines under the header, '
                         'not inline' % name)
            elif not run:
                p.append('slot "%s" is empty — omit it rather than leaving a header' % name)
            elif [x for x in run if not x.strip().startswith('- ')]:
                p.append('slot "%s" is a list — every line under it must start with "- "' % name)
        elif not rest and not run:
            p.append('slot "%s" is empty — omit it rather than leaving a header' % name)
    return p


def annex_slug(label):
    """Filename-safe key for an annex label.

    The label in the doc's `Annex:` line is the identity; this is only how it
    reaches the filesystem. Renaming a label therefore orphans its sidecar — on
    purpose, and loudly: `validate` reports the missing file rather than
    silently starting a second one.
    """
    s = re.sub(r'[^a-z0-9]+', '-', (label or '').lower()).strip('-')
    return s or 'annex'


def annex_path(cycle_id, label):
    return os.path.join(state_dir(), '%s.annex.%s.md' % (cycle_id, annex_slug(label)))


def jira_tasks(topic):
    """Every Jira-bound task under a topic, in doc order.

    Includes done ones and `~` nice-to-haves: a shipped ticket still needs its
    write-up findable, and a nice-to-have that gets built needs one too.
    """
    out = []
    for sc in topic['scopes']:
        for k in sc['tasks']:
            if k['kind'] == 'jira':
                out.append({'text': k['text'], 'scope': sc['name'], 'hill': sc['hill'],
                            'done': k['done'], 'nice': k['nice']})
    return out


class Annex:
    """Parsed view of an annex sidecar.

    Line 1 is `# Annex: <label>`, matching the doc's `Annex:` line exactly.
    Line 2 is `Cycle: <id> · Topic: <topic name>`.
    Anything before the first `##` is shared background, rendered as written.
    A `##` section is ticket-bound when its first non-blank line is `Task: <the
    task text, verbatim from the cycle doc>`; every other section (background,
    an ordering note) is free-form and carries no `Task:` line.
    """

    def __init__(self, path):
        self.path = path
        self.lines = read(path).split('\n')
        self.label = None
        self.cycle_id = None
        self.topic = None
        self.preamble = []
        self.sections = []      # {title, task, line, body[]}
        self.problems = []
        self._parse()

    def _parse(self):
        m = ANNEX_HEAD_RE.match(self.lines[0] if self.lines else '')
        if m:
            self.label = m.group(1)
        else:
            self.problems.append('CYC-16: line 1 of %s must be "# Annex: <label>"'
                                 % os.path.basename(self.path))
        for ln in self.lines[1:4]:
            mm = ANNEX_META_RE.match(ln)
            if mm:
                self.cycle_id, self.topic = mm.group(1), mm.group(2)
                break
        if self.topic is None:
            self.problems.append('CYC-16: %s must carry "Cycle: <id> · Topic: <topic name>" '
                                 'in its first lines' % os.path.basename(self.path))

        cur = None
        for i, raw in enumerate(self.lines, start=1):
            if i <= 2:
                continue
            s = ANNEX_SECTION_RE.match(raw)
            if s:
                cur = {'title': s.group(1), 'task': None, 'jira': None, 'line': i, 'body': []}
                self.sections.append(cur)
                continue
            if cur is None:
                self.preamble.append(raw)
                continue
            t = ANNEX_TASK_RE.match(raw)
            if t and cur['task'] is None and not [x for x in cur['body'] if x.strip()]:
                cur['task'] = t.group(1)
                continue
            j = ANNEX_JIRA_RE.match(raw)
            if j and cur['jira'] is None:
                cur['jira'] = j.group(1)
            cur['body'].append(raw)

    @property
    def ticket_sections(self):
        return [s for s in self.sections if s['task'] is not None]

    def stubs(self):
        out = []
        for s in self.ticket_sections:
            body = '\n'.join(s['body'])
            written = [x for x in s['body'] if x.strip() and not ANNEX_JIRA_RE.match(x)]
            if ANNEX_STUB_MARK in body or not written:
                out.append((s, 'the write-up is still the generated stub'))
            elif s['jira'] is None:
                out.append((s, 'no "### Jira ticket name:" line'))
            elif not s['jira'] or s['jira'].startswith('TODO'):
                out.append((s, 'the Jira ticket name is still a placeholder'))
        return out


def topic_annexes(d, topic):
    """(label, url, path, Annex|None) for each annex declared on a topic."""
    out = []
    for label, url in parse_annexes(topic['fields'].get('Annex:')):
        p = annex_path(d.cycle_id, label)
        a = Annex(p) if os.path.isfile(p) else None
        out.append((label, url, p, a))
    return out


def annex_problems(d, strict=False):
    """CYC-16 conformance: every annex has a sidecar, and the sidecar's ticket
    sections match the topic's Jira-bound tasks exactly.

    `strict` additionally refuses unwritten stubs. Structure is checked always,
    because it is cheap to fix and a drifting annex is the whole defect; the
    prose is only demanded when the page is about to be published, so that
    adding a ticket never blocks an unrelated local snapshot.
    """
    p = []
    for t in d.topics:
        entries = topic_annexes(d, t)
        if not entries:
            # CYC-16 v5.1.0: a shaped topic that has produced Jira-bound tasks owes
            # an annex. Annexes were optional while they were hand-authored in
            # Notion, where creating one cost real effort; generated from a sidecar
            # the cost is one `annex sync`, so a shaped topic with tickets and no
            # annex is an oversight rather than a decision. A shaping topic is
            # exempt without needing a clause: it has only `self:` tasks, so there
            # is nothing to write up.
            if t['state'] == 'shaped' and jira_tasks(t):
                p.append('topic "%s": CYC-16 — shaped, with %d Jira-bound task(s), and no "Annex:" '
                         'line. A shaped topic that has produced tickets owes their write-up; add '
                         'the line, then run "cycle.py annex sync".'
                         % (t['name'], len(jira_tasks(t))))
            continue
        want = [k['text'] for k in jira_tasks(t)]
        for label, url, path, a in entries:
            where = 'annex "%s" (topic "%s")' % (label, t['name'])
            if a is None:
                p.append('%s: CYC-16 — no sidecar at %s. The annex is generated from a local '
                         'file; run "cycle.py annex sync" to create it.'
                         % (where, os.path.basename(path)))
                continue
            p.extend(a.problems)
            if a.label and a.label != label:
                p.append('%s: CYC-16 — sidecar says "# Annex: %s"; the doc says %r. '
                         'The label is the identity — make them match.' % (where, a.label, label))
            if a.cycle_id and a.cycle_id != d.cycle_id:
                p.append('%s: CYC-16 — sidecar belongs to cycle %r, not %r'
                         % (where, a.cycle_id, d.cycle_id))
            if a.topic and a.topic != t['name']:
                p.append('%s: CYC-16 — sidecar names topic %r; it is linked from %r'
                         % (where, a.topic, t['name']))

            have = [s['task'] for s in a.ticket_sections]
            for task in want:
                if task not in have:
                    p.append('%s: CYC-16 — no section covers the ticket %r. Every Jira-bound '
                             'task in the topic needs one; run "cycle.py annex sync" to insert '
                             'the stub, then write it.' % (where, task[:70]))
            for task in have:
                if task not in want:
                    p.append('%s: CYC-16 — a section covers %r, which is no longer a Jira-bound '
                             'task in this topic. Delete the section or restore the task.'
                             % (where, task[:70]))
            dupes = [x for x in set(have) if have.count(x) > 1]
            for x in dupes:
                p.append('%s: CYC-16 — %d sections claim the same ticket %r; one section per '
                         'ticket' % (where, have.count(x), x[:70]))
            for sec in a.ticket_sections:
                if ANNEX_STUB_MARK in '\n'.join(sec['body']):
                    continue
                for why in slot_problems(sec):
                    p.append('%s: CYC-17 — section "%s" (line %d): %s. A ticket write-up is a '
                             'fixed set of slots in a fixed order; see references/tickets.md.'
                             % (where, sec['title'][:50], sec['line'], why))
            if strict:
                for s, why in a.stubs():
                    p.append('%s: CYC-16 — section "%s" (line %d): %s. An annex is published only '
                             'once its write-up is written — the structure is generated, the words '
                             'are not (CYC-14).' % (where, s['title'][:50], s['line'], why))
    return p


ANNEX_SKELETON = """# Annex: %(label)s
Cycle: %(cycle)s · Topic: %(topic)s

%(intro)s
"""


def cmd_annex(a):
    if a.action == 'list':
        return annex_list(a)
    if a.action == 'sync':
        return annex_sync(a)
    if a.action == 'render':
        return annex_render(a)
    die('unknown annex action %r' % a.action)


def annex_list(a):
    d = Doc(resolve(a.id))
    n = 0
    for t in d.topics:
        entries = topic_annexes(d, t)
        if not entries:
            continue
        want = [k['text'] for k in jira_tasks(t)]
        for label, url, path, ax in entries:
            n += 1
            print('%s  [%s] %s' % (label, ','.join(t['repos']), t['name']))
            print('  sidecar: %s%s' % (os.path.basename(path), '' if ax else '  (MISSING)'))
            print('  page:    %s' % url)
            if ax:
                have = [s['task'] for s in ax.ticket_sections]
                stubs = ax.stubs()
                print('  covers:  %d of %d ticket(s)%s'
                      % (len([x for x in want if x in have]), len(want),
                         ', %d still a stub' % len(stubs) if stubs else ''))
                for task in want:
                    if task not in have:
                        print('    missing: %s' % task[:70])
                for task in have:
                    if task not in want:
                        print('    orphan:  %s' % task[:70])
            print('')
    if not n:
        print('no annexes declared in %s' % os.path.basename(d.path))
    return 0


def annex_sync(a):
    """Create missing sidecars and insert a stub section per uncovered ticket.

    Never deletes and never rewrites prose: an orphaned section is reported, not
    removed, for the same reason `reconcile` never deletes a task.
    """
    d = Doc(resolve(a.id))
    touched, made = [], 0
    for t in d.topics:
        entries = topic_annexes(d, t)
        if not entries:
            continue
        want = jira_tasks(t)
        for label, url, path, ax in entries:
            if ax is None:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(ANNEX_SKELETON % {
                        'label': label, 'cycle': d.cycle_id, 'topic': t['name'],
                        'intro': '<!-- Shared background goes here: what the system is in plain '
                                 'terms, what is settled, what is open. Once, never per ticket '
                                 '(references/tickets.md). -->',
                    })
                print('created %s' % os.path.basename(path))
                made += 1
                ax = Annex(path)
            have = [s['task'] for s in ax.ticket_sections]
            add = [k for k in want if k['text'] not in have]
            if not add:
                continue
            body = read(path).rstrip('\n')
            for k in add:
                body += '\n\n## %s\nTask: %s\n%s\n%s\n' % (
                    k['text'], k['text'], ANNEX_STUB_JIRA, ANNEX_STUB)
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(body.rstrip('\n') + '\n')
            print('%s: +%d stub section(s)' % (os.path.basename(path), len(add)))
            for k in add:
                print('    %s' % k['text'][:70])
            touched.append(path)
    probs = annex_problems(d)
    if probs:
        print('\nstill not conforming:')
        for x in probs:
            print('  - %s' % x)
        return 1
    if not (touched or made):
        print('every annex already covers its tickets')
    else:
        print('\nwrite the stub sections before mirroring — the structure is generated, '
              'the write-up is not.')
    return 0


def mirror_json():
    p = os.path.join(cycle_home(), '.state', 'mirror.json')
    if not os.path.isfile(p):
        return {}
    try:
        return json.loads(read(p))
    except ValueError:
        return {}


def cycle_page_url(cycle_id):
    return ((mirror_json().get('cycles') or {}).get(cycle_id) or {}).get('url')


def annex_snapshot_path(cycle_id, label):
    d = os.path.join(cycle_home(), '.state')
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, '%s.annex.%s.mirror.md' % (cycle_id, annex_slug(label)))


def render_annex(d, topic, label, url, ax):
    """The Notion body for one annex page.

    The backlink is derived from `.state/mirror.json`, never typed: the first
    hand-written annex pointed at a page that was not the cycle's, and nothing
    in the system could notice.
    """
    out = []
    back = cycle_page_url(d.cycle_id)
    who = '[%s](%s)' % (d.cycle_id, back) if back else d.cycle_id
    tickets = ax.ticket_sections
    out.append('%d ticket%s. %s owns the scopes and their state; this is only what goes in the '
               'tickets. {color="gray"}' % (len(tickets), '' if len(tickets) == 1 else 's', who))
    out.append('Generated from `%s` — edit there, not here. {color="gray"}'
               % os.path.basename(ax.path))
    out.append('')
    pre = '\n'.join(ax.preamble).strip('\n')
    if pre:
        out.append(pre)
        out.append('')
    n = 0
    for s in ax.sections:
        if s['task'] is None:
            out.append('## %s' % s['title'])
        else:
            n += 1
            out.append('## %d. %s' % (n, s['title']))
        body = '\n'.join(s['body']).strip('\n')
        if body:
            out.append(body)
        out.append('')
    return '\n'.join(out).rstrip('\n') + '\n'


def annex_render(a):
    d = Doc(resolve(a.id))
    probs = d.check() + annex_problems(d, strict=True)
    if probs:
        print('not rendering a non-conforming annex - fix these first:')
        for x in probs:
            print('  - %s' % x)
        return 1
    hits = []
    for t in d.topics:
        for label, url, path, ax in topic_annexes(d, t):
            if a.label and a.label != label:
                continue
            hits.append((t, label, url, ax))
    if not hits:
        die('no annex matching %r' % a.label if a.label else 'no annexes declared')
    for t, label, url, ax in hits:
        body = render_annex(d, t, label, url, ax)
        if a.json:
            print(json.dumps({'label': label, 'url': url, 'body': body}, ensure_ascii=False))
        else:
            print('--- annex: %s' % label)
            print('--- page:  %s' % url)
            print('')
            print(body)
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

    ax = sub.add_parser('annex', help='ticket write-ups: the local sidecar behind an Annex: link')
    ax.add_argument('action', choices=('list', 'sync', 'render'),
                    help='list: coverage per annex · sync: create sidecars and stub the '
                         'uncovered tickets · render: the Notion body for an annex page')
    ax.add_argument('--label', help='render one annex by its label; default is all of them')
    ax.add_argument('--json', action='store_true')
    ax.add_argument('--id')
    ax.set_defaults(fn=cmd_annex)

    z = sub.add_parser('close', help='close preflight, then flip status')
    z.add_argument('--id')
    z.set_defaults(fn=cmd_close)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == '__main__':
    main()
