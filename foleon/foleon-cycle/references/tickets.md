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

A shaped topic with any Jira-bound task gets an **annex** (see `doc-format.md`): a local sidecar
file, one section per ticket, rendered to its own Notion page. It is not optional — without it the
tickets reach Jira with nothing behind them and none of the slots below apply. A shaping topic has
only `self:` tasks, so it has nothing to annex.
`cycle.py annex sync` creates the section the moment a Jira-bound task appears and the cycle doc
stops validating until it is written — so the annex cannot fall behind the ticket list (CYC-16).
What it will not do is write it: a generated write-up is the same failure as generated acceptance
criteria, one page larger. That page has a hard budget.

**Roughly ten lines per ticket, and no more than one screen of shared background.** A 145-line
document about three tickets does not get read, and an unread document is worth less than no
document. Length is not thoroughness; it is a failure to decide what matters.

### The slots (CYC-17)

Per ticket, exactly these, in this order and nothing else. Three are required; the rest are written
only when they apply and **omitted** — never left as an empty header — when they do not.

| Slot | | What goes in it |
|---|---|---|
| `**Expected outcome**` | required | One or two sentences: what this ticket must achieve, observable from outside the change, in words that survive being read by someone who has never opened the repo. |
| `**Environment**` | if applicable | Settled facts the implementer must respect but did not choose — an id, a gate, a pattern to copy, a sequencing constraint. |
| `**Build constraints**` | if applicable | What the implementation must respect and did not get to choose. **A bullet list, one item per line, each carrying what it buys — under the fixed gloss, verbatim: `— what the implementation must respect, and what each one buys.`** |
| `**Open questions**` | if applicable | What is still undecided inside this ticket, and who settles it. (This replaces the old **Ask first**.) |
| `**Done when**` | required | One sentence, observable: the signal that the ticket is finished. |
| `**Criteria**` | required | The testable statements about this change, run together on one line separated by `·`, never a bulleted list of full sentences. |
| `**Lives under**` | if applicable | Where the code goes — a path, not a paragraph. |
| `**Expected testing**` | required | Which tests, at which level, naming the project and the file convention. The literal `none` when there are none. |
| `**As built**` | if applicable | Where the build diverged from the constraints above. **A bullet list, one divergence per line, each `- **<verdict>** · <the line it contradicts> — <what actually happened>`** — under the fixed gloss, verbatim: `— where the build diverged from the constraints above, and what each divergence changes.` Written after the code, never by hand: see [`deviations.md`](deviations.md). |

`Done when` and `Criteria` are **siblings, not a nested pair**. They answer different questions —
*how do I know I am finished* and *what would fail if I were not* — and the first version of this
standard nested the second inside the first, which buried the only half a reviewer can check.

`Build constraints` is a **list** because its items are independent constraints. Run together behind
`·` they make the reader do the separating that punctuation should have done for them.

**Why it carries a gloss, and why the gloss is fixed.** The slot was called `Parameters` until the
first developer to read a slotted ticket took its three bullets for the function's argument list and
asked which three arguments were meant. The name invited it — half these tickets *are* about writing a
function. So: renamed, and glossed, because the two things the reader needs are derivable from no
header at all — that these are constraints the implementer did not get to choose, and that every line
states what it buys. The gloss is a **fixed string**, not a sentence you write per ticket: that makes
it machine-checked, and stops one slot acquiring forty different explanations of itself.

**Never point at another ticket by position.** No "ticket 2 adds the real one", no "the first three
tickets". The reader has the tracker open and none of this page, so the number resolves to nothing —
and it is the annex's running order, so it is wrong the moment a ticket is added or split, with
nothing able to notice. Say what happens instead: *"which is what lets the real transport land later
without reopening any feature code"*. Sequencing goes in the **Order** section at the end of the
annex, which is free-form, never pasted into Jira, and the one place a running order is correct by
construction. A background section may name a ticket by its **title**; never by its number.

**Why `Expected testing` is required even when the answer is `none`:** unstated testing is how "no
tests" gets decided by whoever is in a hurry rather than by whoever wrote the ticket. Where a
criterion cannot be tested — vendor behaviour, prose — say so in the slot and name the manual check.

**There is no "what to build" list.** The maintainer pasted the first ticket into Jira and deleted
exactly that: three bullets of implementation steps with no reason attached to any of them, which
reads as noise to whoever picks the ticket up and duplicates what the code will say anyway. A step
that genuinely constrains the implementation goes in `**Build constraints**` **with what it buys**; a step that
does not is not the ticket's business. `cycle.py validate` enforces the slots, their order and the
two lines under `Acceptance criteria`.

Above all of it, the **proposed Jira ticket name** — the summary that goes in the tracker. Write it to
survive being read in a list of forty tickets with none of this page around it: imperative, naming the
thing and the system it belongs to. `annex sync` stubs it and `annex render` refuses to publish the
placeholder, so it is never silently the section heading.

Shared background sits once at the top: what the system is in plain terms, what is already settled,
what is still open. Never repeated per ticket.

**Cut on sight:**

- "Why it is its own ticket", "why this matters", "what exists now" as separate headed paragraphs —
  fold the load-bearing half into the first sentence and delete the rest.
- Restating a decision that the settled-list at the top already carries.
- Explaining a concept the reader will meet in the code anyway.
- Priority, estimate and dependency lines repeated per ticket when a two-line **Order** section at the
  end says the same thing once.
- A `**Build constraints**` item with no reason attached — that is the banned checklist wearing a slot name.
- A reference to another ticket by number or position — it resolves to nothing in the tracker and rots
  on the next reorder.
- A slot padded to look justified: an `Expected outcome` that argues for itself, or states something
  trivially true of the code as it stands. Write the outcome and stop.

**`As built` is the only slot that is not a proposal.** Everything above it was agreed before the
code existed; that half is never rewritten to match what happened, because a plan edited to match its
outcome can no longer be wrong, and the close routine then reads nothing. The divergence is *appended*
and the proposal stands (CYC-19).

**Assume no prior knowledge, not no intelligence.** Name the file and the function that already solve
the problem — `rum.ts`, `identifyEditorUser`, `monitoringEnabled()` — instead of describing at length
what they do. A path is shorter than a paragraph and more useful.

## The list is disposable

It is regenerated from the doc every time and is never a second source of truth (CYC-14). Don't store
it, don't mirror it to Notion as a task database (CYC-10), and don't hand-edit it — change the doc and
regenerate. Once tickets are pasted into Jira, Jira owns their state; the cycle doc keeps tracking the
*scopes*, which is the level status conversations actually work at.
