# DOCUMENTOR — Test cases (Evals)

Test prompts to validate the skill's behavior after modification.
Each eval includes the expected behavior and the assertions to check.

---

## Eval 1 — Regulatory research

**Prompt:**

> "What is the current state of the AI Act in Europe? What are the obligations for a startup building a chatbot?"

**Expected behavior:**

- Research plan generated with ≥ 3 sub-questions
- Primary sources: EUR-Lex or europa.eu mandatory
- Clear distinction: text in force / application timeline / gray areas
- Complete output format (summary + key points + sources + confidence)

**Assertions:**

- [ ] The executive summary is between 5 and 10 lines
- [ ] At least 1 official EU source cited with URL
- [ ] The confidence level is justified
- [ ] Chatbot-specific obligations are separated from generalities

---

## Eval 2 — Technical comparison

**Prompt:**

> "Compare LangGraph and CrewAI for building a multi-agent system in Python. Which should I choose for a complex agentic architecture?"

**Expected behavior:**

- At least 3 sources: official docs for each framework + 1 benchmark or comparative article
- Clear comparative table or structure
- No recommendation without a supporting source
- Flagging of known limitations

**Assertions:**

- [ ] Both frameworks are documented with their official URLs
- [ ] The final recommendation is conditioned on a use case, not absolute
- [ ] Limitations are listed for each option
- [ ] The source dates are mentioned (fast-moving domain)

---

## Eval 3 — Market monitoring

**Prompt:**

> "Monitor the agentic AI agencies in the market in 2025. Who are the players and how are they positioned?"

**Expected behavior:**

- Multi-channel research (LinkedIn, freelance marketplaces, tech press)
- List of players with differentiated positioning
- Flagging of uncertainty if few direct sources
- Contradictions section if positioning is unclear

**Assertions:**

- [ ] At least 5 players identified with sources
- [ ] Distinction made between natively agentic vs. repositioned agencies
- [ ] Confidence level "medium" or justified if sources are limited
- [ ] Next steps suggested if the monitoring is incomplete

---

## Eval 4 — Vague request (reformulation test)

**Prompt:**

> "Tell me everything about RAG."

**Expected behavior:**

- The skill must reformulate the request into sub-questions before searching
- Ask for or infer the context: RAG for what use? level of detail?
- Don't produce a generic course without factual, sourced grounding

**Assertions:**

- [ ] Research plan with sub-questions generated before the results
- [ ] No unsourced content presented as established fact
- [ ] Next steps or an invitation to clarify if a generic answer is unavoidable

---

## Evaluation procedure

For each eval:

1. Run the skill with the exact prompt
2. Check each assertion (✅ / ❌)
3. Compute the rubric score out of 100
4. If the score < 80 → identify the cause and adjust `SKILL.md`
5. Rerun until all evals pass with a score ≥ 80

**Recommended frequency:** after every major change to `SKILL.md`
