# OpenClaw — Configuration reference

## Role in the lab

OpenClaw is the runtime that executes SKILL.md skills on any LLM.
It replaces Claude Code for multi-model testing while keeping the same skill format.

## Docker installation

```yaml
# docker-compose.yml excerpt
openclaw:
  image: ghcr.io/openclaw/openclaw:latest  # Pin in production
  ports:
    - "3007:3007"
  volumes:
    - ~/.openclaw:/root/.openclaw
    - ~/llm-lab/skills:/root/openclaw/workspace/skills
  environment:
    - OPENCLAW_PROVIDER=openai-compatible
    - OPENCLAW_API_BASE=http://litellm:4000/v1
    - OPENCLAW_API_KEY=${LITELLM_MASTER_KEY}
    - OPENCLAW_MODEL=qwen3-72b
  extra_hosts:
    - "host.docker.internal:host-gateway"
  networks:
    - llm-lab
```

Key point: OpenClaw points at LiteLLM (not directly at Ollama or Claude).
Switching models = changing `OPENCLAW_MODEL` in the config.

## Configuration (~/.openclaw/config.json)

```json
{
  "providers": {
    "llm-lab": {
      "type": "openai-compatible",
      "apiBase": "http://localhost:4000/v1",
      "apiKey": "sk-master-CHANGE-ME",
      "models": {
        "default": "qwen3-72b",
        "fast": "qwen3-8b",
        "reasoning": "deepseek-r1-70b",
        "cloud": "claude-opus"
      }
    }
  },
  "defaultProvider": "llm-lab",
  "workspace": {
    "root": "~/openclaw/workspace"
  },
  "security": {
    "allowClawHub": false,
    "sandbox": {
      "enabled": true,
      "backend": "docker"
    }
  }
}
```

## Structure of an OpenClaw skill

```
~/.openclaw/workspace/skills/<name>/
├── SKILL.md          # Instructions (same format as Claude Code)
└── references/       # Reference files (optional)
```

### SKILL.md format

```yaml
---
name: my-skill
description: >
  Description of the skill and when to trigger it.
---

# Skill title

Instructions in markdown...
```

Identical to Claude Code except for the tool names (see the mapping in the main SKILL.md).

## Porting a skill Claude Code → OpenClaw

### Semi-automatic porting script

```bash
#!/bin/bash
# port-skill.sh <skill-name>
SKILL_NAME=$1
SRC="$HOME/.claude/skills/$SKILL_NAME"
DST="$HOME/llm-lab/skills/$SKILL_NAME"

if [ ! -d "$SRC" ]; then
  echo "Skill $SKILL_NAME not found in ~/.claude/skills/"
  exit 1
fi

cp -r "$SRC" "$DST"

# Adapt the tool names
cd "$DST"
find . -name "*.md" -exec sed -i '' \
  -e 's/\bRead\b/read_file/g' \
  -e 's/\bEdit\b/edit_file/g' \
  -e 's/\bWrite\b/write_file/g' \
  -e 's/\bGrep\b/search/g' \
  -e 's/\bGlob\b/search/g' \
  -e 's/\bWebSearch\b/web_search/g' \
  -e 's/\bWebFetch\b/web_fetch/g' \
  {} +

echo "Skill ported to $DST"
echo "⚠️  Check manually: references to absolute paths, Agent/subagent calls"
```

### Manual porting checklist

- [ ] Tool names adapted (see the mapping in SKILL.md)
- [ ] Absolute paths `~/.claude/` → `~/openclaw/workspace/`
- [ ] `Agent` (subagent) calls → not supported, restructure into sequential steps
- [ ] References to MCP servers → check OpenClaw MCP compatibility
- [ ] Test with a representative prompt on the target model

## Useful commands

```bash
# List the installed skills
openclaw skill list

# Test a skill in interactive mode
openclaw chat --skill my-skill --model qwen3-72b

# Run a one-shot task
openclaw run --skill my-skill --prompt "My task here" --model qwen3-8b

# Switch models on the fly
openclaw chat --model claude-opus
```

## Multi-channel (future phase)

OpenClaw natively supports Slack, Telegram, WhatsApp, and Discord.
Configure it in `~/.openclaw/config.json` under `channels`.
Enable it once the lab is stabilized (Phase 5+).
