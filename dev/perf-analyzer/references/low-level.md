# Low-level analysis — V8, allocation, serialization, event loop

This reference covers the layer that most web audits ignore: what actually
happens at the V8 runtime level. The approach comes from the embedded/C world
(avionics, critical systems) where every CPU cycle counts.

**When this analysis is relevant:**
- Hot paths (code that runs very frequently)
- Handling large datasets (>10k elements)
- High-load services (>100 req/s)
- Batch or streaming processing
- Unexplained latency despite "clean" application code

---

## V8 Engine & JIT Compilation

V8 compiles JS into machine code via TurboFan (JIT). It optimizes
**predictable** code and deoptimizes **polymorphic** code.

| Pattern to detect | What actually happens | Severity |
|---|---|---|
| Objects with variable shapes — properties added conditionally, `delete obj.prop` | V8 loses its hidden classes/inline caches, falls back to dictionary mode (~10x slower) | High |
| Polymorphic functions — the same function with different argument types | Beyond 4 seen types (megamorphic), TurboFan gives up on optimization | Medium |
| `arguments` used in hot functions (instead of rest params) | Forces the allocation of a special object, prevents certain optimizations | Medium |
| `try/catch` wrapping large blocks of hot code | V8 optimizes the contents less well — keep the block to the strict minimum | Medium |
| `eval()`, `with`, `new Function()` in frequently run code | Completely destroys optimizations — V8 can no longer make assumptions about the scope | Critical |

## Memory allocation & GC pressure

V8 uses a generational GC (Scavenge for young space, Mark-Sweep-Compact for old space).
Each collection pauses the main thread (stop-the-world).

**Embedded → web analogy:** in C, you avoid `malloc` in critical loops and
pre-allocate buffers. Same principle in JS: reuse objects, avoid allocations
in hot paths, prefer controlled mutation over copying.

| Pattern to detect | What actually happens | Severity |
|---|---|---|
| Chained `.map().filter().reduce()` on large arrays | Creates an intermediate array at each step — on 100k elements = 3 allocations of 100k | High |
| Spread on large objects (`{...bigObj, newProp: val}`) in frequently run code | Full O(n) copy in memory and CPU on every call | Medium |
| String concatenation in a loop (`str += chunk`) | Each `+=` creates a new string (immutable). Use an array + `.join()` | High |
| Closures capturing large scopes in frequent callbacks | The scope is retained on the heap as long as the closure exists | Medium |
| `JSON.parse(JSON.stringify(obj))` for deep clone | O(n) in time AND space, 2 copies. Use `structuredClone()` | High |

## Data locality & data structures

In C/C++, cache locality (L1/L2/L3) is a major factor. In JS, the impact is
indirect but real via V8 — typed arrays and homogeneous arrays are contiguous in memory.

| Pattern to detect | What actually happens | Severity |
|---|---|---|
| Array of Objects (AoS) on large datasets vs Structure of Arrays (SoA) | SoA is more cache-friendly for operations on a single property, enables TypedArrays | Medium |
| `Object`/`Map` as a lookup with numeric keys | `array[id]` is O(1) and faster than a hash lookup | Low |
| Sparse arrays | V8 switches from "elements" mode (fast) to "dictionary" mode (slow) | Medium |
| Iterating over `Map`/`Set` vs arrays for sequential processing | Arrays are optimized for sequential iteration in V8 | Low |

## Serialization & I/O

The code/I/O boundary is often the real bottleneck.

| Pattern to detect | What actually happens | Severity |
|---|---|---|
| `JSON.stringify`/`JSON.parse` on large objects in hot paths | Single-threaded, O(n). On 1MB ≈ 5-10ms blocking. Use `fast-json-stringify` | High |
| Reading whole files into memory instead of streams | Loads everything into RAM. Streams = fixed memory footprint | High |
| Unnecessary Buffer copies (Buffer → string → Buffer) | Each conversion allocates. Work directly with Buffers (zero-copy) | Medium |
| API responses serialized in full instead of streamed | Buffers the whole response in memory before sending. Streaming = chunks sent as soon as ready | High |
| Synchronous logging of objects on hot paths | `console.log(bigObj)` = serialization + synchronous I/O. Use pino (async) | Medium |

## Event Loop & concurrency

The event loop = a single-threaded cooperative scheduler, like a main loop
in a real-time embedded system.

| Pattern to detect | What actually happens | Severity |
|---|---|---|
| `for` loops on large datasets without yielding (>50ms) | Blocks the event loop. Break it up with `setImmediate()` or a worker thread | Critical |
| `Promise.all` with hundreds of I/O promises | File descriptor saturation, memory spike. Use p-limit/p-map | High |
| Sequential `await` on independent operations | Latency = sum instead of max. `Promise.all` (with a pool) = N times faster | High |
| Worker threads for I/O-bound tasks | Serialization overhead with no benefit | Low |
| No backpressure on streams | Unbounded memory accumulation. Respect the `.write()` return value, use `pipeline()` | High |
