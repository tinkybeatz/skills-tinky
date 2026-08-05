# The five admission gates (CHS-2)

A finding earns a bullet only if it passes **all five**. Most don't. The log keeps everything either
way, so rejecting is free — and a page that admits everything is just the log with a nicer font.

| Gate | Question | Fails when |
|---|---|---|
| 1. Recurrence | Will this plausibly be looked up *again*? | It's history: what we did, once, on one ticket |
| 2. Retrieval cost | Was re-deriving it expensive (~10 min+, or required reading source)? | A grep or a glance at config answers it |
| 3. Non-obviousness | Is it absent from — or contradicted by — the obvious source? | `package.json`, the README or the official docs already say it |
| 4. Actionability | Does it resolve to a *do this*? | It's explanation, background, or a fact with no action attached |
| 5. **Not already said** | Read the current page. Is this — or something close enough — already there? | It matches an existing bullet, even in different words |

Gate 5 did not exist in v1.x. Its absence is the actual root cause of the v1.x failure below — read
this before applying the other four, because a finding can pass gates 1–4 cleanly and still fail gate
5, and gate 5 is the one that actually protects the page.

---

## The v1.x failure, in numbers

On 2026-08-03 a batch of 18 "findings" were written as new database rows (each — because Notion rows
are pages — a new page). The maintainer rejected the whole thing on sight: *"this is not a
cheat-sheet, it's a document with 10000 of infos."*

On inspection, **13 of the 18 rows restated a bullet already on the maintainer's own hand-written
page**, just longer and in a worse place:

| New row said | Already on the page, one line |
|---|---|
| "Editor won't boot after a build" → copy env-config.js | `cp src/env-config.js dist/env-config.js # after every build, or the editor won't boot` — in `## Commands` |
| "403 Forbidden from local requests" → run prepare-auth.sh | `sh scripts/prepare-auth.sh # fixes 403 Forbidden` — in `## Commands` |
| "Card content rounds along with the card" → clip-path fix | `**Cards**: ... Children use border-radius: inherit → clip with clip-path...` — in `## Gotchas` |
| "Animation won't replay after swapping the asset" → remount with key | `**Animations are pure CSS** — ... Remount with a key.` — in `## Gotchas` |
| ...9 more, all Playwright gotchas | Already one-liners in `## Playwright gotchas` |

None of this was a wording problem. The admission gates that existed (recurrence, retrieval cost,
non-obviousness, actionability) were checking each new finding against *other database rows* and
against generic sources like `package.json` — **never against the maintainer's own page.** A finding
can be genuinely non-obvious relative to the codebase and still be completely obvious relative to a
page that already says it. Gate 5 exists specifically to close that hole, and it is checked by
reading the page directly — there is no shortcut, because there is no property to query.

---

## Worked examples (post-gate-5)

Page state referenced below is a snapshot from when these were written — the maintainer has since
pruned and restructured (page-per-category, headings instead of bold-in-bullet). Re-fetch the real
page before trusting any "already there" claim; the *technique* each example teaches is what to take
away, not the specific wording quoted.

### ✅ ADMIT — a genuinely new, short, durable fact

> Log entry: "TWO SEPARATE test suites, easy to confuse: `pnpm editor:test` runs only UNIT tests
> (Vitest); the integration/e2e suite is `pnpm --filter @foleon/editor test:playwright`, which reads
> *rendered* CSS. A green local vitest run does NOT cover integration."

- **Recurrence** ✓ — this distinction recurs every time someone changes a DOM layer.
- **Retrieval cost** ✓ — costs a full debugging cycle to learn the hard way.
- **Non-obviousness** ✓ — nothing in `package.json` states which suite covers what.
- **Actionability** ✓ — resolves to "run the other command too."
- **Not already said** ✓ — the page has no mention of the vitest/Playwright distinction anywhere.

Proposed bullet, under `## Gotchas`: *"**Two test suites**: `pnpm editor:test` is unit-only (Vitest);
`pnpm --filter @foleon/editor test:playwright` is integration and reads rendered CSS — a green vitest
run doesn't cover it."* 28 words, one line, matches the page's existing voice.

### ❌ REJECT — gate 5 (already said), despite passing 1–4 cleanly

> Log entry: "Card-item DOM has 2 layers: `.CardItemInnerContainer` (content) and
> `.CardItemBackgroundContainer` (frame, bg/border/radius/shadow). Children use `border-radius:
> inherit`, so radius on the content layer rounds every child. Fix: radius on the frame layer,
> `clip-path: inset(0 round …)` on the content layer."

Gates 1–4 all pass — this is a real, costly, non-obvious, actionable finding. **Gate 5 fails anyway**:
the page already has *"**Cards**: `.CardItemBackgroundContainer` = frame ..., `.CardItemInnerContainer`
= content ... Children use `border-radius: inherit` → clip with `clip-path: inset(0 round …)`
instead."* Same fact, already said, arguably in a tighter form. This is the exact shape of 13 of the 18
v1.x mistakes — check gate 5 *first* on anything that smells like a rendering/DOM gotcha, since that's
where the existing `## Gotchas` section already has the most coverage.

### ❌ REJECT — gate 1 (recurrence): a fix narrative

> Log entry: "Fix for PROD-3816: moved the card frame styling off `.CardItemInnerContainer` onto
> `.CardItemBackgroundContainer` ... border cssSelector changed in BOTH `card-item.model.ts` AND the
> editor's brand-settings preview component."

This is a record of *what was done on one ticket*. Nobody arrives at a cheat sheet asking "what did
PROD-3816 change?" — they ask git or the ticket. The reusable insight inside it is the Cards bullet
above, already on the page; the ticket narrative is not separately admissible.

### ❌ REJECT — gate 4 (actionability): a fact with no action

> Log entry: "Fuller (historical, partly aspirational) convention lists live in the ripley repo's
> `.cursor/rules/*.mdc`. Treat them as reference, not ground truth."

Genuinely non-obvious, genuinely true, and resolves to a *posture* rather than an action — "trust
`project-facts.md` instead." That's exactly where it lives, in `project-facts.md`. Not everything
worth knowing is a cheat-sheet bullet.

---

## Rejection is the healthy outcome — and it's the majority every time

If a routine sync proposes more than one or two bullets, stop and re-check gate 5 specifically —
proposing a lot is the single strongest signal that the gates are being applied loosely, and it is
exactly what happened the first time this system ran.
