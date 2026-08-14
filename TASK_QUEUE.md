# TASK_QUEUE.md

Active task board only. Completed history lives in `TASK_ARCHIVE.md` and narrative progress lives in `logs/daily_progress.md`.

Status: `todo` / `doing` / `blocked` / `done`.
Approval = does this need Josh's OK before acting? (see `SECURITY.md`).

Operating rule: exactly one `doing` DECISION lane for Josh; Hermes may advance up to 3 draft-only lanes per day (see `COMMANDER_LOOP.md` intensity rules). Parked lanes are `blocked` with a clear reopen condition, not half-active.
Josh's calibration (2026-07-02 interview): job lane = primary decision lane; Bad Boys + Primoscapes + DeFi product ideation = the push lanes; same-day 60-second verdicts in the 8–9am window; reports must shrink (CC-24).

| ID | Project | Pri | Task | Status | Next action | Approval |
|----|---------|-----|------|--------|-------------|----------|
| FE-1 | Family Freedom Engine / Boring Report | 1 | First sellable proof — paid agent evidence primitive | doing | Extend `verify_scorecard.py` so it hashes the new 2026-08-14 snapshot bundle and rejects uncited deployment claims; the first bounded WETH fact row is already landed, while heartbeat/staleness stay zero-claim. Reuse the new local run note as the next draft-only checklist. | publish/payment/account gate later |
| CI-1 | Career/Income | 1 | Global high-compensation cash runway | todo | Ripple Treasury Manager packet / decision brief / form-prep note stays the live decision surface; keep the official-source non-Coinbase scan queued behind Josh’s hold/tweak/kill verdict. | **yes** to submit/send |
| WO-2 | Weather Oracle | 2 | Compounding capture loop | blocked | Reopen only after the Boring Report proves paid demand or when a buyer/partner wedge makes Forecast Receipts commercially concrete. | no |
| BB-25 | Bad Boys/Joycat | 3 | CARTOON LAB | blocked | Reopen only after Family Freedom Engine proof or explicit Josh creative call. Prior experiments are rejected; no more composite-video churn. | gate 2 |
| PS-1 | Primoscapes | 2 | Fall Native Prairie prep | blocked | Reopen when Josh supplies price basis, licensing/insurance status, and public-name call; then turn it into one real offer and outreach test. | yes to send |
| CC-21 | Command Center | 3 | Model-worker benchmark + cron pinning | done→archive | `openai-codex/gpt-5.4-mini` passed the structured operator benchmark in 19s; all 6 active agent crons are now explicitly pinned to it. Reopen only if the next scheduled run fails. | no |
| BB-26 | Bad Boys/Joycat | 3 | Idea-bank cron | blocked | Reopen only after one finished Bad Boys clip has been reviewed. Finished media outranks premise-bank automation. | **yes** |
| CC-24 | Command Center | 3 | 5-line daily dispatch | done→archive | Retired as a perpetual parser-check lane. Fix only if an actual dispatch failure recurs. | no |
| CC-19/18/22/23/10/13 | Command Center | 3 | Legacy system build tasks | done→archive | Retired from the active board; reopen only for a demonstrated runtime failure or explicit Josh request. | no |
| BB-24/17/23 | Bad Boys/Joycat | 3 | Merch/posting/account theory | blocked | Reopen after a real clip receives a keep verdict or public signal. | **yes** |
| MA-1 | Market Activity | 3 | Market activity tracker | blocked | Reopen only if it directly feeds the flagship scorecard or a specific paid opportunity. | no |

## Parking lot rules

- Do not add a new active row unless it has a concrete next action.
- If an idea is interesting but not today's lane, capture it in the relevant project doc or `logs/daily_progress.md`, not as `doing`.
- When a task finishes, move it to `TASK_ARCHIVE.md` during the next hygiene pass.
- Silent running (Josh away): work the draft-only `todo` rows top-down; batch all approval asks into the next morning report.
- **KILLED by Josh taste call 2026-07-02: the IN-1 $690 research-services pilot.** Josh does not want to sell research services. Do not resurrect or propose service-selling offers; his research edge feeds the job lane and DeFi product ideation instead.
