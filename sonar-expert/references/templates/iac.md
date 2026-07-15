# SonarQube Template — Infrastructure as Code

Use when the scanner detects Terraform, Kubernetes YAML, Helm, Docker, CloudFormation, Ansible or deployment manifests.

## Project scope

```properties
sonar.sources=.
sonar.sourceEncoding=UTF-8
```

For IaC-only repos, coverage is normally not applicable. Do not add fake coverage properties.

## Exclusions

```properties
sonar.exclusions=**/.terraform/**,**/terraform.tfstate*,**/vendor/**,**/charts/**,**/charts/**/templates/tests/**,**/generated/**,**/dist/**,**/build/**
sonar.cpd.exclusions=**/generated/**,**/fixtures/**,**/examples/**
```

Do not exclude Kubernetes or Terraform application manifests just because they produce findings. Findings are often the point of IaC analysis.

## Quality profile

- Use Sonar way profiles for available IaC languages.
- Complement with domain tools already present: `terraform validate`, `tflint`, `checkov`, `trivy config`, `kubeconform`, `ansible-lint`.

## Quality gate

- Gate should focus on new code security/configuration issues and reviewed hotspots.
- Coverage conditions are not relevant unless the repo also contains testable application code.

## CI notes

- Run format/validate/lint before Sonar where the repo already exposes those commands.
- For GitOps repos, avoid making generated manifests the primary source unless the repo stores only generated output.

