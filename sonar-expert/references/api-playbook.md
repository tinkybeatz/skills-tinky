# SonarQube API Playbook

Use this reference when the user asks to create/update SonarQube projects, quality gates, quality profiles, new code definitions, or to automate SonarQube configuration. It is a safe operational checklist, not a guarantee that the target instance supports every endpoint.

Always prefer the target instance's API documentation:

```text
<SONAR_HOST_URL>/web_api
```

For SonarQube Cloud, use the Cloud docs because v1/v2 base URLs differ from Server:

- EU v2: `https://api.sonarcloud.io`
- EU v1: `https://sonarcloud.io/api`
- US v2: `https://api.sonarqube.us`
- US v1: `https://sonarqube.us/api`

Official endpoint families checked while creating this playbook:

- `api/qualitygates`: create/copy conditions, select gate for project, set default.
- `api/qualityprofiles`: copy, activate rules, bulk activate rules, associate project.
- `api/new_code_periods`: set/list/show/unset new code definition.
- `api/projects`: create/search/update project metadata.

---

## Safety rules

1. Never print or commit `SONAR_TOKEN`.
2. Use `curl -fS` so failed HTTP calls fail loudly.
3. Run read-only checks first.
4. Prefer copying `Sonar way` over creating from scratch when possible.
5. Do not delete gates, profiles or conditions unless explicitly requested.
6. If the API returns "insufficient privileges", stop and report the missing permission instead of retrying with guesses.
7. If the endpoint or parameter differs on the target instance, defer to `<SONAR_HOST_URL>/web_api`.

---

## Common environment

```bash
export SONAR_HOST_URL="https://sonarqube.example.com"
export SONAR_TOKEN="<redacted>"
export SONAR_PROJECT_KEY="org-repo-service"
export SONAR_PROJECT_NAME="Org Repo Service"
```

Auth pattern for SonarQube Server v1 APIs:

```bash
curl -fS -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/server/version"
```

---

## Read-only discovery

### Server version

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/server/version"
```

### Existing project

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/projects/search?projects=$SONAR_PROJECT_KEY"
```

### Current project quality gate

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/qualitygates/get_by_project?project=$SONAR_PROJECT_KEY"
```

### Quality gate status after analysis

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=$SONAR_PROJECT_KEY"
```

### Quality profiles

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/qualityprofiles/search"
```

### New code definition

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/new_code_periods/show?project=$SONAR_PROJECT_KEY"
```

---

## Project creation

Create the project only if it does not exist:

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/projects/create" \
  -d "project=$SONAR_PROJECT_KEY" \
  -d "name=$SONAR_PROJECT_NAME"
```

Notes:

- Some DevOps-platform-bound projects should be created/imported through platform integration endpoints instead of bare `api/projects/create`.
- If the repo uses SonarQube Cloud, check Cloud v2 APIs first.

---

## Quality gate playbook

### Option A - copy Sonar way

Use this for most custom gates:

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/qualitygates/copy" \
  -d "sourceName=Sonar way" \
  -d "name=standard-app"
```

Then review conditions in UI or via:

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/qualitygates/show?name=standard-app"
```

### Option B - create from scratch

Current SonarQube docs state custom gates can be created and conditions added via `api/qualitygates/create` and `api/qualitygates/create_condition`.

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/qualitygates/create" \
  -d "name=standard-app"
```

Add conditions only after checking exact metric keys on the target instance. Common condition intent:

- no new issues;
- all new security hotspots reviewed;
- new code coverage >= 80%;
- new code duplication <= 3%.

Do not hardcode metric keys blindly across versions. Confirm in `<SONAR_HOST_URL>/web_api/api/qualitygates` and the UI.

### Associate a project to a gate

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/qualitygates/select" \
  -d "gateName=standard-app" \
  -d "projectKey=$SONAR_PROJECT_KEY"
```

Permissions: `Administer Quality Gates` or project administration rights, depending on endpoint and instance.

---

## Quality profile playbook

### Find profiles

```bash
curl -fS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/qualityprofiles/search?language=ts"
```

Language keys vary by analyzer. Common examples: `js`, `ts`, `py`, `java`, `cs`, `go`, `cpp`.

### Copy a profile

Copy `Sonar way` only when customization is justified:

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/qualityprofiles/copy" \
  -d "fromKey=<source-profile-key>" \
  -d "toName=typescript-standard"
```

### Associate a project with a profile

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/qualityprofiles/add_project" \
  -d "key=<quality-profile-key>" \
  -d "project=$SONAR_PROJECT_KEY"
```

### Activate one rule

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/qualityprofiles/activate_rule" \
  -d "key=<quality-profile-key>" \
  -d "rule=<repository>:<rule-key>"
```

### Bulk activate rules

Use only with precise filters:

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/qualityprofiles/activate_rules" \
  -d "targetKey=<quality-profile-key>" \
  -d "languages=ts" \
  -d "tags=owasp-a1,cwe"
```

Confirm parameter names in the target instance. Bulk activation can create a noisy profile quickly.

---

## New code definition playbook

Set project-level new code definition:

```bash
curl -fS -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST_URL/api/new_code_periods/set" \
  -d "project=$SONAR_PROJECT_KEY" \
  -d "type=REFERENCE_BRANCH" \
  -d "value=main"
```

Other common types may include previous version or number of days depending on version. Confirm exact enum values in `<SONAR_HOST_URL>/web_api/api/new_code_periods/set`.

Use reference branch for PR/feature branch workflows. Use previous version for regular release/versioned projects. Avoid floating day windows for strict release governance unless the team understands the tradeoff.

---

## CI scanner wait for quality gate

For CLI scanner workflows, when appropriate:

```properties
sonar.qualitygate.wait=true
```

Use carefully:

- good for deployment-blocking stages;
- can slow CI if the SonarQube server is overloaded;
- Jenkins with SonarQube plugin may use `waitForQualityGate` instead.

---

## Final-answer wording

When API calls were not executed:

```markdown
I have not applied the changes on the SonarQube server: a token/admin or the target URL is missing.
I have provided the exact API playbook to run once permissions are validated.
```

When API calls were executed:

```markdown
Changes applied via the Web API:
- project created/verified;
- gate associated;
- profiles associated;
- new code definition configured.
```

When the API differs:

```markdown
The target instance exposes a different API variant. I stopped before any destructive change; check `<SONAR_HOST_URL>/web_api` for the exact parameters.
```
