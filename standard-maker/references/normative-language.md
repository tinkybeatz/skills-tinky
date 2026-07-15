# Normative language guide

Based on RFC 2119 and adapted to the context of internal engineering standards.

## The 5 keywords

### MUST / MUST NOT

**Force:** absolute. No exception possible without a formal waiver.

**When to use it:**
- Critical security rules (authentication, encryption)
- Regulatory/compliance constraints
- System invariants whose violation causes an outage

**Examples:**
```
- Secrets MUST NOT be committed to version control.
- All API responses MUST include a `Content-Type` header.
- Database migrations MUST be wrapped in a transaction.
```

**Abuse signal:** if more than 50% of a standard's rules are MUST, the standard is probably too rigid. Check whether some rules can be SHOULD.

---

### SHOULD / SHOULD NOT

**Force:** strong recommendation. Exceptions allowed but must be justified.

**When to use it:**
- Best practices with legitimate exceptions
- Quality rules that can be relaxed in certain contexts
- Team conventions with known edge cases

**Examples:**
```
- PRs SHOULD stay below 400 changed lines.
- Functions SHOULD NOT have more than 3 parameters.
- Error responses SHOULD include a machine-readable error code.
```

**Abuse signal:** if every rule is SHOULD, the standard has no teeth. At least the security and integrity rules should be MUST.

---

### MAY

**Force:** optional. The practice is recognized as valid but not required.

**When to use it:**
- Recommended but non-essential practices
- Optional features in an API contract
- Permitted alternatives within the scope of the standard

**Examples:**
```
- Services MAY implement health check endpoints beyond /healthz.
- Documentation MAY include architecture diagrams using Mermaid.
- Emergency fixes MAY bypass the PR size rule with post-merge review.
```

---

## Common trap: the SHOULD disguised as a MUST

```
Bad:  "Developers MUST write unit tests for every function."
```

If the project's reality includes trivial functions (getters, constructors) that do not warrant a test, this is a SHOULD, not a MUST. A MUST that is not enforced 100% of the time destroys the standard's credibility.

**Decision rule:** if you cannot automate or audit compliance 100% of the time, it is probably a SHOULD.

---

## Frequent combinations

| Pattern | Usage |
|---|---|
| "MUST ... unless [condition]" | Requirement with a structured exception |
| "SHOULD ... when [context]" | Conditional recommendation |
| "MUST NOT ... except [waiver]" | Prohibition with a waiver process |
| "MAY ... if [condition]" | Conditional permission |

**Examples:**
```
- PRs MUST be approved by a code owner unless classified as documentation-only.
- Services SHOULD implement circuit breakers when calling external APIs.
- Secrets MUST NOT be logged, except hashed fingerprints for debugging.
- Teams MAY use custom linter rules if they extend (not override) the base config.
```

---

## Consistency within a standard

A well-written standard distributes the keywords as follows (a guide, not an absolute rule):

| Keyword | Typical proportion | Signal if too high |
|---|---|---|
| MUST | 20-40% | Standard too rigid, hard to adopt |
| SHOULD | 30-50% | Normal — this is the core of best practices |
| MAY | 10-20% | Normal — explicit flexibility |
| MUST NOT | 5-15% | If > 20%, the standard is mostly a list of prohibitions |

A standard that is 100% MUST is a standard no one will follow. A standard that is 100% MAY is not a standard.
