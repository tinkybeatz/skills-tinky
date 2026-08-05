# Standard — Project-Context Skill (PCS)

| Field | Value |
|---|---|
| **Status** | Active |
| **Version** | 2.0.0 |
| **Owner** | skills-tinky maintainer |
| **Approvers** | skills-tinky maintainer |
| **Effective date** | 2026-07-20 |
| **Applies to** | Every skill whose purpose is to carry one specific project's context in `skills-tinky` |

---

## Problem

The project-awareness router (`hooks/session-claude-md-check.sh`) promises that when you
open a shared/work repo mapped as `<repo> -> <skill>` in `hooks/awareness-ignore.txt`, it
will tell Claude to load that skill for context. That promise is only dependable if **every
project-context skill is built the same way** — same files, same self-enrich loop, same
boundaries. Without a strict architecture, these skills drift, the router points at
inconsistent things, and project knowledge leaks into repos that must stay AI-config-free.

**Success metrics** — see [§ Metrics](#metrics). In short: 100% of mapped repos resolve to a
conforming skill, and **zero** AI/context files are committed into a served project's checkout.

## Scope

**In scope:** skills that exist to supply one project's context (stack, layout, conventions,
gotchas) to other skills — e.g. `foleon/foleon-ripley` (the reference implementation).

**Out of scope:** reusable cross-project skills (`dev/`, `infra/`, …); the per-repo `CLAUDE.md`
system (see [PCS-9](#pcs-9-exclusivity-vs-the-in-repo-claudemd-system)); personal-domain skills (`personal/`).

---

## Normative rules

### PCS-1 Placement
- A project-context skill **MUST** live under a work/client silo category folder that has its
  own `_category.md` (e.g. `foleon/`). `[SRC-001]` `[SRC-003]`
- It **MUST NOT** live in `personal/` or in a functional category (`dev/`, `infra/`, …). `[SRC-003]`

**Enforcement:** concierge taxonomy check (every skill under a `_category.md` ancestor); review.

### PCS-2 Naming & deterministic mapping
- The skill folder name **MUST** be `<silo>-<repo>` in kebab-case and globally unique
  (e.g. repo `ripley` in silo `foleon` → `foleon-ripley`). `[SRC-001]` `[SRC-002]`
- The name **MUST** be the exact target of the served repo's `<repo> -> <skill>` line in
  `hooks/awareness-ignore.txt` (see [PCS-8](#pcs-8-registration)). `[SRC-002]`

**Enforcement:** router resolves the mapped name to an installed skill; concierge uniqueness check.

### PCS-3 Required file structure
A conforming skill **MUST** contain exactly these files (more `references/` allowed):
```
<silo>/<silo>-<repo>/
├── SKILL.md
└── references/
    ├── project-facts.md
    └── knowledge.md
```
`[SRC-001]`

**Enforcement:** conformance checklist; proposed concierge check.

### PCS-4 SKILL.md content
`SKILL.md` **MUST**:
- set `user-invokable: true` and a `description` containing **both** natural trigger phrases
  (repo name, product name, app names) **and** the explicit `/skill` invocation; `[SRC-001]` `[SRC-004]`
- contain: a "how to use" flow (**load `project-facts.md` → apply conventions → check
  `knowledge.md`**), a self-enrich instruction ([PCS-6](#pcs-6-knowledgemd-discoveries-log)),
  a boundary statement ([PCS-9](#pcs-9-exclusivity-vs-the-in-repo-claudemd-system)), and a
  **failure-modes table**. `[SRC-001]` `[SRC-005]`
- **SHOULD** stay under ~80 lines (project facts belong in `references/`, not here). `[SRC-005]`

**Enforcement:** skill-creator authoring + constraint validation; review.

### PCS-5 project-facts.md
- **MUST** hold curated, **stable** knowledge only: stack, package/layout, commands, and
  **verifiable** conventions. `[SRC-001]`
- **MUST** be treated as the authoritative reference; when a fact goes stale, the live served
  repo (`package.json`, config) wins and this file **MUST** be corrected. `[SRC-001]`

### PCS-6 knowledge.md (discoveries log)
- **MUST** be a dated, append-only log for non-obvious findings, **one entry per finding**. `[SRC-001]`
- Each entry **MUST** follow the structured schema:
  ```
  - YYYY-MM-DD · <area> · <symptom> — <finding> · refs: <paths|tickets> · sheet: <yes|no|none>
  ```
  `<area>` **SHOULD** roughly track the mirror's own headings (PCS-11) so the two stay easy to
  cross-reference, but it is not a controlled enumeration shared with the mirror — the mirror has no
  properties to share. `sheet: yes` = mirrored onto the page; `sheet: no` = proposed and declined;
  `sheet: none` = never evaluated or rejected by the gates. `[SRC-006]`
- Before appending, the writer **MUST** search the log for the finding's key terms. On a match it
  **MUST** extend or correct the existing entry and refresh its date, rather than append a
  near-duplicate. `[SRC-006]`
- Where a **script** exists for that search, the writer **MUST** use it rather than judging by eye —
  a dedupe rule enforced only by instruction is the weakest link in the system. Reference
  implementation: `foleon/foleon-cheatsheet/scripts/log.py check`. `[SRC-006]`
- Entries **MAY** stay dense, multi-clause and jargon-heavy — the audience is an agent that reads the
  whole file. Human-facing rewriting happens **only** in the mirror (PCS-11). `[SRC-006]`
- **MUST** state that when it grows heavy, stable facts are promoted into `project-facts.md`
  and the log pruned. `[SRC-001]`

**Enforcement:** review; the append path performs the pre-append search (PCS-6 dedupe).

### PCS-7 Self-enrich boundary (critical)
- New discoveries **MUST** be written to this skill's `references/knowledge.md` inside
  `skills-tinky` (a repo the maintainer owns). `[SRC-002]`
- The skill **MUST NOT** write `CLAUDE.md`, `.claude/`, or any AI/context file into the served
  project's checkout. `[SRC-002]`

**Enforcement:** served repo git status stays free of AI files (metric); review.

### PCS-8 Registration
- The served repo **MUST** be registered in `hooks/awareness-ignore.txt` as `<repo> -> <skill>`,
  added via `hooks/awareness-ignore-add.sh . <skill>` (which appends + commits only that file). `[SRC-002]`

**Enforcement:** router test; the mapping resolves to an installed skill.

### PCS-9 Exclusivity vs the in-repo CLAUDE.md system
- A served repo **MUST** use **either** a project-context skill (this standard) **or** an in-repo
  `CLAUDE.md`, **never both**. Skills are for repos that must stay AI-config-free; `CLAUDE.md` is
  for repos the maintainer owns. `[SRC-002]`

**Enforcement:** a repo mapped in `awareness-ignore.txt` MUST NOT also carry a committed `CLAUDE.md`.

### PCS-10 Inherited skill constraints
- The skill **MUST** satisfy the repo's baseline skill constraints: `SKILL.md` < 500 lines,
  `description` < 1536 chars, `name` equals the folder name, failure-modes section present. `[SRC-005]`

**Enforcement:** concierge audit; skill-creator constraint validation.

### PCS-11 External mirror (optional)
- A project-context skill **MAY** mirror admitted findings to **exactly one** external, human-facing
  surface. Zero or one — never several. `[SRC-006]`
- The mirror **MUST** be a **single page** (or a small fixed set of pages) organized by heading, never
  a database of per-finding rows. A database whose rows are individual findings is, mechanically, a
  new page per finding — the exact structure PCS-11 exists to prevent. `[SRC-006]`
- `references/knowledge.md` **MUST** remain authoritative. A finding **MUST NOT** exist only in the
  mirror. `[SRC-006]`
- The mirror's content **MUST** be governed by its own editorial standard — for cheat sheets,
  [`CHEAT_SHEET.md`](CHEAT_SHEET.md). `[SRC-006]`
- The log → mirror transform **MUST** be a **rewrite for a human audience**, never a copy, excerpt, or
  paste of the log entry. The two artifacts have opposite optimisation targets: the log maximises
  completeness, the mirror maximises omission. `[SRC-006]` `[SRC-007]`
- The **majority of log entries MUST NOT be mirrored.** Admission is a filter and rejection is the
  expected outcome; a skill that mirrors everything is non-conforming. `[SRC-006]`
- **Review MUST be conversational, before the write** — the exact bullet and heading shown to the
  maintainer, in the session that produced it, with an explicit yes required before anything is
  written. There **MUST NOT** be a Notion-side (or equivalent) review-status field. A per-item
  approval workflow inside the mirror is, again, the per-finding structure this rule exists to
  prevent — it re-imports rows, IDs, and review states through the back door. `[SRC-006]`
- On a decline, the corresponding log entry **MUST** be marked (`sheet: no`) so the same finding is
  not re-proposed on a later sync. `[SRC-006]`
- The mirror **MUST NOT** relax [PCS-7](#pcs-7-self-enrich-boundary-critical): nothing is written into
  the served project's checkout. `[SRC-002]`
- **Read-back.** The mirror's **current full content** **SHOULD** be pulled into the skill as a
  **generated** reference file, refreshed whenever the mirror changes, so the skill's own context
  benefits from what the maintainer has written or approved there. The file **MUST** be marked
  generated and **MUST NOT** be hand-edited; it **MUST NOT** replace `project-facts.md` or
  `knowledge.md`. Because the mirror holds nothing that was not already conversationally approved,
  read-back is a plain **copy** of the mirror's current text — there is no per-item "approved" filter
  to apply, because there is no per-item anything. Reference implementation:
  `foleon-ripley/references/cheatsheet-approved.md`. `[SRC-006]`

**Rationale:** a database of per-finding rows and a Notion-side review-status field were both tried
(2026-08-03) and both reintroduced the same defect: content the maintainer never asked for, split
across pages, most of it duplicating what the maintainer had already written by hand. Every rule
above exists to keep that specific failure from recurring, not to describe an ideal in the abstract.

**Enforcement:** `CHEAT_SHEET.md` conformance checklist; manual review of the conversation transcript
where the write was approved.

---

## Conformance checklist

A project-context skill is conforming when **all** are true:

- [ ] Lives under a work/client silo folder with a `_category.md` (PCS-1)
- [ ] Named `<silo>-<repo>`, kebab-case, globally unique (PCS-2)
- [ ] Has `SKILL.md` + `references/project-facts.md` + `references/knowledge.md` (PCS-3)
- [ ] `SKILL.md`: `user-invokable: true`; description has trigger phrases **and** `/skill` (PCS-4)
- [ ] `SKILL.md`: how-to-use flow + self-enrich instruction + boundary + failure-modes table (PCS-4)
- [ ] `project-facts.md` holds only stable, verifiable facts (PCS-5)
- [ ] `knowledge.md` is a dated append log with a promote/prune rule (PCS-6)
- [ ] Log entries follow the structured schema, and appends are deduplicated first — by script where one exists (PCS-6)
- [ ] At most one external mirror, and it is a page (or small page set) organized by heading — never a per-finding database (PCS-11)
- [ ] Mirrored content is rewritten (not copied) and approved conversationally, before the write, with no Notion-side review-status field (PCS-11)
- [ ] The mirror's current content is pulled back into a generated, never-hand-edited reference file (PCS-11)
- [ ] No `CLAUDE.md`/`.claude/` written into the served repo (PCS-7)
- [ ] Registered `<repo> -> <skill>` in `hooks/awareness-ignore.txt` (PCS-8)
- [ ] Served repo does not also carry a committed `CLAUDE.md` (PCS-9)
- [ ] Passes concierge audit; SKILL.md < 500 lines, description < 1536 chars (PCS-10)

---

## Enforcement

| Mechanism | Covers |
|---|---|
| `skill-creator` (authoring) | Scaffolds to PCS-3/4; validates PCS-10. Should scaffold new project-context skills to this template. |
| `concierge` audit (`meta/concierge/scripts/audit.sh`) | PCS-1, PCS-2, PCS-10 today; PCS-3 and PCS-9 are candidate automated checks. |
| Project-awareness router | Exercises PCS-2/PCS-8 — a broken mapping surfaces at session start. |
| Manual review | PCS-4, PCS-5, PCS-6, PCS-7 (judgement-based). |
| [`CHEAT_SHEET.md`](CHEAT_SHEET.md) conformance checklist + conversation review | PCS-11 — admission, rewrite-not-copy, conversational approval. |

## Exceptions

Exceptions follow the repo's standard waiver process: rule ID, justification, risk, mitigation,
expiry (≤ 90 days), rollback. A skill under active migration to this standard **MAY** be
temporarily non-conforming if tracked with a dated note in its `knowledge.md`.

## Metrics

- **Mapping resolution:** 100% of `<repo> -> <skill>` entries resolve to an installed, conforming skill.
- **Leakage:** 0 AI/context files (`CLAUDE.md`, `.claude/`) committed into any served repo.
- **Conformance:** % of project-context skills passing the checklist (target 100%).

## Sources

- `[SRC-001]` Reference implementation — `foleon/foleon-ripley/` (SKILL.md + references/).
- `[SRC-002]` Project-awareness router & registry — `hooks/session-claude-md-check.sh`, `hooks/awareness-ignore.txt`, `hooks/awareness-ignore-add.sh`.
- `[SRC-003]` Repo taxonomy — `CATEGORIES.md`, `foleon/_category.md`.
- `[SRC-004]` Anthropic — Agent Skills (description-driven triggering). https://code.claude.com/docs/en/skills.md
- `[SRC-005]` skill-creator constraints — `meta/skill-creator/SKILL.md` (SKILL.md < 500 lines, description < 1536 chars, failure-modes required).
- `[SRC-006]` Cheat-sheet editorial standard — [`CHEAT_SHEET.md`](CHEAT_SHEET.md) (admission gates, one page/one bullet, rewrite-not-copy, conversational review, full-page-read dedupe).
- `[SRC-007]` Internal — *Research brief: what makes a cheat sheet usable* (2026-08-03), Notion → Foleon - Knowledge System. Evidence that a machine log and a human lookup surface have opposite optimisation targets.

## Change log

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-20 | Initial standard. Codifies the `foleon-ripley` architecture as the required shape for project-context skills. |
| **2.0.0** | 2026-08-05 | **PCS-11 rewritten.** The mirror MUST be a single page organized by heading, never a per-finding database — a database row is mechanically a new page per finding, exactly what a database-backed mirror produced and the maintainer rejected on sight. Review MUST be conversational, before the write; a Notion-side review-status field is explicitly disallowed, since it reintroduces the same per-item structure. `sheet:` in PCS-6 becomes `yes\|no\|none` (no external row ID exists to reference). Read-back simplifies to a plain copy of the mirror's current text, since everything on it was already conversationally approved. Scope change; version bumped MAJOR. |
| 1.2.0 | 2026-08-03 | **PCS-6**: where a dedupe script exists the writer MUST use it — a rule enforced only by instruction was the weakest link. **PCS-11**: added the **read-back leg**. Approved rows SHOULD be pulled back into a generated reference file, because the mirror was one-directional and a finding could exist on the external surface while being in no skill-facing file — found by audit, not theory. Checklist and enforcement updated. |
| 1.1.0 | 2026-08-03 | **PCS-6 amended** — structured entry schema (`date · area · symptom — finding · refs · sheet`) and a mandatory dedupe-before-append search. **PCS-11 added** — optional single external mirror: log stays authoritative, transform is a rewrite not a copy, most entries are correctly rejected, cross-linked by external ID, created in a review state, PCS-7 boundary preserved. Checklist, enforcement table and sources updated. |
