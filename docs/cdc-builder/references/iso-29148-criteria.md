# ISO/IEC/IEEE 29148:2018 — Quality grid

The international standard that supersedes IEEE 830-1998. It defines the
quality of an **individual requirement** (9 criteria) and of a **set of
requirements** (5 criteria).

---

## Part 1 — Characteristics of an individual requirement (C1–C9)

### C1 — Necessary

The requirement fills a real need whose absence would create harm or a
functional gap. An unnecessary requirement pollutes the CdC and costs effort
to validate/test.

**Quick test**: *"If I remove this requirement, what stops working?"*
If the answer is nothing, remove it.

❌ "The system shall use pleasant colors."
✅ "The system shall follow the brand guidelines [Appendix X]."

### C2 — Appropriate

The level of detail suits the stage and the type of document.
Too detailed → pre-design. Too vague → not testable.

❌ In a client CdC: "The system shall use a bcrypt hashing function with a
   cost factor of 12."
✅ "Passwords shall be stored with a recognized, state-of-the-art hashing
   algorithm (≥ the level recommended by ANSSI)."

### C3 — Unambiguous

One and only one possible interpretation. Test: two readers reading
independently must reach the same understanding.

❌ "The system shall be fast."
✅ "The p95 response time shall be < 200 ms for the endpoints listed in
   [Appendix Y], measured over 1000 consecutive requests."

### C4 — Complete

The requirement is understandable on its own. No broken reference, no
hidden condition, no implicit TBD.

❌ "See Jean's document."
✅ An explicit reference + version + accessibility of the cited document.

### C5 — Singular

One and only one capability, characteristic, constraint, or quality factor
per requirement. No "and" that bundles two needs together.

❌ "The system shall send an email **and** an SMS confirmation."
✅ "FN-001: The system shall send an email confirmation to..."
   "FN-002: The system shall send an SMS confirmation to..."

### C6 — Feasible

Achievable within the known constraints (technology, cost, timeline).
An infeasible requirement is a contractual time bomb.

❌ "The system shall work offline while synchronizing in real time."
   (internal contradiction)
✅ "The system shall retain data locally during offline periods, and
   synchronize it at the next detected connection."

### C7 — Verifiable

Verifiable by inspection, analysis, demonstration, or test. Without a
measurable verification criterion, no legal enforceability is possible.

❌ "The system shall be easy to use."
✅ "A new user shall complete the task [create an account] in < 60 s during
   a user test with 10 subjects, without assistance."

### C8 — Correct

Faithfully represents the source need. Test: does the author of the need
recognize their need in the wording?

### C9 — Conforming

Follows the project's template, glossary, and notation conventions.
A single non-conforming requirement breaks the readability of the whole.

---

## Part 2 — Characteristics of the set (set of requirements)

### S1 — Complete

The set covers all identified needs. No critical use case is left without an
associated requirement.

**Test**: for each persona × priority use case in the matrix, is there at
least one requirement?

### S2 — Consistent

No internal contradiction. No requirements that implicitly contradict each
other (e.g., 99.99% SLA + a single server with no redundancy).

### S3 — Feasible

The set is achievable within the global constraints (budget, timeline,
resources). A set made of individually feasible requirements may be globally
infeasible.

### S4 — Comprehensible

A domain reader can read the CdC in its order and understand the logic.
Glossary, table of contents, consistent navigation.

### S5 — Able to be validated

All requirements can be validated as a whole: the project's final acceptance
is conceivable.

---

## Mapping to IEEE 830-1998 (legacy)

For comparison with older CdCs:

| IEEE 830 (8 criteria) | ISO 29148 |
|-----------------------|-----------|
| Correct | C8 (individual) |
| Unambiguous | C3 |
| Complete | C4 + S1 |
| Consistent | S2 |
| Ranked for importance/stability | (MoSCoW prioritization, external) |
| Verifiable | C7 |
| Modifiable | (documentation management, external) |
| Traceable | (traceability matrix, external) |

ISO 29148 is more granular (it separates individual/set) and makes explicit
the *necessary*, *appropriate*, *singular*, *feasible*, *conforming*
characteristics that were implicit in IEEE 830.

---

## Application in Audit mode

For each requirement in the CdC being audited:
1. Assess C1–C9 (binary pass/fail or a 0–3 score)
2. Compute the average score per requirement
3. List the requirements that fail on ≥ 2 criteria

For the set:
1. Assess S1–S5
2. Identify the missing sections
3. Detect contradictions between requirements

**Robustness threshold**: fewer than 5% of requirements failing on 2+
criteria, and S1–S5 all ≥ 2/3.

---

## Sources

- **ISO/IEC/IEEE 29148:2018** — *Systems and software engineering — Life
  cycle processes — Requirements engineering*
- IEEE 830-1998 (legacy, superseded in 2011)
