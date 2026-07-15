# Audit checklist — what "clean and strong" means

Each item below is either checked mechanically by `scripts/audit.sh` (marked ⚙️) or requires your judgment (marked 🧠). Severity: **WARN** = should fix; **INFO** = heads-up.

## Structure & naming
- ⚙️ **WARN — SKILL.md casing.** Every skill's manifest is `SKILL.md` (uppercase). A lowercase `skill.md` works on macOS but is invisible to Claude Code on case-sensitive Linux/CI. Fix: `git mv skill.md SKILL.md` (via a temp name on a case-insensitive FS).
- ⚙️ **WARN — folder name is kebab-case.** `^[a-z0-9]+(-[a-z0-9]+)*$`. The folder name is the invocation name; keep it lowercase-hyphenated.
- ⚙️ **WARN — duplicate skill names.** Skill folder basenames must be globally unique — they flatten into one directory when symlinked, so two `foo/` folders collide. Fix: rename one.
- ⚙️ **INFO — subfolder naming.** Prefer `references/` (not singular `reference/`); pick one of `evals/`/`evaluations/` repo-wide. Cosmetic but keeps the repo predictable.

## Frontmatter
- ⚙️ **WARN — `name:` present and equals the folder name.** Claude Code discovery and invocation rely on this match.
- ⚙️ **WARN — `description:` present.** Without it the skill won't trigger reliably.
- 🧠 **WARN — trigger coverage.** The `description:` should list the natural phrases a user would actually say (English first; add French equivalents where the user works in French). A one-liner with no triggers is thin — the skill won't auto-activate. Propose an enriched description.
- 🧠 **INFO — `user-invokable`, `args`, `metadata`.** Present and structurally sane where the skill expects explicit invocation or arguments.

## Taxonomy
- ⚙️ **WARN — skill outside the taxonomy.** Every `SKILL.md` must live under a folder whose ancestor chain contains a `_category.md`. An orphan at the repo root or in an unregistered folder should move into a category (or a new category should be created with its own `_category.md`).
- 🧠 **INFO — category fit.** Does the skill match its folder's `_category.md` **Scope**? If it reads like it belongs elsewhere, recommend a move. This is advisory — warn, don't block.
- 🧠 **INFO — convention drift.** Naming style, tone/audience, and required scaffolding should match the folder's `_category.md`.

## Health & hygiene
- ⚙️ **WARN — symlink health.** Each skill has exactly one correct symlink in `~/.claude/skills/` pointing at its real folder; no broken or stale links pointing into the repo. Fix: run `link-skills.sh`.
- 🧠 **INFO — overlap/duplication.** Two skills doing nearly the same job dilute routing accuracy. Recommend merging or sharpening the boundary (and tightening both descriptions).
- 🧠 **INFO — secrets.** No tokens/keys/passwords committed in any skill file. Flag for redaction if found.

## How to report
Rank findings by severity: broken symlinks and invalid/missing frontmatter first (they break discovery), then taxonomy, then cosmetic drift. For each: `path → problem → proposed fix`. Batch the safe mechanical fixes behind one confirmation; propose content changes individually.
