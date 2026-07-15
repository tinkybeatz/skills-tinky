# LiteLLM Proxy — Configuration reference

## Role in the lab

LiteLLM is the central gateway. Every LLM request goes through it, whether it
targets local Ollama, the Claude API, or the OpenAI API. This enables:
- A single endpoint for everything (`http://localhost:4000/v1/`)
- Intelligent routing (fallback, load-balancing)
- Cost tracking per virtual key
- Automatic logging to Langfuse

## Configuration — litellm-config.yaml

```yaml
model_list:
  # --- Local models via Ollama ---
  - model_name: qwen3-8b
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://host.docker.internal:11434

  - model_name: qwen3-72b
    litellm_params:
      model: ollama/qwen3:72b
      api_base: http://host.docker.internal:11434

  - model_name: llama4-scout
    litellm_params:
      model: ollama/llama4-scout
      api_base: http://host.docker.internal:11434

  - model_name: deepseek-r1-70b
    litellm_params:
      model: ollama/deepseek-r1:70b
      api_base: http://host.docker.internal:11434

  # --- Cloud models ---
  - model_name: claude-opus
    litellm_params:
      model: claude-opus-4-6
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-sonnet
    litellm_params:
      model: claude-sonnet-4-6
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-haiku
    litellm_params:
      model: claude-haiku-4-5-20251001
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4.1
    litellm_params:
      model: gpt-4.1
      api_key: os.environ/OPENAI_API_KEY

  - model_name: gpt-4.1-mini
    litellm_params:
      model: gpt-4.1-mini
      api_key: os.environ/OPENAI_API_KEY

# --- Default routing ---
router_settings:
  routing_strategy: simple-shuffle  # or latency-based-routing
  num_retries: 2
  timeout: 120
  allowed_fails: 3

# --- Fallback ---
litellm_settings:
  fallbacks:
    - qwen3-72b: [claude-sonnet]     # If local fails → cloud
    - qwen3-8b: [claude-haiku]
  success_callback: ["langfuse"]      # Automatic logging
  failure_callback: ["langfuse"]

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/LITELLM_DATABASE_URL
```

## Environment variables (.env)

```bash
# LiteLLM
LITELLM_MASTER_KEY=sk-master-CHANGE-ME
LITELLM_DATABASE_URL=postgresql://litellm:litellm@litellm-postgres:5432/litellm

# Cloud providers
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Langfuse callback
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://langfuse:3000
```

## Docker Compose (excerpt)

```yaml
litellm:
  image: ghcr.io/berriai/litellm:main-v1.67.0  # Pin the version
  ports:
    - "4000:4000"
  volumes:
    - ./litellm-config.yaml:/app/config.yaml
  command: ["--config", "/app/config.yaml", "--port", "4000"]
  env_file: .env
  extra_hosts:
    - "host.docker.internal:host-gateway"
  depends_on:
    litellm-postgres:
      condition: service_healthy
    litellm-redis:
      condition: service_healthy
  networks:
    - llm-lab

litellm-postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_DB: litellm
    POSTGRES_USER: litellm
    POSTGRES_PASSWORD: litellm
  volumes:
    - litellm-pg-data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U litellm"]
    interval: 5s
    timeout: 3s
    retries: 5
  networks:
    - llm-lab

litellm-redis:
  image: redis:7-alpine
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 5s
    timeout: 3s
    retries: 5
  networks:
    - llm-lab
```

## Usage

### List the available models
```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-master-CHANGE-ME"
```

### Chat request
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-master-CHANGE-ME" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-8b",
    "messages": [{"role": "user", "content": "Hello, what is your name?"}]
  }'
```

### Create a virtual key
```bash
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-CHANGE-ME" \
  -d '{"key_alias": "test-key", "max_budget": 10.0}'
```

## Adding a new model

1. Install it in Ollama: `ollama pull <model>`
2. Add the entry in `litellm-config.yaml`
3. Restart LiteLLM: `docker compose restart litellm`
4. Verify: `curl http://localhost:4000/v1/models`
