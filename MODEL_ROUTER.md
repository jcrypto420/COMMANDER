# MODEL_ROUTER.md

Route every task to the **cheapest model that can do it well**. Design around a
router, not one fixed provider. See `configs/model_router_template.yaml` for the
machine-readable version and `PROVIDERS.md` for endpoints.

## Tier 0 — Local / nearly free

**Use for:** summarization, classification, text cleaning, task extraction,
low-stakes first drafts, research organization, repetitive formatting.

**Providers:** Ollama on Pi (tiny models only); later Ollama on Mac mini / custom
PC (stronger models).

**Candidates:** Qwen small/medium, GLM (if supported), Gemma, Phi, small Llama,
Hermes open models if feasible.

**Rule:** Never rely on Pi-hosted local models for high-stakes legal, financial,
coding, or final strategic decisions.

## Tier 1 — Cheap hosted

**Use for:** general agent work, routine coding, business drafts, research
synthesis, brainstorming, task planning.

**Providers:** OpenRouter cheap/free, Nous Portal, Venice AI, Hugging Face
Inference Providers, GitHub Models, Together/Fireworks/Groq/DeepInfra if
cost-effective.

**Rule:** Prefer OpenAI-compatible APIs to reduce integration lock-in.

## Tier 2 — Premium / expensive

**Use for:** complex coding, architecture decisions, legal/financial-adjacent
drafting, final review of important materials, debugging stuck issues, strategy.

**Providers:** Claude, GPT-class, premium OpenRouter/Nous Portal models.

**Rule:** Cost-aware. Never use premium for bulk repetitive work.

## Fallback logic

```text
1. Try Tier 0 if task is low-stakes and a local model is available.
2. Else Tier 1 (cheapest capable hosted model).
3. Escalate to Tier 2 only if: high value, high stakes, or Tier 1 failed twice.
4. On provider error/timeout: fall back to the next provider in the same tier.
5. Log provider/model/tokens/cost every call (logs/model_usage.csv).
```
