#!/usr/bin/env python3
"""PostToolUse hook — queue a finding for the Notion cheat-sheet mirror.

Fires after every Edit/Write/MultiEdit. If the edited file is **any** project-context
skill's discoveries log (`<silo>/<silo>-<repo>/references/knowledge.md`), capture the
lines that were just added and append them to hooks/state/cheatsheet-queue.jsonl,
tagged with which project they came from.

Edits that only flip a `sheet:` marker are skipped — see is_bookkeeping().

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
import re
import subprocess
import sys
from datetime import datetime, timezone

# Any project-context skill's discoveries log, not one hardcoded project. The
# backreference encodes PCS-2's `<silo>/<silo>-<repo>/` naming, so this matches
# foleon/foleon-ripley/... and foleon/foleon-fio/... while ignoring the
# references/ directory of every ordinary skill. A new project is picked up with
# no change here — the previous hardcoded path silently dropped fio's findings.
LOG_RE = re.compile(
    r'(?:^|[/\\])([a-z0-9]+(?:-[a-z0-9]+)*)[/\\]\1-([a-z0-9-]+)'
    r'[/\\]references[/\\]knowledge\.md$'
)
MAX_ADDED_LINES = 60  # bound the payload; the log can have a large uncommitted delta
SHEET_MARKER = re.compile(r'sheet:\s*(?:none|no|yes)\b')


def repo_root(script_path):
    d = os.path.dirname(os.path.realpath(script_path))
    while d != '/':
        if os.path.isfile(os.path.join(d, 'CATEGORIES.md')):
            return d
        d = os.path.dirname(d)
    return None


def is_tracked(root, path):
    try:
        return subprocess.run(
            ['git', 'ls-files', '--error-unmatch', '--', path],
            cwd=root, capture_output=True, text=True, timeout=5,
        ).returncode == 0
    except Exception:
        return True  # assume tracked → fall back to the diff path


def added_lines(root, path):
    """Lines added to `path` versus HEAD, per git. Empty list if unavailable.

    An untracked file has no HEAD to diff against, so `git diff` prints nothing and
    the payload would come back empty — which is exactly the case for the FIRST
    finding of a newly created project log. Read the file directly instead: every
    line in it is, by definition, new.
    """
    if not is_tracked(root, path):
        try:
            with open(os.path.join(root, path), encoding='utf-8') as fh:
                lines = [ln.rstrip() for ln in fh if ln.strip()]
            return lines[-MAX_ADDED_LINES:]
        except Exception:
            return []
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


def edit_pairs(tool_input):
    """(old, new) string pairs for this call — Edit's one, or each of MultiEdit's."""
    edits = tool_input.get('edits')
    if isinstance(edits, list):
        return [(e.get('old_string', ''), e.get('new_string', '')) for e in edits]
    if 'old_string' in tool_input:
        return [(tool_input.get('old_string', ''), tool_input.get('new_string', ''))]
    return []


def is_bookkeeping(tool_input):
    """True when this call only flips `sheet:` markers.

    Marking a finding `sheet: no` after the maintainer declines it is a write to
    the log, but it is not a new finding. Queueing it would re-propose what was
    just rejected, and — because the Stop hook nudges whenever the queue is
    non-empty — every rejection would re-arm the nudge for the next session.

    Compared per-call via old_string/new_string rather than against the git diff:
    the diff is taken against HEAD, so it still carries every uncommitted finding
    and cannot tell which lines this particular edit touched.
    """
    pairs = edit_pairs(tool_input)
    if not pairs:
        return False  # Write, or an unrecognised shape → treat as a real edit
    for old, new in pairs:
        if old == new:
            continue
        if SHEET_MARKER.sub('sheet: X', old) != SHEET_MARKER.sub('sheet: X', new):
            return False
    return True


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get('tool_input') or {}
    file_path = tool_input.get('file_path') or ''
    match = LOG_RE.search(file_path.replace(os.sep, '/'))
    if not match:
        return 0
    project = match.group(2)  # 'ripley', 'fio', … — used only for the message

    if is_bookkeeping(tool_input):
        return 0

    root = repo_root(__file__)
    if not root:
        return 0

    # Diff the log that was actually edited, not a fixed one.
    rel_log = os.path.relpath(os.path.realpath(file_path), root)

    queue_dir = os.path.join(root, 'hooks', 'state')
    os.makedirs(queue_dir, exist_ok=True)
    queue = os.path.join(queue_dir, 'cheatsheet-queue.jsonl')

    entry = {
        'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'event': 'knowledge-log-write',
        'project': project,   # which project's log — the flush needs this to pick the Notion page
        'file': rel_log,
        'session': payload.get('session_id', ''),
        'added': added_lines(root, rel_log),
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
                f'A {project} discovery was appended to the log and queued for the '
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
