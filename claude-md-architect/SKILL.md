---
name: claude-md-architect
description: Expert dedicated to creating, auditing, refactoring, and maintaining effective CLAUDE.md files. Use this skill whenever the user asks to audit a CLAUDE.md, score a CLAUDE.md, optimize a CLAUDE.md, create a CLAUDE.md from scratch, generate a CLAUDE.md, refactor a CLAUDE.md that is too long, trim a CLAUDE.md, organize the agentic ecosystem (CLAUDE.md vs skills vs hooks vs subagents vs MCP), diagnose "Claude isn't applying my instruction", "Claude ignores X", "where should this rule go". Also trigger when the user says "my CLAUDE.md is too long", "how should I structure my CLAUDE.md", "what should go in CLAUDE.md", "CLAUDE.md best practices", "improve my CLAUDE.md", "audit my Claude Code ecosystem". Skip if the request concerns another type of configuration file (settings.json, hooks, a standalone MEMORY.md) with no interaction with CLAUDE.md.
---

# CLAUDE.md Architect

Expert in creating, auditing, refactoring, and maintaining effective CLAUDE.md files. Based on official Anthropic documentation and consolidated community best practices.

---

## Founding principle

An effective CLAUDE.md is **short, specific, and well placed in the cascade**.

- It is a **user message** injected into every session, not a system prompt → probabilistic guidance, not enforcement.
- Anything beyond **200 lines degrades adherence**; aim for **< 60 lines** for the root file.
- For rules that must be strictly enforced → **hooks**, not CLAUDE.md.

Canonical source: [Anthropic — memory.md](https://code.claude.com/docs/en/memory.md)

---

## Invocation modes

Identify the mode from the very first message:

| Mode | Signal | Primary action |
|---|---|---|
| 🔍 **Audit** | "score", "audit", "evaluate my CLAUDE.md" | Read the file → apply the rubric → produce a /100 score + diff |
| 🆕 **Create** | "create", "generate a CLAUDE.md for this project" | Short interview → generate < 60 lines WHAT/WHY/HOW |
| ✂️ **Refactor** | "too long", "optimize", "trim" | Audit → reallocate to skills/hooks/rules/MEMORY.md |
| 🔧 **Diagnose** | "Claude isn't applying X", "Claude ignores" | 5-step procedure (see `references/diagnostic-flow.md`) |
| 🗺️ **Architecture** | "where should this rule go", "organize my ecosystem" | Placement matrix: CLAUDE.md vs skill vs hook vs subagent |

If ambiguous, ask explicitly.

---

## Mode 🔍 Audit — workflow

1. **Read** the target CLAUDE.md file(s) (root, user global, subdirectories) plus the adjacent ecosystem (`.claude/skills/`, `.claude/rules/`, `MEMORY.md` if relevant).
2. **Measure** each dimension of the rubric (see `references/scoring-rubric.md`) → /100 score per dimension + weighted overall score.
3. **Detect** anti-patterns (see `references/anti-patterns.md`) → list of occurrences with line numbers.
4. **Map** cross-file duplication (CLAUDE.md ↔ skills ↔ MEMORY.md ↔ rules) if multiple files are provided.
5. **Deliver**:
   - Overall score + per-dimension scores (table)
   - Top 3 priority issues
   - A concrete diff/patch of the proposed CLAUDE.md (before/after)
   - A migration plan for the trimmed content (where does it go?)

**Required output format:**

```
## 📊 Overall score: XX/100 — [Excellent / Good / Needs rework]

| Dimension | Score | Target | Status |
|---|---|---|---|
| Size | X/10 | < 60 lines | ✅ / ⚠️ / ❌ |
| ... | ... | ... | ... |

## 🚨 Top 3 issues
1. [Anti-pattern] line X — [short explanation]
2. ...

## 🔧 Proposed CLAUDE.md (diff)
[unified diff block, or full new content if a complete rewrite]

## 📦 Migration of trimmed content
- "X" → skill `skill-name` (reason: multi-step procedure)
- "Y" → PreToolUse hook (reason: enforcement required)
- "Z" → `.claude/rules/architecture.md` (reason: conditional cross-cutting rule)
```

---

## Mode 🆕 Create — workflow

1. **Short interview** (max 5 questions):
   - Primary tech stack?
   - Project type (library / app / monorepo / client work)?
   - 2-3 conventions/constraints that really matter?
   - Audience for the CLAUDE.md (solo / team / open-source)?
   - Are there already skills/rules/hooks?

2. **Generate** a CLAUDE.md structured as **WHAT / WHY / HOW**:
   - **WHAT** — stack, project structure, working language (3-8 lines)
   - **WHY** — project purpose, critical business constraints (2-5 lines)
   - **HOW** — key commands (test, build, lint), verifiable conventions, "always do X" (10-30 lines)

3. **Apply progressive disclosure** if > 60 lines:
   - Extract conditional cross-cutting rules into `.claude/rules/<topic>.md`
   - Import with `@.claude/rules/<topic>.md` (max 5 hops)
   - Suggest skills for repeatable workflows

4. **Choose the right location** in the cascade:
   - Cross-cutting personal preferences → `~/.claude/CLAUDE.md`
   - Team standards for a project → `<project>/CLAUDE.md` (committed)
   - Personal local notes for a project → `<project>/CLAUDE.local.md` (gitignored)

See `references/templates.md` for 5 ready-to-use templates.

---

## Mode ✂️ Refactor — workflow

1. **Full audit** (Mode 🔍) → score what exists.
2. **Categorize each line/section** using the placement matrix:

   | Content type | Optimal destination |
   |---|---|
   | Multi-step procedure | → Skill |
   | Rule to enforce (no exceptions) | → Hook |
   | Conditional cross-cutting rule (path-scoped) | → `.claude/rules/<scope>.md` |
   | Personal preference (style, tone) | → `~/.claude/CLAUDE.md` or MEMORY.md |
   | Dense reference (API, schemas) | → Reference-style skill |
   | Technical configuration | → `settings.json` |
   | Short, universal "always do X" | → CLAUDE.md (stays) |

3. **Produce 3 deliverables**:
   - The new slim CLAUDE.md
   - The list of files to create (skills, rules, hooks) with their content
   - A migration script or checklist

See `references/decision-matrix.md` for the complete matrix and concrete examples.

---

## Mode 🔧 Diagnose — workflow

Follow the official Anthropic 5-step procedure — see `references/diagnostic-flow.md`.

Quick summary:
1. `/memory` → confirm the file is actually loaded
2. Check the location in the cascade
3. Make the instruction more specific (test: can it be verified objectively?)
4. Look for cross-level contradictions
5. If critical → migrate to a hook

---

## Mode 🗺️ Architecture — workflow

The user asks "where should this rule go" or "organize my ecosystem".

1. **Read** the rule/content in question.
2. **Apply the placement matrix** (`references/decision-matrix.md`).
3. **Verify** that no equivalent rule already exists elsewhere (anti-duplication).
4. **Propose** the location with justification + a concrete diff.

---

## Core knowledge (always keep in mind)

### 5-level concatenated hierarchy (top-to-bottom, from most conceptually authoritative to least)

1. **Managed policy** (org/IT) — `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS)
2. **User global** — `~/.claude/CLAUDE.md`
3. **Project root** — `./CLAUDE.md` or `./.claude/CLAUDE.md`
4. **Project local** — `./CLAUDE.local.md` (not committed)
5. **Subdirectory** — `./<subdir>/CLAUDE.md` (lazy-loaded on file access)

Discovery works by **walk-up** from the CWD to the git root. All levels are concatenated (not overwritten). On conflict: Claude may arbitrate arbitrarily → maintain consistency manually.

Full details: `references/hierarchy.md`.

### Imports

- Syntax: `@path/to/file` (relative to the host file)
- Max depth: **5 recursive hops**
- First external import → approval dialog
- Enables the progressive disclosure pattern

### Surviving compaction

- ✅ Project root (`./CLAUDE.md`): reloaded from disk after `/compact`
- ❌ Subdirectories: no automatic reload

### Native Claude Code tools

- `/memory` — lists loaded files, toggles auto memory
- `/context` — shows token consumption
- `InstructionsLoaded` hook — deterministic logging

---

## Golden rules (apply consistently)

1. **Always measure before editing** — score BEFORE, score AFTER.
2. **Prefer removal over addition** — every line consumes context in every session.
3. **One rule = one destination** — never the same rule in CLAUDE.md AND a skill AND MEMORY.md.
4. **Verifiability > politeness** — "Use 2-space indentation" always beats "format properly".
5. **If a rule must be strictly enforced → hook, not CLAUDE.md.**
6. **Cite Anthropic sources** in recommendations to anchor authority.

---

## Failure modes & recovery

| Failure | Signal | Corrective action |
|---|---|---|
| Audit with no source file | The user didn't provide a path | Ask for the path OR read `~/.claude/CLAUDE.md` by default and confirm it |
| Refactor without ecosystem context | No access to existing skills/rules | Ask for the project `pwd` or list `~/.claude/skills/` |
| Score < 50/100 with no clear cause | Multiple anti-patterns mixed together | Do a radical refactor (clean-slate WHAT/WHY/HOW) rather than micro-fixes |
| User conflict ("I want to keep X") | Disagreement over a removal | Document the user's reason in an HTML comment `<!-- kept because X -->` (not sent to the model) |
| Recommendation contradicting Anthropic docs | Web source vs official source | Always prefer Anthropic; flag the divergence to the user |
| CLAUDE.md already optimal (> 85/100) | Nothing to improve | Say so explicitly; don't invent cosmetic changes |
| Request mixing CLAUDE.md + another file | Fuzzy scope | Handle CLAUDE.md first, then suggest a dedicated skill for the other file |
| Multi-step procedure left in CLAUDE.md | Anti-pattern not eliminated after refactor | Re-check: if > 3 steps, it's a skill, not a CLAUDE.md instruction |

---

## Additional resources

Load only if needed for the active mode:

| File | When to read it |
|---|---|
| `references/scoring-rubric.md` | Audit mode — detailed 9-dimension rubric, score calculation |
| `references/anti-patterns.md` | Audit / Refactor mode — catalog of the 10 anti-patterns with before/after examples |
| `references/hierarchy.md` | Create / Architecture mode — cascade details, imports, conflicts |
| `references/decision-matrix.md` | Refactor / Architecture mode — where to place each type of content |
| `references/templates.md` | Create mode — 5 ready-to-use templates (library, app, monorepo, client, personal) |
| `references/diagnostic-flow.md` | Diagnose mode — detailed 5-step procedure |

---

## Source references (official docs)

- [Anthropic — Memory & CLAUDE.md](https://code.claude.com/docs/en/memory.md)
- [Anthropic — Features overview](https://code.claude.com/docs/en/features-overview.md)
- [Anthropic — Context window](https://code.claude.com/docs/en/context-window.md)
- [Anthropic — Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)
- [Anthropic — Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

Community best practices: [humanlayer.dev](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [geuneda/claude-md-optimizer](https://github.com/geuneda/claude-md-optimizer).
