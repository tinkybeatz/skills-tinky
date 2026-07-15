# SRS anti-patterns

Patterns to avoid while writing. If one of these patterns is detected,
fix it right away.

---

## The 7 most common mistakes

### 1. Vague objectives

**Symptom**: The SRS doesn't clearly answer "what does this system do, and
why?"

**Consequence**: Scope creep, delays, budget overruns. 42% of projects fail
because of unclear objectives (PMI 2024).

**Fix**: Define SMART objectives in section 1.2 Scope. Every objective must
be measurable.

### 2. Excluded stakeholders

**Symptom**: The SRS is written without involving end users, ops, QA, or
security.

**Consequence**: A product that doesn't match the real needs. Projects with
strong stakeholder involvement have a 76% success rate vs. 29% with weak
involvement (Standish Group 2024).

**Fix**: Identify all stakeholders in section 2.3 and validate the SRS with a
representative from each group.

### 3. Neglected NFRs

**Symptom**: Section 4 is empty or has vague wording ("the system must be
performant").

**Consequence**: A system that breaks under load, is vulnerable, or is
unusable. 48% of IT projects stumble on performance issues tied to neglected
NFRs (Gartner 2024).

**Fix**: Every NFR has a metric and a threshold. Use the section 4 template
in `templates.md`.

### 4. Ambiguous language

**Symptom**: Requirements containing "quickly", "user-friendly",
"efficiently", "roughly", "if possible".

**Consequence**: 54% of project failures come from misinterpreting
requirements due to ambiguity (IIBA 2024).

**Fix**: Apply the requirements smell detector. Replace each vague term with
a measurable metric.

### 5. No prioritization

**Symptom**: Every requirement is "important", or none has a priority
assigned.

**Consequence**: Critical features not delivered, budget wasted on secondary
items.

**Fix**: Apply MoSCoW to each requirement. The Must Haves should form a
coherent set that can be delivered independently.

### 6. Unmaintained SRS

**Symptom**: The SRS dates from the start of the project and has never been
updated despite scope changes.

**Consequence**: A gap between the spec and reality, post-launch costs.

**Fix**: Version control (git), regular reviews, markdown or wiki format (not
a frozen PDF).

### 7. Insufficient detail

**Symptom**: One-line requirements with no acceptance criteria, no edge case,
no error condition.

**Consequence**: Massive rework. One documented case: $100K + 2 months to fix
unspecified security features.

**Fix**: Every requirement has a statement, acceptance criteria, and a source.

---

## Structural anti-patterns

### Over-design (mixing WHAT/HOW)

**Symptom**: The SRS prescribes implementation choices ("use PostgreSQL",
"implement in React", "microservices architecture").

**Why it's a problem**: The SRS must stay design-independent so that
alternative solutions can be explored.

**Exception**: Imposed constraints (existing stack, client choice) go in
section 2.5 Design Constraints, not in the requirements.

**Fix**: Reword in terms of capability, not technology.
- Bad: "Use Redis for caching"
- Good: "The system shall support a session cache with a configurable TTL"

### Gold plating

**Symptom**: Requirements added by the author that don't correspond to any
stated stakeholder need.

**Fix**: Every requirement must have a traceable source. If the source is
"best practice", flag it and prioritize it as Could Have.

### Copy-paste legacy

**Symptom**: Requirements copied from an old system without validating their
relevance in the new context.

**Fix**: Every requirement carried over from an existing system must be
re-validated with the stakeholders.

### Design by committee

**Symptom**: Requirements that reflect political compromises rather than real
needs.

**Fix**: Identify the source of each requirement. If it's a compromise,
document it and prioritize it accordingly.

### Static document

**Symptom**: An SRS in Word/PDF with no version control, emailed around,
never updated.

**Fix**: Use a versionable format (markdown + git, wiki, or a requirements
management tool).

---

## Requirements smells (linguistic signals)

If one of these patterns is detected in a requirement, it's a warning sign.
Reword it right away.

| Smell | Examples | Problem |
|-------|---------|----------|
| **Subjective** | "user-friendly", "intuitive", "modern" | Not measurable, not testable |
| **Ambiguous adverb** | "quickly", "efficiently", "easily" | Varying interpretation |
| **Superlative** | "the best", "the fastest", "optimal" | Not measurable |
| **Totality** | "all cases", "never", "always", "none" | Unverifiable in practice |
| **Pure negative** | "must not crash", "without errors" | Says what it does NOT do, not what it DOES |
| **Comparative without reference** | "better than before", "faster" | No comparison baseline |
| **Soft conditional** | "if possible", "as far as possible" | No commitment |
| **Passive without agent** | "the data will be processed" | By whom? By what? |
| **Combination** | "the system must do A and B and also C" | Multiple requirements in one |
| **Etc/etc.** | "emails, SMS, etc." | Open-ended, unverifiable list |
