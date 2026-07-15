# APTE methodology — Functional analysis

Rooted in value analysis (Lawrence D. Miles, 1947), the APTE method
(APplication aux Techniques d'Entreprise) is the canonical French methodology
for expressing a need as a set of service functions.

Compliant with **NF EN 16271** (February 2013, which replaced NF X50-151).

---

## Tool 1 — The "bête à cornes" (horned beast)

Identifies the **fundamental need** before any design work.

```
            ┌─────────────────────────────┐
            │    Whom does it serve?      │
            │    (end user)               │
            └──────────────┬──────────────┘
                           │
            ┌──────────────▼──────────────┐
            │      [THE PRODUCT]          │
            └──────────────┬──────────────┘
                           │
            ┌──────────────▼──────────────┐
            │      What does it act on?   │
            │      (the object worked on) │
            └─────────────────────────────┘

         To what end? (fundamental need)
```

**3 validation questions:**

1. *Why does this need exist?* (cause)
2. *Why might it evolve or disappear?* (risks)
3. *What would happen if this need went unmet?* (severity)

If all 3 answers converge, the need is validated. Otherwise, rephrase it.

---

## Tool 2 — The octopus diagram (diagramme pieuvre)

Inventories the **service functions** by interaction with the surrounding
environment.

### Primary functions (FP)

The product connects **two elements** of the surrounding environment.
Form: *"FP1: enable [E1] to [act on / use] [E2]"*

### Constraint functions (FC)

The product adapts to **a single element** of the surrounding environment.
Form: *"FC1: comply with [constraint]"*

### Generic examples for a web project

| Code | Function | Type |
|------|----------|------|
| FP1 | Enable a visitor to browse the product catalog | Primary |
| FP2 | Enable a logged-in customer to place an order | Primary |
| FC1 | Comply with GDPR and the ePrivacy directive | Constraint |
| FC2 | Integrate with the existing CRM via a REST API | Constraint |
| FC3 | Be WCAG 2.1 level AA accessible | Constraint |
| FC4 | Stay within a budget of < €50k | Constraint |
| FC5 | Be delivered before 30 September 2026 | Constraint |

---

## Tool 3 — Characterizing the functions

Each function must include:

| Field | Description | Example |
|-------|-------------|---------|
| **Assessment criterion** | A measurable element | Load time |
| **Level** | Target value | < 1.5 s |
| **Tolerance** | Acceptable range | ± 0.3 s |
| **Flexibility** | F0 / F1 / F2 / F3 | F0 |

### Flexibility scale

- **F0** — Mandatory, non-negotiable (regulatory, safety-critical)
- **F1** — Barely negotiable (strong client expectation)
- **F2** — Negotiable (preference with no blocking impact)
- **F3** — Very flexible (a wish, *nice to have*)

---

## Tool 4 — The FAST diagram (Function Analysis System Technique)

Breaks each service function down into **technical sub-functions** following
the "why → how" logic, left to right.

```
[Service function]  ──why←  [Sub-function A]
                            │
                            ↓ how
                            [Sub-function A.1]
                            [Sub-function A.2]
```

On the left: the purpose (the **why**).
On the right: the means (the **how**).

FAST lets you **descend from the functional to the technical** without
imposing a solution at the point of expressing the need.

---

## Complete APTE workflow

1. **Bête à cornes** → validated fundamental need
2. **Octopus diagram** → exhaustive list of the FPs and FCs
3. **Characterization** → each function made measurable
4. **FAST** (optional at this stage) → technical breakdown
5. **Prioritization** → sort by priority (MoSCoW or F0–F3 flexibility)
6. **Writing the CdCF** → final structured document

Functional analysis is done **before** writing the document.
Skipping this step produces a disordered feature list, not a CdC.

---

## Common mistakes

| Mistake | Consequence | Fix |
|--------|-------------|------------|
| Confusing FP and FC | Poor prioritization | FP = connects 2 elements; FC = adapts to 1 element |
| Non-measurable function | Ineffective in court | Add criterion + level + tolerance |
| Skipping the bête à cornes | A CdC with no through-line | Always start with the fundamental need |
| Confusing function and solution | Locks out the provider's creativity | "Enable browsing the catalog" ≠ "A WordPress site" |
| No flexibility | Everything becomes F0 → deadlocked project | Prioritize F0–F3 explicitly |

---

## Normative source

- **AFNOR NF EN 16271** (February 2013) — *Value management — Functional
  expression of the need and functional performance specification*
- Replaced NF X50-151 (1991, revised 2007). No longer cite X50-151 as a
  reference in force.
