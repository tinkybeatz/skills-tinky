#!/usr/bin/env bash
# SessionStart hook — project-awareness nudge.
# When the current repo has no CLAUDE.md, inject a note asking Claude to offer
# seeding one with /claude-md-architect — or to opt the repo out of this system.
# Silent (exit 0, no output) for: non-git dirs, repos that already have a
# CLAUDE.md, and repos opted out via awareness-ignore.txt.
#
# Opt-out list (awareness-ignore.txt, next to this script): one entry per line,
# a bare repo folder name (portable across machines) OR an absolute path
# (matches only on this machine); '#' starts a comment. Use it for shared/work
# repos where AI config must stay OUT of the checkout — capture that project's
# knowledge in a skill you own instead.
#
# Paths are resolved RELATIVE TO THIS SCRIPT, so the repo can live anywhere / on
# any laptop. Only the command path in ~/.claude/settings.json is per-machine.
#
# Wired from ~/.claude/settings.json → hooks.SessionStart. Documented in
# README.md ("Project awareness").

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ignore_file="$script_dir/awareness-ignore.txt"
add_helper="$script_dir/awareness-ignore-add.sh"

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0   # not a git repo → silent
[ -z "$root" ] && exit 0

name="$(basename "$root")"

# --- opt-out list (match on bare name OR absolute path) ----------------------
if [ -f "$ignore_file" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    line="${line%%#*}"                               # strip trailing comment
    line="${line#"${line%%[![:space:]]*}"}"          # ltrim
    line="${line%"${line##*[![:space:]]}"}"          # rtrim
    [ -z "$line" ] && continue
    if [ "$line" = "$root" ] || [ "$line" = "$name" ]; then
      exit 0                                         # opted out → silent
    fi
  done < "$ignore_file"
fi

# --- nudge if no CLAUDE.md ----------------------------------------------------
if [ ! -f "$root/CLAUDE.md" ] && [ ! -f "$root/.claude/CLAUDE.md" ]; then
  msg="No CLAUDE.md found in this repo ($name). It is not AI-aware yet. Offer the user two options: (1) run /claude-md-architect to seed one, or (2) if this is a shared/work repo where AI config should stay out of the checkout, opt it out — run \`$add_helper\` (no args: opts out the current repo by name and auto-commits the change to skills-tinky)."
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$msg"
fi

exit 0
