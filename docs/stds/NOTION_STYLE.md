# Standard — Notion Style (NST)

| Field | Value |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Owner** | skills-tinky maintainer |
| **Approvers** | skills-tinky maintainer |
| **Effective date** | 2026-08-20 |
| **Applies to** | Every Notion page a `skills-tinky` skill generates or maintains in the maintainer's workspace — the cycle mirror ([`CYCLE_DOC.md`](CYCLE_DOC.md) CYC-10/CYC-15), the cheat-sheet hub and its project and category pages ([`CHEAT_SHEET.md`](CHEAT_SHEET.md)), and any page written by `notion-knowledge-capture` or a successor |

**Reference implementation** — `foleon/foleon-cycle/scripts/cycle.py`'s `render`, the only renderer in
this repo that emits a styled Notion body. Every mechanic asserted below (callout blocks, the
`{color=}` attribute, `<table fit-page-width>`, `####` headings, mermaid in a fenced block) is
asserted because that renderer already writes it successfully to this workspace `[NSRC-006]` — not
from Notion's documentation, which this standard does not cite. See
[§ Evidence gaps](#evidence-gaps).

---

## Problem

Two skills in this repo write Notion pages, a third is planned, and each one arrived at its own
answer to the same questions: what is a heading for, when does a callout earn its box, what does the
colour orange mean. The result is a workspace where the conventions are per-page folklore living in
one renderer's comments.

The concrete failure that triggered this standard is not that the pages were ugly. It is that they
were **complete and unreadable** — every required fact present, none of it findable. The cycle
mirror's first version buried the hill, the doc's primary signal, as a grey inline code chip three
screens down `[NSRC-002]`. Its second version fixed that and still drew this verdict on the page as
a whole:

> *"i want to have a clear 'Shape 1 : ...' for each shape. just make more visible sections … why is
> 'fio' just here like that without any context??? … 'self:' -> this is not aesthetic … this is a
> bit pathetic."* `[NSRC-001]`

Read together, the two rounds of feedback are one defect with three faces:

1. **No frame.** Blocks sit at the top of a page with nothing naming what they collectively are, so
   the reader has to infer the page's shape from its contents.
2. **No landmarks.** Repeated peer items — topics, projects — render as bare titles, so a page of
   three shapes reads as one undifferentiated column.
3. **Classification carried as literal text.** A machine-meaningful attribute (`self:`) repeated as a
   prefix on forty consecutive lines: forty tokens of noise that convey a grouping the eye cannot
   see.

The maintainer reads and works in these pages `[NSRC-003]`, which makes readability a functional
property of the tool, not a cosmetic finish. Shape Up's whole argument for the hill chart is that it
is *seen* — *"you can see at a glance"* `[NSRC-005]` — and the same is true of every other signal a
generated page carries: one nobody looks at has stopped working.

**Success metrics** — see [§ Metrics](#metrics). In short: a generated page's shape is legible before
its content is read, one colour means one thing across the workspace, and no reader edit is ever
corrupted by styling.

## Scope

**In scope:** the visual and structural contract of a *generated* Notion page — section framing,
heading hierarchy, colour semantics, callout and table use, how a machine-meaningful attribute is
rendered, what may be drawn to scale, and who owns the styling.

**Out of scope:**
- **What a page is allowed to contain.** Admission is each governing standard's job:
  [`CHEAT_SHEET.md`](CHEAT_SHEET.md) for the cheat sheet, [`CYCLE_DOC.md`](CYCLE_DOC.md) for the
  cycle mirror. NST governs how admitted content reads, never whether it belongs.
- **Page-versus-database architecture, hierarchy and titling.** CHS-9a and CYC-10 own those.
- **The consent gate before a write.** CHS-9 and CYC-11 own it; NST adds no write path.
- **Pages a human authored by hand.** This standard binds generators. A hand-written page is the
  maintainer's own business.

---

## Normative rules

### NST-1 A generated page is derived output

- A generated page **MUST** be reproducible in full from its source of truth, and **MUST** be written
  by whole-page regeneration rather than by patching blocks. `[NSRC-006]`
- Where a page has a writable surface — a place the maintainer edits and the generator reads back —
  that surface **MUST** be named exhaustively in the governing standard and **MUST** be the narrowest
  thing that satisfies the need. Everything else is derived, and a Notion-side edit to it is reported
  and ignored, never silently kept.

**Rationale:** two writable surfaces drift. One writable surface plus regeneration means the page can
always be rebuilt, which is what makes every rule below safe to change — a restyle is a re-render,
not a migration.

**Enforcement:** structural. The generator has one write path and it emits a whole body.

### NST-2 Every block sits under a named section

- A page **MUST NOT** open with an unframed content block. Its first element is either a page-level
  section heading or a single orientation callout (NST-11), never a bare table, list or paragraph.
- Peer content blocks **MUST** be grouped under a heading that names what they collectively are, in
  the reader's language rather than the generator's — `Preview`, `The bet`, `Dev log`, not `Summary
  table 1`.
- Heading levels **MUST** carry one meaning per page and be assigned top-down: **h1** = page-level
  section, **h2** = a block within it, **h3**/**h4** = structure inside a block. A level **MUST NOT**
  be chosen for the size it renders at.
- A heading level **MUST NOT** be skipped upward — an h4 may not appear where no h2 opened the
  section — with one permitted exception: a level **MAY** be left unused throughout a page when a
  lower level is pinned by a parser (see NST-7), and the exception **MUST** be recorded in the
  governing standard.
- Repeated peer items of the same kind **MUST** be distinguishable at a glance by their heading
  alone: a stable ordinal, an icon, or both. `[NSRC-001]`
- An ordinal in a heading is **positional and derived**. It **MUST NOT** be stored, and **MUST NOT**
  be used as an identifier anywhere else — not in a log line, a commit message, or a conversation
  the generator writes. Items are referred to by name, which is stable; the ordinal renumbers the
  moment one is added or reordered.

**Rationale:** the reader's first question about any page is "what is this and how is it laid out",
and a section heading answers it before a word of content is read. The ordinal answers the second
question — "how many of these are there and which one am I in" — which a bare title cannot.

**Enforcement:** a layout assertion inside the generator's render path, fail-closed like NST-7's
round-trip check: the first line is a page-level heading or a callout, and every repeated peer item's
heading matches the ordinal pattern. A generator that cannot assert it **MUST NOT** ship the layout.

### NST-3 Colour is semantic, fixed workspace-wide, and never decorative

- A colour **MUST** mean one thing across every page in the workspace, and that mapping **MUST** be
  written down. Reference mapping, derived from the pages already in use `[NSRC-006]`:

  | Colour | Means | Seen in |
  |---|---|---|
  | **purple** | the maintainer's own accent — meta, orientation, "this block is about you" | the cycle header callout; `top` on the hill |
  | **orange** | unknowns, research, not yet settled | `uphill`; a shaping topic; research tasks |
  | **blue** | settled, executing, agreed | `downhill`; a shaped topic's outcome; ticket work |
  | **green** | done | `done` on the hill |
  | **yellow** | assumed, not confirmed — read this before trusting the block above | an `Assumptions:` callout |
  | **red** | over budget, or a failure the reader must act on | an over-booked appetite |
  | **grey** | subordinate detail: true, needed, and outranked by what is above it | constraints, tallies, orientation lines |

- A colour **MUST NOT** be chosen per page, per section, or to break up a wall of text. If a block
  needs no semantic colour it gets none.
- A generated page **SHOULD** use at most four colours outside grey. Past that the mapping stops
  being learnable and colour reverts to decoration.

**Rationale:** a colour's whole value is that the reader learns it once. A mapping that moves between
pages teaches nothing and costs the reader a legend on every page.

**Enforcement:** review against the mapping table above; grep the renderer for colour literals — the
set it can emit is finite and readable in one pass.

### NST-4 A callout is for the block that decides everything under it

- A callout **MUST** carry exactly one idea, and its icon **MUST** be semantic — the same icon for
  the same kind of block across pages.
- A callout **MUST** be reserved for content that changes how the reader reads the rest of the
  section: the outcome a section's work is judged against, an orientation frame, a caveat that
  qualifies the block above it. Ordinary prose **MUST NOT** be boxed.
- Consecutive callouts **MUST NOT** exceed two. Three boxes in a row is a page with no emphasis at
  all.

**Rationale:** emphasis is a fixed budget. Every additional box spends from the same pot, and a page
where everything is boxed reads exactly like a page where nothing is.

**Enforcement:** review; countable in the rendered body (consecutive callout blocks are greppable).

### NST-5 A table is for scanning a column, not for holding prose

- A table **MUST** be used when the reader's question is answered by scanning one column across rows,
  and **MUST NOT** be used to lay out content that is read row by row as prose.
- A table **SHOULD NOT** exceed five columns, and every header cell **MUST** be bold.
- A cell **MUST NOT** contain a paragraph. One sentence or one value; anything longer belongs in the
  body under a heading.

**Rationale:** the reason the cycle's dev log became a table is that the reader scans it by date and
scope — forty bullets made those two facts unfindable. The reason a topic's outcome is *not* in a
table is that nobody scans outcomes; they read one.

**Enforcement:** review at render-design time; column count is countable in the renderer.

### NST-6 A repeated literal prefix is a grouping, not text

- When a machine-meaningful attribute would render as the **same literal prefix on every line** of a
  list — `self:`, `TODO:`, `[perso]` — it **MUST NOT** be rendered as that prefix. It **MUST** become
  one of: a labelled group of the lines that carry it, a section of its own, or a page property.
  `[NSRC-001]`
- The chosen rendering **MUST** be visible without reading: a label line, a colour on that label, or
  a heading. Moving the prefix elsewhere without making the grouping visible fixes nothing.
- The attribute's **local syntax is unaffected**. A source-of-truth file may keep the prefix — it is
  a good syntax for a file a parser reads. This rule binds the rendered page only.
- Where the group's rendering, rather than a per-line marker, is what carries the attribute, the
  source of truth **MUST** keep items of one kind **contiguous**, so that rendering the group
  preserves item order (NST-7 requires the render to round-trip byte-identically).
- A group label **MUST** state what the group *is* to the reader, not what the parser calls it —
  "research, mine, never a ticket" over "kind: self".

**Rationale:** a prefix repeated forty times costs forty lines of noise to convey one grouping, and
conveys it only to a reader who already knows the code. The eye reads grouping and colour for free
and reads repeated literals as texture.

**Enforcement:** grep the rendered body — no literal appears as a line-leading prefix on more than
two consecutive parsed lines. Contiguity is checked by the source-of-truth validator.

### NST-7 Anything parsed back renders plain

- A line the generator **parses back** out of the page **MUST** be rendered with no colour, no
  attribute list and no decoration of any kind.
- Styling for such a line **MUST** be carried by an adjacent line that is *not* parsed — a group
  label, a heading, a grey caption — or by a derived block elsewhere on the page.
- The generator **MUST** verify the round trip **before writing**: render → parse → assert the parsed
  result is byte-identical to the source of truth, and **refuse to write** on any difference. The
  check **MUST** live in the write path, not only in a test suite.
- A parser **SHOULD** tolerate an attribute list and Notion's own outbound transformations
  (autolinking anything domain-shaped, escaping markdown metacharacters) on the lines it reads, and
  **MUST** undo them before any comparison. Tolerating them is the belt to this rule's braces; it is
  not permission to emit them.

**Rationale:** this is the one rule whose violation loses data rather than looking bad. On a page
with a writable surface, the reader's line *is* the new value — so a `{color=}` appended to it is
swallowed into the content on the next read, and the merge cannot tell the difference between that
and the maintainer retitling the item. A styling change that corrupts the source of truth is a
data-loss bug wearing a styling change's clothes.

**Enforcement:** the round-trip assertion inside the render path, fail-closed. Implemented in this
repo as `roundtrip_problems()` in `cycle.py`, run by `render` itself `[NSRC-006]`.

### NST-8 Draw quantities only over real quantities

- A bar, chart, gauge or track **MAY** be drawn over a quantity the source of truth actually states —
  a time budget, a count of items, a size.
- A bar, chart or gauge **MUST NOT** be drawn over completion of open-ended work, and completion
  **MUST** be reported as a count (`2 of 7`), never a percentage.
- An ordinal scale **MUST** be rendered along its own stops — a position track — and **MUST NOT** be
  given a second axis, a fill, or an interpolated value. A fill bar over four ordinal stops reads
  "half done", which is a claim nobody made.

**Rationale:** a bar to scale over a real quantity states a fact and is the fastest way to read it. A
bar over must-haves-done is a percentage in costume: it implies the remaining work is known, which is
precisely what unfinished exploratory work guarantees it is not.

**Enforcement:** review of every chart the renderer can emit — a finite, readable set. For the cycle
mirror this is also CYC-6 and CYC-15.

### NST-9 Styling is the renderer's, never the hand's

- All styling **MUST** be produced by the generator. A human **MUST NOT** hand-apply styling to a
  generated page.
- A change to how a page looks **MUST** be a change to the generator plus a change to the governing
  standard, in the same pass.

**Rationale:** whole-page regeneration (NST-1) erases a hand-applied flourish on the next write, and
while it survives it is indistinguishable from a rendering bug. Worse, it teaches the maintainer that
the page is editable in ways the merge does not honour.

**Enforcement:** structural — regeneration overwrites. Reviewed when a page looks different from what
the renderer emits.

### NST-10 Group a long list before it becomes a wall

- An undifferentiated list **SHOULD NOT** exceed ten items. Past that it **MUST** be grouped under
  labels, split into sections, or turned into a table (NST-5).
- Items in a list the reader refers to by position — questions, ranked work — **MUST** be numbered,
  and the numbering **MUST** match whatever the generator's own commands print, so a number is
  sayable off the page and lands in the tool.

**Rationale:** ten is where scanning stops working and the eye needs a handle. Matching the tool's
numbering is what makes "3 and 5 are settled" a sentence the maintainer can say without translating.

**Enforcement:** countable in the rendered body; numbering parity is a test against the generator's
own listing command.

### NST-11 A section says what it is before it says anything else

- Every page-level section **MUST** be followed, before its first content block, by either a callout
  or a single orientation line naming what the section covers and why the reader is looking at it.
  `[NSRC-001]`
- An orientation line **MUST** be rendered subordinate (grey, per NST-3) and **MUST** be short enough
  to read in one pass — one line.
- An orientation line's content **MUST** be either **derived** from the source of truth (counts,
  totals, dates) or **quoted from a stated source** — for a project section, the project-context
  skill's own description of that project. It **MUST NOT** be composed by the generator from
  inference. A section with nothing derivable and no source gets counts alone, or nothing.

**Rationale:** a bare project name is a heading that assumes the reader already has the context the
page exists to give them — *"why is 'fio' just here like that without any context???"* `[NSRC-001]`.
The inference ban is the same discipline the rest of this repo's standards apply to content: a
plausible sentence the generator invented is worse than a count, because it reads like a fact.

**Enforcement:** layout assertion in the render path (NST-2's check covers the presence of the line);
the derived-or-sourced requirement is judged at review — a generator with no source for a gloss has
no code path that can emit one.

---

## Conformance checklist

A generated Notion page is conforming when **all** are true:

- [ ] Reproducible in full from its source of truth; written by whole-page regeneration (NST-1)
- [ ] The writable surface, if any, is exhaustively named in the governing standard; everything else is derived and Notion-side edits to it are reported, not kept (NST-1)
- [ ] The page opens with a section heading or one orientation callout — never a bare block (NST-2)
- [ ] Every content block sits under a heading that names the group in the reader's language (NST-2)
- [ ] Heading levels carry one meaning each, assigned top-down; any skipped level is recorded in the governing standard (NST-2)
- [ ] Repeated peer items carry a stable ordinal and/or icon in the heading; ordinals are derived, never stored, never used as identifiers (NST-2)
- [ ] Every colour on the page appears in the NST-3 mapping with that meaning; at most four non-grey colours (NST-3)
- [ ] Every callout carries one idea, a semantic icon, and content that changes how the section reads; no more than two in a row (NST-4)
- [ ] Every table is scanned by a column, has ≤ 5 bold-headed columns, and holds no paragraph in a cell (NST-5)
- [ ] No machine-meaningful attribute renders as a repeated literal prefix; it is a labelled group, a section, or a property, and the grouping is visible without reading (NST-6)
- [ ] Where a group carries the attribute, the source of truth keeps items of one kind contiguous (NST-6)
- [ ] Every parsed-back line renders plain; styling sits on adjacent unparsed lines (NST-7)
- [ ] The render path asserts the round trip and refuses to write on any difference (NST-7)
- [ ] The parser undoes Notion's autolinking and escaping before comparing (NST-7)
- [ ] Every bar or chart is drawn over a stated quantity; completion is a count, never a percentage; no ordinal scale is charted on a second axis (NST-8)
- [ ] Nothing on the page was styled by hand (NST-9)
- [ ] No undifferentiated list exceeds ten items; position-referenced lists are numbered to match the generator's own output (NST-10)
- [ ] Every page-level section opens with a derived or sourced one-line orientation, rendered grey (NST-11)

## Enforcement

| Mechanism | Covers | Automated |
|---|---|---|
| Round-trip assertion inside the render path, fail-closed | NST-7 | Yes |
| Layout assertion inside the render path (first block, ordinal headings, orientation line present) | NST-2, NST-11 | Yes |
| Whole-page regeneration as the only write path | NST-1, NST-9 | Structural |
| Colour literals in the renderer are a finite, greppable set | NST-3 | Yes (readable), judged (meaning) |
| Contiguity check in the source-of-truth validator | NST-6 | Yes |
| Prefix grep over the rendered body | NST-6 | Yes |
| Numbering parity test against the generator's listing command | NST-10 | Yes |
| Review of the finite set of charts the renderer can emit | NST-8 | No — judgement, by design |
| Callout / table / density judgement at render-design time | NST-4, NST-5, NST-10 | No — judgement, by design |
| No code path exists that composes an unsourced gloss | NST-11 | Structural |

## Exceptions

Exceptions follow the repo's standard waiver process: rule ID, justification, risk, mitigation,
expiry (≤ 90 days), rollback.

**Standing exception — NST-2 (skipped heading level), `foleon-cycle`.** The cycle mirror pins the
scope heading at `####` because `reconcile` parses it and existing mirrored pages carry that level;
the page therefore uses h1 / h2 / h4 and leaves h3 unused. Justification: changing the parsed level
would orphan every task on already-mirrored pages. Risk: none to the reader — Notion heading levels
are styles, not a tree. No expiry: this is the permitted exception NST-2 names, recorded in
[`CYCLE_DOC.md`](CYCLE_DOC.md) CYC-15a as that rule requires.

## Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Shape legible before content** | the maintainer can say what a page's sections are without reading a block | Self-report on the rendered page |
| **Colour consistency** | 0 colours on any page outside the NST-3 mapping | Grep the renderer's colour literals |
| **Corruption from styling** | 0 reader edits mangled by a rendering attribute | Round-trip check; reconcile collision log |
| **Prefix noise** | 0 machine attributes rendered as repeated literal prefixes | Grep the rendered body |
| **Hand-styling** | 0 hand-applied styles surviving a regeneration | Diff the page against a fresh render |
| **Consultation** | the maintainer opens the generated page in preference to the source file | Self-report |

## Evidence gaps

This standard cites **no external source**. Every rule is derived from failures observed on this
workspace's own pages and from the mechanics one renderer in this repo has already exercised
`[NSRC-001]`, `[NSRC-002]`, `[NSRC-006]`. Two consequences, stated rather than papered over:

- **Scope.** NST is a house style for this workspace. It does not claim to describe how Notion pages
  are generally built, and no rule here should be quoted as general practice.
- **The colour mapping and the numeric thresholds** (four colours, five columns, ten list items, two
  consecutive callouts) are conventions chosen for internal consistency, not measured findings. They
  are enforceable because they are fixed, not because they are optimal. Revisit any of them against
  a real page that they made worse — that is the only evidence this standard accepts for changing
  them.

Cheapest way to close the gap if it matters later: `documentor` on Notion's own block and page
documentation to confirm the mechanics, which would upgrade `[NSRC-006]` from "our renderer does
this" to a primary source. It would not settle the judgement rules, which are house style by nature.

## Sources

- `[NSRC-001]` Internal — the maintainer's judgement on the generated Cycle-11 mirror, 2026-08-20, verbatim: *"i want to have a clear 'Shape 1 : ...' for each shape. just make more visible sections (the whole first part before 'fio' could have a 'preview' category). why is 'fio' just here like that without any context??? … same for the questions : 'self:' -> this is not aesthetic, instead you could just use color codes, pills or borders i dont know just something better"*, and on the page as a whole: *"this is a bit pathetic. i've seen so many good looking notion pages in my life!! add a real rule-set for that maybe?"* — the request this standard answers.
- `[NSRC-002]` Internal — the maintainer's judgement on the first rendered mirror, 2026-08-20: *"content-wise im pretty happy with it, but the doc is like so boring to look at"*. Recorded in [`CYCLE_DOC.md`](CYCLE_DOC.md) as `[SRC-017]`; the finding that a complete page nobody reads has failed at its only job.
- `[NSRC-003]` Internal — the maintainer's requirement, 2026-08-19, recorded in [`CYCLE_DOC.md`](CYCLE_DOC.md) as `[SRC-015]`: they read *and edit* in Notion and will not go through the skill to tick a task. This is what makes readability functional and what creates the writable surface NST-7 protects.
- `[NSRC-004]` Internal — [`CHEAT_SHEET.md`](CHEAT_SHEET.md) (CHS 2.4.0): page-not-database, one fact per heading, one bullet per fact, and the v2.0.0 finding that a structure generating a page per fact is a structural defect rather than a tunable one. The precedent for framing content instead of accumulating it.
- `[NSRC-005]` Singer, R. — *Shape Up*, ch. 13 "Show Progress". https://basecamp.com/shapeup/3.4-chapter-13 — the hill chart's value is that it is *seen*: *"you can see at a glance"*; to-do counts cannot show status. Cited for the visibility argument only; Shape Up says nothing about Notion.
- `[NSRC-006]` Internal — `foleon/foleon-cycle/scripts/cycle.py`, `cmd_render_for` / `roundtrip_problems` / `parse_mirror_tasks` as of CYC 2.3.0. The source for every Notion mechanic asserted here — callout blocks with `icon`/`color`, the trailing `{color="…"}` attribute, `<table fit-page-width="true" header-row="true">`, `####` headings, mermaid in a fenced block — and for the fail-closed round-trip pattern NST-7 requires.

## Change log

| Version | Date | Change |
|---|---|---|
| **1.0.0** | 2026-08-20 | **Initial.** Extracted from [`CYCLE_DOC.md`](CYCLE_DOC.md) CYC-15, which had accumulated the workspace's page-styling rules inside a standard about cycle docs — so the cheat sheet and `notion-knowledge-capture` inherited none of them. Eleven rules: section framing and heading meaning (NST-2), the workspace colour mapping (NST-3), callout and table discipline (NST-4, NST-5), the ban on rendering a machine attribute as a repeated literal prefix (NST-6), the parsed-back-renders-plain exclusion with its fail-closed round-trip check (NST-7), quantities-over-quantities-only (NST-8), renderer-owned styling (NST-9), list density and numbering parity (NST-10), and the derived-or-sourced orientation line (NST-11). NST-6 and NST-11 are new in substance and answer `[NSRC-001]` directly; the rest generalise what CYC-15 v2.2.0 had already settled for one page. Carries an [Evidence gaps](#evidence-gaps) section because the standard cites no external source — the rules come from this workspace's own observed failures, and the numeric thresholds are conventions, not measurements. |
