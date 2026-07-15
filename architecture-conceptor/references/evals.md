# ARCHITECTURE_CONCEPTOR Evaluation Set

## Objective

Validate that `ARCHITECTURE_CONCEPTOR` consistently produces well-framed, evidence-based, and actionable architecture decision packages.

## Evaluation protocol

For each test case:

1. Run one full delivery cycle (framing, modeling, options, decision, validation).
2. Produce output using the required contract.
3. Score with `rubric.md`.
4. Record pass/fail and failure reasons.

Pass criteria:

- score >= 80
- no hard fail condition

## Test cases

### TC-01 Greenfield B2B platform

Prompt:

- "Design the architecture for a B2B SaaS order management platform. Requirements: 99.95% availability, moderate cost constraints, 500 concurrent users at launch scaling to 5000 within 18 months, EU data residency."

Expected:

- explicit constraints and quality attribute priorities
- bounded contexts and architecture views
- at least 3 architecture options with quality and cost trade-offs
- weighted scorecard driving recommendation
- validation plan with measurable checkpoints and rollback triggers

### TC-02 Monolith to services migration

Prompt:

- "We have a 200k LOC Rails monolith handling orders, inventory, and billing. Team of 8. Propose a modernization strategy with minimal business disruption."

Expected:

- current state assessment and constraint inventory
- at least 3 migration strategies (strangler fig, modular extraction, parallel rewrite)
- sequencing plan with dependencies
- economic analysis (migration cost vs. status quo cost)
- rollback triggers and coexistence strategy

### TC-03 Event sourcing vs CRUD decision

Prompt:

- "Should we use event sourcing or CRUD for our billing module? We process 10k invoices/month, need full audit trail, and the team has no event sourcing experience."

Expected:

- constraint framing (volumetry, audit needs, team capability)
- at least 3 options (CRUD + audit log, full event sourcing, hybrid)
- trade-offs on complexity, audit capability, team ramp-up time
- clear recommendation with conditions for revisiting

### TC-04 Multi-region deployment architecture

Prompt:

- "We need to serve users in EU and US with strict latency requirements (<200ms p95) and GDPR compliance. Currently single-region. Design the target architecture."

Expected:

- regulatory and latency constraint analysis
- data residency and replication strategy options
- at least 3 deployment topology options
- cost and operational complexity trade-offs
- validation plan with latency and compliance checks

### TC-05 Real-time vs batch processing decision

Prompt:

- "Our analytics pipeline processes 50M events/day in nightly batch jobs. Product wants real-time dashboards. What architecture should we adopt?"

Expected:

- current state assessment and gap analysis
- at least 3 options (optimize batch, lambda architecture, full streaming)
- trade-offs on cost, latency, complexity, and data consistency
- migration path from current to target state
- measurable success criteria

## Reporting template

Use this after each evaluation run:

```md
## Eval Report - <TC-ID>

- Date:
- Evaluator:
- Final score:
- Hard fail: yes|no

### Criterion scores

- Fit to problem and constraints:
- Evidence strength and traceability:
- Trade-off rigor and decision quality:
- Clarity and actionability:
- Limitations and risk transparency:

### Outcome

- Pass|Fail

### Notes

- Strengths:
- Weaknesses:
- Fix actions:
```
