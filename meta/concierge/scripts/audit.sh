#!/usr/bin/env bash
#
# audit.sh — read-only health check for the skills-tinky repo.
# Prints findings; never modifies anything. The concierge skill interprets the
# output and proposes fixes. Findings are WARN (should fix) or INFO (heads-up).
#
# Repo root is derived from this script's own real location (symlinks resolved),
# so it works wherever the repo lives or is cloned.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd -P)"
REPO="$(cd "$HERE/../../.." && pwd -P)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

WC="$(mktemp)"; IC="$(mktemp)"   # warn/info counters
trap 'rm -f "$WC" "$IC"' EXIT
W(){ echo "  [WARN] $*"; echo x >> "$WC"; }
I(){ echo "  [INFO] $*"; echo x >> "$IC"; }
rel(){ echo "${1#$REPO/}"; }

fm_name(){ # $1 = SKILL.md path -> value of name: in frontmatter
  awk 'NR==1&&/^---/{b=1;next} b&&/^---/{exit} b&&/^name:/{sub(/^name:[[:space:]]*/,"");gsub(/["'\'']/,"");gsub(/[[:space:]]+$/,"");print;exit}' "$1"
}
fm_has_desc(){ awk 'NR==1&&/^---/{b=1;next} b&&/^---/{exit} b&&/^description:/{found=1} END{exit !found}' "$1"; }

echo "Concierge audit"
echo "  repo:   $REPO"
echo "  skills: $DEST"
echo "======================================================"

skilldirs="$(find "$REPO" \( -name SKILL.md -o -name skill.md \) -not -path '*/.git/*' -exec dirname {} \; | sort -u)"
nskills="$(printf '%s\n' "$skilldirs" | grep -c . || true)"
echo "Skills found: $nskills"

echo; echo "--- 1. SKILL.md casing ---"
lc="$(find "$REPO" -name skill.md -not -path '*/.git/*')"
if [ -n "$lc" ]; then while IFS= read -r f; do W "lowercase skill.md (rename to SKILL.md): $(rel "$f")"; done <<EOF
$lc
EOF
else echo "  ok"; fi

echo; echo "--- 2. Frontmatter: name present & matches folder, description present ---"
badfm=0
while IFS= read -r d; do
  [ -n "$d" ] || continue
  smd="$d/SKILL.md"; [ -f "$smd" ] || smd="$d/skill.md"
  base="$(basename "$d")"
  nm="$(fm_name "$smd")"
  if [ -z "$nm" ]; then W "missing 'name:' in frontmatter: $(rel "$smd")"; badfm=1
  elif [ "$nm" != "$base" ]; then W "name '$nm' != folder '$base': $(rel "$smd")"; badfm=1; fi
  if ! fm_has_desc "$smd"; then W "missing 'description:' in frontmatter: $(rel "$smd")"; badfm=1; fi
done <<EOF
$skilldirs
EOF
[ "$badfm" -eq 0 ] && echo "  ok"

echo; echo "--- 3. Folder naming (kebab-case) ---"
badkebab=0
while IFS= read -r d; do
  [ -n "$d" ] || continue
  base="$(basename "$d")"
  echo "$base" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$' || { W "folder not kebab-case: $(rel "$d")"; badkebab=1; }
done <<EOF
$skilldirs
EOF
[ "$badkebab" -eq 0 ] && echo "  ok"

echo; echo "--- 4. Name collisions (must be globally unique) ---"
dupes="$(printf '%s\n' "$skilldirs" | while IFS= read -r d; do [ -n "$d" ] && basename "$d"; done | sort | uniq -d)"
if [ -n "$dupes" ]; then while IFS= read -r n; do W "duplicate skill name '$n' (collides when flattened into $DEST)"; done <<EOF
$dupes
EOF
else echo "  ok"; fi

echo; echo "--- 5. Taxonomy: every skill under a category (_category.md ancestor) ---"
orphan=0
while IFS= read -r d; do
  [ -n "$d" ] || continue
  p="$d"; found=0
  while [ "$p" != "$REPO" ] && [ "$p" != "/" ]; do
    p="$(dirname "$p")"
    [ -f "$p/_category.md" ] && { found=1; break; }
  done
  [ "$found" -eq 1 ] || { W "skill outside taxonomy (no _category.md ancestor): $(rel "$d")"; orphan=1; }
done <<EOF
$skilldirs
EOF
[ "$orphan" -eq 0 ] && echo "  ok"

echo; echo "--- 6. Subfolder naming consistency ---"
sing="$(find "$REPO" -type d -name reference -not -path '*/.git/*')"
if [ -n "$sing" ]; then while IFS= read -r f; do W "singular 'reference/' (prefer 'references/'): $(rel "$f")"; done <<EOF
$sing
EOF
fi
evln="$(find "$REPO" -type d -name evaluations -not -path '*/.git/*')"
evls="$(find "$REPO" -type d -name evals -not -path '*/.git/*')"
if [ -n "$evln" ] && [ -n "$evls" ]; then
  while IFS= read -r f; do I "mixed eval dir naming ('evaluations/' vs 'evals/'): $(rel "$f")"; done <<EOF
$evln
EOF
fi
[ -z "$sing" ] && { [ -z "$evln" ] || [ -z "$evls" ]; } && echo "  ok"

echo; echo "--- 7. Symlink health ($DEST) ---"
symok=1
# 7a. each skill has a correct link
while IFS= read -r d; do
  [ -n "$d" ] || continue
  base="$(basename "$d")"; link="$DEST/$base"
  if [ ! -L "$link" ]; then W "not linked (run link-skills.sh): $base"; symok=0
  else
    tgt="$(readlink "$link")"
    [ "$tgt" = "$d" ] || { W "link '$base' points to '$tgt', expected '$d'"; symok=0; }
  fi
done <<EOF
$skilldirs
EOF
# 7b. stale/broken links pointing into this repo
if [ -d "$DEST" ]; then
  for link in "$DEST"/*; do
    [ -L "$link" ] || continue
    tgt="$(readlink "$link")"
    case "$tgt" in
      "$REPO"/*) [ -e "$link" ] || { W "stale link (target gone): $(basename "$link") -> $tgt"; symok=0; } ;;
    esac
  done
fi
[ "$symok" -eq 1 ] && echo "  ok"

echo; echo "======================================================"
nw="$(wc -l < "$WC" 2>/dev/null | tr -d ' ')"; [ -n "$nw" ] || nw=0
ni="$(wc -l < "$IC" 2>/dev/null | tr -d ' ')"; [ -n "$ni" ] || ni=0
echo "SUMMARY: $nw warning(s), $ni info. Skills: $nskills."
[ "$nw" -eq 0 ] && echo "Repo is clean. ✅"
exit 0
