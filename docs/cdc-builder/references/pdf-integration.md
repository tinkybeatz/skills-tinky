# pdf-generator integration

The `cdc-builder` skill produces branded PDF deliverables by orchestrating the
`pdf-renderer` agent from the `pdf-generator` skill.

---

## When to generate a PDF

At the end of any complete mode, **always offer** to generate the PDF:

- Generation mode → complete CdC to deliver to the client
- Audit mode → audit report to deliver to the client
- Legal mode → compliance memo to deliver to the legal team

**Always ask for confirmation** before generating (the user may prefer to stay
in markdown for a revision).

---

## Invocation contract

Spawn the agent via the Agent tool:

```
Agent({
  description: "Generate the cahier des charges PDF",
  subagent_type: "general-purpose",
  prompt: """
  Skill path: ~/.claude/skills/pdf-generator

  Generate a PDF with the following content:

  Title: [Document title]
  Recipient: [Legal name]
  Date: [YYYY-MM-DD]
  Type: report

  Sections:
  1. [Title] — [markdown content]
  2. [Title] — [markdown content]
  ...

  Output path: [/tmp/cdc-{slug}-{YYYYMMDD}.pdf]
  """
})
```

### Required fields

| Field | Description |
|-------|-------------|
| **Title** | Appears on the cover. Suggested format: *"Cahier des charges — [Project name]"* |
| **Sections** | A numbered list. Each section = `<title> — <markdown content>` |

### Optional fields

| Field | Default | Notes |
|-------|--------|-------|
| **Recipient** | none | Appears on the cover |
| **Date** | today | ISO format `YYYY-MM-DD` |
| **Type** | `report` | `report` / `proposal` / `brief` / `audit` |
| **Output path** | `/tmp/cdc-{timestamp}.pdf` | Prefer an explicit path |
| **Format** | A4 portrait | A4/A3, portrait/landscape |

---

## Prompt templates by mode

### Generation mode — complete CdC

```
Title: Cahier des charges — Redesign of [Client]'s site
Recipient: [Legal name, address]
Date: 2026-04-29
Type: report

Sections:
1. Client overview — [content]
2. Context and stakes — [content]
3. SMART objectives — [content]
4. Targets and personas — [content]
5. Functional scope — [content]
6. Functional specifications — [requirements table ID/Statement/Priority/Acceptance]
7. Technical specifications — [content]
8. Design and UX — [content]
9. Constraints (GDPR, accessibility, performance) — [content]
10. Timeline and milestones — [table]
11. Budget and financial terms — [content]
12. Acceptance procedures — [content]
Appendices — [glossary, normative references]

Output path: /tmp/cdc-[project-slug]-[YYYYMMDD].pdf
```

### Audit mode — audit report

```
Title: Cahier des charges audit — [Name of the audited document]
Recipient: [Party commissioning the audit]
Date: 2026-04-29
Type: audit

Sections:
1. Executive summary — overall score, top 3 findings
2. Audit methodology — frameworks applied (ISO 29148, EN 16271)
3. Detailed score by dimension — [table of 7 dimensions × weight]
4. Top 10 prioritized defects — [table ID/Description/Impact/Effort]
5. Anti-patterns detected — [list with locations]
6. Missing sections — [vs. chosen template]
7. Legal risks — [enforceability conformance]
8. Remediation plan — [prioritized actions]
Appendices — [detailed grid, statistics]

Output path: /tmp/audit-cdc-[slug]-[YYYYMMDD].pdf
```

### Legal mode — enforceability memo

```
Title: Contractual compliance memo — [Name of the CdC]
Recipient: [Legal department / Client]
Date: 2026-04-29
Type: report

Sections:
1. Summary — enforceable yes/no/conditional
2. Enforceability checklist — [10 points checked/unchecked]
3. Applicable case law — [TC Paris 2020, CA Paris 2023, etc.]
4. Missing clauses — [list with proposed wording]
5. Identified litigation risks — [scenarios + impacts]
6. Recommendations — [actions before signing]

Output path: /tmp/legal-cdc-[slug]-[YYYYMMDD].pdf
```

---

## Expected agent output

The agent returns (to be parsed):

```
PDF_PATH: /tmp/cdc-projet-x-20260429.pdf
HTML_PATH: /tmp/cdc-projet-x-20260429.html
PAGES: 28
STATUS: success
```

Then tell the user:
- The PDF path
- The page count
- Offer to open it (`open <path>` on macOS)
- Offer a Notion export via `mcp__claude_ai_Notion`

---

## Failure modes

| Failure | Recovery |
|-------|--------------|
| Playwright not installed | The agent handles it automatically (`npx playwright install`) |
| Content too long for one section | Split the section into sub-sections |
| Special characters rendered incorrectly | Check the UTF-8 encoding of the source markdown |
| Playwright timeout | Retry once, then deliver the raw markdown |
| Invalid output path | Fall back to `/tmp/` |
| Status: error | Preserve the source markdown, report the failure, offer a retry |

---

## Slug and naming

Convention for the `output path`:

```
/tmp/{type}-cdc-{client-slug}-{YYYYMMDD}.pdf
```

- `type`: `cdc`, `audit-cdc`, `legal-cdc`
- `client-slug`: kebab-case, no accents, < 30 chars
- `YYYYMMDD`: today's date

Examples:
- `/tmp/cdc-acme-refonte-20260429.pdf`
- `/tmp/audit-cdc-startup-x-20260429.pdf`
- `/tmp/legal-cdc-marche-public-y-20260429.pdf`
