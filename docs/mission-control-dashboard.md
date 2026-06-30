# Commander Mission Control Dashboard

Private Next.js dashboard for Josh's daily tasks, revenue sprint, Commander reports, Hermes status, and Sovereignty Stack read-only context.

## What it shows now

- Today's money move from `MORNING_REPORT.md` / dashboard state
- Daily task queue and approval-gated next steps
- Weekly Money / Revenue Review and Morning Brief excerpts
- Hermes / Telegram / cron status from the state generator
- Sovereignty Stack service inventory and Docker container count
- Safe interaction guidance for Telegram and future approval-gated actions

## Safety model

- Local/private first.
- Dev server binds to `127.0.0.1` by default.
- No public ports.
- No secrets displayed.
- No posting, sending, spending, trading, account creation, or service changes from dashboard buttons.
- Future action buttons should create approval packets first.

## Commands

From `/home/josh/COMMANDER`:

```bash
npm run dashboard:state
npm run dev
npm run build
```

Default local dev URL:

```text
http://127.0.0.1:3010
```

Easiest HP-laptop-on-home-WiFi access:

```bash
npm run dashboard:state
npm run dev:lan
```

Then open:

```text
http://192.168.1.189:3011
```

Note: port `3010` is already used by Josh's existing Sovereignty Stack dashboard/login service. Mission Control should use port `3011` unless that changes.

## Current verification

- `npm run dashboard:state` writes `dashboard/state.json` successfully.
- `npm run build` completes successfully with Next.js 16.2.9.
- `commander-mission-control.service` is enabled and running as a user service.
- `curl http://127.0.0.1:3011/` returned rendered Next.js HTML during service test.

Service details: `docs/mission-control-service.md`

## Known issue

`npm audit --omit=dev` currently reports 2 moderate PostCSS advisories via Next's dependency tree even on Next.js 16.2.9. `npm audit fix --force` suggests a breaking downgrade path and was intentionally not run.
