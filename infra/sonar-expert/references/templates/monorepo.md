# SonarQube Template — Monorepo

Use when the scanner detects multiple apps/packages/services, `pnpm-workspace.yaml`, Turbo, Nx, Maven modules, Gradle multi-project, or many nested build manifests.

## First decision: one Sonar project or many

Prefer **multiple Sonar projects** when:

- services have different owners;
- release cycles differ;
- quality gates should differ by criticality;
- modules use different languages/toolchains;
- PR decoration per service matters.

Prefer **one Sonar project** when:

- modules are tightly coupled;
- the repo is a single product/platform;
- CI already tests/releases everything together;
- the team wants one quality signal.

Document this decision in the final answer.

## Single-project properties

```properties
sonar.sources=apps,packages,services,libs
sonar.tests=apps,packages,services,libs,tests
sonar.sourceEncoding=UTF-8
sonar.exclusions=**/node_modules/**,**/dist/**,**/build/**,**/target/**,**/coverage/**,**/__generated__/**,**/*.generated.*,**/generated/**
sonar.coverage.exclusions=**/*.config.*,**/*.d.ts,**/*.stories.*,**/migrations/**,**/__generated__/**,**/*.generated.*,**/generated/**
sonar.cpd.exclusions=**/fixtures/**,**/__fixtures__/**,**/__generated__/**,**/*.generated.*,**/generated/**
```

Then add language-specific coverage properties from the relevant templates.

## Multi-project pattern

For each service/module, create a minimal `sonar-project.properties` or CI scanner invocation with:

```properties
sonar.projectKey=<org>-<repo>-<module>
sonar.projectName=<repo>/<module>
sonar.projectBaseDir=<module-path>
sonar.sources=<module source paths>
sonar.tests=<module test paths>
```

Do not use `sonar.projectBaseDir` unless the scanner invocation and CI path make that explicit and tested.

## Quality gates

- Shared libraries/frameworks: `critical-system`.
- Normal apps/services: `standard-app`.
- Legacy modules: `legacy-cleanup`.
- AI-heavy modules: `ai-generated-code`.

## CI notes

- Do not create a parallel full-repo scan if CI already has path-aware service pipelines.
- Prefer invoking Sonar in the same unit of build/test ownership as the module.

