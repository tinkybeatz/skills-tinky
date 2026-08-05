# Rewriting a log entry into a bullet (CHS-1, CHS-4, CHS-6, CHS-7)

The log is written for an agent that reads every line. The page is read by a human who wants the
answer in the time it takes to scan a short list. **These need different text.** Copying, excerpting
or lightly editing the log entry violates CHS-1 — the transform is a rewrite, and the result is
exactly **one bullet**, matching the page's existing voice.

Validate the composed bullet with `python3 scripts/row.py check --bullet "..."` before proposing it.
The word cap is numeric — don't estimate it.

## Match the page's own style

The page already has a voice; don't invent a new one. Its existing bullets look like this:

> `**Editor ≠ viewer**: the editor imports Tailwind (Preflight resets borders), the viewer doesn't. Borders can be right in the editor, wrong when published.`
>
> `**Animations are pure CSS** — swapping an asset keeps the same animation-name, so it won't replay. Remount with a key.`

Bold lead phrase, colon or em-dash, then the fact in one breath. That's the whole format. A new
bullet should be indistinguishable in style from one the maintainer wrote themselves.

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

**Bullet (already on the page, for reference — do not re-add it):**

> `**Cards**: .CardItemBackgroundContainer = frame (bg, border, radius, shadow), .CardItemInnerContainer = content + padding. Children use border-radius: inherit → clip with clip-path: inset(0 round …) instead.`

What changed: the DOM tour became nothing (dropped — not needed to act). The causal chain became the
minimum needed to know *which layer to touch*. Three findings in the log became one bullet, because
only one of them clears admission on its own merits.

## Banned openers (CHS-4)

`Issue with` · `Problem with` · `How to` · `Note about` · `Fix for` · `When you` · `Something about` ·
a leading `A` / `An` / `The`. Enforced by `row.py check`.

## Banned voice (CHS-7)

- **Hedges** — `probably`, `possibly`, `might be`, `seems`, `maybe`, `I think`, `unclear`. An uncertain
  fact fails admission gate 4; it doesn't get hedged onto the page.
- **Discovery narrative** — `we found`, `it turned out`, `after investigating`.

Project jargon is *encouraged* — `@foleon/core`, `to-css`, KrakenD, Preflight. The audience is the
maintainer.

## Choosing a heading (CHS-8)

Pick the heading you'd actually look under, not the one that matches where the code lives. Today's
headings: `Commands` · `Packages` · `Conventions` · `Gotchas` · `Playwright gotchas`. A rendering bug
that only shows up during testing goes under `Playwright gotchas` if that's where you'd search for
it, `Gotchas` if it's a general rendering fact you'd hit outside tests too.

**Adding a new heading is rare and deliberate.** If nothing existing fits, say so explicitly when
proposing — "this doesn't fit any current heading; propose a new `## X`?" — rather than forcing it
under the closest one or silently adding a heading. CHS-8 wants 4–8 headings total; check that a new
one is really warranted before proposing it.
