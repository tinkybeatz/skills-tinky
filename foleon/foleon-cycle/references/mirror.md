# Mirror — the Notion page

The mirror exists so the plan is readable — and now editable — without opening a terminal. One page
per cycle, refreshed automatically, with a **narrow writable surface** (CYC-10 v2.0.0). Requires the Notion MCP; if a call fails on connection, say so and stop
— the local file is already authoritative, so there is nothing to fall back to and nothing at risk.

## Shape

The mirror is the **`🔁 Cycles` database** — one row per cycle, each row's page holding that cycle's
content, sectioned by repo (CYC-9).

```
🔁 Cycles (database)          collection://8ef91e3a-d35c-44d2-91ba-9c895b545dbe
                              https://app.notion.com/p/52a92abebbdf407ba1d6b63f46412cc9
├── 2026-C4    In progress   2026-08-18 → 2026-09-26   fio, ripley
│     # Preview                   ← header callout, hill board, the bet (CYC-15a)
│     # fio                       ← project section + a derived orientation line
│     ## 🎯 Shape 1: PDF export   ← topic, numbered across the whole cycle
│     #### page breaks — `uphill` ← scope (stays h4: `reconcile` keys on it)
│     # ripley
│     # Dev log
└── 2026-C3    Done          …
```

**Properties are derived, never input** (CYC-10). Regenerate all four on every mirror:

| Property | From the local file |
|---|---|
| `Name` | the cycle id |
| `Status` | `active` → In progress · `closed` → Done |
| `Dates` | the header's start → end |
| `Repos` | multi-select, union of the topics' repo tags |

A property that cannot be regenerated from the local file must not be added — a hand-editable
property is a second source of truth, which the one-way rule forbids.

Page ids live in `<cycle home>/.state/mirror.json`:

```json
{"data_source_id": "8ef91e3a-d35c-44d2-91ba-9c895b545dbe",
 "cycles": {"2026-C4": {"id": "...", "url": "..."}}}
```

Read it before mirroring, write it after creating a row. **Topics, scopes and tasks are never rows and
never properties** — that is the boundary this shape is allowed to exist inside (CYC-10 v1.4.0).

## What the page carries

### The writable surface

| Editable in Notion, wins on read | Local-authoritative, Notion edits reported and ignored |
|---|---|
| a task's checked state | **every Jira-keyed task** — it renders as a table row, not a to-do item (CYC-18) |
| — | topic fields (outcome, no-gos, done when) |
| a task's text | appetite, topic state (`shaping`/`shaped`) |
| new task lines under an existing scope | **hill positions**, scopes themselves, the dev log |
| a task's **kind**, from the group label it sits under | — |

The hill is excluded on purpose. The maintainer moving it in Notion would satisfy CYC-6 — it is still a
human setting it — but it renders inline in text rather than as a property, so reading it back is
fragility bought for no benefit. Revisit once the checkbox path has a cycle of real use behind it.

| Include | Leave local |
|---|---|
| Repo sections, one per repo the cycle touches | The header line — `Dates` and `Status` are row **properties**; writing them in the body too creates two truths in one page |
| Every topic with all its shaped fields | — |
| Every scope with its hill position and its must-have tally | — |
| Every task, as a to-do item — they are the input surface (CYC-10 v2.0.0) | — |
| Open questions, numbered | — |
| The dev log | — |

Scope-level is still the *reportable* unit — Shape Up's point is that status conversations work
better pointing at finished slices than defending individual outstanding tasks — which is why the
hill board leads the page and the scope carries a must-have tally. Every task is nonetheless
mirrored: v1.x left long task lists out on exactly the "40 checkboxes recreate the weeds" argument,
and v2.0.0 overrode it, because a checkbox the maintainer cannot tick is not weeds, it is a missing
input.

## How it reads — the visual contract (CYC-15)

The renderer owns all of this; it is written down here so a change to it is a deliberate one.

| Rule | Why |
|---|---|
| **Hill board first** — every scope, its position, its must-have tally, colour-coded | The whole cycle on one screen. The hill's value is being *seen*; three screens down as inline text it was the doc's least visible signal |
| One fixed colour per hill value — `uphill` orange, `top` purple, `downhill` blue, `done` green | A colour that moves between cycles teaches nothing |
| **Outcome + done signal** in a blue callout, loudest block in the topic | It is the sentence that decides whether everything under it is the right work |
| Appetite, first cut, no-gos in **grey**, below it | Constraints matter and still lose to what the topic *is* |
| Open questions **numbered**, matching `cycle.py questions` | So "3 and 5 are settled" is sayable straight off the page |
| Topic state stated **once** (in the callout) | It used to be in the heading, the icon and the counter — three renderings of one fact |
| **Page-level sections at `#`** — `Preview`, one per project, `Dev log`; nothing outside a section | The top half used to be three unframed blocks, so the page's shape had to be inferred from its contents |
| Topics as **`## <icon> Shape N: <name>`**, numbered across the whole cycle | Three shapes rendered as three bare titles read as one column. Colon, not em dash — topic names already contain em dashes |
| The ordinal is **derived only** — never in the local doc, a log line, a ticket, or anything the skill says | It renumbers the moment a topic is added or split. Topics and scopes are referred to by **name** |
| A one-line grey **orientation** under every `#` section; for a project, derived counts only | *"why is 'fio' just here like that without any context???"* — and an invented sentence about the repo would read like a fact |
| Task kind as a **coloured group label** per scope (research orange, first; ticket work blue) — never a `self:` prefix | Forty lines of `self:` spent forty lines on a grouping the eye reads for free. The label carries the colour the task line never may |
| `###` unused — scopes stay `####` | `reconcile` keys on that level and mirrored pages already carry it (the skipped-level exception NST-2 permits, recorded in CYC-15a) |
| Dev log as a table: when · scope · what changed | Fine as four bullets, unreadable as forty |
| Completion as a count (`2 of 7`), never a percentage | CYC-6 |
| **The bet** table + a mermaid bar chart: appetite per topic against the 6w window, with the unbooked remainder | "How much time is it worth" was only answerable by reading three topics and adding up |
| Bars and charts over **time only** — never over task completion | An appetite is a real quantity. A bar over must-haves-done implies the remaining work is known, which `uphill` says it isn't |
| The hill as a **position track** (`◉ ─ ○ ─ ○ ─ ○`), never a fill bar and never a 2-axis plot | Four ordinal stops. A fill bar reads "half done"; a plot needs a coordinate nobody stated (CYC-6) |

**The one hard exclusion: nothing `reconcile` parses back may carry a rendering attribute.** Scope
headings (`#### name — \`hill\``) and task lines render plain, with no `{color=}` and no decoration.
A colour attribute on a task line is swallowed into the task's *text*, and task text is
Notion-authoritative under CYC-10 v2.0.0 — so styling the writable surface hands the three-way merge
corrupted input. That is a data-loss bug wearing a styling change's clothes. The hill gets its colour
in the board instead, which is derived output nothing reads back — and the task's kind gets its
colour on the **group label**, which is not parsed either. That is the whole trick of CYC-15b: the
label line can be as loud as it likes because nothing reads it back, so the writable line stays bare.

The general rules behind all of this — heading meaning, the workspace colour mapping, callout and
table discipline, "a repeated literal prefix is a grouping, not text", parsed-back-renders-plain —
live in [`docs/stds/NOTION_STYLE.md`](../../../docs/stds/NOTION_STYLE.md) (NST) and bind every
generated page in the workspace. This table is only what is specific to the cycle mirror.

## Sequence

**1. Validate first, then plan.** `python3 scripts/cycle.py validate` — never mirror a non-conforming
doc, or the malformation gets a second home.

```bash
python3 scripts/cycle.py mirror plan            # which pages Notion is behind on
python3 scripts/cycle.py mirror plan --json     # id, kind, label, url and body for each
```

**`mirror plan` is the list of pages to write, and it is not optional.** A cycle owns more than one
Notion page — the cycle page and one per annex — and they move together: a `jira sync` that retitles a
ticket or moves its status changes both. `plan` compares each page's render against the snapshot of
what was last written to it, so the mirror is no longer a matter of remembering that annexes exist.
Write every page it lists, in one pass. Anything it does not list is already current and must be left
alone.

Every command that changes the doc — `log`, `jira sync`, `reconcile`, `annex sync`, and `validate` and
`status` besides — ends by naming the pages that have fallen behind. That report is the trigger to
mirror; the maintainer should never have to ask for it.

**2. Fetch the current page.**
```
mcp__notion__notion-fetch
  id: <cycle page id from .state/mirror.json>
```
Fresh, every time. This is also the divergence check: if the page holds anything the local file
doesn't, **stop and surface it** — someone edited the mirror by hand. Local wins (CYC-10), but
overwriting silently would destroy whatever they wrote there. Show them, then let them decide.

**3. Render with the script, never by hand.**
```bash
python3 scripts/cycle.py render            # body + derived properties, for review
python3 scripts/cycle.py render --json     # {"properties": {...}, "body": "..."} for the calls
```
It refuses to render a non-conforming doc, and it is deterministic — the first hand-render duplicated
`Dates`/`Status` in the body when the row's properties already carried them, which is exactly the
drift a script prevents.

The render is the whole page from the local file. Whole-page regeneration is the only write path —
never patch a line, never diff. (Note the deliberate contrast with `foleon-cheatsheet`, which appends
one bullet and is forbidden from replacing a page: there, the page is hand-authored and the skill is a
guest; here, the page is *generated output* and the local file is the author.)

**4. Refreshing an existing page needs no permission** (CYC-10 v2.0.0). The page is generated output
and the local file is its author, so regenerating it costs nothing and asking each time is friction
the maintainer explicitly does not want. The consent gate covers **creating** a cycle's row for the
first time, and nothing else. Step 2's divergence check still applies: if the page holds something the
local file does not, stop and show it before overwriting.

**5. Write.** Content and properties both, in that order:
```
mcp__notion__notion-update-page
  data: { page_id: <id>, command: "replace_content", new_str: "<rendered markdown>" }
mcp__notion__notion-update-page
  data: { page_id: <id>, command: "update_properties",
          properties: { "Status": "In progress",
                        "date:Dates:start": "2026-08-18", "date:Dates:end": "2026-09-26",
                        "Repos": ["fio", "ripley"] } }
```
For a new cycle, `mcp__notion__notion-create-pages` with
`parent: { type: "data_source_id", data_source_id: "8ef91e3a-d35c-44d2-91ba-9c895b545dbe" }`, then
record the new id in `<cycle home>/.state/mirror.json`.

## Access — why this database and not another (2026-08-19)

This database was **created by the skill**, which is what gives it full access including schema
changes (`update_data_source`). That was not cosmetic: the maintainer's own hand-made `Cycles`
database accepted `create_pages` and `update_page` but refused **all** schema DDL with
`object_not_found`, and the Claude connector could not be added to it from Notion's
`•••` → Connections menu (searching "Claude" returned no results — it is a workspace-level
integration, not a per-object one). Every property and every select option there had to be added by
hand.

So: **if a schema call ever fails with `object_not_found` while page writes succeed, the database is
not the one the skill created.** Check the id above before concluding anything is broken.

**A new repo joins a cycle.** `Repos` is a multi-select, and setting an option that does not exist
fails the *whole* `update_properties` call with `validation_error`. Because the skill owns the schema,
the fix is automatic — add the option, then retry:
```
mcp__notion__notion-update-data-source
  data_source_id: collection://8ef91e3a-d35c-44d2-91ba-9c895b545dbe
  statements: ALTER COLUMN "Repos" SET MULTI_SELECT('fio':blue, 'ripley':purple, '<new>':green)
```
If that ever fails, fall back to mirroring **without** `Repos` and say which option is missing. Never
let a select option abort a mirror — the body is the point, the property is a convenience.

**5b. Annex pages, same write path — and in the same pass.** Any topic with an `Annex:` line has a
local sidecar that is its source of truth (CYC-16), and its page is regenerated from that file
whenever `mirror plan` lists it:

```bash
python3 scripts/cycle.py annex list                    # coverage; is anything missing or a stub?
python3 scripts/cycle.py annex render --json           # {"label", "url", "body"} per annex
```

`mirror plan --json` already carries the same body and url for every stale annex, so in a normal
mirror there is nothing extra to run — this is the command to reach for when inspecting one annex on
its own. Write each one with `replace_content` to the `url` the sidecar's `Annex:` line carries. The body
already contains the backlink to the cycle page — derived from `mirror.json`, never typed, because
the first hand-written annex pointed at the wrong page and nothing could tell.

`annex render` **refuses while any section is still a stub.** That is not an obstacle to work around:
the structure is generated, the write-up is not (CYC-14). Write it, then render.

Annexes are **never reconciled**. They have no writable surface, so a Notion-side edit to one is lost
on the next render — which the page says on itself. Nothing to merge, nothing to lose.

**6. Record the snapshot — always, and only for the pages whose write actually succeeded:**
```bash
python3 scripts/cycle.py mirrored --wrote cycle --wrote "<annex label>"
python3 scripts/cycle.py mirrored                    # every page, when the whole mirror went through
```
This records the cycle page's snapshot — the merge base for the next reconcile — and one snapshot per
annex, which is what makes "is the annex stale?" answerable without fetching Notion. It is what makes
the next read a three-way merge rather than a guess: without a current snapshot, a task unticked in
Notion is indistinguishable from one that was never ticked, and one side wins silently.

**Name the pages you wrote when you did not write all of them.** A snapshot is a claim that Notion now
says this, and recording one for a page that was never written is how a stale annex passes for fresh:
on 2026-08-28 a `jira sync` moved PROD-4357 to `Doing`, the cycle page was written, the annex was not,
and bare `mirrored` snapshotted both — after which nothing in the system could see the drift. A page
left out of `--wrote` keeps its old snapshot, so it stays stale and every later command says so.
`mirrored` with no `--wrote` still records everything, and now says out loud that it is doing so.

**7. Report** what was written and where.

## Reading it back

Every flow starts here, because the maintainer may have ticked things off since the last mirror.

```bash
# fetch the page, save the body, then:
python3 scripts/cycle.py reconcile --from /tmp/fetched.md
```

What it does, and deliberately does not do:

- **Three-way merge** against `.state/<id>.mirror.md`. Their side and the local side are each compared
  to that snapshot, so a change on one side applies and a change on neither is left alone.
- **Never deletes.** A task missing from Notion is reported and left in place. Removing the
  maintainer's work automatically is never the right default.
- **Re-validates** the merged doc, and refuses to commit if it no longer conforms.
- **Stops with nothing written on a collision.** In practice the only real collision is the same task
  renamed on both sides: a *checked-state* collision cannot happen, because two sides moving a boolean
  off the snapshot necessarily move it to the same value.
- **Ignores everything outside the writable surface**, and says what it ignored.
- **Undoes Notion's own rewrites first.** Notion autolinks anything domain-shaped on the way out, so
  a task mentioning `docs/observability/gtm.md` comes back as
  `docs/observability/[gtm.md](http://gtm.md)`. Left alone, `difflib` matches that at >0.8 and
  reconcile applies it as a **retitle** — writing the autolink into the local doc as the task's real
  text. `unautolink()` unwraps a link only where the URL is the link text with a scheme bolted on,
  which is the autolink signature; a link the maintainer typed themselves survives. It also
  un-escapes the brackets Notion adds (`\[fio\]`). Any new Notion-side rewrite belongs here, not in
  the merge.

On success it commits as `<id>: reconciled from Notion (N change(s))`, so the history still records
work that arrived from the other direction.

## Never

- **Never a row below cycle level.** A cycle may be a row; a topic, scope or task may not, and none of
  them may carry Notion properties. The cheat sheet's v2.0.0 reversal is the precedent — one row per
  atom turns a readable page into a tracker — and the cycle row is the one exception that survives it
  (CYC-10 v1.4.0), because a cycle is bounded and substantial where a finding is neither.
- **Never read the mirror back** into the local file as an update path.
- **Never write without a yes.** Not because the gates passed, not because it's "just a refresh".
- **Never mirror a closed cycle again** except once at close, to publish the final state.
