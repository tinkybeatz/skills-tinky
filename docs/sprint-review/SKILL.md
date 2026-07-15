---
name: sprint-review
description: >-
  Analyzes a project's most recent technical work (commits, code, PRs) and produces
  a structured agile progress report: logical next steps, continuous improvement,
  efficiency metrics, architecture review, and security review. PDF export included.
  Use this skill whenever the user asks: "analyze what was done",
  "sprint review", "sprint review", "what should we do next",
  "next steps", "project progress", "technical review", "sprint recap",
  "measure efficiency", "progress report", "what's left to do".
---

# Sprint Review

Automatic analysis of recent technical work with prioritized recommendations, an architecture review, and a security review.

## When to use

- End of sprint or end of week — a recap
- Before a client meeting — to prepare the next steps
- To measure the efficiency of a period of work
- To decide what to do next (prioritization)

## Workflow — Fan-out / Fan-in (3 agents in parallel)

### Step 1 — Collect the data

Before spawning the agents, collect the shared context:
```bash
git log --oneline --since="7 days ago" --no-merges
git diff --stat HEAD~20 HEAD
```

This context (list of commits + changed files + diffs) is passed to all 3 agents.

### Step 2 — Spawn the 3 agents IN PARALLEL

Launch all 3 agents in the same message (fan-out):

**Agent 1: `sprint-analyzer`** — agile analysis
- Work categorization (feature/fix/refactor/infra)
- Metrics: throughput, feature/debt ratio, hotspots
- Prioritized next steps (Value/Effort)
- Continuous improvement

**Agent 2: `architecture-reviewer`** — architecture review
- Architectural consistency (bounded contexts, imports, layers)
- Coupling and dependencies introduced
- Architectural debt introduced
- Score A/B/C/D + recommendations

**Agent 3: `security-reviewer`** — security review
- OWASP Top 10 scan on the diffs
- Dangerous patterns (injection, broken access, exposed secrets)
- Configuration (CORS, headers, debug mode)
- Score A/B/C/D + vulnerabilities

### Step 3 — Synthesize (fan-in)

Combine the 3 reports into a single deliverable with 5 sections:

1. **Summary** — period, throughput, architecture/security scores
2. **What was delivered** — categorized, factual
3. **Efficiency metrics** — throughput table, ratio, hotspots
4. **Architecture review** — score, debt introduced, recommendations
5. **Security review** — score, vulnerabilities, fixes
6. **Logical next steps** — prioritized next steps, incorporating the architecture + security recommendations
7. **Decisions to make** — timeboxed

The architecture and security scores influence the prioritization of next steps: architectural debt rated D or a critical vulnerability is automatically promoted to a Quick Win.

### Step 4 — Deliver and offer the export

Present the consolidated report. Then offer:

> "Would you like me to generate a branded PDF with this report?"

If yes → call `pdf-generator` with the structured content.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| Period | 7 days | `--since` for git log |
| Branch | current | Branch to analyze |
| Depth | 20 commits | Maximum number of commits |

## References

Read `references/agile-metrics-guide.md` for prioritization frameworks (RICE, WSJF, Value/Effort), progress metrics, and technical debt management.

## Agents

| Agent | Role | Based on |
|---|---|---|
| `sprint-analyzer` | Agile analysis, metrics, next steps | Agile documentor report |
| `architecture-reviewer` | Architecture review, structural debt | `architecture-conceptor` skill |
| `security-reviewer` | Security review, OWASP scan | `pentest-audit` skill |

The 3 agents are spawned in parallel, then their results are merged.

## PDF Export

Via `pdf-generator`:
- Dark UI Kit cover
- KPI cards: throughput, architecture score (A-D), security score (A-D)
- Tables: next steps, vulnerabilities, debt
- Back cover CTA

## Failure modes

| Failure | Recovery |
|-------|----------|
| No git repository | Report it and ask for the path |
| No commits in the period | Widen the period |
| Architecture/security agent timeout | Deliver the report without the missing section |
| Too many commits (100+) | Limit to 50, mention it |
| PDF export fails | Deliver as text |
</content>
</invoke>
