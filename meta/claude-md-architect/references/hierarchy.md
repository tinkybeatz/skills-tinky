# CLAUDE.md hierarchy — in-depth guide

Canonical source: [Anthropic — memory.md](https://code.claude.com/docs/en/memory.md).

## Full cascade (5 levels)

| # | Scope | Path | Who loads it | When | Versioned? |
|---|---|---|---|---|---|
| 1 | **Managed** | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br/>Linux: `/etc/claude-code/CLAUDE.md`<br/>Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | IT/DevOps | Session start | Managed by IT |
| 2 | **User global** | `~/.claude/CLAUDE.md` | User | Session start | No (personal) |
| 3 | **Project root** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team | Session start | Yes (committed) |
| 4 | **Project local** | `./CLAUDE.local.md` | User (on the project) | Session start | No (gitignored) |
| 5 | **Subdirectory** | `./<subdir>/CLAUDE.md` | Variable | Lazy (on file access) | Depends on scope |

**Key rule**: all levels are **concatenated**, not overwritten. CLAUDE.local.md is appended after CLAUDE.md at the same level.

---

## Discovery by walk-up

Claude Code walks up the tree from the **CWD** (current working directory) to the git root (or filesystem root). At each level, it looks for `CLAUDE.md` and `CLAUDE.local.md`.

Example: CWD = `~/projects/acme/backend/src/auth/`

Loaded files:
1. Managed (if present)
2. `~/.claude/CLAUDE.md`
3. `~/projects/acme/CLAUDE.md` (if git root)
4. `~/projects/acme/CLAUDE.local.md` (if present)
5. `~/projects/acme/backend/CLAUDE.md` (if present — loaded on file access under `backend/`)
6. `~/projects/acme/backend/src/auth/CLAUDE.md` (if present — lazy)

---

## Imports `@path/to/file`

### Syntax

```markdown
See @README.md for project context.
Testing standards: @.claude/rules/testing.md
Personal preferences: @~/.claude/preferences.md
```

### Rules

- Paths are **relative to the host file** (not to the CWD)
- Absolute paths supported (`@~/...`)
- Max depth: **5 recursive hops**
- The first external import (outside the project tree) → **security approval dialog**

### Progressive disclosure pattern

```markdown
# CLAUDE.md (root — 35 lines)

## Stack
- React + TypeScript + Vite
- Tests: Vitest

## Conventions
- See @.claude/rules/conventions.md

## Architecture
- See @.claude/rules/architecture.md

## Security
- See @.claude/rules/security.md
```

Each modular rule file is loaded only if CLAUDE.md references it and the session touches it.

---

## Surviving compaction

| File | Reloaded after `/compact`? |
|---|---|
| `~/.claude/CLAUDE.md` (user global) | ✅ Yes |
| `./CLAUDE.md` (project root) | ✅ Yes |
| `./.claude/CLAUDE.md` (root variant) | ✅ Yes |
| `./CLAUDE.local.md` | ✅ Yes |
| `./<subdir>/CLAUDE.md` | ❌ Not automatically (reloaded on the next file access under `<subdir>/`) |
| Files imported via `@path` | ✅ If the host CLAUDE.md reloads, so do its imports |

**Practical implication**: truly critical rules → root (never in a subdirectory alone).

---

## Cross-level conflicts

**Documented Anthropic behavior**:
> "When instructions conflict, Claude may pick one arbitrarily."

**No deterministic override**. All levels are concatenated and presented to Claude, which must reconcile them.

### Strategies

1. **Manual consistency** — audit periodically with `/memory` + a diff across levels.
2. **Scope specialization** — avoid a rule appearing at 2 levels; pick the most specific relevant one.
3. **HTML comments** — `<!-- kept because X -->` (not sent to the model) to document why a rule exists at a given level.

### Anthropic design principle

> "Personal state or cross-project coordination → global; team-shareable project config → project level."

| Rule type | Right level |
|---|---|
| Personal style (informal address, language, tone) | `~/.claude/CLAUDE.md` |
| Team code conventions | `<project>/CLAUDE.md` |
| Personal notes on this project (WIP tasks, local secrets) | `<project>/CLAUDE.local.md` |
| Technical sub-domain standards | `<project>/<subdir>/CLAUDE.md` |
| Org security policy | Managed |

---

## Auto memory (MEMORY.md) vs CLAUDE.md

| Aspect | CLAUDE.md | MEMORY.md (auto memory) |
|---|---|---|
| Who writes it | You | Claude (learns it) |
| Content | Rules, conventions | Detected preferences, learnings |
| Scope | 5-level cascade | Per worktree |
| Loading | Complete | First 200 lines OR 25 KB |
| Use case | "Claude must always do X" | "Claude noticed I prefer Y" |

**Golden rule**: if you want to write it yourself → CLAUDE.md. If Claude should learn it by observation → let MEMORY.md handle it.

---

## Quick diagnosis of a hierarchical setup

Useful commands:

```bash
# List everything that would be loaded from this CWD
/memory          # in Claude Code

# Visualize the weight of each source
/context         # in Claude Code

# Inspect the user global file
cat ~/.claude/CLAUDE.md | wc -l

# List the project's CLAUDE.md files
find . -name "CLAUDE.md" -not -path "*/node_modules/*"

# Detect CLAUDE.local.md files (potentially gitignored)
find . -name "CLAUDE.local.md"
```
