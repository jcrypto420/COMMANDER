---
name: commander-command-center-ops
description: "Operate Josh's COMMANDER command-center repo: money-loop execution, dashboard/reports, jobs/cartoon-lab/boring-report domains, safe autonomy, and GitHub-visible progress."
version: 1.1.0
author: Commander
license: private
metadata:
  hermes:
    tags: [commander, command-center, money-ops, github, model-routing, autonomy]
---

# Commander Command-Center Ops

Use this skill when working in Josh's `/home/josh/COMMANDER` repo or when the
user asks about Commander workflow, money-loop execution, reports, jobs,
Bad Boys cartoon lab, Boring Report, phone access, safe autonomy, or model
delegation.

## Operating posture

- Lead with execution, not theory. If Josh says "move forward" or redirects
  away from a side topic, stop the tangent and advance the highest-priority
  queued goal.
- If Josh calls out "bullshitSlop" or wants systems/loops polished, switch to
  Anti-Slop Systems Reset: pause shiny lanes, clean source-of-truth docs, make
  parked lanes explicit, keep one `doing` task, calm the loop before adding
  features.
- Keep GitHub visible: after meaningful repo updates, commit+push if already
  bounded-approved and verify the remote SHA; otherwise ask first.
- Use repo files as the source of truth and compact context cache — prefer
  updating durable docs over carrying a long chat. When a domain has its own
  authoritative doc (jobs, cartoon lab, Boring Report — see below), read and
  point at THAT file; do not re-explain its methodology inline here.
- Treat public/outbound actions as drafts until Josh approves: no posting,
  sending, spending, deploying, secrets, or financial/DeFi actions without
  explicit approval.

## Source-of-truth read order

1. `README.md` → `GOALS.md` → `NOW.md`
2. one relevant project file under `projects/`
3. `TASK_QUEUE.md`
4. relevant support docs (`SPRINT_69.md`, `MODEL_DELEGATION.md`, domain files below)

Do not load the whole repo unless the task genuinely requires it.

Before ANY repo task, sync first: if the tree is dirty, stash safely, then
`git pull --rebase`; only then diagnose missing files or make edits. A file
"missing" before a pull is not missing.

Before choosing the next task, read gate verdicts from
`dashboard/commander_inbox.jsonl` (`lane=gate-verdict`) — `COMMANDER_INBOX.md`
itself is capture-only and never executes actions.

## Money-loop workflow

1. Read focus from `NOW.md`, task status from `TASK_QUEUE.md`.
2. Pick one highest-leverage task advancing income, assets, leverage, or
   optionality.
3. Execute if safe; otherwise prepare a precise approval packet.
4. Save outputs to repo docs/project files; update `logs/daily_progress.md`
   and task statuses (append/patch, never replace history from a partial read).
5. Verify with `git status`, `git diff --stat`, `git diff --check`, and a
   basic secret scan on staged files (assignment/private-key patterns, not
   bare words, so "no secrets" text doesn't false-positive).
6. Ask before commit/push unless already explicitly approved.
7. **Run `commander-goals-alignment` at the end of the loop** — name the
   ladder item advanced or flag drift honestly. A metadata-only run (refreshed
   a queue row, restated a target, without producing a real artifact) is a
   FAILED run per the artifact rule in `COMMANDER_LOOP.md`, not progress.

## Reports & cadence

- Josh powers the Pi off nightly — nothing survives overnight in-session.
  Durable path: `hermes-gateway-commander.service` (linger=yes) + Hermes cron,
  workdir `/home/josh/COMMANDER`.
- Morning dispatch (`MORNING_REPORT.md`, CC-24 format): **exactly 5 lines** —
  Status, Shipped this week, CI-1 update, one optional lane update, ONE bolded
  Decision. Long detail goes in `logs/daily_progress.md`, never the brief.
  When `NIGHT_SHIFT.md` delivered drafts overnight/at boot, the optional lane
  line lists them with repo paths — Josh's 7am block judges them first.
- Weekly Money/Revenue Review: Mondays 8am, rewrites `WEEKLY_MONEY_REVIEW.md`,
  under ~80 lines, leads with the Shipped scoreboard, one money thesis, one
  primary next-7-days move, accountability call-outs (fake productivity,
  shiny-object chasing, overbuilding tech, avoiding marketing/sales).
- Default when Josh is quiet: keep reports flowing, don't guilt/escalate;
  after 3+ quiet days shorten to Baby Mode (one tiny task, one health/family
  anchor, urgent approvals only) — shortens the MESSAGE, never the work. On
  return: clean re-entry brief (what matters, what to ignore, today's move).
- Always show safety state (no posting/sending/spending/secrets) and GitHub
  visibility (committed+pushed vs local-only, with reason).

## Command Center Dashboard (Mission Control)

- Treat it as an execution cockpit, not an infra hobby project. Private/LAN
  first; no public ports without explicit approval.
- Live surfaces: `/` (lane cockpit), `/gate-deck` (tap-to-verdict cards →
  capture-only inbox API, `lane=gate-verdict` — never executes directly),
  `/docs` (Library — curated + self-organizing job packets), `/files/...`
  (whitelisted repo artifacts; blocks `.env`/secrets/credentials/`.git`/
  `node_modules`/traversal).
- `commander-mission-control.service` (user-level, LAN port 3011) runs
  `npm run dashboard:state` then `npm run start:lan`. Verify with
  `npm run build` + a local HTTP check before any restart; ask before
  restarting the live service.
- Lane cards parse `## Status` blocks from `projects/*.md`. Gate Deck verdicts
  use ship/kill/(role-specific) vocabulary and stay capture-only — Hermes
  reads and acts on verdicts next loop, buttons never execute directly.
- Do not `npm audit fix --force` on breaking advisories — report and keep the
  verified build.

## GitHub / repo hygiene

- Top-level files: stable source-of-truth docs, current reports, key plans
  only. `projects/` for durable briefs/packets. `logs/daily_progress.md` is
  the timeline — don't create a new progress doc per action.
- `TASK_QUEUE.md` stays active/backlog only; completed rows move to
  `TASK_ARCHIVE.md`. Maintain the one-`doing` invariant; parked lanes are
  explicit `blocked` rows with reopen conditions.
- If rebase is blocked by generated untracked files (`dashboard/state.json`,
  `.next/`), move the disposable files aside, finish the rebase, restore only
  what's needed, verify with `git status`/`git diff --check`/a build.
- On any repo-lifecycle change (an application applied, a gate verdicted, a
  task done), update EVERY table that references it in the same commit — a
  stale row in one table while another says "done" causes duplicate work
  (see: the 2026-07-06 Coinbase tracker-desync incident).

## Domain playbooks (read the live doc, don't duplicate it here)

- **Jobs/career:** `jobs/TRACKER.md` (single source of truth — check FIRST,
  every time, before any job work) and `jobs/SEARCH_PLAYBOOK.md` (discovery,
  scoring, tailoring method). Applications live in
  `jobs/packets/active/<company-role>/`, archive to `jobs/packets/archive/`
  same-commit as the tracker update on applied/killed. Never submit, send
  outreach, or create accounts without explicit Josh approval.
- **Bad Boys cartoon lab:** `projects/badboys-cartoon-lab.md` is the full
  constitution (face law, monoline purity, deadpan-over-corny, edge law) and
  7-stage pipeline. Run `commander-critic-passes` before banking any premise
  or script for Josh's Gate 1. Do not invent new creative rules here — that
  file is authoritative.
- **The Boring Report:** `projects/boring-report-prd.md` (methodology, QA,
  milestones) + `products/boring-report/CORRECTIONS.md` (flawless-streak
  ledger). `verify.py` must pass before any issue reaches Josh's Gate Deck.
  Numbers with no source snapshot are a P0 bug, not a rounding choice.
- **Model delegation:** per `MODEL_DELEGATION.md` — cheap/default models for
  daily execution, premium only for genuinely hard review/blockers. MoA
  (`hermes moa list`) runs a free `gpt-5.4-mini` self-consistency ensemble for
  critic passes — never switch it to a paid preset without Josh's approval.

## Phone / Telegram

- Telegram (Commander profile) is locked to Josh: `TELEGRAM_ALLOWED_USERS`,
  `TELEGRAM_HOME_CHANNEL` set to his chat.id, `GATEWAY_ALLOW_ALL_USERS=false`,
  `TELEGRAM_ALLOW_ALL_USERS=false`, profile `.env` mode `600`. Never rely on
  temporary all-users access after setup.
- Never put bot tokens in GitHub, repo files, or chat — redact if one appears.
- Hermes blocks self-restart of the gateway from inside a gateway session —
  report the exact outside-shell restart command instead of trying to route
  around it.
- Use `/home/josh/.local/bin/hermes --profile commander ...` explicitly;
  omitting `--profile commander` can configure the default profile instead
  and spawn a second gateway service receiving Josh's messages.
- If "No LLM provider configured" appears, don't assume the model is broken —
  test CLI chat for the profile first, then check for a duplicate gateway
  service. If Codex OAuth specifically fails, the fix is usually
  `hermes -p commander auth` re-login (~2 min, Josh-only OAuth) — this has
  happened after both a session crash and a ChatGPT subscription cancel/renew.

## Pitfalls

- Don't keep researching an interesting tool after Josh says stop — switch
  back to the goal immediately.
- Don't turn model-routing discussion into a long premium session.
- Don't assume GitHub web uploads are invisible locally — `git pull --ff-only`
  and verify assets arrived.
- Don't treat uploaded assets as automatically public-safe — inventory and
  ask usage-rights questions first.
- Don't duplicate a rule that already lives in a domain's authoritative file
  (jobs/TRACKER.md, cartoon-lab.md, the PRD) — point at it instead. This
  skill degraded once already from exactly this pattern (2026-07-06 cleanup:
  381 lines → this version, after "Operating posture" alone had drifted to
  three duplicate empty headers).
