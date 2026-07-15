# Context Management — Keeping Skills & Agents Sharp

The biggest risk with skills and agents isn't writing them — it's **context
drift** over time. A skill that works perfectly today can silently degrade as
the codebase evolves, the user's needs shift, or the context window fills with
irrelevant content.

---

## The Progressive Disclosure Budget

Every token has a cost. Understanding where tokens go helps write efficient
skills:

| Layer | When loaded | Token budget | What belongs here |
|-------|-------------|-------------|-------------------|
| Description (metadata) | Every session, always | ~100 words max (1,536 chars) | Trigger conditions, key phrases, "when to use" |
| SKILL.md body | On trigger only | <500 lines ideal, <5k words max | Core workflow, decision logic, output format |
| references/ | On demand, when Claude reads them | Unlimited | Detailed patterns, examples, schemas, domain knowledge |
| scripts/ | Execute without loading into context | Unlimited | Deterministic code, validators, formatters |

**The critical insight**: after **compaction** (when Claude's context approaches
its limit and gets compressed), CLAUDE.md is re-read from disk and only the 5
most recently invoked skills are re-attached (5,000 tokens each, 25,000 combined
budget). Most recently invoked skills get priority. This means:

- A skill's core workflow should fit within 5,000 tokens to survive compaction
  intact
- Heavy reference material should stay in `references/` — it can be re-read on
  demand
- Scripts are ideal for deterministic tasks because they execute without
  consuming context tokens

---

## Writing Descriptions That Actually Trigger

The description is the single most important piece of text in a skill or agent.
It's the only content always in context, and it's the sole basis for Claude's
triggering decision.

**What makes a good description:**

1. **Include exact trigger phrases** — the words a user would actually type. Not
   abstract categories, but concrete phrases: "create a migration", "deploy to
   staging", "review this PR".

2. **Be a little pushy** — Claude tends to undertrigger. Add phrases like "Use
   this skill whenever the user mentions X, even if they don't explicitly ask
   for Y."

3. **Cover edge cases** — include non-obvious triggers. A deployment skill
   should also trigger on "push to prod", "ship it", "release this".

4. **Name competing skills** — if another skill covers adjacent territory,
   mention the boundary. "Use this for database migrations, NOT for schema
   design (use architecture-conceptor for that)."

5. **Use third person** — "This skill should be used when..." not "Use me
   when..."

**For agents**: the description field uses `<example>` blocks instead of
free-text trigger phrases. Include 2-4 concrete scenarios.

---

## Preventing Drift Over Time

Skills and agents degrade in two ways: **content rot** (instructions become
outdated) and **context pollution** (the skill grows bloated with accumulated
additions).

**Anti-drift checklist:**

1. **Separate facts from procedures.** Facts change (API endpoints, framework
   versions, team conventions). Procedures are more stable ("how to write a
   migration"). Put facts in `references/` where they can be updated without
   touching the core workflow.

2. **Date-stamp volatile content.** If a skill references specific versions,
   tool names, or external resources, note when this was last verified. A
   reference file that says "As of 2025-03: React 19 supports..." is easier to
   audit than one without dates.

3. **Include a "what this skill does NOT do" section.** Boundary clarity
   prevents scope creep. When the user or future editors want to add adjacent
   functionality, a clear "out of scope" section forces a conscious decision
   rather than gradual bloat.

4. **Keep the iteration loop tight.** The eval/benchmark workflow in this
   skill-creator isn't just for initial creation — run it periodically on
   existing skills to check for regression. If a skill's pass rate drops,
   investigate why.

5. **Prune aggressively.** For each line in a SKILL.md, ask: "Would removing
   this cause Claude to make mistakes?" If not, cut it. Lean skills are
   resilient skills — they survive compaction better and leave more room for
   the user's actual content.

---

## Cross-Tool Compatibility (AGENTS.md Bridge Pattern)

If the user works with multiple AI coding tools (Cursor, Codex, Gemini CLI,
etc.), recommend the **bridge pattern**:

- Maintain one `AGENTS.md` at the project root with all instructions
- Create a `CLAUDE.md` containing only `@AGENTS.md` (single-line import)
- Skills and agents remain tool-specific (in `.claude/skills/` and
  `.claude/agents/`)
- Facts and rules that should work across tools go in AGENTS.md, not in skills

This ensures instructions are portable without duplicating content across
tool-specific configs.
