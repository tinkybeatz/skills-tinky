#!/usr/bin/env bash
# Opt a repo OUT of the project-awareness nudge (optionally binding it to a
# context skill), then auto-commit ONLY the blacklist file.
#
# Usage:
#   awareness-ignore-add.sh                    # current repo, by name, plain opt-out
#   awareness-ignore-add.sh <repo>             # explicit repo (name or abs path)
#   awareness-ignore-add.sh <repo> <skill>     # repo + context-skill mapping
#   awareness-ignore-add.sh . <skill>          # current repo + context-skill mapping
#
# Prefer a bare repo name (portable across machines) over an absolute path.
# Re-running updates an existing repo's mapping in place — never duplicates.
# Paths resolve relative to this script, so it works wherever skills-tinky lives.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ignore_file="$script_dir/awareness-ignore.txt"
repo_root="$(cd "$script_dir/.." && pwd)"          # skills-tinky root (hooks/ is one level down)
[ -f "$ignore_file" ] || touch "$ignore_file"

trim() { local s="$1"; s="${s#"${s%%[![:space:]]*}"}"; s="${s%"${s##*[![:space:]]}"}"; printf '%s' "$s"; }

entry="${1:-}"
skill="${2:-}"
if [ -z "$entry" ] || [ "$entry" = "." ]; then     # default / '.' → current repo by name
  cur="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  [ -z "$cur" ] && { echo "Not in a git repo; pass a repo name explicitly." >&2; exit 1; }
  entry="$(basename "$cur")"
fi

if [ -n "$skill" ]; then desired="$entry -> $skill"; else desired="$entry"; fi

# Rewrite the list: update our repo's line in place if present, else append.
tmp="$(mktemp)"
action="add"
found=0
while IFS= read -r l || [ -n "$l" ]; do
  core="${l%%#*}"
  if [[ "$core" == *"->"* ]]; then rp="$(trim "${core%%->*}")"; else rp="$(trim "$core")"; fi
  if [ "$found" -eq 0 ] && [ -n "$rp" ] && [ "$rp" = "$entry" ]; then
    found=1
    if [ "$(trim "$core")" = "$desired" ]; then
      action="same"; printf '%s\n' "$l" >> "$tmp"
    else
      action="update"; printf '%s\n' "$desired" >> "$tmp"
    fi
  else
    printf '%s\n' "$l" >> "$tmp"
  fi
done < "$ignore_file"
if [ "$found" -eq 0 ]; then printf '%s\n' "$desired" >> "$tmp"; fi

if [ "$action" = "same" ]; then
  rm -f "$tmp"; echo "Already opted out: $desired"; exit 0
fi
mv "$tmp" "$ignore_file"
case "$action" in
  add)    echo "Added to opt-out list: $desired" ;;
  update) echo "Updated opt-out mapping: $desired" ;;
esac

# Commit ONLY the blacklist file (pathspec) — never sweeps up other staged work.
git -C "$repo_root" commit -m "Opt out '$entry' from project-awareness nudge${skill:+ (context skill: $skill)}" \
  -- "$ignore_file" >/dev/null
echo "Committed to skills-tinky (blacklist only; other changes left untouched)."
