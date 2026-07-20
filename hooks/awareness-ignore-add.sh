#!/usr/bin/env bash
# Opt a repo OUT of the project-awareness nudge, then auto-commit the change.
#
# Usage:
#   awareness-ignore-add.sh              # opt out the CURRENT git repo, by name (portable)
#   awareness-ignore-add.sh <name>       # opt out by bare repo name (matches on any machine)
#   awareness-ignore-add.sh <abs-path>   # opt out by absolute path (this machine only)
#
# Prefer the bare name: it's portable across laptops (awareness-ignore.txt is
# committed and synced), whereas an absolute path only matches where it was written.
# Paths resolve relative to this script, so it works wherever skills-tinky lives.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ignore_file="$script_dir/awareness-ignore.txt"
repo_root="$(cd "$script_dir/.." && pwd)"          # skills-tinky root (hooks/ is one level down)
[ -f "$ignore_file" ] || touch "$ignore_file"

entry="${1:-}"
if [ -z "$entry" ]; then                            # default: current repo, by name
  cur="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  [ -z "$cur" ] && { echo "Not in a git repo and no argument given." >&2; exit 1; }
  entry="$(basename "$cur")"
fi

# idempotent: skip if already listed (exact match on a non-comment line)
if grep -vE '^[[:space:]]*#' "$ignore_file" | grep -qxF "$entry"; then
  echo "Already opted out: $entry"
  exit 0
fi

printf '%s\n' "$entry" >> "$ignore_file"
echo "Added to opt-out list: $entry"

# Commit ONLY the blacklist file. The pathspec form commits this one path from the
# working tree and leaves any other staged/unstaged changes untouched — so it never
# sweeps up a commit-in-progress you have waiting.
git -C "$repo_root" commit -m "Opt out '$entry' from project-awareness nudge" \
  -- "$ignore_file" >/dev/null
echo "Committed to skills-tinky (blacklist only; other changes left untouched)."
