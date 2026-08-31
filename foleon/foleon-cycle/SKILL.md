---
name: foleon-cycle
description: >-
  Runs the maintainer's ShapeUp/Scrum cycle end to end: opens one doc per cycle,
  interviews each topic into shape, factors it into scopes tracked on a four-value
  hill, proposes a prioritised work list (Jira tickets + personal tasks), logs
  progress, mirrors to the `Cycles` Notion database, and closes by handing the
  retro to `sprint-review`. Topics start `shaping` — appetite plus open questions,
  no spec required — and flip to `shaped` when the answers arrive. Local markdown
  in `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES/` is the source of truth; in Notion
  you may tick, rename and add tasks, and the next run reconciles that back.
  Covers every Foleon repo a cycle touches — `ripley`, `fio`, and any added later.
  Enforces `docs/stds/CYCLE_DOC.md` (CYC-1…CYC-19).
  **Explicit invocation only — `/foleon-cycle`.** Per CYC-11 this skill
  deliberately carries no trigger phrases and must not auto-load: do not invoke
  it because a message mentions a cycle, a topic, an estimate, planning, or
  progress. Wait for `/foleon-cycle`. When a hook reports unlogged work at
  session start or as a turn ends, that is a cue to *offer* this skill — not to
  run it. Do NOT use it to record durable project facts (that is `foleon-ripley`
  / `foleon-fio`'s `knowledge.md`), to write the Notion cheat sheet (that is
  `foleon-cheatsheet`), or to run the cycle retrospective (`sprint-review`).
user-invokable: true
---

# foleon-cycle

The maintainer's team hands over a cycle as **topics with an estimated time each**. Turning that into
a development plan — and knowing on any given Wednesday where the work actually stands — is the
developer's job. This skill is that job, done in one file per cycle.

Governed by [`docs/stds/CYCLE_DOC.md`](../../docs/stds/CYCLE_DOC.md) (CYC-1…CYC-19). The standard wins
any disagreement with this file. The Notion mirror also conforms to
[`docs/stds/NOTION_STYLE.md`](../../docs/stds/NOTION_STYLE.md) (NST-1…NST-11), which carries the
workspace-wide page rules — section framing, colour meanings, and the ban on styling anything the
skill parses back.

A cycle is **8 weeks: 6 of dev, then 2 of cooldown**. The doc covers the **dev window only** —
cooldown is bug-fixing and research, which has no appetite and nothing to put on a hill, so it stays
off-book (CYC-2). Appetites are validated against the 6 weeks, not the 8.

**The doc answers four questions at a glance:** what am I building, how much time is it worth, where
are the unknowns, and what gets cut first. Task state is the *least* valuable thing in it — Shape Up
is explicit that counting to-dos cannot tell you a project's status, because there is no way to know
whether the number of outstanding tasks will go down or up.

## Target

| Thing | Value |
|---|---|
| Cycle docs | `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES/<cycle-id>.md` — one per cycle, **local file is the source of truth**. Overridable with `FOLEON_CYCLE_HOME` (CYC-1) |
| Never | inside any repo — not `ripley`, not `fio`, and **not `skills-tinky`**, which is a skills repo, shared pro/perso and pushed to GitHub (CYC-1 v1.1.0) |
| Repos covered | whatever is registered in `hooks/awareness-ignore.txt` (`ripley`, `fio`, …). One cycle doc spans all of them |
| Notion mirror | the **`🔁 Cycles` database** — one row per cycle, sectioned by repo inside the page. Topics/scopes/tasks are page content, never rows or properties (CYC-10 v1.4.0) |
| Annexes | `<cycle-id>.annex.<slug>.md` beside the cycle doc — **the sidecar is the source of truth**; its Notion page is generated, one section per Jira-bound task, and the cycle doc stops validating when the two disagree (CYC-16) |
| Queue | `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES/.state/cycle-queue.jsonl` — dates on which a Foleon repo was edited. Evidence work happened, not log lines |
| History | local-only git in the cycle directory — **no remote, never pushed**. `new`, `log` and `close` commit on their own; `snapshot --why "..."` records a hand-edit (CYC-1 v1.2.0) |
| Jira | Read-only. A task may carry its ticket's key at the end of its line, `[PROD-1234 · Review]`, and Jira then owns that task's title and checkbox (CYC-18). **Nothing here ever writes to Jira** |
| Ticket comments | `.state/<cycle-id>.comments.json` — what has been read, and what was decided about it. A comment that says the build diverged from the write-up is **reduced**, never pasted, into that ticket's `As built` slot (CYC-19) |
| Mechanics | `scripts/cycle.py` (skeleton, hill, tasks, log patterns, annex coverage, close preflight), `scripts/queue.sh` |

The Notion mirror requires the **Notion MCP**. If a call fails because it is not connected, say so and
stop — the local doc is already authoritative, so there is nothing to fall back to and nothing lost.

## How it is invoked

**`/foleon-cycle` on its own, or with anything you want to say.** The verbs below exist, but they are
shortcuts, not a vocabulary the maintainer has to learn. Never make them type one.

**Free text is the primary interface.** `/foleon-cycle here's what came out of the call with Chiel: …`
is a shape flow. `/foleon-cycle where am I` is status. Read what they said and pick the flow; do not
answer a plain-English request by asking them to choose a verb.

**Bare, with nothing else: work out what's next and say it in one line — do not print a menu.** Run the
state check first (`active`, `questions`, `queue.sh count`, `status`), then lead with the single most
likely next step and offer the rest only if they ask:

| State | Almost certainly next |
|---|---|
| No cycle doc | **open a cycle** — ask for the brief |
| Shaping topics, and they've pasted something that reads like answers | **shape** — re-evaluate |
| Shaping topics, nothing new | **questions** — show what's open, ask if anything got answered |
| All shaped, no scopes or tasks | **plan** — factor scopes, read the code |
| A ticket URL was pasted | **jira link** — record the key on the task they name |
| Keyed tasks whose status is stale, or none synced yet | **jira sync** — fetch the keys and refresh |
| A ticket has comments nobody has decided about | **deviations** — read them, reduce what changed the plan, dismiss the rest |
| Tasks exist, queue has unlogged days | **log** — propose lines for those days |
| Tasks exist, queue empty | **status**, then offer the work list |
| Past the dev window end | **close** |

Reconcile from Notion before any of it (flow 6) — they may have ticked things off since you last looked.

| Shortcut | Flow |
|---|---|
| `new` | **1. Open a cycle** — guided intake from a raw brief |
| `shape` | **1b. Shape** — the answers arrived; re-evaluate and decide |
| `questions` | **1c. Open questions**, numbered |
| `plan` | **2. Scopes and tasks** for a shaped topic |
| `tickets` | **3. Work list** — Jira tickets + personal tasks |
| `jira` | **3b. Jira** — link a created ticket, refresh titles and statuses (read-only) |
| `deviations` | **3c. Divergences** — what a ticket's comments say the build actually did |
| `status` | **4. Status** — where every scope sits |
| `log` | **5. Log** what happened |
| `mirror` | **6. Mirror** to Notion |
| `close` | **7. Close** the cycle |

An unrecognised verb is a request in prose, not an error. Anything after a verb is input for that flow.

---

### 1. Open the cycle — guided, not a questionnaire

**Step 1 — ask for everything at once, raw.** One short prompt, not a list of demands:

> Paste whatever you've got for this cycle — the brief as your team handed it over, topics with their
> estimated time, dates, whatever's in the message. Raw is fine; I'll pull it apart and only ask about
> what's missing.

**Step 2 — parse it and show what you found**, as a table of what's present and what's missing:

```
Cycle id:  2026-C4          ✓ from "Cycle 4"
Dates:     —                 missing
Topics:    PDF export        2w
           Search relevance  3d
           Editor polish     1w   ← reads like a grab-bag, not a topic
```

**Step 3 — ask only for the gaps**, batched with `AskUserQuestion`. Never re-ask what the brief already
answered; that is what makes a form feel like an interrogation. If the brief has no dates, ask for
dates — not for the topics you can already see.

**Step 4 — confirm the parse, then create:**
```bash
python3 scripts/cycle.py new --id <cycle-id> --start <date> --end <date>
```
The cycle id is whatever the team calls it — this skill invents no naming scheme. One active cycle at
a time; `new` refuses while another is active.

A wrong parse poisons every question after it, which is why step 2 stops for confirmation and the
topic interview only starts once the shape is agreed.

**Step 5 — interview each topic, but only as far as the topic actually is.** Two states (CYC-3):

- **`shaping`** — nobody can specify it yet. It needs a repo tag, an appetite (`(provisional)` allowed)
  and its **open questions**, verbatim. Then stop. Do **not** ask for the outcome, done signal or first
  cut: those are spec questions, and asking them of an unshaped topic produces either a guess in the
  file or a frustrated maintainer. Give it one `uphill` scope of `self:` research tasks — *"self:
  scoping call with the PO and data engineer → produces the outcome and done signal"* — and that list
  is the real work list for now.
- **`shaped`** — the answers exist. Interview for all six fields: outcome, appetite, first cut, no-gos,
  done signal, repo tag. Batch with `AskUserQuestion` — four at a time turns an interrogation into a
  conversation. Depth scales to appetite: a two-day topic needs outcome, no-gos and done signal,
  nothing more.

**Most cycles start with everything shaping. That is not a failed intake — it is what week one is
for.** Record what *was* decided (id, dates, appetite split, ordering) and let the rest be open
questions. The question bank, depth ladder and the shapeable-yet test are in
[`references/intake.md`](references/intake.md) — read it before the first interview.

Two rules that matter more than the rest:

- **The outcome must be observable from outside the code.** "A reader can download the doc as a PDF
  that matches the on-screen layout" — not "refactor the extractor". If it can't be written, the topic
  isn't shaped, and no amount of task planning will fix that.
- **Anything unanswered is recorded, never inferred.** It goes under `Open questions:` in the
  maintainer's own words. A proposal of yours is not an answer, and an inferred outcome is
  indistinguishable from an agreed one three weeks later.

`cycle.py validate` checks each topic against its declared state and names what's missing.

### 1b. Shape — re-evaluate when answers arrive

This is a **decision** flow, not a form, and it is the most-used flow in the first weeks. Full
procedure: [`references/shaping.md`](references/shaping.md).

**1. Take the dump and re-anchor it.**
```bash
python3 scripts/cycle.py questions     # numbered, per topic
```
Ask for whatever came out of the call, then map answers onto the numbers — they should be able to say
*"1, 4 and 7 are settled"* rather than re-pasting nine questions.

**2. Classify what's left.** One test only: *could you write the outcome, or name the done event,
without this answer?* No → **blocking**. Yes → **non-blocking**. Be strict; "it'd be nice to know" is
not blocking, and a topic held hostage to a non-blocking question is a topic nobody is working on for
no reason.

**3. Propose one of three moves — with the reasoning — and wait for agreement:**

- **Hold** — something blocking is still open. Name who can answer and how it gets asked (a `self:`
  task, not a hope). When the same question has been open across several attempts to get it answered,
  the honest recommendation is *escalate*, not *research more*.
- **Split** — enough is known for *part* of it. Make it two topics: a **shaped** half that is
  independently shippable, and a **shaping** half carrying the unanswered questions. Divide the
  appetite rather than duplicating it. This is Shape Up's own move — hammer a vague topic into a real
  bet — and it is usually the right answer after a partial call.
- **Shape** — everything blocking is answered. Run the full interview, flip to `— shaped`, then go to
  flow 2.

**4. Execute what was agreed:** drop the answered questions, log each answer that changed something
(`--gate surprise`), tick the research tasks it completed, apply the move, then `validate`,
`snapshot`, re-mirror.

Never flip to `shaped` on your own inference, never treat a partial answer as permission to invent the
rest, and never quietly downgrade a blocking question to get a topic moving.

### 2. Factor into scopes, then tasks

**Scopes first, and they are the maintainer's to name.** Propose vertical slices — each independently
finishable, a few days or less, integrating whatever front-end and back-end work that slice needs —
and present the names as a **draft**. Only a name they accepted or rewrote goes in the file. This is
not politeness: scopes become the language the work is discussed in, and a name they wouldn't say out
loud defeats the point.

A UI-only or back-end-only scope is allowed when the work is a genuine **iceberg** (one side far more
complex, not interdependent with the other) — write the reason in the doc.

Ask for the starting hill position per scope; default to `uphill` only if they decline to say. The four
values are `uphill` (figuring it out), `top` (approach known, nothing built), `downhill` (executing),
`done`. **Never infer a position** — not from files touched, not from tasks closed (CYC-6).

**Read the code before proposing tasks.** A task list derived from a topic title is invention (CYC-14).
Load the target repo's context skill — `foleon-fio` or `foleon-ripley`, per the topic's repo tag — and
look at the actual source for the area in question; use `Explore` for a wider sweep, or `senior-dev`
when the rabbit hole is architectural. What you learn changes the task breakdown, the sizing, and the
acceptance criteria. This is the step that makes the difference between a plausible list and a usable one.

**Then tasks, once scopes are accepted.** Half a day to two days each, under exactly one scope.
Must-have by default; a nice-to-have is written `- [ ] ~ …` and never blocks a scope reaching `done`.

**Two kinds of task** (CYC-7), because only one belongs in Jira:
- **Unmarked** — implementation work, becomes a Jira ticket.
- **`self: …`** — yours alone: research, conceptualising, deciding an approach. Its outcome is usually
  *producing the tickets*, e.g. `- [ ] self: research how nested tables paginate → produces the tickets`.
  When it closes and adds three new tasks to its scope, that is the system working, not scope creep.
  **When it closes, its answer goes on the task line** — `→ answer: <what was decided>` (CYC-7). The
  task is the question, so ticking it silently discards what it produced; the dev-log line still goes
  in where a gate admits one, because the log is chronological and the inline answer is findable.
  Under a scope, write **all the `self:` tasks first, then the Jira-bound ones** — the mirror renders
  the kind as a group label instead of repeating `self:` on every line (CYC-15b), and it keeps the
  file's order, so interleaved kinds fail `validate`.
Marking a task `~` **is** the scope-hammering action — so it earns a dev-log line as a decision.

**A shaped topic with any Jira-bound task must have an annex**, and a new ticket changes it. Annexes
are generated from a local sidecar (CYC-16), so `validate` fails until the topic has its `Annex:`
line and every ticket has its section:
```bash
python3 scripts/cycle.py annex sync     # stubs the uncovered tickets
```
`sync` writes the structure. **You write the write-up** — from the code, never generated, for the same
reason acceptance criteria are never generated (CYC-14). An unwritten stub cannot be published.

Every ticket section is **eight named slots in a fixed order** (CYC-17), not free prose: required are
`Expected outcome`, `Done when`, `Criteria` and `Expected testing` — that last one even when the
answer is the literal `none`. Conditional are `Environment`, `Build constraints`, `Open questions`
and `Lives under`, omitted rather than left empty. `Build constraints` is a bullet list under its
fixed verbatim gloss — *what the implementation must respect, and what each one buys.*
— one constraint per line. **There is no "what to build" bullet list**: a step that constrains the
implementation goes in `Build constraints` *with what it buys*, and one that does not is not the
ticket's business. **A ticket never points at another by position** — no "ticket 2"; say what happens
instead and leave sequencing to the annex's ordering section. Contract:
[`references/tickets.md`](references/tickets.md) § The slots.

Edit the markdown directly, then always:
```bash
python3 scripts/cycle.py validate
python3 scripts/cycle.py snapshot --why "PDF export shaped, 3 scopes"
```
`snapshot` refuses to commit a non-conforming doc, so validate-then-snapshot is one habit, not two.
Format details, the exact skeleton and every mechanical rule: [`references/doc-format.md`](references/doc-format.md).

### 3. The work list

```bash
python3 scripts/cycle.py tickets          # prioritised; personal tasks first, then Jira tickets
python3 scripts/cycle.py tickets --json    # machine-readable
```

**Unknowns first** — a task under an `uphill`/`top` scope outranks a must-have under a `downhill` one,
because attacking the unresolved part early leaves time to react to what it reveals. `~` nice-to-haves
come last. Each item carries `P1`/`P2`/`P3` for Jira's own field; where order and P-level disagree for
a given cycle, the order is advice and the maintainer's judgement wins.

**The script emits acceptance criteria as a TODO placeholder on purpose.** Your job is to fill them in
after reading the code — one or two testable statements about *that* change. Never restate the topic
outcome: it reads like a criterion and tests nothing, which is worse than a blank because it looks
finished (CYC-14). Full contract: [`references/tickets.md`](references/tickets.md).

### 3b. Once a ticket exists in Jira

**You never write to Jira.** Not a ticket, not a field, not a transition, not a comment — the
maintainer writes every one of them themselves. The tooling here cannot reach Jira at all: it takes
fetched issues as a local file, and the connector in use is authorised read-only. Full contract and
failure modes: [`references/jira.md`](references/jira.md) (CYC-18).

They create the ticket, then hand you its URL:

```bash
python3 scripts/cycle.py jira link --url <ticket-url> --task "<enough of the task text>"
```
Never guess which task a URL belongs to. They reword tickets on the way into Jira — that divergence is
the reason this exists — so a title match is confident and wrong. `link` lists the candidates and stops
if the fragment is ambiguous.

**From then on Jira owns that task's title and its checkbox**, and the doc keeps what Jira has no
concept of: scope, hill, appetite, the `~` mark, ordering. Refresh it by fetching and feeding the
payload in:

```bash
# fetch with searchJiraIssuesUsingJql — key in (…), fields summary + status — save the payload, then:
python3 scripts/cycle.py jira sync --from /tmp/jira.json
python3 scripts/cycle.py jira list                  # what is linked, what is not, current statuses
```

Two things worth knowing before you touch any of it. **Completion comes from `statusCategory`
(`new`/`indeterminate`/`done`), never a status name** — names are per-project, the maintainer's board
carries `To Do`, `Doing`, `Review`, `QA`, `Done` and `Funnel`, and a name test fails in the direction
that calls unfinished work finished. And **a Jira rename rewrites the annex too**: `sync` updates the
section's `Task:` line, because CYC-16 identifies a section by the task text it quotes. The write-up
body is never regenerated.

A keyed task leaves the checkbox list entirely and renders as a **table row** — key, coloured status,
summary — because a checkbox Jira owns is a control that does nothing. `reconcile` reports a Notion-side
change to one and ignores it. That is the payoff: one status, in one place.

### 3c. What the ticket's comments say the build actually did

The annex is a **proposal**, written before the code existed, and sometimes the build disproves it: a
constraint that turns out unnecessary, one that was wrong about the repo, a stated reason that was
already out of date. That lands as a Jira comment, where nothing acts on it — so the write-up keeps
saying what it said, and the next ticket copies the stale constraint. Full contract:
[`references/deviations.md`](references/deviations.md) (CYC-19).

```bash
# fetch with getJiraIssue INCLUDING the comment field, save the payload, then:
python3 scripts/cycle.py deviations sync --from /tmp/comments.json
python3 scripts/cycle.py deviations list
```

**A comment is never mirrored — it is reduced.** Three fixed parts, all enforced: a **verdict**
(`dropped` = the constraint was unnecessary · `changed` = replaced by a different one · `stale` = the
instruction stands, the reason given for it was wrong), the **anchor** — the write-up line it
contradicts, quoted closely enough that `add` can find it — and what actually happened.

```bash
python3 scripts/cycle.py deviations add --key PROD-4357 --verdict dropped \
        --anchor "Hold events fired before GTM loads and release them once it is up" \
        --note "no queue was built; the dataLayer is a plain array the container drains on load" \
        --comment 10501
python3 scripts/cycle.py deviations dismiss --key PROD-4357 --comment 10502 --why "acknowledgement"
```

**Propose the reduction and wait for a yes.** Their comment is prose; your entry is a claim about
their plan — the same reason `jira link` never guesses which task a key belongs to. And **most
comments are dismissed**: a question, a thank-you, a link. That is the expected outcome, not a failure
to find something.

Two things the entry does not do. It **never rewrites the write-up** — a plan edited to match its
outcome can no longer be wrong, and the retro then reads nothing. And it does not discharge CYC-12: a
divergence that is really a fact about the repo (*"`VITE_APP_ENV` is only set by the staging deploy
workflow"*) belongs in the project skill's `knowledge.md` as well, because the cycle is archived
within weeks.

### 4. Status

```bash
python3 scripts/cycle.py status
```
Prints each topic, its appetite, every scope with its hill position and must-have count, open
questions, and — last — every scope not yet downhill, because that list *is* the risk register. Report
it as-is; resist adding a percentage or a "roughly N% done" gloss (CYC-6).

### 5. Log what happened

```bash
bash scripts/queue.sh peek          # what the hook noticed: dates + repos
python3 scripts/cycle.py log --repo fio --scope "extraction pipeline" \
        --gate surprise --text "nested tables need their own layout pass"
bash scripts/queue.sh drain         # only after the maintainer has resolved the day
```

**A line must pass one of three gates** (CYC-8), and `--gate` makes you name which:

1. **state** — a scope moved on the hill, a must-have completed, a scope reached `done`, work blocked.
2. **decision** — something chosen or cut: a `~` mark, an appetite re-bet, an approach picked.
3. **surprise** — reality differed from the shaping: a rabbit hole opened, an assumption fell, an open
   question got answered.

**Most work earns no line.** Nothing that git already records — files changed, commits made — and no
routine narration. `cycle.py log` rejects "worked on", "continued", "WIP" and friends outright, but the
gate judgement is yours: the test is whether a line would still be worth reading at cycle close.

**Ask which scopes moved.** The queue knows a repo was edited on a date; it cannot know whether that
afternoon was execution or discovering the approach was wrong. Propose the lines, show them, write only
what's approved.

### 6. Mirror to Notion — and read it back

The maintainer reads and works in Notion, so the mirror refreshes at the **end of every flow that
changed the doc**, no permission asked (CYC-10 v2.0.0). A generated page costs nothing to regenerate;
the consent gate only covers *creating* a cycle's row the first time.

**Every flow starts by reconciling**, because they may have ticked things off since you last looked:

```bash
# 1. fetch the cycle page with mcp__notion__notion-fetch, save its body to a file
python3 scripts/cycle.py reconcile --from /tmp/fetched.md
```

Three things are read back from Notion and win: a task's **checked state**, a task's **text**, and
**new task lines** added under an existing scope. Everything else — fields, appetite, topic state,
**hill positions**, scopes, the dev log — is local-authoritative; a Notion-side edit to those is
reported and ignored. The hill is deliberately excluded even though the maintainer setting it there
would satisfy CYC-6: it lives inline in rendered text, and parsing it back is fragility bought for
nothing.

`reconcile` is a **three-way merge** against the snapshot of what was last mirrored. It deletes
nothing (a task gone from Notion is reported and left in place), re-validates before committing, and
stops with nothing written on a real collision — which in practice only happens when the same task was
renamed on both sides.

Topics with an `Annex:` line get their page regenerated in the same pass —
`cycle.py annex render --json` gives the body and the target url, backlink already derived. Annexes
are never read back; a Notion-side edit to one is lost on the next render.

**What to write is not a judgement call — ask the script:**
```bash
python3 scripts/cycle.py mirror plan            # every page Notion is behind on
python3 scripts/cycle.py mirror plan --json     # id, kind, label, url and body for each
```
A cycle owns the cycle page *and* one page per annex, and they move together — a `jira sync` that
retitles a ticket or moves its status changes both. `plan` diffs each page's render against the
snapshot of what was last written to it, so write everything it lists and nothing it doesn't. Every
command that changes the doc ends by naming the pages that fell behind, so the mirror is prompted by
the tooling rather than by the maintainer.

**After a successful write, always — naming the pages that actually went through:**
```bash
python3 scripts/cycle.py mirrored --wrote cycle --wrote "<annex label>"
python3 scripts/cycle.py mirrored     # every page, when the whole mirror succeeded
```
Skipping it is the one way to break the merge: without a fresh snapshot, "unticked in Notion" and
"never ticked" become indistinguishable. Recording a snapshot for a page that was *not* written is the
other way, and it is worse, because it makes the drift invisible — a page left out of `--wrote` keeps
its old snapshot and stays visibly stale instead. Full call sequence and page shape:
[`references/mirror.md`](references/mirror.md).

### 7. Close the cycle

```bash
python3 scripts/cycle.py close
```
Refuses until every topic records `Shipped:` and `Cut:`. On success it flips the doc to read-only and
prints every scope that never reached downhill — **a shaping signal, not a personal failure**: it means
those topics were under-shaped at intake, which is the one feedback loop this system has. Carry it into
the next intake. Then hand the closed doc to `sprint-review` for the retro; this skill does not do
retrospection. Details: [`references/close.md`](references/close.md).

## Boundaries

- **Explicit invocation only.** Do not load or run this skill because a message mentions a cycle, a
  topic, an estimate, planning, or progress. A hook nudge is a cue to *offer*, never to run (CYC-11).
- **Never write to Notion without an explicit yes** on the exact content, in that conversation.
- **Never infer a hill position.** Not from files, commits, task counts, or elapsed time (CYC-6). A
  scope going back uphill is normal and must not be "corrected".
- **Never write a cycle doc into a repo checkout.** `cycle.py` resolves its state dir from its own
  location precisely so a wrong cwd cannot cause this (CYC-1).
- **Never put a durable fact in the dev log.** A gotcha, convention or command that outlives the cycle
  belongs in `foleon-ripley` / `foleon-fio`'s `knowledge.md` (CYC-12) — say which one, and route it
  there. The cycle doc is archived within weeks; a fact parked in it is lost.
- **Never revise an appetite upward** without recording a re-bet as a log line (CYC-4). The response to
  overrun is scope hammering, not more time.
- **No percentages, anywhere.** Not in the doc, not in the mirror, not in a status report (CYC-6).
- **Never write an annex by hand in Notion, and never generate its write-up.** The sidecar is the
  source of truth (CYC-16); the page is output. The structure is automated, the words are not — a
  generated ticket write-up is a generated acceptance criterion one page larger (CYC-14).
- **Never write to Jira** — no ticket, field, transition or comment, however the request is phrased.
  The maintainer writes every ticket themselves (CYC-18). Reading is the point; writing is not on offer.
- **Never paste a comment into an annex, and never record a divergence the maintainer has not
  agreed.** A comment is reduced to a verdict, the line it contradicts and what happened (CYC-19);
  their comment is prose, your entry is a claim about their plan.
- **Never rewrite a ticket write-up to match what was built.** The divergence is appended; the
  proposal stands. A plan edited to match its outcome can no longer be wrong, and close reads nothing.
- **Never infer which task a Jira key belongs to.** The maintainer names it. A title match is wrong
  exactly where it matters, because rewording on the way into Jira is what the key exists to survive.
- **Never edit a closed doc.** Follow-on work belongs to the next cycle.
- **Never give the cycle directory a git remote**, and never push it. The maintainer authorised
  auto-commit *because* the history stays on the laptop; a remote would silently convert a private
  journal into a published one. `cycle.py` refuses to commit if one appears (CYC-1 v1.2.0).

## References

| File | Read when |
|---|---|
| [`references/intake.md`](references/intake.md) | Interviewing a topic into shape — question bank, depth ladder, worked example |
| [`references/doc-format.md`](references/doc-format.md) | Writing or fixing the markdown — exact skeleton, hill semantics, task rules |
| [`references/mirror.md`](references/mirror.md) | Pushing to Notion — page shape, call sequence, consent gate |
| [`references/doc-format.md`](references/doc-format.md) § Annexes | Ticket write-ups — the sidecar, the coverage rule, `annex sync`/`render` |
| [`references/shaping.md`](references/shaping.md) | Re-evaluating a shaping topic — the blocking test, and the hold/split/shape decision |
| [`references/tickets.md`](references/tickets.md) | Producing the work list — ticket shape, ordering, code-grounding |
| [`references/jira.md`](references/jira.md) | A ticket now exists in Jira — linking it, refreshing it, and why nothing here may write |
| [`references/deviations.md`](references/deviations.md) | A ticket has comments — reducing what the build disproved into the annex, and what never goes in it |
| [`references/close.md`](references/close.md) | Closing a cycle and handing off to `sprint-review` |

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Auto-loaded without `/foleon-cycle` | This skill is running and the maintainer never typed the command | Stop and say so. CYC-11 makes explicit invocation part of the standard, not a preference. |
| Made the maintainer pick a verb | Answered a plain request, or a bare invocation, with a menu of nine flows | Read the state and lead with the likely next step. The verbs are shortcuts; nobody should have to learn nine names to use this. |
| Wrote to Notion without a yes | Mirror content appears that was never approved | The worst failure this skill can produce. Say so plainly, and treat the local file as truth when regenerating. |
| Inferred a hill position | A scope moved and the maintainer never said it did | Revert it and ask. The hill measures knowledge, which no file-level signal can see (CYC-6). |
| Tasks planned before scopes were accepted | A topic has tasks but its scope names were never confirmed | Stop; get the scope names right first. Tasks under a wrong slicing are wasted work. |
| Interview became an interrogation | Eight questions for a two-day topic | Depth scales to appetite (CYC-3). Ask three and move on. |
| Asked spec questions of an unshaped topic | The maintainer answers "I don't know yet" to outcome, done signal, first cut | Stop; it's a `shaping` topic (CYC-3). Record the open questions verbatim, give it `self:` research tasks, move on. This exact deadlock is why the states exist. |
| Wrote `Outcome: TBD` to pass validation | A field filled with a placeholder nobody said | Never. It validates and produces the untrustworthy doc CYC-3 exists to prevent. Mark the topic `shaping` instead. |
| Flipped a topic to `shaped` without the answers | State changed after a conversation with you, not with the PO | Revert. The transition follows answers arriving from people (CYC-3). |
| Filled a blank with a guess | An outcome or done-signal the maintainer never said | Move it to `Open questions:` verbatim and ask. Inferred fields are the fastest way to make the doc untrustworthy. |
| Dev log turned into a diary | Multiple lines per day, "continued on…", file lists | Re-read the three gates. Most work earns no line; `cycle.py validate` catches the phrasings, not the volume. |
| Durable fact logged in the cycle doc | A gotcha or convention sitting in the dev log | Route it to the project skill's `knowledge.md` (CYC-12) and say which. From there the cheat-sheet pipeline can reach it; from a cycle archive, nothing can. |
| Queue drained but nothing logged | Queue empty, no new log lines, work unaccounted for | `bash scripts/queue.sh restore` before the turn ends. |
| Two active cycles | `cycle.py active` prints more than one | Close the stale one (CYC-1). One active cycle is what makes "the doc" unambiguous. |
| Git commit failed (no identity, locked index) | `cycle.py` prints a note but the file saved | Nothing to recover — the markdown is the artifact. Fix `user.email`/`user.name` if they want history working again. |
| Proposed tasks without reading the code | A breakdown that could have been written from the topic title alone | Stop and read the source (CYC-14). Plausible-but-wrong task lists are the most expensive output this skill can produce. |
| Acceptance criteria restate the outcome | Every ticket's criteria say the same thing | Replace with testable statements about that change, or leave the placeholder. Filler that looks finished is worse than an admitted blank. |
| Held a topic on a non-blocking question | A topic sat shaping for a week over something discoverable later | Apply the blocking test (`references/shaping.md`). Split it and start the shapeable half. |
| Split into halves that aren't independent | The "shaped" half only makes sense once the other lands | Then it is not a split — it is one topic still shaping. Revert it. |
| Cooldown work pushed through intake | A "topic" with no real appetite, e.g. "bug fixing" | Cooldown is off-book (CYC-2). Don't shape it; it doesn't belong in the doc. |
| Ticket write-up is free prose, or a bare "what to build" list | A section without the CYC-17 slots, or with implementation bullets carrying no reason | `validate` fails on it. Rewrite into the slots; a constraining step goes in `Build constraints` with what it buys, the rest is deleted. |
| Shaped topic with tickets and no annex | `validate` names the topic and its ticket count | Add the `Annex:` line, then `cycle.py annex sync`. Optional annexes date from when they were hand-written (CYC-16 v5.1.0). |
| Annex drifted from the ticket list | A ticket was added and the annex still describes the old set | `cycle.py validate` now fails on it (CYC-16). `annex sync` inserts the stub; write it before mirroring. |
| Wrote an annex write-up from the task title | A section that could have been written without opening the repo | Same failure as generated acceptance criteria, one page larger. Read the code (CYC-14), or leave the stub and say it is unwritten. |
| Edited an annex in Notion | Content on the annex page that is not in the sidecar | It is lost on the next render — annexes have no writable surface. Move it into the sidecar before re-rendering, and say so. |
| Wrote to Jira | Any ticket, field, transition or comment changed by this skill | The worst failure it can produce, worse than an unapproved Notion write, because the maintainer's own tracker now says something they did not write. Say so immediately and name exactly what changed. Nothing in the design was supposed to make it reachable (CYC-18). |
| Pasted a Jira comment into the annex | An `As built` line that is a paragraph of prose | `validate` rejects it (CYC-19). Reduce it to verdict, anchor and note; if it reduces to nothing, it was a dismissal. |
| Recorded a divergence nobody agreed to | An `As built` entry written straight from a comment | Remove it and propose. Reading their prose is not the same as being told what it means for the plan. |
| Edited the write-up to match the build | A constraint deleted or reworded instead of a divergence appended | Restore it (CYC-19). The proposal is the record of what was agreed; overwritten, the close routine has nothing to report. |
| Guessed which task a Jira key belongs to | A key linked without the maintainer naming the task | Unlink it and ask. Rewording on the way into Jira is the whole reason keys exist; a title match is confident and wrong. |
| Read completion from a status name | A `Review` or `QA` ticket showing as done | Read `statusCategory` (CYC-18). Status names are per-project, and the name test fails in the direction that calls unfinished work finished. |
| Notion MCP unavailable | An MCP call errors on connection | Carry on locally — the local doc is authoritative, so the only cost is a stale mirror. Say so, and refresh next time. |
| Mirrored but forgot `mirrored` | Next reconcile reports changes the maintainer already made, or misses ticks | The snapshot is the merge's only reference point. Run it after every successful write, never before. |
| Wrote the cycle page and not the annex | Notion's annex quotes a ticket status or title Jira has already moved past | Run `cycle.py mirror plan` — it lists every page that is behind, and a mirror writes all of them. This is why the plan step exists. |
| Snapshotted a page that was never written | `mirrored` recorded an annex the mirror skipped, so nothing can see the drift | Name the pages actually written: `mirrored --wrote <id>`. A page left out keeps its old snapshot and every later command reports it stale. |
| Reconcile wanted to delete a task | A task vanished from Notion | It is reported, not deleted (CYC-10). Deleting the maintainer's work automatically is never right; they can remove it locally if they meant it. |
| Notion-side edit to a field or the hill | The page's fields differ from the local doc | Report and ignore (CYC-10). Only checked-state, task text and added tasks come back. |
| Tempted to add a Notion database, status property or approval workflow | Any urge to give topics/scopes/tasks Notion properties | Don't (CYC-10/CYC-11). The cheat sheet already cost a full architecture reversal to learn this once. |
