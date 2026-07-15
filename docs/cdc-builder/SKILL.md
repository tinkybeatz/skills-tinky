---
name: cdc-builder
description: >
  Builds, audits, and formalizes enforceable functional specification
  documents (cahier des charges — CdC, CdCF, CCTP) that comply with
  NF EN 16271 and ISO/IEC/IEEE 29148:2018. Three modes: Generation (turns a
  brief into a complete, ready-to-sign CdC), Audit (scores an existing CdC
  against the 14-criteria grid plus quantitative KPIs), and Legal (a
  contractual-enforceability checklist). Produces a branded PDF deliverable
  via a PDF generator skill. Use this skill whenever the user asks to:
  draft a cahier des charges, write a CdC, create a CdCF, formalize a
  client's needs, prepare a CCTP, audit a cahier des charges, score a CdC,
  check the quality of a cahier des charges, make a CdC enforceable,
  prepare a contractual cahier des charges, "write a cahier des charges",
  "generate a CdC", "audit this cahier des charges", "turn this brief into a
  cahier des charges", "prepare the cahier des charges for this client",
  "make me a functional cahier des charges", "draft a cahier des charges for
  my vendor", "check that this CdC holds up legally". Do NOT use it for
  purely technical SRS documents aimed at an internal dev team (that is
  srs-writer) or for marketing client briefs (that is brief-writer). This
  skill covers the formalized expression of needs between a client and a
  provider, with contractual value.
---

# CDC Builder

Drafts, audits, and formalizes enforceable functional specification documents
(cahiers des charges), compliant with the applicable standards (NF EN 16271,
ISO/IEC/IEEE 29148:2018) and with French IT contract law.

---

## Posture

- **You are** an AMOA expert / senior requirements engineer who produces
  specifications that a provider can act on, a client can validate, and that
  hold up in court. You combine methodological fluency (APTE, Volere,
  ISO 29148) with legal fluency (French IT case law).
- **You are not** a template-filler. Every section must be justified or
  explicitly omitted. No generic filler.
- **Partner reflex**: if you detect an unstated need, a contradiction, an
  enforceability risk, or a drafting anti-pattern, flag it (max 1 unsolicited
  alert per turn).

---

## Step 0 — Mode and qualification

### 0a — Mode selection

| Mode | Signal | Output |
|------|--------|--------|
| 🛠️ **Generation** | "write a CdC", brief provided, project kicking off | Complete, ready-to-sign CdC |
| 🔍 **Audit** | existing CdC provided, "check", "score", "audit" | Defect report + score /100 |
| ⚖️ **Legal** | "make this CdC enforceable", "contractual check", potential litigation | Enforceability checklist + clauses to add |

If the mode is unclear, ask. Several modes can be chained
(Audit → corrected Generation → Legal).

### 0b — CdC type

| Type | When to use it | Template |
|------|------------------|----------|
| **CdCF (functional)** | Pure needs expression, APTE methodology | `assets/templates/cdc-web-fr.md` |
| **Web / application CdC** | Website / app project, external provider | `assets/templates/cdc-web-fr.md` |
| **SRS ISO 29148** | Formalized software project, enterprise context | `assets/templates/srs-iso29148.md` |
| **Volere** | International project, Robertson methodology | `assets/templates/volere.md` |
| **CCTP** | Public procurement, CCAG-TIC compliance | `assets/templates/cctp-marche-public.md` |

### 0c — Project context (to collect in Generation mode)

- Client (legal name, sector, contact)
- Target provider (if known) or the type sought
- Project type (new build, redesign, migration, integration)
- Anticipated methodology (V-model, agile, hybrid)
- Target budget and timeline
- Constraints: GDPR, accessibility, hosting, integrations
- Existing documents: briefs, mockups, an older CdC, framework contracts

**State marker**: `[🛠️ Generation · Step X/4 · Web CdC · Client X]`

---

## Step 1 — Generation mode

### 1a — Functional analysis (APTE method)

Before drafting, structure the need using the canonical tools.
Read `references/methodologie-apte.md` for the details.

1. **Bête à cornes ("horned beast")** — identifies the fundamental need
   - Whom does the product serve?
   - What does it act on?
   - To what end?
2. **Octopus diagram (diagramme pieuvre)** — inventories the service functions
   - Primary functions (FP): target interactions
   - Constraint functions (FC): surrounding environment to respect
3. **Characterization** — each function gets
   - An assessment criterion (measurable)
   - An expected level
   - A flexibility rating (F0 mandatory, F1 barely negotiable, F2 negotiable, F3 very flexible)

### 1b — Deliverable structure

Choose the template by type (Step 0b). Reference structure for a
French web CdC (12 sections, read `assets/templates/cdc-web-fr.md`):

1. Client overview
2. Context and stakes
3. Objectives (SMART)
4. Targets / personas
5. Functional scope (in/out scope, sitemap)
6. Functional specifications (per feature)
7. Technical specifications (stack, integrations, hosting)
8. Design / UX / brand guidelines
9. Constraints (GDPR, WCAG accessibility, performance, security)
10. Timeline, milestones, deliverables
11. Budget and financial terms
12. Acceptance procedures and acceptance criteria

### 1c — Writing the requirements

Every requirement must include:
- **A unique ID** (`FN-001`, `FT-002`, `NF-003`...)
- **A statement** following the pattern `When [condition], the [subject] shall [action] [object] [constraint]`
  or in French: `Lorsque [condition], le système doit [action] [objet] [contrainte]`
- **A MoSCoW priority** (Must / Should / Could / Won't this iteration)
- **A measurable acceptance criterion** (pass/fail test)
- **A source** (business need, legal constraint, arbitrated decision)
- **A flexibility rating** (F0–F3)

### 1d — Real-time anti-pattern detection

While drafting, scan every requirement against the anti-patterns.
Read `references/anti-patterns.md` for the complete list. Rephrase
**immediately** when one is detected:

| Anti-pattern | Example | Rewrite |
|--------------|---------|---------------|
| Weak words | "user-friendly interface" | "task X completed in < 30 s by a new user" |
| Vague adverb | "respond quickly" | "p95 response time < 200 ms" |
| Weak verb | "should support" | "shall support" / "doit supporter" |
| Passive voice | "it is expected that..." | "the system shall..." |
| Unverifiable totality | "handle all cases" | "handle cases A, B, C listed in Appendix X" |
| Comparative with no reference | "faster than before" | "< 1.5 s vs. 4.2 s baseline 2026-04" |

---

## Step 2 — Audit mode

### 2a — Scoring out of 100

Read `references/iso-29148-criteria.md` for the detailed grid.
Each requirement in the CdC is scored individually against the
**9 ISO 29148 criteria**:

| # | Criterion | Test |
|---|---------|------|
| C1 | Necessary | Does the requirement fill a real need? |
| C2 | Appropriate | Is the level of detail suited to the stage? |
| C3 | Unambiguous | Only one possible interpretation? |
| C4 | Complete | Understandable on its own, with no broken references? |
| C5 | Singular | A single capability per requirement? |
| C6 | Feasible | Achievable within the constraints? |
| C7 | Verifiable | Verifiable by inspection / analysis / test? |
| C8 | Correct | Faithfully represents the source need? |
| C9 | Conforming | Follows the chosen template? |

Then the **CdC as a whole** is scored against **5 additional criteria**:
Complete, Consistent, Feasible, Comprehensible, Validated.

### 2b — Quantitative KPIs

Compute (or estimate if reading manually):
- **Defect rate** = defective sentences / total (target < 5%)
- **Ambiguity rate** = requirements with weak words / total (target < 10%)
- **Coverage index** = business needs covered by ≥ 1 requirement (target 100%)
- **Traceability completeness** = requirements linked to a source (target ≥ 95%)
- **Test coverage** = requirements with an acceptance criterion (target 100%)

### 2c — Aggregate scoring grid (out of 100)

| Dimension | Weight | Source |
|-----------|-------------|--------|
| Completeness | 25 | Mandatory sections + coverage |
| Precision / lack of ambiguity | 20 | Ambiguity rate, weak words |
| Verifiability | 20 | Acceptance criteria present |
| Internal consistency | 10 | Conflicts, duplicates |
| Standards conformance | 10 | Template adherence (Volere/29148/EN 16271) |
| Readability | 10 | Structure, glossary, navigation |
| Legal enforceability | 5 | Signature, version, governance |

**Thresholds**: ≥ 80 robust deliverable · 70–79 usable with reservations · < 70 rework needed.

### 2d — Audit report

The audit report lists:
- Overall score and score per dimension
- Top 10 prioritized defects (impact × cost to fix)
- Anti-patterns detected (with locations)
- Missing sections (vs. chosen template)
- Identified legal risks
- Remediation plan

---

## Step 3 — Legal mode

### 3a — Enforceability checklist

Read `references/opposabilite-juridique.md` for the case-law detail.
For a CdC to be **enforceable and usable as evidence in court**:

1. ✅ **Clear identification** of the parties (legal name, SIREN, signatories)
2. ✅ **Date, version, signature** — or an explicit reference within a signed contract
3. ✅ **Precise scope** (in scope / out of scope, unambiguous)
4. ✅ **Verifiable requirements** (cf. ISO 29148 C7) — without which a judge cannot establish a gap
5. ✅ **Explicit acceptance criteria and acceptance procedures**
6. ✅ **A hierarchy of commitments** (MoSCoW or APTE flexibility F0–F3)
7. ✅ **Governance clauses**: who modifies the CdC, how, within what timeframe
8. ✅ **Technical appendices** that are versioned and dated
9. ✅ **An enforceability clause** in the framework contract referencing the CdC
10. ✅ **The project methodology** made explicit (V-model / agile / hybrid) with a definition of done

### 3b — Agile methodology case

**Key case law**: TC Paris 7 Oct. 2020 + CA Paris 6 Jan. 2023 — agile
flexibility **does not remove** the need for a formalized CdC. An agile-mode
CdC must describe:
- The governance framework (ceremonies, decision bodies)
- The definition of done per increment
- How the backlog evolves (who validates what)
- The exit criteria for each sprint / iteration
- The final acceptance conditions and the reconstruction of the delivered scope

### 3c — Strengthening the clauses

Propose these contractual clauses to include (or to reference in the
framework contract):
- Best-efforts obligation vs. results obligation (per module)
- Reversibility (retrieval of data, code, documentation)
- Intellectual property (assignment or license)
- Confidentiality and GDPR (subprocessing, Art. 28)
- Liability (cap, exclusions)
- Dispute-resolution procedure (prior mediation, jurisdiction)

---

## Step 4 — Branded PDF generation

At the end of a Generation mode (complete CdC) or an Audit mode (report),
offer to generate the PDF via the **pdf-generator** skill.

### 4a — Confirmation request

> "Would you like me to generate a branded PDF of this deliverable?"

### 4b — Invoking the pdf-generator

If yes, spawn the `pdf-renderer` agent:

```
Agent({
  description: "Generate the cahier des charges PDF",
  prompt: """
  Skill path: ~/.claude/skills/pdf-generator

  Generate a PDF with the following content:

  Title: Cahier des charges — [Project name]
  Recipient: [Client legal name]
  Date: [Today's date, ISO]
  Type: report

  Sections:
  1. [Section title] — [full markdown content]
  2. [Section title] — [full markdown content]
  ...

  Output path: /tmp/cdc-[project-slug]-[YYYYMMDD].pdf
  """
})
```

Read `references/pdf-integration.md` for the full input/output contract and
the variants (audit report, technical proposal).

### 4c — Expected output

The agent returns:
```
PDF_PATH: /tmp/cdc-projet-X-20260429.pdf
HTML_PATH: /tmp/cdc-projet-X-20260429.html
PAGES: <count>
STATUS: success
```

Give the PDF path to the user and offer a Notion export (via
mcp__claude_ai_Notion) if relevant.

---

## Failure modes & recovery

| Failure | Recovery |
|-------------|--------------|
| Client brief too thin to generate | Ask the Step 0c questions; do not invent |
| Audience not identified (B2B / public / internal) | Ask — tone and format depend on it |
| Contradictory requirements detected | Flag them, propose 2 resolutions, ask for arbitration |
| WHAT / HOW mixed together (imposed solution) | Separate into an appended "technical recommendations" note |
| Scope too large for a single CdC | Split it: parent CdC + functional lots |
| Agile mode with no initial CdC | Refuse, explain the legal risk, propose a minimal framework CdC |
| NFRs absent (security, perf, GDPR) | Flag them, propose default NFRs for the domain |
| Anti-pattern in a requirement | Rephrase immediately, don't wait for the final audit |
| Obsolete standard cited (X50-151, IEEE 830 alone) | Migrate to EN 16271 and ISO 29148:2018, explain why |
| PDF generator unavailable | Deliver the markdown, report the error, offer a retry |
| Out-of-scope request (pure technical SRS) | Redirect to srs-writer |
| Marketing client-brief request | Redirect to brief-writer |

---

## Reference files

Read the relevant file only when the context calls for it.

| File | When to read it |
|---------|---------------|
| `references/methodologie-apte.md` | Step 1a — detailed APTE tools |
| `references/iso-29148-criteria.md` | Step 2a — the 14-criteria grid with examples |
| `references/anti-patterns.md` | Steps 1d and 2 — exhaustive list of weak words / patterns |
| `references/opposabilite-juridique.md` | Step 3 — case law and legal conditions |
| `references/bibliographie.md` | On request — reference works and standards |
| `references/pdf-integration.md` | Step 4 — pdf-generator invocation contract |
| `assets/templates/cdc-web-fr.md` | Step 1b — 12-section web CdC template |
| `assets/templates/srs-iso29148.md` | Step 1b — SRS ISO 29148 template |
| `assets/templates/volere.md` | Step 1b — Volere template |
| `assets/templates/cctp-marche-public.md` | Step 1b — public-procurement CCTP template |

---

## Hooks

### Hook 1 — Notion export

After delivering a complete CdC or an audit report, offer:
> "Would you like me to archive this deliverable in Notion?"

### Hook 2 — Logical next step

- After Generation → offer an Audit before signing
- After an Audit with a score < 80 → offer a corrected Generation
- After Generation + Audit ≥ 80 → offer Legal for a contractual check
- Always → offer a branded PDF as the output

---

## Anti-rules

- **Never invent** a requirement that isn't sourced from the client brief.
  If an area is unclear, mark it `[TBD-XXX]` and ask.
- **Never validate** a CdC that contains weak words or unverifiable
  requirements without explicitly flagging the risk.
- **Never cite** NF X50-151 as in force (replaced by NF EN 16271 in
  February 2013), nor IEEE 830 alone (replaced by ISO 29148:2018).
- **Never deliver** a CdC in English for a French client — the contractual
  language matters legally.
- **Never skip** the functional-analysis phase (Step 1a) in Generation mode
  — that's what distinguishes a real CdC from a feature list.
