# Standard — Cheat Sheet (CHS)

| Field | Value |
|---|---|
| **Status** | Active |
| **Version** | 2.1.0 |
| **Owner** | skills-tinky maintainer |
| **Approvers** | skills-tinky maintainer |
| **Effective date** | 2026-08-05 |
| **Applies to** | The single human-facing Notion page a project-context skill maintains for its maintainer (reference implementation: `Foleon - Cheat Sheet`) |

> **v2.0.0 replaces the entire v1.x architecture.** v1.x built a Notion *database* with one row per
> admitted finding. In Notion, every database row **is a page** — so "one row per finding" is
> mechanically identical to "a new page per finding," which is exactly what the maintainer rejected
> on sight: *"this is not a cheat-sheet, it's a document with 10000 of infos."* Worse, the admission
> gates checked new findings against *other rows*, never against the maintainer's own existing
> page — so most of what got written duplicated a bullet that was already there, longer and in a
> worse place. Both defects are structural, not tunable. The whole database is gone; nothing here
> carries it forward. See the [v2.0.0 changelog entry](#change-log) for the full account.

**Reference implementation** — the page itself, no database:
`Foleon - Cheat Sheet` (`https://app.notion.com/p/3aae7f9407e780df888df6c667a4f4e1`), organized by
`##` heading, one bullet per fact.

---

## Problem

A project-context skill accumulates findings in `references/knowledge.md` — dense, complete,
append-only, written **for an agent that reads everything**. That log is the wrong artifact for a
human. The cheat sheet exists to give the human a *fast* surface instead: a page they wrote (or would
write) for themselves, organized by heading, short enough to scan in the time it takes to remember
they needed it. As many as **40% of queries are re-finding queries** — people re-searching something
they already knew `[SRC-006]` — and that recurrence is what justifies the whole system.

That surface fails the moment it stops being **one page you can scan**. Scannability is not a nice
property to aim for; it is measured to matter: 79% of readers scan rather than read, and scannable +
concise + objective text measured **124% higher usability** than the same content written
conventionally `[SRC-002]`. A structure that turns every fact into its own page defeats this by
construction — there is no "scan the page" left to do, because there is no longer one page.

**Success metrics** — see [§ Metrics](#metrics). In short: the whole cheat sheet stays short enough to
read end to end in under a minute, nothing on it duplicates anything else on it, and the maintainer
still finds it worth opening.

## Scope

**In scope:** what earns a place on the page, how a fact is worded, which heading it goes under, and
who approves it before it is written.

**Out of scope:**
- The AI-facing discoveries log — governed by [`PROJECT_CONTEXT_SKILL.md`](PROJECT_CONTEXT_SKILL.md)
  PCS-6 and PCS-11.
- The automation that moves findings between them (hook + skill mechanics).
- Long-form documentation, ADRs, runbooks, and explanation of *why a system is designed as it is* —
  different documentation types; mixing them is the failure mode Diátaxis names explicitly `[SRC-007]`.

---

## Normative rules

### CHS-1 Audience separation

- The cheat sheet **MUST** be written for a human reader; the discoveries log **MUST** remain the
  machine-facing artifact. `[SRC-017]`
- A cheat-sheet bullet **MUST NOT** be a copy, excerpt, or lightly-edited paste of a log entry — it is
  a **rewrite** (see PCS-11). `[SRC-017]`
- The cheat sheet **MUST NOT** be the only home of any finding — the log stays authoritative.

**Rationale:** the two artifacts optimise for opposite things (completeness vs omission). One text
cannot serve both.

**Enforcement:** reviewed at proposal time (CHS-10); a bullet that reads like its log entry is rejected.

### CHS-2 Admission — five gates

- Every candidate finding **MUST** be evaluated against all five gates below, and **MUST NOT** be
  proposed for the page unless it passes **all five**. `[SRC-006]` `[SRC-015]` `[SRC-007]`
  1. **Recurrence** — will this plausibly be looked up *again*? `[SRC-006]`
  2. **Retrieval cost** — was re-deriving it expensive (roughly 10 minutes or more, or required reading
     source code)?
  3. **Non-obviousness** — is it absent from, or contradicted by, the obvious source (the code,
     `package.json`, the official docs)? If the tool already tells you, the page **MUST NOT** repeat
     it. `[SRC-007]`
  4. **Actionability** — does it resolve to a *do this*? Pure explanation fails this gate. `[SRC-014]` `[SRC-008]`
  5. **Not already said** — is the fact absent from the page's **current** content, read in full,
     including near-equivalent phrasing? This gate did not exist in v1.x, and its absence is the
     reason most of the v1.x backfill duplicated the maintainer's own page.
- Rejection is the normal outcome, not a failure: most log entries will correctly never reach the
  page. (Descriptive, not normative — the binding rule is the five-gate test above.)
- A rejected finding **MUST** remain in the discoveries log. Nothing is deleted by this standard.

**Rationale:** a cheat sheet is "not a repository for every possible task but a curated selection of
crucial actions" `[SRC-015]`. Gate 5 exists because a page has no property to query against — the only
way to know something is already said is to read the page, so the standard requires it explicitly
rather than assuming it happens. `[SRC-010]`

**Enforcement:** the writing agent states the passing rationale per gate when proposing; the maintainer
sees the full proposal before anything is written (CHS-10).

### CHS-3 Atomicity

- One bullet **MUST** cover exactly one fact or symptom. `[SRC-013]` `[SRC-016]`
- A finding spanning several facts **MUST** become several bullets, placed under whichever headings
  fit each one — never merged into a single bullet joined by "and".

**Rationale:** the minimum information principle — an item "should never ask about more than one
thing" `[SRC-013]`; troubleshooting entries stay "focused tightly on one symptom" `[SRC-016]`.

**Enforcement:** reviewed at proposal time; a bullet containing "and" joining two unrelated facts is a signal.

### CHS-4 Lead phrase

- A bullet **SHOULD** open with a **bold lead phrase** naming the observable thing, in the reader's own
  words — matching the page's existing style (`**Editor ≠ viewer**: …`, `**Cards**: …`). `[SRC-016]` `[SRC-008]`
- The lead phrase **MUST** front-load the informative words — the first two or three words alone
  **SHOULD** convey what the bullet is about. `[SRC-003]`
- A bullet **MUST NOT** open with a non-informative lead-in: `Issue with`, `Problem with`, `How to`,
  `Note about`, `Fix for`, `When you`, `Something about`, or a leading article. `[SRC-003]`

**Rationale:** users read roughly the first two words of a line before deciding whether to keep
reading `[SRC-003]`; the layer-cake scanning pattern — a bold lead phrase acting like a mini-heading —
is "by far the most effective way" to scan a list of short items `[SRC-001]`.

**Enforcement:** banned-opener list is mechanically checkable; lead-phrase quality is reviewed at proposal time.

### CHS-5 One page, one artifact — no per-fact structure

- A fact **MUST** be **one entry** — a bullet, optionally followed by a short explanatory clause and/or
  a fenced code block — under an existing or new `##` heading on the page. It **MUST NOT** be its own
  page, its own database row, or carry any per-item property (status, ID, dedupe key, verified-on
  date). `[SRC-018]`
- A fenced code block **MAY** follow a bullet whenever the fact is a command, snippet, or short
  sequence. This is a **normal** part of an entry, not an exception — the page already does this
  throughout `## Commands`.
- A bullet **MAY** carry a short "what it's for" or "how to use it" clause when the bare fact would be
  ambiguous or unusable without it. Richness that serves understanding is not the defect v2.0.0
  corrected; a *database of per-finding pages* was.

**Rationale:** this is the direct correction of the v1.x defect. A database's row-is-a-page structure
is incompatible with "read it in one scan"; there is no version of a database of individual findings
that avoids this, because the incompatibility is in what a database row *is*, not in how it is
configured. That correction is about **structure** (one page, not many), not about **content**
richness — conflating the two was the mistake in the first CHS-6 (see the v2.1.0 changelog entry).

**Enforcement:** structural — there is no schema left to violate. Reviewed at proposal time.

### CHS-6 Length — judged by the fact, not a word count

- There is **no fixed word or line cap.** A bullet **MUST** be as short as the fact allows, and **MAY**
  extend to include an explanatory clause or a fenced code block (CHS-5) whenever the fact is
  genuinely ambiguous or unusable without one.
- The **lead phrase (CHS-4) MUST still make the topic identifiable from the first clause alone** —
  length below that line is fine; ambiguity in it is not.
- The action, if there is one, **SHOULD** come first; caveats and explanation after (inverted pyramid).
  `[SRC-002]`
- The **whole page SHOULD stay short enough to read end to end in a few minutes** — see the
  page-length metric. This is enforced by CHS-2 (most findings are rejected) and CHS-3 (one bullet,
  one fact), **not** by capping any individual entry's length.

**Rationale (revised 2026-08-05, see v2.1.0):** the original version of this rule set a hard ~35-word
cap and treated anything longer as a violation — which meant an entry that legitimately needed a
"why" clause or a command snippet failed the standard by design. That was wrong: the actual goal
(halving word count measured +58% usability on its own, `[SRC-002]`) is about **cutting waffle**, not
about **banning explanation**. A page stays short because almost nothing is admitted (CHS-2) and each
admitted thing is exactly one fact (CHS-3) — length of an individual, real, one-fact entry was never
the lever that mattered.

**Enforcement:** judged at proposal time — does the lead phrase alone identify the topic? Is there
exactly one fact here, or should this split (CHS-3)? There is no numeric check to run.

### CHS-7 Voice

- Bullets **MUST** use the second-person imperative for any action ("Rebuild core first, then copy
  `env-config.js`").
- Bullets **MUST NOT** narrate discovery ("we found that…", "it turned out…", "after investigating…").
- Bullets **MUST NOT** hedge (`probably`, `it seems`, `might be`, `I think`). If a fact is uncertain, it
  fails CHS-2 gate 4 and does not belong here.
- Tone **SHOULD** be neutral; promotional or emphatic language **MUST NOT** be used. `[SRC-002]`
- Project-native jargon (`@foleon/core`, `to-css`, KrakenD) **MAY** be used freely — the audience is
  the maintainer. `[SRC-015]`

**Rationale:** hyperbole "imposes a cognitive burden" and measurably slows task performance `[SRC-002]`;
checklist wording should be "simple and exact" in "the familiar language of the profession" `[SRC-015]`.

**Enforcement:** hedge-word and narrative-phrase lists are mechanically greppable; reviewed at proposal time.

### CHS-8 Headings, not properties

- Categories **MUST** be the page's own `##` headings — there is no `Area` property, no select field,
  nothing to configure. New headings are added by writing them. `[SRC-018]`
- The page **SHOULD** hold roughly **4 to 8** headings at a time. Reference implementation currently
  has 5 (`Commands`, `Packages`, `Conventions`, `Gotchas`, `Playwright gotchas`).
- A heading whose bullet list exceeds roughly **10 items** **SHOULD** be split into two more specific
  headings, rather than left to grow.

**Rationale:** working-memory focus of attention holds about 4 chunks, not 7±2 `[SRC-005]`. The
specific headings above are not invented — they are the maintainer's own pre-existing organisation
`[SRC-018]`, which is stronger evidence than any theoretical taxonomy this standard could propose instead.

**Enforcement:** reviewed at proposal time; heading count and per-heading bullet count are visible just
by opening the page.

### CHS-9 Review gate — conversational, not a status field

- A proposed bullet **MUST** be shown to the maintainer — exact wording, exact heading — **before**
  anything is written to Notion. `[SRC-011]`
- Only an explicit **yes** from the maintainer, given in that conversation, authorises the write. No
  default, no auto-approval, no "propose and forget."
- On a **no**: nothing is written. The corresponding log entry **MUST** be marked so the same finding
  is not re-proposed on a later sync (PCS-11).
- There **MUST NOT** be a per-item review status, review queue, or approval workflow inside Notion —
  the conversation *is* the review. Building a Notion-side approval mechanism reintroduces the v1.x
  per-item structure this version removes.

**Rationale:** the maintainer's stated requirement is a check on what lands in their own reference
material. A live conversation gives them that check with strictly less machinery than a database
status field, and — unlike a status field — cannot silently drift out of sync with what they actually
wanted.

**Enforcement:** structural — there is no write path that skips the conversation, because there is no
API call to trash-database rows or set a status; the only way in is the page-edit call, made after a
yes.

### CHS-10 Dedupe — read the page

- Before proposing anything, the writer **MUST** fetch the page's current content and read it in full.
  `[SRC-010]`
- If the fact is already covered — even in different words — it fails CHS-2 gate 5 and is not proposed.
- There is no property, no key, no query to run. The page is small enough that reading it *is* the
  dedupe mechanism, by design (CHS-6, CHS-8).

**Rationale:** the Notion API cannot search page-body text via a query `[SRC-010]` — under the v1.x
model that forced a Dedupe-key *property*. Under this model there is nothing to force: the artifact
being deduped against is short enough to read directly, which is simpler and cannot drift from the
real content the way a derived key could.

**Enforcement:** the write path fails closed if the page was not freshly re-fetched immediately before
the edit (stale reads risk missing something added since).

### CHS-11 Scope limit — memorisation rules do not apply

- Rules optimised for **recall** **MUST NOT** be imported into this standard: cloze deletion, imagery,
  mnemonics, emotional-state cues, interference management. `[SRC-013]`
- Only the **retrieval-compatible** subset of `[SRC-013]` applies: atomicity (CHS-3) and provide-sources
  (a bullet **SHOULD** name the file/ticket it came from when that helps re-derive it, inline, not as a
  separate field).

**Rationale:** `[SRC-013]` is written for spaced-repetition memorisation. A cheat sheet is *consulted on
demand*, never recalled from memory. Importing the rest would be a category error.

**Enforcement:** review; this rule exists to be cited when rejecting such an addition.

---

## Documented overrides

| # | Source rule | Override | Justification |
|---|---|---|---|
| 1 | Diátaxis: reference "should mirror the structure of the product" `[SRC-007]` | Headings are **concern-based** (CHS-8), not product/package-based | A cheat sheet is a how-to index; Diátaxis itself requires how-to titles to name the problem, not the tool `[SRC-008]`. |
| 2 | Gawande: checklists carry 5–9 items `[SRC-015]` | ≤10 bullets per heading, 4–8 headings total (CHS-8) | Cowan's review puts the working-memory limit at ~4, not the Miller-era 7±2 `[SRC-005]`; a page is read start to end, so both the per-section and total counts matter. |
| 3 | Wozniak's 20 rules `[SRC-013]` | Only 2 of 20 adopted (CHS-11) | Optimised for memorisation; this artifact is optimised for a one-minute read. |

---

## Conformance checklist

A cheat-sheet bullet is conforming when **all** are true:

- [ ] Rewritten for a human, not copied from the log (CHS-1)
- [ ] Passes all five admission gates, including "not already said" (CHS-2)
- [ ] Covers exactly one fact (CHS-3)
- [ ] Opens with a front-loaded bold lead phrase, no banned opener (CHS-4)
- [ ] Is one bullet line under an existing heading — no new page, no property (CHS-5)
- [ ] As short as the fact allows, but not artificially truncated; lead phrase alone identifies the topic (CHS-6)
- [ ] Imperative, neutral, no discovery narrative, no hedging (CHS-7)
- [ ] Placed under one of ~4–8 headings; no heading exceeds ~10 bullets (CHS-8)
- [ ] Shown to the maintainer, exact wording, and approved **before** the write (CHS-9)
- [ ] The full page was freshly read immediately before proposing (CHS-10)

## Enforcement

| Mechanism | Covers | Automated |
|---|---|---|
| Writing agent pre-proposal validation (banned openers, hedge words, narrative phrases) | CHS-4, CHS-7 | Yes |
| Length and richness judged against the fact, not a number (CHS-6) | CHS-6 | No — judgement, by design |
| Fresh full-page read before every proposal | CHS-2 gate 5, CHS-10 | Yes (mechanical fetch), judged by the writer |
| Conversational approval before any write | CHS-1, CHS-2, CHS-3, CHS-9, CHS-11 | No — by design (CHS-9) |
| Heading/bullet count visible on open | CHS-8 | No — visual, not enforced |

## Exceptions

Exceptions follow the repo's standard waiver process: rule ID, justification, risk, mitigation,
expiry (≤ 90 days), rollback.

None standing. CHS-5/CHS-6 already accommodate explanatory clauses and code blocks directly — v2.0.0
had one exception here (a "MAY use a fenced code block... rather than being forced into 35 words"),
which was itself evidence the underlying rule was wrong; v2.1.0 removed the rule instead of keeping
the exception.

## Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Page length** | readable end to end in < 1 minute (rough proxy: ≤ 150 lines total) | Manual — open the page |
| **Duplicate rate** | 0 bullets restating another bullet | Manual read-through at each sweep |
| **One-glance test** | the topic of every entry is identifiable from its lead phrase alone | Reviewed at proposal time, not measured |
| **Admission precision** | maintainer still finds ≥ 90% of bullets worth keeping at a periodic read-through | Sweep outcome |
| **Consultation** | the maintainer actually opens the page when stuck, instead of re-deriving | Self-report |

## Sources

- `[SRC-001]` NN/g — *Text Scanning Patterns: Eyetracking Evidence* (Pernice, 2019-08-25). https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/ — layer-cake pattern.
- `[SRC-002]` NN/g — *How Users Read on the Web* (Nielsen, 1997-09-30). https://www.nngroup.com/articles/how-users-read-on-the-web/ — 79%/16% scanning; usability deltas; word-count halving.
- `[SRC-003]` NN/g — *First 2 Words: A Signal for the Scanning Eye*. https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/ — front-loading.
- `[SRC-005]` Cowan, N. — *The magical number 4 in short-term memory* (2001). https://philpapers.org/rec/COWTMN — ~4-chunk working-memory limit.
- `[SRC-006]` Teevan, Adar, Jones & Potts — *Information Re-Retrieval* (SIGIR 2007). http://teevan.org/publications/papers/sigir07.pdf — ~40% of queries are re-finding.
- `[SRC-007]` Diátaxis — *Reference*. https://diataxis.fr/reference/
- `[SRC-008]` Diátaxis — *How-to guides*. https://diataxis.fr/how-to-guides/
- `[SRC-010]` Notion — *Filter database entries* (API reference). https://developers.notion.com/reference/post-database-query-filter — property-only filtering; no page-body full-text search. Under v2.0.0 this is the reason dedupe is a full-page read, not the reason for a property.
- `[SRC-011]` Notion — *Database properties*. https://www.notion.com/help/database-properties — retained for historical context only; no longer load-bearing.
- `[SRC-013]` Wozniak, P. — *Twenty rules of formulating knowledge*. https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge
- `[SRC-014]` *Minimalism (technical communication)*. https://en.wikipedia.org/wiki/Minimalism_(technical_communication)
- `[SRC-015]` Gawande, A. — *The Checklist Manifesto*, ch. 6, via summaries. https://www.projectmanagement.com/blog-post/21259/creating-a-killer-checklist--lessons-from--the-checklist-manifesto-
- `[SRC-016]` Troubleshooting-article convention. https://docs.document360.com/docs/troubleshooting-articles
- `[SRC-017]` Internal — *Research brief: what makes a cheat sheet usable* (2026-08-03).
- `[SRC-018]` Internal — the maintainer's own hand-written `Foleon - Cheat Sheet` page. The strongest evidence in this standard: it is what the maintainer actually built for themselves, unprompted, and it survived two rounds of "this is wrong" completely untouched.

## Change log

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-03 | Initial standard: database, per-finding rows, closed field set, `Status`/`Dedupe key` properties, 90-day decay. |
| 1.1.0 | 2026-08-03 | Corrections from building the reference implementation (title property naming, `ID` field, formula-based staleness, `Status` as `select`). |
| 1.2.0 | 2026-08-03 | Log dedupe scripted; read-back leg added (approved rows → local file). |
| **2.1.0** | 2026-08-05 | **CHS-6 corrected on direct maintainer pushback.** The v2.0.0 version of CHS-6 set a hard ~35-word cap and CHS-5 treated a fenced code block as a rare exception to it. The maintainer rejected both: a bullet needing a "how to use it" clause or a command snippet is normal, not a violation. CHS-6 now sets **no fixed length** — an entry is as short as the fact allows, may include an explanatory clause and/or a code block, and is judged only by whether its lead phrase (CHS-4) still identifies the topic in one clause. CHS-5's code-block allowance is promoted from "standing exception" to a normal part of an entry. What actually keeps the page short is unchanged: CHS-2 (most things are rejected) and CHS-3 (one bullet, one fact) — length was never the real lever, and pretending otherwise is what produced the wrong rule. Conformance checklist, enforcement table, exceptions and one metric updated accordingly. |
| 2.0.0 | 2026-08-05 | **Full architecture reversal.** The maintainer rejected the v1.x database on sight: every finding created a new page ("this is not a cheat-sheet, it's a document with 10000 of infos"), and — found on inspection — 13 of the 18 rows created during the v1.2.0 backfill duplicated a bullet already on the maintainer's own hand-written page, because admission never checked against that page's actual content, only against other database rows. The v1.x database was trashed in full. **CHS-5 (closed field set), CHS-9 (staleness/decay), CHS-10 (Status review gate) and CHS-11 (Dedupe-key property) are removed.** Replaced with: one page, one bullet per fact under an existing heading (CHS-5, rewritten), a fifth admission gate — "not already said" (CHS-2) — checked by reading the whole page (CHS-10, rewritten), and a conversational review gate before any write (CHS-9, rewritten) in place of a Notion-side status field. Net effect: fewer rules (11 vs 12), because most of what v1.x enforced with schema is now enforced simply by there being one short page. |
