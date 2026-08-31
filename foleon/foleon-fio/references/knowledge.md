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
  and is unrelated noise. · refs: `package.json:56` (the unusable `gcp-auth` script), `.npmrc`,
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
  (394 duplicated lines, `packages/agent/src/activity.ts`) and are NOT what the commit gate runs. The gate
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
  `vi.stubEnv("VITE_..._FORCE_ENABLE", undefined)` in `beforeEach`; `rum.test.ts` has the same exposure.
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
