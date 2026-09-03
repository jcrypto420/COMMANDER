# PROVIDERS.md

Inference providers, base URLs, and env-var patterns. **Placeholders only — no
real keys here.** Real keys go in a local `.env` (see `configs/`, `SECURITY.md`).

Prefer **OpenAI-compatible** endpoints to reduce lock-in.

## Day-one order

```text
1. Nous Portal OR OpenRouter  -> quickest working Hermes setup
2. Venice AI                   -> OpenAI-compatible alternative
3. Ollama local               -> tiny low-cost tasks
4. Additional cheap providers  -> after the model router exists
```

Don't perfect every provider on day one.

## Provider reference

| Provider | Base URL (VERIFY) | Env var | OpenAI-compatible | Tier |
|----------|-------------------|---------|-------------------|------|
| OpenRouter | `https://openrouter.ai/api/v1` | `OPENROUTER_API_KEY` | yes | 1 |
| Nous Portal | VERIFY in docs | `NOUS_PORTAL_API_KEY` | likely | 1 |
| Venice AI | `https://api.venice.ai/api/v1` (VERIFY) | `VENICE_API_KEY` | yes | 1 |
| Hugging Face | `https://router.huggingface.co/...` (VERIFY) | `HF_TOKEN` | varies | 1 |
| GitHub Models | VERIFY in docs | `GITHUB_MODELS_TOKEN` | varies | 1 |
| Together | `https://api.together.xyz/v1` | `TOGETHER_API_KEY` | yes | 1 |
| Groq | `https://api.groq.com/openai/v1` | `GROQ_API_KEY` | yes | 1 |
| DeepInfra | `https://api.deepinfra.com/v1/openai` | `DEEPINFRA_API_KEY` | yes | 1 |
| Ollama (Pi) | `http://localhost:11434/v1` | none | yes | 0 |
| Ollama (LAN) | `http://<mac-mini-tailscale-ip>:11434/v1` | none | yes | 0 |
| "Surplus" / experimental | VERIFY | per-provider | VERIFY | 0/1 |
| Claude | `https://api.anthropic.com` | `ANTHROPIC_API_KEY` | no (native) | 2 |
| OpenAI/GPT | `https://api.openai.com/v1` | `OPENAI_API_KEY` | yes | 2 |

> **VERIFY** = confirm the exact base URL / auth from the provider's live docs
> before relying on it. URLs change.
