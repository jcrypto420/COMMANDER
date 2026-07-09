# Project: Weather Oracle MVP (Priority 4)

## Status — 2026-07-08
- **State:** WO-1 revenue scan DRAFTED (Josh-prompted CRE ideation session) —
  concept: **"Forecast Receipts"** (working name, Josh names it): a Chainlink
  CRE cron workflow that commits multi-provider forecasts onchain BEFORE the
  weather happens (NWS + Open-Meteo models; $0 keyless sources), fetches
  official station actuals next day, and maintains rolling per-forecaster
  skill scores onchain. The commit-before-outcome receipt is the thing no
  offchain accuracy site (ForecastAdvisor) can match; nobody does forecaster
  accountability onchain (AccuWeather sells data via its Chainlink node;
  Arbol/dClimate do B2B insurance — checked 2026-07-08).
- **Business model (Josh's framing):** Josh sponsors the LINK/gas (testnet $0
  now; mainnet = cheap L2 writes + CRE billing TBD, early access); money made
  another way: (1) Polymarket weather-trader audience — 200+ weather markets,
  ~$18.8M category volume, daily NWS-settled temperature markets; skill data
  is handicapping edge → dashboard/newsletter/x402 API; (2) deadpan
  weatherman-grading content flywheel (Bad Boys production skills) →
  sponsorship; (3) Chainlink grant/showcase — clean canonical CRE demo
  (cron + consensus HTTP + EVM write); (4) career proof-of-work side effect.
- **Next action:** CAPTURE PIPELINE LIVE, ALL 12 SOURCES (Josh GO
  2026-07-08): KFOR SOLVED same evening — page needs curl's HTTP/2
  fingerprint + full browser headers, AND the 4Warn team's broadcast 7-day
  graphic found at a stable URL (`media.psg.nexstardigital.net/kfor/weather/
  7day.jpg` — the human forecast itself; vision-pass extraction at grading,
  JPEG is the receipt). Full capture: `captures/2026-07-08_2012/`.
  Next: Hermes installs Pi cron (WO-2), then Fox 25 + News 9 parsers.
  CRE layer deferred by Josh ("can do CRE later").
- **Waiting on:** name (batches 1+2 rejected; next angle: name the thing
  after it exists — working title stays "weather-oracle")

## MVP spec — OKC metro first (2026-07-08 session)

- **Name candidates (Josh picks):** Partly Wrong (rec) · Hindcast ·
  The Dry Line · They Said Sunny · Forecast Receipts.
- **Why OKC:** most weather-obsessed TV market in the US (SPC/National
  Weather Center in Norman, Oklahoma Mesonet ~120 stations, legendary
  channel weather wars). Audience already keeps score; we add receipts.
- **Graded rows (~7):** KFOR, KOCO 5, News 9, Fox 25, NWS Norman + ECMWF/GFS
  robot baselines ("is Channel 4 beating a free robot?"). Social forecaster
  row possible if predictions are documented enough to capture fairly.
- **Mechanics:** Day-0 evening capture of station-site next-day high/low/PoP
  (numbers = facts; screenshot archive as evidence) → hash committed onchain
  via CRE before outcomes; Day-1 actuals from official stations (Will Rogers
  KOKC; Wiley Post = The Village/Warr Acres; Tinker = Midwest City; Norman;
  Mesonet pending commercial-license check).
- **Scores:** temp MAE, precip Brier, and the Hype Index (severe/precip
  overcall bias) — the argue-about-it-at-work metric.
- **10¢ hyperlocal tier (x402):** skill-weighted consensus + "who to trust
  tonight" per suburb (Edmond, Warr Acres, The Village); hyperlocal grain
  from 3km model data + nearest-station actuals, honestly labeled.
- **Edge law:** grade channels/broadcasts, never named meteorologists.
- **Sequencing:** capture pipeline can start NOW ($0, read-only, no
  approvals) — skill scores need weeks of history; CRE commit layer bolts
  on at C0 after cre CLI install approval; x402/mainnet gated later.

**Goal:** Keep warm unless it can become a profitable side income, grant /
public-good project, portfolio asset, or product.

**Concept:** Hold local news/weather stations accountable and provide better
local weather insight, ideally using Chainlink where it creates real leverage.

## Outputs

- Repo cleanup
- Forecast source ingestion
- Local news/weather scraping or API alternatives
- Actuals comparison
- Accuracy scoring
- Frontend improvements
- README / demo documentation
- GitHub issues

## Status

- [ ] Repo cleanup pass
- [ ] Revenue-option scan before build work
- [ ] One forecast source ingested
- [ ] Actuals vs forecast comparison
- [ ] Accuracy score v0
- [ ] README/demo doc

## Notes

Prefer free/cheap data sources. Log any API that costs money before using it.
Do not build deeply until a revenue, grant, or portfolio-leverage path is clear.
