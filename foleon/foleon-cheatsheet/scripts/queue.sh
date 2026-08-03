#!/usr/bin/env bash
# Pending-findings queue for the cheat-sheet mirror.
#
# The queue exists so an ungraceful exit (cmd+Q) can't lose a finding: the
# PostToolUse hook appends the instant a finding is logged, and the flush is
# opportunistic. `drain` prints BEFORE truncating, and keeps a backup, so a
# crash between the two loses nothing.
#
# Usage: queue.sh {count|peek|drain|restore|append|clear|path}

set -euo pipefail

# Resolve the repo root from this script's real location (it may be reached
# through the ~/.claude/skills symlink), by walking up to CATEGORIES.md.
resolve_repo_root() {
	local src="${BASH_SOURCE[0]}"
	while [ -L "$src" ]; do
		local target
		target="$(readlink "$src")"
		case "$target" in
			/*) src="$target" ;;
			*) src="$(cd -P "$(dirname "$src")" && pwd)/$target" ;;
		esac
	done
	local dir
	dir="$(cd -P "$(dirname "$src")" && pwd)"
	while [ "$dir" != "/" ]; do
		if [ -f "$dir/CATEGORIES.md" ]; then
			printf '%s\n' "$dir"
			return 0
		fi
		dir="$(dirname "$dir")"
	done
	echo "queue.sh: could not locate the skills-tinky root (no CATEGORIES.md above $src)" >&2
	return 1
}

REPO_ROOT="$(resolve_repo_root)"
QUEUE="$REPO_ROOT/hooks/state/cheatsheet-queue.jsonl"
BACKUP="$QUEUE.drained"

mkdir -p "$(dirname "$QUEUE")"

cmd="${1:-count}"

case "$cmd" in
	path)
		printf '%s\n' "$QUEUE"
		;;
	count)
		if [ -s "$QUEUE" ]; then wc -l < "$QUEUE" | tr -d ' '; else echo 0; fi
		;;
	peek)
		[ -s "$QUEUE" ] && cat "$QUEUE" || true
		;;
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
		# append '<json line>' — used by the hook.
		[ $# -ge 2 ] || { echo "usage: queue.sh append '<json>'" >&2; exit 2; }
		printf '%s\n' "$2" >> "$QUEUE"
		;;
	clear)
		: > "$QUEUE"
		: > "$BACKUP"
		;;
	*)
		echo "usage: queue.sh {count|peek|drain|restore|append|clear|path}" >&2
		exit 2
		;;
esac
