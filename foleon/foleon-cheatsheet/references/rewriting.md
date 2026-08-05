# Rewriting a log entry into an entry (CHS-1, CHS-4, CHS-6, CHS-7)

The log is written for an agent that reads every line. The cheat sheet is read by a human who wants
the answer in the time it takes to scan a short list of titles. **These need different text.**
Copying, excerpting or lightly editing the log entry violates CHS-1 — the transform is a rewrite, and
the result is exactly **one entry**, matching the target category page's existing voice.

Validate the composed entry with `python3 scripts/row.py check --bullet "..."` before proposing it.
It checks voice (banned openers, hedging, discovery narrative) — **not length**. There is no word cap
(CHS-6, v2.1.0): an entry is as short as the fact allows, and extends to include a short explanatory
clause or a fenced code block whenever the bare fact would be ambiguous or unusable without one. The
one thing that must stay short is the **lead phrase** — it alone has to identify the topic.

## Match the target page's own style

The category pages already have a voice; don't invent a new one. Two shapes, both current:

**Most entries are their own heading**, title = lead phrase, body = the fact:

> `## Editor ≠ viewer`
> `The editor imports Tailwind (Preflight resets borders), the viewer doesn't. Borders can be right in the editor, wrong when published.`

**Within a sub-heading grouping related facts** (e.g. `Commands` → `## Building`), a fact can stay a
short bulleted line inside the group rather than getting its own heading — that's a judgement call,
not a rule; if in doubt, give it a heading, headings are cheap.

Front-loaded title, then the fact in as many sentences as it needs. A new entry should be
indistinguishable in style from one the maintainer wrote themselves.

## The four moves

1. **Find the symptom, not the cause.** The log records what you learned (the cause). The bullet is
   indexed by what you'd notice (the symptom or the topic) — lead with that.
2. **Front-load the lead phrase.** `**Card content rounds along with the card**` scans faster than
   `**When you set a radius on the card...**`.
3. **Cut to the lever.** One action, one line. Drop the reasoning trail, the file tour, the ticket
   number — if a ticket number matters, it can trail at the end in parentheses, but it's rarely worth
   the words.
4. **Strip the narrative.** No "we found", no "it turned out", no hedging. If it's not certain, it
   fails admission gate 4 — it doesn't get softened onto the page.

## Worked transform

**Log entry (169 words, three findings interleaved):**

> 2026-07-21 — Card-item DOM has 2 layers under the root: `.CardItemInnerContainer` (holds the
> content — image/text/button — AND `overflow:hidden` + the CSS border + padding) and
> `.CardItemBackgroundContainer` (absolute, behind, holds bg color/image). The card corners/
> border-radius setting is written to BOTH via `appendToCSS` and an explicit `set(...)`. Because
> InnerContainer wraps content + has `overflow:hidden`, its radius CLIPS the content → rounding the
> card also rounds the image/text/button inside.

**Entry (illustrative — the maintainer has since pruned this specific one off the page, so don't
expect to find it there; the technique is what matters):**

> `## Cards`
> `.CardItemBackgroundContainer = frame (bg, border, radius, shadow), .CardItemInnerContainer = content + padding. Children use border-radius: inherit → clip with clip-path: inset(0 round …) instead.`

What changed: the DOM tour became nothing (dropped — not needed to act). The causal chain became the
minimum needed to know *which layer to touch*. Three findings in the log became one entry, because
only one of them clears admission on its own merits.

## Worked transform — when the fact genuinely needs more (CHS-6, v2.1.0)

Not every admissible fact fits a single clause. When the bare instruction would be unusable without
knowing *why* or *how*, extend the entry — an explanatory clause, a fenced code block, or both. This
is not a violation; a rigid length cap here was tried and rejected as unusable.

**Log entry:**

> 2026-07-22 — the apps bundle `@foleon/core`'s built `dist`, not its source. Editing core `src` alone
> does nothing visible until you rebuild the whole chain: core, then editor, then copy env-config —
> forgetting the last step leaves the editor unable to boot.

**Entry (lead phrase + why + code, all admissible under CHS-6):**

> `**Changed @foleon/core?** The apps bundle its built dist, not the source — editing src alone changes nothing until you rebuild the chain:`
> ```bash
> pnpm --filter @foleon/core build
> pnpm --filter @foleon/editor build
> cp src/env-config.js dist/env-config.js
> ```

The lead phrase (`**Changed @foleon/core?**`) still identifies the topic in one clause — that's the
only thing CHS-6 actually requires. Everything after it is exactly as long as needed to make the fact
usable, no longer.

## Banned openers (CHS-4)

`Issue with` · `Problem with` · `How to` · `Note about` · `Fix for` · `When you` · `Something about` ·
a leading `A` / `An` / `The`. Enforced by `row.py check`.

## Banned voice (CHS-7)

- **Hedges** — `probably`, `possibly`, `might be`, `seems`, `maybe`, `I think`, `unclear`. An uncertain
  fact fails admission gate 4; it doesn't get hedged onto the page.
- **Discovery narrative** — `we found`, `it turned out`, `after investigating`.

Project jargon is *encouraged* — `@foleon/core`, `to-css`, KrakenD, Preflight. The audience is the
maintainer.

## Choosing a category page, then a heading (CHS-8)

Two decisions, in order:

1. **Which category page?** Fetch the hub for the real, current list — today: `Commands` ·
   `Packages` · `Conventions` · `Gotchas` · `Debugging`. Pick the one you'd actually look under, not
   the one that matches where the code lives. A rendering gotcha you'd hit while debugging generally
   goes on `Gotchas`; a reusable console technique goes on `Debugging`.
2. **New top-level heading, or under an existing sub-heading?** Once on the right page, check whether
   it belongs alongside a natural cluster already there (e.g. `Commands` already groups `Building` /
   `Running` / `Testing` / `Fixes`) — if so, it's a bullet under that sub-heading. Otherwise it's a new
   `##` heading of its own.

**Both a new category page and a new top-level heading are rare and deliberate.** If nothing existing
fits at either level, say so explicitly when proposing — "this doesn't fit any current category;
propose a new page for `X`?" — rather than forcing it into the closest one. CHS-8 wants 4–8 categories
total (however they're split between pages and headings) and ~10 entries per category before it needs
to split further; check both before proposing something new.
