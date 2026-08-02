# Weather Oracle — exact Pi one-shot capture run sheet

## Purpose
Run `capture_daily.py` once on the Pi, keep it local-only, and verify that the robot-baseline gate lands cleanly in a fresh capture directory.

## Safety boundaries
- Local-only capture
- No posting
- No sending
- No spending
- No service changes
- No account creation

## Exact run
1. `cd /home/josh/COMMANDER`
2. Confirm the working tree is clean enough to run the capture once.
3. Run `python3 products/weather-oracle/capture_daily.py`
4. Watch for the summary line like `YYYY-MM-DD_HHMM: X ok, Y failed`.
5. Open the new `products/weather-oracle/captures/<YYYY-MM-DD_HHMM>/manifest.json`.
6. Verify the pass gate:
   - `manifest.sources.nws_forecast.status == 200`
   - `manifest.sources.openmeteo_models.status == 200`
   - both rows wrote source files to the run directory
7. Check the run directory contains the expected receipt set when sources cooperate:
   - `manifest.json`
   - `nws_forecast.json`
   - `nws_forecast_hourly.json`
   - `openmeteo_models.json`
   - `openmeteo_hourly.json`
   - `nws_cli_okc.json`
   - `obs_kokc.json`
   - `obs_kpwa.json`
   - `obs_ktik.json`
   - `obs_koun.json`
   - `koco.html.gz`
   - `news9.html.gz`
   - `okcfox.html.gz`
   - `kfor.html.gz`
   - `kfor_7day.jpg`
8. Save the result note from `projects/weather-oracle-capture-result-note-template.md`.

## Pass / fail
Treat the run as a pass only if all of the following are true:
- the script exits `0`
- a fresh timestamped `captures/<YYYY-MM-DD_HHMM>/` directory is created
- `manifest.json` exists in that directory
- `nws_forecast` is present with `status: 200`
- `openmeteo_models` is present with `status: 200`
- the manifest records source files for both baseline rows

Treat the run as a fail if any of the following happen:
- no new timestamped capture directory appears
- `manifest.json` is missing
- either baseline row is missing or non-200
- the directory is reused or stale
- the run requires any posting, sending, spending, or service change to succeed

## Result-note checklist
Record these fields immediately after the run:
- timestamp (UTC)
- timestamp (Central)
- capture directory
- exit code
- `nws_forecast` status and file
- `openmeteo_models` status and file
- `nws_forecast_hourly` status
- `nws_cli_okc` status
- `obs_kokc` / `obs_kpwa` / `obs_ktik` / `obs_koun` status
- `koco` / `news9` / `okcfox` / `kfor` status
- `kfor_7day` status
- missing source files, if any
- reused directory warning, if any
- one-line result and next action

## Common failure modes

- stale capture directory from a prior run; clear or ignore old artifacts before reading results
- source fetch returns 4xx/5xx or times out; treat as upstream failure, not a local pass
- manifest missing expected entries; do not assume success from partial files alone
- non-gate sources fail after the gate pair passes; note the partial receipt set and keep the pass/fail decision tied only to `nws_forecast` + `openmeteo_models`
- reused folder or timestamp collision; ensure the run writes to a fresh path before trusting artifacts
- operator rule: save the result note and stop; do not retry by changing services or sending anything

## Canonical references
- Verification packet: `projects/weather-oracle-capture-verification-packet.md`
- Result-note template: `projects/weather-oracle-capture-result-note-template.md`
- Capture script: `products/weather-oracle/capture_daily.py`
