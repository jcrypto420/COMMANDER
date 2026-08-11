# Weather Oracle — first Pi capture result note draft

Use this after the first local-only Pi capture proof run. This is a draft-only scaffold, not a claim that the run has happened yet.

## Draft closeout
- Run command: `python3 products/weather-oracle/capture_daily.py`
- Scope: local-only capture, no posting, no sending, no spending, no service changes
- Gate: `nws_forecast` and `openmeteo_models` both return `200` and write source files into a fresh capture directory

## One-line pass wording
- `Pass — fresh capture directory created; nws_forecast and openmeteo_models both returned 200 and wrote source files; result note saved locally.`

## One-line fail wording
- `Fail — capture did not produce a fresh directory and/or the robot baseline pair did not both return 200; note the missing files/statuses and leave the lane draft-only.`

## Operator note
- Single next safe action: run one local-only Pi capture proof once, then save the result note locally.
- Exact 200 gate: `manifest.sources.nws_forecast.status == 200` and `manifest.sources.openmeteo_models.status == 200`.
- Also confirm both gate rows wrote source files into the fresh capture directory.
- Update locally: `projects/weather-oracle.md`, `TASK_QUEUE.md`, `logs/daily_progress.md`, `logs/model_usage.csv`.
- Safety limits: no posting, no sending, no spending, no service changes.
- Keep the lane draft-only until the single local proof and note are recorded.

## Public-source recheck (2026-08-05)
- `nws_forecast` live URL: `https://api.weather.gov/gridpoints/OUN/97,94/forecast` — 200
- `openmeteo_models` live URL: `https://api.open-meteo.com/v1/forecast?latitude=35.4676&longitude=-97.5164&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&temperature_unit=fahrenheit&timezone=America%2FChicago&forecast_days=3` — 200
- Draft implication: the first Pi proof still points at live public inputs, so the remaining work is the local-only capture run and saved result note.

## Draft preflight snapshot (2026-08-08)
- Recheck status: both public/no-login gate endpoints returned 200 in a fresh local check today.
- `nws_forecast` status: 200
- `openmeteo_models` status: 200
- What changed: the note now has a literal 2026-08-08 preflight snapshot to copy into the eventual run record instead of relying on memory.
- Next safe action: run the single local-only Pi capture proof, then fill in the result note from the template.

## Draft preflight snapshot (2026-08-09)
- Recheck status: both public/no-login gate endpoints returned 200 in a fresh local check today.
- `nws_forecast` status: 200
- `openmeteo_models` status: 200
- What changed: the note now has a current 2026-08-09 preflight snapshot to copy into the eventual run record instead of relying on memory.
- Next safe action: run the single local-only Pi capture proof, then fill in the result note from the template.

## Live recheck details (2026-08-08)
- `nws_forecast`: 200 `application/geo+json`
- `openmeteo_models`: 200 `application/json; charset=utf-8`
- Draft implication: the public gate is still live, so the remaining work stays the local-only Pi proof and saved result note.

## Live recheck details (2026-08-09)
- `nws_forecast`: 200 `application/geo+json`
- `openmeteo_models`: 200 `application/json; charset=utf-8`
- Draft implication: the public gate is still live, so the remaining work stays the local-only Pi proof and saved result note.

## Live recheck details (2026-08-09 18:01)
- `nws_forecast`: 200 `application/geo+json`
- `openmeteo_models`: 200 `application/json; charset=utf-8`
- Draft implication: the gate is still live after a second same-day check, so the next real step remains the single local-only Pi capture proof and saved result note.

## Draft re-entry note (2026-08-08)
- This note is the current draft-only handoff for WO-2; keep the lane pointed at the single local-only Pi capture proof.
- The 2026-08-08 preflight snapshot is already captured here, so the next real step is to run `capture_daily.py` once on the Pi and fill the template immediately after.

## Draft re-entry note (2026-08-09)
- This note is the current draft-only handoff for WO-2; keep the lane pointed at the single local-only Pi capture proof.
- The 2026-08-09 preflight snapshot is already captured here, so the next real step is to run `capture_daily.py` once on the Pi and fill the template immediately after.

## Draft re-entry note (2026-08-11)
- This note is the current draft-only handoff for WO-2; keep the lane pointed at the single local-only Pi capture proof.
- The next real step is still one local-only Pi capture proof followed by an immediate fill-in of the saved result note.
- Keep the queue/project wording aligned with this handoff so the live board does not drift away from the draft packet.

## Copy/paste fill-in block
- timestamp (UTC):
- timestamp (Central):
- capture directory:
- exit code:
- `nws_forecast` status and file:
- `openmeteo_models` status and file:
- missing source files or reused-directory warning:
- one-line result:
- next action:

## Fill-in order after the run
1. timestamp (UTC)
2. timestamp (Central)
3. capture directory
4. exit code
5. `nws_forecast` status and file
6. `openmeteo_models` status and file
7. any missing source files or reused-directory warning
8. one-line result
9. next action
