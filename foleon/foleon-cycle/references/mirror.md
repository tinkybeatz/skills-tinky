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
│     ## fio
│     ### PDF export          ← topic, with its shaped fields
│     ## ripley
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
| a task's checked state | topic fields (outcome, no-gos, done when) |
| a task's text | appetite, topic state (`shaping`/`shaped`) |
| new task lines under an existing scope | **hill positions**, scopes themselves, the dev log |

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
in the board instead, which is derived output nothing reads back.

## Sequence

**1. Validate first.** `python3 scripts/cycle.py validate` — never mirror a non-conforming doc, or the
malformation gets a second home.

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

**4. Propose. Wait for an explicit yes.** Show the rendered content and the exact target page. A
"looks good" is a yes; silence is not (CYC-11). On a no: write nothing.

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

**6. Record the snapshot — always, and only after the write succeeded:**
```bash
python3 scripts/cycle.py mirrored
```
This is what makes the next read a three-way merge rather than a guess. Without a current snapshot,
a task unticked in Notion is indistinguishable from one that was never ticked, and one side wins
silently.

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
