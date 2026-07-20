# skills-tinky — project knowledge (discoveries log)

Append non-obvious findings here as you learn them: gotchas, implicit conventions,
architectural "why"s, sharp edges. Keep entries short and dated. When this file grows
heavy, run `/claude-md-architect` (refactor mode) to promote stable facts into the
root `CLAUDE.md` and prune the rest.

Format: `- YYYY-MM-DD — <finding>`

## Discoveries
- 2026-07-20 — This repo is the home of the **project-awareness system**: the
  SessionStart hook lives in `hooks/session-claude-md-check.sh` and is wired from the
  user's global `~/.claude/settings.json`. Docs in `README.md` → "Project awareness".
