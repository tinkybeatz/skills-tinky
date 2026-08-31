<!-- GENERATED FILE — DO NOT HAND-EDIT.

     Written by `foleon-cheatsheet` as a verbatim copy of the `Fio` project page's
     category pages in Notion (PCS-11 read-back). Hand edits are overwritten on the next
     sync and, worse, would put content here that the maintainer never approved.

     Scope: `Fio`'s own category pages only — never `Ripley`'s, and never the hub's other
     projects (PCS-11). A file mixing two projects would put ripley facts in front of every
     fio task, which is the context bleed the per-project split exists to prevent.

     This is a read-only input: consult it for what the maintainer has already written or
     approved. It does not replace `project-facts.md` or `knowledge.md`.

     Source: https://app.notion.com/p/3bae7f9407e7812b85e2fb1484e3dbee  (project page `Fio`)
     Last refreshed: 2026-08-13
-->

# Fio — cheat sheet (mirror)

pnpm + turbo monorepo — the **foleon.ai** editor (`apps/editor`) and API (`apps/api`), replacing
ripley.
Node `>=24 <25` · TypeScript + React · oxlint + oxfmt · Vitest · Playwright

## Fio - Commands

### 403 Forbidden on @foleon/* — not pnpm gcp-auth

```bash
gcloud auth login    # only if gcloud itself can no longer mint a token
npx --yes google-artifactregistry-auth --repo-config=./.npmrc
pnpm install
```

The `~/.npmrc` token is a Google access token and expires in ~1h, so an install that worked earlier
fails later. `pnpm gcp-auth` **cannot** refresh it — pnpm runs `install` before any script body, so
it dies on the same 403 it exists to fix.

### gcloud auth list says ACTIVE while the token is dead

```bash
gcloud auth print-access-token   # the real test
```

The listed account and the ability to mint a token expire separately, so `gcloud auth list` showing
your account proves nothing during a 403. Test with `print-access-token`; if it fails, re-run
`gcloud auth login`.

Ignore `✗ Lockfile failed supply-chain policy check` — it prints on every install, including
successful ones, and is unrelated to the 403 it appears next to.

## Fio - Feature Flags

### Every flag in fio is off — nothing fills the record

`apps/editor/src/routes/_authenticated/route.tsx:52` builds the runtime with a hardcoded
`featureFlags: {}`, and the API passes `noFeatureFlags` (`edit-capabilities.service.ts:76`). Every
lookup runs `flags[name] ?? false`, so an unknown flag reads `false` — fail-closed, no error, no
warning. The Collections tab (`mediaLibrary.collections`) is hidden for this reason, not a bug.
Adding a flag changes nothing until a source exists.

How ripley sources its flags, and what fio has to build to match, is written up in **Foleon -
Documentations → Fio → Flags and Events in fio**.
