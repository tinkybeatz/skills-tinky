#!/usr/bin/env python3
"""PostToolUse hook — queue a finding for the Notion cheat-sheet mirror.

Fires after every Edit/Write/MultiEdit. If the edited file is the ripley
discoveries log, capture the lines that were just added and append them to
hooks/state/cheatsheet-queue.jsonl.

Why a queue at all: the flush needs a model (it has to judge admission and
rewrite the text), but the model may never get the chance — the terminal can be
closed mid-task. Appending here is instant and reasoning-free, so a finding is
durable the moment it is logged. The `Stop` and `SessionStart` hooks then flush
opportunistically, and `SessionStart` guarantees a crash is only ever a delay.

Python rather than bash because this reads JSON on stdin and writes JSON on
stdout; quoting a diff safely through bash is a footgun.

Wired from ~/.claude/settings.json -> hooks.PostToolUse. Never blocks: any
failure exits 0 silently, because losing a cheat-sheet row must never break the
user's edit.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

TARGET_SUFFIX = os.path.join('foleon', 'foleon-ripley', 'references', 'knowledge.md')
MAX_ADDED_LINES = 60  # bound the payload; the log can have a large uncommitted delta


def repo_root(script_path):
    d = os.path.dirname(os.path.realpath(script_path))
    while d != '/':
        if os.path.isfile(os.path.join(d, 'CATEGORIES.md')):
            return d
        d = os.path.dirname(d)
    return None


def added_lines(root, path):
    """Lines added to `path` versus HEAD, per git. Empty list if unavailable."""
    try:
        out = subprocess.run(
            ['git', 'diff', '-U0', '--', path],
            cwd=root, capture_output=True, text=True, timeout=5,
        ).stdout
    except Exception:
        return []
    lines = [
        ln[1:].rstrip()
        for ln in out.splitlines()
        if ln.startswith('+') and not ln.startswith('+++')
    ]
    lines = [ln for ln in lines if ln.strip()]
    return lines[-MAX_ADDED_LINES:]


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    file_path = (payload.get('tool_input') or {}).get('file_path') or ''
    if not file_path.endswith(TARGET_SUFFIX):
        return 0

    root = repo_root(__file__)
    if not root:
        return 0

    queue_dir = os.path.join(root, 'hooks', 'state')
    os.makedirs(queue_dir, exist_ok=True)
    queue = os.path.join(queue_dir, 'cheatsheet-queue.jsonl')

    entry = {
        'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'event': 'knowledge-log-write',
        'file': os.path.relpath(file_path, root) if file_path.startswith(root) else file_path,
        'session': payload.get('session_id', ''),
        'added': added_lines(root, TARGET_SUFFIX),
    }

    try:
        with open(queue, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except Exception:
        return 0

    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PostToolUse',
            'additionalContext': (
                'A ripley discovery was appended to the log and queued for the '
                'Notion cheat sheet. Do not sync now — finish the task first. '
                'The Stop hook will prompt for it, or run /foleon-cheatsheet.'
            ),
        }
    }))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # never break an edit over a cheat-sheet row
