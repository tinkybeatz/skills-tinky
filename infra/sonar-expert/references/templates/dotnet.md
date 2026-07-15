# SonarQube Template — .NET / C#

Use when the scanner detects `.sln`, `.csproj`, C# files, ASP.NET, worker services or libraries.

## Scanner flow

Prefer SonarScanner for .NET:

```bash
dotnet sonarscanner begin \
  /k:"<project-key>" \
  /d:sonar.host.url="$SONAR_HOST_URL" \
  /d:sonar.token="$SONAR_TOKEN" \
  /d:sonar.cs.opencover.reportsPaths="coverage.opencover.xml" \
  /d:sonar.cs.vstest.reportsPaths="TestResults/*.trx"

dotnet build
dotnet test --collect:"XPlat Code Coverage" --logger trx

dotnet sonarscanner end /d:sonar.token="$SONAR_TOKEN"
```

If the project already uses Coverlet/OpenCover, adapt report paths.

## Generic properties fallback

Use fallback properties only when the .NET scanner cannot be used:

```properties
sonar.sources=.
sonar.tests=.
sonar.test.inclusions=**/*Tests.cs,**/*.Tests.cs
sonar.sourceEncoding=UTF-8
sonar.cs.opencover.reportsPaths=coverage.opencover.xml
sonar.cs.vstest.reportsPaths=TestResults/*.trx
```

## Exclusions

```properties
sonar.exclusions=**/bin/**,**/obj/**,**/TestResults/**,**/Generated/**,**/*.g.cs,**/*.Designer.cs
sonar.coverage.exclusions=**/*Tests.cs,**/*.Tests.cs,**/Program.cs,**/Startup.cs,**/*Migrations/**,**/*.g.cs,**/*.Designer.cs
sonar.cpd.exclusions=**/Generated/**,**/*.g.cs,**/*.Designer.cs,**/Fixtures/**
```

Do not exclude `Program.cs` if it contains business logic or security wiring.

## Quality profile

- Start with `Sonar way` for C#.
- Keep Roslyn analyzers and nullable reference types settings as complementary quality gates.

## Quality gate

- `standard-app` for normal services/libraries.
- `critical-system` for auth, payment, identity, finance or shared infrastructure components.

