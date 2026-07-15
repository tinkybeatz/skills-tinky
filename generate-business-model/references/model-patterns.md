# Model Patterns for Web and Mobile Projects

## Selection Matrix

| Model | Best for | Avoid when | Key metrics |
|---|---|---|---|
| Subscription SaaS | Repeated workflow, recurring value, B2B or productivity | Usage is rare or value is one-off | MRR, churn, NRR, CAC payback, activation |
| Usage-based | Value and cost scale with consumption: AI, APIs, infra, data, transactions | Users need budget predictability and usage is hard to understand | ARPU, gross margin, usage expansion, cost per unit |
| Hybrid subscription + usage | Base access plus variable value/cost | Billing complexity would block adoption | MRR, overage revenue, gross margin, retention |
| Freemium | Low marginal cost, viral/collaborative product, huge market | CAC is high, free tier has expensive support or infra | free-to-paid conversion, activation, retention, viral coefficient |
| Free trial / reverse trial | Product value appears quickly after onboarding | Time-to-value is long or requires setup | trial start, trial-to-paid, time-to-value, refund |
| Marketplace commission | Two-sided transaction with trust, payments, repeat supply/demand | Liquidity is hard to bootstrap or transaction can bypass platform | GMV, take rate, liquidity, repeat rate |
| Transaction fee | Payments, booking, fintech, ticketing, procurement | Margins are thin or regulation is heavy | TPV, take rate, loss/fraud rate, payment success |
| Advertising | Massive attention, frequent usage, low willingness to pay | Small niche, privacy-sensitive, low session volume | DAU/MAU, sessions, ARPDAU, fill rate |
| Ecommerce margin | Physical/digital product sales | Supply chain, returns, or CAC break margins | gross margin, AOV, repeat purchase, CAC |
| Creator/community membership | Identity, content, status, access, belonging | Value is purely transactional or community is weak | paid members, engagement, churn, content cadence |
| Enterprise license | High-value B2B, compliance, workflow integration | Buyer is individual, sales capacity is low | ARR, pipeline, win rate, implementation time |
| Service-assisted product | Early custom delivery, complex B2B, agency-to-product transition | Delivery cannot be standardized | gross margin, delivery hours, repeatability, expansion |

## Pattern Guidance

### B2B SaaS

Use subscription when value is tied to access and recurring workflow. Use usage-based when the value metric is objective and grows with customer success: API calls, messages sent, processed documents, seats automated, workflows run.

For AI products, consider hybrid pricing: base subscription for predictability plus usage/credits for costly AI operations.

### Consumer Mobile Apps

Subscription works best when value is habitual: health, education, productivity, media, utilities. Freemium works when free usage increases data, brand, habit, or virality without destroying margin.

For mobile apps, account for app store rules, refunds, trials, plan duration, and platform commissions. Web onboarding and web billing may matter depending on country and platform rules.

### Marketplaces

Only recommend marketplace commission if:

- both supply and demand sides are identifiable
- the transaction needs trust, discovery, payment, scheduling, insurance, or reviews
- early liquidity can be built in a narrow niche/geography

If supply is scarce, start service-assisted or curated before opening self-serve.

### Ecommerce and Transactional

Use transaction fees or margins when the product is tied to a clear purchase event. Watch payment fees, refunds, fraud, logistics, VAT/sales tax, support, and chargebacks.

### Advertising

Do not default to advertising. It requires scale, frequent usage, strong attention, and enough inventory quality. For niche apps, advertising usually under-monetizes unless it is sponsorship or intent-driven.

## Country and Sector Adaptation

Check:

- local willingness to pay and purchasing power
- preferred payment methods
- subscription maturity
- VAT/sales tax and invoicing norms
- app store billing constraints
- consumer protection and cancellation rules
- regulated-sector constraints
- B2B buying behavior and procurement friction

Examples:

- Europe: VAT, GDPR, consumer cancellation expectations, DMA app distribution changes.
- US: card-first payment culture, higher SaaS willingness to pay, strong B2B subscription adoption.
- Africa and emerging markets: mobile money and local payment methods can dominate over card payments.
- Asia: super-app ecosystems, wallets, local app store/payment expectations, market-specific pricing.
