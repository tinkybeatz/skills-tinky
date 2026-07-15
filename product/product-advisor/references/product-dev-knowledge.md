# Product Development Knowledge Base — product-advisor reference

Synthesis of a research report (April 2026, 60+ sources, 8 MECE agents).

## The translation funnel

```
BUSINESS GOAL (Impact)
  → OUTCOME (measurable result)
    → OPPORTUNITY (need/pain — JTBD)
      → SOLUTION (capability)
        → FEATURE (output, user story)
          → IMPLEMENTATION (code, architecture)
```

If you can't trace a feature back up to a business goal, it's an orphan feature.

## Frameworks

### Jobs-to-be-Done (Christensen/Ulwick)
Customers "hire" products to get a job done. The job is stable; products change.
- Functional job: the concrete task
- Emotional job: how the customer wants to feel
- Social job: how they want to be perceived
- Desired Outcome Statement (Ulwick): "[Direction] + [metric] + [context]" — solution-free, measurable, stable

### Opportunity Solution Tree (Torres)
1. Desired Outcome (root) — measurable business result
2. Opportunities — needs/pains/desires discovered through interviews
3. Solutions — at least 3 per opportunity (compare & contrast)
4. Assumption Tests — validate before building

### Impact Mapping (Adzic)
WHY (Goal) → WHO (Actors) → HOW (Impacts) → WHAT (Deliverables)
Each feature justified by an impact, itself tied to an actor and a goal.

### Shape Up (Singer)
- Fixed appetite, variable scope (6 weeks)
- No backlog — betting table
- Circuit breaker: not done = cancelled by default

### Lean Startup (Ries)
Build-Measure-Learn. MVP as a learning tool. Pivot or Persevere.

## Validation & measurement

### Before the build
- **ICE**: Impact × Confidence × Ease (average, fast)
- **RICE**: (Reach × Impact × Confidence) / Effort (quantified)
- **Fake door**: button leading to a non-existent feature, measure CTR
- **Concierge MVP**: manual service, the customer knows it
- **Wizard of Oz**: manual service, the customer doesn't know it
- Sequence: Fake door → Concierge → Wizard of Oz → Build

### After the build
- Feature Adoption Rate: median 16.5%, good >24.5%
- Retention curves by cohort (D1/D7/D30/D90)
- North Star Metric: the core value delivered
- AARRR: Acquisition → Activation → Retention → Revenue → Referral
- Users who adopt within the first 7-14 days = 6-month retention ×3.7

### Kill criteria
- Adoption < threshold at D+90
- Retention curve that doesn't flatten
- Maintenance cost > value delivered
- Set the criteria BEFORE the build

## Feature vs Capability vs Outcome

| Concept | Definition | Trap |
|---|---|---|
| Output (Feature) | What you ship | "We shipped 12 features" |
| Capability | What the system enables | "You can export to PDF" |
| Outcome | Measurable change | "Churn dropped by 5%" |
| Impact | Business effect | "MRR grew by 15%" |

## Domain impact

The business domain is the complexity multiplier:
- Marketing SaaS: 1-2×
- E-commerce: 2-4×
- Logistics: 4-8×
- Healthcare: 5-10×
- Finance: 8-15×

Strategic DDD (bounded contexts) > tactical DDD (aggregates).
Event Storming to discover bounded contexts in a single day.

## Mobile vs Web

| Criterion | Web | Native mobile |
|---|---|---|
| Deploy | Seconds | 1-5 days |
| Feedback loop | Real-time | 4-5 days min |
| Maintenance cost/year | 5-10% | 15-20% |
| A/B testing | Very fast | Slow |
| Acquisition | SEO | ASO, push |

Web is the optimal default for validating. Mobile when the use case demands it.

## Sources of feature ideas

### Qualitative
- User interviews (min 1/week, focus on past behaviors)
- Contextual observation (contextual inquiry)
- Support tickets (categorize by theme/frequency)
- Feature requests = symptoms, trace back to the job

### Quantitative
- Funnel analysis (every drop-off = an opportunity)
- Heatmaps / session recordings
- Product analytics (engagement, retention, adoption)

### Competitive
- Competitor feature matrix
- Competitors' App Store reviews (their weaknesses = your opportunities)
- Public changelogs

## Prioritization

| Framework | When | Strength |
|---|---|---|
| MoSCoW | MVP, fixed deadline | Simple |
| Value/Effort | Quick wins early-stage | Visual |
| RICE | Mature product with data | Quantified |
| Kano | Discovery, emotional | User-centered |
| WSJF | Large scale, time-critical | Optimal sequencing |
