# SonarQube Edition Matrix

Use this reference when the user asks for capabilities, automation, CI integration, PR decoration, AI Code Assurance, prioritized rules, security depth, or when the SonarQube edition is unknown.

This matrix is deliberately conservative. SonarSource changes packaging over time, so verify the target instance's version and edition before promising a feature. Prefer the local instance documentation at:

```text
<SONAR_HOST_URL>/web_api
<SONAR_HOST_URL>/api/server/version
```

Official references checked while creating this matrix:

- Branch analysis is available starting in Developer Edition: https://docs.sonarsource.com/sonarqube-server/10.3/analyzing-source-code/branches/branch-analysis
- Pull request analysis is available starting in Developer Edition in SonarQube Server historical docs: https://docs.sonarsource.com/sonarqube-server/9.8/analyzing-source-code/pull-request-analysis/
- Quality gates include Sonar way and Sonar way for AI Code: https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/introduction
- Prioritized-rule quality gate conditions start in Enterprise Edition: https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/managing-custom-quality-gates
- AI CodeFix is Enterprise/Data Center according to current docs: https://docs.sonarsource.com/sonarqube-server/ai-capabilities/overview
- SonarQube Cloud API has different v1/v2 base URLs: https://docs.sonarsource.com/sonarcloud/advanced-setup/web-api/

---

## Quick reading

| Capability | Community Build / Community Edition | Developer Edition | Enterprise Edition | Data Center Edition | SonarQube Cloud |
|---|---:|---:|---:|---:|---:|
| Main branch analysis | Yes | Yes | Yes | Yes | Yes |
| Multiple branch analysis | No / main branch only | Yes | Yes | Yes | Plan-dependent |
| Pull request analysis | No | Yes | Yes | Yes | Yes, plan-dependent on Cloud Free |
| PR decoration in DevOps platform | Limited/no for Server Community | Yes with integration | Yes | Yes | Yes |
| Quality profiles | Yes | Yes | Yes | Yes | Yes |
| Custom quality profiles | Yes | Yes | Yes | Yes | Yes |
| Quality gates | Yes | Yes | Yes | Yes | Yes |
| Custom quality gates | Yes | Yes | Yes | Yes | Yes |
| New Code Definition at project level | Yes | Yes | Yes | Yes | Yes |
| New Code Definition at branch level | No | Yes | Yes | Yes | Plan-dependent |
| Prioritized rules in custom profiles | No | No | Yes | Yes | Check plan |
| Quality gate condition on prioritized rules | No | No | Yes | Yes | Check plan |
| AI Code Assurance gate/profile workflow | Version/edition-dependent; verify | Version/edition-dependent; verify | Yes in current docs | Yes in current docs | Plan-dependent |
| AI CodeFix | No | No | Yes | Yes | Plan-dependent |
| Security hotspot review | Yes | Yes | Yes | Yes | Yes |
| Taint analysis / injection rules | Language/edition/version-dependent; verify | Better coverage depending edition | Better coverage depending edition | Better coverage depending edition | Cloud-managed |
| Portfolio / governance reporting | No | No | Yes | Yes | Enterprise plan features |
| High availability / cluster | No | No | No | Yes | SaaS-managed |

---

## How to decide what to configure

### If edition is unknown

Assume only the portable baseline:

- `sonar-project.properties`
- main branch analysis
- project-level quality gate association if credentials permit
- project-level quality profiles if credentials permit
- project-level new code definition
- no branch-specific profile assumptions
- no prioritized-rule gate condition
- no AI CodeFix promise

State clearly: "edition unknown; branch/PR/AI/prioritized-rule features require verification."

### If Community Build / Community Edition

Optimize for:

- reliable main branch analysis;
- Clean as You Code on main;
- CI wait on quality gate after main/PR-like build if the workflow supports it;
- custom quality profiles and gates when admin rights exist;
- no assumption of native branch or PR analysis.

Do not design the workflow around branch-level gates or PR decoration unless the instance proves it supports them.

### If Developer Edition

Add:

- branch analysis;
- pull request analysis;
- PR quality gate feedback;
- branch-level new code definition when useful.

Keep quality profiles shared from main branch expectations; do not promise Enterprise-only prioritized-rule gates.

### If Enterprise Edition

Add:

- prioritized rules in custom quality profiles;
- quality gate conditions based on prioritized issues;
- AI CodeFix if enabled by instance admin and supported for the language;
- portfolio/governance workflows if relevant.

Use this when the project has critical systems, compliance reporting, AI-generated code governance, or many teams.

### If Data Center Edition

Treat as Enterprise plus operational scale:

- clustering/high availability;
- larger organization governance;
- same project-level configuration concepts, but avoid heavy API automation without rate/operational safeguards.

### If SonarQube Cloud

Use Cloud documentation and base URLs, not Server assumptions:

- EU v2: `https://api.sonarcloud.io`
- EU v1: `https://sonarcloud.io/api`
- US v2: `https://api.sonarqube.us`
- US v1: `https://sonarqube.us/api`

Cloud plans change. Check plan before promising branch/PR/AI/remediation capabilities.

---

## Final-answer wording

When edition is unknown, include:

```markdown
SonarQube edition unknown. The delivered configuration stays baseline-compatible.
Features to verify before enabling: branch analysis, PR decoration, prioritized-rule gate, AI Code Assurance, AI CodeFix.
```

When a feature is edition-gated, include:

```markdown
This recommendation depends on the edition. If the instance is Community, keep the gate on main/new code and document the limitation.
```

