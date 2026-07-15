# Category: design

**Scope.** Everything visual and UX — creating interfaces and refining them. Split into two subcategories:

- **`build/`** — create interfaces, translate designs to code, and the one-time design-context setup.
- **`refine/`** — take an *existing* interface and improve one specific dimension (the cohesive design-partner suite).

All design skills should read the project's `## Design Context` in `CLAUDE.md` (established once by `teach-impeccable`) so output stays consistent with the project's look & feel.

**Naming.** `build/` = descriptive (`frontend-design`, `mobile-responsive`). `refine/` = a single verb or adjective naming the transformation (`polish`, `bolder`, `quieter`, `distill`).

**Tone & audience.** Senior product designer. Opinionated on craft, avoids generic AI aesthetics, accessibility-aware (light + dark).

**Required scaffolding.** `references/` for design principles/examples where useful; most `refine/` skills are single-file.

**Default frontmatter.**
```yaml
name: <folder-name>
description: <what it does + trigger phrases>
user-invokable: true
```

See `build/_category.md` and `refine/_category.md` for the per-subcategory rules.
