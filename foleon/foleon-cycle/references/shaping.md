# Shaping — re-evaluating when answers arrive

The flow behind `/foleon-cycle shape`. Governed by CYC-3.

Shape Up assumes a topic is shaped before it is bet on. Here it isn't: the maintainer receives a title
and an estimate, so shaping is the cycle's own first work. That makes this the most-used flow in the
first week or two, and it is a **decision** flow, not a form.

## Step 1 — take the dump, then re-anchor

```bash
python3 scripts/cycle.py questions      # numbered, per topic
```

Ask for whatever came out of the call, however rough. Then map each answer onto a numbered question.
The maintainer should be able to say *"1, 4 and 7 are settled, 3 is a maybe"* — never re-paste the list.

## Step 2 — classify what's left

The only classification that matters:

| | Test |
|---|---|
| **Blocking** | Could you write the outcome sentence, or name the done event, without this answer? If no → blocking. |
| **Non-blocking** | Annoying, discoverable later, or affects a part you could cut. |

Be strict. "It would be nice to know" is not blocking. A topic held hostage to a non-blocking question
is a topic nobody is working on for no reason.

## Step 3 — propose one of three moves

State which, with the reasoning, and **wait for agreement**.

### Hold
Something blocking is still open.

- Name **who** can answer it and **how** it gets asked (a `self:` task, not a hope).
- Judge whether asking again is still the move. Nothing measures how long a topic has been shaping —
  the doc records no date it entered that state, and the maintainer shapes one topic at a time
  (CYC-3, v7.0.0). What counts is the question's own history: once it has survived several attempts
  to get it answered, the honest recommendation is *escalate*, not *research more*.
- Drop the answered questions, log them (`--gate surprise`), keep the rest.

### Split — the usual answer to a partial call
Enough is known for **part** of the topic. A topic is shaped or shaping as a whole, so the way to
express "half of this is knowable" is to make it two topics:

```
## [fio] GTM analytics — plumbing — shaped        Appetite: 1.5w (fixed) · First cut: …
## [fio] GTM analytics — event list — shaping     Appetite: 1.5w (provisional)
```

Rules for a split:
- The **shaped half must be independently shippable**. If it only makes sense once the other half
  lands, it isn't a split — it's one topic still shaping.
- **Divide the appetite**, don't duplicate it. The sum stays what it was; `status` reports the total
  against the 6-week window and flags over-booking.
- The unanswered questions travel with the **shaping** half. The shaped half must have none.
- Name both halves in the maintainer's words. `— plumbing` / `— event list`, not `— phase 1` / `— phase 2`.

This is Shape Up's own move: hammer a big vague topic down to a real bet, and leave the rest for when
it can be shaped.

### Shape
Everything blocking is answered. Run the full topic interview, fill all six fields, flip the heading to
`— shaped`, then go to the plan flow — factor scopes, read the code, propose tasks.

## Step 4 — execute what was agreed

1. Remove answered questions from `Open questions:`.
2. Log each answer that changed something: `log --gate surprise` — an open question closing is exactly
   a surprise, and it is what makes the cycle readable at close.
3. Tick the `self:` research tasks the answers completed.
4. Apply the move (hold / split / shape).
5. `validate`, `snapshot --why "…"`, then re-mirror.

## What never happens here

- **A topic is never flipped to `shaped` on your inference.** The answers come from people. If the call
  didn't settle it, it isn't settled.
- **A partial answer is not permission to invent the rest.** Half an answer means the question is
  rewritten more narrowly, not deleted.
- **A blocking question is never quietly downgraded** to get a topic moving. If it stops you writing the
  outcome, holding is the correct outcome of this flow.
