# TASK_QUEUE.md

Active task board only. Completed history lives in `TASK_ARCHIVE.md` and narrative progress lives in `logs/daily_progress.md`.

Status: `todo` / `doing` / `blocked` / `done`.
Approval = does this need Josh's OK before acting? (see `SECURITY.md`).

Operating rule: exactly one `doing` DECISION lane for Josh; Hermes may advance up to 3 draft-only lanes per day (see `COMMANDER_LOOP.md` intensity rules). Parked lanes are `blocked` with a clear reopen condition, not half-active.

Josh's calibration (2026-07-02 interview): job lane = primary decision lane; Bad Boys + Primoscapes + DeFi product ideation = the push lanes; same-day 60-second verdicts in the 8–9am window; reports must shrink (CC-24).

| ID | Project | Pri | Task | Status | Next action | Approval |
|----|---------|-----|------|--------|-------------|----------|
| CI-1 | Career/Income | 1 | Daily job/application process | doing | draft-ahead FULL packets for slate roles 1–2 (Chainlink Data Risk Ops, Coinbase Billing Ops); refresh slate each weekday; Josh gives same-day verdicts | **yes** to send |
| CC-24 | Command Center | 1 | 5-line daily dispatch | todo | format folded into the recreated 07:30 morning loop prompt; verify tomorrow's dispatch actually arrives as 5 lines + ONE bolded decision, then archive | verify only |
| BB-24 | Bad Boys/Joycat | 1 | Refocus on real assets — **REOPENED by Josh 2026-07-02** | todo | refresh the real-asset plan; pick the first sellable artifact (sticker-pack v0 leading candidate) and its storefront path; draft-only | no |
| BB-17 | Bad Boys/Joycat | 2 | Week 1 posting packet | todo | rebuild packet around real assets + bone-circle avatar so it is post-ready the day Josh creates the account | yes to post |
| BB-23 | Bad Boys/Joycat | 2 | TikTok account creation | todo | JOSH action (~30 min): create account per runbook; credentials/2FA stay Josh-only | **yes** |
| PS-1 | Primoscapes | 2 | Fall Native Prairie prep | todo | facts confirmed (OKC metro, 1–2 solo installs/wk): define ONE tiny fall offer sized to that; draft one-pager + OKC lead list; no outreach without approval | yes to send |
| DF-1 | DeFi/Chainlink | 2 | DeFi product ideation memo | todo | 10 product concepts from Josh's real edge (oracle risk, RWA/tokenization, stablecoin risk, market infra); rank by build-cost vs revenue path; concepts only — no financial actions, no custody, no trades | no |
| CC-19 | Command Center | 1 | Midday + evening cron loops | todo | jobs live; morning loop recreated 07:30 pinned (drift-guard fix). Verify 1pm/6pm commits land 2026-07-03, then archive | verify only |
| CC-18 | Command Center | 1 | Loop sync protocol | todo | embedded in cron prompts step 0/8; verify no skipped pull on 2026-07-03, then archive | no |
| CC-21 | Command Center | 2 | Hermes self-audit | todo | skills/cron audit + FIX: `model_usage.csv` still empty on 07-03 (resume per-call logging) + remove vestigial `model.base_url` line + COMPLIANCE: cron conflict-resolution must prefer REMOTE for state docs (NOW.md was flattened 07-03 morning) | no |
| CC-22 | Command Center | 2 | Mission Control per-lane status cards | todo | parse `## Status` blocks from `projects/*.md` into `state.json`; render one card per lane | yes to deploy |
| CC-23 | Command Center | 2 | Hermes browser chat | todo | phase 1 DONE 2026-07-02 (loopback :3012 + SSH tunnel, commander profile). Phase 2: password_hash + LAN bind + user systemd service (show unit file first) | **yes** |
| CC-10 | Command Center | 2 | Private phone access (Tailscale-first) | todo | try Tailscale SSH / dashboard before any chat platform | **yes** |
| CC-13 | Command Center | 3 | Test model-specific worker pattern | todo | run one cheap read-only worker and log result | no |
| WO-1 | Weather Oracle | 4 | Revenue-option scan before build | todo | filler lane for silent running; identify profitable/grant/leverage angles | no |
| MA-1 | Market Activity | 3 | Market activity tracker | blocked | reopen after CI-1 + push lanes run smoothly for a week | no |

## Parking lot rules

- Do not add a new active row unless it has a concrete next action.
- If an idea is interesting but not today's lane, capture it in the relevant project doc or `logs/daily_progress.md`, not as `doing`.
- When a task finishes, move it to `TASK_ARCHIVE.md` during the next hygiene pass.
- Silent running (Josh away): work the draft-only `todo` rows top-down; batch all approval asks into the next morning report.
- **KILLED by Josh taste call 2026-07-02: the IN-1 $690 research-services pilot.** Josh does not want to sell research services. Do not resurrect or propose service-selling offers; his research edge feeds the job lane and DeFi product ideation instead.
