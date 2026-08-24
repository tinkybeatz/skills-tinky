# Standard — Cycle Doc (CYC)

| Field | Value |
|---|---|
| **Status** | Active |
| **Version** | 5.1.0 |
| **Owner** | skills-tinky maintainer |
| **Approvers** | skills-tinky maintainer |
| **Effective date** | 2026-08-24 |
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
how much time is it worth, where are the unknowns, and what gets cut first.** From those answers it
produces the thing the maintainer actually works from: a **prioritised list of tickets and tasks**
(CYC-14) — tickets to paste into Jira, and personal tasks for the work Jira handles badly. Task state is the least
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
- A cycle is **8 weeks: a 6-week dev window followed by 2 weeks of cooldown** (bug-fixing, research).
  The header's `Dates:` range **MUST** be the **dev window**, with the cooldown end recorded after it:
  `Dates: 2026-08-18 → 2026-09-29 · Cooldown: → 2026-10-13`. `[SRC-013]`
- **Cooldown work MUST NOT be tracked in the doc.** It has no appetite, no no-gos and nothing to place
  on a hill, so putting it through intake would force shaping onto work that is unshaped by
  definition. The doc covers the dev window; cooldown is off-book. `[SRC-013]`
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

### CYC-3 Two topic states: shaping, then shaped

- Every topic **MUST** declare its state in its heading — `## [fio] GTM Analytics — shaping` or
  `— shaped`. An undeclared state is a conformance error, not a default. `[SRC-014]`
- A **shaping** topic is one nobody can specify yet. It **MUST** carry only: a **repo tag**, an
  **appetite** (which **MAY** be marked `(provisional)`), and at least one **open question** — the
  open questions are what make it *shaping* rather than merely unstarted. It **MUST NOT** be required
  to state an outcome, done signal or first cut. `[SRC-014]`
- A shaping topic's scopes **MUST** all be `uphill`, and it **MUST** hold only `self:` research tasks
  (CYC-7). Implementation work requires a shaped topic. `[SRC-014]`
- A **shaped** topic **MUST** carry all six fields: **outcome**, **appetite**, **first cut**,
  **no-gos**, **done signal**, **repo tag**. `[SRC-001]` `[SRC-005]`
- The transition **MUST** be a deliberate act — the answers arrive (a call, a decision, a document),
  the research tasks that asked for them are closed, the fields are filled, and the state flips. The
  writing agent **MUST NOT** flip a topic to `shaped` on its own inference. `[SRC-014]`
- When answers arrive, they **MUST** be **re-evaluated** rather than simply applied: each remaining
  open question is classified **blocking** (the outcome or done signal cannot be written without it) or
  **non-blocking**, and one of three moves is proposed **with its reasoning** and agreed before
  execution — **hold**, **split**, or **shape**. A topic **MUST NOT** be held on a non-blocking
  question, and a blocking question **MUST NOT** be downgraded to get a topic moving. `[SRC-016]`
- A topic **MAY** be **split** when only part of it is knowable: one `shaped` half plus one `shaping`
  half. The shaped half **MUST** be independently shippable — if it only makes sense once the other
  half lands, it is one topic still shaping, not a split — **MUST** carry no open questions, and the
  appetite **MUST** be divided between the halves rather than duplicated. `[SRC-016]`
- The **sum of all appetites SHOULD NOT** exceed the dev window; `status` reports the total booked
  against it and names over-booking. `[SRC-016]`
- An entry under `Open questions:` **MUST** actually ask something — a question mark anywhere, or a
  clause opening with an interrogative. A caveat or an inference **MUST** go on an `Assumptions:` field
  instead, or be rewritten as the question that would settle it. `[SRC-016]`
- A topic **SHOULD** be escalated rather than researched further once it has spent roughly a quarter
  of its appetite still `shaping`: three weeks of research is not a three-week bet. This is Shape Up's
  circuit breaker applied to shaping. `[SRC-004]` `[SRC-014]`
- Once shaped, the **outcome MUST** be one sentence describing something **observable from outside the code** —
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

**Rationale (revised 2026-08-19, v1.6.0):** v1.0.0 had one state and a hard six-field gate, because
Shape Up assumes shaping happens *before* the bet — done by a senior pair during cool-down, so a team
receives work already shaped. **This maintainer's hybrid does not work that way:** topics arrive as a
title and an estimate, and shaping is part of the cycle. The single gate therefore produced a
deadlock — the research tasks that would answer the questions could not be created until the
questions were answered — and its only escape was writing a guessed `Outcome: TBD`, which passes
validation while producing exactly the untrustworthy file the rule exists to prevent `[SRC-014]`.
Two states keep the rule's purpose (never build against a guess) while letting the *finding out* be
tracked, prioritised and committed like any other work.

Shape Up's grab-bag failure is still diagnosed as not knowing what done looked like
`[SRC-001]`, and shaping still exists to surface rabbit holes *before* implementation
`[SRC-005]`. The recorded-not-inferred rule is the maintainer's own standing preference, and it is
also the only way the doc stays trustworthy: an inferred outcome is indistinguishable from an agreed
one three weeks later.

**Enforcement:** `scripts/cycle.py validate` branches on the declared state — a shaping topic is
checked for appetite and open questions, a shaped one for all six fields — and rejects an undeclared
state, a non-`self:` task under a shaping topic, and a shaping scope that is not `uphill`.
`status` prints the state and warns when a topic has overrun its shaping budget.

### CYC-4 Appetite is a budget, not an estimate

- The appetite **MUST** be recorded as the time the topic is *worth*, marked `(fixed)`, even when the
  number came from the team as an estimate. `[SRC-001]`
- The appetite **MUST NOT** be revised upward mid-cycle. When work exceeds it, the response **MUST**
  be scope hammering (CYC-7) or an explicit re-bet — and a re-bet **MUST** be recorded as a dev-log
  line stating what changed and who decided. `[SRC-001]` `[SRC-004]`
- An appetite **MUST** fit inside the **6-week dev window** (CYC-2). An appetite of 7 weeks or more, or
  over 30 working days, **MUST** be refused at intake — hammer the scope or split the topic. `[SRC-013]`
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
- A **shaping** topic (CYC-3) **MUST** hold only personal tasks — the work of a shaping topic is
  finding out, and finding out is never a ticket. `[SRC-014]`
- A task is one of **two kinds**, because only one belongs in a tracker: `[SRC-013]`
  - **Jira-bound** (the default, unmarked) — implementation work that becomes a ticket (CYC-14).
  - **Personal**, written `self: <text>` — work the maintainer does that is not a ticket: research,
    conceptualising, deciding an approach. Its outcome is typically *producing the tickets*.
- A personal task completing and **adding new tasks to its scope is expected**, not scope creep — that
  is what resolving an unknown does, and CYC-5 already allows a scope to exist before its tasks are
  known. `[SRC-013]`
- A **personal task MUST carry its answer inline when it completes**, appended to the task text as
  `→ answer: <what was decided or found out>`. The task is the question; leaving it ticked and silent
  discards the only thing it produced. The dev-log line stays required where CYC-8 admits one, but the
  log is chronological and the answer belongs where the question is. `[SRC-020]`
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

### CYC-10 The mirror — readable, and writable in one narrow place

- The mirror **MUST** be one Notion **page** per cycle. That page **MAY** be a row in a dedicated
  **`Cycles` database** — a cycle is a bounded unit of a few per year, so a row per cycle is a real
  index, not the unbounded row-per-atom shape `CHEAT_SHEET.md` v2.0.0 removed. `[SRC-012]`
- **Topics, scopes and tasks MUST remain page content.** They **MUST NOT** become database rows and
  **MUST NOT** carry Notion properties. This is the line that matters: the cycle is the unit a row may
  represent, and nothing inside it is. `[SRC-007]` `[SRC-012]`
- The cycle row **MAY** carry properties, and each one **MUST** be **derived** from the local file and
  regenerated on every mirror — never authoritative, never hand-edited as input. The reference set:
  `Name` (cycle id), `Status` (`active` → In progress, `closed` → Done), `Dates` (start → end), and
  `Repos` (multi-select from the topics' repo tags). A property that cannot be regenerated from the
  local file **MUST NOT** be added. `[SRC-012]`
- The mirror **MUST** carry: the header, every topic with its full shaped fields, every scope with its
  hill position and its **must-have completion state**, open questions, and the dev log.
- The mirror **MUST** carry each scope's tasks as **Notion to-do items**, preserving the `~` and
  `self:` markers. These checkboxes are the maintainer's **input surface**: ticking one in Notion is a
  supported way to record that work is done, without going through this skill. `[SRC-015]`
- Exactly **three things MAY be edited in Notion** and taken as authoritative on the next read: a
  task's **checked state**, a task's **text**, and **new task lines** added under an existing scope.
  `[SRC-015]`
- Everything else **MUST** stay local-authoritative, and a Notion-side edit to it **MUST** be reported
  and ignored: topic fields, appetite, no-gos, topic state, **hill positions**, scopes themselves, and
  the dev log. Those either need a gate (the log's three gates) or a human statement that a text box
  cannot enforce (the hill). `[SRC-015]`
- Reading Notion back **MUST** be a **three-way merge** against a stored snapshot of what was last
  mirrored, never a two-way comparison: without the snapshot, a task that is unticked in Notion is
  indistinguishable from one that was never ticked, and one side silently wins. The snapshot **MUST**
  be recorded only after a successful write. `[SRC-015]`
- Reconciliation **MUST NOT** delete anything. A task that disappears from Notion is **reported and
  left in place** locally. `[SRC-015]`
- A genuine collision **MUST** stop the reconcile with nothing written, and **MUST** be resolved by the
  maintainer. Note that a **checked-state collision is unreachable by construction**: if both sides
  move a boolean away from the snapshot they move it to the same value, so the only real collision is
  the same task renamed differently on both sides.
- After a reconcile the doc **MUST** be re-validated, and **MUST NOT** be committed if it no longer
  conforms. `[SRC-015]`
- The mirror **MUST** be regenerated whole from the local file, never patched line by line from a
  diff, and **MUST** be refreshed at the end of every flow that changed the doc — the maintainer reads
  Notion, so a stale mirror is a wrong answer. `[SRC-015]`
- Mirror writes **MUST NOT** require per-write approval. A generated page costs nothing to regenerate,
  so a consent gate there is ceremony; CYC-11's gate applies to **creating** a cycle's row the first
  time, not to refreshing its content. `[SRC-015]`

**Rationale (revised 2026-08-19, v2.0.0):** v1.x made the mirror strictly one-way, on the principle
that two writable surfaces drift. That principle is sound and the conclusion was still wrong for this
maintainer: *"if i want to say i finished a task i dont want to go through claude to tell it that i
did it. i want to update and then claude would be aware the next time i use the cycles tool"*
`[SRC-015]`. A tool that makes you ask permission to tick a checkbox will be abandoned for the tool
that doesn't.

What makes this safe is not trust, it is **scope and mechanism**: exactly three editable things, a
three-way merge against a snapshot so drift is *detectable* rather than silent, no automatic deletion,
and a re-validate before anything is committed. Everything requiring judgement or a gate stays local —
which is why the hill is deliberately not editable in Notion even though the maintainer setting it
there would satisfy CYC-6: it lives inline in rendered text, and parsing it back is fragility bought
for no benefit.

**Earlier rationale (v1.4.0):** v1.0.0 banned a database outright, importing
`CHEAT_SHEET.md` v2.0.0's finding wholesale. That was over-broad. The cheat-sheet defect was one page
per *fact* — unbounded growth, one row per atom, properties standing in for content. A cycle is
categorically different: bounded (a few a year), substantial (a document in its own right), and
already the unit the maintainer's workspace files under `Docs`-style databases `[SRC-012]`. What
carried over correctly is the inner boundary: the moment a *topic* or *scope* becomes a row, the
mirror stops being a readable page and becomes the tracker this whole standard exists to avoid.
Derived-only properties keep the local file authoritative — a property a human can edit is a second
source of truth, which CYC-10's one-way rule forbids.

The mirror exists so the plan is readable and shareable without opening a terminal —
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
- A hook **MAY** additionally **report** a **time-based** signal that the doc's own dates make
  computable — a topic still `shaping` past its shaping budget (CYC-3), or the dev window nearing its
  end — on the same report-only terms as the queue. Such a nudge **MUST NOT** write anything, and
  **MUST NOT** imply or propose a hill position: CYC-6 names *elapsed time* among the things a hill
  may never be derived from. `[SRC-018]`
- There **MUST NOT** be an approval status, review queue, or workflow inside Notion — the
  conversation is the review. `[SRC-007]`
- `foleon-cycle` **MUST** be invoked **explicitly** (`/foleon-cycle`). Its description **MUST NOT**
  carry phrase triggers intended to auto-load it, and **MUST** state that it is only for explicit
  invocation. `[SRC-009]`

**Rationale:** the maintainer's standing preference is explicit control over automation, and the
cheat-sheet pipeline already proves the shape works: a hook makes capture durable and reasoning-free,
a conversation decides what it means `[SRC-007]`. The explicit-invocation rule is a direct
requirement — a skill that loads itself on a keyword phrase is an automatic action by another route. A
time-based nudge is admitted on the same terms: the shaping circuit breaker `[SRC-004]` is only useful
while there is cycle left to react in, and a signal the tool computes but never volunteers is one the
maintainer learns too late to act on.

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
- A topic still in the **shaping** state at close **MUST** be reported as the strongest such signal
  available: it was bet on before anyone could say what done looked like, and that belongs with
  whoever sets the topics rather than with the developer. `[SRC-014]`
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

### CYC-14 The proposed work list

- `foleon-cycle` **MUST** be able to produce, from the doc alone, a **prioritised work list** split into
  **Jira tickets** (one per Jira-bound task, CYC-7) and **personal tasks**. `[SRC-013]`
- A ticket **MUST** carry: an imperative **summary**, its **epic** (the topic) and **scope**, the
  topic's **outcome** as the why, the topic's **done signal**, and **acceptance criteria**.
- **Acceptance criteria MUST be specific to that ticket, and MUST NOT restate the topic outcome.** A
  criterion copied from the outcome reads like a test and tests nothing, which is worse than an
  admitted blank because it looks finished. Where they cannot yet be written, the list **MUST** emit an
  explicit placeholder rather than filler.
- A ticket proposal **MUST** be grounded in the **actual code** of the repo it targets — read the
  relevant source (via that repo's project-context skill) before proposing tasks or writing criteria.
  A task list derived from a topic title alone is invention. `[SRC-013]`
- A **shaping** topic **MUST NOT** contribute Jira tickets. Its research tasks appear in the personal
  list, and the work list **MUST** say which topics are still shaping — that is the honest statement
  of what this cycle's work currently is. `[SRC-014]`
- Ordering **MUST** put unknowns first: a task under an `uphill` or `top` scope outranks a must-have
  under a `downhill` one, and `~` nice-to-haves come last. Each item also carries a **priority level**
  (`P1`/`P2`/`P3`) so Jira's own field can be set. Where the two disagree for a given cycle, the
  running order is advice and the maintainer's judgement wins. `[SRC-013]`
- The work list is **derived and disposable**: it is regenerated from the doc, never stored as a second
  source of truth, and never mirrored to Notion as a task database (CYC-10).

**Rationale:** the doc's purpose is not record-keeping — it is to produce the next action. Shape Up
stops at scopes and to-dos because a Basecamp team works directly from them; this maintainer's
implementation work has to land in Jira by hand, so the list is the hand-off artifact. The two kinds
exist because a research task in a ticket tracker is a ticket nobody can close: its output is more
tickets. The code-grounding rule exists because a plausible task list is the easiest thing in this
system to generate and the most expensive to act on when wrong.

**Enforcement:** `scripts/cycle.py tickets` produces the list and refuses filler criteria by emitting a
placeholder; code-grounding is a review judgement at proposal time.

### CYC-15 The mirror's visual hierarchy

The general rules — heading meaning, the workspace colour mapping, callout and table discipline,
the parsed-back-renders-plain exclusion — now live in [`NOTION_STYLE.md`](NOTION_STYLE.md) (NST), which
binds every generated page in the workspace. The mirror **MUST** conform to NST; what follows is what is
specific to *this* page and is not derivable from NST alone.

- The mirror **MUST** answer the doc's four questions — what am I building, how much time is it worth,
  where are the unknowns, what gets cut first — **from the top of the page**, without reading a topic
  through. `[SRC-017]`
- A **hill board** — every scope in the cycle with its position and its must-have tally — **MUST** be
  the first thing on the page after the header callout. It is the only block that shows the whole
  cycle at once.
- A hill position **MUST** carry visual weight of its own, and the four values **MUST** map to one
  fixed colour each, stable across cycles. Rendering the hill as undifferentiated inline text makes
  the doc's primary signal its least visible one.
- Within a topic, the **outcome and done signal MUST be the most prominent block**, and the
  constraints — appetite, first cut, no-gos — **MUST** be rendered subordinate to them. What the topic
  *is* outranks what it is not.
- `Open questions:` **MUST** be rendered as a **numbered** list, numbered as `cycle.py questions`
  numbers them, so a question can be referred to by number from the page itself.
- A topic's state (`shaping`/`shaped`) **MUST** be stated once per topic. Repeating it in the heading,
  an icon, and a counter is three renderings of one fact.
- **Anything `reconcile` parses back MUST be rendered plain** — no colour, no attribute list, no
  decoration. This covers the scope heading and every task line. A `{color=}` attribute swallowed into
  a task's text *becomes* that task's text on the next read, because task text is Notion-authoritative
  (CYC-10); the same attribute on a scope heading can orphan every task under it.
- Completion state **MUST** be a count, never a percentage (CYC-6).
- **A bar, chart or gauge MAY be drawn over time, and MUST NOT be drawn over task completion.** An
  appetite is a quantity of weeks the maintainer bet, so drawing it to scale states a fact. A bar
  over must-haves-done is the banned percentage in costume: it implies the remaining work is known,
  which is exactly what an `uphill` scope guarantees it is not.
- The hill **MUST NOT** be charted on a second axis. It is four ordinal stops; any plot of it needs a
  coordinate nobody stated, and inventing one is the inference CYC-6 forbids. A **position track**
  along its own four stops is the faithful rendering — not a fill bar, which reads as "half done".
- The styling **MUST** be produced by the renderer, never hand-authored — whole-page regeneration is
  the only write path (CYC-10), so a hand-applied flourish is erased on the next flow and is
  indistinguishable from a rendering bug while it survives.

**Rationale:** the maintainer reads and works in Notion `[SRC-015]`, which makes the mirror's
readability a functional property rather than a cosmetic one. The first implementation was
*complete* and unreadable: every fact CYC-10 requires was present, and none of it was findable —
the hill rendered as a grey inline code chip three screens down, the fact that a topic was the
cycle's main priority sat mid-sentence inside `First cut`, the state was spelled three times per
topic, and twelve open questions carried the same visual weight as forty checkboxes `[SRC-017]`.
Shape Up's argument for the hill is that it is *seen* — *"you can see at a glance"* `[SRC-002]` —
and a hill nobody looks at is a hill that has stopped working. The parse-back exclusion is the one
hard boundary: v2.0.0 bought a writable surface with a three-way merge, and decorating that surface
would hand the merge corrupted input, which is a data-loss bug wearing a styling change's clothes.

- The reverse of the same rule binds the read: **Notion's own transformations of a parsed-back line
  MUST be undone before the merge sees it.** Notion rewrites content on the way out — it autolinks
  anything domain-shaped and escapes markdown metacharacters — and an untreated transformation is
  indistinguishable from the maintainer retitling the task.

**Enforcement:** `scripts/cycle.py render` is the only render path and is deterministic, and it
**refuses to emit a body that does not parse back** — the round-trip check (render →
`parse_mirror_tasks` → assert every scope and task is byte-identical to the local doc) runs inside
`render` rather than in a test, so a failing body cannot reach Notion at all. The read side is
covered by normalising Notion's transformations in `parse_mirror_tasks` before any comparison.

### CYC-15a Page sections, numbered shapes, and the project frame

- The mirror **MUST** be divided into **page-level sections at `#`**: a `Preview` section, one section
  per project the cycle touches, and `Dev log` — in that order. No content block may sit outside a
  section. `[SRC-019]` (NST-2)
- `Preview` **MUST** hold the header callout, the hill board and the bet, each as an `##` block within
  it. Those blocks answer the doc's four questions, and grouping them under one named section is what
  makes the page's shape readable before its content is.
- A topic heading **MUST** be an `##` inside its project section and **MUST** carry a **shape
  ordinal**: `## <state icon> Shape N: <topic name>`. The separator **MUST** be a colon, not an em
  dash — topic names contain em dashes (`GTM analytics — plumbing`), and `Shape 1 — GTM analytics —
  plumbing` is unparseable by the eye.
- The ordinal **MUST** be assigned in doc order across the **whole cycle**, not restarted per project,
  so `Shape 2` names one topic unambiguously on a multi-project page.
- The ordinal is **derived and positional**. It **MUST NOT** be written into the local doc, a dev-log
  line, a ticket, or anything the skill says in conversation — topics and scopes are referred to by
  **name**, which is stable, while an ordinal renumbers the moment a topic is added, split (CYC-3) or
  reordered.
- The scope heading **MUST** stay at `####`. `reconcile` keys on that level and already-mirrored pages
  carry it, so the page uses `#` / `##` / `####` and leaves `###` unused. This is the skipped-level
  exception NST-2 permits, recorded here as NST-2 requires.
- Every `#` section **MUST** be followed, before its first block, by the orientation NST-11 requires.
  For `Preview` the **header callout is that orientation** — NST-11 accepts a callout in place of the
  line, and a second grey line under it would say the same thing twice. For `Dev log` the line is
  derived: how many entries, over what span.
- A **project** section's orientation line **MUST** be built from **derived** facts only — how many
  topics the project carries this cycle, how many of its scopes are not yet downhill, how much of the
  dev window it books — optionally preceded by a gloss **quoted** from that project's project-context
  skill (`foleon-fio`, `foleon-ripley`; see [`PROJECT_CONTEXT_SKILL.md`](PROJECT_CONTEXT_SKILL.md)).
  A gloss the renderer composed itself **MUST NOT** be emitted: a bare repo name is unhelpful, but an
  invented sentence about the repo is worse, because it reads like a fact.

**Rationale:** the second round of feedback on the mirror was not about colour. Three shapes rendered
as three bare titles under a bare `## fio`, with the whole top half of the page unframed, and the
maintainer's reading of it was *"i want to have a clear 'Shape 1 : ...' for each shape. just make more
visible sections … why is 'fio' just here like that without any context???"* `[SRC-019]`. Sections
give the page a shape; the ordinal turns three peers into `Shape 1` of three; the orientation line
answers the question a bare project name assumes the reader has already answered. The ban on using
the ordinal as an identifier is the price of having it — a number that renumbers must never be
something a log line points at.

**Enforcement:** a layout assertion inside `cycle.py render`, fail-closed on the same terms as the
round-trip check: the body's first line is `# Preview`, every project and `Dev log` is a `#`, every
topic heading matches `^## .* Shape \d+: `, every `#` section is followed by an orientation line, and
no `###` is emitted. The derived-or-quoted requirement is structural — the renderer has no code path
that composes a gloss.

### CYC-15b Task kind is a labelled group, never a line prefix

- `self:` **MUST NOT** appear as a prefix on a mirrored task line. Under a scope, tasks **MUST** be
  rendered in **kind groups**, each opened by a label line stating what the group is to the reader —
  research and decisions that are the maintainer's own and will never be a ticket, versus work that
  becomes a Jira ticket (CYC-7). `[SRC-019]` (NST-6)
- The label line **MUST** be coloured per the NST-3 mapping — research groups orange (unknowns),
  ticket groups blue (execution) — and **MUST NOT** be parseable as a task line or a scope heading.
  It is not read back, which is exactly why it may carry the colour the task line may not.
- When both kinds are present under one scope, the research group **MUST** come first. Unknowns before
  execution is the ordering CYC-14 already requires of the work list.
- Tasks of one kind under one scope **MUST** be contiguous in the local doc, so that rendering them as
  a group preserves task order and the CYC-15 round-trip stays byte-identical. This is a validation
  rule on the local file, checked with the rest of CYC-7's task syntax.
- The local doc **MUST** keep the `self:` prefix as its own syntax (CYC-7 is unchanged). This rule
  binds the rendered page only.
- `parse_mirror_tasks` **MUST** derive a task's kind from the group label above it, and **MUST** still
  accept an inline `self:` prefix on a line — a task the maintainer types into Notion by hand may
  carry one, and it must not be read as part of the task's text. A task added **above** any label
  takes CYC-7's default and is Jira-bound.
- The round-trip check **MUST** compare kind alongside text, done and nice-to-have state. Losing a
  task's kind silently promotes a research task into a Jira ticket.
- The task line itself stays plain. CYC-15's hard exclusion is unchanged and this rule does not bend
  it: the grouping carries the attribute precisely *because* the line cannot.

**Rationale:** `self:` on forty consecutive lines was the maintainer's third complaint and the most
clear-cut — *"'self:' -> this is not aesthetic, instead you could just use color codes, pills or
borders"* `[SRC-019]`. The prefix spends forty lines conveying a grouping the eye could read for free,
and conveys it only to a reader who already knows the code. The mechanism matters as much as the
result: the obvious fix — a colour on the checkbox — is the one thing CYC-15 forbids, because that
attribute becomes the task's text on the next read. A group label is the rendering that gets the
visual weight without touching the writable surface, and the contiguity requirement is what keeps
the render order identical to the file's so the round-trip check still passes byte-for-byte.

**Enforcement:** the CYC-15 round-trip check, extended to kind (already compared in
`roundtrip_problems`); a contiguity check in `cycle.py validate`; and a grep over the rendered body
asserting no task line begins with `self:`.

---

### CYC-16 An annex is generated from a local sidecar, never authored in Notion

- A topic **MAY** carry an `Annex:` line linking a supporting document — a ticket write-up, a list of
  questions for a call — that is too long to live in the topic.
- A **shaped** topic that has produced at least one **Jira-bound task MUST** carry one. Annexes were
  optional while they were hand-authored in Notion, where creating one cost real effort; generated
  from a sidecar the cost is a single `annex sync`, so a shaped topic with tickets and no annex is an
  oversight rather than a decision, and its tickets go to Jira with no write-up behind them.
  `[SRC-025]` A **shaping** topic needs no clause: it has only `self:` tasks (CYC-3, CYC-7), so there
  is nothing to write up, and a shaped topic whose scopes hold only `self:` tasks is exempt for the
  same reason.
- Where one exists, its content **MUST** live in a **local sidecar file** in the cycle directory,
  named `<cycle-id>.annex.<slug>.md`, and that file **MUST** be the source of truth. The Notion page
  is generated output, exactly as the cycle page is (CYC-1, CYC-10). `[SRC-021]`
- The sidecar **MUST** open with `# Annex: <label>` matching the doc's `Annex:` label verbatim, and
  **MUST** name its cycle and topic on the following line. The label is the identity; a renamed label
  orphans its sidecar, which **MUST** be reported rather than silently starting a second one.
- Every **Jira-bound task** under the topic **MUST** be covered by exactly one section of the sidecar,
  and every ticket-bound section **MUST** declare which task it covers by quoting the task text. A
  section covering a task that no longer exists, a task with no section, and two sections claiming one
  task are all **validation errors on the cycle doc**, not warnings. This is the rule's whole point:
  adding a ticket makes the doc non-conforming until the annex accounts for it.
- A ticket-bound section **MUST** carry a proposed **Jira ticket name** on its own line — the summary
  to paste into the tracker. The section heading is written for someone reading the annex; a Jira
  summary is read in a list of forty, out of context, so the two are not interchangeable and the
  heading **MUST NOT** be reused as the name by default. `[SRC-022]`
- Sections that carry no task — shared background, an ordering note — are free-form and unconstrained.
  Background **MUST** sit once at the top, never per ticket (CYC-14).
- `foleon-cycle` **MUST** be able to insert a **stub** section for an uncovered ticket, carrying a
  placeholder Jira name alongside the placeholder write-up, and the stub **MUST** be visibly
  unwritten. A stub **MUST NOT** be publishable: rendering an annex for Notion
  **MUST** fail while any of its sections is still a stub.
- The write-up itself **MUST NOT** be generated. CYC-14 already forbids generated acceptance criteria
  on the grounds that filler which looks finished is worse than an admitted blank, and a generated
  annex is that failure at page scale. What this rule automates is **structure, coverage and links**;
  the words are written by a human or by an agent that has read the code.
- The annex page **MUST** carry a link back to its cycle page, and that link **MUST** be **derived**
  from the recorded page id, never typed. The first hand-authored annex pointed at a page that was not
  its cycle's, and nothing in the system could notice. `[SRC-021]`
- An annex **MUST NOT** be read back from Notion. It is generated output with no writable surface, so
  CYC-10's three-way merge does not apply to it and a Notion-side edit to an annex is lost on the next
  render — which the page **MUST** say, on the page.
- The consent position is CYC-10's: refreshing a generated annex needs no permission; creating its
  page the first time does (CYC-11).

**Enforcement:** `annex_problems` in `cycle.py`, folded into `Doc.check()` so `validate`, `snapshot`
and `render` all carry it; the strict variant additionally refuses stubs and gates
`cycle.py annex render`. `cycle.py annex list` reports coverage, `cycle.py annex sync` creates
sidecars and stubs the uncovered tickets, and `cycle.py mirrored` records an annex snapshot alongside
the cycle's.

---

### CYC-17 A ticket write-up is a fixed set of slots, in a fixed order

- Every **ticket-bound** section of an annex **MUST** be written as the slots below, in this order.
  Sections carrying no `Task:` line — background, an ordering note — are unaffected and stay free-form.

  | Slot | | Holds |
  |---|---|---|
  | `**Expected outcome**` | **MUST** | What the ticket must achieve, observable from outside the change |
  | `**Environment**` | if applicable | Settled facts the implementer must respect but did not choose — an id, a gate, an existing pattern to copy, a sequencing constraint |
  | `**Parameters**` | if applicable | The surface the ticket exposes: the call, its arguments, the pieces that ship — **a bullet list, each item with the reason it is there** |
  | `**Open questions**` | if applicable | What is still undecided inside this ticket, and who settles it |
  | `**Done when**` | **MUST** | The one-sentence finish signal, observable |
  | `**Criteria**` | **MUST** | The testable statements about this change, run together on one line separated by `·` |
  | `**Lives under**` | if applicable | Where the code goes |
  | `**Expected testing**` | **MUST** | Which tests, at which level — or the literal `none` when there are none |

- `**Done when**` and `**Criteria**` are **two slots, not two lines inside one**. They answer different
  questions — *how do I know I am finished* and *what would fail if I were not* — and nesting the
  second inside the first buried the only half a reviewer can check. `[SRC-024]`
- `**Parameters**` **MUST** be a bullet list, one item per line under the header, never a run-on
  behind `·`. Its items are independent constraints; running them together makes the reader do the
  separating that punctuation should have done for them. `[SRC-024]`

- A conditional slot that does not apply **MUST** be **omitted**, never left as an empty header. An
  empty slot is CYC-14's failure in miniature: it looks answered and says nothing.
- `**Expected testing**` is required *including* when the answer is `none`, because unstated testing
  is how "no tests" gets decided silently by whoever is in a hurry rather than by whoever wrote the
  ticket. Where a criterion cannot be tested — vendor behaviour, prose — the slot **MUST** say so and
  name the manual check instead. `[SRC-023]`
- A ticket write-up **MUST NOT** carry a bare checklist of implementation steps. The maintainer
  deleted exactly that from the first ticket pasted into Jira: a list of what to build, with no reason
  attached to any item, which reads as noise to whoever picks the ticket up and duplicates what the
  code will say anyway. `[SRC-023]` Where a step genuinely constrains the implementation it belongs in
  `**Parameters**` **with its reason**; where it does not, it does not belong in the ticket.
- Slot **order** is enforced, not merely recommended: the value of a fixed shape is that a reader
  finds the same thing in the same place across forty tickets, and a section carrying every slot in
  its own order defeats exactly that.
- A slot **MUST NOT** be padded to look justified. An `Expected outcome` that argues for itself, or
  states something trivially true of the code as it stands, is filler wearing a required slot's name —
  CYC-14's failure in the one place the rule cannot catch it. Write the outcome and stop. `[SRC-024]`
- CYC-16's exclusion still governs the words. This rule fixes the **shape**; the content of each slot
  is written by a human or by an agent that has read the code, never generated (CYC-14).

**Enforcement:** `slot_problems` in `cycle.py`, called from `annex_problems` for every ticket-bound
section, so `validate`, `snapshot` and `annex render` all carry it. It runs on written sections only —
an unwritten stub is already caught as a stub, and reporting both would bury the one that matters.
`cycle.py annex sync` emits the required slots as its stub, so a new ticket starts in the right shape.

---

## Documented overrides

| # | Source rule | Override | Justification |
|---|---|---|---|
| 1 | Shape Up: a team of two or three **discovers** its own scopes `[SRC-002]` | An agent **proposes** scopes; only maintainer-accepted names are written (CYC-5) | The team is one developer plus an assistant. A proposal is a draft, not an authority — and the naming requirement (maintainer's own words) preserves what the original rule protects. |
| 2 | Shape Up: shaping produces no task list; tasks are discovered while building `[SRC-002]` | Intake produces a first task list per accepted scope (CYC-7) | The maintainer's stated need is to plan the development up front `[SRC-009]`. Mitigated: tasks require accepted scopes first, scopes may hold no tasks (CYC-5), and tasks are never a status measure (CYC-6). |
| 3 | Shape Up: six-week cycles plus two-week cool-down `[SRC-001]` | **8 weeks: a 6-week dev window + 2 weeks cooldown**, cooldown untracked (CYC-2, v1.5.0) | Not an override at all, as it turns out — the maintainer's team runs almost exactly Shape Up's shape. v1.0.0 left length unspecified for fear of hard-coding the wrong number; once the real shape was stated `[SRC-013]`, encoding it bought appetite validation against the window and a "week 4 of 6" status reading. |
| 4 | Scrum: the Daily Scrum is a synchronous 15-minute team event `[SRC-006]` | An asynchronous dev-log line, written when something changes (CYC-8) | A solo developer has no team to synchronise with; the *purpose* the Scrum Guide states — inspect progress, adapt the plan — is preserved, only the ceremony is dropped. |
| 6 | Shape Up: shaping happens **before** the bet, by a senior pair, during cool-down `[SRC-002]` `[SRC-005]` | Shaping is **inside** the cycle, as a first-class topic state with its own research tasks (CYC-3, v1.6.0) | The maintainer's team hands over a title and an estimate, not a pitch. Pretending otherwise deadlocked intake `[SRC-014]`. The protection Shape Up gets from up-front shaping is preserved differently: a shaping topic cannot produce implementation tickets. |
| 5 | Shape Up: the hill chart is a continuous position on a curve `[SRC-003]` | Four discrete values: `uphill`, `top`, `downhill`, `done` (CYC-2) | A markdown file needs a token a checker can validate. The four values keep the only distinction the metaphor is *for* — unknowns versus execution — and the `top` value preserves the pivot point where estimation first becomes meaningful `[SRC-003]`. |

---

## Conformance checklist

A cycle doc is conforming when **all** are true:

- [ ] One doc for the whole cycle, local file authoritative, stored in the maintainer's cycle directory — outside every code repo, `skills-tinky` included (CYC-1)
- [ ] If the cycle directory keeps git history: no remote, never pushed, `.state/` unversioned, and a failed commit never costs the write (CYC-1)
- [ ] Header, topics, dev log — in order, no empty sections, hill values from the closed set of four (CYC-2)
- [ ] Every topic declares `— shaping` or `— shaped` (CYC-3)
- [ ] A shaping topic has an appetite and at least one open question, all-uphill scopes, and only `self:` tasks (CYC-3, CYC-7)
- [ ] A shaped topic has outcome, appetite, first cut, no-gos, done signal, repo tag; unanswered items recorded as open questions, never inferred (CYC-3)
- [ ] No topic has been flipped to `shaped` by inference rather than by the answers arriving (CYC-3)
- [ ] Remaining questions classified blocking / non-blocking; the hold-split-shape move was proposed with reasoning and agreed (CYC-3)
- [ ] Any split has an independently shippable shaped half with no open questions, and a divided — not duplicated — appetite (CYC-3)
- [ ] Every `Open questions:` entry asks something; caveats and inferences live on `Assumptions:` (CYC-3)
- [ ] Appetite marked `(fixed)`, never revised upward without a logged re-bet; first cut named at intake (CYC-4)
- [ ] Scopes are independently finishable slices, named in the maintainer's words, integrated unless a stated iceberg (CYC-5)
- [ ] Every hill position traceable to a maintainer statement; no percentages anywhere (CYC-6)
- [ ] Every task under exactly one scope; nice-to-haves prefixed `~`; scope `done` ignores outstanding `~` (CYC-7)
- [ ] Personal tasks marked `self:`; unmarked tasks are Jira-bound (CYC-7)
- [ ] Header dates are the 6-week dev window with the cooldown end recorded; no cooldown work in the doc (CYC-2)
- [ ] Every appetite fits inside the 6-week dev window (CYC-4)
- [ ] The work list orders unknowns first, carries a P-level, and its acceptance criteria are ticket-specific and code-grounded — never a restatement of the outcome (CYC-14)
- [ ] The mirror opens with a hill board covering every scope; the hill has a fixed colour per value (CYC-15)
- [ ] Within a topic the outcome and done signal are the most prominent block; constraints render subordinate (CYC-15)
- [ ] Open questions are numbered as `cycle.py questions` numbers them; topic state is stated once (CYC-15)
- [ ] Scope headings and task lines render plain — nothing `reconcile` parses back carries a rendering attribute (CYC-15)
- [ ] The mirror conforms to [`NOTION_STYLE.md`](NOTION_STYLE.md) (NST-1…NST-11) (CYC-15)
- [ ] Every shaped topic with at least one Jira-bound task carries an `Annex:` line (CYC-16)
- [ ] Every `Annex:` link has a local sidecar that is its source of truth; the Notion annex page is generated (CYC-16)
- [ ] Every Jira-bound task is covered by exactly one annex section, and every annex section covers a task that still exists (CYC-16)
- [ ] No annex is published while any of its sections is still a stub; no annex write-up was generated (CYC-16, CYC-14)
- [ ] Every annex page links back to its cycle page by a derived id, and says it is generated (CYC-16)
- [ ] Every ticket-bound annex section carries the required slots — expected outcome, done when, criteria, expected testing — in the standard's order, with conditional slots omitted rather than left empty and `Parameters` written as a bullet list (CYC-17)
- [ ] No ticket write-up carries a bare implementation checklist; a constraining step sits in `Parameters` with its reason (CYC-17)
- [ ] Page-level sections at `#` — `Preview`, one per project, `Dev log` — with no block outside a section (CYC-15a)
- [ ] Every topic heading is `## <icon> Shape N: <name>`, numbered across the whole cycle, colon-separated, and the ordinal is never used as an identifier (CYC-15a)
- [ ] Scope headings stay `####`; `###` is unused (the recorded NST-2 exception) (CYC-15a)
- [ ] Every `#` section opens with a one-line grey orientation built from derived facts or a quoted project-context gloss — never an invented one (CYC-15a)
- [ ] No mirrored task line begins with `self:`; kind is a coloured group label, research group first (CYC-15b)
- [ ] Tasks of one kind are contiguous under a scope in the local doc; the round-trip compares kind (CYC-15b)
- [ ] The parser derives kind from the group label and still accepts a hand-typed inline `self:` (CYC-15b)
- [ ] Every dev-log line passes a state-change / decision / surprise gate; nothing restates git; append-only (CYC-8)
- [ ] Topics repo-tagged; cross-repo topics written once; mirror nested by project (CYC-9)
- [ ] Mirror is one page per cycle, regenerated whole from local, refreshed at the end of every flow that changed the doc (CYC-10)
- [ ] Tasks render as Notion to-do items; only checked-state, task text and added task lines are read back (CYC-10)
- [ ] Notion-side edits to fields, appetite, state, hill, scopes or the dev log are reported and ignored (CYC-10)
- [ ] Reconciliation is a three-way merge against a post-write snapshot, deletes nothing, and re-validates before committing (CYC-10)
- [ ] The cycle may be a row in the `Cycles` database; no topic, scope or task is a row or a property (CYC-10)
- [ ] Every cycle-row property is derived from the local file and regenerated on each mirror (CYC-10)
- [ ] Nothing written to Notion without an explicit yes in that conversation; hooks queue or report, never write; skill is explicit-invocation only (CYC-11)
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
| Round-trip check inside `render` — render → parse → byte-identical, fail-closed | CYC-15, CYC-15b | Yes |
| Layout assertion inside `render` — section levels, `Shape N:` headings, orientation lines, no `###` | CYC-15a | Yes |
| Task-kind contiguity check in `validate`; `self:`-prefix grep over the rendered body | CYC-15b | Yes |
| No renderer code path composes an unsourced project gloss | CYC-15a | Structural |

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
- `[SRC-016]` Internal — the maintainer's requirement after a partial scoping call, 2026-08-19: *"i would like to re-evaluate the current state and from there take a decision (if too many left over open questions, push on waiting for more answers, if a few answers help working on a first part of the shape, then the skill should be able to ask me if agree)"*, and on the mis-filed entry: *"3 is a fair point, it's not a question. make sure this doesnt happen anymore."* Also the observation that this is the general case, not a special one: *"shapeup IS about figuring out solutions"* — under Scrum a PO and scrum master pre-prepared the tasks; here that work is the developer's.
- `[SRC-019]` Internal — the maintainer's second reading of the rendered Cycle-11 mirror, 2026-08-20, verbatim: *"i want to have a clear 'Shape 1 : ...' for each shape. just make more visible sections (the whole first part before 'fio' could have a 'preview' category). why is 'fio' just here like that without any context??? … same for the questions : 'self:' -> this is not aesthetic, instead you could just use color codes, pills or borders i dont know just something better"*, and on the page as a whole: *"this is a bit pathetic. i've seen so many good looking notion pages in my life!! add a real rule-set for that maybe?"* The "rule-set" request is what produced [`NOTION_STYLE.md`](NOTION_STYLE.md); the three specific complaints are CYC-15a and CYC-15b.
- `[SRC-018]` Internal — the maintainer's decision, 2026-08-20, on whether loops or hooks suit this system. Loops were rejected on three grounds: every flow ends at a consent gate a loop cannot satisfy, `/loop` only runs while a session is open and there is nothing to poll during one, and the cycle directory is local-only with no remote (CYC-1) so a scheduled cloud agent cannot read it. The gap found instead was time: `cycle.py`'s `shaping_overrun` and `week_of` are computed only on an explicit `status` call, so a topic can pass its escalate threshold unannounced. Their constraint on the fix, verbatim: *"don't overcomplicate it tho."*
- `[SRC-017]` Internal — the maintainer's judgement on the first rendered mirror, 2026-08-20: *"content-wise im pretty happy with it, but the doc is like so boring to look at"* — a complete page that is not read is a reporting surface that has failed at the only thing it is for.
- `[SRC-015]` Internal — the maintainer's requirement, 2026-08-19: *"for notion, i want to both be able to read and edit (the local should then change too based on that automatically): if i want to say i finished a task i dont want to go through claude to tell it that i did it. i want to update and then claude would be aware the next time i use the cycles tool for something"*, and on the hill: *"we'll see for hills later, for now no editing the hills within notion."*
- `[SRC-014]` Internal — the deadlock, observed live 2026-08-19. Asked for the outcome of an unshaped topic, the maintainer answered: *"I don't understand the question... I don't have a wanted outcome yet! this afternoon i'll be in a call to discuss this with PO, Data Engineer, etc... For now unknown like mentionned everywhere"*, and on the first cut: *"I feel like we can discuss bout this later on."* Their requirement: *"the cycle tasks could start by being 'make research and ask questions blablabla...' and then once i have more info i give everything to the skill and it would mark those tasks as done and create new ones"* — *"I want to have a system that helps me get through those steps and to adapt to what i can/cannot/know/dont know."*
- `[SRC-013]` Internal — the maintainer's clarifications, 2026-08-19: *"a cycle is always 8 weeks, but the first 6 weeks are the dev session. the 2 last weeks are just 'cooldown' in which we do bug-fixing/research etc"*; that the point of the system is *"a list of priorised tickets generated for me (or at least a proposition) that i could then add into Jira (by-hand for now)"*; that not everything is a ticket — *"if i add a brand new feature i need to conceptualize... this won't be a ticket in JIRA, this will be a task for me -> the task could be 'research on how to implement, expected outcome of the task : make tickets to implement after research'"*; and that proposals should be code-grounded — *"it could be worth it having a technical skill read through the code of the mentionned repos"*.
- `[SRC-025]` Internal — the maintainer, 2026-08-24, on being told CYC-17's slots only reach tickets that have an annex: *"why would a topic have no Annex? this is a genuine question."* The two honest answers were a shaping topic, which has no tickets, and an oversight. They asked for the oversight to be closed.
- `[SRC-024]` Internal — the maintainer on the first slotted annex, 2026-08-24: *"I want to have *Done when* -- and *Criteria* -- separated"* — the nested pair read as one block and the criteria line was lost inside it — and *"parameters would be better if list also i think"*. They also flagged padding in an `Expected outcome` that justified itself rather than stating the outcome, which is where the no-filler line in this rule comes from.
- `[SRC-023]` Internal — the maintainer's report, 2026-08-24, after pasting the first shape-1 ticket into Jira: they kept the outcome, the done signal, the criteria and the location, and deleted the three-bullet "what to build" list — *"Your 3 points didn't make a lot of sense. I would like to have a reason for having those pointers. We need a stable and validated structure that we need to follow everytime."* The slot list, `Expected testing` included, is theirs.
- `[SRC-022]` Internal — the maintainer's request, 2026-08-24, on the shape-1 annex: *"i would like to have a proposition for a task name for Jira for all options"*, sketched as a `### Jira Ticket name :` line under each ticket heading. The annex's own headings are written for a reader of the page and read poorly as tracker summaries, which is the gap the separate line closes.
- `[SRC-021]` Internal — the maintainer's requirement, 2026-08-24, on the shape-1 ticket annex, verbatim: *"this should be deeply-linked! automatically updated once we add a new ticket! can you enforce that rule please? … i mean enforce this as a global thing for the whole cycle system! not just for that cycle."* Raised on an annex whose page still read *"Three tickets"* over a topic that had four, and whose own "Cycle 11" backlink pointed at a page that was not the cycle's. Both defects follow from the same v2.x position — that where an annex lives *"is not this skill's call to invent"* — which left the annex as the one hand-authored surface in a system whose every other page is generated.
- `[SRC-020]` Internal — the maintainer's request, 2026-08-21: *"can we make the answer to points being written down next to them when answered? it would be easier than just having them mixed up in the logs."* Raised on a shape-1 research task whose answer already sat four rows up the dev-log table, unfindable from the task that asked for it.
- `[SRC-012]` Internal — the maintainer's decision, 2026-08-19: *"i would like the cycles to be in the database 'Cycles' i just created (same location as Docs, in Foleon)"*, and on properties: *"i don't mind properties!! if they make sense obvs."* Their workspace files documents as rows in a `Docs` database (the cheat-sheet hub is one), so a `Cycles` database is the native shape there.
- `[SRC-011]` Internal — the maintainer's authorisation, 2026-08-19, verbatim: *"SHAPEUP-CYCLES may auto-commit"*, given after asking for a system that needs no repo handling: *"i am just scared of the handling of the repo. how often do we push? can you make a system that is 100% independant?"* The answer that satisfied it — no remote, so no pushing is possible, and commits made by the tool rather than by hand — is what CYC-1 now requires.
- `[SRC-010]` Internal — the maintainer's correction, 2026-08-19: *"we are completely going out of scope on skills-tinky repo! it's supposed to be a repo for skills and things that revolve around that, not to keep track of my cycles. this repo is used by me for both pro and perso."* The v1.0.0 placement (the skill's own `state/` directory) was wrong on both counts — off-topic for that repo, and pushed to GitHub.
- `[SRC-009]` Internal — the maintainer's stated requirements, session of 2026-08-17/18: local-first with a Notion mirror; scopes and tasks with a hill chart; hook proposes and the maintainer approves; Foleon-only across `ripley`, `fio` and future repos; `/foleon-cycle` explicit invocation with no phrase triggers.

## Change log

| Version | Date | Change |
|---|---|---|
| **5.1.0** | 2026-08-24 | **A shaped topic with tickets owes an annex.** CYC-17's slots only reach ticket write-ups, and write-ups only exist inside an annex, which CYC-16 had left optional — so the whole ticket standard could be skipped by not linking one `[SRC-025]`. CYC-16 now **requires** an annex on any shaped topic carrying at least one Jira-bound task. The optionality dated from v2.x, when an annex was hand-authored in Notion and creating one cost real effort; generated from a sidecar it costs one `annex sync`. Shaping topics need no exemption clause — they hold only `self:` tasks, so there is nothing to write up. MINOR: additive, and the only shaped topic in the only live cycle already carries its annex. |
| **5.0.0** | 2026-08-24 | **The slots, corrected by first use.** 4.0.0's shape survived one reading. `Acceptance criteria` nested `Done when` and `Criteria` as two lines under one header, and the maintainer's report was that it *"looks weird"* — the criteria line disappeared into the block above it, which is the half a reviewer actually checks `[SRC-024]`. They are now two sibling slots. `Parameters` is now a **bullet list**, enforced: its items are independent constraints and a run-on behind `·` makes the reader separate them by hand. Added a ban on **padding a slot to look justified** — the first slotted ticket's outcome argued for itself and asserted something trivially true of the code as it stood, which is CYC-14's filler failure in the one slot the coverage rules cannot see. MAJOR: every 4.0.0 annex is non-conforming; migration is splitting one slot and bulleting another. |
| **4.0.0** | 2026-08-24 | **A ticket write-up gets a fixed shape.** v3.1.0 fixed the annex's structure — one section per ticket, a Jira name on each — and left the section body as free prose, so every ticket invented its own arrangement. The maintainer pasted the first one into Jira and cut most of it: what survived was outcome, done signal, criteria and location; what went was a three-bullet list of what to build with no reason attached to any item `[SRC-023]`. New **CYC-17** replaces free prose with seven named slots in a fixed order — three required (`Expected outcome`, `Acceptance criteria` as done-when plus criteria, `Expected testing`), four conditional (`Environment`, `Parameters`, `Open questions`, `Lives under`) — bans the bare implementation checklist, and requires a reason on anything kept in `Parameters`. `Expected testing` is required even when the answer is `none`, because the alternative is that answer being made silently. Order is enforced for the reason the shape exists: the same thing in the same place across forty tickets. MAJOR: every annex conforming at 3.1.0 is now non-conforming; migration is rewriting each ticket section into the slots, which cannot be automated for the same reason the write-up cannot (CYC-14). |
| **3.1.0** | 2026-08-24 | **A ticket section proposes its Jira summary.** CYC-16 shipped the annex as the place a ticket is written up, and the maintainer went to paste one into Jira and found nothing to paste: the section heading is written for someone reading the annex top to bottom, where a Jira summary is read in a list of forty with no surrounding page `[SRC-022]`. A ticket-bound section now carries a proposed Jira ticket name on its own line, `annex sync` stubs it alongside the write-up, and `annex render` refuses to publish while either placeholder stands — the name is a proposal for the maintainer to accept or rewrite, exactly as scope names are (CYC-5). MINOR: additive, and the only existing annex already carries the line. |
| **3.0.0** | 2026-08-24 | **Annexes become generated output.** v1.x through v2.5.0 linked an annex and deliberately said nothing about it — *"where the annex itself lives is not this skill's call to invent"* — which made it the only page in the system authored by hand in Notion. The consequence was visible on the first one: a ticket added to the cycle doc left the annex reading "Three tickets" over four, and the annex's own backlink pointed at a page that was not its cycle's, with nothing able to notice either `[SRC-021]`. New **CYC-16** moves an annex's content into a **local sidecar** beside the cycle doc, makes that file authoritative, and requires **exactly one section per Jira-bound task** — a missing, orphaned or duplicated section is a validation error on the cycle doc, so adding a ticket makes the doc non-conforming until the annex accounts for it. The backlink is derived from the recorded page id rather than typed. The load-bearing exclusion is what is *not* automated: the write-up itself **MUST NOT** be generated. CYC-14 already forbids generated acceptance criteria because filler that looks finished beats an admitted blank at being wrong, and a generated annex is that failure at page scale — so the tooling inserts a **stub** that cannot be published, and a human or a code-reading agent writes the words. Annexes are not read back from Notion: they have no writable surface, CYC-10's merge does not apply, and the page says so. MAJOR: a doc that conformed at 2.5.0 with an `Annex:` line and no sidecar no longer conforms; migration is one `cycle.py annex sync` plus moving the existing page's prose into the sidecar. |
| **2.5.0** | 2026-08-21 | **A closed research task records its own answer.** CYC-7 gave personal tasks a purpose — *finding out* — and no place to put what was found, so the answer went to the dev log and only there. The dev log is chronological, which is right for a narrative and wrong for a lookup: the maintainer hit this on a shape-1 task whose answer sat four rows up the same table, invisible from the question that produced it `[SRC-020]`. CYC-7 now requires the answer inline on the task, `→ answer: <…>`, when a personal task completes. The dev-log line is unaffected where CYC-8 admits one — the two are not redundant, they are indexed differently. Mechanically free: task text is already free-form and Notion-authoritative under CYC-10 v2.0.0, so the appended clause round-trips through `reconcile` with no renderer or parser change. MINOR: additive, and no existing doc stops conforming — untouched historic tasks simply carry no answer clause. |
| **2.4.0** | 2026-08-20 | **The page gets a shape, and `self:` stops being text.** v2.2.0's CYC-15 fixed *what is loudest* and left the page's structure alone, which the second reading found immediately: the whole top half was unframed, three topics rendered as three bare titles under a bare `## fio`, and `self:` repeated as a prefix on forty consecutive lines `[SRC-019]`. Two additions. **CYC-15a** makes the page's sections normative — `#` for `Preview` / each project / `Dev log`, topics as `## <icon> Shape N: <name>` numbered across the whole cycle (colon-separated, because topic names already contain em dashes), and a one-line grey orientation under every section that must be **derived or quoted**, never composed, so a project section explains itself without the renderer inventing a sentence about the repo. The ordinal is derived-only and explicitly banned as an identifier — it renumbers on every split. **CYC-15b** bans `self:` as a rendered prefix and replaces it with a coloured **group label** per scope, research group first. The mechanism is the interesting part: the obvious fix (a colour on the checkbox) is exactly what CYC-15's hard exclusion forbids, since that attribute becomes the task's text on the next read — so the label line, which nothing parses, carries the weight the task line cannot, and a new **contiguity** requirement on the local file keeps render order identical to file order so the round-trip still passes byte-for-byte. Also: the general page-styling rules were **extracted** into [`NOTION_STYLE.md`](NOTION_STYLE.md) (NST 1.0.0) so the cheat sheet and `notion-knowledge-capture` inherit them instead of re-deriving them; CYC-15 now layers only the cycle-specific rules on top. MINOR: additive, and the extraction moves no rule's meaning. |
| **2.3.0** | 2026-08-20 | **The hook remit covers the calendar, not just unlogged work.** v2.2.0's CYC-11 authorised a hook to detect *unlogged work* and nothing else, which left the one signal no edit can ever produce unowned: `cycle.py` already computes the shaping circuit breaker (`shaping_overrun`, added in v1.6.0) and the dev-window week, but only when `status` is run — so a topic could pass its escalate threshold in silence and the system's own warning arrive too late to act on `[SRC-018]`. CYC-11 now lets a hook **report** a time-based signal on the same report-only terms as the queue. The load-bearing clause is the exclusion: such a nudge **MUST NOT** imply or propose a hill position, because CYC-6 names *elapsed time* among the things a hill may never be derived from — a "14 days shaping, probably still uphill" nudge would launder precisely the inference CYC-6 exists to prevent. Loops were considered and rejected in the same pass, for reasons recorded in `[SRC-018]`. MINOR: additive, and no v2.2.0 implementation stops conforming. |
| **2.2.0** | 2026-08-20 | **The mirror gets a visual contract.** v2.0.0 settled *what* the mirror carries and said nothing about how it reads, and the first real page showed why that is not a cosmetic gap: every required fact was present and none of it was findable `[SRC-017]`. New CYC-15 makes the reading order normative — a **hill board** covering every scope first on the page, one fixed colour per hill value, the outcome as the loudest block in a topic with the constraints subordinate to it, open questions **numbered** to match `cycle.py questions`, and topic state stated once instead of three times. The load-bearing clause is the exclusion: **anything `reconcile` parses back renders plain**. A `{color=}` attribute on a task line is swallowed into the task text, and task text is Notion-authoritative under v2.0.0 — so decorating the writable surface would feed the three-way merge corrupted input, which is a data-loss bug dressed as a styling change. Enforced by a round-trip check (render → `parse_mirror_tasks` → assert byte-identical to local) that must pass before any mirror write. MINOR: additive, and no v2.1.0 doc stops conforming. |
| **2.1.0** | 2026-08-19 | **Shaping becomes a decision, and a topic can be split.** v1.6.0 gave topics two states but only one transition — apply the answers and flip — which broke on the first real partial call: some questions answered, some not, and no way to express *"the plumbing is knowable, the event list isn't"* because state is per-topic `[SRC-016]`. CYC-3 now requires answers to be **re-evaluated**: remaining questions are classified **blocking** (can the outcome or done signal be written without it?) or non-blocking, and one of **hold / split / shape** is proposed with reasoning and agreed before anything changes. A **split** produces one shaped half — independently shippable, no open questions — and one shaping half carrying the questions, with the appetite divided rather than duplicated. Holding on a non-blocking question is forbidden, as is downgrading a blocking one to get moving. `status` now reports total appetite booked against the dev window. Also: an `Open questions:` entry must actually ask something, with caveats and inferences moved to a new `Assumptions:` field (rendered as a callout) — the first version of that check demanded a trailing `?` and rejected six good questions carrying a "why this matters" clause, so it now accepts a question mark anywhere or a clause opening with an interrogative. |
| **2.0.0** | 2026-08-19 | **The mirror becomes writable in one narrow place.** v1.x was strictly one-way on the sound principle that two writable surfaces drift — but the maintainer's actual need is to tick a task in Notion without going through the skill `[SRC-015]`, and a tool that requires permission to tick a checkbox loses to one that doesn't. CYC-10 now renders tasks as Notion to-do items and reads back exactly three things: checked state, task text, and task lines added under an existing scope. Everything else — fields, appetite, topic state, **hill**, scopes, dev log — stays local-authoritative and a Notion edit to it is reported and ignored. Safety comes from mechanism, not trust: a **three-way merge** against a snapshot recorded only after a successful write (without it, unticked and never-ticked are indistinguishable), **no automatic deletion** (a task missing from Notion is reported and left), a re-validate before any commit, and a stop-with-nothing-written on collision. Noted in passing: a checked-state collision is unreachable by construction — two sides moving a boolean off the snapshot move it to the same value — so renames are the only real collisions. Also: the mirror refreshes at the end of every flow, and CYC-11's consent gate no longer applies to refreshing a generated page (only to creating a cycle's row the first time). MAJOR because one-way derivation was a load-bearing property of v1.x. |
| **1.6.0** | 2026-08-19 | **Two topic states, because shaping happens inside this cycle.** v1.0.0's single six-field gate assumed Shape Up's world, where a team receives work already shaped by a senior pair in cool-down. This maintainer receives a title and an estimate, so the gate deadlocked: the research tasks that would answer the intake questions could not exist until the questions were answered, and the only escape was a guessed `Outcome: TBD` — validation-passing and worthless `[SRC-014]`. CYC-3 now defines **`shaping`** (repo tag + appetite, optionally `(provisional)`, + at least one open question; scopes all `uphill`; only `self:` research tasks) and **`shaped`** (all six fields), with the state declared in the topic heading and never defaulted. The transition is a deliberate act on the answers arriving, never an inference. CYC-7 forbids implementation tasks under a shaping topic, CYC-14 excludes it from Jira tickets while requiring the work list to name it as still shaping, and CYC-13 reports a never-shaped topic as the strongest shaping signal the system produces — one that belongs with whoever sets the topics. New override #6 records the divergence from Shape Up honestly. Also: a shaping topic **should** be escalated rather than researched further past roughly a quarter of its appetite (the circuit breaker, applied to shaping), which `status` now warns about. |
| **1.5.0** | 2026-08-19 | **The real cycle shape, and the output the system exists for.** Three things the maintainer clarified `[SRC-013]`. (1) A cycle is **8 weeks — 6 dev + 2 cooldown**; the header's dates are now the dev window with the cooldown end recorded after it, appetites are validated against the 6 weeks rather than the 8, and cooldown work is deliberately **not** tracked (it has no appetite, no no-gos, nothing to put on a hill). Override #3 is rewritten: it was never an override, the team runs almost exactly Shape Up's shape. (2) Tasks come in **two kinds** (CYC-7): Jira-bound by default, or `self:` for research and conceptualising, whose outcome is usually *producing the tickets* — and such a task adding new tasks when it closes is expected, not scope creep. (3) New rule **CYC-14**: the doc must produce a **prioritised work list** — tickets for Jira plus personal tasks — ordered unknowns-first with a P-level, where acceptance criteria must be ticket-specific and **grounded in the actual code**, never a restatement of the topic outcome, with an explicit placeholder rather than filler when they cannot yet be written. |
| **1.4.0** | 2026-08-19 | **The cycle mirror may be a row in a `Cycles` database.** v1.0.0's blanket "MUST NOT be a database" imported `CHEAT_SHEET.md` v2.0.0's finding too broadly: that defect was one page per *fact*, unbounded and property-driven, whereas a cycle is bounded and substantial, and the maintainer's workspace already files documents as database rows `[SRC-012]`. CYC-10 now permits the per-cycle page to be a row in a dedicated `Cycles` database, and states the inner boundary explicitly — topics, scopes and tasks stay page content, never rows, never properties, because that is the line whose crossing turns the mirror into a tracker. Cycle rows **may** carry properties provided each is **derived** from the local file and regenerated on every mirror (reference set: `Name`, `Status`, `Dates`, `Repos`); a property that cannot be regenerated is forbidden, since a hand-editable property is a second source of truth. |
| **1.3.0** | 2026-08-19 | **Commits in the cycle history carry a `Co-Authored-By: Claude` trailer**, at the maintainer's request and scoped to this history alone — not a global git convention. The cycle doc's plans and log lines are written collaboratively, so the history says so. |
| **1.2.0** | 2026-08-19 | **Local-only git history in the cycle directory, authorised as a named carve-out.** The maintainer wanted history without repo maintenance — *"how often do we push? can you make a system that is 100% independant?"* — and authorised auto-commit for this directory alone `[SRC-011]`. CYC-1 gains four bullets: the directory MAY keep git history; `foleon-cycle` MAY commit at open / approved log line / close / explicit `snapshot`; the history MUST NOT have a remote and MUST NOT be pushed (the skill refuses to commit if one exists), and `.state/` MUST NOT be versioned; a failed commit MUST NOT fail the write. Recorded here rather than left as folklore precisely because it is an exception to a standing rule — the exception is auditable, scoped to one directory, and cannot become a habit that spreads. |
| **1.1.0** | 2026-08-19 | **Storage moved out of `skills-tinky`.** v1.0.0's CYC-1 put cycle docs in the skill's own `state/` directory, reasoning from PCS-9a's silo principle. The maintainer corrected it before any doc existed: `skills-tinky` is a repo for skills, used for both professional and personal work, and pushed to GitHub — so cycle docs there are both out of scope and published `[SRC-010]`. CYC-1 now requires a dedicated maintainer-owned cycle directory outside every code repository (default `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES`, overridable via `FOLEON_CYCLE_HOME`), and puts the unlogged-work queue in that same directory under `.state/` so the system has one location rather than two. Enforcement changed from "not inside a known repo checkout" to "resolved from the configured cycle directory, never the cwd". No other rule is affected: local-first, one-way mirroring and the consent gate are unchanged. |
| **1.0.0** | 2026-08-18 | Initial standard. Thirteen rules covering: one local-authoritative doc per cycle stored outside every checkout (CYC-1), a fixed skeleton with four discrete hill values (CYC-2), a six-field intake gate with unanswered items recorded rather than inferred (CYC-3), appetite as a fixed budget with the first cut named at intake (CYC-4), maintainer-named integrated scopes with the iceberg allowance (CYC-5), human-only hill positions and no percentages (CYC-6), tasks under scopes with Shape Up's `~` nice-to-have marker as the scope-hammering action (CYC-7), a three-gate dev log that never restates git (CYC-8), multi-repo nesting reusing CHS-9a/9b (CYC-9), a one-way whole-page Notion mirror that is never a database (CYC-10), a conversational consent gate with hooks that queue but never write and explicit-only invocation (CYC-11), durable facts routed out to the project-context logs (CYC-12), and a close routine that flags residual uphill work as a shaping signal and delegates the retro to `sprint-review` (CYC-13). Five documented overrides record where solo work and the maintainer's hybrid diverge from Shape Up and Scrum as written. |
