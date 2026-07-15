# SonarQube Template — C / C++ / Objective-C

Use when the scanner detects C/C++ files, embedded code, native libraries, performance-critical systems or safety/security standards such as MISRA/CERT.

## Build context is mandatory

Do not configure CFamily analysis as a simple file scan. SonarQube needs a real build context:

- build-wrapper output, or
- compilation database `compile_commands.json`.

Build-wrapper example:

```bash
build-wrapper-linux-x86-64 --out-dir build_wrapper_output_directory make clean all
sonar-scanner
```

Properties:

```properties
sonar.sources=src,include
sonar.tests=tests
sonar.cfamily.build-wrapper-output=build_wrapper_output_directory
sonar.sourceEncoding=UTF-8
```

Compilation database example:

```properties
sonar.sources=src,include
sonar.tests=tests
sonar.cfamily.compile-commands=compile_commands.json
sonar.sourceEncoding=UTF-8
```

Use only one of `sonar.cfamily.build-wrapper-output` or `sonar.cfamily.compile-commands`.

## Coverage

Coverage depends on tooling:

- GCOV / llvm-cov / Bullseye depending on project conventions.
- Do not invent coverage properties if reports are absent.

## Exclusions

```properties
sonar.exclusions=**/build/**,**/cmake-build-*/**,**/third_party/**,**/external/**,**/vendor/**,**/generated/**,**/*.pb.cc,**/*.pb.h
sonar.coverage.exclusions=**/tests/**,**/test/**,**/third_party/**,**/external/**,**/generated/**,**/*.pb.cc,**/*.pb.h
sonar.cpd.exclusions=**/third_party/**,**/external/**,**/generated/**,**/fixtures/**
```

Be careful: excluding part of a C/C++ project can reduce the accuracy of full-project and symbolic-execution rules.

## Quality profile

- Start with `Sonar way` for normal native projects.
- For C++17+ mission-critical code, recommend `Mission critical` when available.
- Map rules to MISRA/CERT/CWE when the domain requires safety or security evidence.

## Quality gate

- `critical-system` by default for embedded, safety, auth, crypto, runtime, deployment or infra-control C/C++.
- Keep new-code gate strict and document legacy deviations separately.

