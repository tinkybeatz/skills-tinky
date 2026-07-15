# TASKER Source Policy

## Source tiers

### Tier 1 — Execution source of truth (default priority)

- backlog artifacts (item objective, scope, acceptance criteria, dependencies, owner, ready status)
- `references/BACKLOG_STANDARD.md`
- standards referenced by the backlog traceability matrix
- repository-native evidence: code, tests, CI results, logs, runbooks

### Tier 2 — Strong supporting sources

- architecture decisions and design records linked by backlog artifacts
- testing and audit standards and related audit folders
- feature documentation for traceability and closure consistency

### Tier 3 — Context-only sources

- undocumented team assumptions
- informal chat notes without traceable artifact links
- opinions without reproducible evidence

## Usage rules

- Always prioritize Tier 1 for execution and closure decisions.
- Use Tier 2 to complete operational and governance context.
- Use Tier 3 only to generate follow-up verification tasks, never as closure evidence.
- For each applicable standard, retrieve and verify its associated audit artifact before closure.

## Minimum evidence policy

- Each acceptance criterion must have at least 1 direct evidence artifact.
- High-impact closure decisions require at least 2 independent evidence types.
- No critical completion claim without explicit test or runtime validation proof.
- Each applicable standard must have at least 1 associated audit evidence entry (`pass`, `fail`, or justified `not-applicable`).

## Freshness policy

- For active execution cycles, use current branch/recent CI evidence only.
- For volatile constraints (security/performance/ops), prefer latest validated runs and timestamps.
- If evidence is stale, mark item as `iterate` until fresh validation is provided.

## Credibility checks

Before accepting evidence, verify:

- source ownership and reproducibility
- direct linkage to the target backlog item
- consistency with referenced standards
- consistency between each standard and its associated audit result
- explicit result state (`pass`/`fail`)

## Rejection rules

Reject or down-rank evidence when:

- no timestamp, no owner, or no execution context
- result cannot be reproduced from declared commands or pipeline
- claim is disconnected from acceptance criteria
- standard coverage is asserted without rule-level linkage
- a standard is marked compliant without associated audit verification

## Citation format standard

For each evidence entry include:

- backlog item ID
- acceptance criterion ID or criterion text
- standard ID
- associated audit ID/check reference
- evidence type
- location (file path, report path, URL, or log reference)
- date/time (when available)
- one-line relevance rationale
