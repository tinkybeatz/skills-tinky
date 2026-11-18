#!/usr/bin/env bash
# launch.sh <slug> — open a herdr tab for a feature PM, start Claude in it, hand it the brief.
# Run from inside herdr (HERDR_ENV=1). Prints "tab=<id> pane=<id> agent=pm-<slug>".
set -euo pipefail

slug="${1:?usage: launch.sh <slug>}"
fio="/Users/gaeldelouis/Documents/GAEL/FOLEON-DEV/fio"
brief="docs/roadmap/features/${slug}/brief.md"
agent="pm-${slug}"

[ "${HERDR_ENV:-}" = 1 ] || { echo "not running inside herdr" >&2; exit 1; }
[[ "$agent" =~ ^[a-z][a-z0-9_-]{0,31}$ ]] || { echo "bad agent name: $agent" >&2; exit 1; }
[ -f "$fio/$brief" ] || { echo "brief missing: $fio/$brief" >&2; exit 1; }

created="$(herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$fio" --label "$slug" --no-focus)"
tab="$(jq -r '.result.tab.tab_id // .result.tab.id' <<<"$created")"
pane="$(jq -r '.result.root_pane.pane_id // .result.root_pane.id' <<<"$created")"
if [ -z "$tab" ] || [ "$tab" = null ] || [ -z "$pane" ] || [ "$pane" = null ]; then
  echo "could not read tab/pane ids from: $created" >&2
  exit 1
fi

# A fresh tab's shell takes a moment to reach its prompt; until then herdr answers
# agent_pane_busy. Retry only that error, for up to ~20 s.
started=""
for _ in $(seq 1 20); do
  if out="$(herdr agent start "$agent" --kind claude --pane "$pane" --timeout 60000 -- -n "PM ${slug}" --model opus 2>&1)"; then
    started=1
    break
  fi
  case "$out" in
    *agent_pane_busy*) sleep 1 ;;
    *) break ;;
  esac
done
if [ -z "$started" ]; then
  echo "agent start failed: $out" >&2
  echo "tab $tab left open for inspection (close it with: herdr tab close $tab)" >&2
  exit 1
fi

kickoff="You are ${agent}, the PM for the feature '${slug}' only. Read ${brief} first, then follow its 'Your rules' and 'First move'. Your notes live in docs/roadmap/features/${slug}/."
herdr agent prompt "$agent" "$kickoff" >/dev/null

echo "tab=${tab} pane=${pane} agent=${agent}"
