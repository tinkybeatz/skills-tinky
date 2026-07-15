# DOCUMENTOR — Annotated examples

Real input/output examples to calibrate the skill's behavior.
Each example includes the expected intermediate reasoning, the selected mode,
and the pitfalls to avoid.

---

## Example 1 — EU regulatory question

**Input:** "What is the current state of the European AI Act?"

**Mode:** 📋 Standard · **Audience:** internal use · **Language:** local + EN

**Generated research plan:**

1. What is the current legislative status (in force / in progress / proposal)?
2. What are the obligations for providers of high-risk systems?
3. What are the key application dates?
4. Are there differences in interpretation between member states?

**Targeted sources:** EUR-Lex, European Parliament, national data-protection authority, commission.europa.eu

**Expected output (structure):**

```
Executive summary
→ The AI Act entered into force in August 2024. Phased application through 2026.

Key points
→ [dated, sourced facts, separated from interpretations]

Ranked sources
→ 1. EUR-Lex — official text — https://... — [date] — Primary legislative source

Contradictions / limits
→ Interpretation of "high-risk systems" still debated between states.

Confidence: high for the legal text / medium for the application deadlines

Next steps → Monitor the Commission's delegated acts
```

**Annotation:** Systematically separate law in force / announcements / proposals.
Don't treat a Commission communication as an adopted legal text.

---

## Example 2 — Technical comparison of frameworks

**Input:** "What are the differences between LangGraph and CrewAI for multi-agent work?"

**Mode:** 📋 Standard · **Audience:** internal use · **Language:** EN first

**Generated research plan:**

1. What is each framework's fundamental architecture (graph vs. roles)?
2. What use cases do their respective authors recommend?
3. What limitations are documented in the GitHub issues and the community?
4. What is the maintenance activity (commits, releases, active contributors)?
5. Are there reproducible benchmarks comparing the two?

**Targeted sources:** official GitHub (LangChain-AI/langgraph, crewAIInc/crewAI),
technical docs, Towards Data Science, community benchmarks

**Expected output:**

- Comparative table by dimension: orchestration, memory, tooling, latency, learning curve
- Direct citations from the official documentation for each claim
- Explicit flagging of non-reproducible or self-published benchmarks

**Critical annotation:**
Never conclude "X is better than Y" in absolute terms.
Phrase it: "according to [dated source], X is better suited to [specific case] because [technical reason]".
Benchmarks published by the framework's own creators are weak sources (confirmation bias) —
flag them as such and complement them with independent sources.

---

## Example 3 — Scientific evaluation of an LLM (critical benchmark)

**Input:** "Is Claude 3.5 Sonnet really better than GPT-4o at coding tasks?"

**Mode:** 🔬 Deep · **Audience:** internal use · **Language:** EN

**Generated research plan:**

1. What standardized benchmarks exist for evaluating LLMs on code?
   (HumanEval, MBPP, SWE-bench, LiveCodeBench...)
2. What are the respective scores of Claude 3.5 Sonnet and GPT-4o on these benchmarks?
3. Have these benchmarks been reproduced independently (outside Anthropic/OpenAI)?
4. Do the benchmarks measure the same thing as real development tasks?
5. Are there human evaluations (human preference) on real coding tasks?
6. Are the test conditions comparable (temperature, prompting, context window)?

**Targeted sources:** Papers With Code, Arxiv, LMSYS Chatbot Arena,
GitHub (reproducible evals), EpochAI, independent reports (e.g. Scale AI HELM)

**Expected output:**

```
Executive summary
→ On HumanEval (Python), Claude 3.5 Sonnet reaches X% vs Y% for GPT-4o
  according to [source, date]. On SWE-bench (real tasks), the results
  reverse / confirm according to [independent source].

Key points
→ Distinguish: synthetic benchmark (HumanEval) vs. real task (SWE-bench)
→ Self-published Anthropic/OpenAI scores should be treated as weak sources
→ LMSYS Arena (human votes) gives a useful orthogonal measure

Contradictions
→ Results vary significantly depending on the prompting used —
  no benchmark controls this parameter uniformly.

Confidence: medium — the domain moves too fast for stable conclusions
```

**Critical annotation — pitfalls specific to this type of request:**

- Official leaderboards (Anthropic, OpenAI) are **primary but biased** sources —
  score them 20–25/30 on credibility, never 30/30
- A "state of the art" benchmark from September may be superseded by November —
  always check the publication date AND the version of the model tested
- Distinguish: "better on the benchmark" ≠ "better for my use case"
- If results are contradictory across independent sources → LOW confidence level mandatory,
  never fill the gap with a personal opinion

---

## Example 4 — Technology maturity assessment (TRL)

**Input:** "Is Anthropic's MCP (Model Context Protocol) ready for a production deployment at an industrial client?"

**Mode:** 🔬 Deep · **Audience:** end client (decision brief) · **Language:** EN + local

**Generated research plan:**

1. What is the current maturity level of the MCP protocol? (stable spec / draft / experimental)
2. Which MCP servers are available in production vs. experimental?
3. Which companies have deployed MCP in production? With what documented results?
4. What are the known and documented security limitations?
5. What is Anthropic's official roadmap and the cadence of breaking changes?
6. Are there comparable alternatives with equivalent or higher maturity?

**Targeted sources:** official MCP spec (modelcontextprotocol.io), GitHub anthropics/mcp,
changelogs, Hacker News posts (field feedback), engineering blogs of adopting companies

**Expected output (adapted to a client audience):**

```
Executive summary (plain language)
→ MCP is a protocol that lets Claude connect to your business tools.
  It is technically functional but still in a consolidation phase —
  suited to pilot projects, to be evaluated before critical deployment.

Key points
→ Spec v1.0 published [date] — breaking changes possible before v2.0
→ Official servers available: [sourced list]
→ No public documented feedback on critical industrial deployment to date

Contradictions / limits
→ Anthropic's messaging is enthusiastic but there is little independent field feedback
→ Security questions (prompt injection via MCP) are documented, not yet addressed
  by a dedicated security standard

Confidence: medium on maturity / high on the documented limitations

Recommendation (conditional, sourced)
→ A pilot phase is recommended before any critical deployment,
  based on the limitations documented in [source]
```

**Critical annotation:**
For client audiences, rephrase without jargon but without losing precision.
Recommendations MUST be conditional and sourced — never absolute assertions.
An unsourced "I think it's ready" is a skill failure.

---

## Example 5 — Contradictory sources (hard case)

**Input:** "Is fine-tuning more effective than RAG for proprietary data?"

**Mode:** 🔬 Deep · **Audience:** internal use · **Language:** EN

**Generated research plan:**

1. What studies directly compare fine-tuning and RAG on proprietary datasets?
2. On what dimensions is the comparison made? (accuracy, cost, latency, maintenance)
3. Are the studies reproducible, and on which base models?
4. What factors tip the recommendation one way or the other?
5. Is there consensus or an active debate in the literature?

**Expected behavior when facing contradictions:**

Sources will necessarily contradict each other on this topic — it's an active debate.
DOCUMENTOR must NOT arbitrarily pick a side. It must:

1. Map the positions: "RAG camp" vs. "fine-tuning camp" with their sourced arguments
2. Identify the **moderating variables**: dataset size, update frequency,
   compute budget, need for explainability
3. Produce a conditional **decision matrix**:

```
If [dataset > X examples] AND [stable data] → fine-tuning according to [source]
If [frequently updated data] AND [limited budget] → RAG according to [source]
If [need for source traceability] → RAG according to [source]
```

4. Conclude with a MEDIUM confidence level and an explicit justification

**Critical annotation — fundamental rule:**
A topic with contradictory sources of equivalent quality does not call for a
synthesis that "picks a side" — it calls for a mapping of the conditions.
Any non-conditional conclusion on this type of topic is a skill failure.

---

## Example 6 — Technology audit for a client brief

**Input:** "My retail client wants to automate customer service with an AI agent.
What solutions exist, what are the risks, and what do you recommend?"

**Mode:** 🔬 Deep · **Audience:** end client · **Language:** local (with EN sources)

**Generated research plan:**

1. What AI-agent solutions for customer service are available in 2025?
   (turnkey SaaS vs. custom)
2. What resolution rates are documented, and under what conditions?
3. What incidents / failures are publicly documented (Air Canada case, etc.)?
4. What are the legal obligations for a customer-facing AI agent?
   (GDPR, disclosure requirement, right to human recourse)
5. What is the real cost of deployment and maintenance (TCO)?
6. What criteria distinguish a retail-appropriate solution from a generic one?

**Expected behavior:**

- Don't limit yourself to well-known solutions — also look for independent comparisons
- Case studies published by vendors are weak sources (bias) —
  look for independent feedback (Gartner, Forrester if accessible, professional forums)
- The "Risks" section must be as substantial as the "Solutions" section
- Legal obligations are facts, not opinions — source them from primary sources

**Expected output (excerpt, risks section):**

```
Documented risks
→ Hallucination in a commercial context: [source + documented case]
→ Legal liability in case of an incorrect answer: [legal source]
→ Degraded customer experience if human escalation is mishandled: [study]
→ Underestimated maintenance cost: [independent TCO benchmark]
```

**Critical annotation:**
For a client brief, risks carry as much value as opportunities.
A deliverable that doesn't document them just as rigorously is incomplete.
DOCUMENTOR's role is not to sell a solution — it's to provide the elements
for an informed decision.

---

## Example 7 — Nonexistent sources (edge case)

**Input:** "What is the reliability benchmark for MCP agents in production in 2025?"

**Mode:** 📋 Standard · **Audience:** internal use · **Language:** EN

**Expected behavior:**
After 2 research cycles, no reliable source exists on this precise topic
(too recent, proprietary data, no established measurement standard).

**Expected output (compliant empty report):**

```
⚠️ Research unsuccessful

No reliable source (≥ 60/100) found after 2 research cycles on:
"reliability benchmark for MCP agents in production"

Identified reasons:
→ The MCP protocol is too recent to have generated independent
  reliability studies at this date
→ Production data is proprietary and unpublished
→ No reliability measurement standard for MCP agents exists to date

What does exist (weak sources, < 60/100):
→ Anecdotal feedback on forums (Hacker News, Reddit) — unsourced
→ Anthropic messaging about protocol stability — biased

Recommended alternatives:
→ Manually review the GitHub issues at anthropics/mcp (field feedback)
→ Contact documented early adopters (list in references/sources.md)
→ Reformulate as: "what metrics should be used to measure an MCP agent's reliability?"
   → a more tractable question with the existing sources

Confidence: N/A — deliberately empty deliverable
```

**Critical annotation — absolute rule:**
This case is a test of the skill's integrity.
Filling the absence of sources with plausible unsourced content is the worst
possible failure. An honest empty report is infinitely better than a confident
fabricated synthesis.

---

## Example 8 — Issue Tree + MECE decomposition

**Input:** "What are the stakes of agentic AI for an industrial SME?"

**Mode:** 📋 Standard · **Audience:** end client · **Language:** local + EN

**Generated Issue Tree:**

```
Stakes of agentic AI for an industrial SME
├── 1. Operational opportunities
│   ├── 1a. Business-process automation (production, logistics, quality)
│   └── 1b. Documented productivity gains (benchmarks, concrete cases)
├── 2. Technology maturity
│   ├── 2a. State of available frameworks and tools (LangGraph, CrewAI, AutoGen...)
│   └── 2b. Technical prerequisites (infrastructure, data, internal skills)
├── 3. Risks and limits
│   ├── 3a. Reliability and hallucinations in an industrial context
│   └── 3b. Vendor dependency and technology lock-in
├── 4. Regulatory framework
│   ├── 4a. AI Act — classification and obligations for agentic systems
│   └── 4b. Legal liability in case of an erroneous autonomous action
└── 5. Cost and ROI
    ├── 5a. Deployment and maintenance costs (TCO)
    └── 5b. Documented ROI on comparable cases
```

**MECE test applied:**

| Test                  | Result | Comment                                                                             |
| --------------------- | ------ | ----------------------------------------------------------------------------------- |
| Overlap 1a / 1b       | ✓ ME   | 1a = which processes, 1b = which gains → distinct angles                            |
| Overlap 3 / 4         | ✓ ME   | 3 = technical risks, 4 = legal risks → no overlap                                   |
| Exhaustiveness        | ✓ CE   | Opportunities + maturity + risks + regulation + cost = complete coverage            |
| Potential gap?        | ⚠️     | "Change management / human factor" might be missing → add if relevant               |

**Annotation:** The Issue Tree is built BEFORE the research. It guides the queries.
If the research reveals an unforeseen angle (e.g. the human factor), the tree is updated.
A good Issue Tree is a living document, not a frozen plan.

**Anti-pattern:** a "flat" research plan (a list of 7 questions with no hierarchy)
makes the synthesis harder — the results don't organize themselves naturally.
The tree structure forces structure from the start.
