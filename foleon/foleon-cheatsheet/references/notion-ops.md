# Notion operations

Target: **a hub page + a small, fixed set of category child pages.** No database, ever.

Hub: `Foleon - Cheat Sheet` — `https://app.notion.com/p/3aae7f9407e780df888df6c667a4f4e1`
Category pages (as of the last check — **always re-fetch the hub to get the real, current list**):
`Commands` · `Packages` · `Conventions` · `Gotchas` · `Debugging`.

Requires the Notion MCP. If a call fails on connection, **stop and report** — never fall back to
writing the fact somewhere else.

## 1. Fetch the hub, then the target category page — always fresh

```
mcp__notion__notion-fetch
  id: 3aae7f94-07e7-80df-888d-f6c667a4f4e1        # the hub — gives the current category-page list
```

Read the hub's `<page url="...">Title</page>` entries to get each category page's real ID — don't
hardcode the IDs above across sessions, they're a snapshot. Then:

```
mcp__notion__notion-fetch
  id: <the target category page's id, from the hub>
```

Read the category page's content in full. This is CHS-2 gate 5 ("not already said") and CHS-10
(dedupe) at once — there is no property to query, the fetch *is* the check. Never reuse a fetch from
earlier in the conversation; something may have changed since (including your own prior edit this
session).

## 2. Decide the category, the heading, and compose the entry

Deciding the **category** means picking which child page it belongs on — see
`references/rewriting.md` for how. Deciding the **heading** means: a new top-level `##` heading (the
usual case), or a bullet under an existing `##`/`###` sub-heading grouping related facts (e.g.
`Commands` → `## Building`). Validate the composed entry with
`python3 scripts/row.py check --bullet "..."` before moving on.

## 3. Propose in chat — this is the review gate (CHS-9)

Show the maintainer, verbatim: which category page, which heading (new or existing), and the exact
entry text (title + body + any code block). Wait for an explicit yes. There is no Notion-side approval
step to fall back on if this is skipped — skipping it means writing something the maintainer never
agreed to, which is the single worst outcome this skill can produce.

- **No response, a "maybe," or silence is not a yes.**
- **No** → don't write. Mark the log entry `sheet: no`. Say so and stop.

## 4. Write — one targeted edit to the category page, never a full-page replace

```
mcp__notion__notion-update-page
  page_id: <the category page's id>
  command: update_content
  content_updates: [{
    old_str: "<the exact text of the CURRENT last entry on that page — or under that sub-heading>",
    new_str: "<same text>\n<the new heading + body, or the new bullet>"
  }]
```

Use the text you just fetched in step 1 for `old_str`, verbatim — a stale copy from earlier in the
conversation can mismatch and either fail the edit or, worse, match the wrong occurrence. **Never use
`replace_content`** on a category page for this — that rewrites the whole page and risks losing
something added by hand since the last fetch.

## 5. A genuinely new category page (rare — see CHS-8)

This is the one case where creating a new Notion page is correct, and it is **not** the v1.x mistake:
a page per bounded *category* (a handful, fixed, chosen deliberately) is fine; a page per *finding*
(unbounded, one per fact) is what's forbidden. Only do this when nothing on the current category-page
list fits, and only after the maintainer has explicitly agreed to the **new category itself** — not
just to the finding.

```
mcp__notion__notion-create-pages
  parent: {"type": "page_id", "page_id": "3aae7f94-07e7-80df-888d-f6c667a4f4e1"}   # the hub
  pages: [{"properties": {"title": "<Category name>"}, "icon": "<an emoji>", "content": "<first entry>"}]
```

Then add a `<page url="...">Title</page>` line to the **hub's** content (via `update_content`,
appending after the last existing `<page>` line) so it's linked and discoverable — a category page
that exists but isn't linked from the hub is just as bad as not creating it.

## 6. Cross-link and refresh the local mirror

- Edit the log entry's `sheet:` field in `foleon/foleon-ripley/references/knowledge.md`: `sheet: yes`
  on a write, `sheet: no` on a decline. Never write into the ripley checkout (PCS-7) — the log lives
  in `skills-tinky`.
- Regenerate `foleon/foleon-ripley/references/cheatsheet-approved.md`: fetch the hub for the current
  category-page list, fetch **each** category page, and concatenate them under matching section
  headers into the one local file — verbatim, no rewriting, since everything on them already went
  through conversational approval. This keeps Claude's side as "read one file" even though the human
  side is split across several. Refreshed whenever any category page changes.

## Failure to avoid

Do not, under any circumstance for this skill, call `notion-create-database`, `notion-create-pages`
with a `data_source_id` parent, or create a page for an individual finding. A new page is only ever
for a whole new **category**, approved as such, and stays rare — the category-page count should
still read as "a handful," same as CHS-8 always required of headings. If a task seems to need a page
per finding, that's the signal to stop and re-read `docs/stds/CHEAT_SHEET.md` CHS-5 — the whole point
of v2.0.0 is that this skill never does that again.
