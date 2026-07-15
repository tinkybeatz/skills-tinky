# Reference standards for SRS

This file details the applicable standards, their history, and when to use
them.

---

## IEEE 830-1998 (Superseded, still referenced)

**Title**: IEEE Recommended Practice for Software Requirements
Specifications

**Status**: Superseded by ISO/IEC/IEEE 29148 in 2011. Still heavily
referenced in industry, teaching, and contracts.

**Scope**: Focused exclusively on the SRS document — content, structure, and
quality characteristics. Does not cover elicitation or validation.

**8 defined quality characteristics**:
1. Correct
2. Unambiguous
3. Complete
4. Consistent
5. Ranked for importance and stability
6. Verifiable
7. Modifiable
8. Traceable

**IEEE 830 structure**:
1. Introduction (purpose, scope, definitions, references, overview)
2. Overall Description (product perspective, functions, user characteristics,
   constraints, assumptions)
3. Specific Requirements (external interfaces, functional, performance,
   design constraints, software system attributes)

**When to use it**: When a client or contract explicitly references IEEE 830,
or for the terminology of the quality characteristics.

---

## ISO/IEC/IEEE 29148:2018 (Current standard)

**Title**: Systems and software engineering — Life cycle processes —
Requirements engineering

**Status**: Current standard. 2018 revision (first version 2011).

**Scope**: Covers the full requirements-engineering cycle:
- Elicitation process
- Analysis process
- Specification process
- Validation process
- Quality criteria for individual requirements AND requirement sets
- Templates for SyRS, SRS, and StRS

**What it adds over IEEE 830**:
- Scope broadened beyond the SRS document
- Alignment with the system life-cycle processes
- Templates for 3 document types (not just SRS)
- Quality criteria for individual requirements

**Qualities of an individual requirement (29148)**:
- Necessary
- Appropriate (to the level of abstraction)
- Unambiguous
- Complete
- Singular (one need per statement)
- Feasible
- Verifiable
- Correct
- Conforming

**Qualities of a requirement set**:
- Complete
- Consistent
- Feasible
- Comprehensible

**When to use it**: By default for any new SRS. This is the skill's reference
template.

---

## Complementary frameworks

### EARS (Easy Approach to Requirements Syntax)

Event-driven wording patterns:

| Pattern | Template | Example |
|---------|----------|---------|
| Ubiquitous | The [system] shall [action] | The system shall log all API calls |
| Event-driven | When [event], the [system] shall [response] | When a user submits valid credentials, the system shall authenticate within 1s |
| State-driven | While [state], the [system] shall [action] | While in maintenance mode, the system shall reject new connections |
| Optional | Where [feature], the [system] shall [action] | Where geolocation is enabled, the system shall display local results |
| Unwanted | If [condition], then the [system] shall [response] | If 3 failed login attempts occur, then the system shall lock the account for 15min |
| Complex | Combination of the patterns above | While connected AND When payment submitted, the system shall process within 5s |

### Gherkin / BDD

For testable acceptance criteria:

```gherkin
Feature: User Login

  Scenario: Successful login with valid credentials
    Given the user is on the login page
    And the user has a valid account
    When the user enters correct email and password
    And clicks the "Sign In" button
    Then the user should be redirected to the dashboard
    And a session token should be created

  Scenario: Failed login with invalid password
    Given the user is on the login page
    When the user enters a valid email but incorrect password
    And clicks the "Sign In" button
    Then an error message "Invalid credentials" should be displayed
    And no session token should be created
```

### MoSCoW (Prioritization)

| Level | Meaning | Commitment |
|--------|-------------|-----------|
| **Must Have** | Essential, the system is useless without it | Delivered in the target version |
| **Should Have** | Important but not blocking | Delivered unless a major constraint arises |
| **Could Have** | Desirable, improves the experience | Delivered if the budget allows |
| **Won't Have** | Explicitly excluded from this version | Documented for future versions |

### SMART Requirements

| Criterion | Application to requirements |
|---------|---------------------------|
| **Specific** | A single need, no combination |
| **Measurable** | Quantifiable acceptance criterion |
| **Achievable** | Feasible within the project constraints |
| **Relevant** | Tied to a business objective |
| **Time-bound** | Target version or sprint identified |

### FMEA (Failure Modes and Effects Analysis)

For critical systems (Deep tier, regulated domain):

| Requirement | Failure Mode | Effect | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Mitigation |
|-------------|-------------|--------|-----------------|-------------------|-------------------|-----|-----------|
| FR-001 | Auth timeout | User blocked | 7 | 3 | 2 | 42 | Retry + local fallback |

RPN (Risk Priority Number) = Severity × Occurrence × Detection
Prioritize the mitigations by descending RPN.
