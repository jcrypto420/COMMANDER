# Phone + Autonomy Workflow

Purpose: make Commander easy to use from Josh's phone while increasing autonomy
without exposing money, secrets, public posting, or system control too quickly.

## Recommended operating model

Use three layers:

1. **GitHub / repo = source of truth**
   - Durable docs, task queue, project files, and daily progress live here.
   - Good for review, history, and recovery.

2. **Phone channel = lightweight command and approval surface**
   - Josh should be able to send short commands, voice/text notes, approvals,
     and corrections from his phone.
   - Phone messages should be summaries, blockers, and approval requests — not
     noisy full logs.

3. **Commander / Pi = execution engine**
   - Runs daily loop, drafts assets, tracks tasks, edits docs, and prepares
     approval-ready actions.
   - Does not spend, send, post, deploy, or touch secrets without approval.

## Autonomy levels

### Level 1 — current / safe default

Commander can:

- Inspect repo files.
- Edit docs, plans, trackers, scripts inside this repo.
- Draft content, outreach, launch plans, research memos, and task lists.
- Run read-only or non-destructive verification.
- Update logs and task queue.
- Run scheduled draft-only jobs.

Commander cannot without approval:

- Spend money or API credits.
- Send/post/apply/upload/deploy.
- Add secrets or credentials.
- Install packages, use sudo, modify services, or expose ports.
- Push to GitHub unless Josh approves the specific push or a bounded push rule.
- Take financial, DeFi, custody, trading, or legal actions.

### Level 2 — proposed next step

After Josh approves a phone channel, Commander can:

- Send daily summaries, blockers, and approval requests to the phone channel.
- Accept short phone replies like "approve draft 2", "pause", "run today's loop",
  or "focus Bad Boys today".
- Keep all public/outbound actions approval-gated.

Suggested bounded push rule for GitHub:

- Commander may auto-commit and push **docs/log/task updates only** when they are
  produced by the daily loop or explicitly approved by Josh.
- Code changes, scripts that affect runtime, config changes, secrets, services,
  or deployment changes still require explicit approval.

### Level 3 — later, after trust

Commander can execute bounded revenue workflows after Josh approves:

- the workflow,
- the budget,
- the accounts/tools used,
- the allowed actions,
- stop-loss / risk limits,
- what requires a fresh approval.

Example later workflow: "draft and queue 7 Bad Boys posts, send them to Josh for
approval, then post only the approved ones through the approved pseudonymous
account."

## Phone channel recommendation

Best first path: **Telegram or another Hermes-supported gateway channel** for
summaries and approvals, with GitHub remaining the durable source of truth.

Why:

- Works from phone.
- Hermes gateway supports platform delivery and slash-style approvals.
- Can keep messages narrow: summaries, blockers, approvals.
- Avoids exposing broad SSH/system access as the main phone workflow.

Tailscale/SSH remains useful for emergency direct access, but it is not the
friendliest daily interaction surface.

Setup checklist: `TELEGRAM_SETUP.md`.

## Setup steps that require Josh approval

- Pick the phone channel: Telegram is the recommended first test.
- Configure Hermes gateway for that platform.
- Add any required token/secret locally, never in git.
- Restart/install gateway if needed.
- Test with a harmless status message.
- Decide whether cron jobs should deliver to that channel or stay local-only.

## Daily phone summary format

Commander should keep phone updates short:

```text
Daily MOG Loop — YYYY-MM-DD

Picked: <one task>
Done: <what changed>
Needs approval: <specific yes/no action, if any>
Metric: revenue=$0, followers=?, sales=?, shipped=?
Next: <one next step>
```

## Approval request format

```text
Approval request: <action>
Why: <business reason>
Risk: <low/medium/high + why>
Cost: <$ or $0>
Reversible: <yes/no>
Exact command/action: <what will happen>
Reply: APPROVE / DENY / EDIT
```

## Immediate recommendation

Do not broaden autonomy by disabling approvals or using yolo mode.

Instead:

1. Keep Level 1 autonomy active.
2. Approve Level 2 phone summaries/approval requests once a channel is chosen.
3. Keep public posting, spending, sending, secrets, system changes, and DeFi
   actions locked behind explicit approval.
