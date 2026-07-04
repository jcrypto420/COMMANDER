# Project: Commander Dashboard / Command Center UI v0

## Status — 2026-07-03

- Current focus: CC-22 draft is now built locally — lane cards parsed from `projects/*.md`, Gate Deck verdict flow wired to the inbox API, and install icons added.
- Next action: keep the draft local until Josh approves a live service restart; then verify the deployed Mission Control refreshes cleanly.
- Safety: local docs only; no posting, sending, spending, or secrets.

## Why this matters

Josh now has the core operator loop working: Commander on the Pi, Telegram access, morning cron, GitHub-visible repo state, and an older Sovereignty Stack already on the same machine.

The next leverage move is a private, visually excellent command center that makes the system easy to run at a glance instead of digging through PuTTY, GitHub files, scattered dashboards, and Telegram threads.

## Recommendation

Build a **private local/Tailscale web dashboard** first, not a public app.

Start as a static + file-backed dashboard inside `COMMANDER`, then progressively connect live read-only data from Hermes, repo docs, cron, git, and selected Sovereignty Stack services.

Design target: Linear precision + VoltAgent cockpit energy.

## What it should show first

### 1. North-star money panel

- 69-day sprint status
- current highest-leverage money move
- current blocker
- next copy/paste approval phrase
- passive-income target progress

### 2. Morning brief / decision queue

- latest `MORNING_REPORT.md`
- approval requests
- decisions waiting on Josh
- “if you do nothing” action

### 3. Task board

- parsed `TASK_QUEUE.md`
- grouped by priority/project/status
- one active `doing` task highlighted
- approval-gated tasks clearly marked

### 4. Hermes status

- gateway online/offline
- Telegram connected
- active cron jobs
- last daily loop run
- current provider/model
- model fallback health

### 5. Subagent / worker monitor

- active delegated tasks
- background processes
- future Hermes Kanban tasks
- stuck/blocked worker warnings

### 6. Sovereignty Stack panel

Read-only integration first:

- CasaOS / Docker service links
- Grafana / ticker / Immich / Uptime Kuma links
- local IP + Tailscale IP
- crypto ticker service status if running
- storage/backup warnings

### 7. Learning / QOL loop

- daily learning note
- one concept to learn
- one family/QOL improvement
- one system improvement

## Data sources v0

Keep it dumb and reliable first:

| Panel | Source |
|---|---|
| Morning brief | `MORNING_REPORT.md` |
| Goals | `GOALS.md` |
| Now | `NOW.md` |
| Tasks | `TASK_QUEUE.md` |
| Daily progress | `logs/daily_progress.md` |
| Hermes cron | `hermes cron list` / cronjob state |
| Gateway | `hermes --profile commander status --all` |
| Sovereignty stack | `/home/josh/sovereignty_stack/STACK_OVERVIEW.md` + service health checks |

## Build stages

### Stage 0 — static visual prototype

Create a beautiful local HTML mockup with realistic data copied from current repo state.

No server. No secrets. No service changes.

Output:

- `prototypes/command-center-dashboard-v0.html`

### Stage 1 — local read-only generator

A script reads repo files and writes `dashboard/state.json`.

Output:

- `scripts/build_dashboard_state.py`
- `dashboard/state.json`
- static HTML reads JSON locally or via a tiny local server

### Stage 2 — private dashboard service

Run a local-only service bound to `127.0.0.1` or Tailscale-only/LAN-only after approval.

Candidate stack:

- Python FastAPI for API/read-only status
- static HTML/CSS/JS frontend
- no database at first
- no public ports

### Stage 3 — action layer with approvals

Buttons do not directly do risky things. They generate approval packets or send Telegram commands.

Examples:

- “Run morning loop now” → safe cron run
- “Verify gateway” → read-only status command
- “Prepare Bad Boys account packet” → doc draft only
- “Approve push” → explicit approval phrase still required

### Stage 4 — integrate jdoink / Sovereignty Stack repo

Read-only first.

Required approach:

1. Josh grants access safely through GitHub account/SSH/token setup without pasting secrets into chat.
2. Clone or add remote read-only if possible.
3. Inventory current repo state.
4. Do not merge repos immediately.
5. Create an integration map: what lives in `COMMANDER`, what lives in `sovereignty_stack`, and what gets surfaced in the dashboard.

## Security rules

- Private-first: LAN/Tailscale only.
- No public port exposure without explicit approval.
- No secrets in repo/dashboard output.
- No raw `.env`, tokens, wallet data, private keys, SSH keys, or passwords shown.
- Service actions stay read-only until an approval workflow is built.
- GitHub push still requires approval unless inside an already-approved bounded rule.

## UX principles

- Beautiful but practical: cockpit, not toy.
- One screen should answer: “What matters today?”
- Dense, but calm.
- Use color for state, not decoration.
- Money/action panels first; infrastructure panels second.
- Mobile/Telegram remains the quick-command surface; dashboard is the command room.

## First concrete deliverable

Build `prototypes/command-center-dashboard-v0.html` as a static visual mockup.

It should include:

- top status bar
- money move card
- morning brief card
- task board preview
- Hermes/Telegram/cron health strip
- Sovereignty Stack integration panel
- subagent monitor placeholder
- approval queue

No installs. No server. No secrets. No deployment.

## CC-24 draft target

Tomorrow's morning brief should compress into one scan-friendly packet:

1. Title line.
2. One money-move sentence.
3. One done-while-away sentence.
4. One review line with `Open:` and `Decide:`.
5. One status/next-action line with the decision in bold.
