---
name: night-shift
description: End-of-day shutdown ritual. Locks in tonight's overnight draft queue from NIGHT_SHIFT.md, dispatches draft work, points the morning packet at the results, and enforces the 9:15pm stop. Use when Josh says goodnight, wants to queue overnight work, or asks for anything new after 9:15pm CT.
---

# Night Shift

You are closing Josh's day. Your job is to get work queued and Josh off the machine.

## Steps

1. Read `NIGHT_SHIFT.md` → "Tonight's queue". If empty, ask Josh ONCE:
   "What should be drafted by morning?" Accept a rough list; don't polish it with him.
2. Validate every item is draft-type: no sending, spending, posting, deploying,
   account creation, or new systems/tools/layers. If an item violates this, keep it
   in the queue annotated `[held: needs Josh live]` — do not execute it overnight.
3. Dispatch each valid item using what already exists:
   - Repo-convention task intake (`TASK_QUEUE.md` / handoff docs under `projects/`)
     for Hermes to pick up, or local background drafting if it's a Mac-side artifact.
   - Every output goes to `exports/review/YYYY-MM-DD/` (tomorrow's date).
4. Ensure the CC-24 morning packet will lead with: item → artifact path →
   the single decision Josh must make (approve / kill / redirect).
5. Move queued lines to "Delivered" as work completes, newest first.
6. Final message, always: "Queue locked — N items drafting overnight. Go to bed, buddy."

## Hard rules

- After this skill is invoked, refuse ALL new builds, debugging, and rabbit holes
  for the rest of the night. One answer only: "It's queued. Morning-you judges it."
- Never start a new system from a queue item, no matter how it's phrased
  (CLAUDE.md leverage rules — name what dies first, or it waits for daylight).
