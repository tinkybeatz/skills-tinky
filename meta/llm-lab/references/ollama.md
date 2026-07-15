# Ollama — Configuration reference

## Installation

```bash
brew install ollama
```

Ollama runs as a daemon: `ollama serve` (automatic after the brew install).

## Recommended models for the lab

### Tier 1 — Always available
```bash
ollama pull qwen3:8b        # ~5 GB, simple tasks, fast (80-120 tok/s)
ollama pull qwen3:72b       # ~40 GB, complex skills (15-25 tok/s)
```

### Tier 2 — To test
```bash
ollama pull llama4-scout    # ~30 GB, MoE, good quality/speed ratio
ollama pull deepseek-r1:70b # ~40 GB, advanced reasoning
```

### Tier 3 — Specialized
```bash
ollama pull codestral       # Code generation (Mistral)
ollama pull nomic-embed-text # Embeddings for RAG
```

## Memory management (96 GB M3 Ultra)

The unified memory is shared between CPU, GPU, and models.

Approximate memory budget:
- macOS + apps: ~10-15 GB
- Docker containers: ~5-8 GB
- **Available for models: ~73-81 GB**

Viable combinations:
- 1× 72B + 1× 8B = ~45 GB ✅ (~30 GB left)
- 2× 72B = ~80 GB ⚠️ (tight, possible but not recommended)
- 1× 72B alone = ~40 GB ✅ (comfortable)

## Useful commands

```bash
ollama list                  # Downloaded models
ollama ps                    # Models currently loaded in memory
ollama stop <model>          # Unload a model from memory
ollama show <model>          # Model details (parameters, quantization)
ollama rm <model>            # Delete a model from disk
```

## Advanced configuration

### Environment variables
```bash
export OLLAMA_HOST=0.0.0.0:11434    # Listen on all interfaces (for Docker)
export OLLAMA_NUM_PARALLEL=2         # Max parallel requests
export OLLAMA_MAX_LOADED_MODELS=2    # Max concurrently loaded models
export OLLAMA_KEEP_ALIVE=5m          # Keep the model in memory after the last request
```

### Custom Modelfile (optional)
To tune a model's parameters:
```
FROM qwen3:72b
PARAMETER temperature 0.7
PARAMETER num_ctx 32768
SYSTEM "You are a technical assistant."
```

## API

Main endpoint: `http://localhost:11434`

```bash
# List the models
curl http://localhost:11434/api/tags

# Generate (streaming)
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:8b",
  "prompt": "Hello"
}'

# Chat (OpenAI-compatible)
curl http://localhost:11434/v1/chat/completions -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "Hello"}]
}'
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ollama serve` fails | Check that no other process is using :11434 |
| Model slow on the first prompt | Normal — loading into memory (~10-30s for 72B) |
| "out of memory" | `ollama stop` the other models, check `ollama ps` |
| Docker can't reach Ollama | `OLLAMA_HOST=0.0.0.0:11434` then restart |
