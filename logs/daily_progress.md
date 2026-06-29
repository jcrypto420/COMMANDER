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

- Returned focus to BB-2 after pausing MoA research. Drafted
  `projects/badboys-brand-onepager.md` and `projects/badboys-content-hooks.md`
  as no-posting/no-spend launch materials for Josh approval.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Pulled Josh-added Bad Boys assets from GitHub: 27 files under
  `assets/badboys/`, including logos/art variants, an 85-page PDF brand guide,
  and a strategist ZIP package. Updated `assets/badboys/inventory.md`.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Added Josh's long-term goal/principle to `GOALS.md`, `INTAKE.md`, and
  `NOW.md`: learning and consistent daily quality-of-life improvement for both
  Josh and Commander/system; consistent, intentional improvement = enjoyment of
  life.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex session.

- Drafted `projects/badboys-approval-packet.md` to package the first public-test
  review into one concise approval-ready artifact, while leaving Telegram setup
  for later.
- Inspected the Bad Boys strategist package / brand guide, confirmed the OG face
  logo is the source of truth, and created `projects/badboys-brand-consistency.md`
  as the next draft step.
- Drafted `projects/badboys-social-calendar-week1.md` from the brand standard,
  focusing week one on manifesto, identity, Joycat crossover, product seed, and
  world-building signal tests.
- Built `projects/badboys-ops-plan.md` to cover content creation, post
  scheduling, long-term planning, and account-creation prep as a reusable
  operating system.
- Drafted `projects/badboys-tiktok-30-day-rollout.md` with week-by-week themes
  for identity, mascot, product seed, and world-building signal tests.
- Added `projects/badboys-tiktok-week2-4-prompt-pack.md` and
  `projects/badboys-tiktok-asset-prompt-manifest.md` to cover the remaining
  assets and map each filename to its prompt source.
- Created seven zero-cost local SVG draft assets under
  `assets/badboys/tiktok/week1/` for the first TikTok content week.
- Created the remaining 23 local SVG draft assets under
  `assets/badboys/tiktok/month1/`, completing the full 30-day internal draft
  asset set.
- Added `projects/badboys-tiktok-month1-asset-generation-order.md` to track the
  full draft asset set and the remaining PNG export/tooling gate.
- Added `projects/badboys-tiktok-month1-posting-queue.md` pairing all 30 draft
  assets with captions, CTAs, and approval-gated statuses.
- Installed local no-sudo PNG export tooling with `@resvg/resvg-js`, added
  `scripts/export_badboys_svgs_to_png.js`, exported all 30 assets to
  `assets/badboys/tiktok/png/`, and verified they are 1080x1920 PNGs.
- Visual spot-check caught footer/CTA/image-reference issues in the first export;
  rebuilt canonical SVG sources under `assets/badboys/tiktok/svg/`, embedded the
  face mark, removed stale footer copy, re-exported all PNGs, and re-verified
  30 valid 1080x1920 outputs.
- Added `projects/badboys-tiktok-week1-manual-posting-packet.md` and
  `projects/badboys-tiktok-png-export-toolchain.md`.
- Added `projects/badboys-tiktok-account-readiness.md` and
  `projects/badboys-tiktok-week1-asset-generation-order.md` so account setup and
  Week 1 production are explicit while remaining approval-gated.
- Revised TikTok account docs after Josh rejected the first handle set, removed
  “Moggers mog” from the bio direction, and locked `bebad4good` as the preferred
  TikTok handle.
- Updated `TASK_QUEUE.md` and `NOW.md` to move active work into Week 1 asset
  review/export and account readiness.
- Estimated spend: $0.00 incremental API spend; used existing ChatGPT/Codex
  session.

- Committed and pushed the TikTok launch kit to GitHub at commit `0347aa2` on
  `feat/command-center-scaffolding`, after verifying 30 valid 1080x1920 PNGs and
  keeping Telegram token helper code untracked.
- Reviewed Week 1 TikTok creative quality and created
  `projects/badboys-tiktok-week1-creative-review.md`: Days 1/2/4/7 are postable
  candidates; Days 3/5/6 should be improved before public posting if possible.
- Updated Week 1 asset/checklist docs to reflect that PNGs now exist and the
  remaining gate is creative refinement + Josh approval, not raw export.

- Built the Week 1 v1 hardmode SVG asset pack under
  `assets/badboys/tiktok/week1-v1-hardmode/`, replacing placeholder-heavy
  Joycat/product/lore cards with stronger visual signal tests.
- Added `projects/badboys-tiktok-harder-launch-push.md` to define the harder
  launch stance while keeping all posting/account/spend actions approval-gated.

- Josh rejected the v1 TikTok hooks as too corny and approved going harder.
  Created the Week 1 v2 less-corny SVG pack under
  `assets/badboys/tiktok/week1-v2-lesscorny/` with colder hooks and simpler
  signal asks.
- Completed more Bad Boys revenue tasks: drafted `projects/badboys-product-backlog-v0.md`,
  `projects/badboys-signal-dashboard.md`, `projects/badboys-first-sticker-pack-brief.md`,
  and `projects/badboys-tiktok-week1-v2-manual-posting-packet.md`.
- Created first product-shaped source assets under `assets/badboys/sticker-pack-v0/`:
  six sticker/PFP SVGs plus a preview sheet, all internal and approval-gated.

- Josh said v2 still felt corny and approved going even harder plus TikTok account prep.
  Studied public mogging/TikTok/meme-brand context and created
  `projects/badboys-mogging-marketing-research.md` plus
  `projects/badboys-mogging-tactics-playbook.md`.
- Created Week 1 v3 Artifact Lab under `assets/badboys/tiktok/week1-v3-artifact-lab/`:
  seven no-hook, artifact-first SVG posts using BAD SAMPLE / FIELD TEST / KEEP-KILL formats.
- Added `projects/badboys-tiktok-week1-v3-artifact-lab-packet.md` and
  `projects/badboys-tiktok-account-creation-runbook.md`. Account creation remains
  blocked on Josh-controlled credentials/verification/2FA and lack of interactive browser on the Pi.

- Josh called the generated TikTok plans/assets wank. Refocused the sprint on real Josh-provided Bad Boys assets instead of generated launch cards.
- Created `assets/badboys/account-ready-real-assets-v0/` with copied real asset candidates and review gallery.
- Created `projects/badboys-refocus-stop-the-wank.md`: new recommendation is avatar from `INSIDEFACE NOBG.png`, first post candidate from `BBTHUNDER_UP_-removebg-preview.png`, minimal copy only.
