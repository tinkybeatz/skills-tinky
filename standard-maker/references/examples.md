# Examples of well-written standards

## Example 1 — Pull Request Review standard

```md
# Standard: Pull Request Review

- Status: Active
- Version: 1.1.0
- Owner: Engineering Enablement
- Approvers: Backend Lead, Frontend Lead
- Effective date: 2026-03-10
- Last review date: 2026-03-10

## Scope

Applies to all repositories in this project.
Does NOT apply to automated dependency update PRs (Renovate, Dependabot).

## Normative rules

### R-REVIEW-01 Test impact note

Requirement:
- Every PR MUST include a test impact note describing what was tested and how. `[SRC-001]`

Rationale:
- Q1 2026 defect review showed 40% of production bugs came from changes with no documented test strategy.

Enforcement:
- PR template includes a mandatory "Test Impact" field
- CI blocks merge if the field is empty

Exceptions:
- Documentation-only PRs MAY skip this requirement.

---

### R-REVIEW-02 Code owner approval

Requirement:
- Every PR MUST be approved by at least 1 code owner before merge. `[SRC-002]`

Rationale:
- Ensures domain expertise is applied to every change in critical paths.

Enforcement:
- GitHub CODEOWNERS file + branch protection rule requiring owner approval

Exceptions:
- None. Emergency fixes still require approval (post-merge within 48h if absolutely necessary).

---

### R-REVIEW-03 PR size limit

Requirement:
- PRs SHOULD stay below 400 changed lines excluding generated files. `[SRC-003]`

Rationale:
- Review quality degrades sharply above 400 lines. Defect detection rate drops from 60% to 15% on large PRs.

Enforcement:
- CI warning (non-blocking) when diff exceeds threshold
- Review checklist reminds authors to split large changes

Exceptions:
- Migrations and generated code MAY exceed this limit with reviewer acknowledgment.

## Enforcement summary

| Rule | Mechanism | Automated |
|---|---|---|
| R-REVIEW-01 | PR template + CI check | Yes |
| R-REVIEW-02 | CODEOWNERS + branch protection | Yes |
| R-REVIEW-03 | CI warning | Partial (warning only) |

## Exceptions process

Emergency production fixes MAY bypass one rule with an incident ticket and 48h retroactive review.

## Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| PRs merged without test note | 35% | < 5% | CI logs |
| Defects from untested changes | 40% of prod bugs | < 15% | Incident post-mortems |
| PRs > 400 lines | 25% | < 10% | GitHub API |

## Sources

- SRC-001 | Internal defect review Q1 | docs/quality/pr-defects-2026-q1.md | Internal | 2026-04-10 | Shows missing test impact notes in failed changes.
- SRC-002 | Code ownership policy | docs/governance/code-owners-policy.md | Internal | 2026-02-18 | Defines mandatory owner-based review model.
- SRC-003 | Engineering productivity benchmark | https://example.com/pr-size-study | External | 2025-11-05 | Supports recommended PR size threshold for review quality.

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-03-10 | Engineering Enablement | Initial release |
| 1.1.0 | 2026-04-15 | Engineering Enablement | Added PR size limit rule (R-REVIEW-03) |
```

---

## Example 2 — API Security standard

```md
# Standard: API Security

- Status: Active
- Version: 1.0.0
- Owner: Security Team
- Approvers: CTO, Backend Lead
- Effective date: 2026-04-01
- Last review date: 2026-03-28

## Scope

Applies to all HTTP APIs exposed to the internet or to third-party consumers.
Internal service-to-service APIs behind a private network are covered by a separate standard.

## Normative rules

### R-SEC-01 Authentication required

Requirement:
- All API endpoints MUST require authentication unless explicitly documented as public. `[SRC-001]`

Rationale:
- Unauthenticated endpoints are the primary attack vector for data exposure (OWASP API Top 10 #1).

Enforcement:
- Middleware rejects unauthenticated requests by default
- Public endpoints require an explicit `auth: "public"` annotation in route definition
- Security audit flags unannotated endpoints

Exceptions:
- Health check endpoints (`/healthz`, `/readyz`) MAY be unauthenticated.

---

### R-SEC-02 Rate limiting

Requirement:
- All public-facing endpoints MUST enforce rate limiting. `[SRC-002]`
- Default: 100 requests per minute per IP.

Rationale:
- Prevents brute-force attacks, credential stuffing, and denial-of-service.

Enforcement:
- Reverse proxy (Traefik) rate limiting middleware
- Application-level rate limiting for sensitive endpoints (login, OTP)

Exceptions:
- Internal service-to-service calls authenticated by API key MAY bypass rate limiting.

## Sources

- SRC-001 | OWASP API Security Top 10 | https://owasp.org/API-Security/ | OWASP | 2023 | Industry baseline for API security risks.
- SRC-002 | NIST SP 800-53 SC-5 | https://csf.tools/reference/nist-sp-800-53/r5/sc/sc-5/ | NIST | 2020 | DoS protection control.

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-01 | Security Team | Initial release |
```

---

## Anti-examples — What NOT to do

**Bad: vague rule**
```
- The code must be clean and well structured.
```
No normative keyword, not testable, not enforceable.

**Good:**
```
### R-CODE-01 Function length
Requirement:
- Functions MUST NOT exceed 50 lines of executable code (excluding comments and blank lines). `[SRC-001]`
Enforcement:
- ESLint rule `max-lines-per-function` configured at 50
```

**Bad: rule without a source**
```
- PRs must be small because it's a good practice.
```

**Good:**
```
- PRs SHOULD stay below 400 changed lines. `[SRC-003]`
[SRC-003 cited in the Sources section with URL and justification]
```

**Bad: no enforcement**
```
- All secrets MUST be stored in a vault.
Enforcement: team awareness.
```
"Team awareness" is not a control mechanism.

**Good:**
```
Enforcement:
- CI scan (gitleaks) blocks merge on detected secrets
- Vault access audit log reviewed monthly
```
