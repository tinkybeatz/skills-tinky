# ADRs — LLM Lab architecture decisions

## ADR-001: Gateway = LiteLLM Proxy

**Status**: Accepted (2026-04-21)
**Context**: We need a single entry point to route requests to N models (local + cloud).

| Option | Strengths | Weaknesses |
|--------|-----------|------------|
| **LiteLLM Proxy** ✅ | Self-hosted, 100+ providers, budget tracking, automatic fallback, OSS | Requires Postgres + Redis |
| OpenRouter | Zero setup, 200+ models | Cloud-only, no data ownership, opaque routing |
| Custom code | Full control | Heavy maintenance, reinventing the wheel |

**Decision**: LiteLLM Proxy
**Rationale**: The only self-hosted option with intelligent routing. Postgres/Redis shared with Langfuse.
**Rollback trigger**: Proxy latency > 50ms p95, or a critical provider not supported.

---

## ADR-002: Skill runtime = OpenClaw

**Status**: Accepted (2026-04-21)
**Context**: Port the Claude Code SKILL.md skills to a multi-model runtime.

| Option | Strengths | Weaknesses |
|--------|-----------|------------|
| **OpenClaw** ✅ | Near-identical SKILL.md format, native MCP, multi-channel, 247K stars | Young (6 months), supply chain risk |
| Custom LangChain agents | Flexible, well documented | No native skill format, boilerplate |
| CrewAI | Role-based, fast | Abstraction too high, less prompting control |

**Decision**: OpenClaw
**Mitigations**: No ClawHub skills. Internal skills only. Pinned Docker version.
**Rollback trigger**: No release in 3 months, or the SKILL.md format diverges significantly.

---

## ADR-003: Observability = Langfuse self-hosted

**Status**: Accepted (2026-04-21)

| Option | Strengths | Weaknesses |
|--------|-----------|------------|
| **Langfuse** ✅ | MIT, Docker, data ownership, native LiteLLM integration | Eval = bring-your-own |
| LangSmith | Visual LangGraph debugging | Cloud-only, vendor lock-in |
| Arize Phoenix | OSS, drift detection | Fewer built-in eval metrics |

**Decision**: Langfuse
**Rollback trigger**: If LangGraph becomes central and LangSmith's visual debugging becomes essential.

---

## ADR-004: Evals = DeepEval + Promptfoo

**Status**: Accepted (2026-04-21)

| Option | Strengths | Weaknesses |
|--------|-----------|------------|
| **DeepEval** ✅ | Native pytest, 50+ metrics, OSS, custom metrics | No automatic PR comments |
| Braintrust | GitHub Action, PR comments | Self-host = enterprise only |
| Promptfoo | Red teaming, YAML | Acquired by OpenAI, uncertain future |

**Decision**: DeepEval (quality) + Promptfoo (security red teaming)

---

## ADR-005: Inference = Ollama native (not Docker)

**Status**: Accepted (2026-04-21)
**Context**: Mac Studio M3 Ultra, no CUDA.

| Option | Strengths | Weaknesses |
|--------|-----------|------------|
| **Ollama native macOS** ✅ | Metal GPU, 96 GB unified memory, zero friction | No CUDA, throughput < H100 |
| Ollama in Docker | Stack uniformity | No Metal GPU access, degraded performance |
| vLLM | Better throughput | CUDA-only, incompatible with Apple Silicon |

**Decision**: Ollama native on macOS
**Rationale**: The only way to exploit the 96 GB of unified memory and Metal 4 acceleration.
Docker → Ollama communication goes through `host.docker.internal:11434`.

---

## ADR-006: Pipeline orchestration = LangGraph (Phase 5, future)

**Status**: Proposed (2026-04-21) — Not implemented, planned for Phase 5

**Provisional decision**: LangGraph for complex autonomous pipelines
**Rationale**: Graph-based, audit trail, HITL, production-ready. Wired via LiteLLM + MCP.
**Activation condition**: When the lab is stable (Phases 1-4 validated) and a client use case requires it.
