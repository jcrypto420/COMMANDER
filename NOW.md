# NOW.md

**Active focus:** Command Center reliability + 69-day revenue sprint discovery.
Commander is live on the Pi and should turn Josh's intake into safe,
low-cost execution.

**Status:** Hermes v0.17.0 installed on `commandcenter`; `commander` profile
created; provider = OpenAI Codex via ChatGPT OAuth (no per-token cost);
default model `gpt-5.4-mini`, premium `gpt-5.5`; first safe read-only task
passed.

## Next 3 tasks

1. Tomorrow hard start: review `projects/tomorrow-hard-start-2026-06-29.md`,
   then inspect only the two real Bad Boys assets in
   `assets/badboys/account-ready-real-assets-v0/review-gallery.html`.
2. If Josh approves the real-asset setup, Josh creates TikTok `bebad4good` from
   phone/laptop; credentials, age-gate, verification, password, recovery, and
   2FA stay Josh-controlled.
3. Next dashboard step: easiest access is LAN on port 3011 (`npm run dev:lan`, then open `http://192.168.1.189:3011`). Permanent user service still requires approval.

_Done: Telegram phone approval channel is live and locked to Josh's Telegram ID; daily money loop and Weekly Money / Revenue Review now deliver to Telegram._
_Done: `weekly-money-review` cron is live Mondays at 8am and first run created `WEEKLY_MONEY_REVIEW.md`._
_Done: Mission Control Dashboard v0 is now a Next.js app with read-only `dashboard/state.json`, Commander reports, task queue, Hermes/cron status, and Sovereignty Stack panels. `npm run build` passed; no service install or public exposure._

_Done: OpenRouter fallback wired (CC-7) — Codex → gemini-2.5-flash → llama-8b._
_Done: daily loop autonomous at 7am (CC-8/9); auto-commits its draft to GitHub
(`logs/daily_progress.md`) via a repo-scoped deploy key — readable from any
device, no notifications/exposure. View on GitHub or `commander chat` on phone._
_Done: onboarding interview saved to `INTAKE.md`; approved follow-up doc edits
are being applied._
_Done: REV-1 selected Bad Boys / Joycat / Mog as the primary 69-day sprint;
see `SPRINT_69.md`. Phone/autonomy plan drafted in `PHONE_AUTONOMY.md`._
_Done: model delegation plan drafted in `MODEL_DELEGATION.md` to prevent premium
usage blockages._
_Done: Bad Boys / Joycat / Mog approval packet drafted for later review without
requiring Telegram._

## Current blockers

- Optional: Nous Portal (`hermes login`) for bundled web/browser
  tools; add when needed.
- Spending/sending actions still require Josh's approval (see `SECURITY.md`).
- Josh's availability may be sporadic around the birth of his son; prefer
  asynchronous systems, queues, drafts, and approval checkpoints.

## Standing long-term principle

- Learning and daily quality-of-life improvement matter alongside money goals:
  consistent, intentional improvement = enjoyment of life.

_Update this file at the start and end of each working session._
