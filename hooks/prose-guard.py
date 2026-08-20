#!/usr/bin/env python3
"""PreToolUse guard: file and page content is persisted prose, never caveman-speak.

The `caveman` output style compresses chat replies. Its Boundaries section already says
persisted content stays normal prose, but that is a prompt instruction and can drift.
This hook re-states the rule deterministically, immediately before every write.

Never blocks. Injects one line of additionalContext and exits 0.
"""
import json
import sys

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
MCP_WRITE_PREFIXES = (
    "mcp__notion__notion-create-",
    "mcp__notion__notion-update-",
    "mcp__notion__notion-duplicate-",
    "mcp__notion__notion-create-comment",
)

REMINDER = (
    "Persisted content, not chat: write normal, well-formed prose here. "
    "The caveman output style does not apply to file or page content — "
    "no dropped articles, no fragments, no compression. "
    "Applies to code, comments, docs, markdown, commit messages, "
    "issue and PR text, memory files and Notion pages alike."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool = payload.get("tool_name", "")
    is_write = tool in WRITE_TOOLS or tool.startswith(MCP_WRITE_PREFIXES)
    if not is_write:
        return 0

    context = REMINDER
    path = (payload.get("tool_input") or {}).get("file_path")
    if path:
        context = f"{context} Target: {path}"

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": context,
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
