# ripley — discoveries log

Append non-obvious findings here as you learn them: gotchas, implicit conventions,
architectural "why"s, sharp edges. Keep entries short and dated. When this log grows
heavy, promote the stable facts up into `project-facts.md` and prune the rest.

Format: `- YYYY-MM-DD — <finding>`

## Discoveries
- 2026-07-20 — Package scope is `@foleon/*`, **not** `@ripley/*`. The legacy Cursor rule
  (`.cursor/rules/global-ripley-rule.mdc` in the ripley checkout) still says `@ripley/` —
  that line is stale; trust `package.json` / `pnpm-workspace.yaml`.
- 2026-07-20 — Fuller (historical, partly aspirational) convention lists live in the
  ripley repo's `.cursor/rules/*.mdc`. Treat them as reference, not ground truth —
  `project-facts.md` and this log are authoritative.
- 2026-07-21 — Card-item DOM (`foleon-core .../card-item/viewer/card-item.viewer.tsx`) has 2
  layers under the root: `.CardItemInnerContainer` (holds the content — image/text/button — AND
  `overflow:hidden` + the CSS border + padding) and `.CardItemBackgroundContainer` (absolute,
  behind, holds bg color/image). The card corners/border-radius setting (`card-item.style.to-css.ts`
  `corners` override) is written to BOTH via `appendToCSS` (cssSelector=`.CardItemInnerContainer`)
  and an explicit `set(...BackgroundContainer...)`. Because InnerContainer wraps content + has
  `overflow:hidden`, its radius CLIPS the content → rounding the card also rounds the image/text/button
  inside. Sharp edge when touching card rounded-corner behavior.
- 2026-07-21 — Fix for the above (PROD-3816): moved the card "frame" styling (border-radius, border,
  box-shadow) off `.CardItemInnerContainer` onto `.CardItemBackgroundContainer` so the frame rounds while
  inset content stays square. Radius+shadow via overrides in `card-item.style.to-css.ts`; border cssSelector
  changed in BOTH `card-item.model.ts` (main render) AND the editor's brand-settings preview
  `@common/theme/components/cards/card-item/card-item.component.tsx`. Note: the to-css layer decides WHICH
  DOM selector a stored style value lands on — `box.mutations.ts`/`setBoxValue` only writes the value into
  the model, it can't target a layer. Full-bleed card BACKGROUND images live on the frame layer so they
  still round; only content-layer elements changed.
- 2026-07-21 — GOTCHA behind the above: card child element viewers use `border-radius: inherit`
  (e.g. `entities/background/viewer/background.shared.tsx`, and the editor's `item-action-overlay`
  selection overlay). So ANY `border-radius` on `.CardItemInnerContainer` is inherited by every child
  (image/text/button) which then rounds its OWN 4 corners → that IS the "content becomes round" bug.
  Therefore you canNOT round the card by putting border-radius on the content container. Final fix:
  border-radius on the FRAME layer (`.CardItemBackgroundContainer`) for bg/border/shadow, and
  `clip-path: inset(0 round ...)` on `.CardItemInnerContainer` to clip content flush-to-the-card-corner
  (e.g. a full-bleed top image) to the rounded silhouette. `clip-path` is NOT inherited, so interior
  content (text/button) never rounds. This is the right lever whenever you need "clip to rounded card
  shape" without children inheriting a radius.
- 2026-07-22 — TWO SEPARATE test suites, easy to confuse: `pnpm editor:test` (→ `vitest ... run`)
  runs only UNIT tests (Vitest, `*.test.ts(x)` next to source); the browser INTEGRATION/e2e suite is
  `pnpm --filter @foleon/editor test:playwright` (Playwright, `tests/integration/**`), which CI runs
  separately and which reads *rendered* CSS. A green local vitest run does NOT cover integration — after
  changing which DOM layer a style lands on, always run the matching Playwright spec. Reproduce one file:
  `cd packages/foleon-core-editor && pnpm test:playwright tests/integration/editor-brand-kit/content/card.ts`.
- 2026-07-22 — CI editor integration runs fail-fast (`--max-failures=1`) sharded 8-way: ONE real failure
  cancels the other 7 shards ("The operation was canceled" / "strategy configuration was canceled") — that
  cascade inflates the annotation count. Don't read N annotations as N distinct bugs; find the single real
  failing spec.
- 2026-07-22 — Consequence of the PROD-3816 layer move: brand-kit card integration tests in
  `editor-brand-kit/content/card.ts` assert border/border-weight/rounded-corners/shadow via
  `getCardInnerContainer` — these had to switch to `getCardBackgroundContainer` (border/radius/shadow now
  live on the frame). Padding/spacing stays on the inner container. Rule of thumb: when a to-css change
  relocates a property's DOM selector, grep the Playwright specs' `elementLocator`s for the old layer.
- 2026-07-22 — Viewer screenshot baselines are PER-PLATFORM: each `toHaveScreenshot` has both a
  `*-linux.png` (what CI compares against) and a `*-darwin.png` (local Mac) baseline under
  `<spec>.spec.ts-snapshots/`. A local Mac run only exercises the darwin ones — it does NOT prove CI
  (linux) will pass, and `--update-snapshots` on a Mac only fixes darwin. Regenerate the LINUX baselines
  inside the pinned Playwright container: `bash scripts/playwright-in-docker.sh bash -c "cd
  packages/foleon-core-viewer && pnpm test:playwright --update-snapshots <spec>"` (image is
  mcr playwright v1.50.1-jammy, matching `@playwright/test`; needs `pnpm viewer:build` first so
  `dist/previewer` exists — the container reuses the host's node_modules, installs nothing). `playwright`
  isn't on PATH in the container — go through the `pnpm test:playwright` script (it also sets
  PLAYWRIGHT_ENV=production for the SSL webServer). When a card/layout change shifts height, expect the
  cascade: everything below the first affected element shows as a red diff (vertical shift), not just the
  element itself.
- 2026-07-22 — Playwright CLI QUIRK in this repo's viewer config: a positional spec-path filter is
  unreliable — passing two file paths + `-g` ran only one file; passing one file path (with or without
  `-g`) ran the WHOLE suite (500+ tests). With `--update-snapshots` that silently reblesses every stable
  screenshot. ALWAYS `git status -- '*.png'` after an update run and revert strays (a flaky
  infographic-counter darwin snapshot got rewritten this way and had to be reverted). Scope the update by
  running in a throwaway and checking the resulting diff, not by trusting the path filter.
- 2026-07-24 — BORDER bug class (PROD-3754): `entities/styles/border/border.to-css.ts` emits
  `border-<side>-style: solid` (unconditionally at size 50) + `border-<side>-color` (whenever a color
  exists), but width ONLY when truthy. The border settings panel's color picker writes color to ALL four
  sides at once (`handleUpdateBorderColor` in `@entities/styles/border/settings-panels/border.tsx`) while
  the per-side weight slider writes width only to the dragged side — so a "bottom-only weight" ends up with
  top/right/left carrying a color but NO width key. Result: `solid` + color + no width → browser falls back
  to `border-width: medium` (~3px). The EDITOR hides this because it imports Tailwind (`src/tailwind.css`
  `@import "tailwindcss"`) whose Preflight resets `*{border-width:0;border-style:solid}`; the VIEWER/published
  doc has no such reset → the phantom border paints. Classic "editor ≠ preview" border divergence.
- 2026-07-24 — FIX for the above: force an explicit `border-<side>-width: 0px` for any side with no positive
  width (`if (!(Number(border[side]?.width) > 0)) appendToCSS(..., '0px')`), AFTER the value loop. Note
  width is stored as a bare number string (`'0'`,`'4'`), and `'0'` is TRUTHY — that's why the original
  `if (value)` check let a real `'0'` through but an ABSENT width slip. Do NOT "fix" by skipping the whole
  side when width≤0: the brand-kit tests `editor-brand-kit/content/card.ts` "changes border color" assert
  `toHaveCSS('border-color', ...)` after setting ONLY a color (no width) — dropping the side removes the
  color and fails them. Emitting explicit width:0 keeps color queryable AND kills the medium fallback.
- 2026-07-24 — `border.to-css.ts` is shared by ALL bordered entities (block/button/image/table/card/text),
  editor AND viewer both bundle it from `@foleon/core`'s ESM dist. So after editing core `src`, you MUST
  rebuild: `pnpm --filter @foleon/core build` (tsc → dist/esm+cjs) THEN `pnpm --filter @foleon/editor build`
  (vite bundles core's dist, no source alias) THEN `cp src/env-config.js dist/env-config.js` before the
  Playwright production webServer (`serve:ssl` serves `dist`) will reflect the change.
- 2026-07-27 — IMAGE render paths DIVERGE between apps, which is why logs "go missing" when debugging
  `foleon-core/src/entities/image/viewer/image.container.tsx`. The VIEWER
  (`foleon-core-viewer/.../entities/image/image.container.tsx`) mounts `ImageViewerContainer` → which calls
  `renderImg` → which renders `ImageContainerWrapper` (`.Container`) > `FigureContainerStyles`
  (`.FigureWrapper`) > `ImageViewer`, passing the full entity `css` to the WRAPPER and **no `styles` prop to
  `ImageViewer`**. The EDITOR (`foleon-core-editor/src/@entities/image/image.editor.tsx`) imports `ImageViewer`
  DIRECTLY and composes its own DOM (`ImageContainerWrapper` > `ImageFigureWrapper` > `BoxResizer` >
  `AnimationClipWrapper` > `ImageViewer`) — it never mounts `ImageViewerContainer` and never reaches
  `renderImg`. So `ImageViewer` is the ONLY shared component; a log in `ImageViewerContainer`/`renderImg` fires
  in viewer/preview only, and `renderImg`'s `shouldShowLinkDisplay` branch is print-mode only.
- 2026-07-27 — IMAGE border-vs-animation layering (PROD-3528, "animation exceeds the border in Editor"):
  `image.model.ts` emits cinematic zoom + scroll animations onto `.${CSSIdentifiers.Image}` (the `<img>` itself)
  and the border onto `.FigureWrapper`. The viewer keeps that split → static bordered wrapper, `<img>` scales
  inside it. But the editor's `separateInnerStyles` (image.editor.tsx) deliberately MOVES background / all
  `border*` / `boxShadow` off `.FigureWrapper` and passes them FLAT as `innerStyles` to `ImageViewer`'s `styles`
  prop, landing them on the same `<img>` the zoom transforms — so the border scales with the animation. The
  documented reason for the move is that `ImageFigureWrapper` hosts the `BoxResizer` handles and a radius/overflow
  there clips the resizer. `AnimationClipWrapper` (renders only when `hasScalingAnimation`) already sits between
  the resizer and the img with `overflow: clip` + the corner radii, and already receives `innerStyles` — it is the
  natural non-animated host for the border/background/shadow.
- 2026-07-27 — Card images CANNOT have animations: the `Animation` / `AnimationCinematic` / `AnimationRepeat`
  panels are gated behind `isInContentStudioEditor && !isRenderedInCard`
  (`foleon-core-editor/src/@entities/image/settings-panel/index.tsx`), and `cardImageBaseStyles`
  (`foleon-core/src/entities/image/image.styles.ts`) carries no animation keys. Also note animation exists only
  in Content Studio, never Content Builder (see [[content-builder-no-animations]]). Corollary for
  `image.editor.tsx`: its second render branch is NOT "the card branch" — the condition is
  `!isNotDisplayed(computed) && !isImgRenderedInCard`, so it also catches ordinary canvas images with
  `visibility: hidden|none` at the active screensize (`visibility.queries.ts` `isNotDisplayed`), which the editor
  still renders behind a `VisibilityOverlay` and which CAN carry a zoom animation. Don't reason about that branch
  as card-only.
- 2026-07-27 — Writing an editor settings-panel Playwright test: four non-obvious gotchas, all cost a run each.
  (1) The settings panel is a DRILL-DOWN (`settings-panel.content-renderer.tsx` `activeIndex`), not an accordion —
  after `openSetting('Border')` the category list is REPLACED, so touching a second setting needs a back click
  (`.settings-panel-category-container-back-icon`); added `SettingsPanel.closeSetting()` for this.
  (2) `AnimationCinematic` is behind the `editor.cinematicAnimations` flag and `return null`s without it — add the
  toggle to `tests/integration/shared/utils/routes/feature-flag-route.ts` or the dropdown simply isn't in the DOM.
  (3) Cinematic keyframe names are PREFIXED: `animation-cinematic.to-css.ts` emits `cinematic-${name}`, so assert
  `animation-name: cinematic-zoomIn`, not `zoomIn`.
  (4) Every `Select.Trigger` shares the fallback testid `dropdownTrigger2`
  (`@foleon/deprecated-ui-kit_dropdown_dropdown-trigger`) — `.first()` inside the Animation category hits the
  ENTRANCE animation dropdown, not Cinematic. Scope it instead:
  `getByTestId(settingsPanelCategoryScreen).filter({ hasText: '<panel label>' }).getByTestId(dropdownTrigger2)`.
  Cycle is `pnpm build:integration` (only needed after a `src` change) then
  `pnpm test:playwright --project="Doc Editor" -g "<title fragment>"`.
- 2026-07-27 — `tests/integration/editor-doc/@entities/image/image.editor-link.test.ts` is FLAKY locally: the
  failing set changes every run (2-3 of 8), always `hover` timeouts in `SettingsPanel.openForEntity`. It's parallel
  execution — local config is `workers: undefined` (all cores) while CI is `workers: 1, retries: 2`. Don't chase
  these as regressions; reproduce with `--workers=1` before believing a failure there is real.
- 2026-07-24 — Editor Playwright discovery: files under `tests/integration/editor-brand-kit/**` are plain
  `*.ts` (NOT `*.spec.ts`) and are found only via their PROJECT (`--project="Brand Kit Editor"`, testDir set
  per project in `playwright.config.ts`). Positional path filters ("content/card.ts") reliably return
  "No tests found" (the known CLI quirk); `-g "Card"` (matches the joined title, `›` are display-only, not
  in the title string) works. `-g "Content tab › Card"` does NOT match — never put `›` in a `-g` pattern.
- 2026-07-28 — PRE-EXISTING RED on `main` (local darwin): `editor-doc/@entities/infographic/infographic-counter/
  infographic-counter.brand-kit-drawer.test.ts` › `SettingsPanel › Animation`. Times out in
  `SettingsPanel.openForEntity('infographic-counter-number', 1)` → `scrollOptionButtonInToView`, waiting for the
  `.nth(1)` active indicator's settings button, i.e. the second counter never becomes interactable after
  `dragElementFromSidebarToColumn`. Verified pre-existing by reverting `src/@entities/image/image.editor.tsx` to
  `main`, rebuilding, and re-running: identical failure. The other 2 tests in the file pass. Full editor
  integration suite otherwise: 644 passed / 1 failed / 1 skipped in 23.7m at `--workers=1`.
- 2026-07-28 — HOW TO TELL a load-flake from a real failure in this suite (they look alike in a CI annotation).
  Load-flake (e.g. `image.editor-link.test.ts`): the failing SET changes run to run, and it passes when run alone
  or at `--workers=1`. Real failure: same test, same line, same locator every time, and it survives CI-style
  `--retries=2`. Decisive tell — Playwright prints `1 flaky` when a retry passes and `1 failed` when none do, so
  run the suspect with `--workers=1 --retries=2` and read that word before blaming the pipeline. Re-running the
  job will NOT clear a `1 failed`.
- 2026-07-28 — Reverting one file to compare against `main` costs TWO `pnpm build:integration` runs (~27s each)
  because the Playwright production webServer serves `dist`, not `src`. Sequence that works:
  `git checkout main -- <file>` (this STAGES it) → `pnpm build:integration` → `cp src/env-config.js
  dist/env-config.js` → run spec → `git restore --staged --worktree <file>` → rebuild → re-copy env-config.
  Forgetting the env-config copy after either build leaves the editor unable to boot.
- 2026-07-31 — CSS ANIMATION RETRIGGER (PROD-3521, "animation not retriggered after replacing a bg image"):
  cinematic/entrance animations are pure CSS — nothing "triggers" them. `background.styles.ts` →
  `animation-cinematic.to-css.ts` emits `animation-name: cinematic-<name>` (20s, 1 iteration, `fill: both`,
  `play-state: paused` + `running` under `.foleon-animation .block-in-viewport &&`) onto the SAME element that
  carries `background-image`: `.viewer-background` (`foleon-core/.../background/viewer/background.shared.tsx`).
  Replacing the asset only mutates `image.assetRef` in place (`background.mutations.ts updateBackgroundImage`),
  so styled-components emits a new class but an IDENTICAL `animation-name` → per spec the browser does not
  restart → new image appears at the animation's end state. Fix: `key` on the asset identity in the editor's
  `background.editor.tsx` (`assetRef || url` for image, `assetRef` for video) → remount → fresh node → runs from 0.
  Covers block AND column backgrounds and both media types in one place, and needs no `@foleon/core` rebuild.
  Precedent for the same class of bug: `animation-cinematic.tsx handleAnimationUpdate` sets the name to 'none'
  then reapplies inside a rAF — that trick writes mutations (dirties the doc), the `key` approach doesn't.
- 2026-07-31 — MEDIA LIBRARY in Playwright: the current ML (`@foleon/assets-library` 1.6.29) lists assets from
  `GET /k/resources/media?...` (KrakenD shape: `{data:[{id,type:'image',name,access_type,view:{created_on,
  parent_topiary_id,filetype,filesize,properties,links:{self,storage_path,storage_path_thumbnail}}}],meta:{total,
  per_page,last_page}}`, mapped by `mapKrakenDToLegacy`), NOT the legacy `/topiary` — so `imageTopiaryRoute` opens
  the modal but leaves the gallery EMPTY. Added `mediaResourcesRoute` (`shared/utils/routes/media-resources-route.ts`)
  for it. In the DOM, gallery items are `[data-file-id="<id>"]` and the confirm button is labelled **"Choose"**;
  the `mediaLibrary*` testids in `data-testids.ts` (`media-library.gallery.media-item...`) are STALE — they match
  nothing (`link-modal.ts` still uses them). `view.links.self` becomes the entity `assetRef`
  (`getMediaItemPropsToChange` reads `_links.self.href`), so give the stub a different image id than the doc's
  current background or a "replace" is a no-op.
- 2026-07-31 — The block's `BackgroundAnimation` settings panel (cinematic + scroll) needs TWO flags to render:
  `editor.scrollAnimations` (else `background-animation.tsx` returns null) AND `editor.cinematicAnimations` (else
  `animation-cinematic.tsx` returns null). Neither is in the shared `featureFlagRoute`; added
  `featureFlagRouteWithAnimations` (base toggles + both) rather than enabling them for every editor-doc test.
- 2026-08-03 — BLOCK SCROLL-EFFECT BACKGROUND STEALS HIT-TESTING FROM STATIC BLOCK CONTENT (PROD-3270,
  "Gallery gear icon / settings unreachable"). Turning a scroll effect on a block background adds a 3-node
  layer — `.parallax-consumer` (`position: fixed`, `transform: translateY(...)`, `overflow: hidden`) nested in
  an `absolute` wrapper inside an `absolute` + `overflow: clip` wrapper. Verified via
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
- 2026-08-03 — TECHNIQUE for any "editor chrome disappears / isn't clickable" bug here: `document.elementsFromPoint(x, y)`
  fired from a keydown handler (you can't hover and type at once), dumping per row `contains(prev)`, whether the
  row is inside the suspect container, and computed `position`/`transform`/`overflow`/`z-index`/`pointer-events`.
  Its order is PAINT order, so it interleaves unrelated subtrees — always test containment separately or you will
  misread it as an ancestor chain. Diff the stack with the feature on vs off, and on a working element vs a broken
  one; the delta is the culprit. Keep the probe in DevTools → Sources → Snippets so it survives the constant reloads.
  Anchor greps on the semantic `ripley__*` classes (they come from identifier constants); `sc-*` hashes are
  build-generated and ungreppable — for those, React DevTools names the component.
- 2026-07-31 — Useful fixture: the `load-hotspot` recording (`url: doc/119281/pages/812305`) has a block with an
  image background whose `assetRef` is `https://api.staging.foleon.cloud/image/1493060` — the go-to recording for
  block-background tests (hotspots need a bg image, hence it exists).
