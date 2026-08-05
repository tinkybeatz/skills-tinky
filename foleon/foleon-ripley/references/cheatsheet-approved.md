# ripley — Foleon cheat sheet (GENERATED, mirrored from Notion)

> **Do not hand-edit.** This is a plain copy of the `Foleon - Cheat Sheet` Notion page, refreshed by
> `foleon-cheatsheet` whenever the page changes. Edit the page, not this file — this file is
> overwritten on the next pull.

Everything below already went through conversational approval before it was written to the page
(CHS-9) — there is no separate "approved" filter to apply here, because there is no per-item anything
on the page. This is the maintainer's own cheat sheet, copied verbatim.

Last pulled: 2026-08-05

---

# Ripley

pnpm monorepo — the Foleon Docs **editor** (creation) and **viewer** (preview & published docs), both
rendering from a shared `@foleon/core`.

Node `>=22 <23` · pnpm `11.1.1` (enforced) · TypeScript + React · Biome · Vitest · Playwright

## Commands

```bash
pnpm bootstrap                              # install + set up workspace
pnpm build                                   # build everything
pnpm ci:compile                              # TypeScript check
pnpm editor:dev / pnpm viewer:dev            # run an app
pnpm editor:test / pnpm viewer:test          # unit tests (Vitest)
pnpm --filter @foleon/editor test:playwright # integration / e2e
pnpm build:integration                       # required before Playwright, serves dist
cp src/env-config.js dist/env-config.js      # after every build, or the editor won't boot
sh scripts/prepare-auth.sh                   # fixes 403 Forbidden
cd packages/foleon-core && pnpm build && cd ../.. && pnpm editor:dev # build core and re-start dev server
```

Changed `@foleon/core`? Rebuild the chain: core → editor → copy env-config. The apps bundle core's
`dist`, not its source.

## Packages — `packages/`, scope `@foleon/*`

| Folder | Package | Role |
|---|---|---|
| `foleon-core-editor` | `@foleon/editor` | editor app |
| `foleon-core-viewer` · `-viewer-dynamic` | `@foleon/viewer` | preview & published docs |
| `foleon-core` | `@foleon/core` | shared entities, styles, rendering |

Plus `navigator`, `search`, `sdk`, `ui-design-system`, `cookie-consent`, `config`. Internal deps use
`workspace:*`.

## Conventions

- Arrow functions only — no `function` declarations.
- No hardcoded strings / numbers / booleans → constants. `const`-assertion unions, not `enum`s.
- Biome: single quotes, width 120.
- Limits: complexity < 10 · file ≤ 300 · component ≤ 200 · function ≤ 50.
- Tests in `__tests__/` next to the code, `*.test.tsx`, `describe > it > expect`, ≥ 80% coverage.
- Global types/constants/hooks/contexts → dedicated folders in `src/`; local ones stay in their
  feature folder.

## Gotchas

- **A `*.to-css.ts` file decides which DOM element a style lands on** — mutations only write the
  value. Wrong element = look there.
- **Editor ≠ viewer**: the editor imports Tailwind (Preflight resets borders), the viewer doesn't.
  Borders can be right in the editor, wrong when published.
- **Cards**: `.CardItemBackgroundContainer` = frame (bg, border, radius, shadow),
  `.CardItemInnerContainer` = content + padding. Children use `border-radius: inherit` → clip with
  `clip-path: inset(0 round …)` instead.
- **Images**: viewer mounts `ImageViewerContainer` → `renderImg`; the editor imports `ImageViewer`
  directly. Only `ImageViewer` is shared — logs in the container never fire in the editor.
- **Animations are pure CSS** — swapping an asset keeps the same `animation-name`, so it won't
  replay. Remount with a `key`.
- Animations exist only in Content Studio, never Content Builder. Card images can't have them.
- Scope is `@foleon/*`, not `@ripley/*` — the `.cursor/rules` file saying otherwise is stale.

## Playwright gotchas

- Path filters are unreliable — a path can silently run the whole suite. With `--update-snapshots`
  that reblesses everything: always `git status -- '*.png'` after.
- Brand-kit specs are plain `*.ts`, found only via `--project="Brand Kit Editor"`. Select with
  `-g "Card"` — never put `›` in the pattern.
- Screenshot baselines are per platform: `*-darwin.png` = your Mac, `*-linux.png` = CI. Use
  `scripts/playwright-in-docker.sh` for linux ones.
- Flaky vs real: local runs use all cores, CI uses `workers: 1, retries: 2`. Re-run with
  `--workers=1 --retries=2` — `1 flaky` = a retry passed, `1 failed` = real.
- CI is sharded 8× fail-fast: one failure cancels the rest. Many annotations usually = one bug.
- Panels return `null` without their flag: `editor.cinematicAnimations`, `editor.scrollAnimations`.
- The settings panel is a drill-down, not an accordion — go back before opening another setting.
- Media library reads `GET /k/resources/media` (KrakenD), not `/topiary`. Items are `[data-file-id]`,
  confirm button is "Choose", `mediaLibrary*` testids are stale.
