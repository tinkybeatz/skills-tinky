# Catalog of the 10 CLAUDE.md anti-patterns

Each anti-pattern is documented with: **detection**, **why it's bad**, **BEFORE example**, **AFTER fix**, **destination of the moved content**.

---

## 1. Too long (> 200 lines)

**Detection**: `wc -l CLAUDE.md` > 200.

**Why**: degraded adherence — Claude starts ignoring rules, especially those buried in the middle. Token cost on every session.

**BEFORE** (350 lines mixing everything together)

**AFTER**: index ≤ 60 lines + modular `@.claude/rules/<topic>.md`.

**Destination**: `.claude/rules/`, skills, hooks, depending on the content type.

---

## 2. Multi-step procedures

**Detection**: numbered sections with ≥ 3 sequential steps ("1. Do X, 2. Then Y, 3. Finally Z").

**Why**: this is a **skill** (workflow), not a persistent rule. It loads the context unnecessarily.

**BEFORE**
```markdown
## To deploy to production
1. Run `npm run test:e2e`
2. Check coverage > 80%
3. Tag the commit
4. Push to `main`
5. Check the GitHub Actions pipeline
6. Notify #deploys on Slack
```

**AFTER** in CLAUDE.md
```markdown
- Prod deployment: use `/deploy` (dedicated skill)
```

**Destination**: skill `~/.claude/skills/deploy/SKILL.md` with `disable-model-invocation: true`.

---

## 3. Formatting rules (linter territory)

**Detection**: "Use 2 spaces", "no trailing whitespace", "use single quotes", "max line length 100".

**Why**: the linter (prettier, eslint, ruff) does it better and deterministically.

**BEFORE**
```markdown
- Use 2-space indentation
- Single quotes for strings
- No trailing whitespace
- Max line 100 chars
```

**AFTER** in CLAUDE.md
```markdown
- Before every commit: `npm run lint` (config in `.eslintrc.json`)
```

**Destination**: `.eslintrc.json`, `.prettierrc`, `pyproject.toml` (linter config).

---

## 4. Inline code snippets > 5 lines

**Detection**: ` ``` ` blocks longer than 5 lines in CLAUDE.md.

**Why**: verbose, quickly outdated, weighs down every session. A `file:line` reference survives refactors.

**BEFORE**
```markdown
## Auth pattern
```typescript
export async function authenticate(token: string) {
  const decoded = jwt.verify(token, SECRET);
  if (!decoded) throw new UnauthorizedError();
  return await db.users.findUnique({ where: { id: decoded.sub } });
}
```
```

**AFTER**
```markdown
- Auth: see `src/auth/index.ts:42-58` (JWT + user lookup pattern)
```

**Destination**: a `file:line` pointer in CLAUDE.md; the code stays where it is.

---

## 5. Vague directives

**Detection**: "follow best practices", "write good code", "be careful", "format properly", "be consistent", "make it clean".

**Why**: not verifiable → Claude doesn't know what to do concretely.

**BEFORE**
```markdown
- Write clean, readable code
- Follow best practices
- Be careful with the database
```

**AFTER**
```markdown
- Variables: `camelCase`; constants: `SCREAMING_SNAKE_CASE`
- DB migrations: always via `npm run migrate:create`, never a direct `ALTER TABLE`
- Every SQL query must use prepared statements (`db.query(SQL`...`, [params])`)
```

**Destination**: stays in CLAUDE.md but rewritten as specific and verifiable.

---

## 6. Narrative paragraph content

**Detection**: long sentences with no bullets, > 3 consecutive lines with no break.

**Why**: Claude scans bullets first. Narrative text is diluting.

**BEFORE**
> This project is a task-management application built for distributed teams. It uses React with TypeScript on the front end and Node.js with Express on the back end. The database is PostgreSQL and we use Prisma as the ORM. Tests are written with Vitest on the front end and Jest on the back end. Deployment runs on Vercel for the front end and Railway for the back end.

**AFTER**
```markdown
## Stack
- Front: React + TypeScript + Vite
- Back: Node.js + Express + Prisma
- DB: PostgreSQL
- Tests: Vitest (front) / Jest (back)
- Deploy: Vercel (front) / Railway (back)
```

**Destination**: stays in CLAUDE.md, converted into structured bullets.

---

## 7. Cross-file duplication

**Detection**: grep a CLAUDE.md rule across `.claude/skills/`, `.claude/rules/`, `MEMORY.md`. If found elsewhere → duplication.

**Why**: drift is guaranteed when one copy is modified and the other isn't. Multiplied context cost.

**BEFORE**
- CLAUDE.md line 23: "Always respond in French"
- `~/.claude/CLAUDE.md` line 5: "Responses in French"
- `MEMORY.md` line 12: "User prefers French"

**AFTER**: a single occurrence (the highest one in the cascade that covers the needed scope).

**Destination**: cross-cutting personal rule → `~/.claude/CLAUDE.md` only. Remove it elsewhere.

---

## 8. Unnecessary non-English content

**Detection**: sections of technical docs in another language that could be in English.

**Why**: other languages can consume **30–50% more tokens** than an English equivalent ([humanlayer.dev](https://www.humanlayer.dev/blog/writing-a-good-claude-md)).

**Legitimate case**: an explicit user preference ("I want to work in French") → keep it.

**Illegitimate case**: code comments, internal technical descriptions → translate to English.

**Destination**: stays in CLAUDE.md, translated.

---

## 9. Wrong placement of critical rules

**Detection**: "always" / "never" rules buried in the middle of a long document.

**Why**: primacy/recency effect — Claude pays more attention to the start and end of the file.

**BEFORE**: critical rule on line 87 of 142.

**AFTER**: critical rule at the top (right after the title) OR at the bottom (an "Inviolable rules" section).

**Destination**: stays in CLAUDE.md, repositioned.

---

## 10. Personal preferences in a project CLAUDE.md

**Detection**: "I prefer", "I like", "my style is", "always use informal address" in a committed `<project>/CLAUDE.md`.

**Why**: pollutes the team CLAUDE.md with personal preferences. Causes conflicts when different devs have different preferences.

**BEFORE** in `<project>/CLAUDE.md`
```markdown
- Use informal address with the user
- No emojis in commits
- Prefer short explanations
```

**AFTER**: moved to `~/.claude/CLAUDE.md` (personal) or `<project>/CLAUDE.local.md` (personal project, gitignored).

**Destination**: `~/.claude/CLAUDE.md` or `<project>/CLAUDE.local.md`.

---

## Bonus — secondary anti-patterns

| Anti-pattern | Detection | Fix |
|---|---|---|
| Auto-generated content | "Generated by X — do not edit" sections | Regenerate or remove |
| Links to dead external resources | 404 URLs | Verify + replace |
| Hardcoded versions | "Use Node 18.2.0" | Prefer "Use the Node version from `.nvmrc`" |
| Contradictory cross-level instructions | User says X, project says Y | Pick a single source of truth |
| Excessive HTML comments | `<!-- -->` everywhere | Useful for internal notes (not sent), but use sparingly |

---

## Reporting format within an audit

```markdown
## 🚨 Anti-patterns detected (X occurrences)

1. **#2 Multi-step procedures** — l.45-58 (deployment)
   → Migrate to skill `deploy`
2. **#5 Vague directives** — l.12 ("write clean code")
   → Rewrite as verifiable rules
3. **#7 Duplication** — l.23 duplicated in `~/.claude/skills/test-writer/SKILL.md` l.5
   → Remove from CLAUDE.md (keep it in the skill)
```
