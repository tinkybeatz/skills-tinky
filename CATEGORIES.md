# Categories

The taxonomy for `skills-tinky`. Folders are a **filing system for humans** — they do not scope where a skill is active. Every skill, once symlinked into `~/.claude/skills/`, is available globally in every project. Project-specific behavior comes from each project's `CLAUDE.md`, not from the folder.

The source of truth for each category's conventions is its `_category.md` file. `skill-creator`, `concierge`, and `god` read these. The category of a skill is its **folder path** (there is no category field in frontmatter).

Entry points: **`god`** turns a goal into a plan across these skills ("/god i want to …"); **`concierge`** keeps the repo healthy; **`skill-creator`** authors new skills.

**Rule:** a folder is a *skill* if it directly contains a `SKILL.md`; otherwise it's an organizational folder. Skill folder names must be **globally unique** (they flatten into one directory when symlinked).

| Category | Purpose |
|---|---|
| `meta/` | Manage Claude Code, this repo, or the skill/agent toolchain |
| `dev/` | Software engineering: architecture, code, tests, review, VCS, ADRs |
| `infra/` | Ops, deploy, databases, sysadmin, security, static analysis |
| `design/build/` | Create interfaces, design-to-code, per-project design setup |
| `design/refine/` | Improve an existing interface along one dimension (design-partner suite) |
| `product/` | Product strategy, prioritization, business modeling, product review |
| `docs/` | Generate formal document deliverables (specs, standards, reports) |
| `notes/` | Notion workspace workflows (requires Notion MCP) |
| `research/` | Research, explanation, and media/content ingestion |
| `personal/` | Personal-life & side-project domains, organized into subfolders |

## Installing / updating

Run `./link-skills.sh` to (re)create the flat symlinks in `~/.claude/skills/`. It recurses the repo, links every `SKILL.md` folder by name, aborts on name collisions, and prunes stale links. A `git pull` alone updates existing skills live; re-run the script only when skills are added, removed, or moved.
