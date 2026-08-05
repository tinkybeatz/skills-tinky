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
- 2026-08-03 · Build & tooling · 403 Forbidden from local requests — run `sh scripts/prepare-auth.sh`.
  Recorded during the PCS-6 migration: this finding existed only on the Notion cheat sheet (row CS-2) and in
  no Claude-facing file, which PCS-11 forbids — the log is authoritative and a finding must never live only in
  the mirror. Date is when it was logged here, not when it was learned.
  · refs: `scripts/prepare-auth.sh` · sheet: none
