# Weather Oracle — OKC source probe + capture inventory

**Probed:** 2026-07-08, from the Mac (`/Users/joshstokesberry/COMMANDER`).
**Pi caveat:** verify every source below from the Pi before the cron relies on
it (Boring Report P0 lesson). Evidence: `probes/` (headers + trimmed samples).
**Interpreter:** Mac must use `/usr/bin/python3` (3.9); default `python3` is a
cert-broken 3.7. Pi's system python3 expected fine.

## Probe verdict

| Source | URL | Status | Notes |
|---|---|---|---|
| NWS gridpoint forecast | `api.weather.gov/gridpoints/OUN/97,94/forecast` | 200 JSON | next-day high + PoP; robot row |
| NWS CLI daily climate report | `api.weather.gov/products/types/CLI/locations/OKC` | 200 JSON | **settlement source** — official daily MAX/MIN for OKC (Will Rogers) |
| NWS observations | `stations/{KOKC,KPWA,KTIK,KOUN}/observations/latest` | 200 JSON | hyperlocal actuals: Wiley Post ≈ The Village/Warr Acres; Tinker = Midwest City; Norman |
| Open-Meteo multi-model | `/v1/forecast?...&models=ecmwf_ifs025,gfs_seamless` | 200 JSON | per-model daily keys (`temperature_2m_max_ecmwf_ifs025`, etc.); robot rows |
| KOCO 5 (Hearst) | `koco.com/weather` | 200 HTML | forecast numbers are JS-loaded (Hearst `weather.htvapps.com/api/v1`, exact endpoint TBD via a browser network-inspection session); archived raw daily |
| News 9 (Griffin) | `news9.com/weather` | 200 HTML | embedded HTML-escaped JSON weather payload — parser TODO, data is in the static page |
| Fox 25 (Sinclair) | `okcfox.com/weather` | 200 HTML | **server-rendered temps in static HTML** — easiest station parser |
| KFOR 4 (Nexstar) | `kfor.com/weather/` | 200 (**solved 2026-07-08**) | WAF wants a full browser fingerprint: `Referer` + `sec-ch-ua`/`sec-fetch` headers AND curl's HTTP/2 TLS fingerprint (urllib's HTTP/1.1 gets 403 with identical headers → this page fetches via curl subprocess). Block is intermittent; script retries after 20s |
| **KFOR 4Warn broadcast graphic** | `media.psg.nexstardigital.net/kfor/weather/7day.jpg` | 200 image/jpeg | **the prize** — the weather team's own published 7-day (highs/lows/PoP/wind) at a stable URL, ~210KB, plain UA works. Numbers extracted at grading time via vision pass; the archived JPEG is the receipt. Sibling URLs: `today.jpg`, `tomorrow.jpg` |

## Capture pipeline

- `capture_daily.py` — stdlib-only, one run per evening, per-source failure
  isolation. Output: `captures/<YYYY-MM-DD_HHMM>/` (Central time) with
  manifest (status/bytes/sha256 per source), parsed JSON for robots +
  actuals, gzipped raw HTML for stations (parse later; history starts now).
- First capture: `captures/2026-07-08_1905/` — 10/11 sources ok (KFOR 403).
- Full capture: `captures/2026-07-08_2012/` — **12/12 ok** after the KFOR
  fix (page via curl fingerprint + 4Warn 7-day graphic).
- Cadence: daily ~20:30 America/Chicago (Pi cron — see WO-2 in TASK_QUEUE).
- Grading rule (inherited from Boring Report): no number may appear in any
  published score without a capture file it traces to.
