---
name: "mobile-responsive"
description: >
  Mobile-responsive rework of existing React components. Analyzes a desktop-first component
  and turns it into a mobile-optimized one by applying standards for touch ergonomics,
  WCAG accessibility, animation performance, and fluid layout. Use this skill whenever the
  user asks to: make a component responsive, adapt a page for mobile, fix the responsive
  behavior, optimize for smartphone, rework the mobile experience, "it doesn't work on mobile",
  "it's broken on small screens", adapt a form for mobile, or any request that involves
  adapting an existing React interface for touch smartphone screens.
---

# Mobile Responsive — Reworking React components

Transforms desktop-first React components into mobile-optimized experiences, grounded in
UX research and accessibility standards.

This skill does not invent components from scratch — it takes existing code and improves it
for mobile. The philosophy: every decision should be traceable to empirical data or an
official standard, not to a hunch.

---

## Workflow

### Step 1 — Audit the component

Before touching any code, read the target component and produce a structured diagnosis.
See `references/audit-checklist.md` for the complete evaluation grid.

**The 6 dimensions to evaluate:**

1. **Touch targets** — Are all interactive elements >= 44px? Are the primary actions in the lower third?
2. **Layout** — Does the layout use rigid breakpoints or fluid design? Are there hardcoded `px` values for spacing?
3. **Typography** — Are sizes in `rem`? Is body text >= 16px? Are inputs >= 16px (otherwise iOS zoom)?
4. **Accessibility** — Are interactions triggered on `pointerup`? Are there alternatives to gestures? Is `prefers-reduced-motion` handled?
5. **Animation** — Do animations use only `transform`/`opacity`? Are durations < 500ms?
6. **Interactions** — Are swipeable elements 24px+ from the edges? Is the mobile keyboard handled?

Present the diagnosis in this format:

```
## Mobile diagnosis — [ComponentName]

| Dimension | Status | Issues |
|-----------|--------|--------|
| Touch     | ...    | ...    |
| Layout    | ...    | ...    |
| Typo      | ...    | ...    |
| A11y      | ...    | ...    |
| Animation | ...    | ...    |
| Interact. | ...    | ...    |

**Priority 1:** [the most impactful issue]
**Priority 2:** [...]
```

### Step 2 — Rework

Apply the fixes in priority order. Each change should be minimal and targeted —
do not refactor what already works.

**Cardinal rules:**

1. **Don't break the desktop.** Every mobile change must be backward-compatible.
   Use `min-width` media queries or container queries, not `max-width`, which overrides the desktop.

2. **Fluid first, breakpoints as a last resort.** Prefer `clamp()` and flexbox/grid
   intrinsic sizing before adding media queries. A well-built responsive component
   often needs no explicit breakpoints at all.

3. **Touch targets: always 44px minimum.** The clickable area can be enlarged with
   padding without changing the visual. Use `min-height: 44px; min-width: 44px;` on
   every interactive element (buttons, links, inputs, selects).

4. **Inputs at 16px minimum.** Otherwise iOS Safari zooms automatically on focus.
   This is the #1 bug users report — and the fix is trivial.

5. **Animations: `transform` and `opacity` only.** Any other animated property
   causes jank on mid-range devices. Budget: 10ms/frame on a Snapdragon 600.

6. **`prefers-reduced-motion` is mandatory.** 10-15% of iOS users enable it.
   Failing to implement it is an accessibility violation.

### Step 3 — Verification

After the rework, check:

- [ ] TypeScript compiles without errors
- [ ] The component looks identical on desktop (no regression)
- [ ] Touch targets >= 44px on all interactive elements
- [ ] Body text >= 16px (1rem)
- [ ] Inputs >= 16px (no iOS zoom)
- [ ] No animation on layout properties
- [ ] `prefers-reduced-motion` handled if any animations exist
- [ ] Safe area insets accounted for if the component sits at the bottom of the screen

---

## Quick reference — Key values

### Touch targets

| Screen position | Minimum size | Reason |
|-----------------|-------------|--------|
| Center | 44px (44x44) | Apple HIG standard / WCAG 2.5.5 |
| Top of screen | 42px (11mm) | Reduced precision at the top |
| Bottom of screen | 46px (12mm) | Safe area compensation + precision |
| Corners | 48px+ | Only 65-75% precision |

### Fluid typography

```css
/* Body — never drop below 1rem */
font-size: clamp(1rem, 0.5vw + 0.875rem, 1.25rem);

/* Heading h1 */
font-size: clamp(1.5rem, 3vw + 0.75rem, 2.5rem);

/* Small text — absolute minimum 0.75rem (12px) */
font-size: clamp(0.75rem, 0.5vw + 0.625rem, 0.875rem);
```

Always use `rem` (never `px` for text) — this respects iOS Dynamic Type
and Android system font-size preferences.

### Fluid spacing

```css
/* Tokenize in the design system or :root */
--space-xs: clamp(0.25rem, 0.5vw, 0.5rem);
--space-s:  clamp(0.5rem, 1vw, 0.75rem);
--space-m:  clamp(0.75rem, 1.5vw, 1.5rem);
--space-l:  clamp(1rem, 2.5vw, 2.5rem);
--space-xl: clamp(1.5rem, 4vw, 4rem);
```

### Animation

| Type | Duration | Easing |
|------|----------|--------|
| Micro (button, toggle) | 100-150ms | `ease-out` |
| Reveal (accordion, dropdown) | 200-300ms | `cubic-bezier(0.2, 0, 0, 1)` |
| Transition (modal, page) | 250-350ms | `cubic-bezier(0.2, 0, 0, 1)` |
| Absolute MAX on mobile | 500ms | — |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Safe areas

```css
/* Bottom fixed elements (nav, FAB, CTA) */
padding-bottom: max(16px, env(safe-area-inset-bottom));

/* Full bleed */
padding: env(safe-area-inset-top) env(safe-area-inset-right)
         env(safe-area-inset-bottom) env(safe-area-inset-left);
```

Prerequisite: `<meta name="viewport" content="..., viewport-fit=cover">`.

### Tailwind v4 breakpoints

| Token | Value | Typical use |
|-------|-------|-------------|
| `sm:` | 640px | Landscape smartphone / small tablet |
| `md:` | 768px | Portrait tablet |
| `lg:` | 1024px | Landscape tablet / small desktop |

---

## Rework patterns by component type

### Forms

1. Stack into a single column below `md:` (15.4s faster to complete)
2. Inputs: `min-height: 44px`, `font-size: 1rem` (no iOS zoom)
3. Semantic HTML5 types (`type="email"`, `type="tel"`) for the right keyboard
4. Sticky CTA at the bottom or above the keyboard (not fixed underneath the keyboard)
5. Enable `autocomplete` on all relevant fields (-75% abandonment)

### Data tables

| Strategy | When |
|----------|------|
| Convert to cards | Default — best mobile readability |
| Progressive disclosure | Rich rows, expand for details |
| Horizontal scroll + indicator | Column comparison required |
| Priority columns | Some columns are non-essential |

### Navigation

- **Bottom tab bar** for 3-5 primary sections (1.5x more interactions than hamburger)
- **Hamburger/drawer** for secondary sections only
- Primary actions in the lower third (98% thumb precision)
- Bottom safe area on fixed navigation

### Modals / Sheets

- Convert modals into **bottom sheets** on mobile (Vaul pattern)
- Snap points for intermediate states
- Drag-to-dismiss with a visual handle
- Focus trap and screen reader announcement

---

## Failure modes & recovery

| Failure | Recovery |
|---------|----------|
| The component has no clear desktop version | Ask the user what the reference desktop design is before making changes |
| The project's design system uses different tokens | Read the tailwind.config / theme before proposing values |
| The component uses specific UI libraries (MUI, Ant, Mantine) | Adapt the fixes to the library's API, not raw CSS |
| The rework breaks an existing test | Fix the test if the behavior changed intentionally |
| The animation uses a JS library (Framer Motion) | Don't replace it with CSS — adapt the Motion config with `reducedMotion="user"` |
| The component is too complex for a single pass | Break it into subtasks and handle it dimension by dimension |

---

## Reference files

Read the relevant file only when the corresponding dimension calls for it:

| File | When to read it |
|------|-----------------|
| `references/audit-checklist.md` | Step 1 — for the full audit grid |
| `references/research-data.md` | When you need precise figures to justify a decision |
