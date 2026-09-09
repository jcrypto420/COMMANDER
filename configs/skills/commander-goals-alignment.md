---
name: commander-goals-alignment
description: "Use at the end of any loop or session that touched the COMMANDER repo. Checks work just done against the live goals ladder (GOALS.md, NOW.md, SPRINT_69.md) and states one line of alignment or drift — the check that catches slate-metadata theater and scope creep before they compound."
version: 1.0.0
author: Commander
license: private
metadata:
  hermes:
    tags: [commander, goals, alignment, drift-detection, artifact-rule]
    related_skills: [commander-command-center-ops, commander-critic-passes]
---

# Commander Goals Alignment

Hermes has no native goal-tracking subsystem — this skill is that subsystem,
built from the repo's own source-of-truth files. It exists because the
documented failure mode this week was never a bad idea; it was quiet drift:
four consecutive loop passes that "advanced" CI-1 by refreshing slate metadata
without ever building the application, a corny script pack shipped twice
before the constitution caught it, a tracker row that went stale and caused a
duplicate rebuild. This skill is the five-second check that catches drift
while it is still one loop old, not four.

## When to use

- The end of every cron loop pass and every interactive Telegram/chat session
  that read or wrote files in `~/COMMANDER`.
- **Don't use for:** pure read-only status checks with zero repo writes, or
  mid-loop (this is a closing check, not a running commentary).

## Procedure

1. **Read the live ladder, not memory of it:**
   - `GOALS.md` — the priority ladder and which lane is currently active.
   - `NOW.md` — this week's active focus and the current shipped-vs-target
     scoreboard.
   - `TASK_QUEUE.md` — the row for whatever lane this loop touched.
2. **Name the goal-ladder item this run actually advanced.** Not the task ID —
   the real-world outcome: "moved CI-1 toward a submitted application" is
   alignment; "updated CI-1's next-action wording again" is not — that is
   metadata, and the ARTIFACT RULE in `COMMANDER_LOOP.md` already calls
   metadata-only runs failed runs. This skill is that rule's enforcement
   moment, not a new rule.
3. **State it in one line, honestly:**
   - Aligned: `Goal check: advanced <ladder item> — <what actually shipped/changed>.`
   - Drift: `Goal check: DRIFT — this run did not advance any ladder item because <reason>. Next run should <specific correction>.`
   Drift is not a failure to hide; it is information. A run that honestly logs
   drift is worth more than one that silently pads the queue with busywork.
4. **Cross-check the scoreboard claim.** If this run touched anything
   scoreboard-relevant (shipped count, flawless-streak count), verify the
   number against real evidence (a submitted application, a Josh-verdicted
   gate) before writing it anywhere — `model_usage.csv` and self-reported
   counts have both been wrong this week. Trust files and gate verdicts, not
   your own prior claim.
5. **Completion criterion:** one alignment/drift line exists in the loop's log
   entry (`logs/daily_progress.md`) before the loop ends. A loop that ends
   without this line is not finished, even if its primary task looked done.

## What this is not

Not a status report Josh has to read — it lives in the log, not the dispatch.
Not a second task-tracker — `TASK_QUEUE.md` stays the single board. Not a
excuse to add process; if a loop is obviously and trivially aligned (e.g. it
built the exact artifact its queue row named), the one-line check still takes
five seconds and still gets written — brevity is not an exemption.
