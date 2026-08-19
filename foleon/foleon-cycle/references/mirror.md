# Mirror — the Notion page

The mirror exists so the plan is readable without opening a terminal. It is **derived, one-way, and
one page per cycle** (CYC-10). Requires the Notion MCP; if a call fails on connection, say so and stop
— the local file is already authoritative, so there is nothing to fall back to and nothing at risk.

## Shape

```
Foleon - Cycles                 ← hub, a bare index: one line per cycle (never a database)
├── Cycle 2026-C4               ← one page per cycle
│   ├── ## fio                  ← section per repo (CYC-9)
│   │   ### PDF export          ← topic, with its shaped fields
│   └── ## ripley
└── Cycle 2026-C3  (closed)
```

Page ids live in `<cycle home>/.state/mirror.json`:

```json
{"hub": {"id": "...", "url": "..."}, "cycles": {"2026-C4": {"id": "..."}}}
```

Read it before mirroring; write it after creating a page. If the hub doesn't exist yet, **ask where it
should live** (which Notion parent) and create it on the first mirror — never guess a parent, and never
pre-create cycle pages for cycles that haven't started (the cheat sheet's CHS-8 lesson: an empty page
is clutter, not structure).

## What the page carries

| Include | Leave local |
|---|---|
| Header: cycle id, dates, status | — |
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

**3. Render the whole page** from the local file. Whole-page regeneration is the only write path —
never patch a line, never diff. (Note the deliberate contrast with `foleon-cheatsheet`, which appends
one bullet and is forbidden from replacing a page: there, the page is hand-authored and the skill is a
guest; here, the page is *generated output* and the local file is the author.)

**4. Propose. Wait for an explicit yes.** Show the rendered content and the exact target page. A
"looks good" is a yes; silence is not (CYC-11). On a no: write nothing.

**5. Write.**
```
mcp__notion__notion-update-page
  data: { page_id: <id>, command: "replace_content", new_str: "<rendered markdown>" }
```
For a brand-new cycle page, `mcp__notion__notion-create-pages` with the hub as parent, then record the
new id in `<cycle home>/.state/mirror.json`.

**6. Report** what was written and where.

## Never

- **Never a database.** No topic-as-row, no scope-as-row, no Notion properties for status, hill, or
  appetite. That mistake cost the cheat sheet a full architecture reversal (CHS v2.0.0) — the reasoning
  transfers exactly: a row is a page, and one page per unit of work is the thing being avoided.
- **Never read the mirror back** into the local file as an update path.
- **Never write without a yes.** Not because the gates passed, not because it's "just a refresh".
- **Never mirror a closed cycle again** except once at close, to publish the final state.
