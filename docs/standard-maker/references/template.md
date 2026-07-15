# Standard template

Copy this template to create a new standard. Fill in every section.

---

```md
# Standard: [TITLE]

- Status: Draft
- Version: 0.1.0
- Owner: [Team or person responsible]
- Approvers: [Who approves the standard]
- Effective date: [Date it takes effect]
- Last review date: [Date of the last review]

## Scope

[Where this standard applies: repos, services, teams, domains]

[What is explicitly out of scope]

## Normative rules

### [R-XXX-01] [Short rule name]

Requirement:
- [Statement with MUST/SHOULD/MAY] `[SRC-XXX]`

Rationale:
- [Why this rule exists — business or technical justification]

Enforcement:
- [How this rule is checked: CI check, lint, review checklist, audit]

Exceptions:
- [When an exception is allowed, who approves it, max duration]

---

### [R-XXX-02] [Short name]

Requirement:
- [Statement] `[SRC-XXX]`

Rationale:
- [Justification]

Enforcement:
- [Mechanism]

Exceptions:
- [Conditions]

---

## Enforcement summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-XXX-01 | [CI check / lint / review / audit] | [Yes/No] |
| R-XXX-02 | [CI check / lint / review / audit] | [Yes/No] |

## Exceptions process

- Exceptions are temporary (max 90 days by default)
- An exception MUST include:
  - the rule identifier
  - business/technical justification
  - risk assessment
  - mitigation controls
  - expiration date
  - remediation plan
- Exceptions are renewable only with a new justification
- Exceptions are recorded in [registry location]

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| [Metric 1] | [Current value] | [Target] | [How to measure] |
| [Metric 2] | [Current value] | [Target] | [How to measure] |

## Sources

- SRC-001 | [Title] | [URL or internal path] | [Publisher] | [Date] | [Why it is relevant]
- SRC-002 | [Title] | [URL or internal path] | [Publisher] | [Date] | [Why it is relevant]
- SRC-003 | [Title] | [URL or internal path] | [Publisher] | [Date] | [Why it is relevant]

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 0.1.0 | [Date] | [Author] | Initial draft |
```

---

## Naming conventions

**Files:**
- Global standards: `docs/stds/STANDARD_NAME.md` (UPPERCASE_SNAKE_CASE)
- Domain standards: `docs/stds/<domain>/STANDARD_NAME.md`
- Versioning lives in the file, not in the file name

**Rule IDs:**
- Format: `R-<DOMAIN>-<NN>` (e.g. `R-SEC-01`, `R-CODE-03`, `R-OPS-07`)
- Common domains: `CODE`, `SEC`, `OPS`, `CI`, `DOC`, `API`, `DB`, `REVIEW`
- IDs are stable — never reuse a deleted ID

**Source IDs:**
- Format: `SRC-<NNN>` (e.g. `SRC-001`, `SRC-042`)
- Incremental sequence per standard
- Each source is cited inline in the rule that uses it: `[SRC-001]`

**Versioning:**
- `MAJOR.MINOR.PATCH`
- PATCH: wording fix with no change of meaning
- MINOR: new rule or modification of an existing rule
- MAJOR: scope change, rule removal, restructuring
