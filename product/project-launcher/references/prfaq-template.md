# Working Backwards — PR/FAQ Template

Primary source: Colin Bryar & Bill Carr, *Working Backwards* (2021). https://workingbackwards.com/concepts/working-backwards-pr-faq-process/

The method used for AWS, Kindle, Prime Video, and most Amazon products since 2004.

---

## Principle

**Write the press release and the FAQ BEFORE writing code.**

Forcing function: if you can't write the PR in a convincing way, the product isn't ready to be designed — let alone built. The PR forces you to take the customer's side, not the technical stack's side.

**Strict format:**
- PR ≤ 1 page
- FAQ ≤ 5 pages

---

## PR structure (1 page)

```
[TITLE — 1 line, the customer benefit in plain words]

[SUBTITLE — 1 sentence, the target audience]

[CITY, FUTURE DATE] — [Company/team name] today announces [product/feature],
[a clear one-sentence description].

## The problem
[2-3 sentences. What real pain, experienced by whom, in what context. Ideally
quotes from the Mom Test interviews.]

## The solution
[2-3 sentences. How the product solves the problem — benefit, not feature.
No technical jargon.]

## Leadership quote
"[Quote attributed to the CEO/founder, 2 sentences, on why now.]"

## Customer quote
"[Quote attributed to a REAL customer — not invented. If you don't have a
customer yet, go back to Phase 1.]"
— [Name, role, company]

## How to get started
[1 sentence + URL. Minimal friction.]
```

**If you can't fill the "Customer quote" with a real customer** → you haven't finished Phase 1. Stop.

---

## FAQ structure (≤ 5 pages)

Two mandatory sections:

### Customer-facing FAQ (≤ 2 pages)

Questions a customer would ask after reading the PR.

- Who exactly is it for?
- How much does it cost and how is it priced?
- How does it compare to [competitor / existing tool]?
- Is it compatible with [the customer's typical stack/ecosystem]?
- How do I integrate it into my current workflow?
- What are the known limitations?
- Is it secure / GDPR-compliant?

### Internal-facing FAQ (≤ 3 pages)

Questions the team / board / investors ask.

- What's the estimated P&L at 12/24 months?
- What are the critical assumptions (about the market, the cost of delivery)?
- What are the risks (Cagan: value, usability, feasibility, viability)?
- What's the technical dependency (LLM models, third-party APIs, infra)?
- Who on the team is accountable?
- What's the kill criterion? (If X doesn't happen within Y weeks → stop)
- What's the maximum investment allowed before a reassessment gate?

---

## Condensed example (internal product mode)

```
## [Company] launches CRM Co-Pilot, the AI agent that automates sales follow-ups
## For founders of tech SMBs who spend 5h/week on manual follow-ups

[CITY], OCTOBER 15, 2026 — [Company] today announces CRM Co-Pilot, an AI agent
that reads your CRM, identifies the leads to follow up with, and sends
contextualized messages on your behalf — with human validation.

## The problem
The founders of tech SMBs (5-30 people) we interviewed spend an average of
4-7h/week triaging their pipeline and writing follow-ups. "I know I should
have followed up with Marc three weeks ago, but I never have the time."
— Pierre, founder of a B2B SaaS, 12 people.

## The solution
CRM Co-Pilot plugs into HubSpot/Pipedrive, identifies "warm" leads according
to rules you define, writes the follow-up in your tone, and lets you validate
or edit it with 1 click. 30 seconds per lead instead of 10 minutes.

"Our conviction: founders don't want a new tool, they want to get back 5 hours
a week. CRM Co-Pilot does that by removing the friction between 'knowing you
need to follow up' and 'sending the follow-up'." — [Founder], founder.

"In 3 weeks with CRM Co-Pilot, we made 40 extra follow-ups and closed 3 deals
we'd have lost. I'm not going back." — Pierre F., founder of a tech SMB.

Available in private beta at [product-url].
```

---

## Checklist before validating Phase 0

- [ ] Can a non-technical person read the title in 5 seconds?
- [ ] Is the customer quote real (from a Mom Test interview)?
- [ ] Does the Customer FAQ answer the 3 questions a skeptic would ask first?
- [ ] Does the Internal FAQ contain an explicit kill criterion?
- [ ] Has someone external read the PR and reacted "I want this now" (not "oh yeah, that's cool")?

If any box is unchecked → don't move to Phase 1.
</content>
