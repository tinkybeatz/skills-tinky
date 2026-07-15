# SonarQube Template — TypeScript / JavaScript / React / Next

Use when the scanner detects `package.json`, TypeScript/JavaScript files, React, Next, Vite, Node services, or frontend/backend JS monorepos.

## Project scope

Prefer explicit source roots discovered in the repo:

```properties
sonar.sources=src,app,pages,components,lib,services,server
sonar.tests=src,app,pages,components,lib,services,server,tests,__tests__
sonar.test.inclusions=**/*.test.ts,**/*.test.tsx,**/*.spec.ts,**/*.spec.tsx,**/*.test.js,**/*.spec.js
sonar.sourceEncoding=UTF-8
```

Remove paths that do not exist. For backend-only Node, prefer `src,server,services,lib`.

## Coverage

Use LCOV when the repo has Vitest, Jest, Playwright component coverage, or another JS coverage runner:

```properties
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.typescript.tsconfigPath=tsconfig.json
```

If the repo has multiple TS configs, choose the production config first. Do not point at a generated or test-only tsconfig unless that is the project build contract.

## Exclusions

```properties
sonar.exclusions=**/node_modules/**,**/dist/**,**/build/**,**/.next/**,**/.turbo/**,**/coverage/**,**/__generated__/**,**/*.generated.*,**/generated/**
sonar.coverage.exclusions=**/*.config.*,**/*.d.ts,**/*.stories.*,**/storybook/**,**/__generated__/**,**/*.generated.*,**/generated/**,**/migrations/**
sonar.cpd.exclusions=**/__generated__/**,**/*.generated.*,**/generated/**,**/fixtures/**,**/__fixtures__/**,**/*.snap
```

Justify every exclusion that touches application code.

## Quality profile

- Start with `Sonar way` for JavaScript and TypeScript.
- Extend/copy only for project-specific rules such as forbidden internal APIs, auth/logging conventions, or stricter complexity.
- Keep ESLint/TypeScript compiler as complementary checks; do not try to move all style rules into SonarQube.

## Quality gate

- Default: `standard-app`, derived from Sonar way.
- Conditions on new code: no new issues, hotspots reviewed, coverage >= 80%, duplication <= 3%.
- For AI-heavy repos, use `ai-generated-code` / AI Code Assurance gate if available.

## CI notes

- Run tests with coverage before scanner, for example `pnpm test -- --coverage`.
- If Jenkins already uses an internal build wrapper, prefer enabling SonarQube through that wrapper instead of adding a parallel scanner workflow.

