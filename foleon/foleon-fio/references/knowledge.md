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
