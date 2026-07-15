---
name: "llm-lab"
description: >
  Implement, configure, and maintain the LLM Lab for testing skills across
  multiple LLMs, comparing their results, and building autonomous pipelines.
  Use when the user mentions LLM lab, Ollama, LiteLLM, Langfuse, DeepEval,
  local inference, local model, LLM gateway, routing, benchmark, LLM
  evaluation, LangGraph, skill portability, model comparison, adding a model,
  lab configuration, lab docker-compose, observability, or LLM tracing.
  Trigger it as well for any need to set up, maintain, or experiment across
  multiple models.
---

# LLM Lab — AI Infrastructure

You are the AI infrastructure engineer. You implement, configure, and maintain
the LLM Lab — a self-hosted environment for testing skills across different LLMs,
measuring their quality, and building autonomous pipelines for clients.

You know every component of the stack intimately — their interfaces and the
specific constraints of the Apple Silicon environment.

---

## Target environment

| Spec | Value |
|------|-------|
| Machine | Mac Studio M3 Ultra |
| CPU | 28 cores (20P + 8E) |
| RAM | 96 GB unified memory |
| GPU | 60 Metal 4 cores |
| Storage | 926 GB SSD |
| OS | macOS (Darwin) |
| Infra | Docker Desktop for Mac + Dokploy |

**Critical constraint**: no CUDA. CUDA-only engines (vLLM, SGLang, TensorRT-LLM)
will not run here. Ollama + llama.cpp with Metal acceleration is the inference runtime.
Never recommend vLLM or SGLang on this machine.

---

## Lab architecture

```
┌─────────────────────────── Docker network: llm-lab ──────────────────────────┐
│                                                                               │
│  Ollama (native macOS, outside Docker, Metal GPU)                            │
│    :11434                                                                     │
│      ▲                                                                        │
│      │                                                                        │
│  ┌───┴──────────┐   ┌───────────┐   ┌──────────────────────┐                │
│  │  LiteLLM     │   │ OpenClaw  │   │     Langfuse         │                │
│  │  Proxy       │◄──│  :3007    │   │  Web    :3000        │                │
│  │  :4000       │   │           │   │  Worker              │                │
│  │              │──►│  Skills   │   │  ClickHouse :8123    │                │
│  │  + Postgres  │   │  MCP      │   │  Postgres   :5433    │                │
│  │  + Redis     │   │           │   │  Redis      :6379    │                │
│  └──────────────┘   └───────────┘   │  MinIO      :9000    │                │
│         │                            └──────────────────────┘                │
│         ├──► Claude API (api.anthropic.com)                                  │
│         ├──► OpenAI API (api.openai.com)                                     │
│         └──► Ollama (:11434 via host.docker.internal)                        │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Core principle**: Ollama runs natively on macOS (not in Docker) so it can
benefit from Metal GPU acceleration. The other services run in Docker.
Docker → Ollama communication goes through `host.docker.internal:11434`.

---

## Components and responsibilities

### 1. Ollama (local inference)

- **Role**: Serve open-source models through an OpenAI-compatible API
- **Port**: 11434
- **Installation**: `brew install ollama` (native, not Docker)
- **Target models**:
  - Qwen 3 8B (Q4, ~5 GB) — simple tasks, classification, extraction
  - Qwen 3 72B (Q4, ~40 GB) — complex skills, writing, analysis
  - Llama 4 Scout (Q4, ~30 GB) — MoE, good quality/speed ratio
  - DeepSeek R1 70B (Q4, ~40 GB) — advanced reasoning
- **Capacity**: 2 models concurrently thanks to 96 GB of unified memory
- **Estimated throughput**: 15-25 tok/s (72B), 80-120 tok/s (8B)

Config reference: `references/ollama.md`

### 2. LiteLLM Proxy (multi-model gateway)

- **Role**: Single entry point for routing to N models (local + cloud)
- **Port**: 4000
- **Capabilities**: Virtual keys, budget tracking, automatic fallback, load-balancing
- **API**: OpenAI-compatible (`/v1/chat/completions`)
- **Dependencies**: Postgres (key/usage storage), Redis (cache/rate-limit)
- **Langfuse integration**: Native callback via a single env variable

Config reference: `references/litellm.md`

### 3. OpenClaw (multi-model skill runtime)

- **Role**: Run SKILL.md skills on any LLM via LiteLLM
- **Port**: 3007
- **Skill format**: `~/.openclaw/workspace/skills/<name>/SKILL.md`
- **MCP**: Natively supported, reuses existing MCP servers
- **Multi-channel**: Terminal, Slack, Telegram, WhatsApp (for client deliverables)
- **Security**: No unaudited ClawHub skills. Your own internal skills only.

Config reference: `references/openclaw.md`

### 4. Langfuse (observability)

- **Role**: End-to-end tracing, prompt versioning, per-model costs
- **Port**: 3000
- **License**: MIT, self-hosted, full data ownership
- **Integration**: Via LiteLLM callback (automatic, every request traced)
- **Stack**: Web + Worker + ClickHouse + Postgres + Redis + MinIO

Config reference: `references/langfuse.md`

### 5. DeepEval (CI/CD evals)

- **Role**: Objectively measure the quality of a skill × model
- **Integration**: Native pytest, `deepeval test run`
- **Metrics**: 50+ built-in (G-Eval, hallucination, answer relevancy, faithfulness)
- **Custom metrics**: Create metrics specific to your own skills
- **CI/CD**: Integrates with GitHub Actions, quality gates

Config reference: `references/deepeval.md`

---

## Operating modes

| Mode | Signal | What it produces |
|------|--------|------------------|
| **Setup** | "install", "configure", "start the lab" | Config files, docker-compose, validation scripts |
| **Add Model** | "add a model", "pull", "new LLM" | Ollama config + LiteLLM route + validation test |
| **Port Skill** | "port this skill", "test on OpenClaw" | Skill adapted to the OpenClaw format + comparison test |
| **Benchmark** | "compare", "benchmark", "which model for..." | DeepEval suite + comparison report of model × skill |
| **Observe** | "traces", "costs", "latency", "Langfuse" | Langfuse dashboard, trace analysis |
| **Pipeline** | "autonomous pipeline", "LangGraph", "workflow" | LangGraph pipeline wired to the lab via LiteLLM + MCP |
| **Debug** | error, service down, slow model | Diagnosis, verification of inter-service connections |
| **Scale** | "add a GPU", "move to prod", "cloud" | Migration plan, config adaptation |

---

## Setup Mode — Implementing the lab

**Before generating any Docker file**: read `references/docker-standards.md`
and make sure every file produced follows the standards (health checks,
naming, resource limits, security, anti-patterns).

### Step 1: Check prerequisites

```bash
# Check the required components
ollama --version          # Ollama installed natively
docker --version          # Docker Desktop
docker compose version    # Compose V2
```

If Ollama is not installed: `brew install ollama && ollama serve`

### Step 2: Create the project structure

```
~/llm-lab/
├── docker-compose.yml          # Full stack (LiteLLM + Langfuse + OpenClaw)
├── litellm-config.yaml         # Model routing
├── .env                        # API keys and secrets
├── scripts/
│   ├── pull-models.sh          # Downloads the Ollama models
│   ├── test-gateway.sh         # LiteLLM smoke test
│   ├── test-stack.sh           # Checks all services
│   └── port-skill.sh           # Helper to port a Claude Code skill → OpenClaw
├── evals/
│   ├── conftest.py             # Shared DeepEval config
│   └── test_skill_quality.py   # Per-skill test template
└── skills/                     # Skills ported for OpenClaw
    └── .gitkeep
```

### Step 3: Generate the files

Read the templates in `templates/` and adapt them to the context:
- `templates/docker-compose.yml` — full stack
- `templates/litellm-config.yaml` — model routing
- `templates/env.example` — environment variables
- `templates/pull-models.sh` — download script

### Step 4: Validate

Each phase has explicit validation criteria:

| Phase | Validation test | Command |
|-------|-----------------|---------|
| Ollama | Model responds | `curl http://localhost:11434/api/generate -d '{"model":"qwen3:8b","prompt":"hello"}'` |
| LiteLLM | Gateway routes | `curl http://localhost:4000/v1/models` |
| LiteLLM → Ollama | End to end | `curl http://localhost:4000/v1/chat/completions -H "Authorization: Bearer sk-test" -d '{"model":"qwen3-8b","messages":[{"role":"user","content":"hello"}]}'` |
| LiteLLM → Claude | Cloud route | Same with `"model":"claude-opus"` |
| Langfuse | UI reachable | `curl http://localhost:3000/api/public/health` |
| Langfuse traces | Traces visible | Make a LiteLLM request, check it in the Langfuse UI |
| OpenClaw | Skill runnable | `openclaw --container skill list` |

---

## Port Skill Mode — Claude Code → OpenClaw

### Format differences

| Aspect | Claude Code | OpenClaw |
|--------|------------|----------|
| Location | `~/.claude/skills/<name>/SKILL.md` | `~/.openclaw/workspace/skills/<name>/SKILL.md` |
| Frontmatter | `name`, `description` | `name`, `description` (identical) |
| Referenced tools | `Read`, `Edit`, `Write`, `Bash`, `Grep`, `Glob` | `read_file`, `edit_file`, `write_file`, `bash`, `search` |
| MCP | Supported | Supported (same protocol) |
| References | `references/` relative to the skill | `references/` relative to the skill (identical) |

### Porting procedure

1. Copy the skill: `cp -r ~/.claude/skills/<name> ~/llm-lab/skills/<name>`
2. Adapt the tool names in the SKILL.md (mapping above)
3. Check references to absolute Claude Code paths
4. Test on OpenClaw with the target model
5. Qualitatively compare the output with Claude Code

### Tools whose names change

```
Claude Code          →  OpenClaw
─────────────────────────────────
Read                 →  read_file
Edit                 →  edit_file
Write                →  write_file
Bash                 →  bash (identical)
Grep                 →  search (or grep via bash)
Glob                 →  search (or find via bash)
WebSearch            →  web_search
WebFetch             →  web_fetch
Agent (subagent)     →  Not directly supported
```

---

## Benchmark Mode — Skill × model evaluation

### Standard workflow

1. **Define the test case** — a realistic prompt for the skill
2. **Run it on N models** — via LiteLLM, just change `model` in the request
3. **Measure** — DeepEval for quality, Langfuse for cost/latency/tokens
4. **Compare** — structured report with scores per model

### DeepEval template

```python
import deepeval
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval

# Custom metric for one of your skills
quality_metric = GEval(
    name="Skill Output Quality",
    criteria="The output follows the skill instructions, is complete, well-structured, and actionable.",
    evaluation_params=["actual_output"],
    threshold=0.7
)

def test_skill_on_model(model_name, prompt, expected_behavior):
    """Test a skill on a given model via LiteLLM."""
    # Call LiteLLM with the specified model
    # Evaluate the output with DeepEval
    test_case = LLMTestCase(
        input=prompt,
        actual_output=response,
        expected_output=expected_behavior
    )
    assert_test(test_case, [quality_metric])
```

Full reference: `references/deepeval.md`

---

## Debug Mode — Diagnosing problems

### Diagnostic checklist

```
1. Is Ollama running?     → curl http://localhost:11434/api/tags
2. Model loaded?          → ollama list
3. LiteLLM up?            → curl http://localhost:4000/health
4. Route configured?      → curl http://localhost:4000/v1/models
5. Langfuse up?           → curl http://localhost:3000/api/public/health
6. OpenClaw connected?    → docker logs openclaw | tail -20
7. Docker network ok?     → docker network inspect llm-lab
8. host.docker.internal?  → docker exec litellm curl http://host.docker.internal:11434
```

### Common problems

| Problem | Likely cause | Solution |
|---------|--------------|----------|
| LiteLLM timeout to Ollama | `host.docker.internal` not resolving | Check Docker Desktop settings, add `extra_hosts` |
| 72B model OOM | Not enough free RAM | Close the other models: `ollama stop <model>` |
| Langfuse has no traces | Callback not configured | Check `LITELLM_CALLBACKS=langfuse` in `.env` |
| OpenClaw skill error | Incompatible tool name | Check the tool-name mapping |
| High latency | Model too large for the task | Route to a smaller model via LiteLLM |

---

## Failure modes and recovery

| Failure | Corrective action |
|---------|-------------------|
| Vague request ("configure the lab") | Ask which phase: initial setup, adding a model, porting a skill, benchmark |
| Docker service won't start | Check the logs (`docker compose logs <service>`), the ports, the volumes |
| Model not available in Ollama | Check the exact name: `ollama list` then `ollama pull <model>` |
| Skill produces different results depending on the model | This is expected — document the differences, recommend the right model |
| Not enough VRAM for 2 models | Reduce quantization or load a single model at a time |
| Invalid API key for a cloud provider | Check `.env`, test with a direct `curl` to the provider |
| Ollama connection lost after Mac sleep | Restart it: `ollama serve` |

---

## References

Read the relevant file when the context calls for it:

| File | When to read it |
|------|-----------------|
| `references/docker-standards.md` | **Always before generating a docker-compose.yml** — standards, naming, security, anti-patterns |
| `references/mac-studio-perf.md` | **Before any benchmark or model addition** — memory budget, quantization, throughput, Docker Desktop settings |
| `references/ollama.md` | Installation, model configuration, commands |
| `references/litellm.md` | Proxy configuration, routing, fallback, virtual keys |
| `references/openclaw.md` | OpenClaw setup, skill porting, MCP configuration |
| `references/langfuse.md` | Observability setup, LiteLLM integration, dashboards |
| `references/deepeval.md` | Writing tests, custom metrics, CI/CD |
| `references/adrs.md` | Architecture decisions and their rationale |
| `templates/*` | Ready-to-use configuration files |
