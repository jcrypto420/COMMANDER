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

## Delegation rule

See `MODEL_DELEGATION.md` for the operating workflow.

- **Current routing:** interactive strategy/review stays on `openai-codex/gpt-5.6-terra`; `openai-codex/gpt-5.4-mini` passed a live structured-operator benchmark in 19 seconds and is the recurring-worker default.
- **Pinned cron rule (verified 2026-07-25):** all six active agent cron jobs explicitly pin `openai-codex/gpt-5.4-mini`. OpenRouter is not a live fallback while its credential is exhausted (402). Use deterministic scripts for mechanical jobs and reserve agent runs for real reasoning.
- GPT-5.6-terra is reserved for high-leverage synthesis, hard debugging, and strategy—not repetitive cron prose.
- Subagents should use restricted toolsets and return compact summaries; do not
  use premium subagents for bulk research or repetitive content generation.
- If premium usage is blocked, continue with cheap models, file briefs,
  no-agent scripts, and compact subagent tasks instead of stopping.

Commander should operate as the project lead: route, delegate, integrate,
review, and only escalate to premium when the task meets the triggers in
`MODEL_DELEGATION.md`.
