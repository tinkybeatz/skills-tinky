# SonarQube Template — Java / Kotlin / JVM

Use when the scanner detects `pom.xml`, `build.gradle*`, `settings.gradle*`, Java/Kotlin files, Spring, Quarkus, Micronaut or Android JVM modules.

## Maven

Prefer the Maven scanner when the project is Maven-native:

```bash
mvn verify sonar:sonar \
  -Dsonar.projectKey=<project-key> \
  -Dsonar.host.url=$SONAR_HOST_URL \
  -Dsonar.token=$SONAR_TOKEN
```

Coverage:

```properties
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

For multi-module Maven, inspect module paths and use each module's generated JaCoCo XML if needed.

## Gradle

Prefer the Gradle Sonar plugin when already present:

```bash
./gradlew test jacocoTestReport sonar
```

Coverage:

```properties
sonar.coverage.jacoco.xmlReportPaths=build/reports/jacoco/test/jacocoTestReport.xml
```

## Generic properties fallback

```properties
sonar.sources=src/main/java,src/main/kotlin
sonar.tests=src/test/java,src/test/kotlin
sonar.sourceEncoding=UTF-8
```

## Exclusions

```properties
sonar.exclusions=**/target/**,**/build/**,**/generated/**,**/generated-sources/**,**/generated-test-sources/**
sonar.coverage.exclusions=**/*Application.java,**/*Config.java,**/*Configuration.java,**/dto/**,**/generated/**,**/generated-sources/**
sonar.cpd.exclusions=**/generated/**,**/generated-sources/**,**/fixtures/**
```

Do not blanket-exclude DTOs if they contain validation or mapping logic.

## Quality profile

- Start with `Sonar way` for Java/Kotlin.
- For high-risk backend APIs, add stricter rules around injection, deserialization, crypto, nullability and concurrency.
- Keep Checkstyle/SpotBugs/ErrorProne if already part of the project; SonarQube is not a full replacement for all JVM static checks.

## Quality gate

- `standard-app` for normal services.
- `critical-system` for internal frameworks, auth services, payment/financial flows or shared libraries.

