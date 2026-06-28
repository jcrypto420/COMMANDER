# Model Delegation + Token Budget

Purpose: keep Commander moving every day without burning premium usage or hitting
GPT-5.5 blockage. Default posture: **premium is a scalpel, not a shovel**.
Commander should operate like a project lead: route tasks to the right model,
delegate narrow subtasks, integrate results, scrutinize/review, and keep the
repo source of truth updated.

## Core policy

1. **Main daily work runs on cheap/default model**
   - Default: `openai-codex/gpt-5.4-mini` or cheapest capable Tier 1 model.
   - Use for repo updates, task planning, drafts, summaries, research synthesis,
     and routine coding.

2. **GPT-5.5 only for high-leverage checkpoints**
   - Onboarding / strategy interviews.
   - Final review of important plans.
   - Hard debugging or architecture after cheaper attempts fail.
   - High-stakes legal/financial-adjacent drafting as draft review only.

3. **Subagents do not mean “premium by default”**
   - Delegate research, extraction, comparison tables, and first drafts to cheap
     models / restricted toolsets.
   - Parent agent should receive only compact summaries and source links.
   - Do not spawn premium subagents for bulk crawling, long browsing, or repetitive
     content generation.

4. **Compress context aggressively through files**
   - Store durable state in repo files: `NOW.md`, `TASK_QUEUE.md`, project docs,
     `SPRINT_69.md`, research briefs, and logs.
   - Start new sessions from files instead of carrying giant chats.
   - Use `session_search` only when needed to recover prior conversation details.

5. **Josh should not micromanage model choice**
   - Commander should proactively choose the cheapest capable model/workflow.
   - Explain escalations only when they affect cost, risk, approvals, or timing.
   - Keep moving with cheaper routes when premium usage is blocked.

## Practical Hermes capability map

- The active chat model can be chosen when starting a session with
  `commander chat -m <model>` or changed interactively with `/model`.
- The built-in `delegate_task` tool runs subagents in isolated contexts, but
  child model selection is inherited from Hermes delegation config; this tool is
  best for narrow parallel work with compact summaries.
- When a specific model is needed for an isolated subtask, Commander can spawn a
  separate one-shot Hermes process with `/home/josh/.local/bin/hermes chat -q ...
  -m <model> --provider <provider>` and a restricted toolset. Use this sparingly
  and log the decision.
- Cron jobs can pin model/provider per job when needed; recurring jobs should
  default cheap and use restricted toolsets.

## Project-lead workflow

For any non-trivial task, Commander should run this loop:

1. **Triage** — classify the task: mechanical, research, creative draft, coding,
   strategy, safety/legal/financial-adjacent, or final review.
2. **Route** — pick model/toolset:
   - mechanical/status → script or cheap model,
   - research/extraction → cheap subagent with narrow tools,
   - first drafts → cheap model,
   - hard synthesis/final review → premium only when justified.
3. **Delegate** — split independent subtasks into small briefs with explicit
   output shape, source requirements, and tool limits.
4. **Integrate** — parent Commander merges results into repo files or a compact
   decision brief; do not dump raw subagent sprawl into the final answer.
5. **Scrutinize** — run at least one review pass for important outputs:
   - factual/source check for research,
   - safety/approval check for public/outbound/financial/system actions,
   - quality/brand check for Bad Boys/Joycat content,
   - test/lint check for code.
6. **Escalate if needed** — use GPT-5.5 only when the cheap route is uncertain,
   high-impact, or failed twice.
7. **Update truth** — write the decision/result to repo docs, logs, and task
   queue so future cheap sessions can continue without loading old chat.

## Routing table

| Work type | Default route | Escalate when |
|-----------|---------------|---------------|
| Daily money loop | Tier 1 mini / cheap hosted | blocked twice or final strategic decision |
| Research collection | Subagent with `web` only, cheap model | source conflict or important final memo |
| Research synthesis | Tier 1 cheap | final review for major decision |
| Draft social/content ideas | Tier 0/1 cheap | only for final brand voice review |
| Asset inventory | File tools + cheap model | never unless complex IP/legal issue |
| Code/doc edits | Tier 1 cheap | hard bug, architecture, security-sensitive |
| Phone summaries | no-agent script or cheap model | never |
| Final public/outbound copy | Tier 1 draft, optional GPT-5.5 review | before major launch only |

## Review lanes

| Output | First pass | Review pass | Approval before action |
|--------|------------|-------------|-------------------------|
| Research brief | cheap web subagent | parent source/safety check | no, unless used publicly |
| Social/content drafts | cheap creative draft | brand + safety review | yes before posting |
| Launch plan | cheap synthesis | premium or parent strategic review | yes before public/spend |
| Code/scripts | cheap coding/session | tests/lint + parent review | depends on side effects |
| Phone/cron summary | script or cheap model | parent sanity check | no for local/log, yes for sending until channel approved |
| Financial/DeFi content | cheap draft/research | premium review if important | yes; never final advice/autonomous action |

## Escalation triggers

Escalate to GPT-5.5 or another premium model only when one is true:

- A decision could materially affect the 69-day sprint path.
- A draft will be public, high-visibility, or reputationally sensitive.
- A cheaper model produced conflicting/low-confidence results twice.
- The task is architecture/security-sensitive.
- The work is legal/financial-adjacent and needs careful review as a draft.

Do **not** escalate for volume, formatting, routine summaries, bulk captions, or
open-ended browsing.

## Subagent patterns

### Good delegation

- “Research public Mog/Joycat sources and return 10 bullets with URLs.”
- “Extract action items from these files.”
- “Compare 4 sprint options in a table.”
- “Draft 20 post hooks from this brief.”
- “Review this launch packet for safety/approval risks only.”
- “Check these 8 claims against their source links and flag weak claims.”

### Bad delegation

- “Browse forever and tell me everything.”
- “Use premium model to generate 100 captions.”
- “Spawn several unrestricted agents with all tools.”
- “Let subagents decide strategy without parent review.”
- “Spawn a premium model because we have many small tasks.”

## Toolset discipline

Use the smallest toolset that can complete the job:

- Research: `web` only.
- Repo edits: `file`, maybe `terminal` for verification.
- Code work: `file`, `terminal`, maybe `coding`.
- Browser only when a page requires interaction.
- Avoid loading all tools into cron jobs or subagents unless necessary.

## One-shot model-specific worker pattern

Use this only when the model must differ from the active session and the task is
bounded. Prefer `delegate_task` for quick inherited-model subtasks.

```bash
/home/josh/.local/bin/hermes chat \
  --provider openai-codex \
  -m gpt-5.4-mini \
  -t file,terminal \
  -q "Read MODEL_DELEGATION.md and review TASK_QUEUE.md for stale statuses. Return only a 10-bullet summary; do not edit files."
```

Rules:

- Give the worker a compact brief and exact output shape.
- Restrict toolsets.
- Prefer read-only unless edits are explicitly needed.
- Parent Commander verifies any claimed file edits or external side effects.
- Log meaningful model usage to `logs/model_usage.csv` where possible.

## Cron discipline

For recurring jobs:

- Prefer `no_agent=True` scripts for fixed-format status/watchdog jobs.
- Use agent cron only when reasoning is required.
- Restrict `enabled_toolsets` on cron jobs.
- Keep cron prompts self-contained and short.
- Have cron write compact summaries to repo/log files, not huge chat transcripts.

## Session discipline

Use a fresh cheap session for most work:

```bash
commander chat -m gpt-5.4-mini
```

Use premium only deliberately:

```bash
commander chat -m gpt-5.5
```

Recommended habit:

- Run day-to-day execution on mini.
- Ask for GPT-5.5 only: “review this plan for blind spots” or “solve this hard blocker.”
- After premium produces the decision, write the decision to repo docs and return
  to mini.

## Anti-blockage workflow

If premium usage is low/blocked:

1. Continue on `gpt-5.4-mini`.
2. Convert the current task into a compact brief file.
3. Use cheap subagents for research/extraction.
4. Use local/no-agent scripts for mechanical work.
5. Queue premium review for later instead of stopping.

## Budget tripwires

- Premium model used for more than one long session in a day → stop and summarize
  to files, then continue on mini.
- Context is getting huge → write a brief, commit/push if approved, start a fresh
  session.
- Subagent output exceeds what is needed → ask for smaller summaries next time.
- Repetitive generation request → use cheap model or script templates.

## What “always moving forward” means

Even without premium access, Commander can still:

- update task queue and logs,
- draft content and offers,
- inventory assets,
- run public research,
- create approval packets,
- prepare phone summaries,
- improve automations,
- create GitHub-visible progress.

Do not wait for GPT-5.5 unless the task truly requires premium reasoning.
