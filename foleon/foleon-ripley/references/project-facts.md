# ripley — project facts

Curated, stable knowledge about Foleon's `ripley` monorepo. Load this before doing
engineering work on Foleon. When something here goes stale, trust the live repo
(`package.json`, `pnpm-workspace.yaml`, `biome.json`) and fix this file.

## What
- **Foleon Docs** applications: creation (**editor**), preview & publishing (**viewer**).
- pnpm **monorepo**. Stack: TypeScript · React · Biome · Vitest + React Testing Library + MSW; Cypress & Playwright for e2e.
- Node `>=22 <23`, pnpm `11.1.1` — pnpm is enforced (`only-allow pnpm`); commit the lockfile.

## Layout — `packages/`, scope `@foleon/*`
- `foleon-core-editor` (`@foleon/editor`) — editor app
- `foleon-core-viewer` (`@foleon/viewer`) · `foleon-core-viewer-dynamic` — preview / publish
- `foleon-core` (`@foleon/core`) — shared core · plus `navigator` · `search` · `sdk` · `ui-design-system` · `cookie-consent` · `config`
- Internal deps use the workspace protocol (`workspace:*`); every package declares its deps explicitly.

## Commands
- Bootstrap: `pnpm bootstrap` · Build all: `pnpm build` · TS check: `pnpm ci:compile`
- Editor: `pnpm editor:dev` · `pnpm editor:test`
- Viewer: `pnpm viewer:dev` · `pnpm viewer:test`
- Lint/format: Biome (`biome.json`) · dead code: `knip` · release: changesets · git hooks: husky + lint-staged

## Conventions (verifiable)
- Functions: **arrow functions only** (`const fn = () => {}`) — no `function` declarations, no mixing styles.
- **Never add comments to generated code.**
- No hardcoded strings/numbers/booleans — use constants; for resource names use `const`-assertion union types, **not enums**.
- Formatting (Biome): **single quotes**, line width **120**.
- Tests: co-located in `__tests__/`, `*.test.tsx`, pattern `describe > it > expect`, coverage ≥ 80%. Vitest + RTL + MSW; Playwright/Cypress for e2e.
- Structure: global types/constants/enums/hooks/contexts → dedicated folders under `src/`; local ones live inside their component/feature folder.
- Limits: cognitive complexity < 10 · file ≤ 300 lines · component ≤ 200 · function ≤ 50.
- If you make a mistake, don't apologize — correct it and continue.
