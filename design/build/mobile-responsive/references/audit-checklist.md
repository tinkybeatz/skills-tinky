# Mobile responsive audit grid — Complete checklist

Use this checklist for step 1 of the workflow (diagnosis).
Each item is scored PASS / FAIL / N/A.

---

## 1. Touch Targets

- [ ] All buttons have `min-height: 44px` and `min-width: 44px` (or equivalent padding)
- [ ] Inline links within text have enough vertical spacing (line-height >= 1.5)
- [ ] Clickable icons have an enlarged tap area (padding, not just the icon)
- [ ] Primary actions are in the lower third of the screen (thumb zone)
- [ ] Spacing between adjacent targets is >= 8px (Material Design recommends 8dp)
- [ ] Targets in screen corners are >= 48px (precision drops to 65-75%)
- [ ] No target < 24x24px (WCAG 2.5.8 AA violation)

## 2. Layout

- [ ] The layout uses flexbox or grid (no `float`, no `position: absolute` for layout)
- [ ] Spacing uses `clamp()` or fluid tokens (no hardcoded `px`)
- [ ] Content does not overflow horizontally at 375px wide
- [ ] No unintentional horizontal scroll
- [ ] Images have `max-width: 100%` and `height: auto`
- [ ] Containers use `min-width: 0` when inside a flex/grid (prevents overflow)
- [ ] Container queries for components reused in different contexts
- [ ] Safe area insets handled for fixed elements at the bottom (`env(safe-area-inset-bottom)`)

## 3. Typography

- [ ] Body text >= 16px (1rem)
- [ ] All inputs and textareas >= 16px (otherwise automatic iOS Safari zoom)
- [ ] Body line-height >= 1.4 (WCAG 1.4.12 recommends 1.5)
- [ ] Sizes in `rem` or `em` (not `px` for text — breaks iOS Dynamic Type)
- [ ] No `vw` alone for font-size (violates WCAG 1.4.4 — use `clamp(rem, vw + rem, rem)`)
- [ ] Text truncated with `line-clamp` or `text-overflow: ellipsis` when needed
- [ ] `aria-label` or tooltip on truncated text for accessibility
- [ ] Contrast >= 4.5:1 for normal text, >= 3:1 for large text (AA)

## 4. Accessibility

- [ ] `<meta name="viewport">` does NOT have `user-scalable=no` or `maximum-scale=1`
- [ ] Interactions trigger on `pointerup`/`click`, not `pointerdown`/`touchstart`
- [ ] Every gesture (swipe, pinch, long press) has a visible alternative (button)
- [ ] Interactive elements have `aria-label` when the visible text is insufficient
- [ ] Focus is visible on all interactive elements
- [ ] Modals/bottom sheets have a focus trap
- [ ] State changes are announced via `aria-live` or equivalent
- [ ] Swipeable elements are >= 24px from screen edges (OS gesture conflicts)

## 5. Animation

- [ ] Only `transform` and `opacity` are animated (not width, height, margin, padding, top, left)
- [ ] Durations are < 500ms (Apple HIG mobile maximum)
- [ ] `prefers-reduced-motion` is handled (disables or reduces animations)
- [ ] No overuse of `will-change` (max 2-3 elements per view)
- [ ] Spring animations are interruptible (if using Framer Motion / React Spring)
- [ ] No `bounce` or `elastic` easing (dated and tacky — Apple HIG)
- [ ] Skeleton screens for loads > 300ms (instead of spinners)

## 6. Mobile interactions

- [ ] The mobile keyboard does not hide active inputs (auto-scroll or VisualViewport API)
- [ ] `overscroll-behavior: contain` on internal scrollable containers (no scroll chaining)
- [ ] Touch event listeners are passive (`{ passive: true }`)
- [ ] No hover-dependent content without a tap/focus alternative
- [ ] Bottom sheets have a visual handle for dragging
- [ ] Custom pull-to-refresh if needed (with `overscroll-behavior-y: contain` on body)
- [ ] Forms use semantic HTML5 `type`s (email, tel, number, url)

---

## Scoring

| Score | Interpretation |
|-------|---------------|
| 90-100% PASS | Mobile-ready component |
| 70-89% PASS | Minor fixes needed |
| 50-69% PASS | Significant rework required |
| < 50% PASS | Full rework recommended |
