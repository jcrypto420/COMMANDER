# Commander Loop

Purpose: keep Josh and Commander moving without building a slop pile.

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
