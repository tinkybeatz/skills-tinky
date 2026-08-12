---
name: foleon-ripley
description: >-
  Project context for the `ripley` monorepo — Foleon's **current production**
  Docs editor and viewer: stack, `@foleon/*` package layout, commands,
  conventions and accumulated gotchas. Use for work in ripley's own code:
  `@foleon/editor`, `@foleon/viewer` / `viewer-dynamic`, or the **source** of any
  `@foleon/*` package (core, navigator, search, sdk, ui-design-system,
  cookie-consent). Trigger phrases: "ripley", "the ripley editor", "the ripley
  viewer", "foleon docs", "@foleon/editor", "@foleon/viewer", "viewer-dynamic",
  "../ripley", or explicit `/foleon-ripley`. **Not for `fio`** — the separate
  foleon.ai repo (`@foleonai/*`, `apps/editor` + `apps/api`) replacing ripley;
  it has its own skill, `foleon-fio`, and the two carry contradictory
  conventions, so never apply one's rules to the other. Disambiguation: on a bare
  "foleon" or "the editor app", choose by the working directory rather than
  defaulting here; and when work merely *consumes* a published `@foleon/*`
  package (fio dev-depends on `@foleon/core`), that is `foleon-fio` — only that
  package's source is this skill. Load it BEFORE senior-dev, test-writer or
  perf-analyzer act on ripley code so they inherit its conventions
  (arrow-functions-only, NO comments, Biome single-quote/120, Vitest+RTL+MSW
  tests in `__tests__`). Append non-obvious ripley discoveries to this skill's
  knowledge log — mirroring one to the Notion cheat sheet is
  `foleon-cheatsheet`'s job. Not for non-Foleon projects.
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
   hard-won specifics that aren't obvious from the code. Entries are indexed by
   **symptom**, so scan for what you're observing, not for the subsystem.
4. **Read the cheat sheet.** `references/cheatsheet-approved.md` is a verbatim mirror
   of the maintainer's own Notion cheat-sheet page. It is the most trustworthy layer —
   every line on it was explicitly approved by the maintainer before it was written —
   so when it disagrees with the log, it wins. It is generated; never edit it by hand.

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
- YYYY-MM-DD · <area> · <symptom> — <finding> · refs: <paths|tickets> · sheet: <yes|no|none>
```

`<area>` is one of: Editor · Viewer · Core / rendering · Build & tooling ·
Tests & Playwright · Conventions.

**Search before you append — with the script, not by eye** (PCS-6):
```bash
python3 ~/.claude/skills/foleon-cheatsheet/scripts/log.py check --project ripley --area "<area>" --symptom "<symptom>"
```
It exits non-zero when an existing entry is a likely duplicate; extend that entry and
refresh its date instead of adding a near-duplicate.

Keep entries **dense** — this file is read by an agent that reads all of it, so
completeness beats brevity here. Human-facing phrasing is a different job: the
`foleon-cheatsheet` skill decides whether a finding also earns a bullet on the
Notion cheat-sheet page, and **rewrites** it for a human if so — only after the
maintainer explicitly approves the exact wording in conversation. Don't write for
a human here, and don't mirror to Notion yourself.

When the log grows heavy, promote the stable facts up into
`references/project-facts.md` and prune the log.

## Boundary
**Repo mode:** silo-only

`ripley` is a shared work repo that must stay AI-config-free, so **all** of its context lives
here and nothing Claude-specific is ever written into its checkout (PCS-7, PCS-9).

This is Foleon-only. For any other project, use that project's own `CLAUDE.md`
(see the project-awareness system in the skills-tinky README) — not this skill.
Note that a Foleon repo the team *owns* may be **dual-home** instead (PCS-9a) — context split
between its committed `CLAUDE.md` and a skill. Don't copy this section into such a skill.

## References
- `references/project-facts.md` — the curated, stable project knowledge (load on use).
- `references/knowledge.md` — the growing, dated discoveries log (append to it).
- `references/cheatsheet-approved.md` — a verbatim mirror of the maintainer's Notion
  cheat-sheet page, generated by `foleon-cheatsheet` (read it; never edit it).

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Facts drift from reality | A command/convention here no longer matches ripley | Trust the live repo (`package.json`, `pnpm-workspace.yaml`, `biome.json`); fix `project-facts.md` and log the correction in `knowledge.md`. |
| Applied to the wrong project | Triggered on a non-Foleon repo | Stop; defer to that repo's own `CLAUDE.md`. This skill is Foleon-only. |
| **Crossed with `fio`** | Applied ripley's rules to fio (or quoted fio facts as ripley's) — the tell is a no-comments or Biome instruction landing in `fio`, whose `CLAUDE.md` *requires* explanatory comments + TSDoc and uses oxlint/oxfmt | Both repos are Foleon and both have an "editor app," so the names collide while the rules contradict. Establish which checkout you are in **before** applying anything; ripley facts stay in this skill's log, fio facts in `foleon-fio`'s. Never copy an entry between the two logs — if a fact is genuinely true of both, it is cross-repo and belongs to whichever log surfaced it (CHS-9b). |
| Convention conflict | Generic default vs a ripley rule | The ripley rule in `project-facts.md` wins; state which you followed. |
| Discovery lost | Learned something but didn't record it | Append it to `references/knowledge.md` before finishing the task. |
| Log bloat | `knowledge.md` sprawling / duplicative | Promote stable facts into `project-facts.md`, prune the log to what's still non-obvious. |
| Wrote for the wrong audience | Log entry reads like polished human copy, or a cheat-sheet bullet reads like the log | The log is dense and machine-facing; the sheet is scannable and human-facing. Hand mirroring to `foleon-cheatsheet` — never write both yourself. |
