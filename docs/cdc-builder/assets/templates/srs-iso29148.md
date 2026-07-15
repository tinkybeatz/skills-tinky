# SRS template — ISO/IEC/IEEE 29148:2018

A structure compliant with the international standard for a Software
Requirements Specification. Suited when the project is highly technical,
multi-team, or aimed at an enterprise/regulated context.

---

## Cover page

```
SOFTWARE REQUIREMENTS SPECIFICATION

System: [System name]
Version: [v1.0]
Date: [YYYY-MM-DD]
Author(s): [Names]
Status: [Draft / Review / Approved]
Conformance: ISO/IEC/IEEE 29148:2018
```

---

## 1. Introduction

### 1.1 Purpose
Describe the purpose of the SRS, the intended audience, and the document's scope.

### 1.2 Scope
- System name, abbreviations
- What the system does / does not do
- Benefits and objectives

### 1.3 Definitions, Acronyms, Abbreviations
Complete glossary.

### 1.4 References
- Upstream documents (BRS, StRS, contract, ADR)
- Standards (GDPR, ISO 27001, OWASP...)
- Technical documents (architecture, data model)

### 1.5 Conventions and Document Overview
- Pattern used (EARS, Gherkin, shall statements)
- Requirement numbering convention
- Document outline

---

## 2. Overall Description

### 2.1 Product Perspective
- Is the product standalone, a subsystem, a replacement?
- Context diagram (external entities interacting with the system)

### 2.2 Product Functions
High-level functional breakdown (epics, modules).

### 2.3 User Classes and Characteristics
| User class | Frequency | Technical level | Privileges |
|------------|-----------|-----------------|------------|
| Admin | Daily | Expert | Full |
| End user | Daily | Beginner | Limited |
| API consumer | Continuous | Expert | Scoped |

### 2.4 Operating Environment
- Platforms (web, mobile, desktop)
- OS, browsers, minimum versions
- Cloud/on-prem infrastructure

### 2.5 Design and Implementation Constraints
- Imposed stack
- Code standards
- Supported languages
- License constraints

### 2.6 Assumptions and Dependencies
- External dependencies (third-party APIs, critical libraries)
- Assumptions made during drafting

---

## 3. Specific Requirements

### 3.1 External Interface Requirements

#### 3.1.1 User Interfaces
Mockups, ergonomics constraints, accessibility conformance.

#### 3.1.2 Hardware Interfaces
If applicable (sensors, printers, IoT).

#### 3.1.3 Software Interfaces
External APIs, databases, consumed services.
For each interface: protocol, format, frequency, error handling.

#### 3.1.4 Communications Interfaces
HTTP, WebSocket, gRPC, MQ... with the associated security.

### 3.2 Functional Requirements

For each requirement:

```
FR-001: [Title]
Statement: [EARS pattern or shall statement]
Priority: [Must / Should / Could / Won't]
Source: [Stakeholder / business need]
Rationale: [Why this requirement exists]
Acceptance criteria:
  - Given [precondition], when [action], then [outcome]
Dependencies: [FR-XXX, NFR-XXX]
Verification method: [Test / Inspection / Analysis / Demonstration]
```

### 3.3 Non-Functional Requirements

#### 3.3.1 Performance
Response time, throughput, capacity, scalability.

#### 3.3.2 Security
Authentication, authorization, encryption, audit, compliance.

#### 3.3.3 Reliability and Availability
SLA, MTBF, MTTR, RPO, RTO.

#### 3.3.4 Maintainability
Code standards, test coverage, modularity.

#### 3.3.5 Portability
Target platforms, containerization.

#### 3.3.6 Usability
Accessibility conformance, internationalization, ergonomics.

#### 3.3.7 Data Requirements
Volume, retention, archiving, GDPR compliance.

### 3.4 Other Requirements

#### 3.4.1 Legal and Regulatory
GDPR, ePrivacy, sector-specific, intellectual property.

#### 3.4.2 Internationalization
Languages, time zones, local formats.

---

## 4. Verification

### 4.1 Verification Methods
| Method | When to use |
|--------|-------------|
| Inspection | Documentation, code review |
| Analysis | Models, calculations, simulation |
| Demonstration | Functional demo |
| Test | Executable test cases |

### 4.2 Traceability Matrix
| Source | Requirement | Verification | Test ID |
|--------|-------------|--------------|---------|
| BRS-1 | FR-001 | Test | TC-001 |

---

## 5. Quality Assessment (ISO 29148 § 5.2)

Before approval, verify that each individual requirement satisfies
the **9 characteristics C1–C9**:

| C# | Characteristic | Pass/Fail |
|----|---------------|-----------|
| C1 | Necessary | |
| C2 | Appropriate | |
| C3 | Unambiguous | |
| C4 | Complete | |
| C5 | Singular | |
| C6 | Feasible | |
| C7 | Verifiable | |
| C8 | Correct | |
| C9 | Conforming | |

And that the set satisfies the **5 characteristics S1–S5**:

| S# | Characteristic | Pass/Fail |
|----|---------------|-----------|
| S1 | Complete (set) | |
| S2 | Consistent | |
| S3 | Feasible (set) | |
| S4 | Comprehensible | |
| S5 | Able to be validated | |

---

## Appendices

### A. Glossary
### B. Diagrams (context, use case, sequence, ERD)
### C. Risk register
### D. Change log
### E. Approval signatures
