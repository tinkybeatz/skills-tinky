---
name: foleon-fio
description: >-
  Project context for `fio` — the **foleon.ai** monorepo (`@foleonai/*`)
  replacing Foleon's older `ripley` editor. Use for any fio work: `apps/editor`,
  `apps/api`, `apps/editor-e2e`, or `packages/*` (compiler, document-mutations,
  db, permissions, sdk-codegen, core-bridge, api-client, chat-contracts,
  pdf-extraction, template-db). Trigger phrases: "fio", "foleon.ai", "foleonai",
  "@foleonai", "the new editor", "the fio editor", "apps/editor", "apps/api", or
  explicit `/foleon-fio`. **Not `foleon-ripley`:** ripley is the OLD production
  editor at `../ripley` (read-only); fio's `CLAUDE.md` says to consult it for
  "what should this behaviour be", so load `foleon-ripley` for ripley's
  behaviour and this skill for fio's own code — both may apply at once. fio
  dev-depends on published `@foleon/*` packages (e.g. `@foleon/core`), so
  *consuming* one is still this skill; only that package's source is
  `foleon-ripley`. Never carry a convention across: fio requires explanatory
  comments + TSDoc and uses oxlint/oxfmt, ripley forbids comments and uses
  Biome. fio is **dual-home**: its team-owned `CLAUDE.md`, `AGENTS.md`,
  `CONTEXT.md`, `docs/` and `.claude/` are read as a source of truth alongside
  this skill, which never writes into the fio checkout. Append non-obvious fio
  discoveries to this skill's knowledge log — mirroring one to the Notion cheat
  sheet is `foleon-cheatsheet`'s job.
user-invokable: true
---

# foleon-fio

Project-context skill for **`fio`**, the foleon.ai monorepo — the AI-driven document
editor and API that replace `ripley`. It carries *your* accumulated knowledge of fio;
the team's own committed docs carry theirs. Both are real, and you read both.

**Repo mode:** dual-home

## When this fires
Any task touching fio — `apps/editor`, `apps/api`, `apps/editor-e2e`, or `packages/*`.
It supplies facts and hard-won gotchas; other skills (`senior-dev`, `test-writer`,
`react-doctor`) do the work.

## How to use it
fio is **dual-home** (PCS-9a): context lives in two places and **both are sources of
truth**. Read them in this order.

1. **The repo's own committed context — first, and directly.** It is team-authored and
   authoritative: `CLAUDE.md` (the "check ripley first" rule, ui-kit rules, comment
   policy, Fallow), `AGENTS.md`, `CONTEXT.md`, and before touching either app its
   `apps/<app>/ARCHITECTURE.md`. `references/project-facts.md` indexes the rest by path —
   it does **not** copy them, so read the real files.
2. **Load `references/project-facts.md`.** An index into the repo's docs, plus the
   *delta*: facts the team's docs don't cover.
3. **Check `references/knowledge.md`.** Dated gotchas, indexed by **symptom** — scan for
   what you're observing, not for the subsystem.
4. **On conflict**, the live repo wins for anything *verifiable* (a command, version,
   path) and this skill gets corrected. That is a staleness tiebreak, not a ranking:
   neither source overrides the other in general.

## Recording what you learn
Append non-obvious findings to `references/knowledge.md`, one entry per finding:

```
- YYYY-MM-DD · <area> · <symptom> — <finding> · refs: <paths|tickets> · sheet: <yes|no|none>
```

**Search the log for the finding's key terms first** — on a match, extend and re-date
that entry instead of appending a near-duplicate. Entries may be dense and jargon-heavy;
the reader is an agent. When the log grows heavy, promote stable facts into
`project-facts.md` and prune.

## Boundary
**Never write to anything inside the fio checkout** — not `CLAUDE.md`, not `docs/`, not
`.claude/`. Those files are the team's (`CLAUDE.md` is 17 commits by sven and Sean
Reilly, none of them yours). Everything you learn goes in this skill's `references/`.
Getting a finding into the team's docs is a **pull request you open by hand** — a human
decision, never an action this skill takes (PCS-7).

`ripley` is likewise read-only, and it is a *different* repo: use `foleon-ripley` for it.

## References
- `references/project-facts.md` — index into fio's own docs + the delta (load on use).
- `references/knowledge.md` — the dated discoveries log (append to it).
- `references/cheatsheet-approved.md` — generated mirror of `Fio`'s Notion cheat-sheet
  pages, written by `foleon-cheatsheet` (read it; never edit it).

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Read only one source | Applied a convention from this skill that `CLAUDE.md` contradicts, or missed a rule the team documented | Both are authoritative — re-read the repo's own context, then this skill. Correct whichever holds the stale *verifiable* fact. |
| Wrote into the fio checkout | A `CLAUDE.md`/`docs/` diff appears in fio's `git status` | Revert it. Move the content into `references/knowledge.md`. If it genuinely belongs to the team, open a PR instead. |
| Confused with ripley | Applied ripley's conventions (Biome, no-comments) to fio, or vice versa | They are different repos with different rules. fio uses oxlint + oxfmt and *requires* comments explaining "why"; ripley forbids them. Check which repo you're in. |
| Facts drift | A path or command here no longer matches fio | Trust the live repo (`package.json`, `turbo.json`, `pnpm-workspace.yaml`); fix `project-facts.md` and log the correction. |
| Restated the team's docs | `project-facts.md` starts explaining fio's conventions rather than pointing at them | Cut it back to a pointer. Duplicated prose goes stale while the original moves on (PCS-9a). |
| Discovery lost | Learned something non-obvious but didn't record it | Append to `references/knowledge.md` before finishing the task. |
