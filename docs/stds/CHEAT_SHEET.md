# Standard — Cheat Sheet (CHS)

| Field | Value |
|---|---|
| **Status** | Active |
| **Version** | 1.1.0 |
| **Owner** | skills-tinky maintainer |
| **Approvers** | skills-tinky maintainer |
| **Effective date** | 2026-08-03 |
| **Applies to** | Every row written to a human-facing cheat-sheet database fed by a project-context skill (reference implementation: the Foleon cheat sheet in Notion) |

> **ID namespaces.** `CHS-n` identifies a rule *in this standard*. `CS-nn` identifies a *row* in
> the cheat-sheet database (Notion Unique ID). They are deliberately different prefixes — never
> mix them.

**Reference implementation** — Notion database `Findings — symptom → fix`, a child of the
`Foleon - Cheat Sheet` page:
- database: `8020892f438f470eac8ad5da4c11809e`
- data source: `collection://a7b041f4-7add-41e8-9ead-5fc6c62d6815`
- views: `Lookup` (approved, grouped by Area) · `Review queue` (needs review) · `Stale` (past 90 days)

---

## Problem

A project-context skill accumulates findings in `references/knowledge.md` — a dense, complete,
append-only log written **for an agent that reads everything**. That log is the wrong artifact for
a human: it is unstructured, hard to search by hand, grows without a quality bar, and nothing in it
was ever reviewed by the person it is supposed to help.

Mirroring the log into Notion would move the problem, not solve it. A cheat sheet is not storage —
it is a **retrieval surface consulted under time pressure**, and the evidence is unambiguous that
retrieval surfaces are governed by *omission*: 79% of readers scan rather than read `[SRC-002]`, and
scannable + concise + objective text measured **124% higher usability** than the same content written
conventionally `[SRC-002]`. Completeness actively harms this artifact.

The system is justified by re-retrieval: as many as **40% of all queries are re-finding queries** —
people re-searching what they have already seen `[SRC-006]`. The cheat sheet exists to intercept
exactly those.

**Success metrics** — see [§ Metrics](#metrics). In short: rows are actually consulted, no duplicates
exist, and the stale queue stays near-empty.

## Scope

**In scope:** the content and form of every row in a cheat-sheet database — what is admitted, how it
is titled, which fields exist, how it is worded, how it decays, and who approves it.

**Out of scope:**
- The AI-facing discoveries log — governed by [`PROJECT_CONTEXT_SKILL.md`](PROJECT_CONTEXT_SKILL.md)
  PCS-6 and PCS-11.
- The automation that moves findings between them (hook + skill mechanics).
- Long-form documentation, ADRs, runbooks, and explanation of *why a system is designed as it is* —
  these are different documentation types and mixing them is the failure mode Diátaxis names
  explicitly `[SRC-007]`.

---

## Normative rules

### CHS-1 Audience separation

- The cheat sheet **MUST** be written for a human reader; the discoveries log **MUST** remain the
  machine-facing artifact. `[SRC-017]`
- A cheat-sheet row **MUST NOT** be a copy, excerpt, or lightly-edited paste of a log entry. The
  transform is a **rewrite** (see PCS-11). `[SRC-017]`
- The cheat sheet **MUST NOT** be the only home of any finding — the log stays authoritative.

**Rationale:** the two artifacts have opposite optimisation targets (completeness vs omission). One
text cannot serve both; attempting it produces a log that is unreadable and a sheet that is untrusted.

**Enforcement:** review at the approval gate (CHS-10); a row whose wording matches its log entry is rejected.

### CHS-2 Admission — the four gates

- Every candidate finding **MUST** be evaluated against all four gates below, and **MUST NOT** be
  written to the sheet unless it passes **all four**. `[SRC-006]` `[SRC-015]` `[SRC-007]`
  1. **Recurrence** — will this plausibly be looked up *again*? `[SRC-006]`
  2. **Retrieval cost** — was re-deriving it expensive (roughly 10 minutes or more, or required
     reading source code / spelunking)?
  3. **Non-obviousness** — is it absent from, or contradicted by, the obvious source (the code,
     `package.json`, the official docs)? If the tool already tells you, the sheet **MUST NOT**
     repeat it. `[SRC-007]`
  4. **Actionability** — does it resolve to a *do this*? Pure explanation fails this gate. `[SRC-014]` `[SRC-008]`
- Rejection is the normal outcome, not a failure: the majority of log entries will correctly never
  reach the sheet. (Descriptive, not normative — the binding rule is the four-gate test above.)
- A rejected finding **MUST** remain in the discoveries log. Nothing is deleted by this standard.

**Rationale:** a lookup artifact is "not a repository for every possible task but a curated selection
of crucial actions" `[SRC-015]`. Because rejection costs nothing (the log keeps everything), the
filter can be aggressive without risk of loss.

**Enforcement:** the writing agent states the passing rationale per gate in the review queue; maintainer
audits at the approval gate.

### CHS-3 Atomicity

- One row **MUST** cover exactly one symptom. `[SRC-013]` `[SRC-016]`
- A finding spanning several symptoms **MUST** be split into one row per symptom, sharing a `Refs`
  value rather than being merged.

**Rationale:** the minimum information principle — an item "should never ask about more than one
thing" `[SRC-013]`; troubleshooting entries stay "focused tightly on one symptom" `[SRC-016]`.

**Enforcement:** review at the approval gate; a title containing "and" joining two symptoms is a signal.

### CHS-4 Symptom-indexed titles

- The title **MUST** name the **observable symptom** in the reader's own words — what you see or
  experience — not the subsystem that owns it. `[SRC-016]` `[SRC-008]`
- The title **MUST** front-load the information-carrying words, and **SHOULD** be written so the first
  two words alone convey what the row is about. `[SRC-003]`
- Titles **MUST NOT** open with a non-informative lead-in. Banned openers include: `Issue with`,
  `Problem with`, `How to`, `Note about`, `Fix for`, `When you`, `Something about`, and any article
  (`A`, `The`) as the first word. `[SRC-003]`
- Exact error text **SHOULD** be included when one exists, verbatim. `[SRC-016]`

**Rationale:** you arrive at the sheet holding a symptom, not a package name. Eyetracking shows users
read roughly the first two words of a heading or link `[SRC-003]`, and the layer-cake scanning pattern —
heading to heading until the right one is found — is "by far the most effective way" to scan `[SRC-001]`.
The title is therefore the entire interface. See [§ Documented overrides](#documented-overrides) for the
deliberate departure from Diátaxis product-mirroring.

**Enforcement:** banned-opener list is mechanically checkable; front-loading is reviewed at the approval gate.

### CHS-5 Closed field set

- A row **MUST** carry exactly these six human fields and no others:

  | Field | Type | Content |
  |---|---|---|
  | `Symptom` | title | the symptom (CHS-4) — the title property is **named** `Symptom`, so the rule is visible every time a row is written |
  | `Area` | select | one value from CHS-8 |
  | `Fix` | text | the action to take (CHS-6) |
  | `Why` | text | one-sentence cause — omitted when unknown `[SRC-016]` |
  | `Refs` | text / url | file paths, ticket IDs, or links |
  | `Verified on` | date | when the fix was last confirmed true `[SRC-013]` |

- A row **MUST** additionally carry exactly two machine fields: `Status` (CHS-10) and
  `Dedupe key` (CHS-11).
- A row **MUST** carry a **unique-ID** field (`ID`, prefix `CS`) — the stable cross-link key required
  by PCS-11. It is system-generated and immutable. `[SRC-011]`
- **Derived** properties (formulas) that hold **no authored content** **MAY** exist where a view
  filter cannot be expressed otherwise (see CHS-9). They are exempt from the closed-set rule because
  they carry no information a human wrote.
- Fields that hold **authored content MUST NOT** be added to the schema without amending this
  standard. `[SRC-009]`
- `Why` **MUST** be left empty rather than filled with speculation when the cause is unknown. `[SRC-016]`

**Rationale:** Google SRE requires teams to "decide collectively what minimal, structured details your
playbooks must have" and to watch for accumulation beyond those essentials `[SRC-009]`. A closed,
governed field set is the mechanism. `Verified on` and `Refs` implement the date-stamping and
provide-sources rules `[SRC-013]`.

**Enforcement:** the database schema *is* the enforcement — adding a property requires an amendment.

### CHS-6 Length caps

- `Symptom` **MUST NOT** exceed **10 words**. `[SRC-003]`
- `Fix` **MUST NOT** exceed **40 words or 3 lines**, whichever is hit first. `[SRC-002]`
- `Fix` **MUST** state the action in its first sentence; caveats and conditions come after
  (inverted pyramid). `[SRC-002]`
- `Why` **MUST NOT** exceed one sentence. If the cause needs more, only a link stays. `[SRC-007]`
- A row **SHOULD** be comprehensible from the grouped table view without opening the page. Anything
  longer belongs *inside* the page. `[SRC-004]`

**Rationale:** halving conventional word count measured +58% usability on its own `[SRC-002]`;
progressive disclosure improves learnability, efficiency and error rate simultaneously, and saves
expert users time by shrinking the initial scan `[SRC-004]`.

**Enforcement:** word/line counts are mechanically checkable and **SHOULD** be validated by the writing
agent before any write.

### CHS-7 Voice

- `Fix` **MUST** use the second-person imperative ("Rebuild core first, then copy `env-config.js`").
- Rows **MUST NOT** narrate discovery ("we found that…", "it turned out…", "after investigating…").
- Rows **MUST NOT** hedge (`probably`, `it seems`, `might be`, `I think`). If a fact is uncertain, it
  fails CHS-2 gate 4 and does not belong here.
- Tone **SHOULD** be neutral and objective; promotional or emphatic language **MUST NOT** be used. `[SRC-002]`
- Project-native jargon (`@foleon/core`, `to-css`, KrakenD) **MAY** be used freely — the audience is
  the maintainer. `[SRC-015]`
- Style **SHOULD** be "austere and uncompromising", prioritising precision over readable prose. `[SRC-007]`

**Rationale:** hyperbole "imposes a cognitive burden" and measurably slows task performance `[SRC-002]`;
checklist wording should be "simple and exact" in "the familiar language of the profession" `[SRC-015]`.

**Enforcement:** hedge-word and narrative-phrase lists are mechanically greppable; tone is reviewed at the gate.

### CHS-8 The `Area` axis

- `Area` **MUST** be exactly one of: **Editor** · **Viewer** · **Core / rendering** ·
  **Build & tooling** · **Tests & Playwright** · **Conventions**. `[SRC-018]`
- The enumeration **MUST NOT** exceed **6 values**. Adding a seventh requires merging or splitting,
  via amendment. `[SRC-005]`
- When one `Area` group exceeds ~9 rows, the maintainer **SHOULD** split that area rather than prune
  rows. `[SRC-015]`

**Rationale:** working-memory focus of attention holds about 4 chunks, not 7±2 `[SRC-005]`, so the
grouped view must stay within a scannable set. The specific six values are derived from how the
maintainer's own hand-written cheat sheet was already organised (Commands / Packages / Conventions /
Gotchas / Playwright) `[SRC-018]` — observed retrieval behaviour beats a theoretical taxonomy. This is a
concern-based axis, deliberately not a package-mirroring one; see
[§ Documented overrides](#documented-overrides).

**Enforcement:** `select` property constrains values; group count visible in the Lookup view.

### CHS-9 Staleness and decay

- Every row **MUST** carry a `Verified on` date. `[SRC-013]`
- A row whose `Verified on` is **older than 90 days** while `Status = Approved` **MUST** surface in
  the `Stale` view. `[SRC-009]`
- The maintainer **SHOULD** clear the `Stale` view at least quarterly, by re-confirming the fix
  (refresh `Verified on`), correcting it, or archiving the row.
- A row found to be wrong **MUST** be corrected or archived, never left standing. A misleading row is
  worse than a missing one.

**Rationale:** Google SRE states playbook "details go out of date at the same rate as the production
environment changes" `[SRC-009]`, making decay the predictable failure mode rather than a surprise.
Wozniak's rule 19 requires date stamping for exactly this reason `[SRC-013]`. The 90-day window is a
maintainer decision (2026-08-03), chosen so the sweep is quarterly and a wrong row cannot survive
half a year.

**Enforcement:** `Stale` view filter (`Past 90 days` is true AND `Status = Approved`).

> **Implementation note (platform limit).** Notion's date filters offer only fixed relative presets
> (today, one week/month/year ago) — **there is no 90-day option**. The window is therefore computed by
> a derived boolean property, `Past 90 days` =
> `if(empty(prop("Verified on")), false, dateBetween(now(), prop("Verified on"), "days") > 90)`,
> and the `Stale` view filters on that. Changing the window means editing this formula, not the view.

### CHS-10 Review gate

- An automated writer **MUST** create rows with `Status = Needs review` and **MUST NOT** write any
  other status. `[SRC-011]`
- Promotion to `Status = Approved` **MUST** be a human action. `[SRC-011]`
- The `Lookup` view **MUST** filter to `Status = Approved`, so unreviewed rows never appear in the
  surface consulted during work. `[SRC-012]`
- `Status` **MUST** offer exactly three states: `Needs review`, `Approved`, `Archived`. `[SRC-011]`
- `Status` **MUST** be implemented as a `select`, or **MAY** be a `status` property if provisioned by
  hand (see note). Either way it **MUST** be API-filterable. `[SRC-010]` `[SRC-011]`

**Rationale:** the maintainer's stated requirement is a check on what lands in their own reference
material. A three-state status with a filtered default view provides it without blocking the
automation.

**Enforcement:** view filter; API writes constrained to `Needs review`.

> **Implementation note (platform limit).** Notion's `status` property type **cannot be created with
> custom options through the API** — it always materialises with the defaults (Not started / In
> progress / Done), and there is no DDL to rename them. A `select` is therefore the only
> machine-provisionable option, and it filters identically via the API. The cost is losing the native
> to-do/in-progress/complete grouping; the gain is that the whole schema is reproducible from this
> standard without manual steps — which matters as soon as a second project gets a sheet.

### CHS-11 Dedupe key is a property

- Every row **MUST** carry a `Dedupe key` **property** — a normalised, lowercased
  `area:symptom-slug` string. `[SRC-010]`
- The dedupe key **MUST NOT** live only in the page body. `[SRC-010]`
- A writer **MUST** query the database by `Dedupe key` (`equals`, then `contains` for near matches)
  **before** creating a row, and **MUST** update the existing row instead of creating a second one on
  a match. `[SRC-010]`
- On an update, `Verified on` **MUST** be refreshed.

**Rationale:** a hard platform limit, not a preference — the Notion query endpoint supports
property-based filtering only; "full-text search of page BODY content is not supported" `[SRC-010]`. A
body-resident key is therefore undedupable by machine.

**Enforcement:** the write path fails closed if the pre-write query was not performed.

### CHS-12 Scope limit — memorisation rules do not apply

- Rules optimised for **recall** **MUST NOT** be imported into this standard: cloze deletion,
  imagery, mnemonics, emotional-state cues, and interference management. `[SRC-013]`
- Only the **retrieval-compatible** subset of `[SRC-013]` applies: atomicity (CHS-3), date
  stamping (CHS-9), and provide-sources (CHS-5 `Refs`).

**Rationale:** `[SRC-013]` is written for spaced-repetition memorisation. A cheat sheet is *consulted
on demand*, never recalled from memory. Importing the rest would be a category error — flagged
explicitly so a future editor does not "complete" the standard by adding them.

**Enforcement:** review; this rule exists to be cited when rejecting such an addition.

---

## Documented overrides

Deliberate departures from a cited source, recorded so they are not mistaken for oversights.

| # | Source rule | Override | Justification |
|---|---|---|---|
| 1 | Diátaxis: reference "should mirror the structure of the product" and is "led by the product it describes" `[SRC-007]` | Rows are **symptom-indexed** (CHS-4), not topic-indexed; product structure is preserved as the `Area` grouping (CHS-8) | A cheat sheet is a *how-to index*, not pure reference. Diátaxis itself requires how-to titles to name the problem, not the tool `[SRC-008]`. The retrieval key must match what the reader arrives with. |
| 2 | Gawande: 5–9 items `[SRC-015]` | 4–6 groups (CHS-8), with 5–9 applied to *rows per group* as a SHOULD | The 5–9 figure descends from the Miller-era estimate; Cowan's review puts the focus-of-attention limit at ~4 `[SRC-005]`. A filtered database is randomly accessed, not read linearly. |
| 3 | Wozniak: the 20 rules of formulating knowledge `[SRC-013]` | Only 3 of 20 adopted (CHS-12) | The set is optimised for memorisation; this artifact is optimised for lookup. |
| 4 | Nielsen's percentages date from 1997 `[SRC-002]` | Treated as directional, not current | NN/g's 2019 eyetracking work `[SRC-001]` confirms scanning still dominates and refines the *how*. Direction is safe; exact effect sizes are not load-bearing for any rule here. |

---

## Conformance checklist

A cheat-sheet row is conforming when **all** are true:

- [ ] Rewritten for a human, not copied from the log (CHS-1)
- [ ] Passes all four admission gates (CHS-2)
- [ ] Covers exactly one symptom (CHS-3)
- [ ] Title names the observable symptom, front-loaded, no banned opener (CHS-4)
- [ ] Carries exactly the six human fields + `Status` + `Dedupe key` + `ID` (CHS-5)
- [ ] `Symptom` ≤ 10 words · `Fix` ≤ 40 words / 3 lines, action first · `Why` ≤ 1 sentence (CHS-6)
- [ ] Imperative, neutral, no discovery narrative, no hedging (CHS-7)
- [ ] `Area` is one of the six permitted values (CHS-8)
- [ ] `Verified on` is set (CHS-9)
- [ ] Created as `Needs review`; promoted only by a human (CHS-10)
- [ ] `Dedupe key` present as a property; pre-write query performed (CHS-11)

## Enforcement

| Mechanism | Covers | Automated |
|---|---|---|
| Notion database schema (closed properties, `select`, `status` types) | CHS-5, CHS-8, CHS-10 | Yes |
| `Lookup` view filter (`Status = Approved`) | CHS-10 | Yes |
| `Stale` view filter (`Verified on` + status) | CHS-9 | Yes |
| Writing agent pre-write validation (word/line counts, banned openers, hedge words, dedupe query) | CHS-4, CHS-6, CHS-7, CHS-11 | Yes |
| Human approval gate (review queue) | CHS-1, CHS-2, CHS-3, CHS-12 | No |
| Amendment to this standard | CHS-5, CHS-8 schema changes | No |

> **Note on the normative mix.** This standard is deliberately MUST-heavy (~78% mandatory), above the
> usual ≤50% guideline. That guideline exists to stop standards demanding behaviour from humans that
> cannot be checked. Here the *writer is a machine* that validates before writing, and every row then
> passes a human gate — so nearly every rule has a real pass/fail test. The rules that are genuine
> judgement calls (front-loading quality, table-view comprehensibility, tone, sweep cadence, area
> splitting) are SHOULD, as they should be.

## Exceptions

Exceptions follow the repo's standard waiver process: rule ID, justification, risk, mitigation,
expiry (≤ 90 days), rollback. Recorded as a dated note on the row itself.

Two standing exceptions, permitted without a waiver:
- **CHS-6 `Fix` cap** — a fix that is irreducibly a multi-step command sequence **MAY** exceed 3 lines
  if it is placed in the page body with a ≤ 40-word summary in the `Fix` property.
- **CHS-9 sweep cadence** — the quarterly sweep **MAY** be skipped for one cycle if the `Stale` view
  is empty.

## Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Consultation rate** | ≥ 50% of approved rows opened at least once in 6 months | Notion page view history / self-report |
| **Duplicate rate** | 0 rows sharing a `Dedupe key` | Query grouped by `Dedupe key` |
| **Stale backlog** | ≤ 5 rows in the `Stale` view at any time | `Stale` view count |
| **Review latency** | median time in `Needs review` ≤ 7 days | `Status` change timestamps |
| **Cap conformance** | 100% of rows within CHS-6 limits | Mechanical check |
| **Admission precision** | ≥ 70% of admitted rows judged still worth keeping at the first sweep | Sweep outcome |

> The **admission precision** metric is the real validation of CHS-2, whose evidence base is the
> weakest in this standard (see `[SRC-017]` § Contradictions). Revisit the four gates once ~20 rows
> exist.

## Sources

- `[SRC-001]` NN/g — *Text Scanning Patterns: Eyetracking Evidence* (Pernice, 2019-08-25). https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/ — layer-cake pattern; F-pattern as failure signal.
- `[SRC-002]` NN/g — *How Users Read on the Web* (Nielsen, 1997-09-30). https://www.nngroup.com/articles/how-users-read-on-the-web/ — 79%/16% scanning; +47/58/27/124% usability deltas; inverted pyramid; word-count halving.
- `[SRC-003]` NN/g — *First 2 Words: A Signal for the Scanning Eye*. https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/ — front-loading.
- `[SRC-004]` NN/g — *Progressive Disclosure* (Nielsen). https://www.nngroup.com/articles/progressive-disclosure/ — row summary vs page detail.
- `[SRC-005]` Cowan, N. — *The magical number 4 in short-term memory* (Behavioral and Brain Sciences, 2001). https://philpapers.org/rec/COWTMN — ~4-chunk focus-of-attention limit.
- `[SRC-006]` Teevan, Adar, Jones & Potts — *Information Re-Retrieval: Repeat Queries in Yahoo's Logs* (SIGIR 2007). http://teevan.org/publications/papers/sigir07.pdf — ~40% of queries are re-finding.
- `[SRC-007]` Diátaxis — *Reference* (Procida). https://diataxis.fr/reference/ — "describe and only describe"; austere style; product-mirroring.
- `[SRC-008]` Diátaxis — *How-to guides* (Procida). https://diataxis.fr/how-to-guides/ — goal-oriented titling; "no digression, explanation, teaching".
- `[SRC-009]` Google — *SRE Workbook*, ch. On-call. https://sre.google/workbook/on-call/ — minimal structured playbook fields; staleness warning; trigger-driven entries.
- `[SRC-010]` Notion — *Filter database entries* (API reference). https://developers.notion.com/reference/post-database-query-filter — property-only filtering; no page-body full-text search.
- `[SRC-011]` Notion — *Database properties*. https://www.notion.com/help/database-properties — `status` vs `select`; Unique ID immutability.
- `[SRC-012]` Notion — *Database views, filters, sorts & groups*. https://www.notion.com/help/views-filters-and-sorts — per-view filter scoping; grouping.
- `[SRC-013]` Wozniak, P. — *Twenty rules of formulating knowledge* (SuperMemo). https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge — minimum information principle (r4), provide sources (r18), date stamping (r19). ⚠️ not peer-reviewed; vendor-authored; memorisation-oriented (see CHS-12).
- `[SRC-014]` *Minimalism (technical communication)* — Carroll's minimalism. https://en.wikipedia.org/wiki/Minimalism_(technical_communication) — action-focused, short task-oriented chunks. ⚠️ primary (*The Nurnberg Funnel*, 1990) not consulted.
- `[SRC-015]` Gawande, A. — *The Checklist Manifesto*, ch. 6, via summaries. https://www.projectmanagement.com/blog-post/21259/creating-a-killer-checklist--lessons-from--the-checklist-manifesto- — killer items; curated selection; one page; profession's language. ⚠️ primary not read; summaries are not mutually independent.
- `[SRC-016]` Troubleshooting-article convention (convergent industry practice). https://docs.document360.com/docs/troubleshooting-articles · https://clickhelp.com/clickhelp-technical-writing-blog/troubleshooting-guide-definition-importance-and-tips-for-creating/ — Symptom → Cause → Resolution; symptom-named titles; omit unknown cause. ⚠️ tier 4–5; corroborated by `[SRC-009]`.
- `[SRC-017]` Internal — *Research brief: what makes a cheat sheet usable* (2026-08-03), Notion → Foleon - Knowledge System. The evidence base for this standard, incl. its Contradictions section.
- `[SRC-018]` Internal — the maintainer's pre-existing hand-written `Foleon - Cheat Sheet` page (Notion, 2026-07/08). Observed evidence for the concern-based `Area` axis (CHS-8).

## Change log

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-03 | Initial standard. Codifies admission gates, closed field set, symptom-indexed titles, length/voice caps, `Area` axis, 90-day decay policy, review gate, property-resident dedupe key, and the memorisation scope limit. Staleness window (90 days) and `Area` axis (concern-based) set by maintainer decision. |
| 1.1.0 | 2026-08-03 | Corrections found by building the reference implementation. **CHS-5**: title property is named `Symptom`; the `ID` unique-ID field (PCS-11 cross-link key) is now part of the required set; derived formula properties are exempt from the closed-set rule. **CHS-9**: the 90-day window is computed by a `Past 90 days` boolean formula — Notion has no 90-day relative date preset. **CHS-10**: `Status` is a `select`, since the `status` type cannot be created with custom options via the API; the three state names are what the rule now binds. Both platform limits are documented inline. |
