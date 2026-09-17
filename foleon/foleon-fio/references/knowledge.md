# fio — discoveries log

Dated, append-only log of non-obvious findings about `fio`. **Indexed by symptom** — scan
for what you're observing, not for the subsystem.

Entry schema (PCS-6), one entry per finding:

```
- YYYY-MM-DD · <area> · <symptom> — <finding> · refs: <paths|tickets> · sheet: <yes|no|none>
```

`sheet:` tracks the Notion cheat sheet — `yes` = mirrored, `no` = proposed and declined,
`none` = never evaluated or rejected by the admission gates. Only `foleon-cheatsheet`
mirrors; never write the sheet yourself.

**Before appending, search this file for the finding's key terms.** On a match, extend and
re-date that entry rather than adding a near-duplicate. Entries may be dense and
jargon-heavy — the reader is an agent reading the whole file.

**When this file grows heavy**, promote the stable facts up into `project-facts.md` and
prune the log to what is still non-obvious. Promotion goes *into this skill*, never into
the fio checkout (PCS-7).

---

- 2026-08-14 · Working rules · Ripley research keeps ending up filed as a fio fact, and `CLAUDE.md`
  looks like it authorises that — it does not. `fio/CLAUDE.md:5` (sven + Sean, team-owned, **not** the
  maintainer's own writing — he was surprised it existed) says *"Ripley is the answer to what this product
  is supposed to do"*, but read the whole section: every following paragraph is about **elements** —
  render/handle/interact, containers, viewers. **It is a rule about where to RESEARCH, not about where to
  FILE, and its scope is UI behaviour parity, not architecture.** Stretching it to justify putting ripley
  facts on a fio page is a documented mistake made here on 2026-08-13 (a whole `Fio - Mixpanel Events`
  cheat-sheet page created with 3 of 4 entries describing ripley; deleted 2026-08-14). The rule that
  actually applies: **a page or log is indexed by what the fact is ABOUT, not by who finds it useful.**
  Ripley's 91 events stay a ripley fact however much they are needed during fio work. Two consequences
  worth internalising: (a) for infrastructure questions — analytics, flags, deployment — the maintainer's
  position is that fio and ripley are **two different projects**, and "so different that we changed the
  repo"; do not cite `CLAUDE.md` back at him as if it settles a product question. (b) **Load
  `foleon-ripley` before researching ripley, not after** — its log already held the GTM/Mixpanel finding
  dated 2026-08-05, so a full day of re-derivation (and one wrong "ripley barely tracks anything"
  conclusion) was avoidable. Cross-repo work means loading BOTH skills up front.
  · refs: `fio/CLAUDE.md:5`, `~/.claude/skills/foleon-ripley/references/knowledge.md` · sheet: none

- 2026-08-13 · Feature flags · A flag added in fio never turns on, and the media-library
  **Collections** tab is permanently hidden with no error anywhere — **fio has the entire
  flag-consumer chain but no flag *source*.** `apps/editor/src/routes/_authenticated/route.tsx:52`
  builds `EditorRuntime` with a literal `featureFlags: {}` (no comment marking it a stub), and the
  API's `edit-capabilities.service.ts:76` passes `noFeatureFlags` — so both surfaces evaluate every
  flag through `isFlagEnabled(flags, name) => flags[name] ?? false` and get `false`, by design
  (fail-closed) rather than by bug. The chain that *is* built: `packages/permissions` defines
  `FeatureFlagSource {isEnabled}` + `FlagId` (opaque string, deliberately not a union — flag names
  belong to the feature that defines them) and composes it with permission facts via
  `createCapabilityFacts()`; `platform/feature-flags/feature-flags.ts` is an 11-line pure lookup;
  `editor-permissions.provider.tsx:49` bridges the record into the interface. One real product flag
  exists — `MEDIA_COLLECTIONS_FLAG = "mediaLibrary.collections"`
  (`media-library-access.mapper.ts:41`). fio already speaks Unleash's dialect **outbound only**:
  `toFlagToggles()` re-inflates its boolean record into Unleash `IToggle[]` for
  `@foleon/assets-library`'s FileManager, stubbing `variant` because "fio has no Unleash variants"
  (`media-library-access.mapper.ts:201-213`) — so the shape a source must produce is already implied by
  code fio ships. No `VITE_UNLEASH_*` exists in `apps/editor/src/env.d.ts`. So wiring flags = supplying a
  source, not building a system. **How ripley sources flags is a ripley fact — see `foleon-ripley`'s log
  (2026-08-14, Unleash behind a proxy), not this one.** · refs: `apps/editor/src/routes/_authenticated/route.tsx:52`,
  `packages/permissions/src/capability/{feature-flags,permission-core}.ts`,
  `apps/api/src/modules/doc/edit/services/edit-capabilities.service.ts:74-80` · sheet: yes

- 2026-08-26 · Tooling/Fallow · A commit that ships infrastructure ahead of its consumers fails the pre-commit
  gate, and the two findings look like bugs in the new code when they are a statement about the rest of the repo.
  `fallow dead-code` walks imports out from real entry points (the browser entry plus every test file), so a
  `platform/<thing>/` folder whose `index.ts` nothing imports yet is reported as an **unused file**, and any
  `export type` with no cross-file consumer as an **unused type**. Building the analytics seam (PROD-4351, ticket
  1 of 4) produced exactly those two: `analytics/index.ts` and `AnalyticsPayload`. Three real exits, and the
  choice matters because two of them silently change the design: (a) point the co-located test's imports at the
  folder's `index.ts` instead of the inner modules — this makes the barrel reachable **and** is a genuine
  improvement, since the test then also proves the barrel exports what a caller needs; (b) stop exporting what
  has no consumer, which shrinks the public surface the ticket asked for; (c) baseline it, which `CLAUDE.md`
  gates behind explicit human approval because it silences a live signal. Note (a) and (b) together turn a
  4-line `index.ts` into 2 lines and drop five type re-exports — a spec-visible narrowing, so they are not
  free "just make the gate pass" moves and must not be applied unasked. **Two mechanical traps around the gate
  itself.** First, `pnpm fallow` resolves scope from the **cwd**: run from `apps/editor/src/platform/analytics/`
  it analysed 23 files and flagged `gtm.transport.ts`/`recording.transport.ts` as CRAP risk with maintainability
  83.5; run from the repo root it analysed 7026, scored 92.2, and flagged neither. Always run it from the root,
  and distrust any health number produced elsewhere. Second, the repo's `fallow-baselines/dead-code.json` was
  **all-empty arrays** before this — the "16 suppressed" the report prints are inline
  `// fallow-ignore-next-line` comments, not baseline entries — so `--save-baseline` was safe to run whole
  (current findings were only ours); it also writes an `analysis_identity` block. On a repo with pre-existing
  findings that same command would silently accept all of them. · refs: `.fallowrc.json`,
  `fallow-baselines/dead-code.json`, `package.json:30-34`, `.claude/hooks/fallow-gate.sh`,
  `apps/editor/src/platform/analytics/` · sheet: none

- 2026-08-20 · Analytics · "Which features are people using?" cannot be answered about fio, and the
  presence of `platform/analytics/` makes it look as if it can — **that folder is Datadog only, and
  Datadog answers is-the-app-broken, not is-the-feature-used.** fio has **no product analytics**: no
  Mixpanel, no GTM, no `dataLayer`, and — the part that actually matters — **zero `addAction` calls in
  the whole repo**, so RUM records "clicked an element labelled *Add block*" derived from the DOM, never
  "the Add Block feature was used"; rename a label and the history breaks. Three things nonetheless
  carry real usage data today: (1) RUM's automatic `trackUserInteractions` clicks plus session replay at
  100%, user-identified; (2) a custom **`draft.turn`** APM span, one per Draft chat turn, countable with
  the read-only `pup traces aggregate` recipe in `docs/observability/datadog.md:44` — the single genuine
  usage number fio has; (3) **the Postgres tables, which are an accidental funnel**: `document_drafts`
  (`accountId`, `createdByUserId`, `createdAt`, `revision`) → `agent_messages` → `draft_materialization_runs`
  (`startedAt`, `terminalStatus` completed|failed, `failureCode`). That funnel is queryable with plain SQL
  and is the fastest route to an adoption number before any instrumentation exists. Hard blockers on
  "adoption when rolled out", all documented by the team at `docs/observability/datadog.md:126-131`: **no
  monitors or dashboards exist for fio at all**, the owning Datadog `engineering` team **has no members**,
  and **there is no production deploy** — `.github/workflows/` holds only `deploy-api-staging.yaml` and
  `deploy-editor-staging.yaml`, both `APP_ENV: staging`, so the `production` tag is wired in code and
  unused. `apps/editor/ARCHITECTURE.md:9,168` reserves `platform/analytics/` and `platform/feature-flags/`
  as infrastructure "arriving later". **Ripley's analytics — GTM, the two `trackingEvents` catalogues,
  Foleon Analytics — are ripley facts and live in `foleon-ripley`'s log (2026-08-14), not here.**
  **Update 2026-08-17 — the plumbing is now DECIDED (not yet built), per the editor team's proposal:** typed
  event catalogue in code (`analytics-events.ts`), one generic `track(name, payload)`, `setAnalyticsContext()`
  merged at the route boundary, transport = **GTM dataLayer** (container `GTM-NFJM6Z`, reused from ripley, so
  zero ops), destination NOT specified — Mixpanel is never named, because routing lives in the GTM web console;
  no RUM mirroring, no cookie-consent gate (first-party, logged-in), names `object.verb-past-tense` designed
  fresh rather than ported, payloads flat `string|number|boolean|null`. Two fio-repo facts that constrain the
  build and were previously unlogged: the env gate is **already written next door** — `rum.ts:99` reads
  `import.meta.env.VITE_APP_ENV` against `MONITORED_ENVIRONMENTS = {staging, production}` with a
  `VITE_DATADOG_FORCE_ENABLE` local opt-out, so `track.ts` should reuse it rather than redefine "which
  environments report"; and the editor uses **`VITE_APP_ENV`** (`apps/editor/src/env.d.ts:4`), so the
  `NODE_ENV`-doubles-as-env problem at `docs/observability/datadog.md:131` is **API-side only** and does NOT
  affect editor analytics — don't raise it as a blocker. Open risk to carry forward: `feature.blocked` is a
  rename of ripley's `clickDisabledFeature`/`unlockFeature`, which are upsell-funnel events with a live
  downstream consumer, so "nothing to port" holds for the AI surfaces and grid but not for that funnel.
  **Update 2026-08-20 — the one gap the decided design does NOT close: navigation.** GTM's built-in
  pageview trigger fires **once, on the initial document load**. fio is a TanStack Router SPA
  (`apps/editor/src/app/router.ts`, `createRouter`), so every navigation after the first is invisible to
  GTM unless something explicitly pushes on route change. `setAnalyticsContext()` merged at the route
  boundary does **not** cover this — it attaches *context* to events, it does not *emit* one, so reading
  the proposal as "navigation is handled" is the trap. The Datadog precedent actively hides the problem:
  RUM auto-tracks views, so nothing in `platform/analytics/datadog/` will hint that GTM needs this wired
  by hand. Decide it explicitly as emit-on-route-change in `track.ts` or as an accepted blind spot; do not
  leave it implicit. Second, smaller convention point: `docs/observability/datadog.md` means the team
  documents each observability integration under `docs/observability/`, so a GTM integration plausibly
  owes a sibling `gtm.md` — confirm rather than assume, but budget for it.
  **Update 2026-08-21 — three repo facts that reshape the decided design.** First, the ambient context
  cannot be set in one synchronous call at the route boundary: `Me` carries only `user_id`, `user_name` and
  `role` (`packages/api-client/src/types/domain.ts:281`) and has **no account id**. The account lives on
  `/self` (`User.account.id` / `_embedded.account.id`, same file line 288), which the boundary fetches
  asynchronously and deliberately does not await, because `identify-editor-user.ts` states that identity
  must never sit in front of the editor rendering. So `setAnalyticsContext` is inherently two-phase and any
  event fired in that window carries no account id — a shape to choose deliberately, not to discover in the
  dashboards. Second, **"viewport" in fio is not a browser dimension**: it is the *page* viewport being
  edited (desktop/tablet/...), derived from editor selection state in
  `features/editor/application/settings/use-active-settings-viewport.hook.ts`. Since `platform/` may not
  import a feature (`apps/editor/ARCHITECTURE.md`, "`src/platform/`"), it cannot be part of a
  platform-owned set-once context; either a feature pushes it in or the events that need it pass it per
  call. Third, **`@foleon/assets-library` (a dependency at `^1.6.17`) already ships GTM machinery** —
  `getGTMScript`, `getDataLayerSnippet`, `GTMProvider` and a throwing `useGTMDispatch`
  (`apps/editor/node_modules/@foleon/assets-library/dist/index.mjs:5182`, `:5190`). Its snippet builder is
  reusable for loading the container; its React provider path is the wrong shape for a plain `track()`
  callable outside React. It also raises a question worth answering before adding a second loader: fio
  mounts assets-library components in the media library, so check whether any of them initialise GTM
  themselves.
  · refs: `apps/editor/src/platform/analytics/datadog/rum.ts:99`, `apps/editor/src/env.d.ts:4`,
  `docs/observability/datadog.md`,
  `packages/db/src/{document-drafts,draft-materialization-runs,agent-messages}/schema.ts` · sheet: none

- 2026-08-17 · Working rules · The Notion doc "Flags and Events in fio" no longer exists under that name —
  it was **split into two pages** because the two halves diverged: flags is a wiring job with an unchanged
  spec, analytics acquired a decided design. `Feature Flags in fio` **keeps the original page URL**
  (`3bce7f9407e781298214c2ff31bf8970`); `Product Analytics in fio` is a new sibling under the `Fio` page
  (`3bfe7f9407e781e8b7e2d961de5b5187`). Both live under Foleon - Documentations → Fio and cross-link each
  other. Note the naming choice and reuse it: the analytics page is deliberately **not** called "Mixpanel"
  — the destination is unconfirmed in both repos, so naming a page after it would bake in an assumption.
  · refs: Notion `Fio` page `3bce7f9407e781c78d8dca181b112a35` · sheet: none

- 2026-08-13 · Environment/setup · agent-browser reports the vault as undecryptable / re-prompts
  for credentials every new terminal, even though `agent-browser auth save foleon` succeeded —
  **`README.md:32` is the cause if its line was pasted into a shell rc verbatim.** It reads
  `export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)`, and the README's own
  instruction is "add to `~/.zshrc`", so the substitution re-runs per shell and mints a *new*
  key each time; the vault was sealed with the key from whichever shell saved it. Generate
  once and paste the literal value. Two adjacent setup facts: `npm i -g agent-browser` lands
  the binary in the *active* nvm version's bin (`~/.nvm/versions/node/vNN/bin`), so it vanishes
  on `nvm use` of another version — install it under the version `.nvmrc` pins (24); and npm's
  `allow-scripts` policy can block agent-browser's postinstall, which is harmless because the
  README's explicit `agent-browser install` step is what fetches Chrome
  (`~/.agent-browser/browsers/`). · refs: `README.md:20-33` · sheet: no

- 2026-08-13 · Environment/setup · `pnpm dev` serves the editor fine (`/` → 200) but every
  embedded-API route 500s with a zod `too_small` on `DRAFT_TOKEN_ENCRYPTION_KEY`, and the
  vite log shows `Error when evaluating SSR module ../api/src/entry.ts` — **cause is a
  verbatim `cp .env.example .env`**. `apps/api/src/env.ts:54` declares the key
  `z.string().min(1).optional()`, so *absent* boots but *present-and-empty* fails; the
  example file ships the bare line `DRAFT_TOKEN_ENCRYPTION_KEY=`, which sets it to `""`.
  `.env.example:24-26` calls it "Required only to materialize a Draft Preview", which is
  misleading in the embedded-dev path: `pnpm dev` mounts the api in-process via
  `@hono/vite-dev-server`, so a bad api env takes down the whole API surface, not just the
  Draft Preview feature. Fix: `openssl rand -base64 32` into it (or delete the line). Same
  blank-vs-absent trap exists for `DATADOG_OTLP_API_KEY`/`DATADOG_OTLP_ENDPOINT`, but those
  are *not* in `apps/editor/vite.config.ts`'s `embeddedApiEnvKeys` (lines 18-31), so their
  blanks never reach the api in dev — only the ~11 forwarded keys can break boot this way.
  Related setup facts, all self-healing so don't chase them: dev needs no `DATABASE_URL`
  (`applyEmbeddedApiEnvDevDefaults` defaults it to the compose URL
  `postgresql://foleon:foleon_dev@localhost:54322/foleon_dev`) but compose itself interpolates
  `POSTGRES_*` with no fallback, so `.env` **is** required for `pnpm db:up`; blank
  `GOOGLE_VERTEX_PROJECT` is fine (defaults `foleon-staging`, location `global`); the
  ripley-facing `FOLEON_API_BASE_URL`/`FOLEON_AUTH_TOKEN_URL` default to staging and are
  absent from `.env.example` by design. Health probe is `GET /editor/health` (`apps/api/src/app.ts:132`),
  reachable through the dev server at `http://localhost:5173/editor/health`. · refs:
  `apps/api/src/env.ts:50-54`, `.env.example:24-27`, `apps/editor/vite.config.ts:16-31,132-154`,
  `compose.yaml:8-15` · sheet: no

- 2026-08-12 · Environment · `pnpm dev` or `pnpm install` dies with
  `[ERR_PNPM_FETCH_403] ... Forbidden` on a `@foleon/*` package (`assets-library`, `sdk`, …)
  while `~/.npmrc` looks correctly configured — the `_authToken` for
  `europe-west4-npm.pkg.dev/foleon-staging/*` is a Google OAuth **access** token (`ya29.*`)
  and lasts only ~1 hour, so an install that worked earlier in the session fails later. Two
  layers expire independently: the npm token, and the gcloud session that mints it.
  **`pnpm gcp-auth` cannot fix this — it is a deadlock.** pnpm's `verify-deps-before-run`
  check runs a full `pnpm install` *before* executing any script body, so the script whose
  whole purpose is refreshing the token dies on the very 403 it exists to repair; the
  escape hatch sits behind the locked door. Working recovery: `gcloud auth login` (only if
  gcloud itself can no longer mint a token — `gcloud auth list` showing the account is
  **not** sufficient, the refresh token expires separately), then
  `npx --yes google-artifactregistry-auth --repo-config=./.npmrc`, which bypasses pnpm
  entirely, reads the registry list from the repo `.npmrc` and rewrites the token into
  `~/.npmrc`. Then `pnpm install`. Expect to repeat roughly hourly. **NOT cross-repo, despite
  appearances** (corrected 2026-08-12 while mirroring): the token expiry itself is common to any
  repo consuming the private `@foleon/*` registry, but that half was already on the maintainer's
  `Ripley - Commands` → `Fixes` page as `gcloud auth login && sh scripts/prepare-auth.sh`, and
  ripley's script *works*. The deadlock is specific to `fio` — it comes from fio's remedy living in
  `package.json` as a pnpm script, plus pnpm's `verify-deps-before-run`. So it belongs under `Fio`,
  not a shared page; CHS-9b's test ("still true if fio were deleted?") answers no. Note also that
  `✗ Lockfile failed supply-chain policy check` prints on every install including successful ones,
  and is unrelated noise. **A failed install also prunes what it could not verify** (added 2026-09-08): the
  403'd run reports `Packages: +2 -1` and removes the workspace-linked `@foleon/core` from
  `packages/core-bridge/node_modules` and `apps/editor/node_modules`, after which `pnpm --filter
  @foleonai/api build` dies with 47 `[UNLOADABLE_DEPENDENCY] Could not load
  ../../packages/core-bridge/node_modules/@foleon/core/dist/esm/...` and takes the pre-push hook
  with it. The build failure looks unrelated to the token and is not: a plain `pnpm install` after
  the token is refreshed restores the package and the build passes untouched. · refs: `package.json:56` (the unusable `gcp-auth` script), `.npmrc`,
  `.npmrc.template`, `~/.npmrc` · sheet: yes
- 2026-08-28 · analytics seam / TS types · a name-payload message type that pairs each event with its own
  payload breaks `pnpm typecheck` inside the generic function that builds it — `Argument of type '{ name:
  "a" | "b"; payload: A | B }' is not assignable to parameter of type 'AnalyticsMessage'` — even though
  every call site is correct. `AnalyticsMessage` in `analytics-transport.ts` is a mapped union (one member
  per event), which is the only shape that rejects one event's name carrying another's payload; a single
  `{ name: AnalyticsEventName; payload: AnalyticsEvents[AnalyticsEventName] }` lets the two widen
  independently and admits mismatches. But `createTrack`'s returned function is generic over `TName`, and
  TypeScript cannot prove an object built from an *unresolved* type parameter lands in the one union member
  that `TName` will resolve to (microsoft/TypeScript#30581, correlated unions). Three workarounds fail
  identically: a distributive conditional type instead of the mapped type, making `send` itself generic,
  and both together. The only fix is `as AnalyticsMessage` on the `transport.send` line. **Currently
  invisible and will surface without warning:** with one event in the catalogue the union has a single
  member, so the object is genuinely assignable and oxlint's `no-unnecessary-type-assertion` *rejects* the
  cast — the pre-emptive fix cannot be committed. Adding the second event flips both at once: typecheck
  starts failing and the cast becomes lintable. A comment on the `transport.send` line records this.
  Cast-free alternative if it ever grates: have `track` take one message argument,
  `track({ name, payload })`, so the caller's literal is checked against the union directly with no
  generic in the way — costs the two-argument call shape. · refs:
  `apps/editor/src/platform/analytics/analytics-transport.ts`,
  `apps/editor/src/platform/analytics/track.ts`, PROD-4351 · sheet: no
- 2026-08-31 · Fallow · clearing a dead-code baseline entry surfaces the *next* masked finding rather than
  going green, so budget more than one pass. Removing the three analytics entries (PROD-4357) exposed ten
  unused re-exports in `platform/analytics/index.ts`; narrowing the barrel to the two symbols the app
  actually imports exposed `AnalyticsPayload`; un-exporting that exposed `AnalyticsValue`. Each was a real
  simplification, not linter-chasing — file-internal types that had been exported on speculation. Also
  worth knowing: **`pnpm fallow:dupes` and `pnpm fallow:health` fail on pre-existing repo-wide state**
  (re-measured 2026-09-02: **832 duplicated lines, 0.5%, across 50 files**, plus health 78/B with `hotspots -10.0 · unit size -10.0`
  and the one refactoring target `packages/agent/src/activity.ts`; the 394 figure was 2026-08-31 and the repo has grown since,
  so do not read a rise as your own change) and are NOT what the commit gate runs. The gate
  (`.claude/hooks/fallow-gate.sh`) runs `fallow audit`, which is **diff-scoped** — "11 changed files vs
  <merge-base>" — so a repo-wide red says nothing about whether your change passes. Check with
  `npx --no-install fallow audit`. · refs: `.claude/hooks/fallow-gate.sh`, `fallow-baselines/dead-code.json`,
  `apps/editor/src/platform/analytics/index.ts` · sheet: none
- 2026-08-31 · Environment · the `pnpm install` that recovers from the expired-`ya29` 403 (see 2026-08-12)
  also leaves the Playwright browser binary missing, so `--project browser` dies with
  `browserType.launch: Executable doesn't exist at .../chromium_headless_shell-1234/...` — a fallout of the
  recovery, not of the change under test. Fix: `pnpm --filter @foleonai/editor exec playwright install
  chromium`. **`pnpm exec playwright install` from the repo root fails** with `Command "playwright" not
  found`: playwright is a dependency of `apps/editor`, not the root, so the filter is required.
  · refs: `apps/editor/package.json` · sheet: yes
- 2026-08-31 · Analytics / env gating · **`VITE_APP_ENV` is undefined on a developer's machine** — it is set
  only by `.github/workflows/deploy-editor-staging.yaml:42` (and declared in `turbo.json`'s build env), never
  by a local `.env` file. So the `monitoringEnabled()` shape in `platform/analytics/datadog/rum.ts:54-61` —
  `if (!environment) return false;` *before* reading the FORCE_ENABLE opt-in — makes that opt-in unreachable
  locally, which is the one place it exists for. Copying that shape for GTM (PROD-4357) reproduced the bug:
  `.env.local` set, dev server restarted, and the transport still took the tracking-off branch. Read the
  opt-in FIRST, then fall through to the environment test. **`VITE_DATADOG_FORCE_ENABLE` is very likely dead
  the same way** — `rum.ts`'s own comment claims it "lets a developer verify instrumentation against the real
  Datadog UI", and `docs/observability/datadog.md:25` documents the environment requirement without mentioning
  the interaction; not fixed here, out of that ticket's scope. Second trap in the same area: **vitest loads
  `apps/editor/.env.local`, and `vi.unstubAllEnvs()` restores it**, so an "off by default" test passes on CI
  and fails on the machine of whoever actually set the opt-in. Pin both inputs with an explicit
  `vi.stubEnv("VITE_..._FORCE_ENABLE", undefined)` in `beforeEach`; `rum.test.ts` has the same exposure. Third
  trap, same area (added 2026-09-08): **the editor reads `apps/editor/.env.local`, and the
  repo-root `.env.local` is invisible to it.** The root file is real and in use — Postgres, Vertex,
  Datadog OTLP, the draft-token key — so `VITE_*` vars land there naturally and then do nothing,
  with no warning and no request to miss in the network tab. Vite resolves `envDir` from the app
  root, not the workspace root.
  · refs: `apps/editor/src/platform/analytics/gtm-container.ts`, `.../datadog/rum.ts:54`,
  `.github/workflows/deploy-editor-staging.yaml:42` · sheet: none
- 2026-08-31 · Analytics / GTM · **sharing ripley's GTM container brings its container-side triggers along,
  but far less of it reaches fio than the dataLayer suggests.** Loading `GTM-NFJM6Z` in fio (PROD-4357) turns
  on GTM's own listeners, so one Present click produced `gtm.click`, `gtm.linkClick`, `gtm.historyChange` and
  four `gtm.scrollDepth` entries alongside our two pushes. **A listener emitting into the dataLayer is not a
  tag firing** — that was the first read of this and it was wrong. Checking the Triggers list: all three
  Scroll Depth triggers are pinned to `Page Hostname equals www.foleon.com` on `/topics/`, `/pricing`,
  `/blog/`; `All link clicks` explicitly *excludes* the editor hostname; every Mixpanel trigger requires
  `mixpanelLoaded equals true`, which fio never sets. Only two look unscoped — `Clicked Theme Trigger`
  (All Elements, Page URL regex on `editor.foleon.co…`) and `Switch Settings Type Button - text click`
  (All Elements, filtered on a CSS class alone). **Settled 2026-08-31 — Chiel: "those are natively tracked by
  GTM, don't worry about it."** So sharing the container costs nothing on the fio side and needs no follow-up;
  the chatter is GTM's own listeners and the container owner is content with it. **Method note:
  read the trigger's filters, never the dataLayer chatter** — the chatter is what GTM listens to, the filters
  are what it records. Also: the container has two workspaces, and only `Dev` previews cleanly — `Default`
  holds ~24 pending changes including a Mixpanel tag with a JavaScript parse error, which blocks Preview.
  `Dev` carries no Click/Scroll triggers, so preview from there shows none of the chatter. · refs:
  `apps/editor/src/platform/analytics/gtm-container.ts` · sheet: none
- 2026-08-31 · Analytics / GTM · **loading the shared GTM container means third-party tools can arrive in the
  fio editor that nothing in the repo imports.** Per Chiel (container owner), tags in `GTM-NFJM6Z` can inject
  whole vendor scripts — the Mixpanel-family tags are already there — and those tools then fire their own
  events independently of anything fio pushes. Not visible yet only because fio has no production deploy and
  the relevant tags are scoped to production hostnames; **expect it the moment fio reaches production.**
  Practical consequence, and the reason this is written down: an unexplained network request, dataLayer entry
  or console error in the editor should be attributed to a GTM-injected tag before it is treated as an editor
  bug — the script has no import anywhere in `apps/editor`, so grepping the repo for it returns nothing and
  reads as a phantom. Chiel's words: *"since you are loading in GTM some tools might be loaded in as well that
  fire their own events … good to know if you see something weird."* · refs:
  `apps/editor/src/platform/analytics/gtm-container.ts` · sheet: none
- 2026-09-02 · Lint / HAL `_embedded` · `pnpm lint` fails with `eslint(no-underscore-dangle): Unexpected dangling '_' in
  '`_embedded`'` on a Foleon HAL read, and the repo's six existing precedents all answer it with an inline
  `// oxlint-disable-next-line eslint/no-underscore-dangle -- Foleon API uses HAL `_embedded` relations.`
  (`apps/api/.../edit-capabilities.service.ts:35,60,62`, `apps/editor/src/platform/authz/api/authz.queries.ts:17,33`,
  `features/template/api/template.queries.ts:117`, `features/template/domain/template.ts:86`). **A suppression is not
  required: the rule fires on the member expression, not on a destructured binding.** `const { account, _embedded } = self;`
  then `account?.id ?? _embedded?.account?.id` lints clean (verified — `pnpm lint` exit 0). Worth knowing because the
  precedents make the disable look like the house style when it is really just the first fix anyone reached for; prefer the
  destructure and leave a one-line comment saying why, or the next reader "simplifies" it back to `self._embedded` and
  re-breaks the gate. The type declaration `_embedded?: {...}` is never flagged, only the read.
  · refs: `apps/editor/src/platform/analytics/analytics-identity.ts`, PROD-4360 · sheet: none
- 2026-09-02 · Browser tests · **`vi.waitFor`'s 1s default is too short for the FIRST `renderRoute()` in a browser test
  file, and the symptom is distinctive: test 1 fails, tests 2 and 3 in the same file pass.** Bringing up
  `@/routeTree.gen` plus resolving the session measured ~3.7s on the first mount and well under 1s afterwards, so a
  `vi.waitFor` barrier looks like a real product bug ("expected undefined to be 42") in exactly one test. Use
  `expect.poll`, which inherits the browser project's `BROWSER_INTERACTION_TIMEOUT_MS` (45s,
  `apps/editor/vite.config.ts`) rather than Vitest's own default. Second finding from the same test (PROD-4360): **a
  whole-route-tree test on a document editing surface needs no document content at all.** `/_authenticated/doc`'s
  `DocLayout` has no loader, so it mounts as soon as `_authenticated`'s `beforeLoad` resolves; answering
  `pages.getPages` with `_embedded.page: []` keeps the canvas renderer — and its measured ~3.5s auto-fit, the source of
  the PROD-4239/4249 flakes — entirely out of a test about route params, and a second document id (`/doc/43/...`) then
  costs nothing because no mock has to distinguish the two. ⚠️ But the surface's route loaders start
  `preloadEditorPermissions` **un-awaited and uncaught**, so `auth.getPrivileges` must still be stubbed
  (`{ data: { _embedded: { grants: [] } } }`) or its rejection surfaces as a Vitest *unhandled error* rather than as a
  failed assertion — `documentOwnershipQueryOptions` is safe by contrast, it wraps its own body in try/catch.
  · refs: `apps/editor/src/platform/analytics/use-document-analytics-context.browser.test.tsx`,
  `apps/editor/src/features/editor/tests/doc-routes.browser.test.tsx`, PROD-4360 · sheet: none

- 2026-09-03 · **A route may not import a feature's internals — only its barrel.** The
  `editor-architecture(boundaries)` oxlint rule rejects any import from `routes/**` that reaches into
  `features/<feature>/**`: *"Routes must import features through features/<feature>/index.ts or
  route.ts, not feature internals."* It fires on the plain `oxlint .` pass, so `pnpm lint` catches it
  before CI. This bites whenever a route has to mount a small feature-owned component — the fix is to
  re-export it from `features/<feature>/index.ts` (or `route.ts` for loader-side helpers) and import
  from `@/features/<feature>`, not to deepen the path. Worked example: mounting
  `AnalyticsDocumentAccountContext` on the `/doc` layout, where the component must live feature-side
  because `platform/` may not import a feature, and the route must reach it through the barrel.
  · refs: `apps/editor/scripts/oxlint-plugin-editor-architecture.js`,
  `apps/editor/src/features/editor/index.ts`, `apps/editor/src/routes/_authenticated/doc/route.tsx`,
  PROD-4360 · sheet: none

- 2026-09-03 · **A new `docs/` subfolder is invisible to git until it is allowlisted in `.gitignore`.**
  The repo ignores `docs/*` wholesale (`.gitignore:64`) and carves out one pair of lines per tracked
  subfolder — `!docs/adr/` plus `!docs/adr/*.md`, and the same for `agents/`, `observability/` and
  `rfc/`; `roadmap/` goes further and allowlists two individual files. So writing a doc into a folder
  that has no carve-out leaves `git status` completely clean: the file exists, nothing reports it
  missing, and it never reaches the PR. Add both lines (the folder and its `*.md`) in the same commit
  as the first file. Worked example: `docs/analytics/gtm.md` (PROD-4361) needed
  `!docs/analytics/` + `!docs/analytics/*.md`. `git check-ignore -v <path>` names the exact rule and
  line when a written file does not show up.
  · refs: `.gitignore:64-83`, `docs/analytics/gtm.md`, PROD-4361 · sheet: none

- 2026-09-04 · **fio's feature-flag seam is fully wired and fed an empty object, so every flag reads
  as off.** `apps/editor/src/routes/_authenticated/route.tsx:53` hardcodes `featureFlags: {}` into
  `EditorRuntime`, and that value is what `editor-permissions.provider.tsx:49` and
  `use-media-library-access.hook.ts:110` evaluate through `isFlagEnabled`
  (`platform/feature-flags/feature-flags.ts`, unknown flag → `false`). `packages/permissions` never
  fetches: it takes a `FeatureFlagSource` (`capability/feature-flags.ts`) and fails closed by
  contract. The API side is the same shape — `edit-capabilities.service.ts:15` supplies
  `noFeatureFlags = { isEnabled: () => false }`. So a feature that looks flag-gated and never
  appears is the expected behaviour of the current code, not a broken flag: nothing populates the
  record yet. Suspect this before suspecting Unleash, and note the inverse trap recorded at
  `settings-panel/controls/media-preview-row.tsx:195-212`, where `featureFlags: {}` was blamed for a
  blank Lottie preview it had nothing to do with.
  · refs: `apps/editor/src/routes/_authenticated/route.tsx:53`,
  `apps/editor/src/platform/feature-flags/feature-flags.ts`,
  `packages/permissions/src/capability/feature-flags.ts`,
  `apps/api/src/modules/doc/edit/services/edit-capabilities.service.ts:13-15` · sheet: none

- 2026-09-04 · **`@foleon/react-flags` cannot be dropped into fio: its Unleash client is built at
  module import time from `window._env_`.** The published package (3.0.2, used by ripley's editor and
  both viewers) constructs `new UnleashClient(...)` at module scope, reading
  `window._env_.UNLEASH_PROXY_ENDPOINT` and `.UNLEASH_PROXY_CLIENT_KEY` with two placeholder string
  fallbacks (`src/client/flags-client.ts:15-21`). `window._env_` is ripley's docker-entrypoint
  convention — `docker-entrypoint.sh:120-121` writes `env-config.js` before the bundle loads. fio
  serves its config through Vite's `import.meta.env`, so importing the package yields a client
  pointed at `https://unleash-proxy-url` that fails silently: no throw, no flags, every value off.
  Making it work would mean assigning `window._env_` before the first import of the package, an
  import-order dependency no type checker enforces. The package is a ~60-line wrapper (client,
  context, `useFlag`, a `FeatureFlag` component) over `unleash-proxy-client`, so depending on that
  library directly is less code than the shim. This is a fio-side choice, not a ui-kit-style change
  to a shared package.
  · refs: `../ripley/packages/foleon-core-editor/node_modules/@foleon/react-flags/src/client/flags-client.ts`,
  `../ripley/docker-entrypoint.sh:120-121`, `../ripley/config/.env.template:11-12` · sheet: none

- 2026-09-04 · **Two Unleash conventions fio must copy exactly or its flags silently miss.** First,
  the environment is derived from the hostname, and any host containing `staging` resolves to
  `development`, not to a staging environment (`EnvironmentResolver`,
  `src/client/flags-client.helpers.ts:8-15`; `acceptance` maps to `acceptance`, everything else to
  `production`). Unleash stores an independent on/off per environment, so a flag switched on in
  `production` reads as off on a staging host and looks exactly like broken wiring. Second, ripley
  identifies the caller to Unleash by **account** id, not user id: `FlagsUserProvider` calls
  `setUserId(authState.author.account.data?.id)`
  (`@lib/feature-flags/flags-user.provider.tsx:14-19`). Every targeting rule in the shared project is
  therefore written against accounts, so fio must send an account id under the same `userId` key or
  no existing rule matches it. Related: ripley's `useFlag` returns `boolean | undefined` and reads
  before `setUserId` unless passed `waitForUser`, which is why a targeted flag can flicker on there.
  · refs: `../ripley/packages/foleon-core-editor/node_modules/@foleon/react-flags/src/client/flags-client.helpers.ts`,
  `../ripley/packages/foleon-core-editor/src/@lib/feature-flags/flags-user.provider.tsx`,
  `../ripley/packages/foleon-core-editor/node_modules/@foleon/react-flags/src/hooks/use-flag.tsx` · sheet: none

- 2026-09-04 · **Flag names are shared across Foleon's surfaces in one Unleash project, and fio
  already reads one.** `MEDIA_COLLECTIONS_FLAG = "mediaLibrary.collections"`
  (`apps/editor/src/features/editor/domain/media-library/media-library-access.mapper.ts:41`) is
  ripley's `FLAGS_LIST.assetManager.enableCollections` verbatim
  (`@shared/flags.ts`, 55 flags namespaced `editor.*`, `dashboard.*`, `format.*`, `mediaLibrary.*`).
  One proxy endpoint and client key serve editor, viewer, viewer-dynamic and dashboard. So fio is
  already a consumer of ripley's project rather than a candidate for its own, and a fio-only prefix
  is not available: the CTO created `editor.grid` in that project on 2026-09-04 for a grid/DnD toggle
  meant to be read by the dashboard, the editor and print mode. Follow the existing `editor.*`
  convention rather than inventing a `fio.*` one.
  · refs: `apps/editor/src/features/editor/domain/media-library/media-library-access.mapper.ts:41`,
  `../ripley/packages/foleon-core-editor/src/@shared/flags.ts`,
  `../ripley/config/.env.template:11-12` · sheet: none

- 2026-09-08 · Feature flags / Unleash · **the frontend proxy returns only the toggles that are ON** —
  `GET <proxy>` answers `{"toggles":[{"name":…,"enabled":true,"variant":{…}}]}` and a flag that is off
  for the asking account is simply absent from the array, not present with `enabled:false`. Verified
  against ripley's shared project (PROD-4658): 32 toggles came back, every one `enabled:true`, and
  `mediaLibrary.collections` — a flag fio genuinely reads — was not among them. So
  `isFlagEnabled`'s unknown-flag-is-`false` default is not a nicety, it is the mechanism by which an
  off flag reads off, and any code that expects to find every known flag in the response is wrong.
  Corollary: `client.getAllToggles()` is a list of what is on, so `Object.fromEntries` over it yields a
  record whose values are all `true` in practice. · refs:
  `apps/editor/src/platform/feature-flags/unleash-flags.ts`, `.../feature-flags.ts` · sheet: none

- 2026-09-08 · Feature flags / dependencies · `unleash-proxy-client@3.8.0` was **already in
  `pnpm-lock.yaml`** before PROD-4658 added it, as a transitive dependency of
  `@foleon/assets-library@1.6.17` (which pulls `@unleash/proxy-client-react@4.5.2` alongside it). So
  adding it as a direct dependency of `@foleonai/editor` resolves nothing new and cannot drift from the
  version the FileManager already runs against — worth pinning to that exact version for the same
  reason. Before the direct dependency lands, the package's types are only readable at
  `node_modules/.pnpm/unleash-proxy-client@3.8.0/node_modules/unleash-proxy-client/build/index.d.ts`;
  the top-level `node_modules/unleash-proxy-client/` path does not exist. · refs: `pnpm-lock.yaml`,
  `apps/editor/package.json` · sheet: none

- 2026-09-08 · Environment / typecheck · **`pnpm --filter @foleonai/editor typecheck` fails on its own
  where the root `pnpm typecheck` passes.** Symptom: `Module '"@foleonai/api-client"' has no exported
  member 'Comment'` / `'CommentStatus'` from `features/shared/domain/comment-wire.ts` and
  `features/shared/api/comments.keys.ts`. The editor consumes workspace packages through their built
  `.d.ts`, and turbo's `typecheck` task depends on `@foleonai/api-client`'s `build:types`; a filtered
  invocation skips that dependency, so tsc reads a stale or absent declaration file. Nothing is wrong
  with the code — run the root `pnpm typecheck` (or `pnpm build:deps` first). Reached after merging
  `main`'s comments feature into a branch on 2026-09-08. · refs: `turbo.json`,
  `packages/api-client/package.json` · sheet: none

- 2026-09-11 · Feature flags / Unleash · **The shared Unleash instance exposes a single environment
  named `default`, so `unleash-config.ts`'s `unleashEnvironment()` mapping selects nothing.** Symptom:
  reasoning about "which environment does staging resolve to" finds no answer in the flag UI — both
  `editor.scheduling` and `mediaLibrary.collections` show one environment row, `default`. The
  `environment` field passed to the client is context for strategy constraints; what actually decides
  the values a read returns is the client key. Treat the staging→`development` mapping as inert until
  someone adds environments, and do not build a behaviour on it. · refs:
  `apps/editor/src/platform/feature-flags/unleash-config.ts` · sheet: yes

- 2026-09-11 · Feature flags / Unleash · **A flag missing from the proxy's snapshot is not a missing
  flag — the proxy returns only the toggles that evaluate enabled for the calling context.**
  `mediaLibrary.collections` exists, is on, and carries three strategies, but is account-targeted, so
  it is absent from a snapshot taken for an untargeted account and correctly reads false.
  `editor.scheduling` (created 2026-01-29, one strategy, enabled for every evaluation) is the one that
  reads true from any account, which makes it the flag to use when verifying the transport or a
  flag-gated surface locally. ⚠️ **Corrected 2026-09-14** — it read true for *ripley*, not for fio; see
  the appName entry below. · refs: `apps/editor/src/platform/feature-flags/feature-flags.ts`
  · sheet: yes

- 2026-09-14 · Feature flags / Unleash · **A flag switched fully on in the Unleash UI can still be
  absent from fio's proxy response, because a strategy constraint matches on `appName` and fio sends
  `fio-editor` while ripley sends `foleon`.** `editor.scheduling` showed "enabled 106 times in the last
  hour" at 100% rollout and returned nothing for us; its Gradual rollout carried two constraints,
  `environment is one of development/acceptance/production` (which fio satisfies) and `appName is one of
  foleon` (which it does not), so the proxy filtered the toggle out. Adding `fio-editor` to that
  constraint list returned it — 32 toggles instead of 31. This is indistinguishable from broken
  transport from inside the app, and the Unleash page shows nothing wrong, so **settle it against the
  proxy, never the UI**: `curl -s -H "Authorization: <client key>"
  "<proxy url>?appName=fio-editor&environment=development&userId=<account id>"`. The context fields the
  constraints match on are set in `unleash-config.ts` (`APP_NAME = "fio-editor"`, `unleashEnvironment()`)
  and `userId` is the document-owning account id from `useOpenEditionAccountId()`; the vendor client
  serialises all three onto the GET. ⇒ any flag shared with ripley must have `fio-editor` added to its
  appName constraint before fio can read it. · refs:
  `apps/editor/src/platform/feature-flags/unleash-config.ts`,
  `apps/editor/src/routes/_authenticated/route.tsx`, PROD-4659, #727 · sheet: yes

- 2026-09-15 · Feature flags · A flag targeted at a customer never matches, because the editor
  sends only the workspace id — **fio now sends two ids to Unleash**: `userId` = the workspace
  account that owns the open edition (unchanged, and the same subject the permission grants
  resolve against), plus `properties.companyId` = that workspace's `parent.id`, read with a
  second `auth.getAccount(accountId)` query (`platform/auth/api/session.queries.ts`
  `accountQueryOptions` / `accountParentId`, hook `useOpenEditionCompanyId` in
  `routes/_authenticated/route.tsx`). Foleon nests `Account > account (workspace) > title
  (project) > edition (doc)`; a customer holds many workspaces, so workspace-only targeting
  means listing every workspace in the strategy — the reason Joost and Saman asked for it
  (2026-09-15; ripley PR #4799 and dashboard-next send the same pair). Two traps: the
  starter must distinguish *unresolved* (`undefined`, wait) from *no parent* (`null`, start
  without the field), because `updateContext` replaces the whole context and a late addition
  costs a second fetch through a `start()` path written to run once; and a **June-of-this-cycle
  revert exists** — the two-hop parent read was tried and reverted on 2026-09-11 (dd3e5f79,
  "target the workspace account"), so the account-id test pins the workspace id deliberately.
  Verified on the wire: the proxy accepts `properties%5BcompanyId%5D=` as a query param and
  answers 200. · refs: `apps/editor/src/platform/feature-flags/feature-flags.provider.tsx`,
  `docs/feature-flags/unleash.md`, PROD-4823 · sheet: no

- 2026-09-16 · Analytics · a new `track()` call fires correctly but nothing appears in the browser
  console — **`VITE_GTM_FORCE_ENABLE=true` in `apps/editor/.env.local` is the cause, and it means the
  events went to the real shared container instead.** The transport's DEV `console.info` echo runs only
  on the tracking-OFF branch (`gtm.transport.ts:50-55`): when the flag is set, `gtmDataLayer()` returns
  the array, the real push happens and nothing is printed. So "no console output" reads as "my listener
  is broken" while actually meaning "it worked and went to GTM-NFJM6Z", the container ripley production
  shares. Left over from the PROD-4357 plumbing work; commented out on 2026-09-16 with a note in the
  file. ⇒ **For every event ticket in PROD-4882: develop with the flag OFF and read the console echo;
  set it only for a deliberate GTM preview check, then unset it.** Events carry real account and
  document ids, so a laptop session counts as customer usage the moment a tag is wired to that event
  name. Second-order trap while it is on: `window.dataLayer`'s last two entries are the `{fio: null}`
  clear and then the event, which is the only way to see anything without unsetting the flag.
  · refs: `apps/editor/.env.local`, `apps/editor/src/platform/analytics/gtm.transport.ts:38-56`,
  `apps/editor/src/platform/analytics/gtm-container.ts:27-35`, PROD-4883 · sheet: yes

- 2026-09-17 · Entities · A mutation that styles a "card" writes the `carousel` or `gallery` table,
  not `card` — so anything keyed on the card identity (analytics, a selector, a guard) sees almost
  nothing. Foleon models a card as a `card` entity holding exactly one `carousel` or `gallery` child
  (`CardParentIdentity`), and **every card style mutation but `set_card_theme_variant` resolves that
  child through `requireCardParent` and writes there** (`card/card-parent-draft.ts:96-101`, which says
  so outright). `set_card_theme_variant` is the single exception, because `themeVariant` lives on the
  card itself. Card ITEM styling is a third table again, `card-item`. Ripley has the identical layout
  and the identical trap: its card panel passes `identity: carouselEntity.identity` to the grid
  mutations (`@entities/card/settings-panels/general-settings.tsx:206-209`) and its other card writers
  reach `state[carouselRef.identity]` (`card.mutations.ts:81-91`). ⇒ Before keying anything on "card",
  check which of the four tables — `card`, `card-item`, `carousel`, `gallery` — the write actually
  lands in. · refs: `packages/document-mutations/src/card/card-parent-draft.ts`, PROD-4883 · sheet: yes

- 2026-09-17 · Editor · **fio cannot add or delete an element yet, and no template contains a chart.**
  The whole mutation catalogue has no element-insert mutation: insertion is `insert_template_content_on_page`
  (a whole block from the templates panel) and `add_column`, nothing more. Deletion is the same —
  `remove_block`, `remove_column`, `remove_card_item` exist, there is no `remove_element`, and the
  Delete key refuses anything but a block ("Only a block can be deleted. Select one first.",
  `zoomable-page-frame.tsx:883-897`; PROD-4576 is the parked ticket to widen it). Separately, **0 of the
  180 bundled templates carry a `chart-link`** — the string "chart" does not appear in
  `packages/template-db/src/templates` at all, and `chart-link` is absent from the 37 entity identities
  they use. ⇒ Any manual check that needs a chart, or an element that is not in a template, has no route
  through the UI: use an existing staging document that already contains one, or a unit test driving the
  store directly. · refs: `packages/document-mutations/src/`, `packages/template-db/src/templates/`,
  `apps/editor/src/features/editor/ui/components/zoomable-page-frame.tsx`, PROD-4883, PROD-4576 · sheet: yes
