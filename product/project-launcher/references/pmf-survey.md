# Measuring PMF — Sean Ellis 40% rule + Vohra framework

Primary sources:
- Sean Ellis (originator of the concept and of growth hacking)
- Rahul Vohra, Superhuman — [First Round Review](https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/)

---

## The 40% rule

Sean Ellis benchmarked ~100 startups. The finding: the companies that scaled easily all had ≥ 40% of users answering **"Very disappointed"** to ONE question:

> *"How would you feel if you could no longer use X?"*

Answer choices:
- Very disappointed
- Somewhat disappointed
- Not disappointed (it isn't really that useful)
- N/A — I no longer use [product]

**PMF threshold: ≥ 40% Very disappointed** among recent active users.

---

## Typeform / Tally template — 4 questions

```
1. How would you feel if you could no longer use [PRODUCT]?
   ○ Very disappointed (I'd be devastated)
   ○ Somewhat disappointed (I'd adapt)
   ○ Not disappointed (not really useful)
   ○ N/A — I no longer use it

2. What type of person do you think would benefit most from [PRODUCT]?
   [Free text]

3. What is the main benefit you get from [PRODUCT]?
   [Free text]

4. How could we improve [PRODUCT] for you?
   [Free text]
```

**Sending criteria:**
- Target: users active **within the last 2 weeks** (otherwise you get an inactive-user bias)
- Minimum sample: 40 respondents for a reliable signal. 100+ is ideal.
- Channel: email (higher response rate than in-app), with a light incentive if needed (a $5 Amazon gift card)

---

## Vohra framework — going from 22% to PMF

If the 40% rule gives < 40%, Vohra proposes a 4-step process to raise the score without pivoting entirely.

### Step 1 — Segment

Filter the "Very disappointed" respondents and identify the **dominant persona** (role, industry, company size, in-app behavior). The typical filter at Superhuman: "executives & managers in tech who use email > 3h/day".

### Step 2 — Understand the job-to-be-done

For that segment only, analyze the answers to questions 2 and 3 (who benefits / what benefit). Identify the **primary benefit** this segment cites most.

At Superhuman: "speed and keyboard shortcuts" for power users.

### Step 3 — Identify the "high-expectation customers"

Among the "Very disappointed", isolate those who are **the most demanding** (detailed answers, precise suggestions, daily retention). They're the ones who set the bar.

### Step 4 — Double down

Build the roadmap from this segment's feedback. Everything else (other segments, features requested by the "Somewhat disappointed") is deprioritized or removed.

**Superhuman result:** PMF score 22% → 58% in under a year, without pivoting the product.

---

## Coexistence with Altman's 4 questions

The 40% rule is quantitative (it makes PMF binary). Altman's 4 questions are qualitative (they check the ground truth). The two should converge.

| Altman question | How to verify it |
|---|---|
| Are users using your product more than once? | Cohort retention (D1, D7, D30 in the analytics) |
| Are users fanatic? | Text answers to Q3/Q4 of the survey (length, emotion) |
| Would users be truly bummed if your company went away? | This is exactly the 40% rule |
| Are users recommending you without asking? | NPS signal + viral coefficient (% of signups via organic referral) |

---

## Defining the NSM (North Star Metric)

Source: Sean Ellis (originator of the term), Lenny Rachitsky (formalization).

**Criteria for a good NSM:**
1. Captures the core value delivered to the user (not the value extracted by the company)
2. Retention-driven (not signups or unqualified MAU)
3. Stable over time (≠ "One Metric That Matters", which changes)
4. Actionable by every team (everyone can influence its progress)

**Bad NSMs (vanity):**
- Total signups
- Total downloads
- Page views
- MAU without usage qualification
- Total revenue (a result, not a proxy for value delivered)

**Good NSMs (by category):**
- Marketplace: transactions completed / week per active user
- Productivity SaaS: core actions per active user (e.g. messages processed, docs edited)
- Social network: meaningful connections per active user
- Agentic tool: tasks completed by the agent per active user / week, or user-validated hours saved
- Customer service: retained revenue (ARR without churn)

---

## Hard gate — refusing to declare PMF

The skill must refuse to move from Phase 3 → Phase 4 if:

1. The 40% rule is NOT measured OR the score is < 40% with no clear Vohra plan
2. The NSM is not defined OR it's a vanity metric

Message to display:

```
⚠️ PMF not validated.

Status:
- 40% rule: [score / "not measured"]
- NSM: [value / "vanity metric"]

Before scaling (hire, raise, ads, partnerships), run this loop:
1. Launch the Ellis survey (40 respondents minimum)
2. If < 40%: apply the Vohra framework
3. Define a retention-driven NSM
4. Come back when these 3 boxes are checked

Ignored risk: hiring / raising on a false signal.
Consequence: 43% of startup deaths come from "no PMF" (CB Insights, 483 post-mortems).
```
</content>
