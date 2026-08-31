# ripley — discoveries log

Non-obvious findings: gotchas, implicit conventions, architectural "why"s, sharp edges.

**This file is machine-facing.** Its audience is an agent that reads all of it, so entries are
**dense** on purpose — completeness beats brevity here. Human-facing phrasing is a different job:
`foleon-cheatsheet` decides whether a finding also earns a row in the Notion cheat sheet and
**rewrites** it for a human. Never write for a human here.

**Schema** (PCS-6 — one finding per entry):

```
- YYYY-MM-DD · <area> · <symptom> — <finding> · refs: <paths|tickets> · sheet: <yes|no|none>
```

- `<area>` — one of: Editor · Viewer · Core / rendering · Build & tooling · Tests & Playwright · Conventions
- `<symptom>` — what you *observe*, so the log can be scanned and deduplicated without reading every finding
- `sheet:` — `yes` if this fact is on the Foleon cheat-sheet page, `no` if it was proposed and
  declined, `none` if never evaluated or rejected by the gates. There is no per-item ID to point at —
  the mirror is one page, not a database.

**Before appending, search this file** for the finding's key terms. On a match, extend that entry and
refresh its date rather than adding a near-duplicate. When the log grows heavy, promote the stable
facts up into `project-facts.md` and prune here.

## Discoveries

- 2026-07-21 · Core / rendering · Card content rounds along with the card — Card-item DOM
  (`foleon-core .../card-item/viewer/card-item.viewer.tsx`) has 2 layers under the root:
  `.CardItemInnerContainer` (holds the content — image/text/button — AND `overflow:hidden` + the CSS
  border + padding) and `.CardItemBackgroundContainer` (absolute, behind, holds bg color/image). The
  card corners/border-radius setting (`card-item.style.to-css.ts` `corners` override) was written to
  BOTH via `appendToCSS` (cssSelector=`.CardItemInnerContainer`) and an explicit
  `set(...BackgroundContainer...)`. Because InnerContainer wraps content + has `overflow:hidden`, its
  radius CLIPS the content → rounding the card also rounds the image/text/button inside.
  · refs: `card-item.viewer.tsx` · `card-item.style.to-css.ts` · sheet: none
- 2026-07-21 · Core / rendering · Card children inherit any radius on the content layer — card child
  element viewers use `border-radius: inherit` (e.g. `entities/background/viewer/background.shared.tsx`,
  and the editor's `item-action-overlay` selection overlay). So ANY `border-radius` on
  `.CardItemInnerContainer` is inherited by every child (image/text/button) which then rounds its OWN 4
  corners → that IS the "content becomes round" bug. Therefore you canNOT round the card by putting
  border-radius on the content container. Correct lever: border-radius on the FRAME layer
  (`.CardItemBackgroundContainer`) for bg/border/shadow, and `clip-path: inset(0 round ...)` on
  `.CardItemInnerContainer` to clip content flush-to-the-card-corner (e.g. a full-bleed top image) to
  the rounded silhouette. `clip-path` is NOT inherited, so interior content (text/button) never rounds.
  Use this whenever you need "clip to rounded card shape" without children inheriting a radius.
  · refs: `background.shared.tsx` · `item-action-overlay` · sheet: none
- 2026-07-21 · Core / rendering · Card frame styling had to move off the content layer (PROD-3816) —
  moved the card "frame" styling (border-radius, border, box-shadow) off `.CardItemInnerContainer` onto
  `.CardItemBackgroundContainer` so the frame rounds while inset content stays square. Radius+shadow via
  overrides in `card-item.style.to-css.ts`; border cssSelector changed in BOTH `card-item.model.ts` (main
  render) AND the editor's brand-settings preview
  `@common/theme/components/cards/card-item/card-item.component.tsx`. Note: the to-css layer decides WHICH
  DOM selector a stored style value lands on — `box.mutations.ts`/`setBoxValue` only writes the value into
  the model, it can't target a layer. Full-bleed card BACKGROUND images live on the frame layer so they
  still round; only content-layer elements changed. · refs: PROD-3816 · `card-item.model.ts` · sheet: none
- 2026-07-22 · Tests & Playwright · Green vitest run, broken integration — TWO SEPARATE test suites, easy
  to confuse: `pnpm editor:test` (→ `vitest ... run`) runs only UNIT tests (Vitest, `*.test.ts(x)` next to
  source); the browser INTEGRATION/e2e suite is `pnpm --filter @foleon/editor test:playwright` (Playwright,
  `tests/integration/**`), which CI runs separately and which reads *rendered* CSS. A green local vitest run
  does NOT cover integration — after changing which DOM layer a style lands on, always run the matching
  Playwright spec. Reproduce one file: `cd packages/foleon-core-editor && pnpm test:playwright
  tests/integration/editor-brand-kit/content/card.ts`. · refs: `tests/integration/**` · sheet: none
- 2026-07-22 · Tests & Playwright · Many CI annotations, one real failure — CI editor integration runs
  fail-fast (`--max-failures=1`) sharded 8-way: ONE real failure cancels the other 7 shards ("The operation
  was canceled" / "strategy configuration was canceled") — that cascade inflates the annotation count. Don't
  read N annotations as N distinct bugs; find the single real failing spec. · refs: — · sheet: none
- 2026-07-22 · Tests & Playwright · Brand-kit card assertions had to follow the layer move — consequence of
  PROD-3816: brand-kit card integration tests in `editor-brand-kit/content/card.ts` assert
  border/border-weight/rounded-corners/shadow via `getCardInnerContainer` — these had to switch to
  `getCardBackgroundContainer` (border/radius/shadow now live on the frame). Padding/spacing stays on the
  inner container. Rule of thumb: when a to-css change relocates a property's DOM selector, grep the
  Playwright specs' `elementLocator`s for the old layer. · refs: `editor-brand-kit/content/card.ts` · sheet: none
- 2026-07-22 · Tests & Playwright · Snapshot passes locally, fails in CI — Viewer screenshot baselines are
  PER-PLATFORM: each `toHaveScreenshot` has both a `*-linux.png` (what CI compares against) and a
  `*-darwin.png` (local Mac) baseline under `<spec>.spec.ts-snapshots/`. A local Mac run only exercises the
  darwin ones — it does NOT prove CI (linux) will pass, and `--update-snapshots` on a Mac only fixes darwin.
  Regenerate the LINUX baselines inside the pinned Playwright container: `bash scripts/playwright-in-docker.sh
  bash -c "cd packages/foleon-core-viewer && pnpm test:playwright --update-snapshots <spec>"` (image is mcr
  playwright v1.50.1-jammy, matching `@playwright/test`; needs `pnpm viewer:build` first so `dist/previewer`
  exists — the container reuses the host's node_modules, installs nothing). `playwright` isn't on PATH in the
  container — go through the `pnpm test:playwright` script (it also sets PLAYWRIGHT_ENV=production for the SSL
  webServer). When a card/layout change shifts height, expect the cascade: everything below the first affected
  element shows as a red diff (vertical shift), not just the element itself.
  · refs: `scripts/playwright-in-docker.sh` · sheet: none
- 2026-07-22 · Tests & Playwright · Playwright reblessed every snapshot — Playwright CLI QUIRK in this repo's
  viewer config: a positional spec-path filter is unreliable — passing two file paths + `-g` ran only one file;
  passing one file path (with or without `-g`) ran the WHOLE suite (500+ tests). With `--update-snapshots` that
  silently reblesses every stable screenshot. ALWAYS `git status -- '*.png'` after an update run and revert
  strays (a flaky infographic-counter darwin snapshot got rewritten this way and had to be reverted). Scope the
  update by running in a throwaway and checking the resulting diff, not by trusting the path filter.
  · refs: — · sheet: none
- 2026-07-24 · Core / rendering · Phantom border in the published doc only (PROD-3754) —
  `entities/styles/border/border.to-css.ts` emits `border-<side>-style: solid` (unconditionally at size 50) +
  `border-<side>-color` (whenever a color exists), but width ONLY when truthy. The border settings panel's
  color picker writes color to ALL four sides at once (`handleUpdateBorderColor` in
  `@entities/styles/border/settings-panels/border.tsx`) while the per-side weight slider writes width only to
  the dragged side — so a "bottom-only weight" ends up with top/right/left carrying a color but NO width key.
  Result: `solid` + color + no width → browser falls back to `border-width: medium` (~3px). The EDITOR hides
  this because it imports Tailwind (`src/tailwind.css` `@import "tailwindcss"`) whose Preflight resets
  `*{border-width:0;border-style:solid}`; the VIEWER/published doc has no such reset → the phantom border
  paints. Classic "editor ≠ preview" border divergence. · refs: `border.to-css.ts` · PROD-3754 · sheet: none
- 2026-07-24 · Core / rendering · Explicit `width: 0px` is the fix, and `'0'` is truthy — force an explicit
  `border-<side>-width: 0px` for any side with no positive width
  (`if (!(Number(border[side]?.width) > 0)) appendToCSS(..., '0px')`), AFTER the value loop. Note width is
  stored as a bare number string (`'0'`,`'4'`), and `'0'` is TRUTHY — that's why the original `if (value)`
  check let a real `'0'` through but an ABSENT width slip. Do NOT "fix" by skipping the whole side when
  width≤0: the brand-kit tests `editor-brand-kit/content/card.ts` "changes border color" assert
  `toHaveCSS('border-color', ...)` after setting ONLY a color (no width) — dropping the side removes the color
  and fails them. Emitting explicit width:0 keeps color queryable AND kills the medium fallback.
  · refs: `border.to-css.ts` · sheet: none
- 2026-07-24 · Build & tooling · Core change not reflected in the editor — `border.to-css.ts` is shared by ALL
  bordered entities (block/button/image/table/card/text), editor AND viewer both bundle it from
  `@foleon/core`'s ESM dist. So after editing core `src`, you MUST rebuild:
  `pnpm --filter @foleon/core build` (tsc → dist/esm+cjs) THEN `pnpm --filter @foleon/editor build` (vite
  bundles core's dist, no source alias) THEN `cp src/env-config.js dist/env-config.js` before the Playwright
  production webServer (`serve:ssl` serves `dist`) will reflect the change. · refs: — · sheet: none
- 2026-07-24 · Tests & Playwright · Playwright finds no tests for a brand-kit spec — files under
  `tests/integration/editor-brand-kit/**` are plain `*.ts` (NOT `*.spec.ts`) and are found only via their
  PROJECT (`--project="Brand Kit Editor"`, testDir set per project in `playwright.config.ts`). Positional path
  filters ("content/card.ts") reliably return "No tests found" (the known CLI quirk); `-g "Card"` (matches the
  joined title, `›` are display-only, not in the title string) works. `-g "Content tab › Card"` does NOT match
  — never put `›` in a `-g` pattern. · refs: `playwright.config.ts` · sheet: none
- 2026-07-27 · Core / rendering · Image container logs never fire in the editor — IMAGE render paths DIVERGE
  between apps, which is why logs "go missing" when debugging
  `foleon-core/src/entities/image/viewer/image.container.tsx`. The VIEWER
  (`foleon-core-viewer/.../entities/image/image.container.tsx`) mounts `ImageViewerContainer` → which calls
  `renderImg` → which renders `ImageContainerWrapper` (`.Container`) > `FigureContainerStyles`
  (`.FigureWrapper`) > `ImageViewer`, passing the full entity `css` to the WRAPPER and **no `styles` prop to
  `ImageViewer`**. The EDITOR (`foleon-core-editor/src/@entities/image/image.editor.tsx`) imports `ImageViewer`
  DIRECTLY and composes its own DOM (`ImageContainerWrapper` > `ImageFigureWrapper` > `BoxResizer` >
  `AnimationClipWrapper` > `ImageViewer`) — it never mounts `ImageViewerContainer` and never reaches
  `renderImg`. So `ImageViewer` is the ONLY shared component; a log in `ImageViewerContainer`/`renderImg` fires
  in viewer/preview only, and `renderImg`'s `shouldShowLinkDisplay` branch is print-mode only.
  · refs: `image.container.tsx` · `image.editor.tsx` · sheet: none
- 2026-07-27 · Core / rendering · Image border scales with the animation (PROD-3528) — "animation exceeds the
  border in Editor": `image.model.ts` emits cinematic zoom + scroll animations onto
  `.${CSSIdentifiers.Image}` (the `<img>` itself) and the border onto `.FigureWrapper`. The viewer keeps that
  split → static bordered wrapper, `<img>` scales inside it. But the editor's `separateInnerStyles`
  (image.editor.tsx) deliberately MOVES background / all `border*` / `boxShadow` off `.FigureWrapper` and
  passes them FLAT as `innerStyles` to `ImageViewer`'s `styles` prop, landing them on the same `<img>` the zoom
  transforms — so the border scales with the animation. The documented reason for the move is that
  `ImageFigureWrapper` hosts the `BoxResizer` handles and a radius/overflow there clips the resizer.
  `AnimationClipWrapper` (renders only when `hasScalingAnimation`) already sits between the resizer and the img
  with `overflow: clip` + the corner radii, and already receives `innerStyles` — it is the natural non-animated
  host for the border/background/shadow. · refs: PROD-3528 · `image.model.ts` · sheet: none
- 2026-07-27 · Editor · Animation panels missing for a card image — the `Animation` / `AnimationCinematic` /
  `AnimationRepeat` panels are gated behind `isInContentStudioEditor && !isRenderedInCard`
  (`foleon-core-editor/src/@entities/image/settings-panel/index.tsx`), and `cardImageBaseStyles`
  (`foleon-core/src/entities/image/image.styles.ts`) carries no animation keys. Animation exists only in
  Content Studio, never Content Builder. Corollary for `image.editor.tsx`: its second render branch is NOT
  "the card branch" — the condition is `!isNotDisplayed(computed) && !isImgRenderedInCard`, so it also catches
  ordinary canvas images with `visibility: hidden|none` at the active screensize (`visibility.queries.ts`
  `isNotDisplayed`), which the editor still renders behind a `VisibilityOverlay` and which CAN carry a zoom
  animation. Don't reason about that branch as card-only.
  · refs: `@entities/image/settings-panel/index.tsx` · sheet: none
- 2026-07-27 · Tests & Playwright · Second setting won't open in the settings panel — the settings panel is a
  DRILL-DOWN (`settings-panel.content-renderer.tsx` `activeIndex`), not an accordion — after
  `openSetting('Border')` the category list is REPLACED, so touching a second setting needs a back click
  (`.settings-panel-category-container-back-icon`); added `SettingsPanel.closeSetting()` for this.
  · refs: `settings-panel.content-renderer.tsx` · sheet: none
- 2026-07-27 · Tests & Playwright · Animation panel missing from the test DOM — `AnimationCinematic` is behind
  the `editor.cinematicAnimations` flag and `return null`s without it — add the toggle to
  `tests/integration/shared/utils/routes/feature-flag-route.ts` or the dropdown simply isn't in the DOM.
  · refs: `feature-flag-route.ts` · sheet: none
- 2026-07-27 · Tests & Playwright · Cinematic keyframe names are prefixed — `animation-cinematic.to-css.ts`
  emits `cinematic-${name}`, so assert `animation-name: cinematic-zoomIn`, not `zoomIn`.
  · refs: `animation-cinematic.to-css.ts` · sheet: none
- 2026-07-27 · Tests & Playwright · Every `Select.Trigger` shares one fallback testid — all share
  `dropdownTrigger2` (`@foleon/deprecated-ui-kit_dropdown_dropdown-trigger`), so `.first()` inside the
  Animation category hits the ENTRANCE animation dropdown, not Cinematic. Scope it instead:
  `getByTestId(settingsPanelCategoryScreen).filter({ hasText: '<panel label>' }).getByTestId(dropdownTrigger2)`.
  Cycle is `pnpm build:integration` (only needed after a `src` change) then
  `pnpm test:playwright --project="Doc Editor" -g "<title fragment>"`. · refs: `data-testids.ts` · sheet: none
- 2026-07-28 · Tests & Playwright · Load-flake vs real failure look alike in a CI annotation — Load-flake
  (e.g. `image.editor-link.test.ts`): the failing SET changes run to run, and it passes when run alone or at
  `--workers=1`. Real failure: same test, same line, same locator every time, and it survives CI-style
  `--retries=2`. Decisive tell — Playwright prints `1 flaky` when a retry passes and `1 failed` when none do,
  so run the suspect with `--workers=1 --retries=2` and read that word before blaming the pipeline. Re-running
  the job will NOT clear a `1 failed`. · refs: — · sheet: none
- 2026-07-28 · Tests & Playwright · `image.editor-link.test.ts` is flaky locally — the failing set changes
  every run (2-3 of 8), always `hover` timeouts in `SettingsPanel.openForEntity`. It's parallel execution —
  local config is `workers: undefined` (all cores) while CI is `workers: 1, retries: 2`. Don't chase these as
  regressions; reproduce with `--workers=1` before believing a failure there is real.
  · refs: `image.editor-link.test.ts` · sheet: none
- 2026-07-28 · Tests & Playwright · Pre-existing red on `main` (local darwin) —
  `editor-doc/@entities/infographic/infographic-counter/infographic-counter.brand-kit-drawer.test.ts` ›
  `SettingsPanel › Animation`. Times out in `SettingsPanel.openForEntity('infographic-counter-number', 1)` →
  `scrollOptionButtonInToView`, waiting for the `.nth(1)` active indicator's settings button, i.e. the second
  counter never becomes interactable after `dragElementFromSidebarToColumn`. Verified pre-existing by reverting
  `src/@entities/image/image.editor.tsx` to `main`, rebuilding, and re-running: identical failure. The other 2
  tests in the file pass. Full editor integration suite otherwise: 644 passed / 1 failed / 1 skipped in 23.7m
  at `--workers=1`. Point-in-time state — re-verify before trusting.
  · refs: `infographic-counter.brand-kit-drawer.test.ts` · sheet: none
- 2026-07-28 · Build & tooling · Reverting one file to compare against `main` costs two builds — ~27s each,
  because the Playwright production webServer serves `dist`, not `src`. Sequence that works:
  `git checkout main -- <file>` (this STAGES it) → `pnpm build:integration` → `cp src/env-config.js
  dist/env-config.js` → run spec → `git restore --staged --worktree <file>` → rebuild → re-copy env-config.
  Forgetting the env-config copy after either build leaves the editor unable to boot. · refs: — · sheet: none
- 2026-07-31 · Core / rendering · Animation won't replay after swapping the asset (PROD-3521) —
  cinematic/entrance animations are pure CSS — nothing "triggers" them. `background.styles.ts` →
  `animation-cinematic.to-css.ts` emits `animation-name: cinematic-<name>` (20s, 1 iteration, `fill: both`,
  `play-state: paused` + `running` under `.foleon-animation .block-in-viewport &&`) onto the SAME element that
  carries `background-image`: `.viewer-background` (`foleon-core/.../background/viewer/background.shared.tsx`).
  Replacing the asset only mutates `image.assetRef` in place (`background.mutations.ts updateBackgroundImage`),
  so styled-components emits a new class but an IDENTICAL `animation-name` → per spec the browser does not
  restart → new image appears at the animation's end state. Fix: `key` on the asset identity in the editor's
  `background.editor.tsx` (`assetRef || url` for image, `assetRef` for video) → remount → fresh node → runs
  from 0. Covers block AND column backgrounds and both media types in one place, and needs no `@foleon/core`
  rebuild. Precedent for the same class of bug: `animation-cinematic.tsx handleAnimationUpdate` sets the name
  to 'none' then reapplies inside a rAF — that trick writes mutations (dirties the doc), the `key` approach
  doesn't. · refs: PROD-3521 · `background.editor.tsx` · sheet: none
- 2026-07-31 · Tests & Playwright · Media library opens but the gallery is empty — the current ML
  (`@foleon/assets-library` 1.6.29) lists assets from `GET /k/resources/media?...` (KrakenD shape:
  `{data:[{id,type:'image',name,access_type,view:{created_on,parent_topiary_id,filetype,filesize,properties,
  links:{self,storage_path,storage_path_thumbnail}}}],meta:{total,per_page,last_page}}`, mapped by
  `mapKrakenDToLegacy`), NOT the legacy `/topiary` — so `imageTopiaryRoute` opens the modal but leaves the
  gallery EMPTY. Added `mediaResourcesRoute` (`shared/utils/routes/media-resources-route.ts`) for it. In the
  DOM, gallery items are `[data-file-id="<id>"]` and the confirm button is labelled **"Choose"**; the
  `mediaLibrary*` testids in `data-testids.ts` (`media-library.gallery.media-item...`) are STALE — they match
  nothing (`link-modal.ts` still uses them). `view.links.self` becomes the entity `assetRef`
  (`getMediaItemPropsToChange` reads `_links.self.href`), so give the stub a different image id than the doc's
  current background or a "replace" is a no-op. · refs: `media-resources-route.ts` · sheet: none
- 2026-07-31 · Tests & Playwright · Block `BackgroundAnimation` panel needs TWO flags — cinematic + scroll:
  `editor.scrollAnimations` (else `background-animation.tsx` returns null) AND `editor.cinematicAnimations`
  (else `animation-cinematic.tsx` returns null). Neither is in the shared `featureFlagRoute`; added
  `featureFlagRouteWithAnimations` (base toggles + both) rather than enabling them for every editor-doc test.
  · refs: `background-animation.tsx` · sheet: none
- 2026-07-31 · Tests & Playwright · Need a block with an image background as a fixture — the `load-hotspot`
  recording (`url: doc/119281/pages/812305`) has a block with an image background whose `assetRef` is
  `https://api.staging.foleon.cloud/image/1493060` — the go-to recording for block-background tests (hotspots
  need a bg image, hence it exists). · refs: `doc/119281/pages/812305` · sheet: none
- 2026-08-03 · Editor · Gallery gear unreachable with a scroll effect (PROD-3270) — BLOCK SCROLL-EFFECT
  BACKGROUND STEALS HIT-TESTING FROM STATIC BLOCK CONTENT. Turning a scroll effect on a block background adds
  a 3-node layer — `.parallax-consumer` (`position: fixed`, `transform: translateY(...)`, `overflow: hidden`)
  nested in an `absolute` wrapper inside an `absolute` + `overflow: clip` wrapper. Verified via
  `document.elementsFromPoint` + per-row `contains()`: that layer is NOT a descendant of the block's content
  subtree, and with the effect OFF the 3 nodes don't exist at all. Every `z-index` is `auto` and every
  `pointer-events` is `auto`, so plain paint order applies (positioned beats static in-flow at the same
  stacking level) and the layer lands ABOVE `.ripley__Gallery--gallery__container` (`position: static`).
  Editor consequence: hovering gallery-but-not-card space hits the parallax layer, the gallery never registers
  as hovered, and its active indicator — which hosts the settings gear — never appears. Hovering a CARD still
  works because the gallery's per-card wrapper is `position: relative; z-index: 1`, out-painting the parallax
  layer; and the card's own `.ripley__CardItem--background--container` at `z-index: -1` does not fall behind
  the parallax layer because that `z-index: 1` wrapper creates a stacking context that traps it. Same class as
  the image border-vs-animation and card-radius-inherit entries above: a layer added for animation/parallax
  ends up co-planar with editor interaction chrome. At-risk beyond the editor: static, unpositioned
  interactive content inside a scroll-effect block (positioned content escapes via its own z-index).
  ROOT CAUSE + FIX: the two parallax wrappers in `background/viewer/parallax/components/parallax.consumer.tsx`
  (`ParallaxConsumerWrapper`, absolute + the `Container` that carries `.parallax-consumer`, fixed) never declared
  `pointer-events: none`, while the element they wrap — `BackgroundContainerStyles` / `.viewer-background` in
  `background/viewer/background.shared.tsx` — always did. So the non-parallax render is click-through and the
  parallax render is not; adding `pointer-events: none` to `ParallaxConsumerWrapper` alone restores parity
  (`pointer-events` is inherited, so the inner `Container` and `BackgroundAnimationClip` are covered — patching
  only the inner `.parallax-consumer` does NOT fix it, because its absolute PARENT still hit-tests).
  Safe because nothing interactive lives in that subtree: `withParallaxConsumer` has exactly ONE usage
  (`background-image.container.tsx`), video backgrounds never take the parallax path, the background renders no
  `children`, and hotspots are siblings of the background rather than descendants (the "hotspots disappear
  outside the background" comment on `.viewer-background`'s `overflow: hidden` is stale). Verified: ci:compile,
  868 core unit tests, 25 editor integration (hotspot + map-form), 174 viewer integration (linking + gallery),
  no screenshot drift. · refs: PROD-3270 · `parallax.consumer.tsx` · `background.shared.tsx` · sheet: none
- 2026-08-03 · Tests & Playwright · Parallax backgrounds are effectively untested — nearly every editor/viewer
  fixture sets `background.scrollRate: "1"`, and `background-image.container.tsx` treats `undefined | '1'` (and
  `prefers-reduced-motion`, and template/overlay routes via `disableParallax`) as "no parallax" — so the whole
  parallax subtree is skipped. The ONLY integration fixture that reaches it is
  `editor-doc/@entities/map-form/__mocks__/load-empty-map-forms/load-empty-map.forms.ts` (`scrollRate: '0'`),
  and it asserts nothing about it. Consequence: a parallax-only regression passes CI. Cheap guard added in
  `background/viewer/__tests__/background-image.container.test.tsx` — render with `scrollRate="0.5"`, then
  `getComputedStyle(container.querySelector('.parallax-consumer').parentElement).pointerEvents === 'none'`;
  jsdom DOES resolve styled-components class rules for this (returns `''` when the declaration is absent, so the
  test genuinely fails without the fix). Note core has NO jest-dom (`toHaveStyle` is unavailable) — use raw
  `getComputedStyle`. · refs: `background-image.container.test.tsx` · sheet: none
- 2026-08-05 · Tests & Playwright · Editor chrome unclickable, cause unknown — TECHNIQUE for any "editor chrome
  disappears / isn't clickable" bug here: press-to-inspect `elementsFromPoint` probe, generalized (v2, supersedes
  the gallery-specific v1). Paste once, hover the suspect area, press `q`; no target selector needed up front:
  ```
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
  `els` is PAINT order (topmost first), not an ancestor chain — it interleaves unrelated subtrees, so read
  `containsPrev` before assuming containment. `style` holds ALL computed CSS properties per layer (not a
  curated subset) via `window.$probe`, so a suspect property you didn't think to list up front is still there.
  Diff helper across two rows of one call, or across two separate `$probe` captures (e.g. feature on vs off):
  ```
  window.$diffStyle = (i, j) => {
    const a = $probe[i].style, b = $probe[j].style, out = {}
    for (const k of Object.keys(a)) if (a[k] !== b[k]) out[k] = { [i]: a[k], [j]: b[k] }
    return out
  }
  ```
  Diffing (on vs off, working element vs broken one) is what actually localizes the bug — the delta is the
  culprit. Keep the probe in DevTools → Sources → Snippets so it survives the constant reloads. Anchor follow-up
  greps on the semantic `ripley__*` classes (they come from identifier constants); `sc-*` hashes are
  build-generated and ungreppable — for those, React DevTools names the component. · refs: PROD-3270 · sheet: yes
- 2026-08-14 · Build & tooling · "Where do ripley's feature flags come from?" returns nothing useful from a
  source grep — flags are **Unleash behind a proxy**, and almost every in-repo hit for `featureFlag` is a test
  fixture, so a source-only search reads as "ripley has no flag system". Config is two runtime values,
  `unleashProxyEndpoint` / `unleashProxyClientKey`, read from `window._env_` in the browser and `process.env` on
  the server (`packages/foleon-core/src/config/urls.ts:108-111`) — runtime injection, so one built bundle serves
  every environment and nothing is inlined at build time. The proxy exists so the real Unleash API key never
  reaches the browser. Wire shape is Unleash's standard frontend payload,
  `{toggles:[{name, enabled, variant:{name, enabled}}]}`; names are `editor.<camelCase>`
  (`editor.multiRowBlocks`, `editor.spellCheck`, `editor.monitoring.dataDog`), and the mock in
  `foleon-core-editor/cypress/fixtures/shared/feature-flags.ts` lists ~26 of them — that fixture is the fastest
  way to read the live flag set. Tests intercept on the URL matching `feature-proxy|unleash-proxy`
  (`tests/integration/shared/utils/routes/feature-flag-route.ts`, `foleon-core-viewer/tests/utils/utils.ts:127`).
  Ripley uses `variant` only as a disabled stub in fixtures, so variants are provisioned-for but unused.
  · refs: `foleon-core/src/config/urls.ts:108-111`, `cypress/fixtures/shared/feature-flags.ts` · sheet: none

- 2026-08-14 · Core / rendering · Mixpanel event missing / no Mixpanel SDK to grep for — ripley NEVER calls a
  Mixpanel SDK; grepping `mixpanel` finds only ONE hit, a test title
  (`foleon-core-viewer/src/apps/previewer/entry.personalization.test.tsx` "should call trackData with data for
  MixPanel"). Everything is pushed to `window.dataLayer` and GTM fans out to Mixpanel downstream, so a missing
  event is a GTM-container problem, not a code problem — the app cannot know whether it reached Mixpanel.
  TWO SEPARATE tracking modules, easy to confuse: (1) `foleon-core/src/shared/tracking/index.ts` — PRODUCT
  analytics for the editor: `trackData(eventName, data)` pushes `{event: eventName, ...data}`; event names live
  in the `trackingEvents` enum (28 exactly: addBackgroundImage, replaceImage, createBlock, publishPublication,
  republishPublication, openPreview, createPage, changedAttribute, viewportChange, activatedFont, …).
  **⚠️ EXTENDED 2026-08-14 — that enum is only HALF the named events.** A *second*, larger catalogue with the
  **same export name** lives in a different package: `foleon-core-editor/src/@shared/tracking/index.ts:97`,
  `export const trackingEvents = {…}` with **74 keys** (a const object, not an enum). The two overlap by 11, so
  the union is **91 distinct named events**; `createElement`, `codeEmbedCreated`, `aiMenuAction` and
  `switchToContentStudio` exist only in the editor one, while `changedAttribute`, `replaceImage` and
  `saveAsBlockTemplate` exist only in the core enum. Counting either alone under-reports, and `grep -c` for
  indented `key:` lines over that whole editor file returns **92** because it also catches `TrackingCategory`,
  `TrackingEvent` and `TrackingLabel` — extract the object body before counting. Second trap in the same file:
  a `useTracking()` hook holding exactly one event (`userLogin`) — landing on it alone makes ripley look barely
  instrumented. **Corrected 2026-08-17: that hook is at line 246, i.e. 150 lines BELOW the catalogue at 97, not
  above it.** The earlier "its FIRST export" phrasing here was wrong in direction and had propagated into a
  Notion doc; both are fixed. **There are FOUR directories
  named `tracking/`** — `foleon-core/src/{common,shared}`, `foleon-core-viewer/src/common`,
  `foleon-core-editor/src/@shared` — so characterise coverage only after reading all four. Real call-site count
  across `packages/*/src` excluding tests: **182 in 93 files** (56 files in foleon-core-editor, 17 in the
  viewer, 10 in foleon-core, 9 in navigator, 1 in cookie-consent). Third system beyond GTM and GA:
  **Foleon Analytics**, an InstantAnalytics script injected into published docs
  (`foleon-core/src/common/tracking/scripts/foleon-analytics.ts`) — the reader-engagement product sold to
  customers, distinct from the internal product analytics above. Beyond both catalogues there are
  free-string call sites that BYPASS the enum (`content.store.ts` `'translate'`/`'undo'`/`'redo'` — and it
  imports `trackDataGTM as trackData`, a different function under the same local name; `assistant/container.tsx`
  `'textAssistanceIdea'`), so the enum is NOT the full event catalogue — grep `trackData(` for that.
  Helpers wrap it: `trackAttribute` (all → `changedAttribute`, suppresses ITEM_SECTION min/max height+width, and
  for `display` on non-xl viewports rewrites `name`→viewport label + `value`→show/hide), `trackPlaceMedia`
  (derives `source` = unsplash|<provider>|stock|custom by sniffing `//cdn.foleon.com/upload/stock/` in
  `_links.image.href`), `syncTrackData` (a promise wrapper, resolves regardless). `trackThis` is the legacy
  GA-UA shape — every call emits the SAME event name `editorEvent` with category/action/label/value props
  (`TrackingCategory`/`TrackingEvent`/`TrackingLabel` enums). (2) `foleon-core/src/common/tracking/**` — READER
  analytics for published docs (`events/google-and-foleon-analytics.ts`, `ITrackingGTM.gtmCode`, per-doc
  `gtm_code` from the API `hal.ts`, `INSTANT_ANALYTICS_URL` + `PARDOT_TRACKING_SCRIPT_URL` in `config/.env.*`).
  Form submissions push their own dataLayer payload directly (`entities/form/viewer/form.viewer.tsx`
  `pushFormDataToWindowDataLayer`), not via `trackData`. GTM snippet is inlined at
  `foleon-core-editor/src/index.html:62`. Playwright strips `googletagmanager` from recordings
  (`create-route-from-recording.ts` thirdPartyFilterWords) → tracking is absent under integration tests by
  design. Two sharp edges in `shared/tracking/index.ts`: `trackData`'s catch does `throw new Error()`, DISCARDING
  the original error and re-throwing an empty one into the caller (a tracking failure can break the user action
  it was instrumenting — it does not fail soft despite looking like it does); and `trackingEvents`/`ItemEnum`/
  `TrackingCategory` are `enum`s, violating the const-assertion-union convention — legacy, don't cargo-cult when
  adding events. · refs: `foleon-core/src/shared/tracking/index.ts` · `common/tracking/**` · sheet: none
- 2026-08-03 · Build & tooling · 403 Forbidden from local requests — run `sh scripts/prepare-auth.sh`.
  Recorded during the PCS-6 migration: this finding existed only on the Notion cheat sheet (row CS-2) and in
  no Claude-facing file, which PCS-11 forbids — the log is authoritative and a finding must never live only in
  the mirror. Date is when it was logged here, not when it was learned.
  · refs: `scripts/prepare-auth.sh` · sheet: none

- 2026-08-07 · Editor · blue options-buttons bar covers a one-line text element so it can't be clicked to edit —
  `OptionsButtons` (`@shared/options-buttons-new/index.tsx`) maps `positionY: 'inside'` to `top: 0` and
  `'outside'` to `top: -27`, and the bar is a fixed `dragIconHeight = 27`px tall. So `'inside'` always eats the
  top 27px of the entity's `ActiveIndicator` box (`@common/active-monitor`, a `Relative` — it is the bar's
  offsetParent; `marginBottom` is real CSS margin so it does not add to that box). Text picks `'inside'`
  whenever it is merely hovered. Any text entity shorter than ~27px is therefore 100% covered on hover. Fix
  (PROD-3457) measures the
  `TextViewerContainer` node (already available in `text.editor.tsx` via `useRefState`) with a ResizeObserver
  and flips `positionY` to `'outside'`. Note the jsdom `ResizeObserver` in `test-utils/setup.ts` is a no-op
  stub (observe/disconnect are `vi.fn()`), so only the synchronous first measurement is testable — keep the
  height predicate a separately exported pure function. UNVERIFIED / DO NOT REPEAT: reading
  `&& !isParentCardItem` in `options-button.tsx` suggests text inside a `card-item` is pinned to `'inside'`,
  but observed behaviour in the editor contradicts that — the bar renders above the text in a card, and one
  bar appears to serve both card texts. The real card positioning is NOT understood; do not reason about it
  from that boolean alone. Note the PROD-3457 fix's `!hasRoomForOptionsButtonsInside ||` sits outside that
  parenthesised group, so it does override the card branch for short texts — a card path that was never
  verified in a browser.
  · refs: `@entities/text/options-buttons/use-options-buttons-placement.tsx`, `@shared/options-buttons-new/use-options-buttons.tsx`, PROD-3457 · sheet: no
- 2026-08-11 · Core / rendering · Swapping a `div` for a `button` in a `@foleon/core` entity looks fine in the
  editor but breaks layout in the viewer — the two hosts ship DIFFERENT global resets. Editor imports Tailwind
  preflight (`foleon-core-editor/src/tailwind.css:1` → zeroes border/padding/margin, `font: inherit`); viewer
  ships only sanitize.css (`foleon-core-viewer/src/styles/sanitize.ts:104`) which DELIBERATELY preserves native
  buttons (`-webkit-appearance: button`). So in the viewer a bare `<button>` inherits UA `display:inline-block`
  (stacked children go side by side), `border: 2px outset` (black ring), `padding: 1px 6px` (+ any
  `overflow:hidden` clips the icon) and UA `font`/`line-height` (wrong box height). Neither reset fixes
  `display`, so inline-block bites BOTH apps. Rule: any `<button>` in `@foleon/core` must carry its own UA
  reset in the styled-component — `display: block; padding: 0; border: 0; margin: 0; font: inherit;
  text-align: inherit; appearance: none;` — placed BEFORE the `${({ styles }) => styles}` interpolation so
  document theme styles still win. Verified: div and reset-button both compute 40×47 block stacked; unreset
  button computes inline-block/2px/6px. · refs: `column-scroll/viewer/common/column-scroll.buttons.tsx`,
  PROD-3885 · sheet: no
- 2026-08-11 · Tests & Playwright · Editor Playwright suite passes while the viewer is visually broken — the
  column-scroll spec `editor-doc/@entities/column/column.settings-panel-navigation.test.ts` asserts only
  background-color, color, border-radius, visibility and role+name. It asserts NOTHING about box geometry, so a
  `div`→`button` regression that reflows the buttons side by side and adds a UA border sails through green.
  Geometry assertions (relative y of up vs down, `border-width`) are the missing coverage. Also: there is no
  viewer-side test for these buttons at all. · refs: `column.settings-panel-navigation.test.ts`, PROD-3885 ·
  sheet: no
- 2026-08-18 · Editor · a child entity's options bar renders BEHIND the block/column options bars, or behind the
  green spacing overlay of the block above, and raising its z-index changes nothing — follow-up to the 2026-08-07 PROD-3457 entry above (same ticket): once a short text's
  bar flips to `'outside'` (`top: -27`) it lands in the same 27px band as the block and column bars, which paint
  over it. ROOT CAUSE: every bar carries the SAME inline `zIndex: 37` (`OptionsButtons` → `OptionButtonsContainer`;
  the styled `Container`'s own `z-index: 35` is always overridden by that inline value), but `StyledColumnContainer`
  in `column.editor.tsx` wraps all column children in `z-index: 13`. It is `position: static` — yet it IS a flex
  item (`.im-column-inner` is `display:flex`, and `ColumnStyledContainer` also forces `display:flex` onto its
  children), and per the flexbox spec a flex item with a non-auto z-index CREATES A STACKING CONTEXT even when
  unpositioned. So a child bar's 37 is only ever compared with its siblings inside that box; against the outside
  world the whole column subtree is one flat layer at 13, and the column/block bars at 37 win. Verified in Chromium:
  `9999` and even `9999 !important` on the child bar change the paint order not at all. Levers that DO work:
  (a) drop the ancestor bars BELOW 13 while the child bar needs to win — what PROD-3457 shipped, as
  `body:has(.foleon-option-buttons__priority) &.foleon-option-buttons__outside:not(.foleon-option-buttons__priority)
  { z-index: 12 !important }` on `Container` (`!important` is REQUIRED — the 37 is inline; `:has()` keeps it scoped
  to while a prioritised bar is actually mounted and self-reverts on mouseleave with no JS state, and the
  `.outside` guard spares the `keepInside` leadgen / sm-overlay bars that sit at `top: 0` over real content);
  (b) delete the `z-index: 13` — also works (the child bar then wins on DOM order alone) but it is load-bearing:
  it lifts column content above z-AUTO positioned siblings, notably the desktop top space-resizer, which is what
  the "options buttons that are rendered outside cannot be used" comment in `spacing-resizer.module.css` is about.
  Note 13 does NOT beat the resizers at 14, so a child's bar is ALREADY below the side/bottom space-resizers today.
  Portaling the bar out is the only true escape, and the codebase already anticipates it: the unused
  (`@knipignore`) floating-ui prototype `@shared/options-buttons-new/use-options-buttons.tsx` carries a
  `zIndexesForLevel` map (page 50 / block 60 / column 70 / column child 80 — i.e. deepest wins, exactly what QA
  asked for) plus a TODO saying a React Portal is probably needed "to break out of the zIndex flow".
  The z-index zoo in this area: 12 yielded · 13 column content · 14 space-resizers · 15 `.column-resizer__inner` gutter
  drag pill · 16 prioritised column content · 20 block dnd indicator · 30 hotspot container · 31 BlockHoverIndicator ·
  35 Container default · 37 all bars · 81 invisible card-item child bar · 121 block resizer · 251 RTE text toolbar.
  SECOND HALF OF THE SAME BUG, reported by QA on 2026-08-18 and fixed the same day: yielding the ancestor BARS does
  nothing about the space-RESIZERS, which is why a short/focused text at the top of a block still ended up under the
  green spacing overlay of the block ABOVE. Mechanism, verified: the column's `SpacingResizer` is a SIBLING of
  `StyledColumnContainer` inside `ColumnStyledContainer` (`@foleon/core` `column.viewer.tsx`), which is
  `position: relative` with z-index AUTO — so it is NOT a stacking context and the resizer's `z-index: 14` escapes to
  the page-level context. `BlockStyledContainer` (`block/viewer/common/inner.tsx`) and `RowStyledContainer` are also
  `position: relative`/no z-index → also not stacking contexts, so 14 (upper block's resizer) and 13 (lower block's
  column content) compare DIRECTLY across blocks, cross-block, regardless of DOM order. The overlay in the report is
  the COLUMN padding resizer specifically — identified from its colour: `spacing-resizer.column.tsx` passes
  `extraStyles={{ backgroundColor: 'rgba(0, 174, 0, 0.8)' }}`, and the 0.8 alpha is exactly why the buried purple bar
  is still visible-but-green-tinted in the screenshot (the `.padding` class colour `#78c883` is opaque and would hide
  it entirely). SHIPPED FIX: scope the lift to the ONE column that owns the prioritised bar, on `StyledColumnContainer`
  — `&:has(.foleon-option-buttons__priority) { z-index: 16 }` (constant
  `priorityColumnContentStackingZIndex = columnResizeHandleZIndex + 1`). 16, NOT 15: `.column-resizer__inner` (the
  10x20 column gutter drag pill, `column.editor.tsx`) is ALREADY at 15, its `StyledResizeHandlerContainer` wrapper is
  `position: relative` with z-index auto so that 15 escapes to page level too, and it renders AFTER the columns — so at
  an equal 15 the pill wins the tie on DOM order and re-buries the bar. Measured in Chromium: at 15 the bar beats the
  resizer but loses to the pill; at 16 it beats both. Whenever you lift something out of this trap, grep for the
  EXISTING occupants of the target value (`z-index: 1[4-9]`) — 15 and 30 are both already taken here
  (`hotspot.editor.tsx` sets 30 with a comment saying it is escaping this very band). Self-reverts on blur with no JS state, exactly like
  the ancestor-yield rule, and no `!important` is needed here because the 13 is from the stylesheet, not inline.
  REJECTED alternative: `body:has(.priority) .bottom/.left/.right { z-index: 12 }` in
  `spacing-resizer.module.css` — it drops EVERY resizer on the page for as long as any text is focused, so the user
  cannot grab any spacing handle until blur. The 15 does not steal the resizers' own drag zones, because a resizer sits
  at `bottom/left/right: 0` of `ColumnStyledContainer`'s PADDING box while `StyledColumnContainer` is a flex item
  confined to the CONTENT box — they only overlap in the 27px band where the outside bar is, which is the point.
  Note `spaceResizerZIndex = 14` in TS MIRRORS the hardcoded 14s in `spacing-resizer.module.css` (a CSS module cannot
  import the constant); both files now carry a "change both together" comment and a unit test asserts the ordering
  13 < 14 < 15 < 37. Portaling remains the only true escape and is still unimplemented.
  · refs: `@common/option-buttons/option-buttons.container.tsx`, `column.editor.tsx`,
  `@common/space-resizer/spacing-resizer.module.css`, `@entities/column/spacing-resizer/spacing-resizer.column.tsx`,
  PROD-3457 · sheet: none
- 2026-08-14 · Editor · a stacking/paint-order question you want answered WITHOUT booting the editor — hand-build a
  minimal HTML mirroring the real nesting + z-indexes (read them out of the styled-components) and drive it with
  the repo's own Chromium: `node script.mjs file:///…/repro.html`, importing playwright by ABSOLUTE path
  since a scratchpad script resolves nothing from the repo. CORRECTED PATH (2026-08-18): it is
  `<repo>/node_modules/.pnpm/playwright-core@1.50.1/node_modules/playwright-core/index.js` — there is NO
  `playwright-core` under `@playwright+test@1.50.1/node_modules/`, so the path in the original entry throws
  ERR_MODULE_NOT_FOUND. It is CJS, so `import pkg from …; const { chromium } = pkg`. Probe with `document.elementsFromPoint` at the
  CENTRE OF THE RECT INTERSECTION of the two elements in question (`(max(left)+min(right))/2`) — probing one
  element's own centre silently misses the overlap and every scenario looks identical, which is how a first pass
  "proves" nothing is wrong. Then flip one property per scenario in `page.evaluate` and print the topmost id: that
  gives a before/after/reverted table in ~2s per run, no auth, no `pnpm build:integration`, no doc fixture. Good
  for z-index/stacking-context/pointer-events questions; useless for anything depending on real styles or data.
  · refs: PROD-3457 · sheet: none
- 2026-08-14 · Tests & Playwright · a new vitest file's `@common/...`-style path alias fails to resolve while the
  identical import works from source — the editor's `tsconfig.json` has `"exclude": ["node_modules",
  "**/*.test.ts", "**/*.test**.ts", "dist"]`, and `vite.config.ts` gets its aliases from `vite-tsconfig-paths`,
  which reads that tsconfig. So a `*.test.ts` file is OUTSIDE the tsconfig and gets NO path aliases →
  `Failed to resolve import "@common/…"`. `*.test.tsx` is not excluded and works. That is why every existing test
  here is `.test.tsx`, even the ones testing a pure function with no JSX. Second trap in the same package: run
  tests only via `vitest --config src/vite.config.ts` (i.e. `pnpm editor:test`) — a bare `npx vitest` finds no
  aliases AND no jsdom, so everything fails with `document is not defined`. Third: a pure helper exported from
  `@shared/options-buttons-new/index.tsx` is NOT unit-testable through the barrel — importing it drags in
  `@common/ai-assistant/ai-assistant.provider.tsx` → `@assistant/chat-sdk`, which explodes with `exports is not
  defined in ES module scope`; put the helper in its own module and import that directly.
  · refs: `packages/foleon-core-editor/tsconfig.json`, `src/vite.config.ts` · sheet: none

- 2026-08-17 · Core / rendering · "How many tracking functions does ripley have?" gets answered as 7 from the
  table people circulate — **it is 12 exported `track*` functions across 3 packages, and four of the NAMES are
  defined more than once**, which is the actual hazard (an import can resolve to a different implementation than
  you think). Verified inventory: `foleon-core-editor/src/@shared/tracking/index.ts` — `trackData:10`,
  `trackDataGTM:39`, `trackThis:73`, `syncTrackData:90`, `trackPlaceChart:221`, `trackPlaceMedia:228`;
  `foleon-core/src/shared/tracking/index.ts` — `trackData:50`, `trackThis:102`, `syncTrackData:117`,
  `trackAttribute:191`, `trackPlaceMedia:233`; `foleon-core-viewer/src/common/tracking/tracking.utils.ts` —
  `trackData:27`. Duplicated names: `trackData` ×3, `trackThis` ×2, `syncTrackData` ×2, `trackPlaceMedia` ×2
  (the circulated table omits `syncTrackData`'s second copy, `trackAttribute` and both `trackPlaceMedia`).
  Three further facts verified in the same pass: (a) the **throw-in-catch hazard exists TWICE**, not once —
  `foleon-core-editor/…/index.ts:24` rethrows `new Error(error.message)` and `foleon-core/…/index.ts:62` throws
  a bare `new Error()`; the editor copy was previously unlogged. (b) **The editor's tracking module has ZERO
  references to environment**, so editor events fire in local dev; the *viewer* does gate —
  `isTrackingAllowed` (`foleon-core-viewer/src/common/tracking/tracking.utils.ts:3`) allows only `publish` and
  `zip`. So the gate exists in ripley, just never where the editor tracks — do not report this as "ripley has no
  env gate". (c) **GTM container is `GTM-NFJM6Z`**, inlined at `foleon-core-editor/src/index.html:67` and
  `foleon-core-viewer/src/apps/previewer/index.html:41`; a *different* container `GTM-KWS7TZG` appears in built
  viewer assets, so the container ID is not one global constant. Counts re-confirmed exactly: core enum 28,
  editor const 74, overlap 11 (addedSwatch, createBlock, createElement, createPage, openMediaLibrary,
  openPreview, progressVideo, publishPublication, republishPublication, userLogin, viewportChange), union 91.
  · refs: `packages/foleon-core-editor/src/@shared/tracking/index.ts`,
  `packages/foleon-core/src/shared/tracking/index.ts`,
  `packages/foleon-core-viewer/src/common/tracking/tracking.utils.ts`, `packages/navigator/src/index.tsx:17`
  · sheet: none

- 2026-08-18 · Build & tooling · `pnpm editor:dev` dies before Vite starts with
  `[ERR_PNPM_MISSING_TIME] The metadata of @tanstack/router-core is missing the "time" field` — NOT a code or lockfile
  problem and nothing to do with the editor. `pnpm run <script>` in pnpm 11.1.1 runs a deps-status check
  (`runDepsStatusCheck`) that shells out to `pnpm install` first; the registry metadata for `@tanstack/router-core` (a
  direct dep of `foleon-core-viewer-dynamic`) lacks the `time` field that pnpm's default `resolution-mode=lowest-direct`
  needs, so the install aborts and takes the dev server with it. The install has nothing to do: the log says
  `downloaded 0, added 0`, node_modules is already complete. `npm_config_verify_deps_before_run=false` does NOT
  suppress the check (tried, still ran). WORKAROUND that works — skip `pnpm run` entirely and do what the script does,
  from `packages/foleon-core-editor`: `chmod +x ../../env-dev.sh && ../../env-dev.sh && cp ../../env-config.js
  ./src/env-config.js && node ./scripts/kill-port.js 3000 && NODE_ENV=development ./node_modules/.bin/vite serve ./src`
  → `VITE v4.5.14 ready`, https://localhost:3000/ (HTTPS, not HTTP). Note `predev` is what copies `env-config.js` into
  `src/` — this is the dev-server analogue of the known `cp src/env-config.js dist/env-config.js` build fix, and
  skipping it is another way to get an editor that will not boot. The registry-side fix the error suggests is
  `resolution-mode=highest`, which mutates pnpm config, so prefer the bypass for a one-off.
  · refs: `packages/foleon-core-editor/package.json` (`predev`), `env-dev.sh` · sheet: none

- 2026-08-18 · Editor · core's `dist` LOOKS stale next to its `src` and you are about to rebuild for nothing —
  `find packages/foleon-core/src -newer packages/foleon-core/dist` compares against the DIRECTORY's mtime, which only
  changes when a top-level entry is added (it read Jul 6 while dist was actually built Aug 14), so it reports ~48 bogus
  "newer" files. Compare newest FILE to newest FILE instead:
  `find <dir> -type f -exec stat -f '%Sm %N' -t '%Y-%m-%d %H:%M' {} \; | sort -r | head -3` on both trees. Also note
  macOS `awk` has no `strftime`, so `stat -f %m | awk strftime` fails — use `stat -t` for formatting. Rebuild core only
  when a `packages/foleon-core/src` file is genuinely newer than the newest `dist` file, or when you changed core
  yourself; an editor-only change never needs it. · refs: `packages/foleon-core/dist` · sheet: none

- 2026-08-18 · Tests & Playwright · you want a real paint-order/stacking assertion in the editor and assume it needs a
  new HAR — it does not, and jsdom is more capable than expected. THREE findings. (a) **jsdom DOES evaluate `:has()`**
  and resolves the cascade: a styled-component with `z-index: 13; &:has(.probe) { z-index: 16 }` computes "13" then
  "16" via `getComputedStyle` in Vitest+jsdom. So a `:has()`-based rule IS unit-testable — assert the computed z-index
  on the wrapper with and without a matching descendant, and render the REAL class producer inside it
  (`OptionButtonsContainer hasPriorityOverAncestors`) so the test wires the actual class to the actual selector. jsdom
  still has no layout, so paint order itself remains Playwright-only. To make a styled-component's rule testable
  without exporting the component, extract the rule into an exported `css` fragment beside its constants and
  interpolate it — DRY and testable at once. (b) Integration docs are HAR replays (`__mocks__/<name>/recording.zip`)
  and you do NOT need to record a new one: dump each recording's doc tree first. The payload is the file inside the zip
  with the most `"refs"` occurrences; walk `content.page[*].refs` → `content.block[*]` → `row` → `column` to print
  each column's children. `load-column` (url `doc/98689/pages/768871`) is 2 blocks x 2 columns, each column holding one
  text — the exact multi-block arrangement QA reported. `load-column-spacing` is the intuitive pick and is USELESS here:
  zero text entities. (c) The DOM is the only authority on selectors: those texts are `header-one`/`blockquote`
  text-items, NOT `paragraph`, so `paragraphSelector` matches nothing — use `textContainerSelector`
  (`core-editor__entities__text__container`). Diagnose by waiting `page.waitForTimeout(8000)` after
  `initTestFromRouteRecording` and dumping `[data-testid]` counts; do NOT `waitFor()` `[data-testid]` first, it resolves
  to the permanently hidden `topbar-drawer` and times out. Reading counts immediately after
  `initTestFromRouteRecording` returns 0 for everything — it resolves before the doc renders, so the first real
  assertion must be auto-waiting.
  · refs: `tests/integration/editor-doc/@entities/text/text.options-buttons-stacking.test.ts` · sheet: none

- 2026-08-18 · Tests & Playwright · a stacking-bug Playwright test passes for the wrong reason —
  `overlayOptionsButtons` (`core-editor__common__options-buttons-container`) is on EVERY bar, and inside a column the
  COLUMN's own bar renders before `StyledColumnContainer`, so `column.getByTestId(overlayOptionsButtons).first()` grabs
  the ancestor bar — the one that deliberately yields to z-index 12 — and the test "fails" against the resizer for a
  reason unrelated to the entity bar. Scope through the entity's own indicator
  (`getByTestId(textActiveIndicator).first().getByTestId(overlayOptionsButtons).first()`) AND assert
  `toHaveClass(/foleon-option-buttons__priority/)` so a future locator change cannot silently pick the wrong bar.
  Two more traps in the same spec: `changeElementSpacingByInput` asserts the rendered band equals the value you set, so
  it CANNOT set a horizontal spacing below 11 (`.horizontal { min-height: 11px }` floors it — passing 0 fails with
  "Expected 0, Received 11"); use 11 as the minimum. And ALWAYS mutation-test a stacking spec: neuter the fix, confirm
  red, and disable the z-index assertion on a second run to prove the HIT TEST is independently non-vacuous — a
  `toHaveCSS('z-index')` assertion that fires first will mask a hit test that never actually runs. The hit test must
  probe the centre of the RECT INTERSECTION of the two elements; helper lives in
  `tests/integration/shared/test-helpers/paint-order.ts`. Scoping a run works fine in the EDITOR config (unlike the
  viewer's): `PLAYWRIGHT_ENV=development npx playwright test --project="Doc Editor" -g "<title>"`, and
  `reuseExistingServer` means it reuses an already-running dev server on 3000 — no `build:integration`.
  · refs: `tests/integration/shared/test-helpers/paint-order.ts`, `resize-and-assert.ts` · sheet: none

- 2026-08-21 · Core / rendering · a GTM variable reads a value from an event that did not set it, or a viewer
  `trackData` call produces no dataLayer push at all — ripley's dataLayer is **flat, never cleared, and pushed to
  from five places that bypass the wrappers**. (a) **No reset anywhere:** no wrapper sets keys to
  `undefined`/`null`, no `dataLayer.length = 0`. Every push spreads a fresh object
  (`{event: eventName, ...data}`, `foleon-core-editor/src/@shared/tracking/index.ts:18`), so GTM's
  last-value-wins variable model keeps any key an earlier event set and a later one omits. Concrete leak:
  `trackPlaceChart:221` pushes `elementType`+`chartType`, then `trackPlaceMedia:228` pushes
  `elementType`+`source` with no `chartType` — a GTM tag on `createElement` still reads the stale chart type.
  Worst case `entities/form/viewer/form.viewer.tsx:457` (`pushFormDataToWindowDataLayer`) spreads the WHOLE form
  API response (`FormSubmissionSuccess`, contact id included) onto the layer, uncleaned. Any "wrong value in
  GTM" bug is therefore a *previous* event's payload, not the current one — read the whole session's pushes, not
  the failing one. (b) **Flat top-level keys, zero namespacing:** `event` is the only discriminator; everything
  else sits at the root and is shared across events, so `category`/`action`/`label`/`value` from `trackThis`
  (`foleon-core/src/shared/tracking/index.ts:107`) collide with the `action`/`label` pushed by
  `common/tracking/events/google-and-foleon-analytics.ts:142`, and `elementType` is reused by createElement /
  replaceImage / createBlock. The ONLY namespacing in the repo is string interpolation, not nesting:
  `cookie-consent/src/modules/gtm/index.ts:12` → `allow_cookieconsent_${option}`. (c) **Five direct
  `window.dataLayer.push` sites that never go through `trackData`** (so a fix or a schema change in the wrappers
  misses them): `@shared/tracking/index.ts:54` (legacy `trackDataGTM`, which also maps `args.callback` →
  `eventCallback`), `google-and-foleon-analytics.ts:142`, `form.viewer.tsx:457`,
  `cookie-consent/src/modules/gtm/index.ts:10`, and `foleon-core-viewer/src/common/tracking/scripts/
  google-analitics-4.ts:72` (`window.gtag` shim pushing `arguments`). (d) **The viewer's `trackData` silently
  DROPS unknown events** — `foleon-core-viewer/src/common/tracking/tracking.utils.ts:28` early-returns unless the
  name is in its own 23-key `TrackingEvents` const (`:6`, a THIRD catalogue beyond the core enum's 28 and the
  editor const's 74); the editor and core copies have no such filter. A viewer event that "does not fire" is
  usually just absent from that list, not broken. (e) **Container `GTM-NFJM6Z` is hardcoded in the inlined
  snippet and identical in every environment** — `foleon-core-editor/src/index.html:67` and
  `foleon-core-viewer/src/apps/previewer/index.html:41`. It is NOT read from `env-config.js` (loaded right after,
  `previewer/index.html:46`) and there is no GTM-named env var in the repo, so dev/staging/prod all feed one
  container. **Corrects the 2026-08-17 entry above:** `GTM-KWS7TZG` is not in built viewer assets — it appears
  only in a Cypress fixture (`foleon-core-viewer/cypress/mocks/data/tracking/pardot/
  pardot-off-cc-off-remarketing-set-to-0.json`) as a customer's own per-doc `gtm_code`
  (`foleon-core/src/type/api/hal.ts:383`, surfaced as `gtmCode` in
  `foleon-core-editor/src/@lib/settings-modal/components/marketing.tsx:68`), which is per-document, not
  per-environment. · refs: `packages/foleon-core-editor/src/@shared/tracking/index.ts`,
  `packages/foleon-core/src/shared/tracking/index.ts`,
  `packages/foleon-core-viewer/src/common/tracking/tracking.utils.ts`,
  `packages/foleon-core/src/entities/form/viewer/form.viewer.tsx:455`,
  `packages/cookie-consent/src/modules/gtm/index.ts` · sheet: none
