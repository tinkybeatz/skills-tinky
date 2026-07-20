# skills-tinky — CLAUDE.md

## What
- A personal library of **Claude Code skills**, organized by category for humans and installed as **flat symlinks** (`~/.claude/skills/`) for Claude Code.
- A skill is a folder containing a `SKILL.md`. Meta-layer: `/god` (route), `/concierge` (maintain), `skill-creator` (author).
- Full map & conventions: `CATEGORIES.md` + each `<category>/_category.md`. Overview: `README.md`.

## Always
- Skill folder names are **globally unique** and **kebab-case** (they flatten into one symlink dir). The filename is exactly `SKILL.md`.
- Keep a `SKILL.md` under **500 lines** and its `description` under **1536 chars** — extract detail to `references/`.
- The **category of a skill is its folder path** — there is no category field in frontmatter.
- Author/edit skills with `skill-creator` (it places them in the right category and enforces the rules above); don't hand-scaffold.
- After any **structural change** (add/move/rename a skill, edit frontmatter), run `/concierge` — the judgment checks (trigger coverage, category fit, overlap) aren't script-checkable.
- Re-run `./link-skills.sh` after skills are **added, removed, or moved** (a plain `git pull` updates existing ones live). Rebuild the README cheat-sheet with `./generate-catalog.sh`.

## Commit gate
- Commits are **blocked on any `[WARN]`** from the concierge audit (git hook `.githooks/` + a `PreToolUse` hook in `.claude/settings.json`). Enable the git hook once per clone: `git config core.hooksPath .githooks`. Bypass intentionally with `--no-verify`.

## Discoveries
Accumulated project knowledge — append non-obvious findings as you learn them:
@.claude/rules/knowledge.md
