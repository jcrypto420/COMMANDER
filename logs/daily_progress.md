# Daily Progress

One short entry per working day. What advanced + estimated spend.

## 2026-06-27

- Created `command-center` repo scaffolding (truth files, project files, configs,
  scripts, logs). Opened PR #1.
- Verified Hermes install commands against live docs.
- Installed Hermes v0.17.0 on the Pi (`commandcenter`, aarch64/Debian 12) over SSH.
- Created `commander` profile; seeded SOUL.md; set cheap default model.
- Connected provider: OpenAI Codex via ChatGPT OAuth (device-code) — no per-token
  cost. Default `gpt-5.4-mini`, premium `gpt-5.5`.
- First safe read-only task passed (Commander summarized its own repo).
- Estimated spend: $0.00 (Codex rides ChatGPT plan; no API tokens billed).
- Next: add OpenRouter as cheap fallback tier; build daily make-money loop.

## 2026-06-28

- Chosen task: CC-8 — Daily make-money loop as cron (draft-only), since it unlocks the highest-leverage daily income workflow with no sending or spend.
- Next action:
  - Review `MONEY_OPS.md` and identify the single safest draft-only cron step.
  - Draft the cron command and guardrails so it only reads state, writes logs, and never sends anything.
  - Verify the task fits the current `commander` defaults and approval rules.
- Cost/automation idea: keep the loop read-only and reuse one cheap local/default model for summaries; only escalate if a check fails.

- Chosen task: IN-1 — First lead list + 1 outreach draft, because it is the highest-leverage safe income step and stays draft-only.
- Next action:
  - Define one narrow target profile for the best-paying lead.
  - Collect 5–10 candidate leads from existing notes or public sources.
  - Draft one tailored outreach message plus one follow-up variant.
  - Save the lead list and drafts for review; do not send anything.
- Cost/automation idea: standardize a reusable outreach template so future drafts can be auto-filled from the lead list.

- Completed onboarding interview and saved strategic intake to `INTAKE.md`.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Applied Josh-approved intake follow-up edits to GOALS/NOW/TASK_QUEUE and
  project files, aligning the repo around the 69-day $6.9K sprint and the
  Bad Boys/Joycat/Mog high-upside revenue lane.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Ran REV-1: selected Bad Boys / Joycat / Mog as the primary 69-day revenue
  sprint, with career / crypto research leverage as the safety backstop.
- Drafted `SPRINT_69.md` and `PHONE_AUTONOMY.md` to make the workflow easier
  from Josh's phone while keeping spending, sending, posting, secrets, service
  changes, and financial actions approval-gated.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Started BB-1/BB-2/CC-10 execution: created Bad Boys asset intake files,
  drafted `projects/badboys-launch-loop.md`, and documented Telegram setup in
  `TELEGRAM_SETUP.md`.
- Telegram setup is blocked on Josh creating/providing a BotFather token through
  a safe local secret-entry path; no token should be committed.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Saved public Joycat / Mog / Mogcoin research to
  `projects/badboys-joycat-research.md` and folded key brand guardrails into
  `projects/badboys-launch-loop.md`.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Drafted `MODEL_DELEGATION.md` and updated model/cost docs so daily execution
  runs on cheaper models, GPT-5.5 is reserved for review/escalation, and
  subagents use narrow toolsets with compact summaries.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Created `logs/model_usage.csv` header so future model/provider/cost usage can
  be tracked in the repo.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Expanded `MODEL_DELEGATION.md` into a project-lead protocol: Commander should
  proactively route tasks, delegate narrow subtasks, integrate results, run
  review/safety passes, and escalate to GPT-5.5 only when justified.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.
