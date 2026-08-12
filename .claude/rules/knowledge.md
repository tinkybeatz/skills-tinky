# skills-tinky — project knowledge (discoveries log)

Append non-obvious findings here as you learn them: gotchas, implicit conventions,
architectural "why"s, sharp edges. Keep entries short and dated. When this file grows
heavy, run `/claude-md-architect` (refactor mode) to promote stable facts into the
root `CLAUDE.md` and prune the rest.

Format: `- YYYY-MM-DD — <finding>`

## Discoveries
- 2026-08-12 — `cheatsheet-queue-append.py` must ignore its own bookkeeping. Marking a
  ripley finding `sheet: no` is a write to `knowledge.md`, so it re-queued the finding
  that was just rejected — and since the Stop hook nudges on any non-empty queue, every
  rejection re-armed the nudge next session. Fixed by comparing the Edit's
  `old_string`/`new_string` (a `sheet:`-only delta is skipped); the git diff can't be
  used for this, as it is taken against HEAD and still carries every uncommitted finding.
- 2026-07-20 — This repo is the home of the **project-awareness system**: the
  SessionStart hook lives in `hooks/session-claude-md-check.sh` and is wired from the
  user's global `~/.claude/settings.json`. Docs in `README.md` → "Project awareness".
