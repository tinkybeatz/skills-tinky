# Mirror — the Notion page

The mirror exists so the plan is readable without opening a terminal. It is **derived, one-way, and
one page per cycle** (CYC-10). Requires the Notion MCP; if a call fails on connection, say so and stop
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

| Include | Leave local |
|---|---|
| Repo sections, one per repo the cycle touches | The header line — `Dates` and `Status` are row **properties**; writing them in the body too creates two truths in one page |
| Every topic with all its shaped fields | — |
| Every scope with its hill position and done/not-done | Individual task checkboxes, when a scope has more than a handful |
| Open questions | — |
| The dev log | — |

Scope-level is the reportable unit: Shape Up's point is that status conversations work better pointing
at finished slices than defending individual outstanding tasks. Mirroring 40 checkboxes recreates
exactly the weeds the hill was adopted to escape.

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

**6. Report** what was written and where.

## Never

- **Never a row below cycle level.** A cycle may be a row; a topic, scope or task may not, and none of
  them may carry Notion properties. The cheat sheet's v2.0.0 reversal is the precedent — one row per
  atom turns a readable page into a tracker — and the cycle row is the one exception that survives it
  (CYC-10 v1.4.0), because a cycle is bounded and substantial where a finding is neither.
- **Never read the mirror back** into the local file as an update path.
- **Never write without a yes.** Not because the gates passed, not because it's "just a refresh".
- **Never mirror a closed cycle again** except once at close, to publish the final state.
