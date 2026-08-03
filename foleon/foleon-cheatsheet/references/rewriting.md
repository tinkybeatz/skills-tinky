# Rewriting a log entry into a row (CHS-1, CHS-4, CHS-6, CHS-7)

The log is written for an agent that reads every line. The sheet is read by a
human under time pressure who scans headings until one matches, then reads three
lines. **These need different text.** Copying, excerpting or lightly editing the
log entry violates CHS-1 — the transform is a rewrite.

Validate every result with `python3 scripts/row.py check …` before writing. The
caps are numeric; don't estimate them.

## The five moves

1. **Find the symptom.** The log records the *cause* (it's what you learned). The row is indexed by the *effect* (it's what you'll notice). Invert it.
2. **Front-load.** The first two words carry the scan. `Card content rounds…` not `When the card has…`.
3. **Cut to the lever.** One action. Drop the reasoning trail, the file tour, the ticket number (that goes in `Refs`).
4. **Compress the cause to one sentence** — or leave `Why` empty. Empty beats speculation.
5. **Strip the narrative.** No "we found", no "it turned out", no hedging.

## Worked transform

**Log entry (169 words, 3 findings interleaved):**

> 2026-07-21 — Card-item DOM (`foleon-core .../card-item/viewer/card-item.viewer.tsx`)
> has 2 layers under the root: `.CardItemInnerContainer` (holds the content —
> image/text/button — AND `overflow:hidden` + the CSS border + padding) and
> `.CardItemBackgroundContainer` (absolute, behind, holds bg color/image). The card
> corners/border-radius setting (`card-item.style.to-css.ts` `corners` override) is
> written to BOTH via `appendToCSS` (cssSelector=`.CardItemInnerContainer`) and an
> explicit `set(...BackgroundContainer...)`. Because InnerContainer wraps content +
> has `overflow:hidden`, its radius CLIPS the content → rounding the card also
> rounds the image/text/button inside. Sharp edge when touching card rounded-corner
> behavior.

**Row (`CS-3`):**

| Field | Value |
|---|---|
| `Symptom` | Card content rounds along with the card |
| `Area` | Core / rendering |
| `Fix` | Put border-radius on `.CardItemBackgroundContainer` (the frame). Clip the content with `clip-path: inset(0 round …)` on `.CardItemInnerContainer` — never border-radius. |
| `Why` | Child viewers use `border-radius: inherit`, so any radius on the content layer rounds every child. |
| `Refs` | `card-item.style.to-css.ts` · `card-item.model.ts` · PROD-3816 |

What changed: the DOM tour became `Refs`. The causal chain became one `Why`
sentence. "Sharp edge when touching…" — narrator commentary — was dropped. The
symptom, which the log never actually states as a symptom, became the title.

## Atomicity (CHS-3)

That log entry contained three findings: the DOM layering, the inherit gotcha,
and the ticket's fix. One symptom is admissible, so it produces **one** row. If
two genuinely distinct symptoms are admissible, write two rows sharing a `Refs`
value — never one row with "and" in the title.

## Banned openers (CHS-4)

`Issue with` · `Problem with` · `How to` · `Note about` · `Fix for` · `When you` ·
`Something about` · a leading `A` / `An` / `The`. Enforced by `row.py check`.

They waste the two words that carry the scan. `Issue with the editor not booting`
→ `Editor won't boot after a build`.

## Banned voice (CHS-7)

- **Hedges** — `probably`, `possibly`, `might be`, `seems`, `maybe`, `I think`, `unclear`, `not sure`. An uncertain fact fails admission gate 4; it doesn't get hedged onto the sheet.
- **Discovery narrative** — `we found`, `it turned out`, `turns out`, `after investigating`, `during debugging`.
- **Emphasis** — no ALL CAPS shouting, no "critical!!". The log uses caps for the agent's benefit; the sheet doesn't.

Project jargon is *encouraged* — `@foleon/core`, `to-css`, KrakenD, Preflight.
The audience is you.

## Choosing `Area` (CHS-8)

Pick where you would **look for it**, not where the code lives.

| Finding is about | Area |
|---|---|
| Editor-only behaviour, panels, brand settings | Editor |
| Viewer / published-doc rendering, preview | Viewer |
| Shared rendering, entities, styles, `to-css`, animations | Core / rendering |
| pnpm, builds, env config, auth scripts, CI plumbing | Build & tooling |
| Playwright, Vitest, snapshots, flakiness, test selectors | Tests & Playwright |
| Code style, naming, file limits, arrow-functions-only | Conventions |

A rendering bug that only manifests in the editor goes to **Editor** if that's
where you'd hunt for it. When two areas fit equally, the tie-break is the symptom's
observation point, not the fix's location.
