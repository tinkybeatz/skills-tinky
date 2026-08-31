#!/usr/bin/env python3
"""SessionStart + Stop hook — surface unlogged work, and the calendar.

Compares the cycle queue (dates on which a Foleon repo was edited) against the
dev-log dates in the active cycle doc. Both live in the maintainer's cycle
directory (CYC-1), resolved from FOLEON_CYCLE_HOME or its default — never inside
skills-tinky. A date with work but no log line is
"unlogged" and gets reported.

Two triggers, deliberately different in force — same shape as
cheatsheet-queue-check.py, for the same reasons:

  Stop          fires when Claude finishes responding. Blocks the stop ONCE per
                session, so the day's state changes get logged while the context
                is still warm and the maintainer still remembers which scope
                moved. Once per session is a hard guarantee (marker file) — a
                stop hook that can re-fire on an unresolved queue is a loop.

  SessionStart  reports only, never blocks. This is the crash-recovery path: if
                the terminal was closed before the Stop nudge could be acted on,
                the work is still queued and surfaces here. A hard exit costs a
                delay, not the record.

SessionStart also reports the one **time-based** signal the doc's dates make
computable, which no edit can ever produce (CYC-11): which week of the dev window
today is. It fires independently of the queue, and only on SessionStart, because
the Stop nudge blocks and the week number is not something to act on at the end
of a turn.

There is deliberately no shaping-budget nudge. The maintainer shapes one topic at
a time, so elapsed days since the cycle start say nothing about whether the topic
they are not currently on has overrun anything (CYC-3, v7.0.0).

This hook proposes; it never writes (CYC-11). It cannot infer a hill position
from files touched or from elapsed time (CYC-6), so it never suggests one — it
reports what it sees and leaves the judgement, and the write, to the maintainer.

Silent when: no active cycle doc (no cycle, no expectation), or every date with
work already has a log line.

Wired from ~/.claude/settings.json. Never raises: everything exits 0.
"""

import glob
import json
import os
import re
import sys

LOG_DATE = re.compile(r'^- (\d{4}-\d{2}-\d{2})\s+\[')


CYCLE_HOME_DEFAULT = '~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES'


def cycle_home():
    """The maintainer's cycle directory (CYC-1) — same resolution as cycle.py."""
    return os.path.abspath(os.path.expanduser(
        os.environ.get('FOLEON_CYCLE_HOME') or CYCLE_HOME_DEFAULT))


def queue_file():
    return os.path.join(cycle_home(), '.state', 'cycle-queue.jsonl')


def repo_root(script_path):
    d = os.path.dirname(os.path.realpath(script_path))
    while d != '/':
        if os.path.isfile(os.path.join(d, 'CATEGORIES.md')):
            return d
        d = os.path.dirname(d)
    return None


def queued():
    """{date: {repos}} from the queue."""
    q = queue_file()
    out = {}
    if not os.path.isfile(q):
        return out
    try:
        with open(q, encoding='utf-8') as fh:
            for ln in fh:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    rec = json.loads(ln)
                except Exception:
                    continue
                d, r = rec.get('date'), rec.get('repo')
                if d and r:
                    out.setdefault(d, set()).add(r)
    except Exception:
        return {}
    return out


def active_doc():
    for p in sorted(glob.glob(os.path.join(cycle_home(), '*.md'))):
        try:
            with open(p, encoding='utf-8') as fh:
                head = [next(fh, '') for _ in range(3)]
        except Exception:
            continue
        if any('Status: active' in ln for ln in head):
            return p
    return None


def logged_dates(path):
    out = set()
    try:
        with open(path, encoding='utf-8') as fh:
            for ln in fh:
                m = LOG_DATE.match(ln)
                if m:
                    out.add(m.group(1))
    except Exception:
        pass
    return out


def dev_window_week(doc):
    """Which week of the dev window today is (CYC-11).

    Imports cycle.py and calls its own `week_of` rather than re-deriving the
    arithmetic here: the window length is a rule of the standard, and two copies
    of it would drift.

    Report-only, and deliberately carries no hill judgement: CYC-6 names *elapsed
    time* among the things a hill position may never be derived from, so "week 4
    of 6" must never become "probably downhill by now".
    """
    root = repo_root(__file__)
    if not root:
        return ''
    scripts = os.path.join(root, 'foleon', 'foleon-cycle', 'scripts')
    if not os.path.isfile(os.path.join(scripts, 'cycle.py')):
        return ''
    try:
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        import cycle
        return cycle.week_of(cycle.Doc(doc)) or ''
    except Exception:
        return ''   # a broken import must never cost the maintainer a session


def phrase(pairs):
    """'2026-08-18 (fio), 2026-08-19 (fio, ripley)'"""
    return ', '.join(f'{d} ({", ".join(sorted(rs))})' for d, rs in pairs)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    event = payload.get('hook_event_name') or (sys.argv[1] if len(sys.argv) > 1 else '')
    session = payload.get('session_id') or 'unknown'

    root = repo_root(__file__)   # only for the Stop once-per-session marker

    doc = active_doc()
    if not doc:
        return 0  # no active cycle → nothing to be behind on

    done = logged_dates(doc)
    unlogged = sorted((d, rs) for d, rs in queued().items() if d not in done)

    if not unlogged:
        return 0

    where = dev_window_week(doc)
    cycle = os.path.splitext(os.path.basename(doc))[0]
    days = phrase(unlogged)
    n = len(unlogged)
    day_word = 'day' if n == 1 else 'days'

    if event == 'SessionStart':
        bits = [f'Cycle {cycle}' + (f' — {where}.' if where else '.')]
        bits.append(
            f'{n} {day_word} of Foleon work has no dev-log line: {days}. Offer to run '
            f'/foleon-cycle to log it — do not guess what changed, and never infer a hill '
            f'position from the files that were touched.')
        bits.append('Mention this to the user and offer /foleon-cycle. Do not run it unprompted.')
        print(json.dumps({
            'hookSpecificOutput': {
                'hookEventName': 'SessionStart',
                'additionalContext': ' '.join(bits),
            }
        }))
        return 0

    if event == 'Stop':
        if not root:
            return 0  # no marker dir → cannot guarantee once-only → do not nudge
        marker_dir = os.path.join(root, 'hooks', 'state')
        try:
            os.makedirs(marker_dir, exist_ok=True)
            marker = os.path.join(marker_dir, f'cycle-stop-nudged-{session}')
            if os.path.exists(marker):
                return 0  # already nudged this session — never loop
            with open(marker, 'w', encoding='utf-8') as fh:
                fh.write('')
        except Exception:
            return 0  # cannot guarantee once-only → do not nudge at all

        print(json.dumps({
            'decision': 'block',
            'reason': (
                f'Cycle {cycle} has {n} {day_word} of work with no dev-log line: {days}. '
                f'Invoke /foleon-cycle now to log it: read the queue with '
                f'`bash scripts/queue.sh peek`, then for each state change, decision or surprise '
                f'worth a line (CYC-8 — most routine work earns none), draft the line and show it '
                f'to the maintainer. Ask which scopes moved on the hill rather than inferring it '
                f'from the files touched (CYC-6). Write only what they approve, with '
                f'`cycle.py log --gate ...`, then drain the queue. Then stop. '
                f'This prompt fires only once per session.'
            ),
        }))
        return 0

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
