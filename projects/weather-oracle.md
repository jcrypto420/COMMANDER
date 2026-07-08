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
- **Next action:** Josh verdict on direction; on GO → C0: port to CRE
  workflow, run in free local simulator (needs cre CLI install approval)
- **Waiting on:** Josh's go/no-go + working-name pick

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
