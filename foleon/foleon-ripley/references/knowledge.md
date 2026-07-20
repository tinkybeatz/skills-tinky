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
