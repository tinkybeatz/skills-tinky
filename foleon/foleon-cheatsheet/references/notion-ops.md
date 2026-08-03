# Notion operations

Live targets:

- database `8020892f438f470eac8ad5da4c11809e`
- data source `collection://a7b041f4-7add-41e8-9ead-5fc6c62d6815`

Requires the Notion MCP. If a call fails on connection, **stop and report** —
never fall back to writing the row somewhere else.

## 1. Dedupe query — always before a write (CHS-11)

The API filters on **properties only**; page-body text is not searchable. That is
why `Dedupe key` is a property, and why this step cannot be skipped.

```
mcp__notion__notion-query-data-sources
  data_source_url: collection://a7b041f4-7add-41e8-9ead-5fc6c62d6815
  filter on "Dedupe key" equals "<key from row.py key>"
```

If `equals` returns nothing, try a `contains` pass on the distinctive stem of the
symptom slug (e.g. `card-content-rounds`) to catch a near-duplicate someone
phrased differently. Two cheap queries beat one duplicate row.

**Outcomes**

- **Exact match** → update that row (step 3). Never create.
- **Near match** → prefer updating, and improve the existing `Symptom` if the new phrasing scans better. Two rows for one symptom is the failure this system exists to prevent.
- **No match** → create (step 2).

If the query did not run — for any reason — **do not write**. Fail closed.

## 2. Create

```
mcp__notion__notion-create-pages
  parent: {"type": "data_source_id",
           "data_source_id": "a7b041f4-7add-41e8-9ead-5fc6c62d6815"}
  pages: [{
    "properties": {
      "Symptom": "...",
      "Area": "Core / rendering",
      "Fix": "...",
      "Why": "...",                        // omit entirely if unknown
      "Refs": "...",
      "date:Verified on:start": "YYYY-MM-DD",
      "Status": "Needs review",            // never anything else
      "Dedupe key": "area-slug:symptom-slug"
    }
  }]
```

Notes that will bite otherwise:

- The date property is written as **`date:Verified on:start`**, not `Verified on`.
- `Status` is a `select` (not Notion's `status` type — it cannot be API-provisioned with custom options; see CHS-10).
- Leave the page **body empty** unless the fix genuinely needs a long command sequence, in which case the body holds it and `Fix` holds a ≤40-word summary (the one standing CHS-6 exception).
- Do **not** set `ID` — it is system-generated and immutable.

The response returns `userDefined:ID` (e.g. `CS-7`). Keep it for step 4.

## 3. Update an existing row

```
mcp__notion__notion-update-page
  page_id: <the matched row>
  command: update_properties
  properties: {
    "Fix": "...",                          // only if the new one is better
    "date:Verified on:start": "YYYY-MM-DD" // always refresh on a re-verify
  }
```

Rules: refresh `Verified on` on every confirming touch — that is what keeps the
`Stale` view honest. Never change `Status` to `Approved`. If the row is already
`Approved`, the only permitted edit is `Verified on` plus a genuine correction.

## 4. Cross-link back into the log (PCS-11)

Edit the log entry's `sheet:` field in
`foleon/foleon-ripley/references/knowledge.md`:

```
- 2026-08-03 · Core / rendering · Card content rounds with the card — … · refs: … · sheet: CS-3
```

For a rejected finding write `sheet: none`, so a later sync doesn't re-litigate
it. This is the mechanism that keeps the two artifacts pointing at each other
instead of duplicating each other.

**Never write into the ripley checkout** (PCS-7). The log lives in
`skills-tinky`. If a path you're about to write resolves inside ripley, stop.

## 5. Reading the surface

```
mcp__notion__notion-query-database-view
  view_url: https://app.notion.com/p/8020892f438f470eac8ad5da4c11809e?v=<view-id>
```

| View | id (dashless) |
|---|---|
| Lookup | `3b1e7f9407e7812f819b000cea854f44` |
| Review queue | `3b1e7f9407e7819fa39c000c3b18ab31` |
| Stale | `3b1e7f9407e781e0a7a1000caddceb4d` |

Use **Review queue** to check what is already pending before adding more, and
**Stale** for the quarterly sweep.

> **Unverified:** the `Stale` view filters a boolean formula compared as the text
> `"true"`. It returns empty today because nothing is 90 days old yet — which is
> also what a broken filter returns. Confirm it once by temporarily back-dating an
> approved row before trusting it.
