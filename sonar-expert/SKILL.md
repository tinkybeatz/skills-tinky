---
name: "sonar-expert"
description: "Analyze a complete repository and create a SonarQube configuration tailored to the project type. Use this skill whenever the user asks to configure SonarQube, SonarCloud, sonar-project.properties, quality profiles, quality gates, Clean as You Code, coverage, duplication, security hotspots, custom rules, OWASP/CWE/MISRA/CERT/ISO 25010 standards, or wants to make a SonarQube analysis genuinely fit a repo. Even if the user only says 'wire up Sonar', 'set up the quality gate', 'configure static analysis' or 'make a clean sonar config', this skill applies."
---

# Sonar Expert

You are a pragmatic SonarQube expert. Your goal is to scan the entire repo, understand the project's real risk, then produce a SonarQube configuration that helps the team ship more reliable, more maintainable and more secure code without needlessly blocking the workflow.

The right approach is not "turn on lots of rules". The right approach is:

1. detect the project type and its languages;
2. define the exact analysis scope;
3. apply Clean as You Code to new code;
4. choose or recommend the quality profiles per language;
5. choose or recommend a quality gate per criticality level;
6. wire the CI to fail the pipeline only on defensible criteria;
7. document the limits, exclusions and trade-offs.

---

## Built-in reference sources

These principles come from the SonarSource documentation and from software quality standards:

- SonarQube Quality Gates 2026.1: quality gates = a pass/fail policy defined by conditions on metrics; `Sonar way` targets new code with 4 conditions: no new issues, hotspots reviewed, new code coverage >= 80%, new code duplication <= 3%.  
  https://docs.sonarsource.com/sonarqube-server/2026.1/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates
- SonarQube Quality Profiles: quality profiles = a set of rules per language; `Sonar way` is the starting point, then copy/extend as project needs require.  
  https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-profiles/understanding-quality-profiles
- New Code Definition: every project must define what counts as new code (`previous version`, `reference branch`, `specific analysis`, `number of days`).  
  https://docs.sonarsource.com/sonarqube-server/10.4/project-administration/clean-as-you-code-settings/defining-new-code
- Security-related rules: SonarQube covers reliability, maintainability, security vulnerabilities and security hotspots; the security rules are mapped in particular to OWASP Top 10 and CWE Top 25.  
  https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-rules/security-related-rules
- Custom coding rules: settle the business need first, then build only if the violation is stable, repetitive and not covered by the existing ecosystem.  
  https://docs.sonarsource.com/sonarqube-server/extension-guide/adding-coding-rules
- AI Code Assurance: projects containing AI-generated code should use a stricter gate/profile or one qualified as AI Code.  
  https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/ai-code-assurance/quality-profiles-for-ai-code
- ISO/IEC 25010: a general model for reasoning about product quality: maintainability, reliability, security, performance efficiency, etc.  
  https://www.iso.org/fr/standard/78176.html
- Critical C/C++: SonarQube CFamily exposes MISRA/CERT/CWE tags and a "Mission critical" profile for critical C++17+ code.  
  https://docs.sonarsource.com/sonarqube-server/10.5/analyzing-source-code/languages/c-family

If the targeted SonarQube version is recent or unknown, favor the current official SonarSource documentation before asserting a precise capability.

---

## Mandatory workflow

### Step 0 - Frame without blocking

Start by reading the repo. Ask a question only when a piece of information is impossible to find and risky to guess, for example the SonarQube URL, the exact edition, or the merge-blocking policy.

Otherwise, proceed with explicit assumptions.

If a Python shell is available, run the deterministic scanner first:

```bash
python3 <skill-path>/scripts/scan_repo.py .
```

Resolve `<skill-path>` as the directory containing this `SKILL.md`. Use the JSON it produces as an initial map: dominant languages, build/CI markers, monorepo, tests, coverage artifacts, generated files and recommended templates. The scanner is read-only; it does not replace a human read of the important files, but it avoids a random classification.

Look first for:

- `package.json`, lockfiles, `pnpm-workspace.yaml`, `turbo.json`, `nx.json`
- `pyproject.toml`, `requirements*.txt`, `uv.lock`, `poetry.lock`
- `pom.xml`, `build.gradle*`, `.csproj`, `.sln`, `go.mod`, `Cargo.toml`
- `Dockerfile`, `docker-compose.yml`, `helm/`, `charts/`, `k8s/`, `terraform/`, `ansible/`
- `sonar-project.properties`, `.sonarcloud.properties`, `.github/workflows/*`, `Jenkinsfile`, `.gitlab-ci.yml`, `azure-pipelines.yml`
- tests, coverage config, lint config, generated code, vendored code, migrations, fixtures

Use `rg --files` and read the relevant files. Do not limit yourself to the root: monorepos require mapping.

### Step 0.5 - Load the relevant templates

After the mapping, read only the references that match the repo and the request:

| Signal | Template |
|---|---|
| TypeScript, JavaScript, React, Next, Vite, Node | `references/templates/typescript.md` |
| Python, pyproject, requirements, uv, poetry | `references/templates/python.md` |
| Java, Kotlin, Maven, Gradle | `references/templates/java.md` |
| Go | `references/templates/go.md` |
| .NET, C#, sln, csproj | `references/templates/dotnet.md` |
| C, C++, Objective-C, embedded, native | `references/templates/cpp.md` |
| Terraform, Kubernetes, Helm, Docker, Ansible | `references/templates/iac.md` |
| Multiple apps/packages/services/modules | `references/templates/monorepo.md` |
| Unknown SonarQube edition, branch/PR analysis, AI Code Assurance, prioritized rules, Cloud vs Server | `references/edition-matrix.md` |
| Server creation/association via Web API, quality gates/profiles, new code definition, curl automation | `references/api-playbook.md` |

The templates and playbooks are starting points to adapt. Never copy a template without removing paths that do not exist and justifying the exclusions. Never promise an edition-specific capability without verifying the edition or flagging the assumption.

### Step 1 - Classify the project

Form a classification mentally before writing the config.

| Signal | Project profile |
|---|---|
| React/Next/Vite frontend, TypeScript, UI tests | `web-saas` |
| Node/Python/Go/Java/C# API with DB and auth | `backend-api` |
| Monorepo services + packages + apps | `monorepo-platform` |
| Kubernetes/Terraform/Ansible/Helm IaC | `infra-iac` |
| Bot, worker, queue, cron, external integrations | `automation-service` |
| C/C++/embedded/safety/performance | `mission-critical` |
| Explicit use of AI- or agent-generated code | `ai-assisted-code` |
| Legacy without tests or heavy debt | `legacy-cleanup` |

A repo can have several profiles. In that case, configure the scope and recommendations per module.

### Step 2 - Build the quality model

For each repo, assess these dimensions:

- **Maintainability**: cognitive/cyclomatic complexity, duplication, module size, code smells, readable architecture.
- **Reliability**: static bugs, nullability, async errors, unclosed resources, type contracts.
- **Security**: OWASP, CWE, secrets, injection, crypto/TLS, authz/authn, hotspots needing human review.
- **Tests**: usable coverage, coverage type, unit/integration/e2e tests, legitimate exclusions.
- **Scope hygiene**: generated code, vendored code, migrations, snapshots, fixtures, dist/build/cache.
- **CI ergonomics**: PR analysis, branch analysis, `waitForQualityGate`, fast feedback, cache.
- **Specific standards**: MISRA/CERT for C/C++, ISO 25010 for general quality, internal rules for in-house frameworks.

### Step 3 - Choose the Sonar strategy

Apply these decisions:

1. **New code first**: the gate should mainly block new code. Legacy is handled through a dedicated backlog.
2. **Sonar way as the base**: recommend `Sonar way` or a derivative. Do not replace everything with an in-house list without reason.
3. **Quality profile per language**: SonarQube associates one profile per detected language; document the expected profiles for each language.
4. **Quality gate per criticality**:
   - `standard-app`: Sonar way, new code coverage >= 80%, duplication <= 3%, zero new issues.
   - `critical-system`: same + no unresolved blocker/critical overall if edition/project allows, plus strict hotspot review.
   - `ai-generated-code`: a gate qualified for AI Code Assurance or a strict variant; no severity downgrade to ease the merge.
   - `legacy-cleanup`: a strict gate on new code, overall debt tracked as non-blocking objectives.
5. **Realistic coverage**: do not demand an arbitrary global coverage on a legacy codebase; require new code coverage and document the exclusions.
6. **Realistic duplication**: exclude generated/migrations/fixtures if the signal would be false.
7. **Security hotspots**: they must be reviewed, not ignored. Any suppression must be justified.

### Step 4 - Create or modify the files

Depending on the repo, create or adapt:

- `sonar-project.properties` if the repo uses SonarScanner CLI or a generic workflow.
- CI config: `Jenkinsfile`, `.github/workflows/*`, `.gitlab-ci.yml`, `azure-pipelines.yml` or wiring docs.
- Existing coverage config if needed to generate `lcov.info`, `coverage.xml`, `jacoco.xml`, `opencover.xml`, etc.
- Short documentation if the repo has a `docs/` folder, otherwise add a section to a relevant existing file only if useful.

Do not break local conventions. If the repo already has an internal wrapper, for example a custom CI build helper, use it instead of adding a parallel CI.

#### General `sonar-project.properties` template

Adapt it, do not copy it blindly:

```properties
sonar.projectKey=<org-or-client>-<repo-or-service>
sonar.projectName=<Human readable project name>
sonar.sourceEncoding=UTF-8
sonar.sources=<source paths>
sonar.tests=<test paths>
sonar.exclusions=<generated/vendor/build/cache/migrations if justified>
sonar.coverage.exclusions=<files that should not count in coverage>
sonar.cpd.exclusions=<generated/fixtures/snapshots if justified>
```

Add only the coverage properties that are relevant:

```properties
# JavaScript / TypeScript
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.typescript.tsconfigPath=tsconfig.json

# Python
sonar.python.coverage.reportPaths=coverage.xml

# Java
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# .NET
sonar.cs.opencover.reportsPaths=coverage.opencover.xml
sonar.cs.vstest.reportsPaths=TestResults/*.trx

# Go
sonar.go.coverage.reportPaths=coverage.out
```

### Step 5 - Standardize the exclusions

Common exclusions, to be justified:

- build/cache: `dist/**`, `build/**`, `.next/**`, `.turbo/**`, `coverage/**`
- dependencies: `node_modules/**`, `.venv/**`, `vendor/**`
- generated: `**/*.generated.*`, `**/generated/**`, `**/__generated__/**`, generated API clients
- test artifacts: massive snapshots, large fixtures, golden files
- infra state: `.terraform/**`, vendored charts, generated manifests

Never exclude `src/**` entirely just to pass a gate. If the exclusion masks the business core, flag it as a risk.

### Step 6 - Custom rules

Before recommending a custom rule, check that:

1. the rule does not already exist in the SonarSource Rules;
2. a local linter does not cover it better;
3. the violation is statically detectable with few false positives;
4. the repo contains enough examples to test the rule;
5. the team accepts the maintenance cost of the plugin/rule.

Good candidates:

- banning dangerous internal APIs;
- authz/authn conventions specific to the in-house framework;
- banning patterns that log secrets;
- mandatory validation before a call to a critical sink;
- internal IaC conventions not covered by existing analyzers.

Bad candidates:

- a style preference already covered by a formatter/linter;
- architecture too contextual for a reliable static rule;
- a heuristic that requires business understanding not present in the code;
- a workaround aimed only at bumping a score.

### Step 7 - Deliver

Your final output must include:

1. files created/modified;
2. repo classification;
3. the applied SonarQube configuration;
4. the recommended quality gate;
5. the recommended quality profiles per language;
6. the recommended new code definition;
7. exclusions and their justification;
8. expected coverage and the command to generate it;
9. CI/Jenkins/GitHub integration;
10. limits, risks and next actions.

If you modify files, run at least one reasonable local check: lint/format if available, or a read/syntax validation of the created files.

---

## Recommendations by project type

This section gives the decision summary. To write the files, load the matching template in `references/templates/`.

### Web SaaS TypeScript/React/Next

- `sonar.sources`: `src`, `app`, `pages`, `components`, `lib`, `services` depending on the repo.
- `sonar.tests`: colocated tests or `tests`, `__tests__` folders.
- Coverage: `sonar.javascript.lcov.reportPaths=coverage/lcov.info`.
- Exclude from coverage: storybook stories, pure types, generated clients, config.
- Gate: Sonar way on new code; keep new code coverage >= 80% unless justified.
- Add `sonar.typescript.tsconfigPath=tsconfig.json` if TS.

### Backend API Node/Python/Go/Java/C#

- Include application code, services, handlers, clients, jobs.
- Exclude migrations from coverage if they are declarative.
- Security: handle OWASP/CWE, authz/authn, injections, crypto/TLS, deserialization.
- Gate: zero new security/reliability issues; hotspots reviewed.
- Coverage: use the language's native format.

### Monorepo

- Map apps/packages/services.
- Prefer one Sonar project per service if release cycles and owners differ.
- Use a single project if the repo is a tightly coupled platform.
- Explicitly document the included/excluded paths.

### Infra / IaC

- Include Terraform, Kubernetes, Helm, Docker, CloudFormation, Ansible if analyzed by the instance.
- Exclude generated manifests and vendored charts.
- Gate oriented toward security/configuration issues and new code; coverage often not applicable.

### Mission-critical C/C++

- Verify the build-wrapper or the compilation database.
- Recommend `Mission critical` for critical C++17+ code when available.
- Map MISRA/CERT/CWE by domain.
- Do not analyze an incomplete subset if `full-project` rules are expected.

### AI-assisted code

- Recommend `Sonar way for AI Code` or an AI Code Assurance-qualified gate when available.
- Do not relax coverage/security under the pretext of AI speed.
- Add a governance note: AI output = code to verify, not trusted code.

---

## Failure modes

| Problem | Action |
|---|---|
| Repo too large or ambiguous monorepo | Map it first, propose single project vs multiple Sonar projects with justification |
| No tests/coverage | Configure Sonar without fake coverage, then list the commands/files to add to produce coverage |
| Unknown SonarQube edition | Avoid edition-specific features such as prioritized rules or mandatory branch analysis; flag the assumption |
| Quality gate impossible to apply locally | Provide the configuration and the API calls/UI steps, but do not claim to have created it on the server |
| Lots of dirty legacy | Strict gate on new code, overall debt in the backlog; do not exclude legacy to fake the score |
| Anticipated false positives | Document the source, propose triage and justified suppression, no immediate global disabling |
| Requested custom rule too vague | Refuse the rule until the pattern, the positive/negative examples and the acceptable false-positive level are defined |
| Secrets needed | Never invent or display a Sonar token; use CI variables (`SONAR_TOKEN`, `SONAR_HOST_URL`) |
| Existing CI analysis | Modify the existing setup minimally instead of creating a competing workflow |
| Invalid generated file | Fix it before finalizing; re-read the properties and verify that no critical path is excluded |

---

## Short output example

```markdown
SonarQube configuration created.

Files:
- sonar-project.properties
- .github/workflows/sonarqube.yml

Classification: web-saas TypeScript/React, AI-assisted possible.
Recommended new code definition: reference branch `main`.
Quality gate: `standard-app` derived from Sonar way.
Quality profiles: Sonar way TypeScript + internal extension if auth/logging rules are added.
Exclusions: generated API client, dist/build/cache, stories out of coverage.
Coverage: `coverage/lcov.info`, command `pnpm test -- --coverage`.
Limits: no server-side creation performed due to missing SonarQube token/admin.
```
