# SonarQube Template — Go

Use when the scanner detects `go.mod`, Go source files, services, CLIs or workers.

## Project scope

```properties
sonar.sources=.
sonar.tests=.
sonar.test.inclusions=**/*_test.go
sonar.sourceEncoding=UTF-8
```

Because Go projects are often rooted at `.`, exclusions matter.

## Coverage

```properties
sonar.go.coverage.reportPaths=coverage.out
```

Typical command:

```bash
go test ./... -coverprofile=coverage.out
```

## Exclusions

```properties
sonar.exclusions=**/vendor/**,**/bin/**,**/dist/**,**/build/**,**/coverage/**,**/mocks/**,**/mock/**,**/*.pb.go,**/*_generated.go
sonar.coverage.exclusions=**/*_test.go,**/cmd/**,**/migrations/**,**/mocks/**,**/*.pb.go,**/*_generated.go
sonar.cpd.exclusions=**/fixtures/**,**/testdata/**,**/*.pb.go,**/*_generated.go
```

Do not exclude `cmd/**` if it contains meaningful CLI behavior rather than thin wiring.

## Quality profile

- Start with `Sonar way` for Go.
- Keep `go test`, `go vet`, `staticcheck` and `golangci-lint` if already used.

## Quality gate

- `standard-app` for normal services.
- `critical-system` for auth, infra control planes, payment, deployment or security-sensitive tools.

