# BRIEF-WRITER — Annotated examples

Examples of transforming a DOCUMENTOR report → client brief.
Each example shows the input (excerpt), the output, and annotations
explaining the transformation choices.

---

## Example A — Decision-maker client

### DOCUMENTOR input (excerpt)

```
Verified fact: The AI Act classifies AI systems into 4 risk tiers
(unacceptable, high, limited, minimal). High-risk systems must meet
obligations around transparency, data governance, and human oversight.
(EUR-Lex, Regulation 2024/1689, Art. 6-9)

Verified fact: The rollout is phased: bans since February 2025,
obligations for high-risk systems from August 2026. (EUR-Lex, Art. 113)

Derived recommendation: A startup using an LLM for customer scoring
probably falls into the "high-risk" category (Annex III, point 5b).
A compliance audit should be launched before mid-2026.
(Derived from: Annex III classification + Art. 113 timeline)

Assumption: The Commission's implementation guidelines, expected in
late 2025, may clarify the classification thresholds. Moderate confidence.

Overall confidence level: High
```

### Brief output — Decision-maker client

> **Your customer-scoring system will likely be classified "high-risk"
> under the AI Act. We recommend launching a compliance audit before
> mid-2026.**
>
> ### Context
>
> The European AI Act (in force since 2024) classifies AI systems into
> 4 risk tiers. The obligations for high-risk systems — transparency,
> data governance, human oversight — take effect in August 2026.
>
> ### Key findings
>
> - Your use case (LLM-based customer scoring) matches the criteria
>   for the "high-risk" category under Annex III of the regulation
> - The timeline is tight: 17 months before the August 2026 deadline
> - The Commission's guidelines, expected in late 2025, could adjust
>   the thresholds — but waiting would be risky
>
> ### Recommendation
>
> Launch an AI Act compliance audit in Q2 2026, covering:
> the classification of your systems, the gaps against the Annex III
> obligations, and a remediation plan.
>
> ### Risks
>
> - The exact classification depends on guidelines not yet published
> - Failing to meet the obligations exposes you to fines of up to
>   3% of global revenue
>
> ### Next steps
>
> 1. Map your AI systems and their use cases
> 2. Assess the likely classification of each
> 3. Plan the compliance audit
>
> ---
>
> _Detailed sources and methodology available in the full report._
> _Research conducted on 15 March 2026 — high confidence._

### Annotations

| Choice                                      | Rationale                                                                        |
| ------------------------------------------- | -------------------------------------------------------------------------------- |
| Recommendation up front (bold)              | Pyramid Principle — the decision-maker has the answer in the first line          |
| "will likely be classified", not "will be" | The report says "derived recommendation", not "verified fact" — keep the hedge   |
| No mention of EUR-Lex or articles           | Non-technical audience — legal references go in an appendix                      |
| "To be confirmed" omitted on the guidelines | The assumption is folded in as a hedge ("could adjust") with no visible label    |
| Length ~350 words                           | Within the decision-maker target (400-600 words max)                             |
| Fines mentioned under "Risks"               | A factual data point from the report, reworded as business impact               |

---

## Example B — Designer / stakeholder brief

### DOCUMENTOR input (excerpt)

```
Verified fact: Three approaches dominate design-system organization in
2026: Atomic Design (Brad Frost), components by feature, and tokens-first.
(Sources: Frost 2013+2024, Figma docs, Storybook docs)

Verified fact: Atomic Design remains the most documented and most adopted
in teams > 5 designers. (Sparkbox survey 2025, N=400+)

Derived recommendation: For a small team (< 5 designers), a tokens-first
approach with components by feature would be lighter than full Atomic
Design. (Derived from: team size + Atomic Design overhead)

Confidence level: Moderate (little data on small teams)
```

### Brief output — Designer brief

> • **Decision**: choose the design-system organization approach
>
> • **Context**: 3 possible approaches — Atomic Design, components by feature, tokens-first. Atomic Design is the standard for large teams (> 5 designers), but heavy for a team like ours.
>
> • **Options**:
>
> - Full Atomic Design — robust, well documented, but high overhead for < 5 designers
> - Tokens-first + components by feature — lighter, suited to small teams
> - Hybrid — tokens + partial atomic (atoms/molecules only)
>
> • **Recommendation**: tokens-first + components by feature
>
> • **Risk**: little documented experience with this approach for small teams — validate it in real use on 1 pilot project

### Annotations

| Choice                    | Rationale                                                    |
| ------------------------- | ------------------------------------------------------------ |
| 5 lines, bullet format    | Respects the stakeholder format (10-15 lines max)            |
| No sources                | Omitted by default for this type of brief                    |
| "validate it in real use" | The report's moderate confidence → turned into a concrete action |
| 3 options instead of 1    | The stakeholder brief presents the options, not just the rec |

---

## Example C — Sales proposal

### DOCUMENTOR input (excerpt)

```
Verified fact: 73% of French SMEs have no formalized AI strategy in
2026. (Bpifrance Le Lab, AI Barometer 2025, N=2000)

Verified fact: Companies that have deployed at least one AI agent on a
business process report a 15-30% productivity gain on that process.
(McKinsey Digital, "The State of AI", March 2025)

Derived recommendation: A logistics SME could automate the handling of
quote requests with an AI agent, with an estimated ROI in 3-6 months.
(Derived from: observed gains + average deployment cost)
```

### Brief output — Sales proposal

> ### Context
>
> Your sales team handles quote requests manually, a repetitive process
> that ties up 2 to 3 FTEs by your own estimate. 73% of French SMEs have
> not yet formalized their AI strategy (Bpifrance, 2025) — there's a window
> for a competitive lead.
>
> ### Problem
>
> Handling quotes manually creates response delays, data-entry errors,
> and a bottleneck during peak periods.
>
> ### Recommended approach
>
> Deploy an AI agent to handle quote requests, able to:
> extract the data from incoming requests, pre-fill quotes according to
> your pricing grid, and submit them for human validation.
>
> Companies that have deployed this type of agent report 15 to 30%
> productivity gains on the targeted process (McKinsey, 2025).
>
> ### Expected outcomes
>
> - 60-70% reduction in handling time
> - Estimated ROI in 3 to 6 months
> - Freeing up the sales team for higher-value work
>
> ### Next steps
>
> 1. Audit of the current process (1 week)
> 2. Prototype on a sample of quotes (2 weeks)
> 3. Deployment and training (2 weeks)

### Annotations

| Choice                                 | Rationale                                                     |
| -------------------------------------- | -------------------------------------------------------------- |
| Sources woven in as proof              | Proposal format — sources add credibility, they don't inform   |
| "(Bpifrance, 2025)" inline             | Just the name + date, no URL — this is a sales document        |
| ROI figures from the report kept       | Verified fact → direct statement                               |
| Context reworded in client language    | "2 to 3 FTEs" = a concrete rewrite, not DOCUMENTOR jargon      |
| Concrete timeline in next steps        | Commitment-oriented — the client knows what comes next         |

---

## Example D — Creative brief (GET-TO-BY)

### DOCUMENTOR input (excerpt)

```
Verified fact: 68% of IT decision-makers say the main barrier to adopting
agentic AI is a lack of trust in agent autonomy. (Gartner, "Agentic AI
Survey", January 2026, N=800)

Verified fact: Companies that have deployed successfully report that human
oversight (human-in-the-loop) is the #1 success factor.
(McKinsey Digital, March 2025)

Derived recommendation: The company's positioning should emphasize human
oversight as the differentiator, not the technology.
```

### Brief output — Creative brief

> **Background**: the company is launching a positioning campaign on agentic
> AI. The market is saturated with technology promises. Decision-makers
> are wary.
>
> **GET**: The technical director of a French SME, 35-50, who has read
> 20 articles on agentic AI and tells themselves "it sounds powerful
> but I don't trust a robot acting on its own inside my systems."
>
> **TO**: Get in touch with the company for an initial exploratory
> conversation about a specific use case in their organization.
>
> **BY**: The barrier isn't the technology — it's trust. 68% of IT
> decision-makers share exactly this fear. The deployments that work
> all have one thing in common: a human stays in the loop.
> The company doesn't sell autonomy, it sells augmented control.
>
> **Tone**: Reassuring but not condescending. Technical without being
> intimidating. The tone of an expert who listens, not who shows off.
>
> **Deliverables**: Landing page + 3 LinkedIn posts + 1 client case study

### Annotations

| Choice                                  | Rationale                                                                                                  |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| GET describes a person, not a segment   | "technical director who has read 20 articles" > "IT decision-maker, 35-50"                                 |
| BY = insight, not observation           | The observation would be "68% don't trust it". The insight is "the barrier is trust, not the tech"         |
| No visible sources                      | Creative brief — the source report is the record                                                           |
| Tone in one evocative sentence          | Creative direction, not a list of constraints                                                              |

---

## Example E — MECE vs non-MECE findings

### DOCUMENTOR input (excerpt)

```
Verified fact: Agentic AI can automate complex business processes involving
multiple decision steps. (McKinsey Digital, March 2025)

Verified fact: Multi-agent frameworks (LangGraph, CrewAI) are functional
but still consolidating — frequent breaking changes. (GitHub changelogs)

Verified fact: 68% of IT decision-makers cite lack of trust as the main
barrier to adoption. (Gartner, January 2026)

Verified fact: The cost of deploying an AI agent on a business process
is estimated between €15k and €80k depending on complexity. (Wavestone Benchmark 2025)

Verified fact: The AI Act classifies certain agentic systems as "high-risk"
if they make autonomous decisions affecting people. (EUR-Lex, Annex III)

Derived recommendation: An SME should start with a pilot project on a
non-critical process before considering a wide rollout.
```

### Output — NON-MECE findings (bad)

> ### Key findings
>
> - Agentic AI automates complex business processes
> - The tools are still immature (frequent breaking changes)
> - The technology is promising but companies hesitate
> - The cost varies with project complexity
> - Decision-makers lack trust
> - There are regulatory constraints to account for

### Why it's non-MECE

| Problem           | Bullet concerned                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------ |
| **Overlap**       | "companies hesitate" and "decision-makers lack trust" = same idea, stated twice            |
| **Vague**         | "the technology is promising" is not a factual finding                                     |
| **Gap**           | The cost (€15k-80k) is mentioned with no ROI or timeline — incomplete for deciding         |

### Output — MECE findings (correct)

> ### Key findings
>
> - **Capability**: agentic AI automates multi-step processes
>   — documented productivity gains of 15-30% on the targeted processes
> - **Maturity**: the frameworks exist (LangGraph, CrewAI) but are
>   consolidating — keep them to pilot projects
> - **Adoption**: 68% of IT decision-makers cite lack of trust as the
>   main barrier — human oversight is the #1 success factor
> - **Cost**: €15k to €80k per process, estimated ROI in 3-6 months
> - **Regulatory**: the AI Act classifies autonomous agents as "high-risk"
>   if decisions affect people — obligations from August 2026

### Annotations

| Choice                                       | Rationale                                                                              |
| -------------------------------------------- | -------------------------------------------------------------------------------------- |
| 5 bullets instead of 6                       | Duplicates merged → no lost info, better readability                                   |
| Bold labels (Capability, Maturity...)        | Makes the MECE structure visible — each bullet = a distinct axis                       |
| Figures folded into each bullet              | Each finding is self-contained — the decision-maker needn't cross-reference sections   |
| ME test: no fact falls into 2 bullets        | ✓ verified                                                                             |
| CE test: the whole report is covered         | ✓ verified                                                                             |

---

## Anti-example — What NOT to do

### A failed decision-maker brief

> As part of our in-depth analysis of the regulatory implications of the
> European AI Act (Regulation 2024/1689 of the European Parliament and of
> the Council of 13 June 2024), it should be noted that your customer-scoring
> system, which uses a Large Language Model (LLM) for automated creditworthiness
> assessment, could potentially be classified as a high-risk AI system under
> the criteria set out in Annex III, point 5(b) of the said regulation...

### Why it's failed

| Problem                                     | Rule violated                      |
| ------------------------------------------- | ---------------------------------- |
| "As part of" / "it should be noted"         | voice.md — forbidden phrasing      |
| Conclusion on line 4, not line 1            | Pyramid Principle not respected    |
| Unexplained legal jargon                    | Decision-maker audience = plain    |
| Legal references inline                     | Sources in an appendix for a decision-maker |
| Passive, impersonal tone                    | voice.md — active, not passive     |

---

> Last updated: March 2026
