# LOCAL_MODELS.md

Plan for local inference. The Pi is the orchestrator, **not** the heavy LLM box.

## Raspberry Pi 4 limits

- Do not expect the Pi 4 to run large local LLMs well.
- It can run tiny models for cheap, low-stakes tasks only.
- Heavy local inference belongs on a Mac mini / custom PC / GPU machine later.
- Hermes still runs on the Pi as operator/orchestrator and routes heavy
  inference elsewhere.

## Phases

```text
Phase A — Pi tiny-model test
  - Install Ollama only if Josh approves (scripts/install_ollama_optional.sh).
  - Test tiny models (e.g. qwen2.5:0.5b/1.5b, gemma small, phi).
  - Use only for Tier 0 low-stakes tasks.
  - Record performance honestly (speed, quality, RAM).

Phase B — Mac mini / custom PC local AI server
  - Run stronger Qwen / GLM / Gemma / Llama / Hermes models.
  - Expose an OpenAI-compatible endpoint over Tailscale.

Phase C — Hermes model router chooses local/cheap/premium per task
  - Tier 0 → local; Tier 1 → cheap hosted; Tier 2 → premium.
```

## Model test matrix (fill in during Phase A)

| Model | Host | Task type | Speed | Quality | RAM | Keep? |
|-------|------|-----------|-------|---------|-----|-------|
| qwen2.5:0.5b | Pi | summarize | | | | |
| qwen2.5:1.5b | Pi | extract tasks | | | | |
| gemma (small) | Pi | classify | | | | |

> Never use Pi-hosted local models for high-stakes legal/financial/coding/final
> strategic decisions (see `MODEL_ROUTER.md`).
