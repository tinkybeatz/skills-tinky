---
name: foleon-ripley
description: >-
  Foleon project context for the `ripley` monorepo — stack, `@foleon/*` package
  layout, commands, conventions, and accumulated gotchas — so engineering work on
  Foleon acts with project awareness instead of blind. Use whenever a task touches
  Foleon / ripley: reviewing, writing, testing, debugging, refactoring, or planning
  code in the `editor` (`@foleon/editor`), `viewer` (`@foleon/viewer` /
  `viewer-dynamic`), or any `@foleon/*` package (core, navigator, search, sdk,
  ui-design-system, cookie-consent). Trigger phrases: "ripley", "foleon", "foleon
  docs", "foleon editor", "foleon viewer", "the editor app", "the viewer app",
  "@foleon", or explicit `/foleon-ripley`. Load it BEFORE senior-dev, test-writer,
  or perf-analyzer act on Foleon code so they inherit the conventions
  (arrow-functions-only, no comments, Biome single-quote/120, Vitest+RTL+MSW tests
  in `__tests__`). Also append non-obvious discoveries about ripley to this skill's
  knowledge log as you learn them — but mirroring a finding to the Notion cheat
  sheet is `foleon-cheatsheet`'s job, not this one's. Do NOT use for non-Foleon
  projects — those rely on their own repo CLAUDE.md.
user-invokable: true
---

# foleon-ripley

Project-context skill for **Foleon's `ripley` monorepo** (the Foleon Docs editor,
viewer, and publishing apps). It exists so your engineering skills act with Foleon
context **without that context living inside the shared `ripley` codebase** — the
knowledge stays here, in a skill you own.

## When this fires
Any task touching Foleon / ripley — reviewing, writing, testing, debugging, or
planning code in `editor`, `viewer`, or any `@foleon/*` package. It complements the
other skills rather than replacing them: it supplies the *facts and conventions*,
they do the work.

## How to use it
1. **Load the project facts first.** Read `references/project-facts.md` (stack,
   package layout, commands, conventions). Do this before acting so downstream skills
   (`senior-dev`, `test-writer`, `perf-analyzer`) inherit the right assumptions —
   e.g. arrow-functions-only, no comments in generated code, Biome single-quote/120,
   tests in `__tests__/*.test.tsx` with Vitest + RTL + MSW.
2. **Apply the conventions to whatever you produce** — code, reviews, tests, plans.
   When a convention here conflicts with a generic default, this file wins for ripley.
3. **Check the discoveries log.** Skim `references/knowledge.md` for gotchas and
   hard-won specifics that aren't obvious from the code.

## Keep it alive (self-enrich)
Whenever you learn something **non-obvious** about ripley — a gotcha, an implicit
convention, an architectural "why", a sharp edge — **append it to
`references/knowledge.md`**. Editing it via
`~/.claude/skills/foleon-ripley/references/knowledge.md` writes through to the
skills-tinky repo, so the knowledge accumulates in a repo you own — never in the
ripley checkout.

Entries follow the **PCS-6 schema** — one finding per entry, so the log can be
grouped and deduplicated without re-reading it:

```
- YYYY-MM-DD · <area> · <symptom> — <finding> · refs: <paths|tickets> · sheet: <CS-nn|none>
```

`<area>` is one of: Editor · Viewer · Core / rendering · Build & tooling ·
Tests & Playwright · Conventions.

**Search before you append.** If the finding is already logged, extend that entry
and refresh its date rather than adding a near-duplicate.

Keep entries **dense** — this file is read by an agent that reads all of it, so
completeness beats brevity here. Human-facing phrasing is a different job: the
`foleon-cheatsheet` skill decides whether a finding also earns a row in the Notion
cheat sheet, and **rewrites** it for a human if so. Don't write for a human here,
and don't mirror to Notion yourself.

When the log grows heavy, promote the stable facts up into
`references/project-facts.md` and prune the log.

## Boundary
This is Foleon-only. For any other project, use that project's own `CLAUDE.md`
(see the project-awareness system in the skills-tinky README) — not this skill.

## References
- `references/project-facts.md` — the curated, stable project knowledge (load on use).
- `references/knowledge.md` — the growing, dated discoveries log (append to it).

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Facts drift from reality | A command/convention here no longer matches ripley | Trust the live repo (`package.json`, `pnpm-workspace.yaml`, `biome.json`); fix `project-facts.md` and log the correction in `knowledge.md`. |
| Applied to the wrong project | Triggered on a non-Foleon repo | Stop; defer to that repo's own `CLAUDE.md`. This skill is Foleon-only. |
| Convention conflict | Generic default vs a ripley rule | The ripley rule in `project-facts.md` wins; state which you followed. |
| Discovery lost | Learned something but didn't record it | Append it to `references/knowledge.md` before finishing the task. |
| Log bloat | `knowledge.md` sprawling / duplicative | Promote stable facts into `project-facts.md`, prune the log to what's still non-obvious. |
| Wrote for the wrong audience | Log entry reads like polished human copy, or a cheat-sheet row reads like the log | The log is dense and machine-facing; the sheet is scannable and human-facing. Hand mirroring to `foleon-cheatsheet` — never write both yourself. |
