# fio — project facts

**This file is an index + delta, not a description of fio.** Per PCS-9a, fio's own
committed docs are read directly as a source of truth; restating them here would create a
second copy that goes stale while the original moves on. So: below is *where to look*,
plus only what those docs **don't** cover.

Repo: `~/Documents/GAEL/FOLEON-DEV/fio` · monorepo, `apps/*` + `packages/*` · pnpm + turbo
· Node 24 (enforced at install).

---

## Index — the team's own docs (read these directly)

| Path | What it covers |
|---|---|
| `CLAUDE.md` | The governing rules: **"check ripley first"**, agent-browser, Fallow findings, the comment policy (comment the *why*; TSDoc every export; no `TODO`), ui-kit usage, and "read `ARCHITECTURE.md` before changing an app". |
| `AGENTS.md` | Codex-specific browser guidance — `@Browser` for unauthenticated pages, `agent-browser` for authenticated editor routes. |
| `CONTEXT.md` | Domain language for the **AI page-generation** pipeline: Document Outline Draft, Planned Page, Text Policy (`verbatim-source` … `rewrite-source`), Tone of Voice, plus the *Avoid* synonyms for each. |
| `apps/editor/ARCHITECTURE.md`, `apps/api/ARCHITECTURE.md` | Required reading before changing either app — `CLAUDE.md` mandates it. |
| `README.md` | Start commands and the full agent-browser auth/vault setup. |
| `docs/agents/domain.md` | How to consume domain docs; `CONTEXT-MAP.md` and per-context `CONTEXT.md` files get created lazily — **absence is expected, don't flag it**. |
| `docs/agents/issue-tracker.md` | Issues/PRDs are **local markdown in `.scratch/`**, not GitHub Issues. |
| `docs/agents/triage-labels.md` | Triage vocabulary, recorded as a `Status:` line per issue. |
| `docs/adr/` | Architecture decisions, `0004`–`0019` (numbering has gaps). |
| `docs/rfc/` | RFCs `0001`–`0016`. |
| `docs/design/`, `docs/observability/` | Template-selection rules; Datadog. |
| `.claude/agents/dev.md`, `.claude/agents/test.md` | The repo's own dev/test subagents. |
| `.claude/hooks/fallow-gate.sh`, `.fallowrc.json`, `fallow-baselines/` | The Fallow gate that runs on commit/push. |
| `.claude/skills/react-doctor/`, `.claude/skills/ticket/` | Project-local skills; they take precedence for their own tasks. |
| `package.json` | The script surface — `dev`, `build`, `test*`, `lint`/`format` (oxlint + oxfmt), `fallow*`, `db:*`, `eval*`, `typecheck`, `doctor`. |

## Packages (routing aid)

`api-client` · `chat-contracts` · `compiler` · `core-bridge` · `db` ·
`document-mutations` · `pdf-extraction` · `permissions` · `sdk-codegen` · `template-db`

Apps: `editor` · `api` · `editor-e2e`.

---

## Delta — what the team's docs don't cover

- **The README's `pnpm install` is not sufficient on a cold machine.** `@foleon/*` and
  `@libs/*` resolve to a **private Google Artifact Registry**, authenticated by a
  `ya29.*` OAuth token in `~/.npmrc` that expires in about an hour. Nothing in `README.md`
  or `CLAUDE.md` mentions this, so a stale token reads as a broken repo. Recovery, and why
  `pnpm gcp-auth` can't perform it, is in `knowledge.md` (2026-08-12).

- **fio and ripley have opposite code-style rules.** fio *requires* comments that explain
  the **why** and TSDoc on every exported symbol (`CLAUDE.md` → "Code Comments"); ripley
  forbids comments outright. fio is oxlint + oxfmt; ripley is Biome. Carrying a convention
  across the two is the most likely cross-contamination, in both directions.

- **`CLAUDE.md`'s three worked examples are fixed, not open work.** The carousel
  `isInEditor` prop (#374), hotspot's `useBlockEditorState()` (#377) and module's nested
  `EntityStoreProvider` (#384 / RFC 0016) are kept as *illustrations* of the
  render/handle/interact method. Quoting any of them as a live gap is a documented
  mistake — the file says so explicitly.

- **You don't own this repo's agent config.** `CLAUDE.md` is 17 commits by **sven** (12)
  and **Sean Reilly** (5); `AGENTS.md`, `CONTEXT.md` and `.claude/` are sven's. Changing
  them is a PR through the team, which is why your own findings live in this skill instead
  (PCS-9a). Practical consequence: prefer proposing a change over making one.
