# Agent Patterns & Advanced Reference

This reference file contains detailed patterns for creating agents, advanced
frontmatter options, the full taxonomy of Claude Code extension points, and
real-world examples. Read this when creating agents or when the decision between
skill/agent/hook is unclear.

---

## Full Taxonomy of Claude Code Extension Points

Understanding where agents fit in the broader ecosystem prevents choosing the
wrong abstraction. Each extension point serves a distinct purpose:

| Component | Trigger | Context | Use Case |
|-----------|---------|---------|----------|
| **CLAUDE.md / AGENTS.md** | Always loaded, every session | Main conversation | Facts, rules, conventions — things Claude must always know |
| **Skills** | Auto (description match) or manual (`/slash`) | Main conversation or forked (`context: fork`) | Procedures, workflows, domain knowledge |
| **Agents** | Auto (Claude decides based on description) | **Isolated** subprocess, own context window | Parallel tasks, specialized analysis, restricted-tool work |
| **Commands** | Manual only (`/command-name`) | Main conversation | Legacy — now merged into skills with `user-invocable` |
| **Hooks** | Deterministic events (pre/post tool calls) | Shell script, no LLM | Linting, validation, notifications, format enforcement |
| **Rules** | Path-scoped, loaded when Claude touches matching files | Main conversation | File-specific conventions (e.g., "all files in /api/ must...") |

**Decision heuristic:**
- If the behavior should be **deterministic** (same input → same output, no judgment needed) → **Hook**
- If the behavior is a **fact or rule** Claude needs every session → **CLAUDE.md**
- If the behavior is a **procedure** the user or Claude triggers → **Skill**
- If the behavior needs **isolated execution** or **parallel processing** → **Agent**
- If the behavior only applies to **specific file paths** → **Rule** (`.claude/rules/`)

---

## Advanced Agent Frontmatter Options

Beyond the basics (name, description, model, color, tools), agents support:

### Tool Restriction Patterns

Restrict tools to the minimum needed for the agent's job. Common patterns:

```yaml
# Read-only analysis agent
tools: [Read, Glob, Grep]

# Code-writing agent (needs file access + execution)
tools: [Read, Write, Edit, Glob, Grep, Bash]

# Research agent (needs web access)
tools: [Read, Glob, Grep, WebSearch, WebFetch]

# Minimal agent (only reads files)
tools: [Read]
```

The principle of least privilege matters here because agents run autonomously.
A security audit agent shouldn't have Write access. A code review agent
shouldn't have Bash access. Limiting tools constrains the blast radius of
mistakes.

### Model Selection Strategy

```yaml
# Default: inherits from parent conversation
model: inherit

# Fast/cheap: exploration, search, summarization
model: sonnet

# High capability: complex reasoning, code generation, architecture
model: opus

# Ultra-fast: simple classification, routing, formatting
model: haiku
```

Rule of thumb: use `sonnet` for agents that **find** things (search, explore,
classify) and `inherit` or `opus` for agents that **create** things (write code,
design architectures, synthesize complex reports).

---

## Agent Architecture Patterns

### Pattern 1: Fan-Out / Fan-In

Multiple agents analyze different aspects in parallel, results are synthesized.

```
SKILL.md (orchestrator)
├── agents/security-checker.md    → checks for vulnerabilities
├── agents/performance-checker.md → checks for performance issues
├── agents/style-checker.md       → checks code style
└── (skill synthesizes all 3 reports into unified review)
```

**When to use:** Code review, multi-dimensional analysis, comprehensive audits.
Each agent gets the same input but applies a different lens.

### Pattern 2: Pipeline

Agents process data sequentially, each transforming the output of the previous.

```
SKILL.md (orchestrator)
├── agents/extractor.md   → extracts raw data from source
├── agents/transformer.md → normalizes and enriches data
└── agents/reporter.md    → generates final report
```

**When to use:** Data processing, document transformation, multi-stage workflows
where each stage has different tool needs or expertise.

### Pattern 3: Specialist Router

The skill routes to one of several specialized agents based on the input type.

```
SKILL.md (router — decides which agent to spawn)
├── agents/react-expert.md    → React-specific tasks
├── agents/python-expert.md   → Python-specific tasks
└── agents/infra-expert.md    → Infrastructure tasks
```

**When to use:** When a single skill covers a broad domain but the actual work
requires deep specialization. The skill reads enough context to route correctly,
then delegates to the right specialist.

### Pattern 4: Evaluator

One agent does work, another evaluates the quality independently.

```
SKILL.md (orchestrator)
├── agents/generator.md  → produces output
└── agents/evaluator.md  → grades the output blindly
```

**When to use:** When output quality is critical and self-evaluation isn't
reliable. The evaluator never sees the generator's instructions, only its output.

---

## Writing Agent Descriptions That Trigger Correctly

Agent descriptions use `<example>` blocks for triggering. The key difference
from skill descriptions: agents are spawned by Claude (not the user), so the
description must help Claude decide *during its reasoning* whether to delegate.

**Good pattern:**

```yaml
description: >-
  Use this agent when the task involves analyzing code for security
  vulnerabilities, checking for OWASP top 10 issues, or reviewing
  authentication/authorization logic. Spawn this agent instead of doing
  security analysis inline when the codebase is large (>5 files) or
  when the user explicitly asks for a security review.
  <example>User asks to review a PR for security issues</example>
  <example>User asks "is this authentication implementation secure?"</example>
  <example>Multiple files need security scanning before deployment</example>
```

**Key elements:**
1. **What the agent does** (first sentence)
2. **When to spawn it vs. doing the work inline** (the delegation threshold)
3. **2-4 concrete examples** with `<example>` tags

The delegation threshold is critical — without it, Claude might either always
delegate (wasting a subprocess for trivial questions) or never delegate
(doing complex work inline when isolation would be better).

---

## Agent System Prompt Best Practices

### Be Self-Contained

Agents don't see the main conversation. They receive:
- Their system prompt (the .md file body)
- A task description from the spawning context
- Access to their allowed tools

Everything the agent needs to understand its role, quality standards, and output
format must be in the system prompt or discoverable via tools.

### Define the Output Contract

The spawning skill/conversation needs to parse the agent's output. Be explicit:

```markdown
**Output Format:**
Return a JSON block with this structure:
\`\`\`json
{
  "findings": [
    {
      "severity": "high|medium|low",
      "location": "file:line",
      "description": "What's wrong",
      "suggestion": "How to fix it"
    }
  ],
  "summary": "One-paragraph overview",
  "pass": true|false
}
\`\`\`
```

### Include Stopping Conditions

Agents can loop indefinitely without explicit bounds:

```markdown
**Stopping conditions:**
- Stop scanning after processing all files matching the glob pattern
- Stop after 2 failed attempts at the same operation — report the blocker
- If no issues found after scanning all targets, return an empty findings array
  (don't invent problems to justify your existence)
```

### Size Guidelines

- **Ideal:** 500–3,000 characters for the system prompt
- **Maximum:** 10,000 characters
- **If exceeding 3,000:** Consider whether the agent is doing too much. Can it
  be split into two agents? Can reference material be moved to a file the agent
  reads via its tools?

---

## Real-World Examples

### Example: Code Review Skill + Agents

```
code-review/
├── SKILL.md                    # Orchestrates the review workflow
│   - Reads the PR diff
│   - Spawns 3 agents in parallel
│   - Synthesizes their reports
│   - Presents unified review to user
├── agents/
│   ├── correctness.md          # Checks logic, edge cases, bugs
│   ├── security.md             # OWASP checks, auth review, injection
│   └── maintainability.md      # Code clarity, naming, complexity
└── references/
    └── review-criteria.md      # Shared quality criteria
```

### Example: Research Skill + Agents

```
deep-research/
├── SKILL.md                    # User-facing, manages topic decomposition
│   - Breaks question into sub-questions
│   - Spawns research agents per sub-question
│   - Cross-references findings
│   - Produces final synthesis
├── agents/
│   ├── searcher.md             # Finds and scores sources (read-only)
│   └── fact-checker.md         # Corroborates claims across sources
└── references/
    └── source-tiers.md         # Source credibility hierarchy
```

---

## Common Mistakes

1. **Putting everything in one agent.** If an agent's system prompt exceeds
   3,000 chars, it's probably doing too many things. Split it.

2. **Forgetting tool restrictions.** An agent with all tools enabled is a
   liability. Always restrict to the minimum needed.

3. **No output contract.** If the spawning context can't parse the agent's
   output reliably, the whole pipeline breaks.

4. **Vague delegation threshold.** "Use this agent for complex tasks" — what's
   complex? Be specific about when to spawn vs. do inline.

5. **No stopping condition.** Agents that "keep going until done" can loop
   forever if their tools return unexpected results.

6. **Forgetting agents are isolated.** They don't see the main conversation,
   user preferences, or other agents' outputs. Pass everything they need
   through the task description or make it discoverable via tools.
