---
name: foleon-cheatsheet
description: >-
  Moves genuinely useful Foleon / ripley findings from Claude's discoveries log
  onto the maintainer's own Notion cheat-sheet page — one short bullet per
  fact, under an existing heading, proposed in conversation and written only
  after an explicit yes. No database, no new page per finding: everything
  lands on the one page the maintainer already wrote for themselves. Use
  whenever: a finding was just appended to `foleon-ripley`'s `knowledge.md`; a
  hook reports pending findings at session start or as a turn ends; the queue
  needs draining. Trigger phrases: "sync the Foleon cheat sheet", "update the
  Foleon cheat sheet", "add this to the Foleon cheat sheet", "my Foleon cheat
  sheet", "drain the cheatsheet queue", or explicit `/foleon-cheatsheet`.
  Requires the Notion MCP. Enforces `docs/stds/CHEAT_SHEET.md` v2.1.0: most
  findings are correctly REJECTED, a bullet is rewritten never copied, nothing
  is written to Notion without the maintainer's explicit go-ahead in that same
  conversation, and it never creates a new page or database row. Do NOT use it
  for the skills-tinky README skills cheat-sheet — that is `./generate-catalog.sh`.
  Do NOT use it to capture a conversation into an arbitrary Notion page — that
  is `notion-knowledge-capture`. Do NOT use it to record project facts or
  conventions — that is `foleon-ripley`.
user-invokable: true
---

# foleon-cheatsheet

The bridge between two artifacts with opposite goals. **`knowledge.md`** is Claude's working memory:
dense, complete, never pruned. **The Foleon cheat sheet** — one Notion page — is the maintainer's own
lookup surface: short, scannable, aggressively filtered. This skill carries findings across that gap,
rejects most of them on the way, and **never writes anything without the maintainer's explicit
approval in the conversation itself.**

Governed by [`docs/stds/CHEAT_SHEET.md`](../../docs/stds/CHEAT_SHEET.md) v2.1.0 and
[PCS-6 / PCS-11](../../docs/stds/PROJECT_CONTEXT_SKILL.md) v2.0.0. The standards win any disagreement
with this file.

> **Two corrections, both from direct maintainer pushback — read both before touching this skill.**
>
> **v2.0.0:** an earlier version of this skill wrote a Notion *database*, one
> row per finding. Every database row is a page, so that produced a new page per finding — the
> maintainer's own words: *"this is not a cheat-sheet, it's a document with 10000 of infos."* Worse, 13
> of the first 18 rows duplicated a bullet already on the maintainer's hand-written page, because
> nothing had ever checked the finding against that page's actual content. The database is gone. There
> is now exactly **one target: the page itself.**
>
> **v2.1.0:** the first version of CHS-6 set a hard **~35-word cap** and treated a fenced code block as
> a rare exception. Also rejected: *"35 words threshold is bullshit... it also needs to be able to
> contain commands/code snippets."* Correct — an entry needing a "how to use it" clause or a snippet is
> normal, not a violation. **There is no length cap now.** The only fixed requirement is that the lead
> phrase alone identifies the topic; everything else is judged by whether it's still one fact (CHS-3),
> never by a word count.

## Target

| Thing | Value |
|---|---|
| Page | `Foleon - Cheat Sheet` — `https://app.notion.com/p/3aae7f9407e780df888df6c667a4f4e1` |
| Queue | `hooks/state/cheatsheet-queue.jsonl` (repo-relative) |
| Log | `foleon/foleon-ripley/references/knowledge.md` |
| Local mirror | `foleon/foleon-ripley/references/cheatsheet-approved.md` (generated) |
| Headings on the page (today) | `Commands` · `Packages` · `Conventions` · `Gotchas` · `Playwright gotchas` |

Requires the **Notion MCP**. If a call fails because it is not connected, stop and say so — do not
fall back to writing anywhere else.

## Sync flow

**1. Drain the queue.**
```bash
bash scripts/queue.sh count     # how many pending
bash scripts/queue.sh drain     # prints all entries, then truncates
```
An empty or missing queue is a normal outcome: say "nothing pending" and stop. `drain` prints before
truncating, so a crash between the two loses nothing.

**2. Fetch the page — every time, fresh.** Never reuse a page you fetched earlier in the
conversation; something may have changed. This read is also gate 5 below, not a separate step.

**3. Filter — the five gates (CHS-2).** Every finding must pass **all five**:

1. **Recurrence** — will this plausibly be looked up *again*?
2. **Retrieval cost** — was re-deriving it expensive (~10 min+, or required reading source)?
3. **Non-obviousness** — is it absent from or contradicted by the obvious source? If `package.json`
   or the official docs already say it, it fails.
4. **Actionability** — does it resolve to a *do this*? Pure explanation fails.
5. **Not already said** — read the page you just fetched. Is this fact, or something close enough to
   it, already there? If yes, it fails — even if the wording would be better.

**Most findings fail, and that is correct.** The log keeps everything either way, so rejecting costs
nothing. Report each rejection with the failing gate named. Worked examples, including a real
duplicate-detection case: `references/admission.md`.

**4. Compose one entry (CHS-4/6/7).** Never copy the log's prose — it is written for an agent that
reads everything. Match the page's own style: a **bold lead phrase**, front-loaded, then the fact.
There is **no word cap** (CHS-6, v2.1.0) — add a short "why" / "how to use it" clause or a fenced code
block whenever the fact is genuinely ambiguous or unusable without one. What's fixed is the lead
phrase: it alone must identify the topic, imperative if it's an action, no hedging, no discovery
narrative. Decide which existing heading it belongs under (rarely: propose a new heading, only if
nothing existing fits). Full transform guide with before/after pairs, including a rich
explanation-plus-code example: `references/rewriting.md`.

**5. Validate mechanically.**
```bash
python3 scripts/row.py check --bullet "..."
```
Enforces banned openers and hedge/narrative voice — not length, which is judgement (CHS-6). It'll
nudge, not fail, on very long entries as a check against CHS-3 (still one fact?), never on length alone.

**6. Propose in chat. Wait for an explicit yes.** Show the maintainer the exact bullet and the exact
heading. This **is** the review gate (CHS-9) — there is no Notion-side status field, no review queue,
nothing to configure. A "looks good" is enough; silence or a "no" is not a yes.

- **Yes** → go to step 7.
- **No** → do not write anything. Mark the log entry `sheet: no` so it is not re-proposed. Say so and stop.

**7. Write — one `update_content` call, one bullet.** Insert the new bullet as the last item under
its heading's existing list (search-replace the current last bullet under that heading for
"itself + newline + new bullet" — never `replace_content` on the whole page). Exact call shape:
`references/notion-ops.md`.

**8. Cross-link and refresh the mirror.** Mark the log entry `sheet: yes`. Regenerate
`cheatsheet-approved.md` from the page's current content (a plain copy — see PCS-11 read-back).

**9. Report.** Per finding: admitted or rejected (with the gate), and if admitted, what was written
and where. Then the queue is empty.

## The log has its own dedupe script

Unrelated to the mirror, but the same PCS-6 requirement — search before appending to `knowledge.md`:
```bash
python3 scripts/log.py check --area "Tests & Playwright" --symptom "..."
python3 scripts/log.py lint     # verify the whole log against the schema
```

## Boundaries

- **Never write to Notion without an explicit yes in that conversation.** Not "the gates passed," not
  "this seems obviously good" — a yes, from the maintainer, on the exact wording shown.
- **Never create a new page, a new heading without saying so first, or anything resembling a database.**
  If you find yourself about to call a database- or page-creation tool for this skill, stop — that is
  the exact mistake v2.0.0 exists to prevent.
- **Never write into the ripley checkout** (PCS-7). Everything lands in `skills-tinky` or the one
  Notion page.
- **Never delete a log entry.** The log is authoritative and append-only; a decline only means "not on
  the page."
- **One mirror only** (PCS-11). If asked to also push to another surface, decline and point at the standard.

## References

| File | Read when |
|---|---|
| `references/admission.md` | Applying the five gates — worked examples, including the v1.x duplication failure |
| `references/rewriting.md` | Turning log prose into one bullet — before/after pairs, choosing a heading |
| `references/notion-ops.md` | The exact fetch → propose → insert → mirror call sequence |

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Notion MCP unavailable | An MCP call errors on connection | Stop and report. Leave the queue intact — do not drain it, or the findings are lost. |
| Queue drained but nothing written | Findings in context, nothing on the page | Re-append them with `scripts/queue.sh restore` before ending the turn. |
| Wrote without a yes | A bullet appears that was never explicitly approved | This is the single worst failure this skill can produce. Revert the edit, apologize plainly, do not repeat the pattern. |
| Everything gets proposed | Several bullets proposed from one session | Suspect the gates were applied loosely. Re-read `references/admission.md` — a high proposal rate is the classic failure. |
| Duplicated an existing bullet | The maintainer points out it's already on the page | Gate 5 was skipped or the page wasn't freshly fetched. Always re-fetch immediately before proposing. |
| Truncated a genuinely useful explanation or dropped a needed command | An entry that's technically true but unusable without more context | There is no length cap (CHS-6, v2.1.0). Add the "why"/"how to use it" clause or the code block back — don't cut something true just to seem terse. |
| Copied the log's wording | Bullet reads dense, multi-clause, jargon-narrated | Rewrite per CHS-1. A bullet that matches its log entry violates the standard. |
| Tempted to build a database/status field "for tidiness" | Any urge to add structure beyond one bullet under one heading | Don't. That is exactly how this skill ended up wrong the first time. Re-read the v2.0.0 note above. |
| Heading doesn't fit | Finding spans two headings | Split into two bullets, or ask before inventing a new heading — don't force it under the closest existing one. |
