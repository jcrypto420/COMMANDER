---
name: commander-night-shift
description: "Run at the START of the first loop pass after boot. Consumes Josh's overnight queue from NIGHT_SHIFT.md: drafts every queued item before any other lane, logs results under Delivered with repo paths, and hands the list to the morning dispatch so Josh's 7am judgment block opens with finished drafts, not options."
version: 1.0.0
author: Commander
license: private
metadata:
  hermes:
    tags: [commander, night-shift, overnight-queue, drafts, morning-dispatch]
    related_skills: [commander-command-center-ops, commander-goals-alignment]
---

# Commander Night Shift

Josh queues at 9:15pm; the Pi is off overnight; you boot in the morning. This
skill turns his bedtime list into judged-ready drafts before he sits down.
"I wish you could keep working when i sleep" (Josh, 2026-07-07) — this is how,
within the physics of a Pi that sleeps too.

## When to use

- First loop pass after boot, before selecting any other lane.
- **Don't use for:** subsequent passes the same day (queue is consumed once),
  or when "Tonight's queue" is empty — then proceed to the normal loop.

## Procedure

1. `git pull --rebase` first (the queue was written on the Mac last night).
2. Read `NIGHT_SHIFT.md` → "Tonight's queue". For each unchecked item:
   - **Draft-only check:** no sending, spending, posting, deploying, account
     creation, or new systems/tools/layers. Violating items get annotated
     `[held: needs Josh live]` and skipped — never silently dropped.
   - Draft it fully (decision-ready, per the intensity directive), outputs in
     normal repo locations.
3. Move completed lines to "Delivered", newest first:
   `- YYYY-MM-DD · item → path · needs Josh: approve/kill/redirect`.
4. Hand the Delivered list to the morning dispatch — it leads the optional
   lane line with paths (see commander-command-center-ops, CC-24 format).
5. Close with the goals-alignment check as usual; night-shift items count as
   drafts on the scoreboard, never as "shipped".

## Hard rule

The queue never justifies new infrastructure. If an item can't be done with
what exists, deliver instead a 5-line note: what exists that's closest, what's
missing, and the one question for Josh. That note is the draft.
