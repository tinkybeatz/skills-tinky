# Detailed risk factors by change type

## Application code

| Factor | Impact on score | Rationale |
|---------|:---:|---|
| Number of modified files > 20 | +1 | More surface = more regression risk |
| Modifying "hot" files (recent incidents) | +2 | Fragile areas of the code |
| Test coverage < 30% on the diff | +2 | No safety net |
| Test coverage > 80% on the diff | -1 | Solid safety net |
| Refactoring with no functional change | -1 | Reduced risk if tests are green |
| New feature behind a feature flag | -2 | Gradual rollout, instant rollback |

## Database

| Factor | Impact on score | Rationale |
|---------|:---:|---|
| Destructive migration (DROP, ALTER DROP COLUMN) | +3 | Irreversible without a backup |
| Additive migration (ADD COLUMN, CREATE TABLE) | +0 | Generally safe, rollback = DROP |
| Data migration (bulk UPDATE) | +2 | Integrity risk, slow, potential lock |
| No tested reverse migration | +2 | Uncertain rollback |
| Migration tested in staging with the same volume | -1 | Pre-prod validation |

## Infrastructure / Docker / Traefik

| Factor | Impact on score | Rationale |
|---------|:---:|---|
| Port / routing change | +2 | Can cut off the service |
| Volume / persistence change | +2 | Risk of data loss |
| Base image update (node:20 → node:22) | +1 | Possible breaking changes |
| DNS / domain change | +2 | Slow propagation, hard to debug |
| Adding a new service | +1 | Extra complexity but isolated risk |
| Traefik labels change only | +0 | Low risk if the syntax is validated |

## Dependencies

| Factor | Impact on score | Rationale |
|---------|:---:|---|
| Major version bump (semver X.0.0) | +2 | Breaking changes by definition |
| Minor version bump (semver 0.X.0) | +0 | Backward compatible in theory |
| Patch version bump (semver 0.0.X) | -1 | Bug fix, improvement |
| Dependency with < 1000 GitHub stars | +1 | Less community validation |
| Security dependency (auth, crypto, session) | +1 | Impact on the attack surface |
| Lockfile fully regenerated (not just a diff) | +1 | Risk of transitive regression |

## Security / Auth

| Factor | Impact on score | Rationale |
|---------|:---:|---|
| Change to the authentication flow | +2 | Risk of locking users out |
| Cookie / session change | +2 | Existing sessions potentially invalidated |
| Adding/modifying CORS | +1 | Risk of blocking legitimate requests |
| Change to security headers | +1 | Can break integrations |
| Change to permissions / RBAC | +2 | Possible privilege escalation |

## Monitoring and observability

| Factor | Impact on score | Rationale |
|---------|:---:|---|
| Monitoring in place for the key metrics | -1 | Fast detection if there's a problem |
| Alerting configured on error rate / latency | -1 | Automatic notification |
| No monitoring on the affected service | +2 | Deploying blind |
| Health check endpoint available | -1 | Automatic rollback possible |
