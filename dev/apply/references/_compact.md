# Apply — Compact Reference

## Backlog Horizons

| Horizon | Description |
|---------|-------------|
| `Now` | Ready for next 1-2 sprints |
| `Next` | Candidate work, partially refined |
| `Later` | Opportunities requiring discovery |

## Item Types

`Feature` | `User Story` | `Bug` | `Enabler` | `Spike`

`Epic` = grouping container only. MUST NOT be committed to a sprint.

## Mandatory Item Fields (all sprint candidates)

- Unique ID
- Concise title
- Problem statement / user value
- Evidence links (from Evidence Register, e.g. `E-ARCH-005`)
- Acceptance criteria
- Links to evidence (qualitative/quantitative)
- Estimate (relative size or effort band)
- Dependencies / constraints
- Risk notes
- Owner
- Target horizon (`Now`/`Next`/`Later`)
- Release-readiness gate definition
- Release evidence expectations + go/no-go decision owner

### Additional mandatory fields for `Now` items (Technical Backlog Profile)

- Affected components/modules
- Contract impact (`new`/`changed`/`none`) + contract IDs
- Data/security impact classification
- Failure handling strategy (`retry`/`fallback`/`fail-fast`/`manual`)
- Test scope declaration (unit/integration/e2e/security/performance)
- Telemetry expectations (metrics/logs/traces)

## Technical Backlog Profile Activation

Active when any condition is true:
1. Impacts runtime orchestration, module boundaries, protocols, or execution routing
2. Introduces/modifies security-sensitive decision flows
3. Includes fallback/retry/state-machine behavior
4. Depends on AI model decisions affecting runtime behavior

### Required sections when active

- Target Architecture
- Execution Paths (primary + fallback)
- Service Contract Inventory (I/O contracts + owners)
- State Machine (transitions + terminal outcomes)
- Failure Taxonomy (mapped remediation)
- Security Invariants (non-bypass guarantees)
- Observability Contract (correlation IDs + SLO metrics)
- ADR Decisions to Lock
- Delivery Sequencing (rollout phases)

## Definition of Ready Checklist

| # | Criterion | Technical Profile |
|---|-----------|:-:|
| 1 | Value and objective explicit | |
| 2 | Acceptance criteria testable | |
| 3 | Dependencies identified | |
| 4 | Scope fits one sprint | |
| 5 | Estimate agreed by team | |
| 6 | No critical ambiguity | |
| 7 | Release-readiness gates + evidence defined | |
| 8 | Contract impacts identified and owned | X |
| 9 | Failure behavior defined | X |
| 10 | Security implications explicit | X |
| 11 | Observability fields defined | X |

Items failing ANY criterion MUST stay out of sprint commitment.

## Prioritization Formula (WSJF)

```
Priority Score = (Business Value + Time Criticality + Risk Reduction/Opportunity Enablement) / Effort
```

If another method is used, MUST document: formula, tie-breaker rule, review cadence.

### Reprioritization Triggers

- New high-impact customer evidence
- Production incident with product impact
- Major dependency or capacity change
- Strategic objective change

## Evidence Rules

- Every `Now` item MUST include >= 1 evidence link to applicable standard + >= 1 link to runtime/test/operational validation
- High-impact decisions MUST include >= 2 evidence references
- Evidence entries MUST include: source title, path/URL, date, one-line relevance

## Health Metrics + Thresholds

| Metric | Threshold |
|--------|-----------|
| Readiness Ratio (ready / top 20) | >= 70% |
| Backlog Churn (top 10 per sprint) | <= 30% |
| Sprint items linked to AC | 100% |
| Release Gate Coverage (`Now`) | 100% |
| Contract Completeness (Tech Profile `Now`) | 100% |
| Failure Policy Coverage (Tech Profile `Now`) | 100% |
| Observability Coverage (Tech Profile `Now`) | 100% |

## Anti-Patterns (MUST NOT)

- Treat backlog as static requirement document
- Commit unrefined work based only on urgency
- Optimize for story count instead of outcomes
- Keep zombie items (no owner, no evidence, no decision)
- Publish architecture backlogs without execution-path and failure behavior sections

## Standards Traceability Matrix (mandatory in every backlog artifact)

Map each cited standard to: covered scope/items, verification/release gate references, expected evidence artifacts.
