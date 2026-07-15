---
name: "skill-creator"
description: "Create new skills, create agents, modify and improve existing skills or agents, and measure their performance. Use when users want to create a skill or agent from scratch, edit or optimize an existing skill or agent, run evals to test a skill, benchmark skill performance with variance analysis, optimize a skill's description for better triggering accuracy, or when the user mentions \"create a skill\", \"create an agent\", \"make a skill\", \"write a skill\", \"improve this skill\", \"agent creation\", \"subagent\", even if they don't explicitly use those exact terms."
---

# Skill & Agent Creator

A skill for creating new skills and agents, and iteratively improving them.

At a high level, the process goes like this:

- Decide what you want it to do and whether it should be a **skill** or an **agent** (see decision framework below)
- Write a draft
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While runs happen in the background, draft quantitative evals. Use `eval-viewer/generate_review.py` to show results to the user.
- Rewrite based on feedback
- Repeat until satisfied
- Expand the test set and try again at larger scale

Your job is to figure out where the user is in this process and help them progress. Be flexible — if the user says "just vibe with me", skip the formal eval loop.

After the skill is done, you can run the description optimizer (see `references/description-optimization.md`).

---

## Constraint Validation & Automatic Refactoring

Every skill or agent you create or modify must respect these constraints. When any constraint is violated, **refactor immediately** — don't deliver non-compliant output and don't wait for the user to notice.

| Constraint | Threshold | Action when violated |
|-----------|-----------|---------------------|
| SKILL.md line count | < 500 lines | Extract sections to `references/` with clear pointers |
| Description length | < 1,536 chars | Compress trigger phrases, remove redundancy |
| Agent system prompt | < 3,000 words (ideal < 10,000 chars) | Split agent or move reference material to external files |
| Name format | 3-50 chars, lowercase-hyphens, alphanumeric start/end | Fix immediately |
| Progressive disclosure | Core workflow fits in ~5,000 tokens | Move detailed content to references/ |
| Failure modes section | Must exist in every skill | Add before delivering |
| Output contract | Must be defined for every agent | Add before delivering |
| Stopping conditions | Must be defined for every agent | Add before delivering |

**The refactoring rule**: after writing or modifying any skill/agent, re-read it and verify each constraint above. If any is violated, refactor before presenting the result to the user. This is not optional — a skill that violates its own constraints teaches bad patterns to every future user. When refactoring, prefer extracting to `references/` over deleting content.

---

## Skill vs Agent — Decision Framework

Before writing anything, determine whether the user needs a **skill** or an **agent** (or both).

### Quick decision table

| Signal | → Skill | → Agent |
|--------|---------|---------|
| User says "turn this into a command" | x | |
| User needs a slash command trigger | x | |
| Task requires back-and-forth with user | x | |
| Task should run silently in background | | x |
| Multiple parallel analyses needed | | x |
| Tool access should be restricted | | x |
| Heavy context that would pollute main conversation | | x |
| Orchestrator + workers pattern | Both | Both |

**Skill** = enriches main conversation. Progressive loading. User or Claude invokes it.
**Agent** = autonomous isolated subprocess. Own context window. Claude spawns it.
**Both** = skill orchestrates, agents handle subtasks in parallel.

Read `references/agent-patterns.md` for detailed architecture patterns and the full taxonomy (skill vs agent vs hook vs rule).

---

## Communicating with the user

Pay attention to context cues — adjust jargon to the user's level. "evaluation" and "benchmark" are borderline OK. For "JSON" and "assertion", look for cues that the user knows what those are before using them without explaining.

---

## Creating a skill

### Capture Intent

Extract answers from the conversation history first if a workflow is already visible. Then confirm:

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases? (suggest based on skill type, let user decide)

### Interview and Research

Ask about edge cases, input/output formats, example files, success criteria, dependencies. Fill in the **Theme Adaptation Matrix**:

| Field | What to capture |
|-------|----------------|
| **Theme** | Domain name |
| **Typical questions** | 3-7 recurring user prompts |
| **Priority sources** | Where to look first |
| **Major risks** | 3-5 things that can go wrong |
| **Quality threshold** | Minimum acceptable bar |

### Write the SKILL.md

**Frontmatter:**
- **name**: Skill identifier (kebab-case, 3-50 chars)
- **description**: Trigger mechanism. Be pushy — Claude undertriggers. Include exact phrases users would say, edge-case triggers, and competing skill boundaries. Use third person.
- **compatibility**: Required tools/deps (optional, rarely needed)

**Skill anatomy:**
```
skill-name/
├── SKILL.md (required, <500 lines)
├── scripts/    - Deterministic code (execute without loading)
├── references/ - Docs loaded on demand
└── assets/     - Templates, icons, fonts
```

**Progressive disclosure:** Metadata always loaded (~100 words) → SKILL.md body on trigger (<5k words) → references on demand (unlimited). After compaction, only the 5 most recent skills survive (5k tokens each). Keep core workflow within that budget.

**Writing style:** Explain the *why* behind instructions. Prefer imperative form. Avoid heavy-handed MUSTs — reframe as reasoning. Start with a draft, then review with fresh eyes.

**Failure modes:** Every skill needs a failure → recovery table. Use risks from the Theme Adaptation Matrix + universal failures (vague request, missing input, format mismatch, looping, dependency unavailable). Read `references/context-management.md` for anti-drift patterns.

---

## Creating an Agent

Agents live as `.md` files in `agents/` directories. Read `references/agent-patterns.md` for the full guide. Key essentials:

**Frontmatter (all required):**
```yaml
---
name: agent-identifier           # 3-50 chars, lowercase-hyphens
description: >-                  # Triggering conditions + 2-4 <example> blocks
  Use this agent when [context].
  <example>Scenario 1</example>
  <example>Scenario 2</example>
model: inherit                   # inherit | sonnet | opus | haiku
color: blue                      # blue | cyan | green | yellow | magenta | red
tools: [Read, Grep, Glob]       # Optional: restrict to minimum needed
---
```

**System prompt essentials:**
1. **Self-contained** — agents don't see the main conversation
2. **Output contract** — exact structure of what to return (the spawner must parse it)
3. **Stopping conditions** — when to stop ("after 2 failed attempts", "when all files scanned")
4. **Keep under 3,000 words** — no progressive disclosure for agents

**Orchestration pattern:**
```
my-capability/
├── SKILL.md           # Orchestrator (user-facing)
├── agents/            # Workers (isolated)
└── references/        # Shared knowledge
```

---

## Test Cases

After writing the draft, propose 2-3 realistic test prompts. Save to `evals/evals.json`. See `references/schemas.md` for the full schema.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {"id": 1, "prompt": "User's task prompt", "expected_output": "Description", "files": []}
  ]
}
```

## Running and evaluating test cases

This is one continuous sequence — don't stop partway through. Do NOT use `/skill-test`.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory, organized by iteration (`iteration-1/`, `iteration-2/`).

### Step 1: Spawn all runs in the same turn

For each test case, spawn two subagents simultaneously — one with-skill, one baseline.

**With-skill:** `Skill path → Task → Save outputs to workspace/iteration-N/eval-ID/with_skill/outputs/`

**Baseline:** Creating new = no skill. Improving existing = snapshot old version first.

Write `eval_metadata.json` for each test case with descriptive names.

### Step 2: Draft assertions while runs are in progress

Draft objectively verifiable assertions with descriptive names. Update `eval_metadata.json` and `evals/evals.json`. Don't force assertions on subjective skills.

### Step 3: Capture timing data as runs complete

Save `total_tokens` and `duration_ms` from task notifications to `timing.json` immediately — this data isn't persisted elsewhere.

### Step 4: Grade, aggregate, launch viewer

1. **Grade** — spawn grader (`agents/grader.md`). Save `grading.json` with `{text, passed, evidence}` fields.
2. **Aggregate** — `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`
3. **Analyst pass** — see `agents/analyzer.md` for what to look for
4. **Launch viewer:**
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json > /dev/null 2>&1 &
   ```
   For iteration 2+, add `--previous-workspace`. For headless: use `--static <path>`.

### Step 5: Read feedback

Read `feedback.json`. Empty feedback = user was satisfied. Focus improvements on specific complaints.

---

## Improving the skill

1. **Generalize from feedback.** Don't overfit to test cases. If a change only helps one example, rethink it.
2. **Keep the prompt lean.** Read transcripts — if the skill wastes time on unproductive steps, cut those instructions.
3. **Explain the why.** Reasoning > rigid rules. If you're writing ALWAYS/NEVER in caps, reframe as explanation.
4. **Bundle repeated work.** If all test runs independently wrote similar scripts, bundle that script in `scripts/`.

### The iteration loop

1. Apply improvements → 2. Rerun tests in `iteration-N+1/` → 3. Launch reviewer with `--previous-workspace` → 4. Read feedback → 5. Repeat until happy or no progress.

---

## Description Optimization

After creating or improving a skill, offer to optimize its description for better triggering accuracy. Read `references/description-optimization.md` for the full 4-step workflow (generate eval queries → review with user → run optimization loop → apply result).

---

## Package and Present

If `present_files` tool is available, package and present:
```bash
python -m scripts.package_skill <path/to/skill-folder>
```

---

## Advanced: Blind comparison

For rigorous A/B comparison between skill versions, read `agents/comparator.md` and `agents/analyzer.md`. Optional — human review is usually sufficient.

---

## Platform-specific instructions

For **Claude.ai** or **Cowork** environments, read `references/platform-guides.md` — it covers how to adapt the workflow when subagents, browsers, or CLI tools aren't available.

---

## Reference files

| File | When to read |
|------|-------------|
| `agents/grader.md` | Evaluating assertions against outputs |
| `agents/comparator.md` | Blind A/B comparison between outputs |
| `agents/analyzer.md` | Analyzing why one version beat another |
| `references/schemas.md` | JSON structures for evals, grading, benchmarks |
| `references/agent-patterns.md` | Agent architecture, frontmatter, taxonomy, examples |
| `references/context-management.md` | Progressive disclosure, anti-drift, bridge pattern |
| `references/description-optimization.md` | Full description optimization workflow |
| `references/platform-guides.md` | Claude.ai and Cowork adaptations |

---

Core loop reminder:

1. Figure out what the skill/agent is about
2. Draft or edit it — **validate constraints before delivering**
3. Run test prompts → generate viewer → get human feedback
4. Improve → repeat
5. Package and return

Good luck!
