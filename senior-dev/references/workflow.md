# Workflow — Detailed 6 Steps

This file is the **Deep tier playbook**. Standard tier picks a subset (usually 0 + 2 + 3 + 4, skipping the extensive Step 1 framing and Step 5 retro); Quick tier skips the workflow entirely. The SKILL.md summary lists step names + purpose; open this file when you actually need the detail.

Don't apply the workflow mechanically — the value comes from each step's rationale, not from box-checking.

---

## Step 0: Discover Project Standards

Standards load from two sources, in order.

### A. Skill-bundled standards (`std/` directory)

The skill bundles reusable standards in `std/`, organized by project name.

1. **Always load `std/_shared/`** — standards that apply to every project (security, etc.)
2. **Detect the current project** from the working directory name (e.g., if cwd contains `sapain-borne`, look for `std/sapain-borne/`)
3. **Load all `.md` files** from the matching project folder
4. If the user explicitly specifies a project (`/senior-dev sapain-borne`), load that project's standards even if the cwd doesn't match

To see what's available: list the directories in `std/` (excluding `_shared` and `README.md`).

### B. Project-local standards (in the repo itself)

After loading bundled standards, scan the project repo. Search order: `CLAUDE.md` > `docs/decisions/` (past ADRs — read titles, scan recent ones) > `docs/stds/` > `docs/INIT.md` > `docs/CONSTRAINT.md` > tooling configs (tsconfig, eslint, biome, Dockerfile).

Extract: naming conventions, architecture patterns, testing requirements, security rules, deployment constraints, observability standards, **and any past architectural decisions that constrain the current question**. If a recent ADR is directly relevant, cite it explicitly in your response — past decisions are facts, not suggestions.

### Conflict resolution

- **Bundled standards** provide the baseline rules.
- **Project-local standards** override bundled ones when they conflict (the repo is the source of truth for its own conventions).
- If a standard conflicts with the user's request, surface the conflict explicitly.

---

## Step 1: Frame the Engineering Problem

Clarify the **problem** before proposing solutions. Unpack into:

- **Business intent** — what outcome is driving this?
- **Scope boundaries** — what's in vs out?
- **Non-functional requirements** — latency, throughput, reliability, scale, cost targets?
- **Constraints** — regulatory, architectural, team capacity, existing stack?
- **Dependencies and risks** — what could block this?

Ask clarifying questions if critical details are missing. This is also where the **partner reflex #1 (what's missing)** kicks in — if the user's framing has a glaring hole, surface it before going further. Produce a 2-3 paragraph framing with objective, constraints, assumptions, and key unknowns.

---

## Step 2: Evaluate Solution Options

Generate at least **2 viable options** — including 1 low-complexity baseline.

| Dimension | Why it matters |
|---|---|
| **Complexity** | Implementation risk, debugging difficulty, team expertise |
| **Reliability** | Failure modes, blast radius |
| **Scalability** | Headroom before hitting limits |
| **Maintainability** | Operational burden, observability |
| **Time-to-deliver** | How long to production |
| **Cost** | Infrastructure + operational cost |
| **Resource budget** | Memory, CPU, I/O syscalls, network round-trips — what does this cost the machine? |

**The low-level reflex:** For every option, ask: *"What happens at the syscall boundary? How many allocations? How many round-trips? What's the failure mode under load?"* You don't need to optimize prematurely, but you must *know* where the cost is.

Rules: at least 1 option must minimize risk. Be explicit about which constraints each option violates. Reject poor cost/benefit options.

---

## Step 3: Plan Implementation and Validation

Break down into incremental steps with: changes, acceptance criteria (verifiable), tests, monitoring, rollback plan.

**Critical:** no behavior change without test coverage. No release without rollback plan. All acceptance criteria must be mapped to concrete checks.

---

## Step 4: Execute, Test, and Verify Quality

After implementing, **test in the most pertinent form for the context**. Not every change needs the same kind of test — pick the right tool:

| Context | Test form | Why this one |
|---|---|---|
| Pure logic (validation, parsing, math) | Unit test | Fast, deterministic, catches regressions |
| DB queries, migrations, transactions | Integration test against real DB | Mocks hide real SQL bugs (schema drift, constraint violations) |
| HTTP endpoints / API contracts | Request-level test (supertest, curl, httpie) | Validates status codes, payloads, auth, error shapes |
| Multi-service flow (outbox → handler → email) | Manual e2e or scripted scenario | Catches integration gaps between services |
| UI behavior (kiosk screens, forms) | Manual test + visual verification | Automated UI tests are brittle; human eye catches layout/UX issues |
| Race conditions, concurrency | Stress test or targeted repro script | Only way to flush out timing bugs (double-submit, pool exhaustion) |
| Config / env / deployment | Smoke test in target environment | "Works on my machine" is not a test |

**The principle:** test at the boundary where the bug would actually happen. A unit test on a SQL query string catches nothing — run the query against Postgres. A mock of the email service proves nothing — call the real endpoint and check the job landed.

**After every implementation step:**
1. Run `tsc --noEmit` (type safety is the cheapest test)
2. Run the pertinent test form from the table above
3. If the change touches a critical path (payments, auth, lockout), test the failure mode too — not just the happy path

No closure if critical checks fail. Escalate high-severity risks.

---

## Step 5: Review, Learn, and Iterate

Iterate if acceptance criteria are partially validated, risk is unclear, or quality < 80/100. Stop when all criteria pass and risks are documented.
