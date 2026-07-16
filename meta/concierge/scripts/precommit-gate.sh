#!/usr/bin/env bash
#
# precommit-gate.sh — turn the read-only concierge audit into a commit gate.
#
# Runs audit.sh, echoes its full report, and EXITS NON-ZERO if any [WARN] is
# present (INFO is allowed through). This is the mechanical half of concierge;
# the judgment half (trigger coverage, category fit, overlap) still needs the
# /concierge skill and cannot be enforced by a script.
#
# Used by both:
#   - .githooks/pre-commit            (blocks `git commit` from the CLI or Bash)
#   - the Claude Code PreToolUse hook (blocks Claude's `git commit` tool calls)
#
# Bypass (intentional, rare): `git commit --no-verify`.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd -P)"
AUDIT="$HERE/audit.sh"

if [ ! -x "$AUDIT" ] && [ ! -f "$AUDIT" ]; then
  echo "precommit-gate: cannot find audit.sh at $AUDIT" >&2
  exit 1
fi

out="$(bash "$AUDIT" 2>&1)"
echo "$out"

if printf '%s\n' "$out" | grep -q '\[WARN\]'; then
  echo
  echo "──────────────────────────────────────────────────────────────"
  echo "COMMIT BLOCKED: concierge audit found [WARN] issue(s) above."
  echo "Fix them (or run /concierge to review + apply fixes), then retry."
  echo "Intentional bypass: git commit --no-verify"
  echo "──────────────────────────────────────────────────────────────"
  exit 1
fi

exit 0
