---
name: progress-report
description: >-
  Generates project progress reports: a non-technical version (3 pages max,
  business language, RAG status) for the client, and a technical version
  (detailed, with metrics, debt, security, RAID) for the team. Branded PDF
  export. Use this skill whenever the user asks for: "progress report",
  "status report", "client report", "technical report", "weekly report",
  "recap of the week", "what did we do this week", "report for the client",
  "report for the team".
---

# Progress Report

Generates progress reports in 2 versions: client (non-technical, 3 pages) and technical (detailed, no limit).

## When to use

- End of week — weekly recap
- End of sprint — review
- Before a client meeting — preparing the status
- Client request — "send me a progress update"

## Workflow — 2 agents in parallel

### Step 1 — Choose the type

The user specifies the type, or both are generated:

| Command | Result |
|---|---|
| "client report" | Non-technical only (3 pages) |
| "technical report" | Technical only (no limit) |
| "progress report" | **Both** in parallel |

### Step 2 — Spawn the agents

**Agent `client-report-writer`** — non-technical report:
- 3 pages max, business language
- RAG status per dimension (scope, schedule, budget, risk)
- Assertive title, 3-sentence summary, achievements in business language
- Risks with 2 options + recommendation
- Decisions required from the client
- Bans all tech jargon

**Agent `tech-report-writer`** — technical report:
- 8 sections: sprint overview, quality metrics, hotspots, technical debt, security, architecture, RAID log, next steps
- Velocity, coverage, build status, feature/debt ratio
- Hotspot files, npm audit vulnerabilities
- Next steps prioritized by Value/Effort
- Full transparency, zero embellishment

### Step 3 — Deliver and offer the export

Present the reports in the conversation. Then offer:

> "Would you like me to generate the branded PDFs?"

If yes → call `pdf-generator` for each report.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| Period | 7 days | `--since` for git log |
| Project | Current directory | Path to the git repository |
| Client | Inferred from the project | Client name for the report |

## Applied standards

Both reports follow the PMI/ISO 21502 standards. Read `references/report-standards.md` for:
- RAG definitions and quantitative thresholds
- Detailed structure of the 2 report types
- Principles: Pyramid Principle, anti-watermelon, bad news early, 5-15 rule
- Visualization rules (Tufte/Knaflic)

## Agents

| Agent | Role | Audience | Limit |
|---|---|---|---|
| `client-report-writer` | Non-technical report | CEO, CFO, client | 3 pages max |
| `tech-report-writer` | Technical report | CTO, devs, tech lead | No limit |

## PDF export

Via `pdf-generator` with:
- Dark UI Kit cover (assertive title, client, date, reference)
- RAG matrix as colored KPI cards
- Tables for milestones, budget, risks, RAID
- Charts for velocity and breakdown (technical only)
- Back cover CTA with contact details

## Failure modes

| Failure | Recovery |
|-------|----------|
| No git repository | Flag it, ask for the path |
| No commits | Widen the period |
| No budget/milestones | Omit the sections, flag it |
| Agent timeout | Deliver the available report |
| PDF export fails | Deliver as text |
| Client report > 3 pages | Trim — 3 pages max, move the overflow to an appendix |
