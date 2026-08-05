# Notion operations

Target: **one page**, no database.
`Foleon - Cheat Sheet` — `https://app.notion.com/p/3aae7f9407e780df888df6c667a4f4e1`

Requires the Notion MCP. If a call fails on connection, **stop and report** — never fall back to
writing the fact somewhere else.

## 1. Fetch — always fresh, every time

```
mcp__notion__notion-fetch
  id: 3aae7f94-07e7-80df-888d-f6c667a4f4e1
```

Read the returned content in full. This is CHS-2 gate 5 ("not already said") and CHS-10 (dedupe) at
once — there is no property to query, the fetch *is* the check. Never reuse a fetch from earlier in
the conversation; something may have changed since (including your own prior edit this session).

## 2. Decide the heading and compose the bullet

See `references/rewriting.md`. Validate with `python3 scripts/row.py check --bullet "..."` before
moving on.

## 3. Propose in chat — this is the review gate (CHS-9)

Show the maintainer, verbatim, the bullet you're about to write and which heading it goes under.
Wait for an explicit yes. There is no Notion-side approval step to fall back on if this is skipped —
skipping it means writing something the maintainer never agreed to, which is the single worst outcome
this skill can produce.

- **No response, a "maybe," or silence is not a yes.**
- **No** → don't write. Mark the log entry `sheet: no`. Say so and stop.

## 4. Write — one targeted edit, never a full-page replace

```
mcp__notion__notion-update-page
  page_id: 3aae7f9407e780df888df6c667a4f4e1
  command: update_content
  content_updates: [{
    old_str: "<the exact text of the CURRENT last bullet under the target heading>",
    new_str: "<same text>\n<the new bullet>"
  }]
```

Use the text you just fetched in step 1 for `old_str`, verbatim — a stale copy from earlier in the
conversation can mismatch and either fail the edit or, worse, match the wrong occurrence. **Never use
`replace_content`** for this — that rewrites the whole page and risks losing something added by hand
since the last fetch.

If the target is a genuinely new heading (rare — see `references/rewriting.md`), use
`insert_content` with `position: {"type": "end"}` to append the new `## Heading` plus its first
bullet, only after the maintainer has agreed to the new heading specifically, not just the bullet.

## 5. Cross-link and refresh the local mirror

- Edit the log entry's `sheet:` field in `foleon/foleon-ripley/references/knowledge.md`: `sheet: yes`
  on a write, `sheet: no` on a decline. Never write into the ripley checkout (PCS-7) — the log lives
  in `skills-tinky`.
- Regenerate `foleon/foleon-ripley/references/cheatsheet-approved.md`: fetch the page's current full
  content and copy it in — verbatim, no rewriting, since everything on the page already went through
  conversational approval. This is a plain mirror, refreshed whenever the page changes, so `foleon-
  ripley` benefits from what's on the page without needing live Notion access every session.

## Failure to avoid

Do not, under any circumstance for this skill, call `notion-create-database`, `notion-create-pages`
with a `data_source_id` parent, or any tool that would create a new Notion page or database row. If a
task seems to need one, that's the signal to stop and re-read `docs/stds/CHEAT_SHEET.md` CHS-5 — the
whole point of v2.0.0 is that this skill never does that again.
