# Project: Weather Oracle MVP (Priority 4)

## Status — 2026-07-25
- **State:** WO-1 revenue scan still stands as the concept anchor: **"Forecast Receipts"** (working name, Josh names it) — a Chainlink CRE cron workflow that commits multi-provider forecasts onchain BEFORE the weather happens (NWS + Open-Meteo models; $0 keyless sources), fetches official station actuals next day, and maintains rolling per-forecaster skill scores onchain.
- **Business model (Josh's framing):** Josh sponsors the LINK/gas (testnet $0 now; mainnet = cheap L2 writes + CRE billing TBD, early access); money made another way: (1) Polymarket weather-trader audience; (2) deadpan weatherman-grading content flywheel → sponsorship; (3) Chainlink grant/showcase; (4) career proof-of-work side effect.
- **WO-2 draft artifact:** the one-shot Pi capture verification packet now exists at `projects/weather-oracle-capture-verification-packet.md`.
- **WO-2 draft-only preflight:** `products/weather-oracle/capture_daily.py` now matches the packet's hard gate — the run succeeds only if `nws_forecast` and `openmeteo_models` land in the manifest with 200 and source files present. Next action remains the Pi one-shot capture verification.
- **Travel redundancy (2026-07-08, Josh away from home):** Mac LaunchAgent `com.commander.weather-capture` runs the capture nightly 20:35 Mac-local (fires on next wake if asleep) → `logs/weather_capture_mac.log`. Capture-only, no git actions; sessions commit accumulated captures. Remove with: `launchctl unload ~/Library/LaunchAgents/com.commander.weather-capture.plist && rm` that file. Pi cron remains the primary once Hermes confirms WO-2.
- **Waiting on:** name (batches 1+2 rejected; working title stays "weather-oracle")

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
- **Voice law (Josh, 2026-07-10):** the paper is the straight man — "leave
  the corniness to the newscaster." No stamps, no quips in utility copy,
  no editorial winks. The humor budget is the headline verdict only, and
  even that must be a finding ("SKY REMAINS UNDEFEATED"), not a joke.
  Fine Print = plain declarative utility. The material is funny; we are not.
- **Design law (2026-07-10):** newsprint/almanac direction locked (v3):
  Didot masthead + ears, wood-type headline, Courier agate tables,
  OFF-THE-WIRE teletype block quoting the official verdict, ink-line hour
  strip. "Corpo" (system sans, hairlines, chips) is dead.
- **Palette law (2026-07-10, Josh: "Oklahoma blue and green, analog"):**
  cream paper #f4eddd · blue-black ink #24303a · semantic colors only:
  **Oklahoma blue #2f6ca8 = the sky** (section heads, THE SKY verdict rows)
  · **prairie green #3e6b4f = receipts/provenance** · **burnt orange
  #c65d21/#a83415 = ran hot** · **teal #2a7f7a = ran cold** · **gold
  #a8770f ring = exact hit** · hype index stays warm (hot air). Reference
  render: `design/weekly_scorecard_v4_1.html`. Punch card is the Side B
  hero; AVG + HITS columns on the card, W–L lives in standings with the
  round-robin explainer.
- **Sequencing:** capture pipeline can start NOW ($0, read-only, no
  approvals) — skill scores need weeks of history; CRE commit layer bolts
  on at C0 after cre CLI install approval; x402/mainnet gated later.

## Report design + marketing (drafted 2026-07-08, Josh session)

### Design — the unit is the receipt

1. **Weekly Scoreboard (anchor artifact):** one card. Masthead + week +
   "OKC metro". Leaderboard rows: source | avg high-temp miss | rain
   calibration | letter grade. Robots (NWS/ECMWF/GFS) interleaved with
   channels and tagged "(robot)" — the standing storyline is humans vs a
   free robot.
2. **Receipt of the Week:** two panels — the archived forecast (4Warn
   graphic crop / station capture, timestamp + sha) beside what the sky
   did (official CLI number). One deadpan caption. This is the shareable
   unit; the scoreboard is the habit unit.
3. **Robot Check strip:** one sentence ("A free robot beat 3 of 4
   stations this week").
4. **Hype Index meter** per channel — rain/doom overcall bias. The
   argue-at-work metric.
5. **Fine print:** methodology line + "every number traces to an archived,
   hash-stamped capture" (+ onchain commit ref once CRE lands).
6. **Render targets:** design once (HTML), export three crops — 9:16
   (TikTok/Reels/Shorts), 1:1 (X/IG card), 16:9/PDF (web + Gate Deck).
   Reuses the Bad Boys render line.
7. **Voice:** deadpan referee, Boring-Report-adjacent but warmer;
   praise-forward when humans win. Never mean to people; grade
   institutions. Recurring sign-off: "Outlook: revised."

### Marketing — OKC playbook

- **Audience order:** OKC normies (funny) → #okwx nerds/chasers
  (credibility) → Polymarket weather traders (money) → the stations
  themselves (earned media).
- **Channels:** weekly 30s vertical video + X post into #okwx + Reddit
  r/oklahomacity thread; Facebook page later (OK weather fandom is
  FB-native) — account creation/posting = Josh gates.
- **Cadence:** Sunday evening "Weekly Receipts" + opportunistic "receipt
  pending…" teaser on big-miss days. Storm season = distribution spikes.
- **Growth loops:** tag channels when they WIN (mets amplify wins; keeps
  the brand a referee, not a dunk account); suburb shout-outs
  (Edmond/Moore/Norman) for local shares; "who do we grade next" polls.
- **Launch:** collect quietly 2–3 weeks → soft-launch with "we've been
  keeping receipts since July 8" + season-to-date table → weekly cadence.
  First public post = a real SHIPPED item on the NOW.md scoreboard.
- **Monetization staging:** local sponsor line on the card after traction
  ("This week's receipts brought to you by ___" — Braum's energy) → 10¢
  x402 hyperlocal tier after the CRE layer → trader dashboard later.
- **Pre-gate drafting:** content drafts and card renders can pile up ahead
  of Josh's account/posting gates per the intensity principle.

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
