# SRS quality validation grid

This file contains the validation checklist to apply before delivering the
SRS (Step 3 of the workflow).

---

## The 8 IEEE 830 characteristics

### 1. Correct

Each requirement reflects a real stakeholder need.

**Checklist:**
- [ ] Each requirement is traceable to a source (brief, stakeholder, constraint)
- [ ] No requirement invented or extrapolated without validation
- [ ] The NFR metrics are realistic and achievable
- [ ] The domain terminology is correct (validated by the domain)

**Test**: a stakeholder can confirm that each requirement maps to a real need.

### 2. Unambiguous

Each requirement has a single possible interpretation.

**Checklist:**
- [ ] No requirement smell detected (subjective, superlative, comparative without reference)
- [ ] Technical terms are defined in the glossary
- [ ] "The system" is always clearly identified when there are multiple components
- [ ] Boundary conditions are specified (e.g. what happens if the list is empty?)

**Test**: two developers reading the same requirement independently reach the
same understanding.

### 3. Complete

Nothing necessary is missing.

**Checklist:**
- [ ] All identified features are covered
- [ ] Both nominal cases AND error cases are specified
- [ ] The NFRs cover: performance, security, reliability, usability
- [ ] All external interfaces are documented
- [ ] The glossary covers all non-obvious terms
- [ ] Remaining TBDs are documented with a target resolution date
- [ ] Boundary conditions and edge cases are addressed

**Test**: no developer should need to "guess" an unspecified behavior.

### 4. Consistent

No internal contradiction.

**Checklist:**
- [ ] No contradictory requirements (e.g. FR-001 says "email required",
      FR-012 says "signup without email possible")
- [ ] Uniform terminology (the same concept = the same term everywhere)
- [ ] Priorities are coherent (a Must does not depend on a Won't)
- [ ] The NFRs don't contradict the functional ones (e.g. "real time"
      + "daily batch processing" for the same data)

**Test**: automated search for contradictory terms and inconsistent priority
dependencies.

### 5. Verifiable

Each requirement can be tested or demonstrated.

**Checklist:**
- [ ] Each requirement has at least one measurable acceptance criterion
- [ ] The NFRs have quantified thresholds (no "fast" or "secure")
- [ ] The verification method is identifiable (test, inspection, demo, analysis)
- [ ] The acceptance criteria are objective (no subjective judgment)

**Test**: for each requirement, a test case can be written.

### 6. Modifiable

The document accommodates changes without breaking consistency.

**Checklist:**
- [ ] Each requirement has a unique ID
- [ ] No requirement duplication (cross-references instead)
- [ ] Consistent hierarchical structure (sections/subsections)
- [ ] Revision history documented
- [ ] Format allows diff/version control (markdown > Word)

### 7. Traceable

Each requirement is linked upstream and downstream.

**Checklist:**
- [ ] Backward traceability: each requirement → its source (brief, stakeholder)
- [ ] Forward traceability: each requirement → design element and/or test case
      (at least conceptually for the Quick/Standard tiers)
- [ ] Persistent, stable IDs (no renumbering after a deletion)

### 8. Prioritized

Each requirement has an assigned importance level.

**Checklist:**
- [ ] Prioritization method chosen and documented (MoSCoW, scoring)
- [ ] Each functional requirement has a priority
- [ ] The Must Haves form a coherent, deliverable set
- [ ] Dependencies between priorities are explicit

---

## Overall quality score

| Criterion | Points | Minimum threshold |
|---------|--------|--------------|
| Correct | /15 | 12 |
| Unambiguous | /15 | 12 |
| Complete | /15 | 10 |
| Consistent | /15 | 13 |
| Verifiable | /15 | 12 |
| Modifiable | /10 | 7 |
| Traceable | /10 | 7 |
| Prioritized | /5 | 4 |
| **Total** | **/100** | **≥ 77** |

**Thresholds:**
- ≥ 85: high-quality SRS, deliverable with confidence
- 77-84: acceptable SRS with minor reservations
- 65-76: SRS needing fixes before delivery
- < 65: SRS not deliverable, major revision needed
