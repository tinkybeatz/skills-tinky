# ARCHITECTURE_CONCEPTOR Source Policy

## Source tiers

### Tier 1 - Mandatory primary references

- Official cloud provider architecture guidance (AWS Well-Architected, Azure Architecture Center, GCP Architecture Framework)
- Standards bodies (ISO/IEC 25010 for quality attributes, ISO/IEC 42010 for architecture description)
- Official framework and runtime documentation
- Established architecture decision record (ADR) formats and templates
- Vendor-neutral architecture handbooks (e.g., TOGAF, C4 model documentation)

### Tier 2 - Strong supporting references

- Peer-reviewed software architecture research
- Recognized engineering books (Fundamentals of Software Architecture, Building Evolutionary Architectures, Designing Data-Intensive Applications)
- Published postmortems with transparent methodology and reproducible findings
- Architecture case studies from established engineering organizations

### Tier 3 - Context-only references

- Blog posts, conference talks, forum threads
- Vendor marketing pages without independent benchmarks
- Social media discussions and opinion pieces

## Usage rules

- Always prioritize Tier 1 for architecture decisions and quality attribute claims.
- Use Tier 2 to support pattern selection and trade-off reasoning.
- Use Tier 3 only for idea discovery, never as sole evidence for a recommendation.

## Minimum evidence policy

- At least 5 relevant sources per architecture decision package.
- At least 1 formal standard or technical report per decision.
- At least 2 independent sources for each recommended architecture approach.
- Economic claims must reference measurable data (pricing pages, benchmark reports, capacity models).

## Freshness policy

- For cloud services, pricing, and platform capabilities:
  - use the most recent official source
  - include exact update date when available
- For architecture patterns and principles:
  - foundational references are allowed (e.g., Domain-Driven Design, 2003)
  - complement with at least one recent validation source showing current relevance

## Credibility checks

Before retaining a source, verify:

- ownership (standards body, official maintainer, recognized author)
- publication/update date
- reproducibility (benchmarks, data, or explicit methodology)
- conflict of interest and promotional bias indicators

## Rejection rules

Reject or strongly down-rank when:

- no identifiable owner and no date
- claims cannot be reproduced or validated in the target context
- evidence is purely anecdotal for critical architecture decisions
- circular citations with no primary origin
- vendor benchmark without independent validation

## Citation format standard

For each source include:

- title
- URL or internal path
- publication/update date when available
- one-line reason for relevance
