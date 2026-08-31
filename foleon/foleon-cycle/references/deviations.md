# Divergences — what the ticket's comments say the build actually did

Governed by **CYC-19**. Read this when a ticket has picked up a comment, when `jira sync` reports
unread comments, or before writing anything into an annex's `As built` slot.

## The problem it solves

The annex is a **proposal**, written before the code existed. Sometimes the build disproves it: a
constraint turns out unnecessary, one turns out wrong about the repo, a stated reason turns out to be
already out of date. That is the most valuable feedback the cycle produces, and it arrives in the
worst possible place — a Jira comment, read once, by one person.

Nothing acts on it there. The write-up still says what it said, so the **next** ticket copies the
stale constraint, and the criteria a reviewer checks still name a mechanism nobody built.

## The one rule that is not negotiable

**A comment is never mirrored.** It is *reduced*.

Pasting the thread under the write-up would fail twice over. The annex has a hard budget — roughly ten
lines per ticket — and an unread page is worth less than no page. And a comment is prose written to a
reviewer: it argues, it apologises, it thanks someone. What the plan can act on is a much smaller
thing, and it is the only thing that goes in the file.

So an entry is three fixed parts, and `validate` enforces all three:

```
- **dropped** · Hold events fired before GTM loads and release them once it is up — no queue was
  built. The dataLayer is a plain array the container drains on load, so an event pushed before the
  script arrives already reaches GTM; the constraint's purpose holds without a holding mechanism.
```

| Part | What it is |
|---|---|
| **verdict** | `dropped`, `changed` or `stale` — nothing else |
| **anchor** | the write-up line this contradicts, quoted closely enough to find. Checked to exist |
| **note** | what actually happened, and what it changes |

## The three verdicts

| Verdict | Means | The next reader's question it answers |
|---|---|---|
| `dropped` | the constraint was unnecessary, and nothing replaced it | *can I stop doing this?* — yes |
| `changed` | the constraint was replaced by a different one | *what do I do instead?* |
| `stale` | the instruction stands; the **reason** given for it was wrong | *is this still load-bearing?* — yes, for a different reason |

`stale` is the one people leave out, and it is the one that costs most later. A constraint kept for a
reason that has since evaporated is indistinguishable, on the page, from one that is still earning its
place — right up until someone deletes it.

## Why the anchor is checked

Because without it the slot becomes a comment thread with extra steps.

An entry that names no line is filed by **date**, and nobody reads a ticket by date. An entry anchored
on a constraint is found by whoever opens that constraint, which is exactly the person about to repeat
the mistake. `deviations add` refuses an anchor it cannot find in the section, and says what that
means: if the write-up never said it, this is not a divergence — it is a new fact, and it belongs in
the ticket or in the project skill's `knowledge.md`.

An anchor may not contain an em dash; that is what separates it from the note. Quote a shorter run.

## The two commands, and why they are two

```bash
python3 scripts/cycle.py deviations list                    # recorded, and not yet decided about
python3 scripts/cycle.py deviations sync --from <file>      # ingest comments you fetched
python3 scripts/cycle.py deviations add --key PROD-1234 --verdict changed \
        --anchor "<the line it contradicts>" --note "<what actually happened>" --comment <id>
python3 scripts/cycle.py deviations dismiss --key PROD-1234 --comment <id> --why "<one clause>"
```

**`sync`** is mechanical: it reads a payload into a local store and touches nothing anyone wrote.
**`add`** is the moment someone asserts *this comment means that constraint was wrong* — a claim about
the plan, not a transcription. Nothing infers the second from the first, for the same reason
`jira link` never infers which task a key belongs to: a model reading a thread and rewriting the plan
from it is confident and wrong in exactly the cases that matter.

**Propose the reduction and wait for a yes.** The comment is the maintainer's prose; the entry is your
claim about their plan.

### Fetching

`cycle.py` has no network access, here as everywhere (CYC-18). Fetch the comments yourself —
`getJiraIssue` with the **comment** field; an issue fetched for summary and status carries none — save
the payload, then point `sync` at it. It accepts Jira's nested shape verbatim, ADF bodies included, as
well as a flat `{"key": …, "comments": [{"id", "author", "created", "body"}]}`.

Reading comments is a read. **Replying to one is a write, and is not on offer** — the ban in
[`jira.md`](jira.md) covers comments by name.

### Dismissing is the normal outcome

Most comments carry nothing for the plan: a question, an acknowledgement, a link. Dismiss them, with
one clause saying why. Without that step every comment is reported for ever, which is how an inbox
stops being read — and `--why` is required so that a silent mass-dismissal cannot look like an empty
inbox afterwards.

## Where it lands

The entry goes in the annex sidecar, in the section for that ticket, under a final `**As built**`
slot — after the whole proposal, never edited into it. The write-up **body is never rewritten**: the
proposal is what was agreed at the time, and a plan silently edited to match what happened teaches
nothing at close.

In Notion it renders as a yellow callout at the foot of the section. Yellow because the workspace
mapping (NST-3) already gives yellow to *read this before trusting the block above*, which is
precisely what a divergence is.

## The two places it must also go

1. **`knowledge.md`, when the fact outlives the cycle.** The gate that was wrong because
   `VITE_APP_ENV` is only set by the staging deploy workflow is a fact about the repo, true next
   cycle and the one after. The cycle doc is archived within weeks (CYC-12), so a fact parked only
   here is a fact lost. `deviations add` prints the reminder; routing it is yours.
2. **The retro.** `cycle.py close` lists every recorded divergence. It is shaping feedback of the same
   kind as a scope that never reached downhill, arriving from the other end: the first says the work
   was under-shaped, the second says it was **mis**-shaped, confidently and in writing.

## Failure modes

| Failure | Signal | Recovery |
|---|---|---|
| Pasted the comment | An `As built` line that is a paragraph of prose | `validate` rejects it. Reduce it: verdict, anchor, note. If it reduces to nothing, it was a dismissal. |
| Anchored on nothing | `add` refuses; or an entry quoting a line that is not in the section | The write-up never said it, so it is not a divergence. It is a new fact — ticket, or `knowledge.md`. |
| Recorded without asking | An entry the maintainer never agreed to | Their comment is prose; your entry is a claim about their plan. Propose, then write. |
| Rewrote the write-up to match the build | A constraint edited or deleted instead of an entry added | Restore it. The proposal is the record of what was agreed; edited to match the outcome it can no longer be wrong, and the retro reads nothing. |
| Replied in Jira | A comment posted by this skill | The worst failure in this file — see CYC-18. Say so immediately and name exactly what was written. |
| Left every comment unread | `UNREAD TICKET COMMENTS` on every command, for weeks | Dismiss the conversation. The report is only useful while it is short. |
| Durable fact left in the annex | A repo-level gotcha recorded only as a divergence | Also route it to the project skill's `knowledge.md` (CYC-12). The annex is archived with the cycle. |
