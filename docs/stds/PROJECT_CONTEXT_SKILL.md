# Standard — Project-Context Skill (PCS)

| Field | Value |
|---|---|
| **Status** | Active |
| **Version** | 3.0.0 |
| **Owner** | skills-tinky maintainer |
| **Approvers** | skills-tinky maintainer |
| **Effective date** | 2026-07-20 |
| **Applies to** | Every skill whose purpose is to carry one specific project's context in `skills-tinky`, across two repo classes: **silo-only** (the checkout must stay AI-config-free — `ripley`) and **dual-home** (the team owns the checkout and commits its own agent context — `fio`). See [PCS-9](#pcs-9-exclusivity-vs-the-in-repo-claudemd-system) and [PCS-9a](#pcs-9a-dual-home-repos--owned-checkout-plus-private-silo). |

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

**Out of scope:** reusable cross-project skills (`dev/`, `infra/`, …); personal-domain skills
(`personal/`).

**Partially in scope — the per-repo `CLAUDE.md` system.** For a **silo-only** repo the two systems are
mutually exclusive and `CLAUDE.md` is out of scope entirely ([PCS-9](#pcs-9-exclusivity-vs-the-in-repo-claudemd-system)).
For a **dual-home** repo they coexist, and this standard governs the boundary between them — which
class of fact goes to the checkout and which to the skill ([PCS-9a](#pcs-9a-dual-home-repos--owned-checkout-plus-private-silo)).
It does **not** govern the content or shape of the repo's own `CLAUDE.md`; that is the repo's business.

---

## Normative rules

### PCS-1 Placement
- A project-context skill **MUST** live under a work/client silo category folder that has its
  own `_category.md` (e.g. `foleon/`). `[SRC-001]` `[SRC-003]`
- It **MUST NOT** live in `personal/` or in a functional category (`dev/`, `infra/`, …). `[SRC-003]`

**Enforcement:** concierge taxonomy check (every skill under a `_category.md` ancestor); review.

### PCS-2 Naming & deterministic mapping
- The skill folder name **MUST** be `<silo>-<repo>` in kebab-case and globally unique
  (e.g. repo `ripley` in silo `foleon` → `foleon-ripley`; repo `fio` in silo `foleon` →
  `foleon-fio`). `[SRC-001]` `[SRC-002]` `[SRC-008]`
- The rule is **class-independent**: a dual-home skill ([PCS-9a](#pcs-9a-dual-home-repos--owned-checkout-plus-private-silo))
  is named exactly like a silo-only one. Nothing in the name encodes the class — the class is declared
  in `SKILL.md` (PCS-9a) so the name stays a pure function of silo + repo.
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
  `knowledge.md`**; for a dual-home repo the flow **MUST** also read the served repo's own committed
  context files, per [PCS-9a](#pcs-9a-dual-home-repos--owned-checkout-plus-private-silo)), a
  self-enrich instruction ([PCS-6](#pcs-6-knowledgemd-discoveries-log)),
  a boundary statement ([PCS-9](#pcs-9-exclusivity-vs-the-in-repo-claudemd-system)), and a
  **failure-modes table**. `[SRC-001]` `[SRC-005]`
- **SHOULD** stay under ~80 lines (project facts belong in `references/`, not here). `[SRC-005]`

**Enforcement:** skill-creator authoring + constraint validation; review.

### PCS-5 project-facts.md
- **MUST** hold curated, **stable** knowledge only: stack, package/layout, commands, and
  **verifiable** conventions. `[SRC-001]`
- **MUST** be treated as the authoritative reference; when a fact goes stale, the live served
  repo (`package.json`, config) wins and this file **MUST** be corrected. `[SRC-001]`
- **For a dual-home repo this rule is narrowed, not repeated.** The checkout's own committed context
  files already hold that class of fact, so `project-facts.md` becomes an **index + delta** and
  **MUST NOT** restate them — see [PCS-9a](#pcs-9a-dual-home-repos--owned-checkout-plus-private-silo).
  Both files are **read as sources of truth**; on a conflicting *verifiable* fact the live repo wins,
  exactly as above. `[SRC-008]`

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
  implementation: `foleon/foleon-cheatsheet/scripts/log.py check --project <repo>`. `[SRC-006]`
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
- **This holds for both repo classes, without exception.** A dual-home repo's committed context files
  are **read-only input** to the skill ([PCS-9a](#pcs-9a-dual-home-repos--owned-checkout-plus-private-silo)):
  the skill reads them as a source of truth and **never writes to them**. Dual-home changes what the
  skill *reads*, never what it *writes*. `[SRC-008]`
- The reason is ownership, and it is stronger for dual-home than for silo-only: a dual-home repo's
  context files are typically authored by **other people** (`fio`'s `CLAUDE.md` is 17 commits, none of
  them the maintainer's). Appending a personal or unverified finding to a teammate's committed file is
  not a boundary the skill may cross on its own — that is a pull request, a human decision, made by the
  maintainer outside this system. `[SRC-008]`

**Enforcement:** served-repo git status stays free of skill-authored changes, for **both** classes
(metric); review.

### PCS-8 Registration
- The served repo **MUST** be registered in `hooks/awareness-ignore.txt` as `<repo> -> <skill>`,
  added via `hooks/awareness-ignore-add.sh . <skill>` (which appends + commits only that file). `[SRC-002]`

**Enforcement:** router test; the mapping resolves to an installed skill.

### PCS-9 Exclusivity vs the in-repo CLAUDE.md system

**Applies to silo-only repos.** For dual-home repos see [PCS-9a](#pcs-9a-dual-home-repos--owned-checkout-plus-private-silo).

- A **silo-only** served repo **MUST** use **either** a project-context skill (this standard) **or** an
  in-repo `CLAUDE.md`, **never both**. Skills are for repos that must stay AI-config-free; `CLAUDE.md`
  is for repos the maintainer owns. `[SRC-002]`
- A repo is **silo-only** unless it satisfies every PCS-9a eligibility condition and declares itself
  dual-home. **Silo-only is the default**; dual-home is opt-in, declared, and justified. `[SRC-008]`

**Enforcement:** a repo mapped in `awareness-ignore.txt` and **not** declared dual-home MUST NOT also
carry a committed `CLAUDE.md`. The check is class-aware: it reads the mapped skill's `Repo mode:`
declaration (PCS-9a) before flagging, so a conforming dual-home repo does not trip it and an
*undeclared* one does.

### PCS-9a Dual-home repos — owned checkout plus private silo

- A served repo **MAY** carry **both** a committed in-repo context system **and** a project-context
  skill — becoming **dual-home** — **only** when **all** of the following hold. Otherwise
  [PCS-9](#pcs-9-exclusivity-vs-the-in-repo-claudemd-system) applies unchanged. `[SRC-008]`
  1. The maintainer's team **owns** the checkout and may commit agent context to it.
  2. The repo **already** carries committed agent context (e.g. `CLAUDE.md`, `AGENTS.md`).
  3. The maintainer generates findings that **do not belong in the team's committed files** — the four
     classes below (private, unverified, cross-repo, meta). A dual-home declaration with nothing in
     those classes is unjustified: the skill would only restate what the checkout already says.
- **Declaration (required).** The skill's `SKILL.md` **MUST** carry a single line, verbatim format:
  ```
  **Repo mode:** dual-home
  ```
  or `**Repo mode:** silo-only`. Every project-context skill **MUST** declare one. The declaration
  lives in `SKILL.md`, **not** in `hooks/awareness-ignore.txt`: the router strips `#` comments and
  splits each line on `->`, so any inline marker there would either be discarded or corrupt the parsed
  skill name. Declaring in the skill keeps the class machine-readable with **no router parser change**.
  `[SRC-002]` `[SRC-008]`

#### Dual source of truth (read both), single write target (the skill)

- **Both are authoritative.** Where a dual-home repo has committed context files **and** the maintainer
  has this skill, **both MUST be treated as sources of truth and both MUST be read.** Neither replaces
  or overrides the other: the checkout carries what the team agreed, the skill carries what the
  maintainer has learned. Reading only one leaves the task half-informed, which is the specific failure
  this rule exists to prevent. `[SRC-008]`
- **The skill is the only write target.** Every finding the maintainer makes **MUST** be written to this
  skill's `references/knowledge.md`. The skill **MUST NOT** write to the served repo's committed context
  files — see [PCS-7](#pcs-7-self-enrich-boundary-critical), which holds for both classes without
  exception. Promoting a finding into the team's own files is a **pull request the maintainer opens**,
  a human decision explicitly outside this system's scope. `[SRC-008]`
- **Non-duplication.** `references/project-facts.md` **MUST NOT** restate or paraphrase stack, layout,
  commands, or conventions already stated in the repo's committed context files. It **MUST** be an
  **index + delta**: pointers to those files *by path*, plus only what they do not cover. The reason is
  no longer "commit it there instead" — it is that those files are **read directly** on every task, so
  restating them creates a second copy that can go stale while the original moves on. `[SRC-008]`
- **What the skill is for.** In practice the delta falls into four classes; they are a guide to what
  earns a place here, not a gate:
  1. **Private** — the maintainer's own tooling, workflow, or preferences, not the team's.
  2. **Unverified** — a hypothesis, dead end, or observation not yet solid enough to put to the team.
  3. **Cross-repo** — spans this repo *and* another (e.g. a `@foleon/*` registry-auth fact true of both
     `fio` and `ripley`), so it has no single in-repo home.
  4. **Meta** — about the skills/cheat-sheet system itself rather than the project.
- **Conflict resolution is narrow.** Both files being authoritative does not mean both can be right
  about a *verifiable* fact. Where the two state the same checkable thing differently — a command, a
  version, a path — the **live repo wins** and the skill **MUST** be corrected (identical to PCS-5's
  staleness rule; the checkout is what actually runs). This is a staleness tiebreak on facts, not a
  precedence ranking between the two sources.
- **Promotion stays inside the skill.** PCS-6's promote/prune rule is unchanged: when an entry in
  `knowledge.md` stabilises, it is promoted into `project-facts.md` and the log pruned. It is **not**
  promoted into the checkout — the skill has no write access there.

#### Router message

- The awareness router's mapped-repo message **MUST NOT** be emitted unmodified for a dual-home repo.
  Its silo-only wording asserts that the project's context *"intentionally lives OUTSIDE this
  checkout (nothing Claude-specific belongs in this repo)"* — **false** for a dual-home repo, and
  emitted at every session start. The router **MUST** branch on the declared class and, for
  dual-home, direct Claude to read the in-repo context **and** load the skill for private findings.
  `[SRC-002]` `[SRC-008]`

**Rationale — why exclusivity relaxed (read this before reverting).** PCS-9 tested a property of the
**repo** (*may AI config be committed here?*) and used it as a proxy for a property of the **content**
(*is this fact publishable to the team?*). For `ripley` the two coincide perfectly: nothing may be
committed, therefore every fact is private, therefore one home is sufficient and a second would be
pure duplication. `fio` breaks the coincidence — the team owns the checkout, so *most* facts belong
there, yet the maintainer still produces facts that are not publishable: unverified hypotheses, dead
ends, cross-repo facts spanning `fio` and `ripley`, and notes about their own tooling. Under strict
PCS-9 those had nowhere to go. `fio`'s own `CLAUDE.md` bans `TODO`/`FIXME` in committed code and
requires a recorded rationale for every fix, so a half-verified observation *cannot* be committed there
without either publishing it prematurely or discarding it. Two homes here are not duplication; they
are a **content-class split**.

The failure mode PCS-9 existed to prevent — two divergent descriptions of the same thing — is not
addressed by exclusivity in this case; it is addressed **better**, because the non-duplication rule
binds **per sentence** rather than per repo — and because the checkout's files are read directly on
every task rather than copied, so there is no second copy left to drift. Exclusivity is a coarse instrument that
happened to be exactly right while every served repo was silo-only. Do not restore it as a blanket
rule: doing so does not remove the private-fact classes, it only removes their home.

**Enforcement:** the `Repo mode:` line is greppable (concierge, automatable). The write boundary is
mechanically checkable — the served repo's git status stays free of skill-authored changes (PCS-7).
Non-duplication is judgement-based, reviewed when `project-facts.md` changes, and the reviewable
question is narrow: *"is this sentence already in a file we read anyway?"* Router branching is
exercised at every session start in a dual-home repo.

### PCS-10 Inherited skill constraints
- The skill **MUST** satisfy the repo's baseline skill constraints: `SKILL.md` < 500 lines,
  `description` < 1536 chars, `name` equals the folder name, failure-modes section present. `[SRC-005]`

**Enforcement:** concierge audit; skill-creator constraint validation.

### PCS-11 External mirror (optional)
- A project-context skill **MAY** mirror admitted findings to **exactly one** external, human-facing
  surface. Zero or one — never several. `[SRC-006]`
- The mirror **MUST** be a **single page** (or a small fixed set of pages, nested under one project
  page — see below) organized by heading, never a database of per-finding rows. A database whose rows
  are individual findings is, mechanically, a new page per finding — the exact structure PCS-11 exists
  to prevent. `[SRC-006]`
- **Multiple project-context skills MAY share one hub.** A shared hub does not violate "exactly
  one" — each skill's mirror is still exactly one (its own project page and that page's category
  pages); the hub above them is simply a bare index. The hub itself **MUST NOT** hold any project's
  categories directly — one project page per project, categories nested under it, per
  [`CHEAT_SHEET.md`](CHEAT_SHEET.md) CHS-9a. `[SRC-006]`
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
- This holds for **both** repo classes, and is **not** touched by PCS-9a's relaxation. The mirror sync
  writes to exactly two places — `skills-tinky` and the external surface — for a dual-home repo just as
  for a silo-only one. PCS-9a permits the *maintainer's* team-facing facts to be committed to a
  dual-home checkout; it grants the **mirror path** no write access there whatsoever. Keeping the sync
  class-independent is deliberate: it is the one path that runs semi-automatically, so it gets the
  stricter rule. `[SRC-008]`
- **Read-back.** The mirror's **current full content** **SHOULD** be pulled into the skill as a
  **generated** reference file, refreshed whenever the mirror changes, so the skill's own context
  benefits from what the maintainer has written or approved there. The file **MUST** be marked
  generated and **MUST NOT** be hand-edited; it **MUST NOT** replace `project-facts.md` or
  `knowledge.md`. Because the mirror holds nothing that was not already conversationally approved,
  read-back is a plain **copy** of the mirror's current text — there is no per-item "approved" filter
  to apply, because there is no per-item anything. Reference implementation:
  `foleon-ripley/references/cheatsheet-approved.md`. `[SRC-006]`
- **One read-back file per project, owned by that project's skill.** Where a hub serves several
  projects, each skill's file **MUST** contain **only its own** project page's categories — never the
  hub's other projects. `foleon-fio/references/cheatsheet-approved.md` holds `Fio`'s category pages;
  `foleon-ripley`'s holds `Ripley`'s and stays unchanged when a second project is added. A file
  concatenating two projects' pages is non-conforming: it would put `ripley` facts in front of every
  `fio` task, which is the context bleed the per-project split exists to prevent. `[SRC-006]` `[SRC-008]`

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
- [ ] The mirror's current content is pulled back into a generated, never-hand-edited reference file, holding **only this project's** pages (PCS-11)
- [ ] Registered `<repo> -> <skill>` in `hooks/awareness-ignore.txt` (PCS-8)
- [ ] `SKILL.md` declares `**Repo mode:** silo-only` or `dual-home` (PCS-9a)
- [ ] Passes concierge audit; SKILL.md < 500 lines, description < 1536 chars (PCS-10)

**Silo-only** skills additionally require:

- [ ] No `CLAUDE.md`/`.claude/` written into the served repo (PCS-7)
- [ ] Served repo does not also carry a committed `CLAUDE.md` (PCS-9)

**Dual-home** skills additionally require:

- [ ] All three eligibility conditions hold — team owns the checkout, it already carries committed agent context, and private-class findings genuinely exist (PCS-9a)
- [ ] `project-facts.md` is an index + delta: no sentence restates or paraphrases the repo's committed context files (PCS-9a)
- [ ] The how-to-use flow reads **both** sources — the repo's committed context **and** the skill's files (PCS-9a)
- [ ] Nothing in the served repo's checkout was written by the skill — git status is clean of skill-authored changes (PCS-7, PCS-9a)
- [ ] The router emits the dual-home message, not the silo-only "context lives OUTSIDE this checkout" wording (PCS-9a)
- [ ] The mirror sync still writes only to `skills-tinky` and the external surface (PCS-11)

---

## Enforcement

| Mechanism | Covers |
|---|---|
| `skill-creator` (authoring) | Scaffolds to PCS-3/4; validates PCS-10. Should scaffold new project-context skills to this template, including the PCS-9a `Repo mode:` line. |
| `concierge` audit (`meta/concierge/scripts/audit.sh`) | PCS-1, PCS-2, PCS-10 today; PCS-3 and PCS-9 are candidate automated checks. The PCS-9 check **MUST** read the mapped skill's `Repo mode:` line first — a class-blind check flags every conforming dual-home repo and is worse than no check. `Repo mode:` presence is itself trivially greppable. |
| Project-awareness router | Exercises PCS-2/PCS-8 — a broken mapping surfaces at session start. **MUST** branch on repo class (PCS-9a); the silo-only message is factually wrong in a dual-home repo. |
| Manual review | PCS-4, PCS-5, PCS-6, PCS-9a non-duplication + read-both flow (judgement-based). PCS-7's write boundary is mechanical, not judgement — see the leakage metric. |
| [`CHEAT_SHEET.md`](CHEAT_SHEET.md) conformance checklist + conversation review | PCS-11 — admission, rewrite-not-copy, conversational approval. |

## Exceptions

Exceptions follow the repo's standard waiver process: rule ID, justification, risk, mitigation,
expiry (≤ 90 days), rollback. A skill under active migration to this standard **MAY** be
temporarily non-conforming if tracked with a dated note in its `knowledge.md`.

## Metrics

- **Mapping resolution:** 100% of `<repo> -> <skill>` entries resolve to an installed, conforming skill.
- **Leakage:** 0 skill-authored changes to any served repo's checkout, **both classes**. For silo-only
  that means no AI/context files at all; for dual-home it means the context files that already exist
  are never edited by the skill (only read).
- **Class declared:** 100% of project-context skills carry a `Repo mode:` line (PCS-9a).
- **Duplication (dual-home only):** 0 sentences in `project-facts.md` restating the served repo's own
  committed context files. Measured by reading the file against the repo's `CLAUDE.md` at each change —
  this is the metric that replaces exclusivity, so letting it drift un-checked reintroduces exactly the
  defect PCS-9 was written to prevent.
- **Conformance:** % of project-context skills passing the checklist (target 100%).

## Sources

- `[SRC-001]` Reference implementation — `foleon/foleon-ripley/` (SKILL.md + references/).
- `[SRC-002]` Project-awareness router & registry — `hooks/session-claude-md-check.sh`, `hooks/awareness-ignore.txt`, `hooks/awareness-ignore-add.sh`.
- `[SRC-003]` Repo taxonomy — `CATEGORIES.md`, `foleon/_category.md`.
- `[SRC-004]` Anthropic — Agent Skills (description-driven triggering). https://code.claude.com/docs/en/skills.md
- `[SRC-005]` skill-creator constraints — `meta/skill-creator/SKILL.md` (SKILL.md < 500 lines, description < 1536 chars, failure-modes required).
- `[SRC-006]` Cheat-sheet editorial standard — [`CHEAT_SHEET.md`](CHEAT_SHEET.md) (admission gates, one page/one bullet, rewrite-not-copy, conversational review, full-page-read dedupe).
- `[SRC-007]` Internal — *Research brief: what makes a cheat sheet usable* (2026-08-03), Notion → Foleon - Knowledge System. Evidence that a machine log and a human lookup surface have opposite optimisation targets.
- `[SRC-008]` The `fio` repo — the first dual-home case, and the evidence for PCS-9a. Committed agent context the team inherits (`CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, `.claude/agents/`, `.claude/hooks/`, `docs/adr/`, `docs/rfc/`, `docs/agents/`) alongside a maintainer who still generates non-committable findings. Its `CLAUDE.md` bans `TODO`/`FIXME` in committed code and requires a recorded rationale per fix — the concrete reason an unverified finding has no in-repo home. Router-parser constraint (`#`-stripping, `->` splitting) verified in `hooks/session-claude-md-check.sh` and `hooks/awareness-ignore-add.sh`.

## Change log

| Version | Date | Change |
|---|---|---|
| **3.0.0** | 2026-08-12 | **Two repo classes; exclusivity narrowed, not removed.** Triggered by `fio` `[SRC-008]`: a repo the team owns, already carrying committed agent context, which the maintainer nonetheless wants backed by a private silo. Strict PCS-9 forbade that outright. **PCS-9 narrowed** to *silo-only* repos (unchanged in force there; silo-only remains the default) and its enforcement made class-aware. **PCS-9a added** — dual-home repos: three eligibility conditions, a required `**Repo mode:**` declaration in `SKILL.md` (deliberately *not* in `awareness-ignore.txt`, whose parser strips `#` comments and splits on `->`, so no router-parser change is needed), and the boundary that replaces exclusivity — **dual source of truth on read, single write target on write**: both the checkout's committed context and the skill's files are authoritative and both MUST be read, while **every** write goes to the skill and **none** to the checkout. Plus a **non-duplication** rule turning `project-facts.md` into an index + delta (the checkout's files are read directly, so restating them just creates a copy that can go stale), a narrow **staleness tiebreak** (live repo wins on a conflicting verifiable fact, per PCS-5), and four classes describing what earns a place in the skill (private, unverified, cross-repo, meta) — a guide, not a gate. **PCS-7**'s no-writes-to-checkout prohibition is **retained in full for both classes**: a dual-home repo's context files are typically authored by other people (`fio`'s `CLAUDE.md` is 17 commits, none the maintainer's), so appending to them is a pull request the maintainer opens, never an action the skill takes. **PCS-11** unchanged for the mirror path in both classes — the semi-automatic path keeps the stricter rule — plus one read-back file per project holding only its own pages. Router **MUST** branch on class: the silo-only message (*"context lives OUTSIDE this checkout"*) is factually false in a dual-home repo and was being emitted at every session start. Checklist split into common / silo-only / dual-home; duplication metric added to replace the leakage metric where the latter is inapplicable. Scope change (the standard now governs two repo classes and a boundary it previously excluded) → MAJOR. |
| 1.0.0 | 2026-07-20 | Initial standard. Codifies the `foleon-ripley` architecture as the required shape for project-context skills. |
| **2.1.0** | 2026-08-05 | **PCS-11 amended for multiple projects.** Clarified that several project-context skills MAY share one hub without violating "exactly one mirror" — each skill's mirror is still exactly one project page (plus that page's categories); the hub is a bare index above them, never holding any project's categories directly. Points at the new `CHEAT_SHEET.md` CHS-9a for the concrete nesting/naming rule. |
| **2.0.0** | 2026-08-05 | **PCS-11 rewritten.** The mirror MUST be a single page organized by heading, never a per-finding database — a database row is mechanically a new page per finding, exactly what a database-backed mirror produced and the maintainer rejected on sight. Review MUST be conversational, before the write; a Notion-side review-status field is explicitly disallowed, since it reintroduces the same per-item structure. `sheet:` in PCS-6 becomes `yes\|no\|none` (no external row ID exists to reference). Read-back simplifies to a plain copy of the mirror's current text, since everything on it was already conversationally approved. Scope change; version bumped MAJOR. |
| 1.2.0 | 2026-08-03 | **PCS-6**: where a dedupe script exists the writer MUST use it — a rule enforced only by instruction was the weakest link. **PCS-11**: added the **read-back leg**. Approved rows SHOULD be pulled back into a generated reference file, because the mirror was one-directional and a finding could exist on the external surface while being in no skill-facing file — found by audit, not theory. Checklist and enforcement updated. |
| 1.1.0 | 2026-08-03 | **PCS-6 amended** — structured entry schema (`date · area · symptom — finding · refs · sheet`) and a mandatory dedupe-before-append search. **PCS-11 added** — optional single external mirror: log stays authoritative, transform is a rewrite not a copy, most entries are correctly rejected, cross-linked by external ID, created in a review state, PCS-7 boundary preserved. Checklist, enforcement table and sources updated. |
