# The four admission gates (CHS-2)

A finding earns a cheat-sheet row only if it passes **all four**. Most don't.
The log keeps everything either way, so rejecting is free — and a sheet that
admits everything is just the log with worse formatting.

| Gate | Question | Fails when |
|---|---|---|
| 1. Recurrence | Will this plausibly be looked up *again*? | It's history: what we did, once, on one ticket |
| 2. Retrieval cost | Was re-deriving it expensive (~10 min+, or required reading source)? | A grep or a glance at config answers it |
| 3. Non-obviousness | Is it absent from — or contradicted by — the obvious source? | `package.json`, the README or the official docs already say it |
| 4. Actionability | Does it resolve to a *do this*? | It's explanation, background, or a fact with no action attached |

Report the **first** gate a finding fails. One named gate is a decision; four
paragraphs of hedging is not.

---

## Worked examples

These are real entries from `foleon-ripley/references/knowledge.md`.

### ✅ ADMIT — card children inherit border-radius

> 2026-07-21 — GOTCHA: card child element viewers use `border-radius: inherit`
> (e.g. `entities/background/viewer/background.shared.tsx`, and the editor's
> `item-action-overlay`). So ANY `border-radius` on `.CardItemInnerContainer` is
> inherited by every child which then rounds its OWN 4 corners → that IS the
> "content becomes round" bug. … Final fix: border-radius on the FRAME layer for
> bg/border/shadow, and `clip-path: inset(0 round …)` on the content container.

- **Recurrence** ✓ — rounded-corner work recurs across card-like components.
- **Retrieval cost** ✓ — cost a full debugging cycle across three files.
- **Non-obviousness** ✓ — nothing in the code announces `inherit`; the symptom actively misleads you toward the wrong layer.
- **Actionability** ✓ — resolves to a concrete lever: radius on the frame, `clip-path` on the content.

Becomes `CS-3`.

### ❌ REJECT — gate 1 (recurrence): the PROD-3816 changelog

> 2026-07-21 — Fix for the above (PROD-3816): moved the card "frame" styling off
> `.CardItemInnerContainer` onto `.CardItemBackgroundContainer` … border
> cssSelector changed in BOTH `card-item.model.ts` AND the editor's
> brand-settings preview.

This is a record of *what was done on one ticket*. You will never arrive at the
sheet asking "what did PROD-3816 change?" — you'll ask git. The reusable insight
inside it is already `CS-3`; the ticket narrative is not separately admissible.

**This is the most common false positive.** A log entry describing a fix reads
like cheat-sheet material because it contains a fix. Ask what *symptom* would
bring you here. If the answer is "none — I'd only find this by already knowing
about it", reject.

### ❌ REJECT — gate 3 (non-obviousness): toolchain versions

> Node `>=22 <23` · pnpm `11.1.1` (enforced)

`package.json` enforces this and will error at you. A row here would be a second
source of truth that can silently go stale — actively worse than nothing.

### ❌ REJECT — gate 4 (actionability): where the old convention lists live

> 2026-07-20 — Fuller (historical, partly aspirational) convention lists live in
> the ripley repo's `.cursor/rules/*.mdc`. Treat them as reference, not ground
> truth — `project-facts.md` and this log are authoritative.

Genuinely non-obvious and worth knowing, but it resolves to a *posture*, not an
action. It belongs in `project-facts.md`, which is exactly where it is. Not
everything valuable is a cheat-sheet row.

### ⚠️ BORDERLINE — the `@foleon/*` scope correction

> Package scope is `@foleon/*`, **not** `@ripley/*`. The legacy Cursor rule still
> says `@ripley/` — that line is stale.

Gate 3 passes strongly (a live file *contradicts* reality). Gate 4 is weak — the
action is "trust `package.json`". Rejected as a row, because it is a **fact about
the project**, and facts belong in `project-facts.md` where they are loaded
automatically. Rows are for *symptom → fix*.

**The rule of thumb this establishes:** a stable fact → `project-facts.md`. A
symptom you'll hit again → a cheat-sheet row. History → the log only.

---

## Rejection is the healthy outcome

Actual result of the 2026-08-03 migration: **30 log entries → 18 rows**, so 12 were
rejected. That admit rate is higher than typical because the log at that point was
unusually dense with test-harness gotchas, which score maximally on all four gates —
you hit them every time you write a Playwright test, each cost a full run to find,
none are documented, and each resolves to a concrete lever.

Do not read 18/30 as the target. What was rejected is the more useful signal:

| Rejected | Gate |
|---|---|
| The PROD-3816 / PROD-3528 fix narratives | 1 — ticket history, no symptom leads there |
| Toolchain versions, `@foleon/*` scope | 3 — `package.json` already says it (→ `project-facts.md`) |
| "`.cursor/rules` are not ground truth" | 4 — a posture, not an action (→ `project-facts.md`) |
| Pre-existing red on `main` | 1 — point-in-time state that will go stale |
| The `load-hotspot` fixture | 2 — cheap to re-find with a grep |
| Cinematic keyframe prefix, shared `dropdownTrigger2` testid | folded into the rows they belong to |

If a *routine* sync admits most of what it sees, the gates were applied loosely — that
is the failure mode this file exists to prevent. Re-read gate 1 and gate 4 first; they
catch the most false positives.
