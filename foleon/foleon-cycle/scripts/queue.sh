#!/usr/bin/env bash
# Pending unlogged-work queue for the cycle dev log.
#
# Lives in the maintainer's cycle directory (CYC-1), NOT in skills-tinky:
#   $FOLEON_CYCLE_HOME/.state/cycle-queue.jsonl
#   default $HOME/Documents/GAEL/FOLEON/SHAPEUP-CYCLES/.state/cycle-queue.jsonl
#
# The queue exists so an ungraceful exit (cmd+Q) can't lose the fact that work
# happened: the PostToolUse hook appends when a Foleon repo file is edited, and
# the flush is opportunistic. `drain` prints BEFORE truncating and keeps a
# backup, so a crash between the two loses nothing.
#
# Queued entries are PROPOSALS (CYC-11) — draining them never writes a log line
# by itself, and nothing here can infer a hill position.
#
# Usage: queue.sh {count|peek|drain|restore|append|clear|path}

set -euo pipefail

HOME_DIR="${FOLEON_CYCLE_HOME:-$HOME/Documents/GAEL/FOLEON/SHAPEUP-CYCLES}"
QUEUE="$HOME_DIR/.state/cycle-queue.jsonl"
BACKUP="$QUEUE.drained"

mkdir -p "$(dirname "$QUEUE")"

cmd="${1:-count}"

case "$cmd" in
	path)   printf '%s\n' "$QUEUE" ;;
	count)  if [ -s "$QUEUE" ]; then wc -l < "$QUEUE" | tr -d ' '; else echo 0; fi ;;
	peek)   [ -s "$QUEUE" ] && cat "$QUEUE" || true ;;
	drain)
		if [ -s "$QUEUE" ]; then
			cat "$QUEUE"
			cp "$QUEUE" "$BACKUP"
			: > "$QUEUE"
		fi
		;;
	restore)
		# Undo a drain whose downstream write failed.
		if [ -s "$BACKUP" ]; then
			cat "$BACKUP" >> "$QUEUE"
			: > "$BACKUP"
			echo "restored $(wc -l < "$QUEUE" | tr -d ' ') entr(ies) to the queue" >&2
		else
			echo "nothing to restore" >&2
		fi
		;;
	append)
		[ $# -ge 2 ] || { echo "usage: queue.sh append '<json>'" >&2; exit 2; }
		printf '%s\n' "$2" >> "$QUEUE"
		;;
	clear)  : > "$QUEUE"; : > "$BACKUP" ;;
	*)      echo "usage: queue.sh {count|peek|drain|restore|append|clear|path}" >&2; exit 2 ;;
esac
