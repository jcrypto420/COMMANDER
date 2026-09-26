# COST_CONTROL.md

Keep token/API spend low without crippling output quality.

## Rules

1. Default to the cheapest model capable of the task.
2. Use local/Ollama for bulk low-stakes work.
3. Use cheap hosted models for normal work.
4. Use premium models only for hard or high-value tasks.
5. Log model/provider usage where possible.
6. Track estimated daily spend.
7. Use small prompts and compact context.
8. Do not load unrelated project files.
9. Cache recurring summaries.
10. Use **briefing files** so agents read 1–3 compact files, not whole chat
    histories.
11. Require human approval for purchases, subscriptions, deployments,
    credentials, and irreversible actions.
12. Treat GPT-5.5 as a review/escalation model, not the default execution model.
13. Use `MODEL_DELEGATION.md` before spawning subagents or starting long sessions.

## Logs

- `logs/model_usage.csv` — one row per model call.
- `logs/daily_progress.md` — what advanced today + estimated spend.

### `model_usage.csv` columns

```text
date,task_id,project,provider,model,input_tokens,output_tokens,estimated_cost,outcome,next_action
```

## Daily spend awareness

At the end of the daily loop, sum `estimated_cost` for the day into
`logs/daily_progress.md` and flag if it exceeds the soft budget (set your own,
e.g. `$1.00/day` to start). If over budget, shift more work to Tier 0/1.

## Usage-blockage prevention

- Prefer fresh cheap sessions over long premium sessions.
- Store context in repo briefs instead of carrying huge chat history.
- Use subagents for narrow research/extraction, not open-ended premium work.
- If a premium model is unavailable, keep moving with cheap/default models and
  queue premium review for later.
