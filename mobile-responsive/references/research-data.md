# Research data — Reference figures

Consult this file when you need to justify a decision with empirical data.
Each figure is traceable to its source.

---

## Touch & Ergonomics

| Data point | Value | Source |
|------------|-------|--------|
| Average fingertip width | 8-10mm | MIT Touch Lab (2003) |
| Thumb interactions | 75% of all mobile interactions | Hoober (1,333 obs., 2013) |
| One-handed use | 49% of users | Hoober |
| Easy zone precision (bottom-center) | 98% first tap | Hoober |
| Hard zone precision (top/corners) | 65-75% | Hoober |
| Error rate for < 8mm targets | 40%+ | Parhi et al. (MobileHCI '06) |
| Hamburger vs bottom nav discovery | -50% discovery with hamburger | NNg (179 participants) |

## Accessibility

| Data point | Value | Source |
|------------|-------|--------|
| WCAG 2.5.8 (AA) minimum | 24x24 CSS px | W3C WCAG 2.2 |
| WCAG 2.5.5 (AAA) enhanced | 44x44 CSS px | W3C WCAG 2.2 |
| AA contrast, normal text | 4.5:1 | W3C |
| AA contrast, large text | 3:1 | W3C |
| Automated tools vs real issues | 30-40% detected | Multiple sources |
| iOS users with reduced-motion on | 10-15% | Aggregated developer telemetry |
| Apps with no a11y metadata (>90% of buttons) | 23% of apps | UW CREATE (~10K apps) |

## Animation & Performance

| Data point | Value | Source |
|------------|-------|--------|
| 60Hz frame budget | 16.67ms (~10ms usable) | Chrome pipeline |
| 120Hz frame budget | 8.33ms (~5ms usable) | Chrome pipeline |
| VRAM per full-screen 1080p layer | ~8MB | Chromium compositor |
| Median Android jank threshold | >6ms main-thread | Chrome telemetry 2024 |
| Skeleton vs spinner perception | -30-40% perceived time | Viget study |
| content-visibility: auto gain | Up to 7x rendering | Chrome benchmarks |
| Framer Motion bundle | ~30-40KB gzipped | npm analysis |

## UX Metrics

| Data point | Value | Source |
|------------|-------|--------|
| Mobile pages passing all 3 CWV | 48% | HTTP Archive 2025 |
| Average mobile LCP | 4.2s | Web Almanac 2025 |
| Abandonment if load > 3s | 53% | Think with Google |
| Bounce +32% from 1s→3s | Measured | Google neural net study |
| Desktop vs mobile conversion | 3.9-4.3% vs 1.5-2.25% | Baymard, Smart Insights |
| Mobile cart abandonment | 75.5-80% | Baymard (49 studies) |
| Form autofill: time | -35% | CXL |
| Form autofill: abandonment | -75% | CXL |
| Single-column vs multi-column | 15.4s faster | Reform (Ben Labay) |
| Mobile error clicks YoY | +667% | FullStory (14B sessions, 2025) |
| Mobile dead clicks | 929/1000 sessions | FullStory |
| CWV Poor→Good: ranking | +5-8 positions | SEMrush 2024 |

## Typography

| Data point | Value | Source |
|------------|-------|--------|
| Default iOS body | 17pt | Apple HIG |
| Default Android body | 14sp | Material Design 3 |
| Absolute web minimum | 12px | Consensus |
| iOS input zoom threshold | < 16px | Deque |
| WCAG 1.4.12 line height | >= 1.5x | W3C |
| Optimal mobile CPL | 30-50 chars | Baymard |
| Descriptions > 80 CPL skipped | +41% | Baymard |
| Line spacing 100%→120%: precision | +20% reading | Baymard |
