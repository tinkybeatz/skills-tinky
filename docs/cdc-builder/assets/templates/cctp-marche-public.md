# CCTP template — Public procurement

Contract-specific technical clauses (Cahier des Clauses Techniques
Particulières) for a public IT procurement contract, compliant with the
CCAG-TIC (Decree of 30 March 2021) and the French Public Procurement Code.

⚠️ For a public contract, the CCTP is **drafted under the responsibility of
the contracting authority** and must allow **fair competition**.
No imposed brand or reference without a "or equivalent" mention.

---

## Cover page

```
CONTRACT-SPECIFIC TECHNICAL CLAUSES
[type] contract — [contract title]

Contracting authority: [Local authority / public body]
Contract number: [reference]
Procedure: [call for tenders / MAPA / framework agreement]
Date: [YYYY-MM-DD]
Version: [v1.0]
```

---

## Article 1 — Purpose of the contract

### 1.1 Contract designation
[Description in one sentence]

### 1.2 Contract form
- Simple contract / framework agreement
- Firm and conditional tranches (where applicable)
- Purchase orders (where applicable)

### 1.3 Breakdown into lots
| Lot | Designation | Allotment |
|-----|-------------|-----------|
| 1 | [...] | Yes / No |

---

## Article 2 — Contract documents

Hierarchy in the event of a contradiction (highest priority to lowest):

1. Deed of commitment (AE)
2. This CCTP
3. Contract-specific administrative clauses (CCAP)
4. Unit price schedule (BPU)
5. Applicable general administrative clauses (CCAG-TIC)

---

## Article 3 — Definitions and acronyms

Complete glossary.

---

## Article 4 — Functional description of the service

### 4.1 Context
- Existing systems and history
- Current volume
- Users (typology, number)
- Existing integrations

### 4.2 Objectives
SMART objectives of the contract.

### 4.3 Expected functional scope
List of expected features, ranked by priority.

### 4.4 Use cases
Description of the main usage scenarios.

---

## Article 5 — Technical specifications

### 5.1 Target architecture
- Expected architecture type (web, mobile, desktop, hybrid)
- Hosting (cloud / on-premise / shared)
- Data location (EU mandatory for personal data)

### 5.2 Technology stack
**Without imposing a brand**, express the needs in terms of:
- Compatibility (browsers, OS, versions)
- Standards to comply with (RGAA, RGS, RGI)
- Interoperability (open formats, APIs)

### 5.3 Security
- RGS (French general security framework) compliance, level [level]
- Authentication (FranceConnect where applicable)
- Encryption (at rest, in transit)
- HDS hosting if health data
- SecNumCloud if sensitive data

### 5.4 Accessibility
- RGAA compliance level [AA] mandatory
- Accessibility audit to be provided
- Multi-year plan (public-sector case)

### 5.5 Interoperability
- RGI (French general interoperability framework) compliance
- Exchange formats (XML, JSON, CSV...)
- APIs (REST, open, OpenAPI-documented)

### 5.6 Performance
| Indicator | Required level |
|------------|---------------|
| Availability | [99.9%] business hours |
| Response time | < [threshold] ms p95 |
| Capacity | [N] concurrent users |

---

## Article 6 — Expected services

### 6.1 Main services
- Design, development, commissioning
- Training (users, administrators)
- Documentation (technical, user)
- Migration of existing data

### 6.2 Complementary services
- Third-party application maintenance (TMA)
- Hosting (where applicable)
- User support

### 6.3 Expected deliverables
| Phase | Deliverable | Format | Deadline |
|-------|-------------|--------|----------|
| Design | Design dossier | PDF + sources | T0 + 4 wks |
| Development | Source code | Git + tag | T0 + 12 wks |
| Acceptance | Acceptance report | PDF | At acceptance |
| Go-live | Cutover procedures | PDF | At go-live |
| Warranty | Monthly reports | PDF | Monthly |

---

## Article 7 — Phasing and deadlines

### 7.1 Provisional schedule
- T0: contract notification
- T0 + [N] weeks: [milestone]
- ...

### 7.2 Performance deadlines
- Overall performance deadline
- Late penalties (cf. CCAP)

### 7.3 Modification procedure
Amendment procedure for scope evolution.

---

## Article 8 — Acceptance procedures

### 8.1 Fitness verification (VA)
Documentation-conformance and installation tests.

### 8.2 Regular-service verification (VSR)
Observation period under real conditions.

### 8.3 Acceptance report
Adversarial confirmation of conformance.

### 8.4 Warranty
- Minimum duration: [12 months]
- Scope: defect correction, operational-condition maintenance

---

## Article 9 — Bid evaluation criteria

(to be coordinated with the consultation rules)

| Criterion | Weight | Sub-criteria |
|---------|--------|--------------|
| Technical value | 60% | Methodology, team, references |
| Price | 30% | DQE / BPU |
| Deadlines | 10% | Proposed schedule |

---

## Article 10 — The holder's particular obligations

### 10.1 Confidentiality
All data and documents are confidential (cf. CCAG-TIC).

### 10.2 Personal-data protection
The holder acts as a **processor** within the meaning of Article 28
of the GDPR. A specific agreement (DPA) supplements the contract.

### 10.3 Intellectual property
- Assignment of economic rights to the bespoke developments
- Usage license for the integrated standard components
- Source code and documentation delivered to the contracting authority

### 10.4 Reversibility
- Mandatory reversibility procedure at the end of the contract
- Transfer period: [N] months
- Data format: open standards

### 10.5 Subcontracting
Compliance with the subcontracting declaration in the AE.

---

## Article 11 — Appendices

### A.1 Target architecture (diagram)
### A.2 Existing data model (where applicable)
### A.3 List of integrations
### A.4 Applicable frameworks (RGS, RGAA, RGI)
### A.5 List of personal data processed (GDPR register)

---

## Usage notes

- The CCTP is **public** (viewable by any candidate) → do not put sensitive
  information in it.
- Any non-measurable requirement is a risk of post-award litigation
  → apply the ISO 29148 grid even in public procurement.
- If the contracting authority lacks the technical expertise, the drafting can
  be entrusted to an external AMOA — but the responsibility remains that of
  the contracting authority.

**Sources**:
- French Public Procurement Code
- Decree of 30 March 2021 — CCAG-TIC
- DAJ Bercy — public procurement guides
