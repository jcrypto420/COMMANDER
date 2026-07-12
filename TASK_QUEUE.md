# TASK_QUEUE.md

Active task board only. Completed history lives in `TASK_ARCHIVE.md` and narrative progress lives in `logs/daily_progress.md`.

Status: `todo` / `doing` / `blocked` / `done`.
Approval = does this need Josh's OK before acting? (see `SECURITY.md`).

Operating rule: exactly one `doing` DECISION lane for Josh; Hermes may advance up to 3 draft-only lanes per day (see `COMMANDER_LOOP.md` intensity rules). Parked lanes are `blocked` with a clear reopen condition, not half-active.

Josh's calibration (2026-07-02 interview): job lane = primary decision lane; Bad Boys + Primoscapes + DeFi product ideation = the push lanes; same-day 60-second verdicts in the 8–9am window; reports must shrink (CC-24).

| ID | Project | Pri | Task | Status | Next action | Approval |
|----|---------|-----|------|--------|-------------|----------|
| CI-1 | Career/Income | 1 | Job search per `jobs/SEARCH_PLAYBOOK.md` | doing | 2026-07-12 Coinbase Institutional Business Operations packet is the next decision surface; Josh should approve apply / tweak / kill, while the old IN-1 research-services backstop stays historical | **yes** to send |
| CC-24 | Command Center | 1 | 5-line daily dispatch | todo | 2026-07-11 draft-only re-check packet is ready; next safe step is tomorrow's 07:30 parser re-check — assert 5 lines, confirm `Open:` / `Decide:` stay on line 4, keep exactly one bolded `Decision:`, then archive if clean | verify only |
| BB-25 | Bad Boys/Joycat | 1 | CARTOON LAB pilot — motion recovery | doing | `Collateral Damage` scene package is fixed: farmer uses carrot as loan collateral, receives coin, then destroys desk with it. Claude’s next build is the 12–15s locked-panel / 2D-composite cut in `projects/badboys-collateral-damage-motion-fix.md`; no Kling collision/character-action rerun. | gate 2 |
| BB-26 | Bad Boys/Joycat | 1 | Hermes idea-bank + MoA critics cron | todo | draft packet now also defines the weekly bank file shape, review packet, and first-run prompt skeleton; next safe step is Josh approval to verify the 10 premise prompts and approve the weekly cron surface | **yes** |
| BB-24 | Bad Boys/Joycat | 2 | First sellable artifact (sticker-pack v0) | todo | `Bad Boys Mark Sheet v0` decision packet is ready: three-piece die-cut sticker sheet; Fourthwall is the future low-overhead storefront after content signal. Next safe step is Josh approval for local print-ready masters + preview only. | no |
| BB-17 | Bad Boys/Joycat | 2 | Week 1 posting packet | todo | rebuild packet around real assets + bone-circle avatar so it is post-ready the day Josh creates the account | yes to post |
| BB-23 | Bad Boys/Joycat | 2 | TikTok account creation | todo | JOSH action (~30 min): create account per runbook; credentials/2FA stay Josh-only | **yes** |
| PS-1 | Primoscapes | 2 | Fall Native Prairie prep | doing | Offer v0 ("Native Prairie Patch Install") + real lead-channel list DONE (`projects/primoscapes.md`) — verified local orgs, no invented contacts, no outreach sent. BLOCKED on Josh: pricing model/number, licensing/insurance status, public name confirm | yes to send |
| DF-1 | DeFi/Chainlink | 2 | DeFi product lab | done→archive | co-ideation session 2026-07-05 produced 8 ranked concepts; Josh selected the merged "boring ratings" brand — see BR-0 | no |
| BR-1 | Boring Report | 1 | W28 v0 fixes + Gate 1 | doing | USYC/BUIDL/USDY asset-class fix DONE (Claude); generator/verifier de-duplicated to one scoring source; report regenerated + verified. NEXT: Josh reads W28 on Gate Deck (ship/kill/one-liner) — first flawless-streak week starts on his verdict | gate 1 |
| WO-2 | Weather Oracle | 2 | OKC daily capture cron | todo | Josh approved data collection 2026-07-08; first capture DONE from Mac (10/11 sources; KFOR 403 — see `products/weather-oracle/SOURCES.md`). Hermes: verify sources fetch from Pi, then install daily cron 20:30 America/Chicago → `python3 products/weather-oracle/capture_daily.py` + commit `captures/`. CRE layer deferred by Josh | no |
| CC-19 | Command Center | 1 | Midday + evening cron loops | todo | jobs live; morning loop recreated 07:30 pinned (drift-guard fix). Verify 1pm/6pm commits land 2026-07-03, then archive | verify only |
| CC-18 | Command Center | 1 | Loop sync protocol | todo | embedded in cron prompts step 0/8; verify no skipped pull on 2026-07-03, then archive | no |
| CC-21 | Command Center | 2 | Hermes self-audit | todo | skills/cron audit + `model_usage.csv` proved UNRELIABLE (claimed codex while OpenRouter billed $9.87 in 5 days incl. GPT-5.5 at $2.66 — log from response metadata, not assumption) + NEW RULE: Telegram alert whenever a fallback provider serves a call + conflict-resolution prefers REMOTE + auth.json backup (crash wiped codex creds 07-03 17:16) | no |
| CC-22 | Command Center | 2 | Mission Control: Gate Deck + PWA | todo | GATE DECK + PWA SHIPPED 2026-07-05 by Claude (/gate-deck live, manifest live, verdicts → capture-only inbox; Hermes had built only the nav link). Remaining: lane-status cards; HERMES RULE: read gate verdicts from dashboard/commander_inbox.jsonl (lane=gate-verdict) every loop | no |
| CC-23 | Command Center | 2 | Hermes browser chat | todo | phase 1 DONE 2026-07-02 (loopback :3012 + SSH tunnel, commander profile). Phase 2: password_hash + LAN bind + user systemd service (show unit file first) | **yes** |
| CC-10 | Command Center | 2 | Private phone access (Tailscale-first) | todo | try Tailscale SSH / dashboard before any chat platform | **yes** |
| CC-13 | Command Center | 3 | Test model-specific worker pattern | todo | run one cheap read-only worker and log result | no |
| WO-1 | Weather Oracle | 4 | Revenue-option scan before build | done→archive | DONE 2026-07-08 (Josh-directed CRE session): forecaster-accountability oracle, OKC-first — concept, business model, MVP spec all in `projects/weather-oracle.md` | no |
| WO-2 | Weather Oracle | 2 | OKC nightly capture cron on Pi | todo | Josh GO 2026-07-08; capture proven from Mac (12/12 sources incl. KFOR — `products/weather-oracle/SOURCES.md`). HERMES DO: (1) from repo root run `python3 products/weather-oracle/capture_daily.py`, confirm output "12 ok" (2) run `sh scripts/install_weather_capture_cron.sh` — idempotent, targets 20:30 America/Chicago (3) log result. Mac→Pi SSH dropped 2026-07-08 ~20:25 CT before Pi-side verify could run; if any source 403s from the Pi, record it in SOURCES.md, do not retry-spam | no |
| MA-1 | Market Activity | 3 | Market activity tracker | blocked | reopen after CI-1 + push lanes run smoothly for a week | no |

## Parking lot rules

- Do not add a new active row unless it has a concrete next action.
- If an idea is interesting but not today's lane, capture it in the relevant project doc or `logs/daily_progress.md`, not as `doing`.
- When a task finishes, move it to `TASK_ARCHIVE.md` during the next hygiene pass.
- Silent running (Josh away): work the draft-only `todo` rows top-down; batch all approval asks into the next morning report.
- **KILLED by Josh taste call 2026-07-02: the IN-1 $690 research-services pilot.** Josh does not want to sell research services. Do not resurrect or propose service-selling offers; his research edge feeds the job lane and DeFi product ideation instead.
