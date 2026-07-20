# Taxonomy & placement (skills-tinky)

How to place a new skill correctly inside the **skills-tinky** repo: pick the right category, scaffold at the right path, apply that category's conventions, keep names unique, and wire it up. Follow this whenever you create a skill for skills-tinky (the default context — but always confirm first, see Step A).

## Step A — Confirm the target context (ALWAYS ask)
Default is a **skills-tinky global skill**, but never assume silently — confirm with the user each time:
- **skills-tinky (default)** — a reusable, globally-available skill that lives in this repo and symlinks into `~/.claude/skills/`.
- **Project-scoped** — a skill meaningful only inside one specific repo → it belongs in that repo's `.claude/skills/`, NOT here. If the user wants this, create it there and stop following this file.
- **Somewhere else** — honor whatever path the user specifies.

Only continue with the steps below if the target is skills-tinky.

## Step B — Locate the repo root
This skill lives at `<repo>/meta/skill-creator/`. Resolve the repo root robustly (it may be reached via a symlink):
```bash
# from the skill's real dir, walk up to the folder containing CATEGORIES.md
```
The repo root is the directory containing `CATEGORIES.md`, `link-skills.sh`, and the category folders. Confirm it exists before writing anything.

## Step C — Determine the category (infer, then confirm)
1. Read `CATEGORIES.md` (the map) and every `<category>/_category.md` **Scope** line.
2. Infer the best-fit category from the new skill's purpose.
3. **Confirm with the user** via AskUserQuestion — present your inferred category as the recommended option plus the closest alternatives. Never place silently.
4. **`personal/` is nested by domain.** If the target is personal, ask which domain subfolder (`personal/music/`, `personal/home/`, …). If the chosen domain doesn't exist yet, create the subfolder and a starter `_category.md` for it (scope, naming, tone, default frontmatter — mirror the format of the sibling `_category.md` files).

## Step D — Name & uniqueness
- Follow the **naming style in the target `_category.md`** (e.g. `design/refine/` = a single verb/adjective; `dev/` = verb-first; `docs/` = `<artifact>-writer`).
- Enforce kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`).
- **Pre-check global uniqueness:** scan every existing skill folder name (`find "$REPO" -name SKILL.md -exec dirname {} \; | xargs -n1 basename`). Skill names must be globally unique because they flatten into one directory when symlinked. If the name collides, pick another before creating.

## Step E — Scaffold at the right path, apply conventions
- Create the skill at `<repo>/<category-path>/<name>/SKILL.md` (e.g. `dev/my-skill/SKILL.md`, `personal/music/my-skill/SKILL.md`). Never at the repo root or cwd.
- Apply the target `_category.md`: **tone/audience**, **required scaffolding** (which of `references/`, `scripts/`, `assets/` it expects), and **default frontmatter** (usually `user-invokable: true`). Note: `personal/` allows a bare `SKILL.md` and non-English content; functional categories are English-first with trigger coverage.
- `name:` in frontmatter MUST equal the folder name.

## Step F — Link & verify (offer, one confirmation)
After the skill (and its references) are written:
1. **Offer to run the installer** — with a single confirmation: `bash "<repo>/link-skills.sh"`. This symlinks the new skill into `~/.claude/skills/`. (Don't run it silently; don't just leave a reminder — offer.)
2. **Run the concierge audit** to confirm the repo is still clean: `bash "<repo>/meta/concierge/scripts/audit.sh"`. Report the result. Fix anything it flags for the new skill before finishing.
3. Remind the user to **restart Claude Code / start a new session** for the new skill to become active.

## Project-context skills (special architecture)
If the skill's purpose is to carry **one specific project's context** (stack, layout,
conventions, gotchas) for the project-awareness router — e.g. `foleon-ripley` — it is NOT a
free-form skill. It **MUST** follow the standard at `docs/stds/PROJECT_CONTEXT_SKILL.md`:
place it under a work/client silo category (`foleon/`), name it `<silo>-<repo>`, scaffold
exactly `SKILL.md` + `references/project-facts.md` + `references/knowledge.md`, and register the
served repo in `hooks/awareness-ignore.txt` as `<repo> -> <skill>` (via
`hooks/awareness-ignore-add.sh . <skill>`). Use `foleon/foleon-ripley` as the template.

## Forward hook
Once a generated catalog/cheat-sheet exists at the repo root (README step 4), regenerate it after adding a skill so `god` and `concierge` stay fast and current. (No such file yet — skip until it exists.)
