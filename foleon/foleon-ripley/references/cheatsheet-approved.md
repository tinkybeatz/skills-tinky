# ripley — Foleon cheat sheet (GENERATED, mirrored from Notion)

> **Do not hand-edit.** This concatenates every category page under the `Foleon - Cheat Sheet` Notion
> hub, refreshed by `foleon-cheatsheet` whenever any of them changes. Edit the Notion pages, not this
> file — this file is overwritten on the next pull. The human side is split across several short
> pages for readability (CHS-8); this file stays one, so reading it is still just "read one file."

Everything below already went through conversational approval before it was written (CHS-9) — there
is no separate "approved" filter to apply, because there is no per-item anything on any of these
pages.

Last pulled: 2026-08-05

---

# Ripley

pnpm monorepo — the Foleon Docs **editor** (creation) and **viewer** (preview & published docs), both
rendering from a shared `@foleon/core`.

Node `>=22 <23` · pnpm `11.1.1` (enforced) · TypeScript + React · Biome · Vitest · Playwright

## 💻 Commands

### Building
```bash
pnpm bootstrap        # install + set up workspace
pnpm build             # build everything
pnpm ci:compile        # TypeScript check
pnpm build:integration # required before Playwright, serves dist
```

### Running
```bash
pnpm editor:dev  # run the editor
pnpm viewer:dev  # run the viewer
```

### Testing
```bash
pnpm editor:test / pnpm viewer:test           # unit tests (Vitest)
pnpm --filter @foleon/editor test:playwright  # integration / e2e
```

### Fixes
```bash
cp src/env-config.js dist/env-config.js  # after every build, or the editor won't boot
sh scripts/prepare-auth.sh               # fixes 403 Forbidden
```

### After changing @foleon/core
The apps bundle core's `dist`, not its source — rebuild the chain: core → editor → copy env-config.
```bash
cd packages/foleon-core && pnpm build && cd ../.. && pnpm editor:dev
```

## 📦 Packages

`packages/`, scope `@foleon/*`

| Folder | Package | Role |
|---|---|---|
| `foleon-core-editor` | `@foleon/editor` | editor app |
| `foleon-core-viewer` · `-viewer-dynamic` | `@foleon/viewer` | preview & published docs |
| `foleon-core` | `@foleon/core` | shared entities, styles, rendering |

Plus `navigator`, `search`, `sdk`, `ui-design-system`, `cookie-consent`, `config`. Internal deps use
`workspace:*`.

## 📏 Conventions

### Arrow functions only
No `function` declarations, no mixing styles.

### No hardcoded values
No hardcoded strings / numbers / booleans → constants. `const`-assertion unions, not `enum`s.

### Biome formatting
Single quotes, width 120.

### Size limits
Complexity < 10 · file ≤ 300 · component ≤ 200 · function ≤ 50.

### Test structure
Tests in `__tests__/` next to the code, `*.test.tsx`, `describe > it > expect`, ≥ 80% coverage.

### Folder structure
Global types/constants/hooks/contexts → dedicated folders in `src/`; local ones stay in their
feature folder.

## ⚠️ Gotchas

### to-css.ts decides the DOM element
A `*.to-css.ts` file decides which DOM element a style lands on — mutations only write the value.
Wrong element = look there.

### Editor ≠ viewer
The editor imports Tailwind (Preflight resets borders), the viewer doesn't. Borders can be right in
the editor, wrong when published.

### Images: only ImageViewer is shared
Viewer mounts `ImageViewerContainer` → `renderImg`; the editor imports `ImageViewer` directly. Only
`ImageViewer` is shared — logs in the container never fire in the editor.

### Animations won't replay after an asset swap
Animations are pure CSS — swapping an asset keeps the same `animation-name`, so it won't replay.
Remount with a `key`.

### Animations are Content Studio only
Animations exist only in Content Studio, never Content Builder. Card images can't have them.

## 🐛 Debugging

### Element won't hover or click, no obvious cause
Paste the console probe below in DevTools, hover the spot, press `q` — dumps the full paint-order
stack + CSS; usually an animation/parallax layer sits on top.

```javascript
let p = { x: 0, y: 0 }
addEventListener('mousemove', e => (p = { x: e.clientX, y: e.clientY }), true)
const probe = () => {
  const els = document.elementsFromPoint(p.x, p.y)
  window.$probe = els.map((el, i) => ({
    i, el, tag: el.tagName,
    classes: [...el.classList].filter(c => !c.startsWith('sc-')).join(' ') || '(none)',
    containsPrev: i > 0 ? el.contains(els[i - 1]) : null,
    style: Object.fromEntries([...getComputedStyle(el)].map(k => [k, getComputedStyle(el).getPropertyValue(k)])),
  }))
  console.table(window.$probe.map(({ style, el, ...rest }) => rest))
  console.log('Full CSS per layer: $probe[i].style — e.g. $probe[2].style.transform. Select element: $probe[2].el')
}
addEventListener('keydown', e => { if (e.key === 'q') probe() }, true)
```

**Diff helper** — `$probe[i].style` holds 300+ computed properties per layer, too many to eyeball two
at once:

```javascript
window.$diffStyle = (i, j) => {
  const a = $probe[i].style, b = $probe[j].style, out = {}
  for (const k of Object.keys(a)) if (a[k] !== b[k]) out[k] = { [i]: a[k], [j]: b[k] }
  return out
}
```

How to use:
1. Paste this function once, in the same console as the probe above.
2. Press `q` on the suspect spot to populate `$probe` (do this first — the function reads it).
3. From the printed table, pick two row numbers: the layer that's blocking clicks, and the layer that
   should receive them.
4. Run `$diffStyle(0, 1)` (swap in your row numbers). Returns only the properties that differ, e.g.
   `{ pointerEvents: { 0: 'auto', 1: 'none' } }` — usually the exact property that's eating the click.
5. To compare two separate captures instead (e.g. a feature flag on vs off), run `let before = $probe`
   to save the first capture BEFORE re-probing, toggle the flag, press `q` again, then compare
   `before[i].style` vs `$probe[j].style` the same way — `$diffStyle` itself only reads the current
   `$probe`.
