# TASK_QUEUE.md

Active task board only. Completed history lives in `TASK_ARCHIVE.md` and narrative progress lives in `logs/daily_progress.md`.

Status: `todo` / `doing` / `blocked` / `done`.
Approval = does this need Josh's OK before acting? (see `SECURITY.md`).

Operating rule: exactly one `doing` DECISION lane for Josh; Hermes may advance up to 3 draft-only lanes per day (see `COMMANDER_LOOP.md` intensity rules). Parked lanes are `blocked` with a clear reopen condition, not half-active.

| ID | Project | Pri | Task | Status | Next action | Approval |
|----|---------|-----|------|--------|-------------|----------|
| CI-1 | Career/Income | 1 | Daily job/application process | doing | draft-ahead FULL packets for slate roles 1–2 (Chainlink Data Risk Ops, Coinbase Billing Ops) before Josh picks; refresh slate each weekday; tracker row per role; no submissions/messages without approval | **yes** to send |
| CC-18 | Command Center | 1 | Loop sync protocol fix | todo | every loop starts commit-or-stash + `git pull --rebase`, ends with commit+push (deploy key); clear the current dirty tree first | no |
| CC-20 | Command Center | 1 | Apply intensity rules to live SOUL.md on Pi | todo | copy updated `configs/commander_soul_template.md` sections into `~/.hermes/profiles/commander/SOUL.md` (Josh directed the go-harder posture 2026-07-02) | **yes** |
| CC-19 | Command Center | 1 | Midday + evening draft-only cron loops | todo | add 2 cron jobs (cheap model, restricted toolsets, draft-only); morning loop stays the only report Josh must read | **yes** |
| CC-21 | Command Center | 2 | Hermes self-audit: skills + cron vs intensity rules | todo | list live skills/cron on the Pi, prune stale ones, confirm each job is cheap-model + restricted + draft-only; log result | no |
| CC-22 | Command Center | 2 | Mission Control per-lane status cards | todo | extend `build_dashboard_state.py` to parse `## Status` blocks from `projects/*.md` into `state.json`; render one card per lane; build+verify locally | yes to deploy/restart |
| CC-23 | Command Center | 2 | Hermes browser chat (Open WebUI / API server) | todo | verify against live Hermes docs, then enable API server + web UI on the Pi, LAN-only, no public ports; pairs with CC-10 Tailscale for remote | **yes** |
| CC-10 | Command Center | 2 | Private phone access (Tailscale-first) | todo | try Tailscale SSH / dashboard before any chat platform | **yes** |
| CC-13 | Command Center | 2 | Test model-specific worker pattern | todo | run one cheap read-only worker and log result | no |
| WO-1 | Weather Oracle | 4 | Revenue-option scan before build | todo | identify profitable/grant/leverage angles; good silent-running draft lane | no |
| BB-17 | Bad Boys/Joycat | 3 | Week 1 manual posting packet | blocked | reopen only when Josh says "reopen Bad Boys" | yes |
| BB-23 | Bad Boys/Joycat | 3 | TikTok account creation runbook | blocked | Josh must perform credentials/verification/2FA; Pi browser unavailable | **yes** |
| BB-24 | Bad Boys/Joycat | 3 | Refocus on real assets | blocked | reopen with BB-17 | yes |
| MA-1 | Market Activity | 3 | Personal/open-source market activity tracker | blocked | reopen after CI-1 loop is running smoothly for a week | no |

## Parking lot rules

- Do not add a new active row unless it has a concrete next action.
- If an idea is interesting but not today's lane, capture it in the relevant project doc or `logs/daily_progress.md`, not as `doing`.
- When a task finishes, move it to `TASK_ARCHIVE.md` during the next hygiene pass.
- Silent running (Josh away): work the draft-only `todo` rows top-down; batch all approval asks into the next morning report.
