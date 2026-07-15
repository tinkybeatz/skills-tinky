# Standard: Multi-Claude Workflow

- **Status:** Active
- **Version:** 1.0.0
- **Owner:** Engineering Lead
- **Approvers:** Tech Lead
- **Effective date:** 2026-04-30
- **Last review date:** 2026-04-30

## Scope

Any repo on which **several Claude Code instances** operate in parallel (typical case: a developer launches 2-4 Claude instances simultaneously to parallelize dev work).

Out of scope: repos with a single active Claude instance at a time (standard workflow).

## Problem solved

Without isolation, several Claude instances operating on the **same working directory** create race conditions on:
- The git staging area (one Claude's `git add` sees another's files).
- The working tree (one Claude's `git checkout` or `git reset` wipes another's in-progress changes).
- HEAD (one Claude's branch switch affects all the others).

**Reference incident (2026-04-30)**: commit `70b7e67` on `master` of the `sapain-borne` repo — the message said "animate Segmented count" but the content was 798 lines of another Claude's backend agent module. Cause: staging area collision during `git commit`.

## Core decisions

1. **Isolation via `git worktree`** is the canonical solution (zero overhead vs clone, shares the `.git`).
2. **One branch per Claude/topic** — never two Claude instances on the same branch.
3. **Master is sacred** — no Claude instance pushes directly to master. PR mandatory.

---

## Normative rules

### MC-WF-01 — One Claude instance = one dedicated worktree

**Requirement:** Every Claude Code instance working on a repo in multi-Claude mode MUST operate from a dedicated `git worktree`, never from the repo's main working directory. `[SRC-001]`

**Rationale:** a worktree = an isolated working tree + staging area + HEAD, sharing the same `.git`. Eliminates 100% of working-tree race conditions.

**Enforcement:** human convention + setup script. If several Claude instances are launched without a worktree, the standard is violated.

**Setup pattern:**
```bash
# From the main repo
git worktree add ../<repo>-claude-A feat/claude-A
git worktree add ../<repo>-claude-B feat/claude-B

# Launch Claude from the worktree
cd ../<repo>-claude-A && claude
```

### MC-WF-02 — One branch per Claude/topic

**Requirement:** Each Claude worktree MUST check out a dedicated branch. The branch MUST follow the convention `feat/<topic>` or `feat/claude-<id>` when the topic is not known in advance. Two Claude instances MUST NOT work on the same branch simultaneously.

**Rationale:** makes it explicit in `git log` which Claude did what. Avoids merge conflicts between instances.

**Enforcement:** convention + regular `git branch --remotes` audit.

### MC-WF-03 — Master/main untouchable from a Claude instance

**Requirement:** No Claude instance MUST NOT push directly to `master` / `main`. Every merge to the main branch MUST go through a **PR review** (manual or automated).

**Rationale:** master is the integration point. A Claude that pushes directly bypasses review and creates conflicts if several do it.

**Enforcement:** GitHub branch protection on master (require PR + 1 review).

**Exception:** if the developer operates manually (not via Claude) on master, they take responsibility.

### MC-WF-04 — Explicit communication of in-progress tasks

**Requirement:** When launching several Claude instances in parallel, each Claude SHOULD receive an explicit brief of its scope (file/feature/module) to avoid touching the same areas of the code.

**Rationale:** even with a worktree, two Claude instances that modify the same file on different branches create inevitable merge conflicts.

**Enforcement:** human discipline. Announce the scope when launching each Claude.

### MC-WF-05 — Cleanup after merge

**Requirement:** After merging a Claude PR:
```bash
git worktree remove ../<repo>-claude-A
git branch -d feat/claude-A
git push origin --delete feat/claude-A
```

**Rationale:** abandoned worktrees pollute the filesystem and the repo (orphaned refs).

**Enforcement:** post-merge checklist.

### MC-WF-06 — Reproducible setup script

**Requirement:** Any repo in multi-Claude mode SHOULD include a `scripts/claude-worktree-setup.sh` script that automates creating a worktree with its associated branch.

**Rationale:** reduces setup friction, avoids human errors (wrong path, wrong branch).

**Enforcement:** presence of the script verified when onboarding a repo into multi-Claude mode.

**Minimal example:**
```bash
#!/usr/bin/env bash
# scripts/claude-worktree-setup.sh <claude-id>
set -euo pipefail
ID="${1:?usage: $0 <claude-id>}"
REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
BRANCH="feat/claude-$ID"
WORKTREE_PATH="../$REPO_NAME-claude-$ID"

git worktree add "$WORKTREE_PATH" -b "$BRANCH" 2>/dev/null \
  || git worktree add "$WORKTREE_PATH" "$BRANCH"

echo "✅ Worktree ready: $WORKTREE_PATH (branch: $BRANCH)"
echo "→ cd $WORKTREE_PATH && claude"
```

### MC-WF-07 — No concurrent git operations on the main repo

**Requirement:** When Claude instances operate from worktrees, destructive git operations (`reset --hard`, `checkout`, `stash`, `restore`) MUST NOT be run on the **main repo** if it is itself being used by a Claude instance. Prefer operations within the relevant worktree.

**Rationale:** `.git` is shared between worktrees. A `git reset --hard` on the main repo does not affect the worktrees, but a `git checkout` of a branch already checked out elsewhere **fails explicitly** (native git safety).

**Enforcement:** human discipline.

---

## Anti-patterns

| Anti-pattern | Symptom | Mitigation |
|---|---|---|
| 2+ Claude instances on the same working dir | Stage collisions, commits containing the wrong files | MC-WF-01 (worktrees) |
| `master` branch checked out in several worktrees | git refuses, explicit error | Branch each worktree elsewhere |
| Direct master push from a Claude instance | Bypasses PR, dirty integration | MC-WF-03 (branch protection) |
| Orphaned worktrees | `git worktree list` shows refs to manually deleted dirs | Regular `git worktree prune` |
| Several Claude instances on the same file (even via worktrees) | Merge conflicts | MC-WF-04 (explicit scope) |

---

## Enforcement summary

| Mechanism | Rules | Auto |
|---|---|---|
| GitHub branch protection on master | MC-WF-03 | Yes |
| Presence of `scripts/claude-worktree-setup.sh` | MC-WF-06 | Manual |
| `feat/claude-*` naming convention | MC-WF-02 | Manual |
| Regular `git worktree prune` | MC-WF-05 | Manual |
| Per-Claude scope discipline | MC-WF-04, 07 | Manual |

## Exceptions process

- Single-Claude session: this standard does not apply, use the classic git workflow.
- Urgent hotfix: the developer may operate directly on master without Claude (human responsibility assumed).

## Sources

- `[SRC-001]` Git documentation — git-worktree: https://git-scm.com/docs/git-worktree
- Reference incident: sapain-borne commit 70b7e67 (2026-04-30) — staging area collision between 2 Claude instances.
- Pattern used internally by Anthropic (Agent tool param `isolation: "worktree"`).

## Change log

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0.0 | 2026-04-30 | Team | Initial — triggered by the commit 70b7e67 incident on sapain-borne (staging area collision between parallel Claude instances). |
