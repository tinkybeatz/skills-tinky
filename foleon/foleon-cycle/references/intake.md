# Intake — interviewing a topic into shape

Shaping, done solo with an assistant. The output is a **shaped topic**: six fields filled, rabbit
holes named, scopes drafted. Governed by CYC-3.

The failure this exists to prevent has a name in Shape Up: the "2.0" grab-bag — *"the project turned
out to be a mess because we didn't know what 'done' looked like."* Every question below is aimed at
that.

## Phase 0 — parse, then confirm

Read the pasted cycle description and extract candidate topics with their estimates. **Show the parse
and stop.** No questions yet.

```
I read 3 topics:
  1. PDF export — 2w — [fio?]
  2. Search relevance — 3d — [ripley?]
  3. "Editor polish" — 1w — [?]  ← this reads like a grab-bag, not a topic
Right? Anything mis-split, or an estimate I got wrong?
```

Flag a grab-bag when you see one (a "2.0", a "polish", an "improve X"). It is not a topic yet, and
the honest move is to say so at parse time rather than to interview it as if it were one.

## Phase 1 — the interview

**Batch with `AskUserQuestion`, four at a time.** One-at-a-time questioning is what turns shaping
into an interrogation, and it is the single most likely reason the maintainer stops using this skill.

### Depth ladder

| Appetite | Ask |
|---|---|
| ≤ 2 days | outcome, no-gos, done signal. Stop. |
| 3 days – 1 week | + first cut, rabbit holes |
| > 1 week | all of it, including precedent and dependencies |

Asking eight questions about a two-day topic is how a system like this gets abandoned in week three.

### Question bank, in priority order

1. **Outcome** — "When this ships, what's observably different for a user?" One sentence, visible from
   outside the code. Reject a restatement of the title; reject a technical task. If it can't be
   written, the topic isn't shaped — say that plainly.
2. **Appetite** — "The 2w you were given: is that fixed, or a guess?" Either way it is recorded
   `(fixed)`: an appetite is a *budget*, and the number's origin doesn't change how it functions.
3. **First cut** — "At 80% of the time with 60% done, what goes first?" The most valuable answer in
   the doc and the one nobody writes down. It must be a named piece of the topic — not "polish", not
   "tests".
4. **No-gos** — "What's explicitly out?" Gives scope creep something to bounce off.
5. **Rabbit holes** — "Which part don't you know how to do yet?" Each answer becomes a scope at
   `uphill` or an open question. This is the question that de-risks the cycle.
6. **Repo** — "fio, ripley, or both?" Determines the tag, and which context skill loads during the
   work.
7. **Ripley precedent** — for a `fio` topic: "Does ripley already do this?" `fio`'s own `CLAUDE.md`
   says to consult ripley for *what should this behaviour be* — so ask it here once instead of
   rediscovering it mid-implementation.
8. **Done signal** — "Merged? Deployed? Demoed to whom?" A named event, never a percentage, never
   "when it works".
9. **Blocked on anyone** — design, API, another dev. A dependency discovered in week three was
   usually knowable in week one.

### Recording answers

- Every answer goes in **the maintainer's words**, compressed but not reinterpreted.
- **Every non-answer goes under `Open questions:` verbatim.** Not a guess, not your proposal restated
  as agreement. This is CYC-3 and it is the rule that keeps the doc trustworthy: three weeks later,
  nothing in the file should be indistinguishable from something they actually said.
- If they answer "I don't know yet" to a rabbit-hole question, that *is* an answer — it becomes an
  `uphill` scope.

## Phase 2 — draft the scopes

Propose vertical slices, each independently finishable in a few days or less. Present names as a
**draft** and ask them to rename. Scopes become the language of the work; a name they wouldn't say
out loud is worse than useless.

Sequence the `uphill` scopes first when proposing an order — unknowns are what should be attacked
while there is still time to react to what they reveal.

## Phase 3 — tasks

Only after scope names are accepted. Half a day to two days each, under exactly one scope, must-have
unless marked `~`.

## Worked example

**Pasted:** `PDF export — 2 weeks. Users want to download docs as PDF.`

**Interview yields:**
- Outcome: *A reader can download the doc as a PDF that matches the on-screen layout.*
- Appetite: 2w (fixed) · First cut: *nested-table layout → flatten to single level*
- No-gos: *no print-stylesheet editor, no per-block overrides*
- Done when: *merged to main and demoed to design*
- Rabbit hole: *"no idea how nested tables paginate"* → scope `table pagination` at `uphill`
- Repo: fio · Precedent: *"ripley exports, but I don't know if it shares the extraction path"* →
  open question, verbatim

**Result:** three scopes — `extraction pipeline`, `table pagination` (uphill, attacked first),
`UI trigger` — and one open question that a 20-minute look at ripley will answer before it becomes a
week-three surprise.

Note what did *not* happen: nobody guessed whether the extraction path is shared. It went in the doc
as a question, in the maintainer's own words.
