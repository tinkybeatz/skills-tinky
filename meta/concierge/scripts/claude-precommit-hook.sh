#!/usr/bin/env bash
#
# claude-precommit-hook.sh — Claude Code PreToolUse hook for `git commit`.
#
# Wired from .claude/settings.json (matcher: Bash). On every Bash tool call it
# inspects the command; if it's a `git commit`, it runs the concierge gate and
# BLOCKS the commit (exit 2) when the audit reports a [WARN]. On a clean audit
# it allows the commit but prints a reminder that the *judgment* half of
# concierge (trigger coverage, category fit, overlap) is not script-checkable
# and should have been reviewed via /concierge.
#
# Protocol: stdin = tool-call JSON; exit 0 = allow, exit 2 = block (stderr goes
# back to Claude). Any git commit with --no-verify is intentionally allowed.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd -P)"
GATE="$HERE/precommit-gate.sh"

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"

# Only act on actual `git commit` invocations (allow global flags before it).
if ! printf '%s' "$cmd" | grep -qE '(^|[;&|]|\s)git(\s+-[^ ]+)*\s+commit(\s|$)'; then
  exit 0
fi

# Honor the standard bypass.
if printf '%s' "$cmd" | grep -qE '(--no-verify|(^|\s)-[a-zA-Z]*n)'; then
  exit 0
fi

if [ ! -f "$GATE" ]; then
  exit 0  # gate missing — don't wedge commits
fi

if out="$(bash "$GATE" 2>&1)"; then
  # Clean audit — allow, but nudge on the part a script can't verify.
  echo "concierge: mechanical audit clean ✅  (judgment half — trigger coverage, category fit, overlap — is not script-checkable; run /concierge if you changed any skill's content or placement)" >&2
  exit 0
else
  {
    echo "concierge PreToolUse gate: commit blocked."
    echo
    echo "$out"
    echo
    echo "Resolve the [WARN]s above (run /concierge to review and apply fixes),"
    echo "then retry the commit. Intentional bypass: git commit --no-verify"
  } >&2
  exit 2
fi
