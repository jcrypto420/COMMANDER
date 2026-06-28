# Model Delegation + Token Budget

Purpose: keep Commander moving every day without burning premium usage or hitting
GPT-5.5 blockage. Default posture: **premium is a scalpel, not a shovel**.

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

## Subagent patterns

### Good delegation

- “Research public Mog/Joycat sources and return 10 bullets with URLs.”
- “Extract action items from these files.”
- “Compare 4 sprint options in a table.”
- “Draft 20 post hooks from this brief.”

### Bad delegation

- “Browse forever and tell me everything.”
- “Use premium model to generate 100 captions.”
- “Spawn several unrestricted agents with all tools.”
- “Let subagents decide strategy without parent review.”

## Toolset discipline

Use the smallest toolset that can complete the job:

- Research: `web` only.
- Repo edits: `file`, maybe `terminal` for verification.
- Code work: `file`, `terminal`, maybe `coding`.
- Browser only when a page requires interaction.
- Avoid loading all tools into cron jobs or subagents unless necessary.

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
