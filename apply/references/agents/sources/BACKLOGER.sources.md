# BACKLOGER Source Policy

## Source tiers

### Tier 1 — Primary sources (default priority)

- the source report itself (brief, architecture ADR, senior-dev analysis, audit)
- current codebase state (files, tests, configurations, conventions)
- referenced standards from the source report
- BACKLOG_STANDARD template and rules

### Tier 2 — Strong supporting sources

- git history and recent changes relevant to affected components
- existing test suites and CI/CD pipeline configuration
- related documentation (README, CLAUDE.md, API docs)
- dependency manifests (package.json, Dockerfile, docker-compose)

### Tier 3 — Context-only sources

- verbal or chat-based clarifications from the user without written trace
- assumptions about project conventions not confirmed by codebase reading
- external documentation not referenced in the source report

## Usage rules

- Always prioritize Tier 1 for backlog item creation and evidence linking.
- Use Tier 2 to validate feasibility and identify hidden dependencies.
- Use Tier 3 only as context enrichment, never as sole basis for a backlog item.

## Minimum evidence policy

- At least 1 direct source report reference for every backlog item.
- At least 1 codebase reference for every `Now` item (feasibility confirmation).
- No backlog item created from assumptions not present in the source report.
- Ambiguous decisions must be flagged, not silently interpreted.

## Freshness policy

- Source report is assumed current at time of processing.
- Codebase state must be verified at extraction time (read files, don't rely on memory).
- If the source report references outdated code paths, flag the discrepancy.

## Credibility checks

Before including a source reference, verify:

- the referenced section exists in the source report (quote or section heading)
- the referenced file exists in the codebase (use Glob or Read to confirm)
- the claim is directly relevant to the backlog item being created
- feasibility is confirmed by actual code structure, not assumption

## Rejection rules

Reject or flag sources when:

- source report section is vague and does not contain actionable decisions
- codebase file referenced no longer exists or has been significantly modified
- claim cannot be traced to an auditable source (report section or code file)
- user clarification contradicts source report without explicit change trace

## Citation format standard

For each cited source include:

- source title (report name, file path, or section heading)
- location (file path, section reference, or line number)
- type (`source-report` | `codebase` | `standard` | `user-clarification`)
- one-line relevance rationale
