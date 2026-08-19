# Standard — Cycle Doc (CYC)

| Field | Value |
|---|---|
| **Status** | Active |
| **Version** | 1.3.0 |
| **Owner** | skills-tinky maintainer |
| **Approvers** | skills-tinky maintainer |
| **Effective date** | 2026-08-19 |
| **Applies to** | The per-cycle work doc for Foleon cycles — the local markdown file that is its source of truth, stored in the maintainer's own cycle directory (**not** in `skills-tinky`, see CYC-1), and the single Notion page that mirrors it — written and maintained by the `foleon-cycle` skill across every repo a cycle touches (`ripley`, `fio`, and any future Foleon repo) |

**Reference implementation** — `foleon/foleon-cycle` (to be built against this standard; no
implementation exists at v1.0.0). The Notion mirror is one page per cycle, nested by project the way
[`CHEAT_SHEET.md`](CHEAT_SHEET.md) CHS-9a nests category pages — never a database.

---

## Problem

The maintainer works a **ShapeUp/Scrum hybrid**: each cycle arrives as a set of topics with an
estimated time per topic, and turning those into an actual development plan — tasks, sequence,
progress — is left to the developer. Done in the head, that plan is invisible by Wednesday of week
two: which topic is at risk, what was cut and why, what "done" was agreed to be, and where the
unknowns still sit all decay into recollection. Done in a ticket tracker, it fragments into rows
that record task state and lose the shaping — the appetite, the no-gos, the first thing to cut.

Two failure modes bound this standard, and they pull in opposite directions:

1. **Under-shaped intake.** Work starts before anyone can say what "done" looks like. Shape Up names
   this precisely with the "2.0" grab-bag: *"The project turned out to be a mess because we didn't
   know what 'done' looked like."* `[SRC-001]`
2. **A doc that becomes a diary.** Every session appends narration until the doc is longer than the
   work and nobody opens it. This is the same defect [`CHEAT_SHEET.md`](CHEAT_SHEET.md) v2.0.0
   removed from the cheat sheet — *"this is not a cheat-sheet, it's a document with 10000 of
   infos"* `[SRC-007]` — arriving by a different route.

The doc exists to answer four questions at a glance, at any point in the cycle: **what am I building,
how much time is it worth, where are the unknowns, and what gets cut first.** Task state is the least
valuable thing in it — Shape Up is explicit that counting to-dos cannot tell you a project's status,
because *"there's no way to know whether the number of outstanding tasks will go down or up"*
`[SRC-003]`.

**Success metrics** — see [§ Metrics](#metrics). In short: every topic leaves intake shaped, the dev
log stays signal, and the maintainer can answer "where is this" without reading the whole file.

## Scope

**In scope:** the structure of a cycle doc, what makes a topic ready to leave intake, how scopes and
tasks are recorded, how progress is expressed, what earns a dev-log line, how a multi-repo cycle
nests, and who approves the Notion mirror before it is written.

**Out of scope:**
- **Durable project knowledge** — conventions, gotchas, stack facts. Those belong in the relevant
  project-context skill's `references/knowledge.md`, governed by
  [`PROJECT_CONTEXT_SKILL.md`](PROJECT_CONTEXT_SKILL.md) PCS-6, and reach a human surface via
  [`CHEAT_SHEET.md`](CHEAT_SHEET.md). See [CYC-12](#cyc-12-durable-facts-leave-the-cycle-doc).
- **The retrospective.** Cycle-end analysis of commits and next steps is the `sprint-review` skill's
  job; this standard only requires the doc be left in a state that skill can read (CYC-13).
- **Hook and skill mechanics** — queue format, file watching, MCP call sequences. Implementation
  detail of `foleon-cycle`, constrained here only by CYC-11.
- **Cycle length and the betting process.** The maintainer's cycles are set by their team, not by
  this repo. This standard records what a cycle *is* once given; it does not prescribe six weeks,
  cool-down, or a betting table.

---

## Normative rules

### CYC-1 One doc per cycle, local source of truth, outside every checkout

- There **MUST** be exactly **one** cycle doc per cycle, and it **MUST** cover every repo that cycle
  touches. A per-repo cycle doc **MUST NOT** be created. `[SRC-009]`
- The **local markdown file MUST be the source of truth.** The Notion page is a mirror derived from
  it (CYC-10). `[SRC-009]`
- The file **MUST** live in a **dedicated cycle directory owned by the maintainer**, outside every
  code repository — including `skills-tinky`. The default is
  `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES`, overridable with the `FOLEON_CYCLE_HOME` environment
  variable. `[SRC-008]` `[SRC-010]`
- The doc **MUST NOT** be written into any Foleon repo checkout — not `ripley`, not `fio`, not as a
  git-ignored file — and **MUST NOT** be written into `skills-tinky`, whose scope is skills and their
  scaffolding, not work product. `[SRC-010]`
- Runtime state that supports the doc (the unlogged-work queue) **MUST** live in the same cycle
  directory, under `.state/`, so the whole system has exactly one location. `[SRC-010]`
- The filename **MUST** be the cycle identifier (`<cycle-id>.md`), and the cycle identifier **MUST**
  be whatever the maintainer's team calls that cycle — this standard defines no naming scheme.
- The cycle directory **MAY** keep a **local-only git history**, and `foleon-cycle` **MAY** commit to
  it automatically — at cycle open, on each approved log line, at close, and on an explicit
  `snapshot`. This is a **named carve-out** from the maintainer's standing rule that nothing commits
  without per-message consent, granted for this directory alone. `[SRC-011]`
- That history **MUST NOT** have a git remote and **MUST NOT** be pushed; `foleon-cycle` **MUST**
  refuse to commit if a remote exists. The queue under `.state/` **MUST NOT** be versioned.
  `[SRC-011]`
- Commit messages in this history **MUST** carry a `Co-Authored-By: Claude Opus 5
  <noreply@anthropic.com>` trailer — the plans and log lines are written collaboratively, so the
  history records it. This applies to **this history only**; it is not a global git convention.
  `[SRC-011]`
- A failed commit **MUST NOT** fail the write that preceded it — the markdown is the artifact, the
  history is a convenience.

**Rationale:** a cycle spans repos, so no single checkout can host its state without becoming wrong
for the others. `PROJECT_CONTEXT_SKILL.md` PCS-9a already draws this line for context skills — the
team owns the checkout, the maintainer owns the silo `[SRC-008]`. But the silo for *skills* is not the
silo for *work product*: `skills-tinky` is a skills repo, shared across the maintainer's professional
and personal work and pushed to GitHub, so cycle docs there would be both off-topic and published
`[SRC-010]`. A dedicated directory keeps the two lifecycles apart — skills are versioned and shared,
cycle docs are working artifacts that stay on the laptop. Local-first still means the doc is editable
at conversation speed and survives an absent MCP connection, which a Notion-first design does not.

**Enforcement:** `foleon-cycle` resolves the cycle directory from `FOLEON_CYCLE_HOME` or the default,
never from the cwd; a write resolving inside any git work tree that is not the cycle directory fails
closed. `scripts/cycle.py`'s `snapshot()` stages only the cycle directory, aborts when `git remote`
returns anything, writes a `.gitignore` covering `.state/` at init, and downgrades every git failure
to a warning.

One-file-per-cycle is visible in the directory listing.

### CYC-2 Required structure

- A cycle doc **MUST** contain, in order: a **header** (cycle id, dates, status), one **topic
  section** per topic, and one **dev log** section. Nothing else. `[SRC-009]`
- A topic section **MUST** carry the shaped fields of CYC-3, then its scope subsections.
- A scope subsection **MUST** carry a hill position drawn from exactly these four values:

  | Value | Meaning `[SRC-003]` |
  |---|---|
  | `uphill` | Still figuring out the approach; unknowns unresolved |
  | `top` | Approach is known and all remaining work is visible; nothing built yet |
  | `downhill` | Executing known work |
  | `done` | Every must-have task complete (CYC-7) |

- The canonical skeleton:

  ```markdown
  # Cycle <cycle-id>
  Dates: <start> → <end> · Status: active

  ## [<repo>] <topic name>
  Outcome: <one sentence, observable, user-facing>
  Appetite: <time> (fixed) · First cut: <what goes first>
  No-gos: <explicitly out of scope>
  Done when: <the done signal>
  Open questions: <unanswered at intake, or omitted if none>

  ### scope: <maintainer's name for it> — <hill value>
  - [x] <task>
  - [ ] ~ <nice-to-have task>

  ## Dev log
  - <date> [<repo>] <scope> → <what changed>
  ```

- A field with no content **MUST** be omitted, not written empty. A section heading with nothing
  under it **MUST NOT** exist.

**Rationale:** a fixed skeleton is what lets a hook, a skill, and a human read the same file without
a parser. The four hill values are the hill chart `[SRC-003]` reduced to tokens a text file can carry
and a checker can validate — see [override 5](#documented-overrides).

**Enforcement:** `foleon-cycle` validates the skeleton on every write; unknown hill values and empty
sections fail closed.

### CYC-3 Shaped enough to leave intake

- A topic **MUST NOT** proceed to scopes or tasks until all six fields are present: **outcome**,
  **appetite**, **first cut**, **no-gos**, **done signal**, and **repo tag**. `[SRC-001]` `[SRC-005]`
- The **outcome MUST** be one sentence describing something **observable from outside the code** —
  what a user, reviewer, or demo can see. It **MUST NOT** be a restatement of the topic title, and
  **MUST NOT** be a technical task ("refactor the extractor").
- The **done signal MUST** name the event that ends the topic (merged, deployed, demoed, reviewed by
  a named person) — not a percentage, not "when it works". `[SRC-001]`
- Intake **MUST** ask about **rabbit holes** — the part the maintainer does not yet know how to do —
  and each one named **MUST** become either a scope at `uphill` or an open question. `[SRC-005]`
- Any field the maintainer cannot answer **MUST** be recorded verbatim under **Open questions**. The
  writing agent **MUST NOT** fill it with an inferred answer, and **MUST NOT** treat its own proposal
  as an answer. `[SRC-009]`
- Interview depth **SHOULD** scale to appetite: a topic of two days or less needs only outcome,
  no-gos and done signal; the full set applies at roughly a week or more.

**Rationale:** Shape Up's grab-bag failure is diagnosed as not knowing what done looked like
`[SRC-001]`, and its shaping phase exists to surface rabbit holes *before* the work is bet on
`[SRC-005]`. The recorded-not-inferred rule is the maintainer's own standing preference, and it is
also the only way the doc stays trustworthy: an inferred outcome is indistinguishable from an agreed
one three weeks later.

**Enforcement:** `foleon-cycle` refuses to create scopes for a topic missing any required field; the
missing field is named back to the maintainer.

### CYC-4 Appetite is a budget, not an estimate

- The appetite **MUST** be recorded as the time the topic is *worth*, marked `(fixed)`, even when the
  number came from the team as an estimate. `[SRC-001]`
- The appetite **MUST NOT** be revised upward mid-cycle. When work exceeds it, the response **MUST**
  be scope hammering (CYC-7) or an explicit re-bet — and a re-bet **MUST** be recorded as a dev-log
  line stating what changed and who decided. `[SRC-001]` `[SRC-004]`
- The **first cut MUST** be recorded at intake: the first thing to go when time runs short. It
  **MUST** be a named piece of the topic, not "polish" or "tests".

**Rationale:** *"An appetite is completely different from an estimate. Estimates start with a design
and end with a number. Appetites start with a number and end with a design."* `[SRC-001]` The first
cut is written at intake because that is the only moment it can be decided calmly — at 80% spent it
is decided under pressure, which is when quality is sacrificed instead of scope `[SRC-004]`.

**Enforcement:** reviewed at intake (required field, CYC-3); an upward appetite edit without a
re-bet log line fails closed.

### CYC-5 Scopes — integrated slices, named by the maintainer

- A scope **MUST** be independently finishable and **SHOULD** be a few days or less of work.
  `[SRC-002]`
- A scope **MUST** integrate the work needed to finish that slice — front-end and back-end together —
  by default. A UI-only or back-end-only scope **MAY** be used where the work is a genuine
  **iceberg** (one side substantially more complex than the other and not interdependent with it),
  and the reason **MUST** be stated in the doc. `[SRC-002]`
- Scope names **MUST** be the maintainer's own words. The writing agent **MAY** propose names and
  **MUST** present them as a draft; only a name the maintainer accepted or rewrote may be written.
  `[SRC-002]` `[SRC-009]`
- A scope **MAY** exist with no tasks under it, marking work known to be needed but not yet
  discovered. `[SRC-003]`
- A topic **SHOULD** hold roughly two to five scopes. One scope means the topic was not factored; more
  than five means the scopes are tasks.

**Rationale:** *"Scopes are more than just slices. They become the language of the project at the macro
level."* `[SRC-002]` A name the maintainer would not use in speech defeats the purpose, which is why
the agent proposes and never decides. The iceberg allowance is Shape Up's own — a layer cake is
*"a good default for most 'information system' type apps"*, and factoring the UI out is recommended
specifically when the back end is disproportionately complex `[SRC-002]`.

**Enforcement:** reviewed at intake; scope naming requires an explicit maintainer response before the
write. Scope count is visible in the doc.

### CYC-6 Hill position is set by a human, never inferred

- A scope's hill position **MUST** be set by the maintainer. The writing agent and any hook **MUST
  NOT** derive it from files touched, commits, task counts, or elapsed time. `[SRC-003]`
- When the maintainer does not state a position, it **MUST** remain unchanged. There is no default
  advance.
- A scope moving **backwards** (`downhill` → `uphill`) is a legitimate and expected event. It **MUST
  NOT** be flagged as an error, silently corrected, or averaged away. `[SRC-003]`
- Task completion **MUST NOT** be rendered as a percentage anywhere in the doc or the mirror.
  `[SRC-003]`

**Rationale:** the hill measures *knowledge*, not output — the uphill phase is *"full of uncertainty,
unknowns, and problem solving"* `[SRC-003]`, and no file-level signal distinguishes an afternoon of
productive execution from an afternoon of discovering the approach was wrong. Shape Up adopts the hill
precisely because estimates and task counts *"don't show uncertainty"* `[SRC-003]`; re-introducing a
percentage would import the defect the metaphor exists to remove.

**Enforcement:** structural — no hill value is written except from a maintainer statement; there is no
inference path to disable.

### CYC-7 Tasks — under a scope, must-have by default, `~` for nice-to-haves

- A task **MUST** belong to exactly one scope. A task list at topic level, or a task with no scope,
  **MUST NOT** exist. `[SRC-002]`
- A task **SHOULD** be half a day to two days of work. Anything larger is a scope; anything smaller
  **SHOULD NOT** be tracked at all.
- Tasks **MUST NOT** be created for a topic until its scopes have been accepted by the maintainer
  (CYC-5).
- A task is a **must-have** by default. A **nice-to-have MUST** be written with a leading `~` and
  **MUST NOT** block a scope reaching `done`. `[SRC-004]`
- Marking a task `~` **IS** the scope-hammering action and **MUST** be recorded as such — it is a
  decision, not bookkeeping, and therefore earns a dev-log line under CYC-8 gate 2. `[SRC-004]`
- A scope reaches `done` when every must-have under it is complete; outstanding `~` tasks **MAY**
  remain under a `done` scope. `[SRC-004]`

**Rationale:** verbatim Shape Up convention — nice-to-haves *"are marked with a tilde (~) in front…
The act of marking them as a nice-to-have is the scope hammering"* `[SRC-004]`. Adopting the marker
rather than a status field means hammering costs one keystroke and leaves a visible trail of what was
consciously dropped, which is exactly what a cycle doc should be able to show at the end.

**Enforcement:** mechanically checkable — `~` prefix, task depth under a scope heading, and the
scope-accepted precondition are all validated on write.

### CYC-8 Dev log — three admission gates

- A dev-log line **MUST** pass at least one of three gates: `[SRC-006]`
  1. **State change** — a scope changed hill position, a must-have completed, a scope reached `done`,
     or work became blocked.
  2. **Decision** — something was chosen or cut: a scope hammered (CYC-7), an appetite re-bet
     (CYC-4), an approach picked over another.
  3. **Surprise** — reality differed from the shaping: a rabbit hole opened, an assumption in the
     doc turned out false, an open question got answered.
- A line **MUST NOT** be written for: work git already records (files changed, commits made), routine
  progress narration ("continued on the extractor"), or restating a task's checkbox state.
- A line **MUST** be one line, dated, and tagged with its repo and scope. `[SRC-009]`
- A line **MUST** be written in the past tense and state the outcome, not the activity: *"tables
  deferred — nested cells need their own layout pass"*, not *"worked on tables"*.
- The log **MUST** be append-only within a cycle. Correcting an earlier line means appending a new
  one, never editing history.

**Rationale:** the log's job is what the Daily Scrum's is in the Scrum half of the hybrid — *"to
inspect progress toward the Sprint Goal and adapt the Sprint Backlog as necessary"* `[SRC-006]` —
performed asynchronously by one developer (see [override 4](#documented-overrides)). Anything git
already stores is not progress information, it is duplication, and it is what turns the doc into the
diary this standard exists to prevent.

**Enforcement:** gates are stated by the writing agent when proposing an entry; banned patterns
("worked on", "continued", bare file lists) are greppable. Append-only is checkable by diff.

### CYC-9 Multi-repo cycles nest by project

- Topics **MUST** be tagged with their repo (`[fio]`, `[ripley]`). A topic spanning two repos **MUST**
  carry both tags and **MUST** be written once — never duplicated per repo. `[SRC-007]`
- The Notion mirror **MUST** nest by project the way CHS-9a nests category pages: the cycle page holds
  one section per repo, and a topic appears under its repo's section only. `[SRC-007]`
- A cross-repo topic **MUST** be placed under the repo where the work primarily lands, with the other
  tag naming the dependency. The test is CHS-9b's, adapted: *would this topic still exist if that repo
  were removed from the cycle?* `[SRC-007]`
- The repo tag **MUST** determine which project-context skill applies while working that topic
  (`foleon-fio` or `foleon-ripley`), and `foleon-cycle` **SHOULD** name it when work on that topic
  begins.

**Rationale:** the maintainer works `ripley` and `fio` in the same cycle, with more repos expected.
`CHEAT_SHEET.md` already solved the shape of this exact problem for a second surface — nest by
project, prefix for search, write cross-project facts once `[SRC-007]` — and inventing a second
answer would leave two conventions to remember for one workspace. The context-skill link matters
because the two repos carry contradictory conventions, so knowing which topic you are on determines
which rules apply.

**Enforcement:** tag presence validated on write; duplicate-topic detection by title across repo
sections; reviewed at mirror time (CYC-11).

### CYC-10 Local-vs-mirror boundary

- The mirror **MUST** be a Notion **page** per cycle. It **MUST NOT** be a database, and topics,
  scopes and tasks **MUST NOT** become database rows or carry Notion properties. `[SRC-007]`
- The mirror **MUST** carry: the header, every topic with its full shaped fields, every scope with its
  hill position and its **must-have completion state**, open questions, and the dev log.
- The mirror **SHOULD NOT** carry individual task checkboxes where a scope has more than a handful —
  a scope's hill position and its done/not-done state is the reportable unit. `[SRC-002]` `[SRC-003]`
- The mirror is **derived**. On any divergence, the local file wins. `foleon-cycle` **MUST** surface a
  divergence it detects rather than overwriting silently, and **MUST NOT** read the mirror back into
  the local file as an update path. `[SRC-009]`
- The mirror **MUST** be regenerated whole from the local file, never patched line by line from a
  diff.

**Rationale:** the mirror exists so the plan is readable and shareable without opening a terminal —
that is a reporting surface, and Shape Up is explicit that reporting happens at scope level, where
*"it's more satisfying to have the conversation at a high level and point to finished pieces of
software, instead of going down into the weeds"* `[SRC-002]`. One-way derivation is what keeps two
copies from becoming two truths; the no-database rule is `CHEAT_SHEET.md` v2.0.0's finding, which
cost a full architecture reversal to learn once already `[SRC-007]`.

**Enforcement:** whole-page regeneration is the only write path implemented; database creation calls
are absent by construction. Divergence check runs before every mirror write.

### CYC-11 Consent gate before any Notion write

- Mirror content **MUST** be shown to the maintainer — the actual text, the actual target page —
  **before** anything is written to Notion, and only an explicit **yes** in that conversation
  authorises the write. `[SRC-007]`
- A hook **MAY** detect unlogged work and queue it. A hook **MUST NOT** write to Notion, and **MUST
  NOT** write a dev-log line into the local file on its own. Queued items are **proposals** the
  maintainer accepts, edits, or drops. `[SRC-009]`
- There **MUST NOT** be an approval status, review queue, or workflow inside Notion — the
  conversation is the review. `[SRC-007]`
- `foleon-cycle` **MUST** be invoked **explicitly** (`/foleon-cycle`). Its description **MUST NOT**
  carry phrase triggers intended to auto-load it, and **MUST** state that it is only for explicit
  invocation. `[SRC-009]`

**Rationale:** the maintainer's standing preference is explicit control over automation, and the
cheat-sheet pipeline already proves the shape works: a hook makes capture durable and reasoning-free,
a conversation decides what it means `[SRC-007]`. The explicit-invocation rule is a direct
requirement — a skill that loads itself on a keyword phrase is an automatic action by another route.

**Enforcement:** structural — the only Notion write path runs after a recorded yes; the hook binary
has no Notion credentials and no local-file write path. Description conformance is checked by
`concierge`.

### CYC-12 Durable facts leave the cycle doc

- A discovery that will still be true after the cycle ends — a convention, a gotcha, a command, an
  architectural constraint — **MUST** go to the relevant project-context skill's
  `references/knowledge.md` (PCS-6), and **MUST NOT** be recorded in the cycle doc as its permanent
  home. `[SRC-008]`
- The dev log **MAY** note that such a discovery happened when it also passes a CYC-8 gate (typically
  gate 3, surprise), but the durable statement of the fact belongs in the log of record.
- A cycle doc **MUST NOT** be treated as a knowledge source by any other skill. It is time-bound by
  construction and is archived at cycle end (CYC-13).

**Rationale:** the cheat-sheet pipeline already routes durable facts from `knowledge.md` to a human
surface `[SRC-007]` `[SRC-008]`. A fact recorded only in a cycle doc is invisible to that pipeline and
buried in an archive within weeks — the worst of both. Keeping the boundary sharp is also what stops
the dev log from growing into the second knowledge base nobody maintains.

**Enforcement:** reviewed when logging; a candidate line that states a durable fact is redirected to
the project skill's log instead, and the maintainer is told which one.

### CYC-13 Cycle close

- At cycle end the doc **MUST** record, per topic: what shipped, what was cut (the surviving `~`
  tasks and any hammered scope), and the final hill position of every scope. `[SRC-004]`
- Any scope still `uphill` at close **MUST** be flagged as a **shaping signal**, not a personal
  failure — it indicates the topic was under-shaped at intake. `[SRC-004]`
- The header status **MUST** move to `closed`, and the doc **MUST** become read-only: no new dev-log
  lines, no hill changes. Follow-on work belongs to the next cycle's doc.
- Cycle-end analysis **MUST** be delegated to `sprint-review` rather than performed by
  `foleon-cycle`; the closed doc is its input.

**Rationale:** Shape Up's stopping test is that remaining work be *"all downhill. No unsolved
problems; no open questions. Any uphill work at the end of the cycle points to an oversight in the
shaping or a hole in the concept."* `[SRC-004]` Recording that as a signal is what makes the next
intake better — it is the only feedback loop this system has. Read-only at close protects the archive
from becoming an editable scratchpad, and delegation keeps `foleon-cycle` from reimplementing a skill
that already exists.

**Enforcement:** `foleon-cycle` refuses writes to a `closed` doc; the close routine requires the
per-topic shipped/cut record before flipping status.

---

## Documented overrides

| # | Source rule | Override | Justification |
|---|---|---|---|
| 1 | Shape Up: a team of two or three **discovers** its own scopes `[SRC-002]` | An agent **proposes** scopes; only maintainer-accepted names are written (CYC-5) | The team is one developer plus an assistant. A proposal is a draft, not an authority — and the naming requirement (maintainer's own words) preserves what the original rule protects. |
| 2 | Shape Up: shaping produces no task list; tasks are discovered while building `[SRC-002]` | Intake produces a first task list per accepted scope (CYC-7) | The maintainer's stated need is to plan the development up front `[SRC-009]`. Mitigated: tasks require accepted scopes first, scopes may hold no tasks (CYC-5), and tasks are never a status measure (CYC-6). |
| 3 | Shape Up: six-week cycles plus two-week cool-down `[SRC-001]` | Cycle length unspecified; dates recorded per cycle (CYC-2) | Cycles are set by the maintainer's team in a ShapeUp/Scrum hybrid. Hard-coding six weeks would make the standard wrong on contact. |
| 4 | Scrum: the Daily Scrum is a synchronous 15-minute team event `[SRC-006]` | An asynchronous dev-log line, written when something changes (CYC-8) | A solo developer has no team to synchronise with; the *purpose* the Scrum Guide states — inspect progress, adapt the plan — is preserved, only the ceremony is dropped. |
| 5 | Shape Up: the hill chart is a continuous position on a curve `[SRC-003]` | Four discrete values: `uphill`, `top`, `downhill`, `done` (CYC-2) | A markdown file needs a token a checker can validate. The four values keep the only distinction the metaphor is *for* — unknowns versus execution — and the `top` value preserves the pivot point where estimation first becomes meaningful `[SRC-003]`. |

---

## Conformance checklist

A cycle doc is conforming when **all** are true:

- [ ] One doc for the whole cycle, local file authoritative, stored in the maintainer's cycle directory — outside every code repo, `skills-tinky` included (CYC-1)
- [ ] If the cycle directory keeps git history: no remote, never pushed, `.state/` unversioned, and a failed commit never costs the write (CYC-1)
- [ ] Header, topics, dev log — in order, no empty sections, hill values from the closed set of four (CYC-2)
- [ ] Every topic has outcome, appetite, first cut, no-gos, done signal, repo tag; unanswered items recorded as open questions, never inferred (CYC-3)
- [ ] Appetite marked `(fixed)`, never revised upward without a logged re-bet; first cut named at intake (CYC-4)
- [ ] Scopes are independently finishable slices, named in the maintainer's words, integrated unless a stated iceberg (CYC-5)
- [ ] Every hill position traceable to a maintainer statement; no percentages anywhere (CYC-6)
- [ ] Every task under exactly one scope; nice-to-haves prefixed `~`; scope `done` ignores outstanding `~` (CYC-7)
- [ ] Every dev-log line passes a state-change / decision / surprise gate; nothing restates git; append-only (CYC-8)
- [ ] Topics repo-tagged; cross-repo topics written once; mirror nested by project (CYC-9)
- [ ] Mirror is one page, regenerated whole from local, never read back as an update path, no database (CYC-10)
- [ ] Nothing written to Notion without an explicit yes in that conversation; hooks queue only; skill is explicit-invocation only (CYC-11)
- [ ] Durable facts routed to the project-context skill's `knowledge.md`, not parked in the cycle doc (CYC-12)
- [ ] At close: shipped/cut recorded per topic, residual `uphill` flagged as a shaping signal, status `closed`, retro delegated to `sprint-review` (CYC-13)

## Enforcement

| Mechanism | Covers | Automated |
|---|---|---|
| Skeleton + hill-value validation on every local write | CYC-2, CYC-7 | Yes |
| Path check — write inside a repo checkout fails closed | CYC-1 | Yes |
| Required-field gate before scopes/tasks are created | CYC-3, CYC-5, CYC-7 | Yes (presence), judged (quality) |
| Banned dev-log patterns greppable ("worked on", "continued", bare file lists) | CYC-8 | Yes |
| Hill position written only from a maintainer statement — no inference path exists | CYC-6 | Structural |
| Whole-page mirror regeneration; no database calls in the implementation | CYC-10 | Structural |
| Conversational approval before any Notion write; hook has no write path | CYC-11 | Structural, by design |
| Description carries no phrase triggers | CYC-11 | Yes — `concierge` audit |
| Durable-vs-time-bound routing judgement | CYC-12 | No — judgement, by design |
| Close routine requires shipped/cut record before flipping status | CYC-13 | Yes |

## Exceptions

Exceptions follow the repo's standard waiver process: rule ID, justification, risk, mitigation,
expiry (≤ 90 days), rollback.

None standing.

## Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Intake completeness** | 100% of topics leave intake with all six CYC-3 fields | Checked at intake; countable in the doc |
| **Open-question resolution** | every open question answered or explicitly dropped by close | Read at cycle close |
| **Dev-log signal** | 0 lines restating git or narrating routine work | Read-through at close |
| **Log volume** | roughly ≤ 1 line per working day per active topic | Count at close |
| **Cut visibility** | every cut traceable to a `~` mark or a logged decision | Read at cycle close |
| **Residual uphill** | 0 scopes `uphill` at close; each occurrence feeds the next intake | Recorded at close (CYC-13) |
| **Mirror freshness** | mirror never more than one working day behind the local file while the cycle is active | Divergence check at mirror time |
| **Consultation** | the maintainer opens the doc to answer "where is this", instead of reconstructing it | Self-report |

## Sources

- `[SRC-001]` Singer, R. — *Shape Up*, ch. 3 "Set Boundaries". https://basecamp.com/shapeup/1.2-chapter-03 — appetite as a time budget; *"an appetite is completely different from an estimate"*; fixed time / variable scope; the "2.0" grab-bag and not knowing what done looks like.
- `[SRC-002]` Singer, R. — *Shape Up*, ch. 12 "Map the Scopes". https://basecamp.com/shapeup/3.3-chapter-12 — scopes as integrated slices finishable independently, *"a few days or less"*; scopes as the project's language; reporting at scope level; layer cakes as the default and icebergs as the reason to factor out a UI-only scope.
- `[SRC-003]` Singer, R. — *Shape Up*, ch. 13 "Show Progress". https://basecamp.com/shapeup/3.4-chapter-13 — to-do counts cannot show status; *"estimates don't show uncertainty"*; the hill metaphor, uphill as unknowns and downhill as execution; a scope may exist before its tasks are discovered.
- `[SRC-004]` Singer, R. — *Shape Up*, ch. 14 "Decide When to Stop". https://basecamp.com/shapeup/3.5-chapter-14 — scope grows like grass; cutting scope is not lowering quality; scope hammering; the `~` nice-to-have marker; remaining work must be all downhill at the end or the shaping was wrong.
- `[SRC-005]` Singer, R. — *Shape Up*, ch. 5 "Risks and Rabbit Holes". https://basecamp.com/shapeup/1.4-chapter-05 — shaping must surface rabbit holes before the work is bet on.
- `[SRC-006]` Schwaber, K. & Sutherland, J. — *The Scrum Guide* (2020). https://scrumguides.org/scrum-guide.html — *"The purpose of the Daily Scrum is to inspect progress toward the Sprint Goal and adapt the Sprint Backlog as necessary"*; basis for the dev-log cadence in the hybrid.
- `[SRC-007]` Internal — [`CHEAT_SHEET.md`](CHEAT_SHEET.md) (CHS 2.4.0). Page-not-database (v2.0.0 reversal), CHS-9a project nesting, CHS-9b write-once for cross-project facts, CHS-9 conversational review gate. Reused rather than re-derived.
- `[SRC-008]` Internal — [`PROJECT_CONTEXT_SKILL.md`](PROJECT_CONTEXT_SKILL.md) (PCS). PCS-6 discoveries log as the home of durable facts; PCS-9a silo-versus-checkout boundary; PCS-11 single external mirror.
- `[SRC-011]` Internal — the maintainer's authorisation, 2026-08-19, verbatim: *"SHAPEUP-CYCLES may auto-commit"*, given after asking for a system that needs no repo handling: *"i am just scared of the handling of the repo. how often do we push? can you make a system that is 100% independant?"* The answer that satisfied it — no remote, so no pushing is possible, and commits made by the tool rather than by hand — is what CYC-1 now requires.
- `[SRC-010]` Internal — the maintainer's correction, 2026-08-19: *"we are completely going out of scope on skills-tinky repo! it's supposed to be a repo for skills and things that revolve around that, not to keep track of my cycles. this repo is used by me for both pro and perso."* The v1.0.0 placement (the skill's own `state/` directory) was wrong on both counts — off-topic for that repo, and pushed to GitHub.
- `[SRC-009]` Internal — the maintainer's stated requirements, session of 2026-08-17/18: local-first with a Notion mirror; scopes and tasks with a hill chart; hook proposes and the maintainer approves; Foleon-only across `ripley`, `fio` and future repos; `/foleon-cycle` explicit invocation with no phrase triggers.

## Change log

| Version | Date | Change |
|---|---|---|
| **1.3.0** | 2026-08-19 | **Commits in the cycle history carry a `Co-Authored-By: Claude` trailer**, at the maintainer's request and scoped to this history alone — not a global git convention. The cycle doc's plans and log lines are written collaboratively, so the history says so. |
| **1.2.0** | 2026-08-19 | **Local-only git history in the cycle directory, authorised as a named carve-out.** The maintainer wanted history without repo maintenance — *"how often do we push? can you make a system that is 100% independant?"* — and authorised auto-commit for this directory alone `[SRC-011]`. CYC-1 gains four bullets: the directory MAY keep git history; `foleon-cycle` MAY commit at open / approved log line / close / explicit `snapshot`; the history MUST NOT have a remote and MUST NOT be pushed (the skill refuses to commit if one exists), and `.state/` MUST NOT be versioned; a failed commit MUST NOT fail the write. Recorded here rather than left as folklore precisely because it is an exception to a standing rule — the exception is auditable, scoped to one directory, and cannot become a habit that spreads. |
| **1.1.0** | 2026-08-19 | **Storage moved out of `skills-tinky`.** v1.0.0's CYC-1 put cycle docs in the skill's own `state/` directory, reasoning from PCS-9a's silo principle. The maintainer corrected it before any doc existed: `skills-tinky` is a repo for skills, used for both professional and personal work, and pushed to GitHub — so cycle docs there are both out of scope and published `[SRC-010]`. CYC-1 now requires a dedicated maintainer-owned cycle directory outside every code repository (default `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES`, overridable via `FOLEON_CYCLE_HOME`), and puts the unlogged-work queue in that same directory under `.state/` so the system has one location rather than two. Enforcement changed from "not inside a known repo checkout" to "resolved from the configured cycle directory, never the cwd". No other rule is affected: local-first, one-way mirroring and the consent gate are unchanged. |
| **1.0.0** | 2026-08-18 | Initial standard. Thirteen rules covering: one local-authoritative doc per cycle stored outside every checkout (CYC-1), a fixed skeleton with four discrete hill values (CYC-2), a six-field intake gate with unanswered items recorded rather than inferred (CYC-3), appetite as a fixed budget with the first cut named at intake (CYC-4), maintainer-named integrated scopes with the iceberg allowance (CYC-5), human-only hill positions and no percentages (CYC-6), tasks under scopes with Shape Up's `~` nice-to-have marker as the scope-hammering action (CYC-7), a three-gate dev log that never restates git (CYC-8), multi-repo nesting reusing CHS-9a/9b (CYC-9), a one-way whole-page Notion mirror that is never a database (CYC-10), a conversational consent gate with hooks that queue but never write and explicit-only invocation (CYC-11), durable facts routed out to the project-context logs (CYC-12), and a close routine that flags residual uphill work as a shaping signal and delegates the retro to `sprint-review` (CYC-13). Five documented overrides record where solo work and the maintainer's hybrid diverge from Shape Up and Scrum as written. |
