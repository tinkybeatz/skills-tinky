# Examples: good SRS vs. bad SRS

This file shows concrete examples of well- and poorly-worded requirements,
to guide the writing.

---

## Examples of individual requirements

### Performance

**Bad:**
> FR-001: The system must be fast.

Problems: subjective, not measurable, not testable.

**Good:**
> NFR-P01: The system shall respond to API requests in under 200ms at the
> 95th percentile, measured under a load of 500 concurrent users.
>
> **Priority**: Must Have
> **Acceptance Criteria**:
> - [ ] k6 load test with 500 VUs for 10min: p95 < 200ms
> - [ ] No 5xx errors during the test

### Security

**Bad:**
> FR-012: The system must be secure.

Problems: subjective, not actionable, not testable.

**Good:**
> NFR-S01: The system shall authenticate users via OAuth2/OIDC with an
> OpenID Connect-compliant provider.
>
> NFR-S02: Stored passwords shall be hashed with bcrypt (cost factor ≥ 12).
>
> NFR-S03: After 5 failed login attempts within 15 minutes, the account
> shall be locked for 30 minutes.
>
> **Priority**: Must Have for all three
> **Acceptance Criteria**:
> - [ ] OWASP Top 10 pentest: no critical or high vulnerability

### Functional feature

**Bad:**
> FR-020: The user can manage their orders.

Problems: vague ("manage" = what exactly?), no detail.

**Good:**
> **Feature: Order management**
>
> FR-020: When a customer accesses the Orders page, the system shall
> display a paginated list of their orders sorted by date (most recent
> first), showing: order ID, date, status, total amount.
>
> FR-021: When a customer clicks on an order, the system shall display
> the order detail including: line items, quantities, unit prices,
> shipping address, and tracking number (if available).
>
> FR-022: When a customer clicks "Cancel" on an order with status
> "Pending", the system shall update the order status to "Cancelled"
> and send a confirmation email within 5 minutes.
>
> FR-023: The system shall not allow cancellation of orders with
> status "Shipped" or "Delivered". When attempted, the system shall
> display the message "This order can no longer be cancelled.
> Please contact support."

### User interface

**Bad:**
> FR-030: The interface must be beautiful and modern.

Problems: subjective, not measurable, not testable.

**Good:**
> NFR-U01: The interface shall comply with the WCAG 2.1 level AA
> guidelines.
>
> NFR-U02: The design shall be responsive and functional on viewports
> from 320px to 2560px.
>
> NFR-U03: The completion time for the task "create a new order" shall
> be under 2 minutes for a user who has completed onboarding.

---

## Examples of SRS sections

### Section 1.3 — Intended Audience (non-technical client)

**Bad:**
> This document is intended for all project members.

**Good:**
> ## Intended audience and reading guide
>
> | If you are... | Read first... | To... |
> |--------------|---------------------|---------|
> | The client (Marie, e-commerce manager) | Sections 1, 2 and the section 3 summary | Confirm the system meets your needs |
> | The development team | Sections 3, 4 and 5 | Understand the detailed specifications |
> | The QA team | Sections 3, 4 and 7 | Prepare the test plans |
> | The project manager | Sections 1, 2 and 7 | Track scope and plan the work |

### Section 2.1 — System Perspective (with diagram)

**Bad:**
> The system interacts with other systems.

**Good:**
> ## 2.1 System perspective
>
> The E-Store system fits into the following ecosystem:
>
> ```mermaid
> graph LR
>     Customer[Web/mobile client] -->|HTTPS| EStore[E-Store]
>     Admin[Admin back-office] -->|HTTPS| EStore
>     EStore -->|REST API| Payment[Stripe Payment]
>     EStore -->|REST API| Shipping[Shipping API]
>     EStore -->|SMTP| Email[SendGrid]
>     EStore -->|SQL| DB[(PostgreSQL)]
>     EStore -->|S3 API| Storage[MinIO/S3]
> ```
>
> **System being replaced**: E-Store replaces the current WooCommerce
> solution. The existing data (products, customers, order history) will
> be migrated. Product URLs will be redirected (301) to preserve SEO.

### Section 4.1 — Performance (structured table)

**Bad:**
> The system must be performant and support many users.

**Good:**
> ## 4.1 Performance
>
> | ID | Requirement | Metric | Nominal threshold | Peak threshold | Method |
> |----|------------|---------|--------------|----------|---------|
> | NFR-P01 | Page response time | TTFB | < 300ms | < 800ms | Lighthouse CI |
> | NFR-P02 | API response time | p95 latency | < 200ms | < 500ms | k6 load test |
> | NFR-P03 | Concurrent capacity | Concurrent users | 500 | 2000 | k6 stress test |
> | NFR-P04 | Throughput | Requests/sec | 200 rps | 800 rps | k6 load test |
> | NFR-P05 | Page size | Total weight | < 1.5 MB | — | Lighthouse |
>
> **Test conditions**:
> - Nominal: standard weekday load
> - Peak: Black Friday, sales (4x nominal)
> - Environment: prod-equivalent staging (same server specs)

---

## Example of a TBD list

```markdown
## TBD List

| ID | Item | Section | Owner | Target date | Impact |
|----|------|---------|------------|-----------|--------|
| TBD-001 | Payment provider choice (Stripe vs Adyen) | 5.3 | Marie (client) | 2026-05-01 | Blocks FR-040 to FR-045 |
| TBD-002 | Exact number of products in the initial catalog | 4.1 | Marie (client) | 2026-04-25 | Affects perf NFR-P03 |
| TBD-003 | Exact scope of i18n (supported languages) | 6.3 | Marie (client) | 2026-05-01 | Affects UI effort |
```
