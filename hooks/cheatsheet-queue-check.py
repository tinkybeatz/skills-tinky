#!/usr/bin/env python3
"""SessionStart + Stop hook — flush the cheat-sheet queue when it has entries.

Two triggers, deliberately different in force:

  Stop          fires when Claude finishes responding. Blocks the stop ONCE per
                session with a reason, so findings logged during the session get
                mirrored while the context is still warm. Once per session is a
                hard guarantee (marker file) — a stop hook that can re-fire on an
                unemptied queue is an infinite loop.

  SessionStart  fires on a new session. Only reports; never blocks. This is the
                crash-recovery path: if the terminal was closed with cmd+Q before
                the Stop nudge could be acted on, the findings are still queued
                and surface here. A hard exit therefore costs a delay, not data.

SessionEnd is deliberately NOT used: it is cleanup-only — it cannot inject
context and its output is ignored, so it can never trigger the flush.

Wired from ~/.claude/settings.json. Never raises: a failure here must not break
the session, so everything exits 0.
"""

import json
import os
import sys


def repo_root(script_path):
    d = os.path.dirname(os.path.realpath(script_path))
    while d != '/':
        if os.path.isfile(os.path.join(d, 'CATEGORIES.md')):
            return d
        d = os.path.dirname(d)
    return None


def queue_count(root):
    q = os.path.join(root, 'hooks', 'state', 'cheatsheet-queue.jsonl')
    if not os.path.isfile(q):
        return 0
    try:
        with open(q, encoding='utf-8') as fh:
            return sum(1 for ln in fh if ln.strip())
    except Exception:
        return 0


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    event = payload.get('hook_event_name') or (sys.argv[1] if len(sys.argv) > 1 else '')
    session = payload.get('session_id') or 'unknown'

    root = repo_root(__file__)
    if not root:
        return 0

    count = queue_count(root)
    if count == 0:
        return 0  # nothing pending → silent

    noun = 'finding' if count == 1 else 'findings'
    is_are = 'is' if count == 1 else 'are'
    was_were = 'was' if count == 1 else 'were'

    if event == 'SessionStart':
        print(json.dumps({
            'hookSpecificOutput': {
                'hookEventName': 'SessionStart',
                'additionalContext': (
                    f'{count} ripley {noun} {is_are} queued for the Notion cheat sheet '
                    f'from a previous session that ended before they were synced. '
                    f'Mention this to the user and offer to run the foleon-cheatsheet '
                    f'skill to process the queue. Do not run it unprompted.'
                ),
            }
        }))
        return 0

    if event == 'Stop':
        marker_dir = os.path.join(root, 'hooks', 'state')
        os.makedirs(marker_dir, exist_ok=True)
        marker = os.path.join(marker_dir, f'stop-nudged-{session}')
        if os.path.exists(marker):
            return 0  # already nudged this session — never loop
        try:
            with open(marker, 'w', encoding='utf-8') as fh:
                fh.write('')
        except Exception:
            return 0  # cannot guarantee once-only → do not nudge at all

        print(json.dumps({
            'decision': 'block',
            'reason': (
                f'{count} ripley {noun} {was_were} logged this session and {is_are} queued for '
                f'the Notion cheat sheet. Invoke the foleon-cheatsheet skill now to '
                f'process the queue: apply the four admission gates (most findings are '
                f'correctly rejected), rewrite any survivors for a human, dedupe, and '
                f'write them as "Needs review". Then stop. This prompt fires only once '
                f'per session.'
            ),
        }))
        return 0

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
