#!/usr/bin/env bash
# SessionStart hook — project-awareness router.
# On session start, look at the current repo and do ONE of:
#   - not a git repo ...................... nothing (silent)
#   - opted out + mapped to a skill ....... tell Claude to load that skill for context
#   - opted out, no mapping ............... nothing (silent)
#   - no CLAUDE.md ........................ nudge to create one
#   - has CLAUDE.md ....................... nothing (auto-loads natively)
#
# Opt-out / mapping list: awareness-ignore.txt (next to this script), one entry
# per line. Two forms:
#   ripley                    # opt out of the create-CLAUDE.md nudge
#   ripley -> foleon-ripley   # opt out AND point at the skill that holds this
#                             # project's context (for shared/work repos where
#                             # AI config must stay OUT of the checkout)
# The repo key is a bare folder name (portable) OR an absolute path (this machine).
# Everything resolves relative to this script, so it works wherever skills-tinky lives.
# Only the command path in ~/.claude/settings.json is per-machine.
#
# Wired from ~/.claude/settings.json → hooks.SessionStart. Docs: README ("Project awareness").

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ignore_file="$script_dir/awareness-ignore.txt"
add_helper="$script_dir/awareness-ignore-add.sh"

trim() { local s="$1"; s="${s#"${s%%[![:space:]]*}"}"; s="${s%"${s##*[![:space:]]}"}"; printf '%s' "$s"; }
emit() { printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$1"; }

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0   # not a git repo → silent
[ -z "$root" ] && exit 0
name="$(basename "$root")"

# --- opt-out / mapping list (match on bare name OR absolute path) ------------
if [ -f "$ignore_file" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    core="${line%%#*}"                               # strip trailing comment
    if [[ "$core" == *"->"* ]]; then
      repo_part="$(trim "${core%%->*}")"; skill_part="$(trim "${core#*->}")"
    else
      repo_part="$(trim "$core")"; skill_part=""
    fi
    [ -z "$repo_part" ] && continue
    if [ "$repo_part" = "$root" ] || [ "$repo_part" = "$name" ]; then
      if [ -n "$skill_part" ]; then
        emit "You are in the '$name' repo. Its project/AI context intentionally lives OUTSIDE this checkout (nothing Claude-specific belongs in this repo). All context for this project is in the \`$skill_part\` skill — load it (invoke the $skill_part skill) before doing engineering work here."
      fi
      exit 0                                         # opted out → done (silent unless mapped)
    fi
  done < "$ignore_file"
fi

# --- nudge if no CLAUDE.md ----------------------------------------------------
if [ ! -f "$root/CLAUDE.md" ] && [ ! -f "$root/.claude/CLAUDE.md" ]; then
  emit "No CLAUDE.md found in this repo ($name). It is not AI-aware yet. Offer the user two options: (1) run /claude-md-architect to seed one, or (2) if this is a shared/work repo where AI config should stay out of the checkout, opt it out — run \`$add_helper\` (no args: opts out the current repo by name and auto-commits). To also bind the repo to a context skill, pass it: \`$add_helper . <skill-name>\`."
fi

exit 0
