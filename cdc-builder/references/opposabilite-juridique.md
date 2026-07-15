# Legal enforceability of a cahier des charges

Conditions, French case law, and standard clauses that make a CdC
**enforceable** between the parties and **usable as evidence** in the event of
a dispute.

---

## Fundamental principle

A CdC is not, in itself, a contract. It becomes legally enforceable in **two
cases**:

1. **Adversarial signature** by both parties (client + provider)
2. **An explicit reference** within the signed main contract (integration clause)

Without one or the other, the CdC can be set aside as a mere working
document. *"An IT charter is not enforceable against an employee who was not
made aware of it"* (CA Paris, a transposable principle).

> **Article 1103 of the Civil Code**: *"Contracts lawfully formed have the
> force of law for those who made them."* (formerly 1134 para. 1, applicable
> to contracts concluded before 2016 and still cited in case law).

---

## Cumulative conditions for enforceability

| # | Condition | Why | Verification |
|---|-----------|----------|--------------|
| 1 | Identification of the parties | Without identified parties, no commitment | Legal name, SIREN, authorized signatories |
| 2 | Date and version | Stability over time | Footer: `v1.2 — 2026-04-29` |
| 3 | Signature or contractual reference | Manifestation of consent | Signed pages OR an integration clause in the contract |
| 4 | Precise scope | Without scope, no gap can be established | Explicit in-scope / out-of-scope section |
| 5 | Verifiable requirements | Without measurable criteria, a judge cannot decide | Every requirement has an acceptance criterion |
| 6 | Acceptance procedures | Defines the moment of risk transfer | A dedicated acceptance section |
| 7 | Hierarchy of commitments | Allows arbitration in case of conflict | MoSCoW or APTE flexibility F0–F3 |
| 8 | Documentation governance | Who modifies the CdC, and how | An amendment or change-request procedure |
| 9 | Versioned appendices | Avoids *"we didn't have the same version"* | Dated and numbered appendices |
| 10 | Project methodology | V-model / agile / hybrid made explicit | A dedicated section if non-standard |

---

## Key French case law

### TC Paris, 8th chamber, 7 October 2020 — *OOPET v. Dual Media Communication*

**Facts**: a web/application project run agile, with no CdC, dispute over the
conformance of the deliverable.

**Holding**: *"The flexibility induced by the agile method must not lead to a
lack of rigor between the parties."* Absent a CdC, the client bears the
**burden of proof** that the deliverables are non-conforming — a proof that is
nearly impossible without a written reference.

**Practical consequence**: without a CdC, the client almost systematically
loses litigation over the quality of deliverables.

### CA Paris, 6 January 2023

**Holding**: confirms the need to set down **contractually and precisely** the
methodology, the governance, and the liability consequences, **especially for
agile projects**.

The framework contract must describe:
- The methodology (Scrum / Kanban / SAFe...)
- The decision bodies (committees, ceremonies)
- The allocation of roles (PO on the client side, Scrum Master, dev team)
- The definition of done per increment
- How the backlog is modified

### CA Versailles (repeated case law)

**Holding**: an **imprecise CdC drafted by the provider** can lead to the
rescission of the contract **at the provider's fault**, on the basis of its
heightened duty to inform and its duty to advise.

**Practical consequence**: if the provider drafts the CdC, its quality engages
the provider's liability. Imprecision = professional negligence.

### The IT provider's duty to inform

The provider is required to **inform the client objectively and completely**
about:
- The characteristics of the delivered system
- The conditions of use
- The capabilities and performance
- The technical constraints

This duty **partially reverses** when the client has precisely expressed its
needs via a CdC. That is the major legal effect of a good CdC:
**rebalancing the burden of proof**.

---

## Special case: the agile method

Agile does not remove the need for a CdC, but an agile-mode CdC **does not
have the same content** as in a V-model.

### Agile CdC — mandatory content

1. **Product vision** (business objectives, personas, measurable success)
2. **Scope of the initial backlog** (prioritized epics)
3. **Methodological framework**
   - Ceremonies and their frequency (sprint planning, daily, review, retro)
   - Tools (Jira, Linear, GitHub...)
   - Definition of done per increment
   - Definition of ready (DoR) for stories
4. **Governance**
   - Roles (PO, SM, dev team) and authorizations
   - Steering committee and its frequency
   - Arbitration procedure in case of a blocker
5. **Evolution rules**
   - Who adds / modifies / prioritizes backlog items
   - Change-request validation timeframe
   - Upper limit on scope creep (e.g., ± 20% story points)
6. **Exit criteria**
   - Acceptance per sprint and final acceptance
   - Increment acceptance conditions
   - Reversibility procedure
7. **Progress tracking**
   - Velocity, burndown, weekly indicators
   - Client reporting

### Common agile pitfalls

- *"The backlog is our CdC"* → false; the backlog evolves, whereas the CdC
  fixes the **framework** within which the backlog evolves.
- *"We'll see as we go"* → contractually explosive.
- *"No acceptance criteria because we're agile"* → the criteria are written at
  the story level, not the framework-contract level.

---

## Complementary contractual clauses

To include in the framework contract that references the CdC:

### 1. Integration clause and documentation hierarchy

> *"This contract is supplemented by the following appendices, ranked in
> decreasing order of priority in the event of a contradiction:
> Appendix 1 — Cahier des charges (ref. CdC-X-v1.2 of 2026-04-29);
> Appendix 2 — Financial terms; Appendix 3 — Quality assurance plan."*

### 2. Evolution clause

> *"Any modification of the CdC shall be the subject of a written amendment
> signed by both parties, specifying the impact on the timeline and budget."*

### 3. Acceptance clause

> *"Acceptance consists of the following phases [list]. The client's silence
> beyond [timeframe] constitutes tacit acceptance, subject to the
> enforceability of substantial defects noted later."*

### 4. Reversibility clause

> *"At the end of the contract, the provider delivers to the client:
> documented source code, dependencies, deployment procedures, access to
> third-party accounts..."*

### 5. Intellectual-property clause

> *"The client becomes the owner of the bespoke developments [...] subject to
> full payment."*

### 6. Subprocessing and GDPR (Art. 28 GDPR)

> *"The provider acts as a processor within the meaning of Article 28 of the
> GDPR. A specific agreement [DPA] supplements this contract."*

### 7. Limitation of liability

> *"The provider's liability is capped at the amount invoiced over the last 12
> months, excluding gross or intentional fault."*

### 8. Mediation and jurisdiction

> *"Before any litigation, the parties undertake to refer the matter to
> [mediator]. Failing resolution within [timeframe], the commercial court of
> [city] shall have sole jurisdiction."*

---

## Public procurement

For a public IT procurement contract, the structure is mandated:

| Document | Role |
|----------|------|
| **CCAG-TIC** | General administrative clauses (Decree of 30 March 2021) |
| **CCAP** | Contract-specific administrative clauses |
| **CCTP** | Contract-specific technical clauses (equivalent of the CdC) |
| **AE** | Deed of commitment (acte d'engagement) |

**Hierarchy**: CCAP > CCAG in the event of a contradiction.

The CCTP is the **central document** for expressing the needs. It must:
- Be drafted under the responsibility of the contracting authority
- Precisely define the services to be performed
- Allow fair competition (no imposed brand without a possible equivalent)

---

## Final enforceability checklist

Before signing, check:

- [ ] Complete identification of the parties (legal name, SIREN, signatories)
- [ ] Date, version, pagination
- [ ] Glossary and definitions of key terms
- [ ] In-scope / out-of-scope, unambiguous
- [ ] Every requirement has an ID, a priority, an acceptance criterion
- [ ] Detailed acceptance procedures (phases, duration, formalization)
- [ ] Amendment / change-request procedure
- [ ] Dated and listed appendices
- [ ] If agile: complete methodological framework (see above)
- [ ] Integration clause in the framework contract **OR** signatures on the CdC
- [ ] Confidentiality, GDPR, intellectual property addressed
- [ ] Dispute procedure (mediation + jurisdiction)

Enforceability score: ≥ 90% of boxes checked for a robust deliverable.

---

## Sources

- Article 1103 of the Civil Code (formerly 1134) — binding force of contracts
- TC Paris, 8th chamber, 7 October 2020 — *OOPET v. Dual Media Communication*
- CA Paris, 6 January 2023 — confirmation of agile case law
- CA Versailles — case law on the imprecise provider
- Decree of 30 March 2021, JORF — CCAG-TIC public procurement
- GDPR Art. 28 — processing of personal data

For any legal question not covered here, redirect to the
**conseiller-juridique** skill.
