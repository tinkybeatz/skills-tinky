#!/usr/bin/env bash
# SessionStart hook — project-awareness nudge.
# When the current repo has no CLAUDE.md, inject a note asking Claude to offer
# seeding one with /claude-md-architect before doing engineering work.
# Silent (exit 0, no output) for: non-git dirs, repos that already have a
# CLAUDE.md, and repos opted out via hooks/awareness-ignore.txt.
#
# Opt-out: list repos to skip in hooks/awareness-ignore.txt (one per line;
# absolute path OR bare repo folder name; '#' starts a comment). Use this for
# shared/work repos where AI config must stay OUT of the checkout — capture that
# project's knowledge in a skill you own instead.
#
# Wired from ~/.claude/settings.json → hooks.SessionStart. Versioned here so the
# mechanism is inspectable in the repo. Part of the project-awareness system
# documented in README.md ("Project awareness").

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0   # not a git repo → silent
[ -z "$root" ] && exit 0

name="$(basename "$root")"

# --- opt-out list ------------------------------------------------------------
ignore_file="$HOME/Documents/GAEL/AI/skills-tinky/hooks/awareness-ignore.txt"
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
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"No CLAUDE.md found in this repo (%s). It is not AI-aware yet. Offer to run /claude-md-architect to seed one before doing engineering work."}}\n' "$name"
fi

exit 0
