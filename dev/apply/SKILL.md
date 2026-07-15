---
name: "apply"
description: "Transforms a technical report (brief, architecture, audit, senior-dev) into an actionable backlog, then executes the corresponding tasks. Use this skill whenever the user asks to apply, implement, execute, or carry out the content of a report, a deliverable, an analysis, a brief, an ADR, or a technical decision. Also trigger when the user says: 'apply this', 'implement this report', 'execute this decision', 'carry out this brief', 'turn this into tasks', 'set this up', 'deploy this architecture', 'do the work', 'move to implementation', 'start execution', 'implement this plan', or any phrasing that implies turning an analysis/decision document into concrete implementation work."
---

# Apply — From Report to Delivered Code

This skill orchestrates the transformation of a technical report (brief, architecture, audit, senior-dev) into delivered, validated code, in two sequential phases: **BACKLOGER** (planning) then **TASKER** (execution).

---

## Bundled References

This skill ships with its own agents and standards — read them before executing:

- **BACKLOGER agent**: `references/agents/BACKLOGER.md` — profile of the planning agent
- **TASKER agent**: `references/agents/TASKER.md` — profile of the execution agent
- **BACKLOG_STANDARD**: `references/BACKLOG_STANDARD.md` — backlog structuring standard

Read the relevant agent profile at the start of each phase. Read the BACKLOG_STANDARD before generating the backlog in Phase 1.

---

## When to use this skill

- The user has a report produced by another skill (brief-writer, architecture-conceptor, senior-dev, documentor, etc.)
- They want to move from analysis to implementation
- They say "apply", "implement", "execute", "carry out", "set up"

## Main workflow

```
Source report
    │
    ▼
┌─────────────┐    user            ┌─────────────┐
│  BACKLOGER  │ ─────────────────► │   TASKER    │
│ (backlog)   │    confirmation    │ (execution) │
└─────────────┘                    └─────────────┘
    │                                   │
    ▼                                   ▼
  Structured backlog             Delivered code + evidence
```

**Confirmation rule**: always ask the user for confirmation between BACKLOGER and TASKER, unless they have explicitly requested autonomous execution (e.g. "apply everything without asking", "go ahead").

---

## Phase 1 — BACKLOGER

### Mission

Transform the source report into a structured, prioritized, and actionable backlog. The BACKLOGER is a product-planning agent inspired by the PRODUCT_MANAGER profile — it does not code, it structures the work.

### Required input

- The source report (file, conversation, or pasted content)
- Project context (stack, constraints, current state of the code)

### BACKLOGER workflow

#### Step 1 — Extract actionable decisions

Read the source report and extract:

- The technical decisions made (architecture, patterns, technology choices)
- The required changes (new files, modifications, migrations, configurations)
- The constraints and risks identified
- The success or acceptance criteria

Intermediate deliverable: a raw list of identified changes, grouped by domain.

#### Step 2 — Structure the backlog

Transform the raw list into user stories / backlog items that conform to the standard.

Each item MUST include:

- **ID**: unique identifier (format `BLG-XXX`)
- **Title**: concise and action-oriented
- **Problem / Value**: why this item is needed
- **Scope**: what is included and what is not
- **Acceptance criteria**: verifiable and testable (each criterion must have an ID, format `AC-XX`)
- **Dependencies**: items that must be done first
- **Risks**: what could go wrong
- **Estimate**: S / M / L / XL (relative effort)
- **Horizon**: `Now` / `Next` / `Later`
- **Owner**: who is responsible

#### Step 3 — Prioritize and sequence

Order the items by:

1. Dependencies (foundations first)
2. Business value / risk reduction
3. Effort (prefer quick wins early in the sequence)

Define a clear execution sequence: which item comes first, which ones can be parallelized.

#### Step 4 — Definition of Ready

Validate that each `Now` item is ready for execution:

- Explicit objective
- Testable acceptance criteria
- Dependencies identified and non-blocking
- Scope small enough for one iteration
- No critical ambiguity remaining

Mark each item: `Ready` or `Not Ready` (with reason).

### BACKLOGER output

The complete backlog formatted in Markdown with:

1. **Executive summary**: what the report asks for, how many items, estimated total effort
2. **Execution sequence**: recommended order with justification
3. **Backlog items**: each item with all mandatory fields
4. **Dependency matrix**: visualization of dependencies between items
5. **Global risks**: risks that affect the entire backlog

### BACKLOGER output format

```markdown
# Backlog — [Title of source report]

## Executive summary
[2-3 sentences: what, how many items, estimated effort]

## Recommended execution sequence
1. BLG-001 — [title] (foundation, no dependencies)
2. BLG-002 — [title] (depends on BLG-001)
...

## Items

### BLG-001 — [Title]
- **Horizon**: Now
- **Status**: Ready
- **Estimate**: M
- **Problem / Value**: [why]
- **Scope**: [included / excluded]
- **Acceptance criteria**:
  - AC-01: [verifiable criterion]
  - AC-02: [verifiable criterion]
- **Dependencies**: none
- **Risks**: [identified risks]
- **Owner**: [who]

[...next items...]

## Dependency matrix
| Item | Depends on | Blocks |
|------|-----------|--------|
| BLG-001 | - | BLG-002, BLG-003 |
| BLG-002 | BLG-001 | BLG-004 |

## Global risks
- [risk 1: impact and mitigation]
- [risk 2: impact and mitigation]
```

---

## Confirmation point

After Phase 1, present the backlog to the user and ask:

> "Here is the generated backlog. Do you want me to proceed with execution, or do you want to adjust something first?"

Wait for confirmation before moving to Phase 2. If the user makes adjustments, update the backlog and re-confirm.

Exception: if the user said "go ahead", "apply everything", "no confirmation", or equivalent, move directly to Phase 2.

---

## Phase 2 — TASKER

### Mission

Execute each item of the validated backlog, in the order of the defined sequence, producing code, tests, and validation evidence.

### TASKER workflow (per item)

#### Step 1 — Readiness gate

- Verify the item is `Ready`
- Verify its dependencies are satisfied (previous items completed)
- If not ready: signal the blocker and move to the next non-blocked item

#### Step 2 — Plan the execution

- Break the item down into minimal subtasks
- Map each subtask to an acceptance criterion
- Identify the files to create/modify

#### Step 3 — Implement

- **Use `/senior-dev` for every implementation action** — all code changes, technical decisions, and trade-off evaluations MUST go through the senior-dev skill to guarantee production-grade quality, explicit trade-offs, and a rollback plan.
- Implement in small changes aligned to the subtasks
- Respect the conventions of the existing project (read the code before modifying)
- Do not go beyond the item's scope

Implementation rules:

- Every implementation change MUST be executed via `/senior-dev`
- No silent scope expansion
- No changes unrelated to the current item
- Prefer editing existing files over creating new ones

#### Step 4 — Validate

- Verify each acceptance criterion
- Run the relevant tests (build, lint, unit/integration tests)
- Capture evidence (command results, outputs)

Each criterion must be marked `pass` or `fail` with evidence.

#### Step 5 — Close or iterate

- If all criteria pass: mark the item as `Done`
- If some criteria fail: document the failures, fix if possible, otherwise mark as `Blocked` with a reason

### TASKER output (per item)

```markdown
## BLG-XXX — [Title]: [Done / Blocked / In Progress]

### Changes made
- [file:line]: [description of the change]

### Validation
| Criterion | Result | Evidence |
|---------|----------|--------|
| AC-01 | pass | [command/output/test] |
| AC-02 | pass | [command/output/test] |

### Issues encountered
- [problem and resolution, or remaining blocker]
```

### TASKER final report

After all items, produce a summary:

```markdown
## Execution report

### Summary
- Items completed: X / Y
- Items blocked: Z (with reasons)

### Completed items
- BLG-001: Done
- BLG-002: Done

### Blocked items
- BLG-003: [reason for the blocker]

### Next steps
- [concrete remaining actions]
```

---

## Global rules

### Language

- The backlog and reports are in the user's language by default
- Code and comments follow the project's conventions (usually English)
- If the user writes in English, respond in English

### Scope

- Never implement without a validated backlog (unless explicitly confirmed)
- Never go beyond the scope of the source report
- Flag any blocker or ambiguity immediately rather than guessing

### Quality

- Read the existing code before modifying
- Respect the project's patterns and conventions
- Do not add unrequested complexity
- Test what is testable

---

## Failure Modes & Recovery

| Failure | Recovery |
|---------|----------|
| Source report too vague to extract actions | Ask for clarification before generating the backlog. List what is missing. |
| Too many items generated (backlog overload) | Limit to max 10 `Now` items. Move the rest to `Next`/`Later`. |
| Circular dependency between items | Identify the cycle, propose a merge or a different split. |
| Item not Ready but the user wants to proceed | Flag the risks, propose a reduced scope that IS ready. |
| Implementation blocked by misunderstood code | Read more context (adjacent files, existing tests). Never guess the architecture. |
| Tests fail after implementation | Diagnose, fix. If a fix is impossible, mark the item Blocked and move to the next one. |
| The user changes their mind during execution | Update the backlog, re-confirm, then resume execution. |
