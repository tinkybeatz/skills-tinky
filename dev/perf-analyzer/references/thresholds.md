# Threshold references

## Core Web Vitals (Google, p75)

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP | < 2.5s | 2.5-4.0s | > 4.0s |
| INP | < 200ms | 200-500ms | > 500ms |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |

## RAIL Model (Google)

| Context | Threshold | Rationale |
|---|---|---|
| Response (interaction) | < 100ms | Perceived as instant |
| Animation (frame) | < 16ms | 60fps for smoothness |
| Idle (background task) | < 50ms | Free up the main thread |
| Load (first paint) | < 5s | Beyond this, attention drops off |

## Lighthouse Score Weights

| Metric | Weight |
|---|---|
| Total Blocking Time (TBT) | 30% |
| Largest Contentful Paint (LCP) | 25% |
| Cumulative Layout Shift (CLS) | 25% |
| First Contentful Paint (FCP) | 10% |
| Speed Index (SI) | 10% |

## Cyclomatic complexity

| Value | Interpretation |
|---|---|
| 1-10 | Simple, maintainable |
| 11-20 | Moderate, keep an eye on it |
| 21-50 | Complex, refactoring recommended |
| > 50 | Very complex, high risk of bugs |

## Big O — Complexity of native JS operations

| Structure | Access | Search | Insertion | Deletion |
|---|---|---|---|---|
| `Array` | O(1) index | O(n) | O(1) push, O(n) unshift | O(1) pop, O(n) shift |
| `Object` | O(1) key | O(1) key | O(1) | O(1) |
| `Map` | O(1) | O(1) | O(1) | O(1) |
| `Set` | — | O(1) has | O(1) add | O(1) delete |
