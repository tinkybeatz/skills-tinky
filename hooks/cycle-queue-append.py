#!/usr/bin/env python3
"""PostToolUse hook — record that work happened in a Foleon repo.

Fires after every Edit/Write/MultiEdit. If the edited file sits inside a repo
registered in hooks/awareness-ignore.txt (`ripley -> foleon-ripley`,
`fio -> foleon-fio`, and whatever is added later), append one entry to the
queue in the maintainer's cycle directory (`<cycle home>/.state/cycle-queue.jsonl`,
CYC-1) tagged with the repo and the date.

What this hook does NOT do, by CYC-11: it never writes a dev-log line, never
touches a cycle doc, and never talks to Notion. A queue entry is *evidence that
work happened*, not a log entry — the log line needs a gate judgement and the
maintainer's yes, neither of which a hook can supply. Every automatic thing here
stops at "something happened in fio today."

Why a queue at all: the terminal can be closed mid-task, and a hill position or
a decision that never got logged is gone. Appending here is instant and
reasoning-free, so the *fact* of the work is durable immediately; the Stop and
SessionStart hooks then surface it for the maintainer to turn into log lines.

Reusing awareness-ignore.txt as the repo registry means a new Foleon repo starts
being tracked the moment it's bound to a context skill — no second list to keep
in sync, and no hard-coded paths that break on another machine.

Wired from ~/.claude/settings.json -> hooks.PostToolUse. Never blocks: any
failure exits 0 silently, because losing a queue entry must never break an edit.
"""

import json
import os
import sys

# One (date, repo, file) is recorded once. Beyond this many entries for a repo
# on one date the queue stops growing — the nudge says the same thing whether
# 40 files or 400 were touched, and an unbounded file is its own bug.
MAX_PER_REPO_DATE = 40


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


def known_repos(root):
    """Bare repo names from awareness-ignore.txt — the registry of Foleon repos."""
    names = []
    path = os.path.join(root, 'hooks', 'awareness-ignore.txt')
    try:
        with open(path, encoding='utf-8') as fh:
            for ln in fh:
                ln = ln.split('#', 1)[0].strip()
                if not ln:
                    continue
                left = ln.split('->', 1)[0].strip()
                if left and not left.startswith('/'):
                    names.append(left)
    except Exception:
        return []
    return names


def repo_for(path, names):
    """Which registered repo this file lives in, by path component match."""
    parts = os.path.realpath(path).split(os.sep)
    for n in names:
        if n in parts:
            return n
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get('tool_name') not in ('Edit', 'Write', 'MultiEdit', 'NotebookEdit'):
        return 0

    tool_input = payload.get('tool_input') or {}
    fpath = tool_input.get('file_path') or tool_input.get('notebook_path')
    if not fpath:
        return 0

    root = repo_root(__file__)
    if not root:
        return 0

    real = os.path.realpath(fpath)
    if real.startswith(os.path.realpath(root) + os.sep):
        return 0  # edits to skills-tinky itself are not cycle work

    names = known_repos(root)
    if not names:
        return 0
    repo = repo_for(real, names)
    if not repo:
        return 0

    # Date, not timestamp: the dev log is dated by day (CYC-8), so the day is
    # the only granularity the downstream nudge can use.
    import datetime
    date = datetime.date.today().isoformat()

    queue = queue_file()
    qdir = os.path.dirname(queue)
    try:
        os.makedirs(qdir, exist_ok=True)
        same_key = 0
        if os.path.isfile(queue):
            with open(queue, encoding='utf-8') as fh:
                for ln in fh:
                    ln = ln.strip()
                    if not ln:
                        continue
                    try:
                        rec = json.loads(ln)
                    except Exception:
                        continue
                    if rec.get('date') == date and rec.get('repo') == repo:
                        if rec.get('file') == real:
                            return 0  # already recorded
                        same_key += 1
        if same_key >= MAX_PER_REPO_DATE:
            return 0
        with open(queue, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps({'date': date, 'repo': repo, 'file': real}) + '\n')
    except Exception:
        return 0
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
