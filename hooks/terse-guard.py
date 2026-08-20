#!/usr/bin/env python3
"""UserPromptSubmit guard: re-assert the response-length ceiling on every turn.

The `caveman` output style lives in the system prompt, so it is far from the
current turn and loses to fresher, more specific instructions — in particular the
22 skills in this repo that prescribe a report shape ("Present it in this shape",
"Deliver the plan"). This hook re-states the ceiling as the last thing in
context, immediately next to the user's message, where it cannot drift.

Never blocks. Injects one block of additionalContext and exits 0.
"""
import json
import sys

REMINDER = (
    "Response-length ceiling (caveman output style, still in force this turn): "
    "match reply length to question length. A yes/no or lookup question gets a "
    "yes/no plus at most one line. No headers, no tables, no bullet lists unless "
    "the content is genuinely a list. No closing offer of follow-ups. "
    "If the user asked for a tldr at any point in this session, the cap is three "
    "lines with no structure, and it stays in force for every later turn. "
    "A skill's prescribed output shape governs the file or deliverable it "
    "produces, never the chat reply — the reply stays under this ceiling even "
    "when a skill asks for sections. Count the lines before sending; if over, "
    "delete rather than reorganise."
)


def main() -> int:
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": REMINDER,
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
