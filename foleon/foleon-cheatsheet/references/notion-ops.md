# Notion operations

Target: **a bare hub → one project page per project → a small, fixed set of category child pages.**
No database, ever. Category pages are titled `<Project> - <Category>` even though nesting already
disambiguates them (CHS-9a) — nesting helps browsing, the prefix helps Notion's search/quick-open,
which shows titles but not nesting paths.

Hub: `Foleon - Cheat Sheet` — `https://app.notion.com/p/3aae7f9407e780df888df6c667a4f4e1`
Project pages (as of the last check — **always re-fetch the hub to get the real, current list**):
`Ripley`; `Fio` once its first fact is admitted (it is not created in advance — CHS-8).
`Ripley`'s category pages: `Ripley - Commands` · `Ripley - Packages` · `Ripley - Conventions` ·
`Ripley - Gotchas` · `Ripley - Debugging`. Fio's are `Fio - <Category>`, created one at a time.
An optional single `Foleon - Shared` page holds facts true of several projects (CHS-9b).

Requires the Notion MCP. If a call fails on connection, **stop and report** — never fall back to
writing the fact somewhere else.

## 1. Fetch the hub → the project page → the target category page — always fresh

```
mcp__notion__notion-fetch
  id: 3aae7f94-07e7-80df-888d-f6c667a4f4e1        # the hub — gives the current project-page list
```

Read the hub's `<page url="...">Title</page>` entries to find the project this finding belongs to.
**The project comes from the queue entry's `project` field** (or from which log the finding was
written to) — never guess it from the content. If the fact holds for several projects, apply CHS-9b:
write it once, under the surfacing project, or on `Foleon - Shared` if it would outlive that project.
Don't hardcode IDs across sessions — they're a snapshot. Then:

```
mcp__notion__notion-fetch
  id: <the project page's id, from the hub>       # gives the current category-page list
```

Read the project page's `<page>` entries the same way to find the right category page. Then:

```
mcp__notion__notion-fetch
  id: <the target category page's id, from the project page>
```

Read the category page's content in full. This last fetch is CHS-2 gate 5 ("not already said") and
CHS-10 (dedupe) at once — there is no property to query, the fetch *is* the check. Never reuse a
fetch from earlier in the conversation; something may have changed since (including your own prior
edit this session).

## 2. Decide the category, the heading, and compose the entry

Deciding the **category** means picking which child page (under the right project) it belongs on —
see `references/rewriting.md` for how. Deciding the **heading** means: a new top-level `##` heading
(the usual case), or a bullet under an existing `##`/`###` sub-heading grouping related facts (e.g.
`Ripley - Commands` → `## Building`). Validate the composed entry with
`python3 scripts/row.py check --bullet "..."` before moving on.

## 3. Propose in chat — this is the review gate (CHS-9)

Show the maintainer, verbatim: which project, which category page, which heading (new or existing),
and the exact entry text (title + body + any code block). Wait for an explicit yes. There is no
Notion-side approval step to fall back on if this is skipped — skipping it means writing something
the maintainer never agreed to, which is the single worst outcome this skill can produce.

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

## 5. A genuinely new category page (rare — see CHS-8/CHS-9a)

This is one of the two cases where creating a new Notion page is correct, and it is **not** the v1.x
mistake: a page per bounded *category* (a handful, fixed, chosen deliberately) is fine; a page per
*finding* (unbounded, one per fact) is what's forbidden. Only do this when nothing on the target
project's current category-page list fits, and only after the maintainer has explicitly agreed to
the **new category itself** — not just to the finding.

```
mcp__notion__notion-create-pages
  parent: {"type": "page_id", "page_id": "<the PROJECT page's id, not the hub's>"}
  pages: [{"properties": {"title": "<Project> - <Category name>"}, "icon": "<an emoji>", "content": "<first entry>"}]
```

Title it `<Project> - <Category>` even though it's nested — CHS-9a requires the prefix regardless.
Then add a `<page url="...">Title</page>` line to the **project page's** content (via
`update_content`, appending after its last existing `<page>` line) so it's linked and discoverable —
a category page that exists but isn't linked from its project page is just as bad as not creating it.

## 6. A genuinely new project page (rarer still — see CHS-9a)

Same principle, one level up: only when a finding belongs to a Foleon project that has no page yet
(i.e. a new project-context skill was created), and only after the maintainer agrees to the new
project itself.

```
mcp__notion__notion-create-pages
  parent: {"type": "page_id", "page_id": "3aae7f94-07e7-80df-888d-f6c667a4f4e1"}   # the hub
  pages: [{"properties": {"title": "<Project name>"}, "icon": "<an emoji>", "content": "<short intro>"}]
```

Then add a `<page url="...">Title</page>` line to the **hub's** content. The hub must stay a bare
index — one line per project, nothing else. Never add a project's categories as siblings at the hub
level; they belong under the project page, per step 5.

## 7. Cross-link and refresh the local mirror

- Edit the log entry's `sheet:` field in **that project's own log** —
  `foleon/foleon-ripley/references/knowledge.md` or `foleon/foleon-fio/references/knowledge.md`:
  `sheet: yes` on a write, `sheet: no` on a decline. Never write into the served repo's checkout
  (PCS-7, both classes) — the logs live in `skills-tinky`. A shared-page write is marked in the log
  that surfaced it only; the other project's log is not back-annotated (CHS-9b).
- Regenerate **that project's** `cheatsheet-approved.md`: fetch the hub, then that project page, then
  **each** of its category pages, and concatenate them under matching section headers into the one
  local file — verbatim, no rewriting, since everything on them already went through conversational
  approval. This keeps Claude's side as "read one file" even though the human side is split across
  several. Each project's file holds **only its own** pages: mixing them would put one project's facts
  in front of every task in the other (PCS-11).

## Failure to avoid

Do not, under any circumstance for this skill, call `notion-create-database`, `notion-create-pages`
with a `data_source_id` parent, or create a page for an individual finding. A new page is only ever
for a whole new **category** or a whole new **project**, both approved as such and both staying rare
— the category-page count per project should still read as "a handful," same as CHS-8 always
required. If a task seems to need a page per finding, that's the signal to stop and re-read
`docs/stds/CHEAT_SHEET.md` CHS-5 — the whole point of v2.0.0 is that this skill never does that again.
