# Mac Studio M3 Ultra Performance — Optimization standards

Standards specific to running the Mac Studio M3 Ultra (96 GB, 28 cores,
60 Metal 4 GPU cores) for the LLM Lab.

---

## Memory budget — The main constraint

The unified memory (96 GB) is shared between macOS, Docker, and Ollama.
Everything hinges on this. A poor split = swap = catastrophic latency.

### Target allocation

| Consumer | Budget | Justification |
|----------|--------|---------------|
| macOS + apps (Finder, Safari, terminal) | ~8-10 GB | Non-compressible |
| Docker Desktop VM | **16-20 GB max** | Configurable in Docker Desktop Settings |
| Ollama loaded models | **50-65 GB** | The bulk of the budget — this is where you win |
| Safety margin | ~5-10 GB | Avoids swap, gives the system room to breathe |

### Configuring Docker Desktop

Docker Desktop > Settings > Resources:

```
Memory:         16 GB    (no more — the rest is for Ollama)
CPU:            12       (leave 16 cores for macOS + Ollama)
Swap:           2 GB     (minimum, we want to avoid swap)
Disk image:     64 GB    (enough for images + volumes)
```

Do not allocate more than 20 GB to Docker. The full lab stack uses ~13 GB,
and 16 GB leaves headroom without encroaching on Ollama.

---

## Ollama — Metal optimization

### GPU offloading

Ollama automatically offloads model layers to the Metal GPU.
On the M3 Ultra, **all the layers** of a 72B Q4 model (~40 GB) fit
in unified memory with GPU acceleration. No CPU/GPU split needed.

Check that the GPU is actually being used:
```bash
# During inference, watch Metal GPU usage
sudo powermetrics --samplers gpu_power -i 1000 | grep "GPU"
```

### Context and KV cache memory

The KV cache consumes memory in proportion to the context size.
On 96 GB you have headroom, but it still needs sizing:

| Model | Context 4K | Context 16K | Context 32K | Context 64K |
|-------|-----------|-------------|-------------|-------------|
| Qwen 3 8B (Q4) | +0.5 GB | +2 GB | +4 GB | +8 GB |
| Qwen 3 72B (Q4) | +2 GB | +8 GB | +16 GB | +32 GB |

For a 72B model, a 32K context consumes **~56 GB total** (40 GB model + 16 GB KV).
Beyond that, it no longer fits alongside a second loaded model.

Set the default context size in Ollama:
```bash
export OLLAMA_NUM_CTX=16384    # 16K by default — a good compromise
```

For a prompt that needs more context, specify it in the request:
```json
{"model": "qwen3:72b", "options": {"num_ctx": 32768}}
```

### Managing model loading/unloading

```bash
# Keep the model in memory longer (default: 5min)
export OLLAMA_KEEP_ALIVE=30m

# Limit to 2 concurrent models max
export OLLAMA_MAX_LOADED_MODELS=2

# Number of parallel requests per model
export OLLAMA_NUM_PARALLEL=4

# Reduce the KV cache memory footprint
export OLLAMA_FLASH_ATTENTION=1    # ~30% less KV cache RAM
export OLLAMA_KV_CACHE_TYPE=q8_0   # Quantize the KV cache (half vs f16)

# Default 16K context (enough for 99% of cases)
export OLLAMA_NUM_CTX=16384
```

### Measured impact of the optimizations (M3 Ultra 96 GB)

| Config | qwen3:8b | qwen3:30b-a3b | Total | Free |
|--------|----------|---------------|-------|------|
| Before (max ctx, f16 KV) | 8.6 GB (40K ctx) | 33 GB (262K ctx) | 41.6 GB | 39 GB |
| After (limited ctx, q8 KV) | 7.9 GB (8K ctx) | 22 GB (16K ctx) | 29.9 GB | 51 GB |
| **Gain** | -0.7 GB | **-11 GB** | **-11.7 GB** | **+12 GB** |

The context can be increased per request for specific cases:
```json
{"model": "qwen3-coder:30b", "options": {"num_ctx": 65536}}
```

The first prompt after loading is slow (10-30s for a 30B MoE).
The following ones are fast. `KEEP_ALIVE=30m` avoids unnecessary reloads
during a work session.

---

## Throughput — What to expect

Estimated benchmarks on the M3 Ultra (96 GB, 60 GPU cores):

| Model | Quantization | tok/s (prompt) | tok/s (generation) | Notes |
|-------|--------------|----------------|--------------------|-------|
| Qwen 3 8B | Q4_K_M | ~200 | 80-120 | Fast, interactive use |
| Qwen 3 8B | Q8_0 | ~150 | 60-80 | Better quality, slightly slower |
| Qwen 3 72B | Q4_K_M | ~40 | 15-25 | Usable interactively |
| Qwen 3 72B | Q8_0 | Not viable | — | ~80 GB, leaves nothing for the rest |
| Llama 4 Scout | Q4_K_M | ~50 | 20-30 | MoE, good quality/speed ratio |
| DeepSeek R1 70B | Q4_K_M | ~35 | 12-20 | Slower (dense, not MoE) |

**Rule of thumb**: Q4_K_M is the sweet spot for the lab. Q8 only for
the small models (8B) when you want to maximize quality.

---

## Quantization — Which format to choose

| Format | Size (72B) | Quality | Speed | When to use it |
|--------|------------|---------|-------|----------------|
| Q4_K_M | ~40 GB | Good | Fast | **Default for the lab** — best compromise |
| Q4_K_S | ~38 GB | Acceptable | Faster | If memory is tight |
| Q5_K_M | ~48 GB | Very good | Moderate | When quality matters more than speed |
| Q8_0 | ~72 GB | Excellent | Slow | Small models only (8B, 14B) |
| F16 | ~140 GB | Reference | Very slow | Does not fit in memory on 96 GB |

To download a specific quantization in Ollama:
```bash
ollama pull qwen3:72b-q4_K_M    # Default format, the most common
```

---

## Docker on Mac — Specifics

### Docker Desktop = a Linux VM

Docker on Mac runs inside a Linux VM (via Virtualization.framework).
This means:

- **No Metal GPU access from Docker** — that's why Ollama runs natively
- **Slower disk I/O** than native — bind mounts are most affected
- **Networking via NAT** — `host.docker.internal` is the only gateway to the host

### Optimizing I/O performance

Bind mounts are slow on Docker for Mac (FS sync between the VM and the host).
For large data, prefer named Docker volumes (stored inside the VM).

```yaml
# ✅ Fast — named volume (stored in the VM)
volumes:
  - litellm-pg-data:/var/lib/postgresql/data

# ⚠️ Slower — bind mount (synced with the host)
volumes:
  - ./litellm-config.yaml:/app/config.yaml:ro    # OK because it's a small file
  - ./data:/app/data                              # ❌ Slow for a large data volume
```

For config files (small, read-only), a bind mount is acceptable.
For DB/storage data, always use named volumes.

### VirtioFS (enabled by default)

Docker Desktop uses VirtioFS for bind mounts (replaces gRPC-FUSE).
Check under Settings > General > "Use VirtioFS" = enabled.
It is 2-3× faster than the old system.

---

## macOS — System configuration

### Prevent sleep during long tasks

The Mac can go to sleep during a benchmark or a long inference.

```bash
# Prevent sleep during a command
caffeinate -i deepeval test run test_skill_quality.py

# Or keep the Mac awake for 4 hours
caffeinate -t 14400 &
```

### Disable App Nap for Ollama

macOS may throttle Ollama when it's not in the foreground:
```bash
defaults write com.ollama.ollama NSAppSleepDisabled -bool YES
```

### Check memory usage

```bash
# Quick memory view
vm_stat | head -10

# Memory pressure (the most important)
memory_pressure

# If "System-wide memory status: The system is in a critical state"
# → too many models loaded, run ollama stop
```

### Monitoring during benchmarks

```bash
# CPU + memory + GPU in real time
top -l 1 -s 0 | head -15

# Metal GPU specifically
sudo powermetrics --samplers gpu_power -i 2000 --show-process-gpu

# Temperature (throttling if too hot)
sudo powermetrics --samplers thermal -i 2000
```

The M3 Ultra has a 90W TDP. If the temperature climbs too high, the system
throttles automatically. In normal lab use this is not a problem.
During intensive parallel benchmarks, keep an eye on it.

---

## Performance anti-patterns

| Anti-pattern | Impact | Alternative |
|--------------|--------|-------------|
| Allocating > 20 GB to Docker Desktop | Ollama swaps, latency ×10 | 16 GB max for Docker |
| Loading 3 concurrent 72B models | Guaranteed swap (~120 GB > 96 GB) | 1 × 72B + 1 × 8B model max |
| Q8 on a 72B model | ~72 GB just for the model | Q4_K_M unless a proven quality need |
| Context 64K+ on a 72B | KV cache blows up (~32 GB) | 16K context by default, raise as needed |
| Bind mount for DB data | Slow I/O in the Docker VM | Named Docker volumes |
| `OLLAMA_KEEP_ALIVE=0` | Reloads the model on every request | `30m` minimum during a work session |
| Benchmarks without `caffeinate` | Mac sleeps in the middle of the test | Always `caffeinate -i <cmd>` |
| Docker `--cpus=28` | Starves macOS and Ollama | 12 cores max for Docker |

---

## Pre-benchmark performance checklist

- [ ] Docker Desktop: 16 GB RAM, 12 CPUs max
- [ ] VirtioFS enabled in Docker Desktop
- [ ] `OLLAMA_KEEP_ALIVE=30m` (no reload during the test)
- [ ] `OLLAMA_NUM_CTX=16384` by default
- [ ] `OLLAMA_MAX_LOADED_MODELS=2`
- [ ] A single 72B model loaded during the benchmark
- [ ] `caffeinate` active
- [ ] App Nap disabled for Ollama
- [ ] `memory_pressure` checked (no "critical")
- [ ] Close memory-hungry apps (browser with many tabs, heavy IDEs)
