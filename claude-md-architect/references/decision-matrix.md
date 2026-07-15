# Decision matrix — where to place each type of content

The primary tool for Mode 🗺️ Architecture and Mode ✂️ Refactor.

---

## Main matrix

| Content type | Optimal destination | Why |
|---|---|---|
| Short, universal "always do X" rule | **CLAUDE.md** root | Always-on, cheap |
| Security-critical "never do X" rule | **PreToolUse hook** | Deterministic enforcement |
| Multi-step procedure (≥ 3 steps) | **Skill** | Explicit invocation, no session bloat |
| Workflow triggered by `/<name>` | **Skill** (`disable-model-invocation: true`) | Explicit trigger |
| Reference documentation (API, schemas) | **Reference-style skill** | Loaded on demand |
| Cross-cutting but conditional rule (path-scoped) | **`.claude/rules/<scope>.md`** | Modular, importable |
| Cross-cutting personal preference | **`~/.claude/CLAUDE.md`** | Follows the user |
| Personal preference for this project | **`<project>/CLAUDE.local.md`** | Personal, not committed |
| Technical configuration (permissions, env, model) | **`settings.json`** | Not natural language |
| Connection to an external system | **MCP server** | Integration standard |
| Isolated task to run in parallel | **Subagent** (`.claude/agents/`) | Isolated context |
| Learning / pattern observed by Claude | **MEMORY.md** (auto memory) | Claude writes it itself |
| Reference code snippet | **`file:line` pointer in CLAUDE.md** | The code stays where it is |
| Long explanatory text (architecture, tradeoffs) | **Project `docs/` (markdown)** + a pointer in CLAUDE.md | Not loaded every session |

---

## Concrete cases — before/after examples

### Case 1: "Always validate user input"

**Bad**: in CLAUDE.md (too vague, not verifiable).

**Good**:
- CLAUDE.md: `- Validation: use zod schemas (see src/schemas/)`
- + PostToolUse hook that greps for a missing `parse(` on new endpoints

### Case 2: "Release procedure"

**Bad**: 15 lines of procedure in CLAUDE.md.

**Good**:
- CLAUDE.md: `- Release: use /release` (1 line)
- Skill `~/.claude/skills/release/SKILL.md` with `disable-model-invocation: true`

### Case 3: "The project uses React + TypeScript + Vite + Vitest"

**Bad**: drowned in 8 paragraphs of description.

**Good**: a bulleted `## Stack` section at the top of CLAUDE.md.

### Case 4: "Component naming convention"

**Bad**: 30 lines of examples in CLAUDE.md.

**Good**:
- CLAUDE.md: `- Component naming: see @.claude/rules/naming.md`
- `.claude/rules/naming.md`: detailed rules with examples

### Case 5: "Never commit into .env"

**Bad**: just one line in CLAUDE.md (Claude might ignore it).

**Good**:
- PreToolUse hook that blocks edits to `.env`
- `.gitignore` that includes `.env`
- (Optional) a line in CLAUDE.md to document it

### Case 6: "The user prefers short explanations"

**Bad**: in a committed `<project>/CLAUDE.md` (personal preference).

**Good**: `~/.claude/CLAUDE.md`, or let auto memory learn it.

### Case 7: "Stripe API documentation used by the project"

**Bad**: 200 lines of docs in CLAUDE.md.

**Good**:
- Skill `~/.claude/skills/stripe-reference/` with the full docs in `references/`
- Triggers on "stripe", "payment", "stripe webhook"

---

## Quick-decision tree

```
Initial question:
"Does Claude need to know this on EVERY session, in this project?"

├── YES, and it's short (< 3 lines) and universal
│   └── → CLAUDE.md root
│
├── YES, but it's long or conditional
│   └── → CLAUDE.md reference + .claude/rules/<topic>.md (@ import)
│
├── YES, but it's personal (not team)
│   └── → ~/.claude/CLAUDE.md or <project>/CLAUDE.local.md
│
├── NO, it's on-demand / contextual
│   ├── Executable workflow → Skill
│   ├── Dense reference → Reference-style skill
│   ├── External connection → MCP
│   └── Isolated parallel task → Subagent
│
└── NO, it must be EXECUTED (not read)
    └── → Hook (PreToolUse / PostToolUse / Stop / etc.)
```

---

## Classic anti-decisions

| Temptation | Why it's bad | What to do instead |
|---|---|---|
| "I'll put everything in CLAUDE.md so Claude knows it all" | Bloat → degraded adherence | Index in CLAUDE.md + skills/rules |
| "I'll put my deploy procedure in CLAUDE.md" | It's a workflow, not a rule | Skill `/deploy` |
| "I'll put the security rule in CLAUDE.md" | Not enforced | PreToolUse hook |
| "I'll duplicate it in `~/.claude/CLAUDE.md` AND `<project>/CLAUDE.md`" | Guaranteed drift | Single source, at the highest level needed |
| "I'll put my personal style in the team CLAUDE.md" | Team pollution | `CLAUDE.local.md` or user global |

---

## Migration test (before/after refactor)

After any refactor, check:

1. **Is the root CLAUDE.md < 60 lines?** If not → keep trimming.
2. **Does each rule have exactly ONE destination?** Grep across files, remove duplicates.
3. **Are the security-critical rules in hooks, not only in CLAUDE.md?**
4. **Are the multi-step workflows in skills?**
5. **Are the `@path` imports ≤ 5 hops?**
6. **Did the audit score go up?** (re-run Mode 🔍 Audit)
