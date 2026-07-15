# Web / application CdC template — France

Standard structure for a functional cahier des charges aimed at a web or
application project, between a client and a French IT provider.
Compliant with market practice and with NF EN 16271.

**Usage**: replace the `[placeholders]` and delete the sections that don't
apply (justifying each omission).

---

## Cover page

```
FUNCTIONAL CAHIER DES CHARGES

Project: [Project name]
Client: [Legal name, SIREN]
Target provider: [Legal name or type sought]

Version: [v1.0]
Date: [YYYY-MM-DD]
Author: [Name, role]
Status: [Draft / For review / Approved for signature]
```

---

## Table of contents

(table of contents with numbering)

---

## 1. Client overview

### 1.1 Identity
- Legal name, legal form, SIREN
- Registered-office address
- Website, main contacts

### 1.2 Activity
- Sector, business, market
- Size (headcount, revenue if relevant)
- Positioning, differentiation

### 1.3 Project contacts
- Sponsor (final decision-maker)
- Project manager on the client side
- Functional leads
- Technical leads (IT department, security officer)

---

## 2. Context and stakes

### 2.1 Current situation
- State of the existing system or process
- Identified limitations, pain points
- Current volume, usage, performance

### 2.2 Project drivers
- Why now?
- Opportunities seized, risks avoided
- Strategic dependencies (other projects, partnerships)

### 2.3 Expected benefits
- Measurable (revenue, savings, time)
- Qualitative (image, satisfaction, compliance)

---

## 3. Objectives (SMART)

Each objective must be **Specific, Measurable, Achievable, Realistic, Time-bound**.

| ID | Objective | Indicator | Target | Deadline |
|----|----------|------------|-------|----------|
| OBJ-001 | [example: Reduce order-taking time] | Average time | < 90 s | Q3 2026 |
| OBJ-002 | ... | ... | ... | ... |

---

## 4. Targets and personas

### 4.1 Business targets
- Primary segment, secondary segment
- Expected volume

### 4.2 Personas
For each primary persona:
- **Name and role** (e.g., "Marie, SME purchasing manager")
- **Usage context** (device, frequency, constraints)
- **Main objectives**
- **Current frustrations**
- **Estimated technical skills**

---

## 5. Functional scope

### 5.1 In scope
An explicit list of the modules / features covered.

### 5.2 Out of scope
An explicit list of what is **not** in the project.
This section is legally just as important as the previous one.

### 5.3 Functional sitemap
Diagram or hierarchical list of the modules and screens.

---

## 6. Functional specifications

Each feature gets a structured block:

### 6.1 [Feature name]

**ID**: `FN-001`
**Priority**: Must / Should / Could / Won't
**Persona(s) concerned**: [list]

**Statement**:
> *When [condition], the system shall [action] [object] [constraint].*

**Acceptance criteria**:
- [ ] Measurable criterion 1
- [ ] Measurable criterion 2
- [ ] Measurable criterion 3

**Use cases / scenarios**:
1. Nominal case: ...
2. Alternative cases: ...
3. Error case: ...

**Sources**: [origin of the need]
**Flexibility**: F0 / F1 / F2 / F3
**Dependencies**: [other FN-XXX]

---

## 7. Technical specifications

### 7.1 Stack and architecture
- Imposed or preferred language(s), framework(s)
- Architecture (monolith / microservices / serverless / SPA / SSR...)
- Database(s), cache, search

### 7.2 Hosting and infrastructure
- Cloud / on-premise / hybrid
- Region and compliance (GDPR, sensitive data)
- Required availability (SLA), RPO, RTO

### 7.3 Integrations
| Third-party system | Type | Direction | Frequency |
|---------------|------|-----------|-----------|
| [CRM] | REST API | Bidirectional | Real time |
| [ERP] | Webhook | Outbound | On event |

### 7.4 Security
- Authentication (SSO, MFA, OAuth, SAML...)
- Authorizations (RBAC, ABAC)
- Encryption (at rest, in transit)
- Audit logging
- Compliance (ISO 27001, SOC 2, ANSSI...)

### 7.5 Performance
| Indicator | Target | Measurement |
|------------|-------|--------|
| p95 response time | < 200 ms | Critical API endpoints |
| Time to Interactive | < 2 s | Simulated 4G connection |
| Peak load sustained | 500 req/s | 10 minutes sustained |

---

## 8. Design and UX

### 8.1 Brand guidelines
- Existing (reference document) or to be created
- Colors, typography, iconography

### 8.2 Mockups
- Existing (Figma, Adobe XD...) or to be produced
- Expected level (wireframes / mockups / prototypes)

### 8.3 Ergonomics
- Standards to comply with (Material, HIG, custom)
- Main navigation, key journeys

### 8.4 Accessibility
- Target WCAG 2.1 level (A, **AA**, AAA)
- RGAA if public sector
- Tests to plan for (audit, validation by users with disabilities)

---

## 9. Constraints

### 9.1 Regulatory
- GDPR (register, DPA, consents, rights)
- ePrivacy (cookies, consent)
- Sector-specific (finance, health, public)

### 9.2 Technical
- Browser compatibility (matrix)
- Mobile compatibility (iOS/Android, minimum OS)
- Limits of the existing infrastructure

### 9.3 Budgetary
- Overall budget envelope
- Payment terms (fixed price, time-and-materials, hybrid)

### 9.4 Schedule
- Target go-live date
- Non-negotiable intermediate milestones

---

## 10. Timeline and deliverables

### 10.1 Project phases
| Phase | Duration | Deliverables | Validation |
|-------|-------|-----------|------------|
| Framing | 2 wks | Framing note, initial backlog | Sponsor |
| Design | 4 wks | Mockups, technical architecture | Steering committee |
| Development | 12 wks | 2-week iterations | PO + acceptance |
| Acceptance | 4 wks | Acceptance report | Sponsor |
| Go-live | 1 wk | Cutover, monitoring | IT department |
| Warranty | 12 wks | Fixes, documentation | Client |

### 10.2 Expected deliverables
- Documented source code (Git repository, access)
- User documentation
- Technical documentation (architecture, API, deployment)
- Level-1 support procedures
- User training (if relevant)
- Reversibility plan

---

## 11. Budget and financial terms

### 11.1 Budget breakdown
| Item | Amount (excl. tax) | Notes |
|-------|------------|-------|
| Design | [€] | Fixed price |
| Development | [€] | T&M or fixed price |
| Acceptance and go-live | [€] | Fixed price |
| Warranty | [€] | Included / optional |
| **Total** | [€] | |

### 11.2 Terms
- Down payment / milestone-based / monthly invoicing
- Late penalties
- Performance bonus (if relevant)

---

## 12. Acceptance procedures

### 12.1 Acceptance procedure
- Phases (technical, functional, UAT acceptance)
- Maximum duration
- Defect-reporting procedure
- Defect classification (blocking / major / minor)
- Correction deadline per class

### 12.2 Overall acceptance criteria
The product is considered accepted if:
- 100% of Must requirements are validated
- 90% of Should requirements are validated
- No blocking defect remaining
- Complete documentation delivered
- Training completed (if planned)

### 12.3 Tacit acceptance
Absent any feedback within [timeframe] after delivery, acceptance is
deemed granted, subject to substantial defects noted later.

---

## Appendices

### A.1 Glossary
Definition of key terms and acronyms.

### A.2 Normative references
- NF EN 16271 (2013)
- ISO/IEC/IEEE 29148:2018
- WCAG 2.1
- GDPR
- [Other applicable standards]

### A.3 Supporting documents
- Mockups (link to a versioned Figma)
- Target architecture (diagrams)
- Data model (ERD)
- API mock / OpenAPI contract

### A.4 Traceability matrix
| Business need | Requirement | Associated test |
|---------------|----------|--------------|
| BES-001 | FN-001, FN-005 | TC-012 |

---

## Signatures

| Role | Name | Signature | Date |
|------|-----|-----------|------|
| Client | | | |
| Provider | | | |

> *This cahier des charges constitutes the technical appendix to the contract
> signed between the parties. In the event of a contradiction with other
> contractual documents, the order of priority is defined in the framework
> contract.*
