# NOW.md

**Active focus:** Command Center reliability + CC-24 morning packet repair / CI-1 Coinbase Institutional packet / revenue backstop after overnight rebase; CC-24 exact-shape check passed again this morning.
Commander is live on the Pi and should turn Josh's intake into safe,
low-cost execution.

**Status:** Hermes v0.17.0 installed on `commandcenter`; `commander` profile
created; provider = OpenAI Codex via ChatGPT OAuth (no per-token cost);
default model `gpt-5.4-mini`, premium `gpt-5.5`; first safe read-only task
passed. CC-24 morning packet drift was repaired and the exact 5-line draft shape now passes again.

## Next 3 tasks

1. Review `jobs/packets/active/coinbase-institutional-business-ops/packet.md`, then if Josh approves, prepare the application path or collect tweak notes.
2. Keep Bad Boys real-asset review and the BB-24 sticker-sheet packet as the fallback lane; no posting, account creation, sending, or spending without Josh.
3. Keep the morning dispatch at 5 lines and update logs before commit/push.

## Current blockers

- Spending/sending actions require Josh's approval (see `SECURITY.md`).
- Josh's availability is sporadic around the birth of his son. Silence means
  MORE queued drafts batched for re-entry review — never idling.

## System freeze (2026-07-03, Josh — restored after rebase collision)

The build phase is OVER. CC-19/20/22/23 are the last construction items.
After they land: no new root docs, no new rules, no new tools, no new
process until something SHIPS externally (application submitted, post
published, email sent). The scoreboard metric is **things that leave the
building per week** — drafts, docs, and commits don't count. The weekly
money review leads with the Shipped count. If meta-work beats real-work
two weeks running, the system is failing and Commander must say so.

**This week's definition of success: one submitted application — SMASHED: 5.**

## Standing long-term principle

- Learning and daily quality-of-life improvement matter alongside money goals:
  consistent, intentional improvement = enjoyment of life.

_Update this file at the start and end of each working session. On merge/rebase
conflict, the REMOTE (origin) version of NOW.md wins — restore local edits on
top of it, never flatten it._
