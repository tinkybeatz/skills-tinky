# Migration mode (one-off)

Two jobs, run once, in this order. Both are on the `skills-tinky` side only —
nothing is written into the ripley checkout (PCS-7).

## Job 1 — Restructure the log to the PCS-6 schema

`foleon/foleon-ripley/references/knowledge.md` predates the amended PCS-6: its
entries are free prose. Target schema, one entry per finding:

```
- YYYY-MM-DD · <area> · <symptom> — <finding> · refs: <paths|tickets> · sheet: <CS-nn|none>
```

`<area>` uses the same six values as the sheet (CHS-8), so the log can be grouped
and deduplicated without re-reading every line.

**Rules while migrating**

- **Preserve every fact.** This is a reformat, not a prune. The log is
  authoritative and stays complete — density is *correct* here.
- **Split interleaved entries.** Several existing entries carry two or three
  findings in one bullet. One finding per entry.
- **Keep the dates.** Use the original discovery date, not today's.
- **`<finding>` stays dense.** Do not apply the sheet's caps or voice rules to the
  log — its audience is an agent that reads everything. Applying CHS-6/CHS-7 here
  would destroy information (CHS-1).
- **`sheet:` is filled by job 2.** Write `sheet: none` for now.
- **Promote stable facts.** If an entry is really a stable project fact (toolchain
  versions, package scope, layout), move it into `references/project-facts.md`
  and drop it from the log — that is PCS-6's promote/prune rule, and it is the
  right home for facts that are not symptom→fix.

⚠️ **The log currently has uncommitted changes.** Check `git status` first. If it
is dirty, say so and let the maintainer commit or stash before you rewrite the
file — otherwise their pending work and this reformat land in one unreviewable
diff.

## Job 2 — Backfill the sheet

Run each migrated entry through the normal pipeline: four gates
(`references/admission.md`) → rewrite (`references/rewriting.md`) →
`row.py check` → dedupe query → create as `Needs review` → write `CS-nn` back
into the entry's `sheet:` field.

Expect a **low** admit rate. At the time this skill was written, 6 rows already
existed (`CS-1`…`CS-6`, hand-seeded from the maintainer's original hand-written
cheat sheet), and most remaining log entries are ticket history or stable facts —
both correctly rejected. If the backfill wants to add more than a handful, the
gates are being applied too loosely.

## Job 3 — Normalise the seeded dedupe keys

`CS-1`…`CS-6` were seeded by hand before `row.py` existed, so their `Dedupe key`
values don't match the canonical derivation. Left alone, the next sync will
create duplicates of all six.

Fix once: for each row, derive the canonical key and update it.

```bash
python3 scripts/row.py key --area "Build & tooling"   --symptom "Editor won't boot after a build"
python3 scripts/row.py key --area "Build & tooling"   --symptom "403 Forbidden from local requests"
python3 scripts/row.py key --area "Core / rendering"  --symptom "Card content rounds along with the card"
python3 scripts/row.py key --area "Tests & Playwright" --symptom "Playwright reblessed every snapshot"
python3 scripts/row.py key --area "Tests & Playwright" --symptom "Snapshot passes locally, fails in CI"
python3 scripts/row.py key --area "Core / rendering"  --symptom "Animation won't replay after swapping the asset"
```

| Row | Seeded key | Canonical key |
|---|---|---|
| CS-1 | `build-tooling:editor-wont-boot-after-build` | `build-tooling:editor-wont-boot-after-a-build` |
| CS-2 | `build-tooling:403-forbidden-local-requests` | `build-tooling:403-forbidden-from-local-requests` |
| CS-3 | `core-rendering:card-content-rounds-with-card` | `core-rendering:card-content-rounds-along-with-the-card` |
| CS-4 | `tests-playwright:update-snapshots-reblessed-everything` | `tests-playwright:playwright-reblessed-every-snapshot` |
| CS-5 | `tests-playwright:snapshot-passes-locally-fails-ci` | `tests-playwright:snapshot-passes-locally-fails-in-ci` |
| CS-6 | `core-rendering:animation-wont-replay-after-asset-swap` | `core-rendering:animation-wont-replay-after-swapping-the-asset` |

Then verify: query the data source grouped by `Dedupe key` and confirm no two
rows share one.

**Why the drift happened, so it doesn't recur:** the keys were written by a model
choosing "reasonable" slugs. The derivation is only stable if a *script* produces
it. After this normalisation, never hand-write a key — always `row.py key`.
