# NOW.md

**Active focus:** `CI-1 Daily job/application process` — the career/income lane
is the primary revenue-defense sprint lane. The Anti-Slop Systems Reset (OPS-1)
is complete and archived; its output is `COMMANDER_LOOP.md` + a clean queue.

**Status:** Hermes v0.17.0 on `commandcenter`, `commander` profile, provider =
OpenAI Codex via ChatGPT OAuth (default `gpt-5.4-mini`, premium `gpt-5.5`).
Claude Code node linked from Josh's Mac (clone at `~/COMMANDER`). Intensity
rules v2 adopted 2026-07-02 (see `COMMANDER_LOOP.md`) — Josh's directive:
clean the system up and go harder. Draft-ahead, never idle on "waiting."

## Next 3 tasks

1. `CI-1` (doing): draft-ahead full application packets for the top 2 roles on
   `projects/job-slate-2026-07-02.md` (Chainlink Data Risk Ops + Coinbase
   Billing Ops) BEFORE Josh picks — his yes should be send-ready. Refresh the
   slate each weekday.
2. `CC-18`: fix the loop sync protocol — the 2026-07-02 loop skipped `git pull`
   because of local uncommitted changes on the Pi. Every loop now starts with
   commit-or-stash + `git pull --rebase` (see `COMMANDER_LOOP.md` intensity
   rules).
3. `CC-19` (needs Josh approval): add midday + evening draft-only cron loops so
   the Pi works more than one cycle per day. Cheap model, restricted toolsets,
   same safety gates.

## Current blockers

- Pi working tree is dirty (`NOW.md`, `TASK_QUEUE.md`, untracked `exports/`) —
  resolve via CC-18 on the next loop, then pull this update.
- Spending/sending actions still require Josh's approval (see `SECURITY.md`).
- Josh's availability is sporadic around the birth of his son. Silence means
  MORE queued drafts batched for re-entry review — never idling.

## System freeze (2026-07-03, Josh)

The build phase is OVER. CC-19/20/22/23 are the last construction items.
After they land: no new root docs, no new rules, no new tools, no new
process until something SHIPS externally (application submitted, post
published, email sent). The scoreboard metric is **things that leave the
building per week** — drafts, docs, and commits don't count. The weekly
money review leads with the Shipped count. If meta-work beats real-work
two weeks running, the system is failing and Commander must say so.

**This week's definition of success: one job application actually submitted.**

## Standing long-term principle

- Learning and daily quality-of-life improvement matter alongside money goals:
  consistent, intentional improvement = enjoyment of life.

_Update this file at the start and end of each working session._
