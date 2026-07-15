---
name: "standard-maker"
description: >
  Create, audit, and maintain engineering standards for a software project.
  Use this skill whenever the user asks to: create a standard, write a norm,
  define code rules, establish a convention, write a review standard, or a
  standard for CI/CD, security, monitoring, documentation, or any technical
  standard. Also trigger when the user says: "we should standardize", "create
  a standard for", "define the rules for", "norm for", "convention for",
  "quality standard", "code standard", "security standard", "PR rules",
  "standard process", "audit this standard", "update this standard", "review
  this standard", or any request involving the creation, audit, or maintenance
  of an engineering standard. Do NOT use for one-off architecture decisions
  (that is architecture-conceptor) or for pure research (that is DOCUMENTOR).
---

# Standard Maker

You create engineering standards — normative documents that reduce ambiguity, improve quality, and make technical expectations explicit and testable.

A standard is not an opinion piece. It is a technical contract with verifiable rules, enforcement mechanisms, and a lifecycle.

---

## Operating modes

| Mode | Signal | What it produces |
|---|---|---|
| **Create** | "create a standard for...", "standardize..." | Complete standard with rules, enforcement, sources |
| **Audit** | "audit this standard", "review this standard" | Quality score + recommendations |
| **Update** | "update this standard", "add a rule" | Revised standard with changelog |
| **Template** | "standard template", "empty structure" | Blank standard file ready to fill in |

---

## Create mode — Full workflow

### Step 1 — Frame the problem

Before writing a single rule, clarify:

- **What problem this standard solves** — in one sentence
- **Who is affected** — which teams, which repos, which services
- **What signal triggers this need** — recurring incidents, quality defects, onboarding friction, compliance constraints
- **What the success metrics are** — how to tell whether the standard is working

If the user does not provide these, ask for them before continuing. A standard without a clear problem is a useless standard.

### Step 2 — Gather evidence

Every rule must be backed by evidence. Use the DOCUMENTOR skill if web research is needed.

**Internal sources:** incidents, PR reviews, defects, lead time, quality metrics.
**External sources:** official documentation, recognized standards (OWASP, RFC, ISO), vendor guides, studies.

Minimum evidence rules:
- At least 3 relevant sources per standard
- At least 1 primary/official source when available
- At least 2 independent sources per high-impact rule
- Every source used in a rule is cited explicitly

### Step 3 — Write the rules

Every rule uses a **normative keyword**:

| Keyword | Meaning |
|---|---|
| `MUST` | Absolute requirement |
| `MUST NOT` | Absolute prohibition |
| `SHOULD` | Strong recommendation, limited exceptions |
| `SHOULD NOT` | Discouraged practice, justification required |
| `MAY` | Optional practice |

Every rule is structured as follows:

```md
### [RULE-ID] Short name

Requirement:
- [MUST/SHOULD/MAY statement] `[SRC-XXX]`

Rationale:
- [business/technical justification]

Enforcement:
- [CI check, lint rule, review checkpoint, audit]

Exceptions:
- [when allowed, who approves, expiration]
```

**Mandatory qualities of a rule:**
- **Unambiguous** — only one possible interpretation
- **Testable** — clear pass/fail criterion
- **Enforceable** — manual and/or automated check
- **Scoped** — where it applies and where it does not

### Step 4 — Structure the standard

Consult `references/template.md` for the full template. Every standard contains:

1. Metadata (Status, Version, Owner, Approvers, Effective date)
2. Scope
3. Normative rules (with rule IDs)
4. Enforcement
5. Exceptions process
6. Metrics
7. Sources
8. Change log

### Step 5 — Deliver

Produce the complete markdown file, ready to be saved in `docs/stds/`.

**Naming convention:**
- Global standards: `docs/stds/STANDARD_NAME.md` (UPPERCASE_SNAKE_CASE)
- Domain standards: `docs/stds/<domain>/STANDARD_NAME.md`

---

## Audit mode — Quality rubric

Score an existing standard out of 100 points:

| Criterion | Points |
|---|---|
| Clarity and precision of rules | 25 |
| Testability and enforcement | 25 |
| Evidence quality and traceability | 20 |
| Adoption feasibility | 15 |
| Governance completeness | 15 |

**Thresholds:**
- >= 80: publishable
- 70-79: usable with required revisions
- < 70: not publishable, back to drafting

**Audit checklist:**
- Does every rule use a normative keyword?
- Does every rule have a defined enforcement?
- Is the exception process documented?
- Are versioning and ownership complete?
- Are sources cited and traceable?
- Are the success metrics measurable?

Produce a report with the score, strengths, weaknesses, and corrective actions.

---

## Update mode

When the user asks to modify an existing standard:

1. Read the current standard
2. Identify the requested changes
3. Assess the impact (which rules change, what effect on the existing ones)
4. Apply the changes
5. Update the changelog and increment the version:
   - **PATCH**: wording fixes with no change of meaning
   - **MINOR**: new rules or modifications to existing rules
   - **MAJOR**: scope change, rule removal, restructuring

---

## Template mode

Produce a blank standard file with the complete structure. Consult `references/template.md`.

---

## Exceptions and waivers

When the user requests an exception to a standard, the exception document must contain:

- Identifier of the rule concerned
- Business/technical justification
- Risk assessment
- Mitigation controls
- Expiration date (max 90 days by default)
- Rollback/remediation plan

Exceptions are temporary by default, renewable only with a new justification.

---

## Integration with other skills

- **DOCUMENTOR**: use for external evidence research (step 2)
- **architecture-conceptor**: if the standard involves an architecture decision, delegate the option comparison
- **postgres-expert**: if the standard concerns the database, consult it for PG best practices

---

## Failure modes and recovery

| Problem | Action |
|---|---|
| Topic too vague ("standardize the code") | Ask which aspect of the code (style, review, tests, architecture) and what concrete problem |
| No identifiable triggering signal | Ask which incidents/defects motivate this standard. No problem, no standard. |
| Rules too vague to be tested | Rephrase with an explicit pass/fail criterion. "The code must be clean" → "Functions MUST NOT exceed 50 lines" |
| Standard too strict for the project's reality | Propose a pilot on a reduced scope, adjust after measurement |
| No source for a high-impact rule | Flag the missing evidence, propose a DOCUMENTOR research, do not publish the rule without a source |
| Standard vs ADR confusion | A standard = a durable rule applicable to everyone. An ADR = a one-off decision for a context. Clarify. |

---

## References

- `references/template.md` — full template of a standard with all mandatory fields
- `references/examples.md` — annotated examples of well-written standards
- `references/normative-language.md` — guide to the normative keywords with usage examples
