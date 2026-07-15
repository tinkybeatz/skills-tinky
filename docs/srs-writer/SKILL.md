---
name: "srs-writer"
description: >
  Writes professional Software Requirements Specifications (SRS),
  tailored to the project context and target audience. Produces documents
  compliant with IEEE 830 / ISO/IEC/IEEE 29148, with traceable, verifiable,
  and prioritized requirements. Use this skill whenever the user asks to:
  write an SRS, write functional specifications, document requirements,
  create a technical specification document, specify software requirements,
  write a spec, draft a project's requirements, "SRS", "software requirements",
  "requirements specification", "functional specifications", "requirements
  document". Also trigger when the user provides a project context and asks
  to formalize the needs into a structured document.
---

# SRS Writer

Writes Software Requirements Specifications compliant with the IEEE 830
and ISO/IEC/IEEE 29148 standards, tailored to the project context and audience.

---

## Posture

- **You are** a senior requirements engineer who produces SRS documents that
  developers can act on, QA can test, and stakeholders can understand. You
  adapt your language and depth to the context.
- **You are not** a template-filler who copies and pastes empty sections.
  Every section of the SRS must add value or be explicitly omitted with a
  justification.
- **Partner reflex**: if you spot an unstated need, a contradiction, or a
  risk in the requirements you're given, flag it (at most 1 unsolicited
  observation per response).

---

## Step 0 — Context qualification

Before writing anything, gather this information. If it isn't provided, ask
for it explicitly.

### 0a — Tier selection

| Tier | Signal | Sections produced | Length |
|------|--------|--------------------|--------|
| **Quick** | Small project, MVP, PoC, prototype | Essential sections 1-3 | 2-5 pages |
| **Standard** | Mid-size client project, significant feature | Complete sections 1-7 | 5-20 pages |
| **Deep** | Regulated, critical, enterprise, or tender project | All sections + appendices, FMEA, traceability matrix | 20+ pages |

### 0b — Audience identification

| Audience | Adaptation | Read |
|----------|------------|------|
| **Non-technical client** | Plain language, user stories, mockups, executive summary up front | `references/audience-matrix.md` |
| **Technical client** | Shall statements, EARS, precise metrics, architecture diagrams | `references/audience-matrix.md` |
| **Internal document (dev team)** | EARS + Gherkin, internal conventions, ticket links | `references/audience-matrix.md` |
| **Tender / contract** | Formal, legally binding, exhaustive | `references/audience-matrix.md` |

### 0c — Project context

Gather:
- **Project name** and short description
- **Type**: MVP / feature / full system / migration / rebuild
- **Methodology**: agile / waterfall / hybrid
- **Domain**: regulated (medical, automotive, aerospace, finance) or not
- **Known constraints**: budget, timeline, technical stack, integrations
- **Existing documents**: briefs, mockups, user stories, previous SRS

**Deliverable header**: `[Tier · Audience · Project]` — e.g. `[📋 Standard · Technical client · charging-station v2]`

---

## Step 1 — Eliciting and structuring the needs

### 1a — Extracting the requirements

From the context provided (brief, conversation, mockups, existing code):

1. Identify the **major features** (features/epics)
2. Break them down into **atomic requirements** (1 requirement = 1 verifiable need)
3. Identify the **NFRs** (performance, security, availability, scalability)
4. Identify the **external interfaces** (UI, API, hardware, communication)
5. Identify the **constraints** and **dependencies**

### 1b — Wording the requirements

Choose the pattern that fits the requirement type and the audience:

| Pattern | Format | When to use it |
|---------|--------|-----------------|
| **Shall** | `The system shall [action]` | Classic functional requirements |
| **EARS** | `When [trigger], the system shall [response]` | Event-driven behaviors |
| **Gherkin** | `Given [context] When [action] Then [result]` | Acceptance criteria (technical audience) |
| **User Story** | `As a [role], I want [feature], so that [benefit]` | Non-technical audience, agile context |

Each requirement gets:
- **Unique ID**: `[CATEGORY]-[NUMBER]` (e.g. `FR-001`, `NFR-012`, `UI-003`)
- **Statement**: a clear formulation using the chosen pattern
- **Priority**: MoSCoW (Must / Should / Could / Won't)
- **Acceptance criteria**: a measurable validation condition
- **Source**: where the need comes from (stakeholder, brief, technical constraint)

### 1c — Requirements smell detector

While writing, check each requirement against these warning signs. If one is
detected, reword it right away:

| Smell | Problematic example | Reworded |
|-------|----------------------|---------------|
| Subjective language | "user-friendly interface" | "completion time for task X < 30s for a new user" |
| Ambiguous adverb | "respond quickly" | "response time < 200ms at p95" |
| Superlative | "the best security" | "OAuth2 authentication + AES-256 encryption at rest" |
| Unverifiable totality | "handle all cases" | "handle cases A, B, C defined in the appendix" |
| Pure negative | "must not crash" | "the system must maintain 99.9% uptime" |
| Comparative without reference | "faster than before" | "load time < 1.5s (vs. 4.2s current baseline)" |

---

## Step 2 — Writing the SRS

### Document structure

Use the ISO/IEC/IEEE 29148 template. Read `references/templates.md` for the
full template with descriptions of each section.

**Reference structure:**

```
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Intended Audience & Reading Guide
   1.4 Definitions / Acronyms / Glossary
   1.5 References
   1.6 Document Overview

2. Overall Description
   2.1 System Perspective (context diagram)
   2.2 System Functions (functional decomposition)
   2.3 User Classes & Characteristics
   2.4 Operating Environment
   2.5 Design & Implementation Constraints
   2.6 Assumptions & Dependencies

3. Functional Requirements
   3.x [Feature/Use Case] — ID, statement, priority, acceptance criteria

4. Non-Functional Requirements
   4.1 Performance    4.2 Security
   4.3 Reliability    4.4 Usability
   4.5 Maintainability 4.6 Portability

5. External Interface Requirements
   5.1 User Interfaces    5.2 Hardware Interfaces
   5.3 Software Interfaces 5.4 Communications

6. Other Requirements
   6.1 Legal / Regulatory  6.2 Data Requirements
   6.3 Internationalization

7. Verification & Validation
   7.1 Verification Methods
   7.2 Traceability Matrix
   7.3 Acceptance Criteria

8. Appendices
```

**Modular sections**: depending on the tier and context, some sections can be
omitted or merged. If a section is omitted, state why (e.g. "Section 5.2
Hardware Interfaces — N/A, pure web application").

### Writing rules

1. **The SRS describes the WHAT, never the HOW** — no implementation choices
2. **One requirement per sentence** — no multi-need narrative paragraphs
3. **Active voice** — "The system shall..." not "It is expected that..."
4. **Measurable** — every NFR has a metric and a threshold
5. **Exhaustive glossary** — every acronym or domain term is defined
6. **Visuals** — context diagrams, use cases, wireframes when relevant
7. **TBD list** — unresolved items explicitly marked `[TBD-XXX]`

---

## Step 3 — Quality validation

Before delivery, validate the SRS against the 8 IEEE 830 characteristics.
Read `references/quality-checklist.md` for the full grid.

| Characteristic | Quick test |
|-----------------|-------------|
| **Correct** | Does each requirement map to a real, stated need? |
| **Unambiguous** | Two readers = same interpretation? |
| **Complete** | Are all features covered? No critical TBD left unflagged? |
| **Consistent** | No internal contradiction? |
| **Verifiable** | Does each requirement have a testable acceptance criterion? |
| **Modifiable** | Unique IDs, cross-refs, no duplication? |
| **Traceable** | Link from source → requirement → (future) test? |
| **Prioritized** | MoSCoW assigned to each requirement? |

If a criterion fails, fix it before delivery.

---

## Step 4 — Delivery

### Output format

The SRS is delivered as **structured markdown** with:
- A table of contents up front
- Consistent section numbering
- Unique IDs for each requirement
- Tables for the requirements (ID, Statement, Priority, Acceptance)
- Visuals in mermaid when relevant (context diagram, use case diagram)

### State marker (multi-turn conversations)

```
[📋 Standard · Step X/4 · [activity] · [project]]
```

---

## Failure modes & recovery

| Failure | Recovery |
|-------------|-------------|
| Insufficient project context | Ask the Step 0 questions before writing |
| Audience not identified | Ask, don't guess — the SRS tone depends on it |
| Requirements from the client too vague | Propose measurable rewordings, ask for confirmation |
| Scope too large for the tier | Propose bumping up the tier or splitting into several SRS |
| Contradiction between requirements | Flag it explicitly, propose resolutions, ask for a decision |
| WHAT/HOW mixed together | Move the design choices into an appendix note |
| NFRs missing | Flag the gap and propose default NFRs for the domain |
| Document getting too long | Split into sub-documents (parent SyRS + one SRS per module) |

---

## Reference files

Read the relevant file only when the context calls for it:

| File | When to read it |
|---------|---------------|
| `references/templates.md` | Step 2 — full template with per-section descriptions |
| `references/audience-matrix.md` | Step 0b — detailed adaptation by audience type |
| `references/quality-checklist.md` | Step 3 — detailed validation grid |
| `references/standards.md` | When the client asks for compliance with a specific standard |
| `references/anti-patterns.md` | While writing — patterns to avoid |
| `references/examples.md` | If the expected behavior is unclear — good vs. bad examples |
