# Volere template — Robertson

A skeleton inspired by the **Volere Requirements Specification Template**
(Suzanne & James Robertson, *Mastering the Requirements Process*).
Process-independent: agile, traditional, outsourced.

The full official template is available at volere.org. This skeleton reuses
its main structure, adapted for use as a CdC.

---

## Project Drivers

### 1. The Purpose of the Project
- 1a. The content of the product (what is it?)
- 1b. The business value (why does it exist?)
- 1c. The measurable goals

### 2. The Stakeholders
- 2a. The client / sponsor (who pays, who decides)
- 2b. The users of the product (who uses it)
  - For each user: role name, subject-matter/expertise, interest, mental load
- 2c. Other stakeholders (compliance, ops, support, marketing...)

---

## Project Constraints

### 3. Mandated Constraints
- 3a. Imposed solutions (stack, vendor, existing integration)
- 3b. Implementation environment
- 3c. Imposed partners and collaborations
- 3d. Off-the-shelf applications to use
- 3e. Conventions and standards to comply with
- 3f. Schedule constraints (deadlines)
- 3g. Budget constraints

### 4. Naming Conventions and Definitions
- 4a. Glossary of business terms
- 4b. Acronyms
- 4c. Project naming conventions

### 5. Relevant Facts and Assumptions
- 5a. Facts important to the context
- 5b. Assumptions made by the team

---

## Functional Requirements

### 6. The Scope of the Work
- 6a. The current business context
- 6b. The context diagram (work boundaries)
- 6c. The business events (in/out flows)

### 7. Business Data Model and Data Dictionary
- 7a. Conceptual data model
- 7b. Data dictionary

### 8. The Scope of the Product
- 8a. The product context diagram (boundaries)
- 8b. The identified use cases
- 8c. The actors and their interactions

### 9. Functional Requirements
For each requirement:

```
Requirement #: 
Type: 
Use case # : 
Description: 
Rationale: 
Source: 
Fit Criterion: 
Customer Satisfaction: [1-5]
Customer Dissatisfaction: [1-5]
Priority: 
Conflicts: 
Supporting Materials: 
History: 
```

---

## Non-Functional Requirements

### 10. Look and Feel Requirements
- Appearance, style, brand

### 11. Usability and Humanity Requirements
- Ease of learning, accessibility, languages

### 12. Performance Requirements
- Speed, capacity, precision, reliability, availability

### 13. Operational and Environmental Requirements
- Physical environment, integration, maintenance

### 14. Maintainability and Support Requirements
- Extensibility, support, portability

### 15. Security Requirements
- Confidentiality, integrity, audit, immunity

### 16. Cultural Requirements
- Cultural and political aspects

### 17. Legal Requirements
- Regulatory compliance, norms, standards

---

## Project Issues

### 18. Open Issues
List of unresolved points with a deadline.

### 19. Off-the-Shelf Solutions
- Ready-to-use components available
- Reusable components from other projects
- Products to copy

### 20. New Problems
Effects of the solution on the existing environment.

### 21. Tasks
- Implementation tasks
- Migration plan
- Cutover plan

### 22. Migration to the New Product
Cutover procedures.

### 23. Risks
Risk register with probability and impact.

### 24. Costs
Cost estimate (time, resources, financial).

### 25. User Documentation and Training
Documentation and training plan.

### 26. Waiting Room
Requirements identified but deferred to later.

### 27. Ideas for Solutions
Technical leads (to be validated, not to be fixed).

---

## Usage notes

- **Volere is not a final delivery format** but a very complete
  **elicitation structure**. In practice, some sections merge
  (e.g., 4a-4c → a single glossary).
- The **Fit Criterion** (Volere's acceptance criterion) is the exact
  equivalent of the ISO 29148 verification criterion.
- The **Customer Satisfaction / Dissatisfaction** sections are a
  Volere specificity — useful in agile for prioritizing.
- In a French/contractual context, add a signatures section and a
  documentation hierarchy (cf. cdc-web-fr.md).

Source: volere.org · Suzanne & James Robertson, *Mastering the
Requirements Process*, 4th ed., 2022.
