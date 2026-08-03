---
name: foleon-cheatsheet
description: >-
  Moves Foleon / ripley findings from Claude's discoveries log into the
  human-facing Notion cheat-sheet database — applying the admission filter,
  rewriting each one for a human, deduplicating against what is already there,
  and leaving the row for you to approve. Use whenever: a finding was just
  appended to `foleon-ripley`'s `knowledge.md`; a hook reports pending findings
  at session start or as a turn ends; the queue needs draining; or the
  discoveries log needs migrating to the structured PCS-6 schema. Trigger
  phrases: "sync the Foleon cheat sheet", "update the Foleon cheat sheet",
  "add this to the Foleon cheat sheet", "my Foleon cheat sheet", "drain the
  cheatsheet queue", "migrate the knowledge log", "backfill the cheat sheet",
  or explicit `/foleon-cheatsheet`. Requires the Notion MCP. It enforces
  `docs/stds/CHEAT_SHEET.md`: most findings are correctly REJECTED, rows are
  rewritten never copied, and it never approves its own rows. Do NOT use it for
  the skills-tinky README skills cheat-sheet — that is `./generate-catalog.sh`.
  Do NOT use it to capture a conversation into an arbitrary Notion page — that
  is `notion-knowledge-capture`; this skill moves governed findings into one
  specific database. Do NOT use it to record project facts or conventions —
  that is `foleon-ripley`.
user-invokable: true
---

# foleon-cheatsheet

The bridge between two artifacts with opposite goals. **`knowledge.md`** is
Claude's working memory: dense, complete, never pruned. **The Notion cheat
sheet** is your lookup surface: curated, scannable, aggressively filtered. This
skill carries findings across that gap — and rejects most of them on the way.

Governed by [`docs/stds/CHEAT_SHEET.md`](../../docs/stds/CHEAT_SHEET.md) (CHS-1…CHS-12)
and [PCS-6 / PCS-11](../../docs/stds/PROJECT_CONTEXT_SKILL.md). The standards win any
disagreement with this file; if you find a conflict, fix the standard first.

## Targets

| Thing | Value |
|---|---|
| Notion database | `8020892f438f470eac8ad5da4c11809e` |
| Data source | `collection://a7b041f4-7add-41e8-9ead-5fc6c62d6815` |
| Queue | `hooks/state/cheatsheet-queue.jsonl` (repo-relative) |
| Log | `foleon/foleon-ripley/references/knowledge.md` |
| `Area` values | Editor · Viewer · Core / rendering · Build & tooling · Tests & Playwright · Conventions |
| `Status` values | Needs review · Approved · Archived |

Requires the **Notion MCP**. If a Notion call fails because it is not connected,
stop and say so — do not fall back to writing the row into the log or a file.

## Modes

| Mode | Trigger | What it does |
|---|---|---|
| **Sync** (default) | hook report, or "sync the cheat sheet" | Drain the queue → filter → rewrite → dedupe → write → cross-link |
| **Single** | "add this to the cheat sheet" | Same pipeline for one finding given in conversation, bypassing the queue |
| **Migration** | "migrate the knowledge log" | One-off: restructure `knowledge.md` to PCS-6, then backfill the sheet. See `references/migration.md` |
| **Pull** | "pull the approved rows", after approving a batch | The reverse leg: approved rows → a generated file Claude loads |

## Sync flow

**1. Drain the queue.**
```bash
bash scripts/queue.sh count     # how many pending
bash scripts/queue.sh drain     # prints all entries, then truncates
```
An empty or missing queue is a normal outcome, not an error: say "nothing
pending" and stop. Only truncate after the findings are safely in your context —
`drain` prints before truncating so a crash loses nothing.

**2. Filter — the four gates (CHS-2).** Every finding must pass **all four**:

1. **Recurrence** — will this plausibly be looked up *again*?
2. **Retrieval cost** — was re-deriving it expensive (~10 min+, or required reading source)?
3. **Non-obviousness** — is it absent from or contradicted by the obvious source? If `package.json` or the official docs already say it, it fails.
4. **Actionability** — does it resolve to a *do this*? Pure explanation fails.

**Most findings fail.** That is the design, not an error — the log keeps
everything, so rejecting costs nothing. Report rejections with the failing gate
named. Worked accept/reject examples: `references/admission.md`.

**3. Rewrite for a human (CHS-4/6/7).** Never copy the log's prose — it is
written for an agent that reads everything. Produce:

- **`Symptom`** — what you *observe*, ≤10 words, information-carrying words first. No `Issue with`, `Problem with`, `How to`, `Note about`, `Fix for`, `When you`, or a leading article.
- **`Fix`** — the action, imperative, ≤40 words / ≤3 lines, action in sentence one.
- **`Why`** — one sentence, or **empty** if the cause is unknown. Never speculate.
- **`Refs`** — paths, ticket IDs, links.
- **`Area`** — exactly one of the six.
- **`Verified on`** — today.

Full transform guide with before/after pairs: `references/rewriting.md`.

**4. Validate mechanically — before any write.**
```bash
python3 scripts/row.py check --symptom "..." --fix "..." --why "..."
python3 scripts/row.py key --area "Core / rendering" --symptom "..."
```
`check` enforces the caps, banned openers and hedge words; `key` derives the
canonical `Dedupe key`. Use the script rather than eyeballing — the caps are
numeric and the key must be byte-stable, or dedupe silently breaks.

The log has its own script, for the same reason (PCS-6):
```bash
python3 scripts/log.py check --area "Tests & Playwright" --symptom "..."
python3 scripts/log.py lint     # verify the whole log against the schema
```
`check` exits non-zero when an existing entry is a likely duplicate — extend that
entry and refresh its date instead of appending.

**5. Dedupe — query before you write (CHS-11).** The Notion API **cannot search
page bodies**, only properties, so the key must already be a property. Query the
data source filtering `Dedupe key` `equals` the derived key. If that misses, try
`contains` on the symptom slug's distinctive stem to catch near-duplicates.

- **Match** → update that row (refresh `Fix`/`Why`/`Refs` if better, set `Verified on` to today). Do not create a second row.
- **No match** → create.

**If the query did not run, do not write.** Fail closed and say why. A
duplicate-riddled sheet is worse than a missing row. Exact call shapes:
`references/notion-ops.md`.

**6. Write with `Status = "Needs review"` — always.** Never `Approved`. Promotion
is the maintainer's action alone (CHS-10). This is the whole point of the gate:
they asked for a check on what lands in their own reference material.

**7. Cross-link (PCS-11).** The create call returns `ID` (`CS-14`). Write it back
into the log entry's `sheet:` field so the two artifacts point at each other
instead of restating each other. For a rejected finding, write `sheet: none` so a
later run does not reconsider it from scratch.

**8. Report.** Per finding: admitted or rejected, the gate that failed, the row
ID, and whether it was a create or an update. Then the queue is empty.

## Pull — approved rows back to Claude

Approved rows are the **highest-quality knowledge in the system**: the maintainer personally
verified them, and they are already written to be scanned. Without this leg they serve only the
human, and Claude keeps working from the raw log — which is exactly how a finding ends up on the
cheat sheet but in no Claude-facing file.

1. Query the `Lookup` view (already filtered to `Status = Approved`).
2. Regenerate `foleon/foleon-ripley/references/cheatsheet-approved.md`, grouped by `Area`, one
   line per row: `CS-nn · <Symptom> → <Fix>`, with `Why` and `Refs` appended when present.
3. `foleon-ripley` loads that file as its third context layer.

Rules that keep this safe:

- The file is **generated**. Never hand-edit it — regenerate. Its header says so.
- **Approved only.** `Needs review` rows are not yet trusted and must not reach Claude this way.
- It **replaces nothing**. `project-facts.md` stays the curated stable facts, `knowledge.md` stays
  the authoritative log; this is a third, human-verified layer.
- Rewrite nothing here — the rows are already in their final human form. This leg is a **copy**,
  which is the one place in this system where copying is correct.

Run it after approving a batch. If `Lookup` is empty, write the file's empty state rather than
deleting it, so the mechanism stays visible.

## Boundaries

- **Never write into the ripley checkout** (PCS-7). Everything lands in `skills-tinky` or Notion. If a path resolves inside ripley, stop.
- **Never self-approve** a row, and never edit a row that is already `Approved` except to refresh `Verified on` on a re-verify.
- **Never delete a log entry.** The log is authoritative and append-only; rejection only means "not mirrored".
- **One mirror only** (PCS-11). If asked to also push to another surface, decline and point at the standard.

## References

| File | Read when |
|---|---|
| `references/admission.md` | Applying the four gates — worked accept/reject examples |
| `references/rewriting.md` | Turning log prose into a row — before/after pairs, area mapping |
| `references/notion-ops.md` | The exact MCP call sequence for query / create / update |
| `references/migration.md` | Running the one-off log migration and backfill |

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Notion MCP unavailable | An MCP call errors on connection | Stop and report. Leave the queue intact — do not drain it, or the findings are lost. |
| Queue drained but write failed | Findings in context, nothing in Notion | Re-append them with `scripts/queue.sh restore` before ending the turn. Never end a turn holding undrained findings only in context. |
| Dedupe query skipped | About to create without having queried | Fail closed. Query first; duplicates are the failure this system exists to prevent. |
| Row rejected by `row.py check` | Cap or banned-opener violation | Rewrite tighter. Do not widen the cap or bypass the script — the caps are the standard. |
| Everything gets admitted | Several rows created from one session | Suspect the gates were applied loosely. Re-read `references/admission.md`; a high admit rate is the classic failure of this skill. |
| Copied the log's wording | Row reads dense, multi-clause, jargon-narrated | Rewrite per CHS-1. A row that matches its log entry violates the standard. |
| Duplicate rows appear | Two rows, same symptom | Compare `Dedupe key`s — usually a key-derivation drift. Re-derive both with `row.py key` and merge. |
| `Area` doesn't fit | Finding spans two areas | Pick where you would *look for it*, not where the code lives. If it truly needs a seventh area, that is a standard amendment (CHS-8), not a judgement call. |
| Asked to approve rows | "just approve them for me" | Decline; explain CHS-10. The review gate is the feature they asked for. |
