#!/usr/bin/env bash
#
# link-skills.sh — (re)install this repo's skills into Claude Code.
#
# Walks the repo, finds every folder that directly contains a SKILL.md (at any
# depth), and creates a FLAT symlink for each in ~/.claude/skills/ — because
# Claude Code only discovers personal skills one level deep. Repo folder layout
# (categories) is decoupled from the installed layout.
#
# - Aborts if two skill folders share a name (they'd collide when flattened).
# - Prunes stale symlinks that point into this repo but no longer resolve.
# - Idempotent: safe to run repeatedly. Run after adding/removing/moving skills.
#
# Override the destination with:  CLAUDE_SKILLS_DIR=/path ./link-skills.sh
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"

# All skill folders = dirname of every SKILL.md (excluding .git)
skilldirs="$(find "$REPO" -name SKILL.md -not -path '*/.git/*' -exec dirname {} \;)"

if [ -z "$skilldirs" ]; then
  echo "No SKILL.md found under $REPO — nothing to link."
  exit 0
fi

# Collision check: basenames must be globally unique
dupes="$(printf '%s\n' "$skilldirs" | while IFS= read -r d; do basename "$d"; done | sort | uniq -d)"
if [ -n "$dupes" ]; then
  echo "COLLISION — these skill folder names appear more than once:" >&2
  echo "$dupes" >&2
  echo "Skill folder names must be globally unique (they flatten into one directory). Aborting." >&2
  exit 1
fi

# Prune stale symlinks that point into this repo but no longer resolve
for link in "$DEST"/*; do
  [ -L "$link" ] || continue
  tgt="$(readlink "$link")"
  case "$tgt" in
    "$REPO"/*)
      if [ ! -e "$link" ]; then
        echo "pruning stale link: $(basename "$link")"
        rm "$link"
      fi
      ;;
  esac
done

# Create / refresh symlinks
printf '%s\n' "$skilldirs" | while IFS= read -r d; do
  [ -n "$d" ] || continue
  ln -sfn "$d" "$DEST/$(basename "$d")"
done

count="$(printf '%s\n' "$skilldirs" | grep -c . || true)"
echo "Linked $count skills from $REPO into $DEST"
