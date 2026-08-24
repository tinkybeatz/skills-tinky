# The work list — tickets and tasks

Governed by CYC-14. The doc's purpose is not record-keeping; it is to produce the next action. This is
that output.

```bash
python3 scripts/cycle.py tickets           # human-readable, ordered
python3 scripts/cycle.py tickets --json    # for further processing
```

## Two kinds, because only one belongs in a tracker

| Kind | Written | Becomes |
|---|---|---|
| Implementation | `- [ ] map blocks to PDF primitives` | a Jira ticket |
| Research / conceptualising | `- [ ] self: research how nested tables paginate → produces the tickets` | a task for the maintainer only |

A research task in Jira is a ticket nobody can close, because its output is *more tickets*. Keeping it
out of the tracker is the point — and when it closes and adds three tasks to its scope, that is the
unknown resolving, not scope creep (CYC-7).

## Read the code first — this is not optional

A breakdown written from a topic title is invention, and it is the most expensive wrong output this
skill produces: every ticket after it inherits the mistake.

1. Load the repo's context skill from the topic's tag — `foleon-fio` or `foleon-ripley`.
2. Look at the actual source for the area in question. `Explore` for a wide sweep; `senior-dev` when
   the rabbit hole is architectural rather than a matter of finding the code.
3. Let what you find change the breakdown — tasks you did not anticipate, tasks that turn out
   unnecessary, sizing that was wrong, a scope that should split.

The test: **could this task list have been written without opening the repo?** If yes, it isn't done.

## Ordering — unknowns first

| Rank | What |
|---|---|
| 1 | Must-haves under `uphill` / `top` scopes — the unresolved parts |
| 2 | Must-haves under `downhill` scopes — known execution |
| 3 | `~` nice-to-haves, whatever their scope |

Attacking unknowns early is what leaves time to react to what they reveal; a downhill task done first
buys nothing you didn't already have. Each item also carries `P1`/`P2`/`P3` so Jira's field can be set —
`P1` for must-haves in unresolved scopes, `P2` for known work, `P3` for nice-to-haves. Where the running
order and the P-levels disagree for a particular cycle, the order is advice: the maintainer's judgement
wins, and it should just make sense rather than follow the formula off a cliff.

## What a ticket carries

```
### 2. [fio] handle page-break inside a cell
Epic: PDF export · scope: table pagination (uphill) · P1
Why: A reader can download the doc as a PDF that matches the on-screen layout.
Topic done signal: merged to main and demoed to design
Acceptance criteria: TODO — one or two testable statements about THIS change,
  written after looking at the code. Do not restate the topic outcome.
```

**The criteria placeholder is deliberate.** The script will not generate them, because the only thing
it could generate is the topic outcome pasted per ticket — text that reads like acceptance criteria
and tests nothing. That is worse than a blank: a blank asks to be filled, filler looks finished.

Write them from the code. For the ticket above, that might be: *a table row split across a page break
renders its continuation with the header repeated*, and *no cell content is clipped at the boundary*.
Both are checkable; neither could have been written from the topic title.

## Ticket write-ups — short, and written for a newcomer

When a topic's tickets need more than one line each, they get an **annex** (see
`doc-format.md`): a local sidecar file, one section per ticket, rendered to its own Notion page.
`cycle.py annex sync` creates the section the moment a Jira-bound task appears and the cycle doc
stops validating until it is written — so the annex cannot fall behind the ticket list (CYC-16).
What it will not do is write it: a generated write-up is the same failure as generated acceptance
criteria, one page larger. That page has a hard budget.

**Roughly ten lines per ticket, and no more than one screen of shared background.** A 145-line
document about three tickets does not get read, and an unread document is worth less than no
document. Length is not thoroughness; it is a failure to decide what matters.

Per ticket, in this order and nothing else:

1. **What it is** — one or two sentences. What the thing does, in words that survive being read by
   someone who has never opened this repo.
2. **What to build** — three to six terse bullets. No sub-bullets, no rationale paragraphs.
3. **Done when** — one sentence, observable.
4. **Criteria** — the testable statements, run together on one line separated by `·`, not a bulleted
   list of full sentences.
5. Anything genuinely undecided, marked **Ask first**.

Shared background sits once at the top: what the system is in plain terms, what is already settled,
what is still open. Never repeated per ticket.

**Cut on sight:**

- "Why it is its own ticket", "why this matters", "what exists now" as separate headed paragraphs —
  fold the load-bearing half into the first sentence and delete the rest.
- Restating a decision that the settled-list at the top already carries.
- Explaining a concept the reader will meet in the code anyway.
- Priority, estimate and dependency lines repeated per ticket when a two-line **Order** section at the
  end says the same thing once.

**Assume no prior knowledge, not no intelligence.** Name the file and the function that already solve
the problem — `rum.ts`, `identifyEditorUser`, `monitoringEnabled()` — instead of describing at length
what they do. A path is shorter than a paragraph and more useful.

## The list is disposable

It is regenerated from the doc every time and is never a second source of truth (CYC-14). Don't store
it, don't mirror it to Notion as a task database (CYC-10), and don't hand-edit it — change the doc and
regenerate. Once tickets are pasted into Jira, Jira owns their state; the cycle doc keeps tracking the
*scopes*, which is the level status conversations actually work at.
