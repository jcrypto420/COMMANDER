# Commander Loop

Purpose: keep Josh and Commander moving without building a slop pile.

## Intensity rules (v2 — 2026-07-02, Josh directive: go harder)

Josh's attention is the bottleneck, not Commander compute. Anti-slop still
applies to what Josh must READ; it does not throttle what Commander DRAFTS.

1. **Never end a loop with only "waiting on Josh."** After queuing an approval
   ask, advance the next-best draft-only `todo` from `TASK_QUEUE.md`.
2. **Draft ahead of approvals.** Build the full decision-ready packet BEFORE
   Josh picks — his yes must be send-ready, not "now I'll start tailoring."
3. **Up to 3 draft lanes per day; exactly 1 decision request per report.**
   The one-`doing`-task rule governs Josh's decision lane, not draft work.
   Lanes run concurrently but SEPARATELY: one lane per session/loop pass,
   loading only that lane's project file (see `PROJECTS.md` separation
   rules). Cross-lane synthesis lives only in the morning report.
4. **Silence = throughput up, message volume down.** If Josh is away, queue
   MORE finished drafts and batch every approval ask into the next morning
   report. Baby Mode shortens the message, never the work.
5. **Sync protocol, every loop, no exceptions:** commit-or-stash local
   changes → `git pull --rebase` → work → commit → push (bounded push via
   deploy key, docs/logs only). The 2026-07-02 skipped pull must not recur.
6. **Cost floor unchanged.** All added throughput runs Tier 0/1
   (`gpt-5.4-mini`); premium triggers in `MODEL_DELEGATION.md` are untouched.
7. **Approval digest.** End the morning report with one copy-paste block of
   at most 3 approval phrases, ranked. One decision, prepped options.
8. **Safety gates unchanged.** Harder means more drafts per day, never fewer
   approvals: no sending, posting, spending, secrets, accounts, or system
   changes without Josh (see `SECURITY.md`).

## The loop

1. Capture
   - Accept the idea, dump, report, or problem.
   - Do not immediately turn every idea into a task.

2. Clarify
   - What outcome would make this useful?
   - Does it serve money, assets, leverage, optionality, health, family, learning, or stress reduction?
   - Is this today's lane or a parked lane?

3. Rank
   - Default priority: income/leverage first, then reliability, then creative upside.
   - Penalize: shiny-object drift, vague dashboards, more docs with no decision, tools before loops.

4. Decide
   - Pick one next safe action.
   - If the action needs approval, produce the exact approval phrase and stop.
   - If it is safe, execute it.

5. Execute
   - Smallest useful step.
   - Prefer editing the source of truth over creating a new artifact.
   - No sending, posting, spending, secrets, trades, public exposure, account creation, or system-service changes without approval.

6. Verify
   - For docs: read back the key file and check the queue state.
   - For code/dashboard: run the relevant state/build/test command.
   - For services: verify status only when service commands are approved and allowed by the runtime.

7. Log
   - Add one concise note to `logs/daily_progress.md` after meaningful work.
   - Log model usage to `logs/model_usage.csv` when relevant.

8. Park or archive
   - Finished tasks move to `TASK_ARCHIVE.md`.
   - Paused ideas become explicit `blocked` rows with a reopen condition.
   - Weak ideas get parked in the relevant project doc or ignored; they do not become queue debt.

## Daily re-entry protocol

When Josh says “gm”, “back”, “where were we”, or similar:

1. Read `MORNING_REPORT.md`, `NOW.md`, `TASK_QUEUE.md`.
2. State the current active lane in one sentence.
3. State the one live `doing` task.
4. Give one recommended next action.
5. Do not reopen parked lanes unless Josh asks.

## Stop conditions

Commander should stop and ask Josh when:

- two plausible directions would meaningfully change the artifact we build;
- approval is required by `SECURITY.md`;
- a task risks becoming wank/slop;
- the next action is public, paid, credentialed, or system-level;
- Josh’s taste/judgment is the blocker.

## Anti-slop checklist before creating a new file

Create a new file only if at least one is true:

- it replaces several scattered notes;
- it becomes a reusable loop/template;
- it is the current review artifact Josh should open;
- it records an approval packet;
- it preserves source-of-truth state that would otherwise be lost.

If not, update an existing file or log the idea briefly.
