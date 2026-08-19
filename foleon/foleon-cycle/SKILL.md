---
name: foleon-cycle
description: >-
  Runs the maintainer's ShapeUp/Scrum cycle end to end: opens one doc per cycle,
  interviews each topic into shape (outcome, appetite, first cut, no-gos, done
  signal), factors it into scopes tracked on a four-value hill, plans tasks,
  logs progress, mirrors the doc to one Notion page after an explicit yes, and
  closes the cycle by handing the retro to `sprint-review`. Local markdown in
  `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES/` is the source of truth; Notion is a derived
  mirror. Covers every Foleon repo a cycle touches — `ripley`, `fio`, and any
  added later. Enforces `docs/stds/CYCLE_DOC.md` (CYC-1…CYC-13).
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

Governed by [`docs/stds/CYCLE_DOC.md`](../../docs/stds/CYCLE_DOC.md) (CYC-1…CYC-13). The standard wins
any disagreement with this file.

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
| Notion mirror | one **page** per cycle, nested by project like the cheat sheet's CHS-9a — never a database (CYC-10) |
| Queue | `~/Documents/GAEL/FOLEON/SHAPEUP-CYCLES/.state/cycle-queue.jsonl` — dates on which a Foleon repo was edited. Evidence work happened, not log lines |
| History | local-only git in the cycle directory — **no remote, never pushed**. `new`, `log` and `close` commit on their own; `snapshot --why "..."` records a hand-edit (CYC-1 v1.2.0) |
| Mechanics | `scripts/cycle.py` (skeleton, hill, tasks, log patterns, close preflight), `scripts/queue.sh` |

The Notion mirror requires the **Notion MCP**. If a call fails because it is not connected, say so and
stop — the local doc is already authoritative, so there is nothing to fall back to and nothing lost.

## What this skill is asked to do

Six things. Ask which one if it isn't obvious; don't assume "new cycle" because a cycle is mentioned.

| Ask | Flow |
|---|---|
| A cycle just started, here's the description | **1. Open + intake** |
| Plan this topic / break it down | **2. Scopes and tasks** |
| Where am I / what's the state | **3. Status** |
| Log what happened | **4. Log** |
| Push it to Notion | **5. Mirror** |
| The cycle is over | **6. Close** |

---

### 1. Open the cycle and shape the topics

```bash
python3 scripts/cycle.py new --id <cycle-id> --start <date> --end <date>
```
The cycle id is whatever the team calls it — this skill invents no naming scheme. One active cycle at
a time; `new` refuses while another is active.

**Then parse the pasted description into candidate topics with their estimates, and show that parse
back before asking anything.** A wrong parse makes every later question wrong. Do not interview yet.

**Then interview each topic** until it has all six CYC-3 fields: outcome, appetite, first cut, no-gos,
done signal, repo tag. Batch the questions with `AskUserQuestion` — four at a time turns an
interrogation into a conversation. Depth scales to appetite: a two-day topic needs outcome, no-gos and
done signal, nothing more. The question bank, the depth ladder and worked examples are in
[`references/intake.md`](references/intake.md) — read it before the first interview.

Two rules that matter more than the rest:

- **The outcome must be observable from outside the code.** "A reader can download the doc as a PDF
  that matches the on-screen layout" — not "refactor the extractor". If it can't be written, the topic
  isn't shaped, and no amount of task planning will fix that.
- **Anything unanswered is recorded, never inferred.** It goes under `Open questions:` in the
  maintainer's own words. A proposal of yours is not an answer, and an inferred outcome is
  indistinguishable from an agreed one three weeks later.

A topic with a missing field gets no scopes and no tasks. `cycle.py validate` will say which field.

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

**Then tasks, once scopes are accepted.** Half a day to two days each, under exactly one scope.
Must-have by default; a nice-to-have is written `- [ ] ~ …` and never blocks a scope reaching `done`.
Marking a task `~` **is** the scope-hammering action — so it earns a dev-log line as a decision.

Edit the markdown directly, then always:
```bash
python3 scripts/cycle.py validate
python3 scripts/cycle.py snapshot --why "PDF export shaped, 3 scopes"
```
`snapshot` refuses to commit a non-conforming doc, so validate-then-snapshot is one habit, not two.
Format details, the exact skeleton and every mechanical rule: [`references/doc-format.md`](references/doc-format.md).

### 3. Status

```bash
python3 scripts/cycle.py status
```
Prints each topic, its appetite, every scope with its hill position and must-have count, open
questions, and — last — every scope not yet downhill, because that list *is* the risk register. Report
it as-is; resist adding a percentage or a "roughly N% done" gloss (CYC-6).

### 4. Log what happened

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

### 5. Mirror to Notion

The mirror is **derived and one-way**: regenerated whole from the local file, never patched, never read
back as an update path. Local wins on any divergence — surface it, don't overwrite silently.

**Nothing is written until the maintainer says yes in that conversation** (CYC-11). Show the content
and the target page first. A "looks good" is a yes; silence is not. Full call sequence and page shape:
[`references/mirror.md`](references/mirror.md).

### 6. Close the cycle

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
| [`references/close.md`](references/close.md) | Closing a cycle and handing off to `sprint-review` |

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Auto-loaded without `/foleon-cycle` | This skill is running and the maintainer never typed the command | Stop and say so. CYC-11 makes explicit invocation part of the standard, not a preference. |
| Wrote to Notion without a yes | Mirror content appears that was never approved | The worst failure this skill can produce. Say so plainly, and treat the local file as truth when regenerating. |
| Inferred a hill position | A scope moved and the maintainer never said it did | Revert it and ask. The hill measures knowledge, which no file-level signal can see (CYC-6). |
| Tasks planned before scopes were accepted | A topic has tasks but its scope names were never confirmed | Stop; get the scope names right first. Tasks under a wrong slicing are wasted work. |
| Interview became an interrogation | Eight questions for a two-day topic | Depth scales to appetite (CYC-3). Ask three and move on. |
| Filled a blank with a guess | An outcome or done-signal the maintainer never said | Move it to `Open questions:` verbatim and ask. Inferred fields are the fastest way to make the doc untrustworthy. |
| Dev log turned into a diary | Multiple lines per day, "continued on…", file lists | Re-read the three gates. Most work earns no line; `cycle.py validate` catches the phrasings, not the volume. |
| Durable fact logged in the cycle doc | A gotcha or convention sitting in the dev log | Route it to the project skill's `knowledge.md` (CYC-12) and say which. From there the cheat-sheet pipeline can reach it; from a cycle archive, nothing can. |
| Queue drained but nothing logged | Queue empty, no new log lines, work unaccounted for | `bash scripts/queue.sh restore` before the turn ends. |
| Two active cycles | `cycle.py active` prints more than one | Close the stale one (CYC-1). One active cycle is what makes "the doc" unambiguous. |
| Git commit failed (no identity, locked index) | `cycle.py` prints a note but the file saved | Nothing to recover — the markdown is the artifact. Fix `user.email`/`user.name` if they want history working again. |
| Notion MCP unavailable | An MCP call errors on connection | Report and stop. The local doc is authoritative — no fallback surface, nothing lost. |
| Tempted to add a Notion database, status property or approval workflow | Any urge to give topics/scopes/tasks Notion properties | Don't (CYC-10/CYC-11). The cheat sheet already cost a full architecture reversal to learn this once. |
