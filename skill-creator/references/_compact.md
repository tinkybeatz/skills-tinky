# Skill Creator — Compact Reference

## Extension Point Taxonomy

| Component | Trigger | Context | Use Case |
|-----------|---------|---------|----------|
| CLAUDE.md / AGENTS.md | Always loaded | Main conversation | Facts, rules, conventions |
| Skills | Auto (description match) or `/slash` | Main or forked (`context: fork`) | Procedures, workflows, domain knowledge |
| Agents | Auto (Claude decides) | Isolated subprocess | Parallel tasks, specialized analysis, restricted-tool work |
| Hooks | Deterministic events (pre/post tool) | Shell script, no LLM | Linting, validation, notifications |
| Rules | Path-scoped | Main conversation | File-specific conventions |

### Decision Heuristic

- Deterministic (same in -> same out) -> **Hook**
- Fact/rule needed every session -> **CLAUDE.md**
- Procedure user/Claude triggers -> **Skill**
- Isolated/parallel execution -> **Agent**
- Specific file paths only -> **Rule**

## Agent Frontmatter

### Tool Restriction Patterns

| Profile | Tools |
|---------|-------|
| Read-only analysis | `[Read, Glob, Grep]` |
| Code-writing | `[Read, Write, Edit, Glob, Grep, Bash]` |
| Research | `[Read, Glob, Grep, WebSearch, WebFetch]` |
| Minimal | `[Read]` |

### Model Selection

| Model | Use For |
|-------|---------|
| `haiku` | Classification, routing, formatting |
| `sonnet` | Search, exploration, summarization |
| `opus` / `inherit` | Complex reasoning, code generation, architecture |

Rule: `sonnet` for agents that **find**; `inherit`/`opus` for agents that **create**.

## Agent Architecture Patterns

| Pattern | Structure | When |
|---------|-----------|------|
| Fan-Out/Fan-In | N agents analyze in parallel, skill synthesizes | Multi-dimensional analysis, audits |
| Pipeline | Sequential agents, each transforms previous output | Data processing, multi-stage workflows |
| Specialist Router | Skill routes to one specialized agent | Broad domain with deep specialization needed |
| Evaluator | Generator + independent evaluator | Quality-critical output |

## Agent System Prompt Rules

- MUST be self-contained (agents don't see main conversation)
- MUST define output contract (parseable format)
- MUST include stopping conditions
- Size: 500-3000 chars ideal, 10000 max
- If >3000 chars: split into two agents or move references to files

## Agent Description Format

```yaml
description: >-
  [What it does]. [When to spawn vs inline].
  <example>Scenario 1</example>
  <example>Scenario 2</example>
```

Must include: (1) what agent does, (2) delegation threshold, (3) 2-4 `<example>` blocks.

## Context Management — Token Budget

| Layer | When Loaded | Budget | Content |
|-------|-------------|--------|---------|
| Description | Every session | ~100 words / 1536 chars max | Trigger conditions, key phrases |
| SKILL.md body | On trigger | <500 lines / <5k words | Core workflow, decision logic, output format |
| references/ | On demand | Unlimited | Patterns, examples, schemas |
| scripts/ | Execute only | Unlimited | Deterministic code, validators |

After compaction: CLAUDE.md re-read + 5 most recent skills re-attached (5000 tokens each, 25000 combined).

## Description Optimization Rules

1. Include exact trigger phrases users would type
2. Be pushy (Claude undertriggers)
3. Cover edge cases and non-obvious triggers
4. Name competing skills with boundaries
5. Use third person
6. For agents: use `<example>` blocks instead of free-text

## Anti-Drift Checklist

- [ ] Separate facts (references/) from procedures (SKILL.md)
- [ ] Date-stamp volatile content
- [ ] Include "what this skill does NOT do" section
- [ ] Run evals periodically on existing skills
- [ ] Prune: if removing a line wouldn't cause mistakes, cut it

## evals.json Schema

```json
{
  "skill_name": "string",
  "evals": [{
    "id": "integer (unique)",
    "prompt": "string (task to execute)",
    "expected_output": "string (success description)",
    "files": ["optional file paths"],
    "expectations": ["verifiable statements"]
  }]
}
```

## grading.json Schema

```json
{
  "expectations": [{"text":"string", "passed":"bool", "evidence":"string"}],
  "summary": {"passed":"int", "failed":"int", "total":"int", "pass_rate":"float"},
  "execution_metrics": {"tool_calls":{}, "total_tool_calls":"int", "total_steps":"int", "errors_encountered":"int"},
  "timing": {"executor_duration_seconds":"float", "grader_duration_seconds":"float", "total_duration_seconds":"float"},
  "claims": [{"claim":"string", "type":"string", "verified":"bool", "evidence":"string"}]
}
```

## comparison.json Schema

```json
{
  "winner": "A|B",
  "reasoning": "string",
  "rubric": {"A|B": {"content":{"correctness":1-5,"completeness":1-5,"accuracy":1-5}, "structure":{"organization":1-5,"formatting":1-5,"usability":1-5}, "content_score":"float", "structure_score":"float", "overall_score":"float"}},
  "expectation_results": {"A|B": {"passed":"int","total":"int","pass_rate":"float"}}
}
```

## benchmark.json Critical Fields

- `runs[].configuration`: MUST be `"with_skill"` or `"without_skill"` (viewer key)
- `runs[].result`: Nested object with `pass_rate`, `passed`, `total`, `time_seconds`, `tokens`, `errors`
- `run_summary.{with,without}_skill.{pass_rate,time_seconds,tokens}`: Objects with `mean`, `stddev`, `min`, `max`
- `run_summary.delta`: Difference strings like `"+0.50"`

## Description Optimization Workflow

1. Generate 20 trigger eval queries (8-10 should-trigger + 8-10 should-not-trigger, realistic, detailed, edge-case focused)
2. Review with user via HTML template (`assets/eval_review.html`)
3. Run optimization: `python -m scripts.run_loop --eval-set <path> --skill-path <path> --model <model-id> --max-iterations 5 --verbose`
4. Apply `best_description` to SKILL.md frontmatter

## Common Mistakes

1. Agent system prompt >3000 chars = doing too much
2. Agent with all tools enabled = liability
3. No output contract = pipeline breaks
4. Vague delegation threshold
5. No stopping condition = infinite loop risk
6. Forgetting agents are isolated from main conversation
