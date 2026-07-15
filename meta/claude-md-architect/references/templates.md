# Ready-to-use CLAUDE.md templates

5 templates covering the most common cases. Each is ≤ 60 lines, structured WHAT/WHY/HOW.

---

## Template 1 — Web application (front + back)

```markdown
# CLAUDE.md

## WHAT
- Type: B2B SaaS [domain]
- Front: React + TypeScript + Vite (`apps/web/`)
- Back: Node.js + Express + Prisma (`apps/api/`)
- DB: PostgreSQL (managed via Prisma migrations)
- Tests: Vitest (front) / Jest (back)
- Deploy: Vercel (front) / Railway (back)

## WHY
- Optimize time-to-decision for [target persona]
- Business constraint: GDPR compliance (EU data only)

## HOW

### Commands
- Install: `pnpm install`
- Dev: `pnpm dev` (front + back in parallel via Turborepo)
- Tests: `pnpm test` (before every commit)
- Lint: `pnpm lint --fix`
- DB migration: `pnpm db:migrate:create <name>` (never a direct `ALTER TABLE`)

### Conventions
- React components: `PascalCase.tsx` in `components/`
- Hooks: `useXxx.ts` in `hooks/`
- API routes: RESTful, kebab-case (`/api/users/by-email`)
- Input validation: zod schemas in `src/schemas/` (never raw `req.body`)

### Always
- Before every PR: `pnpm test && pnpm lint`
- Every API endpoint must have a zod schema and an integration test

### Details
- Architecture: @.claude/rules/architecture.md
- Security: @.claude/rules/security.md
```

---

## Template 2 — Open-source library

```markdown
# CLAUDE.md

## WHAT
- Library: [name] — [one-line description]
- Language: TypeScript (targets Node ≥ 18 and modern browsers)
- Build: tsup (ESM + CJS + types)
- Tests: Vitest
- Docs: TypeDoc + Docusaurus site (`docs/`)

## WHY
- Ship a fast, type-safe [domain] standard
- Zero runtime dependencies (peer deps only)

## HOW

### Commands
- Install: `pnpm install`
- Build: `pnpm build`
- Tests: `pnpm test` (coverage > 90% required on main)
- Release: `pnpm changeset` then `pnpm release` (CI)

### Conventions
- Public API: everything exported from `src/index.ts` only
- Breaking changes: follow strict semver, note them in `CHANGELOG.md`
- Tests: one `<module>.test.ts` file per source file

### Always
- Every new public API needs: a test + TypeDoc docs + a README entry
- Types must be exported explicitly (not just inferred)

### Contributing
- See `CONTRIBUTING.md` for the PR procedure
```

---

## Template 3 — Monorepo (Turborepo / Nx)

```markdown
# CLAUDE.md

## WHAT
- Turborepo monorepo
- Apps: `apps/web/`, `apps/admin/`, `apps/api/`
- Packages: `packages/ui/`, `packages/shared/`, `packages/db/`
- Package manager: pnpm workspaces

## WHY
- Code shared across 3 products with independent deployments
- Fast iteration on the shared UI layer

## HOW

### Commands (from the root)
- Install: `pnpm install`
- Dev (all apps): `pnpm dev`
- Dev (single app): `pnpm dev --filter web`
- Tests: `pnpm test` (run affected only via Turbo)
- Build: `pnpm build` (Turbo cache enabled)

### Conventions
- Every internal package: `@myorg/` prefix (e.g. `@myorg/ui`)
- No direct imports between apps (go through packages/)
- Internal versions: `workspace:*`

### Always
- Before push: `pnpm lint && pnpm test --filter=...[origin/main]`
- Any change to `packages/db/` requires a migration test

### Per subdirectory
- Front-specific conventions: @apps/web/CLAUDE.md
- Back-specific conventions: @apps/api/CLAUDE.md
- UI library conventions: @packages/ui/CLAUDE.md
```

---

## Template 4 — Client project (agency)

```markdown
# CLAUDE.md

## WHAT
- Client: [client name]
- Project: [project name] — [type: MVP / rebuild / extension]
- Stack: [main technologies]
- Timeframe: [dates]

## WHY
- Business goal: [one sentence]
- Critical constraints: [budget / deadline / compliance]

## HOW

### Commands
- [Essential project commands]

### Conventions
- Commits: conventional commits (`feat:`, `fix:`, `refactor:`...)
- PRs: description with Summary + Test plan + Screenshots sections
- Code review: at least 1 approval before merging to `main`
- Documentation: every API endpoint documented (OpenAPI or JSDoc)

### Always
- Before a sprint delivery: audit with the `audit` skill (accessibility + perf)
- Before a prod deploy: use the `change-advisor` skill to assess risk

### Client specifics
- @.claude/rules/client-specifics.md (NDA — do not share)
```

---

## Template 5 — Personal configuration (`~/.claude/CLAUDE.md`)

```markdown
# CLAUDE.md (personal)

## Communication preferences
- Responses in English
- Concise: no over-summarizing, no "here's what I did"
- Cite files with `path:line` for navigation

## Working style
- Favor simple solutions (3 repeated lines > premature abstraction)
- Never add comments unless the reasoning is non-obvious
- No README/docs unless explicitly asked
- Ask before destructive actions (rm, force push, drop table...)

## Favorite tools
- Preferred skills: `documentor`, `senior-dev`, `architecture-conceptor`, `apply`
- For research: `documentor` (auto-detected mode)
- For technical decisions: `senior-dev`

## Frequent workflows
- Research → client brief: `/research-brief`
- Code audit: `/code-review`
- Security audit: `/security-review`

## Always
- If an action affects multiple people (push, PR, message) → confirm first
- If a test fails after a change → fix the cause, don't disable the test
```

---

## How to choose / adapt a template

1. **Identify the scope**: project vs personal vs library vs monorepo vs client.
2. **Copy the closest template.**
3. **Customize the WHAT/WHY/HOW sections** with the real information.
4. **Trim** what doesn't apply (don't keep placeholders).
5. **Check the size**: it must stay ≤ 60 lines after customization.
6. **Add `@imports`** if more detail is needed (but outside the main CLAUDE.md).

---

## Anti-template (what NOT to do)

```markdown
# CLAUDE.md (350 mixed-up lines)

## About this project
This project is a comprehensive solution for managing... [3 paragraphs]

## How to do everything
1. To deploy... [15 steps]
2. To debug... [12 steps]
3. To run tests... [8 steps]

## Code style
- Use clean code
- Follow best practices
- Be careful with the database
- Format properly
- Use 2 spaces, single quotes, no trailing whitespace, max 100 chars [...]

## API documentation
[200 lines of inlined Stripe / OpenAI docs]
```

→ Score: ~15/100. Radical refactor required (see Mode ✂️ Refactor workflow).
