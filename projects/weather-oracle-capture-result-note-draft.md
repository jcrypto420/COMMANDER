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
