# Business Model Report Template

Use this structure for the report content sent to `pdf-generator`.

```markdown
# Business Model Report - [Project Name]

Date: [YYYY-MM-DD]
Author: AI agent
Scope: [web/mobile/SaaS/marketplace/etc.]

## 1. Executive Summary

[5-10 lines: recommended model, why, biggest risks, next experiment.]

## 2. Project Diagnosis

- Product:
- Target users:
- Buyer/payer:
- Market/country:
- Current traction:
- Existing monetization:
- Main constraints:

## 3. Evidence and Research

| Source | Type | Score | What it proves |
|---|---|---:|---|
| [source] | [primary/benchmark/academic/platform] | [score] | [claim] |

## 4. Key Assumptions

| Assumption | Status | Why it matters | How to test |
|---|---|---|---|

## 5. Candidate Business Models

| Candidate | Revenue logic | Fit | Main risk | Score |
|---|---|---|---|---:|

## 6. Recommended Business Model

### Recommendation

[Primary model and optional secondary model.]

### Justification

- Verified fact: ...
- Derived recommendation: ...
- Assumption: ...

## 7. Business Model Canvas

| Block | Decision | Justification |
|---|---|---|
| Customer Segments | | |
| Value Proposition | | |
| Channels | | |
| Customer Relationships | | |
| Revenue Streams | | |
| Key Resources | | |
| Key Activities | | |
| Key Partners | | |
| Cost Structure | | |

## 8. Pricing and Monetization

- Pricing metric:
- Packaging:
- Free/paid boundary:
- Payment method:
- Platform/store constraints:
- Country adaptation:

## 9. Unit Economics and KPIs

| KPI | Why it matters | Initial target or learning threshold |
|---|---|---|

## 10. Validation Experiments

| Experiment | Hypothesis tested | Success threshold | Duration |
|---|---|---|---|

## 11. Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|

## 12. Open Questions

[List unresolved questions that materially affect the model.]

## 13. Sources

[Numbered source list with URLs and access dates.]
```

## Style Rules

- Write for a founder or product owner.
- Be concrete and numeric when evidence exists.
- Use "unknown" instead of inventing data.
- Highlight decisions and tradeoffs.
- Keep the PDF concise unless the user asks for a long report.

## `pdf-generator` Payload Contract

When the report is ready, call `$pdf-generator`. It is an orchestrator skill
that spawns the `pdf-renderer` agent. Do not ask `pdf-generator` to do
business-model reasoning; it receives final content and handles layout, PDF
generation, and delivery.

Use this prompt shape:

```text
Skill path: ~/.claude/skills/pdf-generator

Generate a PDF with the following content:

Title: Business Model Report - [Project Name]
Recipient: [Client or "Internal"]
Date: YYYY-MM-DD
Type: report
Format: A4 portrait

Sections:
1. Executive Summary — [content]
2. Project Diagnosis — [content]
3. Evidence and Research — [content]
4. Candidate Business Models — [content]
5. Recommended Business Model — [content]
6. Business Model Canvas — [content]
7. Pricing and Monetization — [content]
8. Unit Economics and KPIs — [content]
9. Validation Experiments — [content]
10. Risks and Mitigations — [content]
11. Open Questions — [content]
12. Sources — [content]

Output path: /tmp/business-model-[slug]-YYYYMMDD.pdf
```

If a tool or agent accepts JSON-like input, the same content may be structured as:

```json
{
  "report_type": "business_model",
  "title": "Business Model Report - [Project Name]",
  "subtitle": "[Short positioning or market]",
  "author": "AI agent",
  "date": "YYYY-MM-DD",
  "language": "en",
  "audience": "founder|client|investor|internal",
  "brand": "[your brand]",
  "format": {
    "output": "pdf",
    "style": "professional",
    "include_table_of_contents": true,
    "include_sources": true
  },
  "metadata": {
    "project_name": "[Project Name]",
    "project_type": "web|mobile|saas|marketplace|ai_app|ecommerce|other",
    "target_country": "[Country/Region]",
    "sector": "[Sector]",
    "confidence": "low|medium|high"
  },
  "sections": [
    {
      "title": "Executive Summary",
      "content_markdown": "[final content]"
    },
    {
      "title": "Project Diagnosis",
      "content_markdown": "[final content]"
    },
    {
      "title": "Evidence and Research",
      "content_markdown": "[final content with inline citations]"
    },
    {
      "title": "Candidate Business Models",
      "content_markdown": "[comparison table]"
    },
    {
      "title": "Recommended Business Model",
      "content_markdown": "[recommendation and justification]"
    },
    {
      "title": "Business Model Canvas",
      "content_markdown": "[canvas table]"
    },
    {
      "title": "Pricing and Monetization",
      "content_markdown": "[pricing logic]"
    },
    {
      "title": "Unit Economics and KPIs",
      "content_markdown": "[KPI table]"
    },
    {
      "title": "Validation Experiments",
      "content_markdown": "[experiment table]"
    },
    {
      "title": "Risks and Mitigations",
      "content_markdown": "[risk table]"
    },
    {
      "title": "Open Questions",
      "content_markdown": "[unresolved assumptions]"
    },
    {
      "title": "Sources",
      "content_markdown": "[numbered source list with URLs]"
    }
  ],
  "delivery": {
    "return_pdf_path": true,
    "return_summary": true
  }
}
```

Expected `pdf-generator` response:

```text
PDF_PATH: /absolute/path/to/file.pdf
HTML_PATH: /path/to/source.html
PAGES: <number>
STATUS: success | error
```

After receiving this response, `generate-business-model` must report the PDF
path to the user. If generation fails, explain the failure and keep the final
Markdown/report payload available for retry.
