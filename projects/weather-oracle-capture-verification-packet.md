# Weather Oracle — one-shot Pi capture verification packet

## Goal
Verify that `products/weather-oracle/capture_daily.py` can run once on the Pi and produce one fresh timestamped capture directory with a valid manifest and the required NWS/Open-Meteo source files.

## Run shape
- **When:** local Pi cron target is ~20:30 America/Chicago
- **Command:** `cd /home/josh/COMMANDER && python3 products/weather-oracle/capture_daily.py`
- **Scope:** local-only capture, no posting, no sending, no spending, no service changes

## Expected output
A new directory under:

`products/weather-oracle/captures/<YYYY-MM-DD_HHMM>/`

Minimum expected files for a successful verification run:
- `manifest.json`
- `nws_forecast.json`
- `openmeteo_models.json`
- `openmeteo_hourly.json`

If the other sources succeed, the directory should also include:
- `nws_forecast_hourly.json`
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

## Pass criteria
Treat the run as a pass only if all of the following are true:
1. The script exits `0`.
2. A **fresh** timestamped `captures/<YYYY-MM-DD_HHMM>/` directory is created for the run.
3. `manifest.json` exists in that directory.
4. `manifest.sources.nws_forecast.status == 200`.
5. `manifest.sources.openmeteo_models.status == 200`.
6. The manifest records the source files for those two rows (`nws_forecast.json`, `openmeteo_models.json`).

## Fail criteria
Treat the run as a fail if any of the following happen:
- no new timestamped capture directory appears
- `manifest.json` is missing
- either `nws_forecast` or `openmeteo_models` is missing or non-200
- the output directory is a reused/stale folder instead of a fresh run
- the run requires any posting, sending, spending, or service change to succeed

## Verification note
The script is intentionally resilient to partial source failure; one bad source should not kill the run. For the verification packet, the hard gate is the robot baseline pair:
- NWS forecast
- Open-Meteo multi-model forecast

That matches the script’s own exit condition and keeps the first Pi check focused on the minimum viable capture proof.
