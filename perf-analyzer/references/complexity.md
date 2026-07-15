# Algorithmic complexity analysis — Time & Space

## Time complexity — Big O on hot paths

The goal isn't an academic audit but to identify when actual complexity
diverges from expected complexity.

| Pattern to detect | Actual complexity | Why it's a problem | Severity |
|---|---|---|---|
| `Array.includes()`/`indexOf()` inside a loop | O(n×m) instead of O(n) | Use a `Set` for O(n) | High if n×m > 10k |
| Nested `Array.find()`/`filter()` (manual join) | O(n×m) | An indexed `Map` = O(n+m) | High |
| `Array.sort()` called on every render/request over stable data | O(n log n) repeated | Sort once when the data changes | Medium |
| `.shift()`/`.unshift()` in loops or buffers | O(n) per operation | Ring buffer or deque = O(1) | High if frequent |
| Unbounded recursion / no memoization | Potentially O(2^n) | Stack overflow risk on large inputs | Critical if hot path |
| Repeated linear search instead of indexing | O(n) instead of O(1) | Build an index once = O(n), each lookup = O(1) | Medium |
| `JSON.parse(JSON.stringify())` for deep clone | O(n) time AND space | `structuredClone()` is faster, controlled mutation = O(1) | High if large |

### Reference: complexity of native JS operations

| Structure | Access | Search | Insertion | Deletion | Notes |
|---|---|---|---|---|---|
| `Array` | O(1) index | O(n) | O(1) push, O(n) unshift | O(1) pop, O(n) shift/splice | Dense V8 arrays are contiguous in memory |
| `Object` | O(1) key | O(1) key | O(1) | O(1) | Hidden classes optimize when the shape is stable |
| `Map` | O(1) | O(1) | O(1) | O(1) | Insertion order preserved, non-string keys OK |
| `Set` | — | O(1) has | O(1) add | O(1) delete | Hash table, ideal for membership tests |
| `WeakMap/WeakSet` | O(1) | O(1) | O(1) | O(1) | No iteration, GC-friendly |

**How to annotate:** `Complexity: O(n²) → O(n) with Map indexing`

---

## Space complexity — Stack vs Heap

In V8, memory is divided as in C (stack + heap) with different characteristics.

### V8 memory model

```
┌─────────────────────────────────┐
│           STACK                 │  ← Fast, LIFO, fixed size (~1MB)
│  • Primitives (number, boolean) │  ← Values directly on the stack frame
│  • References (heap pointers)   │  ← Variable on stack, object on heap
│  • Function call frames         │  ← Recursion depth = stack size
├─────────────────────────────────┤
│           HEAP                  │  ← Large, GC-managed, slower
│  ┌─ Young Generation ──────┐   │  ← Scavenge GC (fast, ~1-5ms)
│  │  Semi-space From / To   │   │  ← ~1-8MB
│  └─────────────────────────┘   │
│  ┌─ Old Generation ────────┐   │  ← Mark-Sweep-Compact (~10-50ms+)
│  │  Old Object Space       │   │
│  │  Large Object Space     │   │  ← Objects > 512KB, never moved
│  │  Code Space             │   │  ← JIT code compiled by TurboFan
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

| Pattern to detect | Memory impact | Severity |
|---|---|---|
| Closures capturing large scopes in long-lived callbacks | Entire scope retained on the heap as long as the closure exists | High |
| Deep recursion (>1000 levels) without TCO | Stack overflow — V8 doesn't support TCO. ~1KB per frame | Critical if input unbounded |
| Object accumulation in Old Generation (caches, global stores) | Migrate to Old Space, GC gets more expensive. The bigger it gets, the longer the pauses | High |
| Massive creation of short-lived objects in hot paths | Young Generation pressure — frequent Scavenge GC | Medium |
| Buffers/TypedArrays > 512KB | Large Object Space — never compacted, possible fragmentation | Medium if frequent |
| Strings concatenated in a loop | Each concat = a new string on the heap. 1000 × 100 chars = ~50KB of intermediate allocations | Medium |

**How to annotate:** `Space: O(n) heap → O(1) with in-place mutation` or
`Stack: O(n) recursive frames → O(1) with iteration`
