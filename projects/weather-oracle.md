# Project: Weather Oracle MVP (Priority 4)

## Status — 2026-08-09
- **State:** WO-1 revenue scan still stands as the concept anchor: **"Forecast Receipts"** (working name, Josh names it) — a Chainlink CRE cron workflow that commits multi-provider forecasts onchain BEFORE the weather happens (NWS + Open-Meteo models; $0 keyless sources), fetches official station actuals next day, and maintains rolling per-forecaster skill scores onchain.
- **Business model (Josh's framing):** Josh sponsors the LINK/gas (testnet $0 now; mainnet = cheap L2 writes + CRE billing TBD, early access); money made another way: (1) Polymarket weather-trader audience; (2) deadpan weatherman-grading content flywheel → sponsorship; (3) Chainlink grant/showcase; (4) career proof-of-work side effect.
- **WO-2 draft artifact:** the one-shot Pi capture verification packet now exists at `projects/weather-oracle-capture-verification-packet.md`.
- **WO-2 draft-only preflight:** the live `capture_daily.py` gate and the packet now match — the run succeeds only if `nws_forecast` and `openmeteo_models` land in the manifest with 200 and source files present. The packet now also includes a Pi execution checklist so the first proof run is easy to audit.
- **WO-2 result note draft:** the packet now includes a post-run result-note template so the first Pi verification can record the capture dir, exit code, and the two required 200 statuses in one pass.
- **WO-2 result-note draft tightening (2026-08-03):** the scaffold now has a copy/paste fill-in block for UTC/Central timestamps, capture directory, exit code, the two baseline statuses, warnings, and next action.
- **WO-2 public source inventory:** the packet now also names the no-login NWS and Open-Meteo endpoints used for the first proof run so the audit trail points at the actual inputs, not just the manifest gate.
- **WO-2 reusable result note:** a compact template now exists at `projects/weather-oracle-capture-result-note-template.md` so the eventual Pi run can record the manifest fields without inventing a format on the spot.
- **WO-2 first-run result-note draft:** a prefilled draft scaffold now exists at `projects/weather-oracle-capture-result-note-draft.md` so the first proof run can be written up immediately after the capture.
- **WO-2 script-shape alignment:** the packet/result note now match the live `capture_daily.py` source list, including the hourly NWS/Open-Meteo captures, CLI report, station observations, and the archived HTML/image receipts.
- **WO-2 public-source sanity check (2026-07-30):** live no-login NWS and Open-Meteo endpoints both returned 200 in a quick draft check, so the packet points at the real public inputs before the first Pi verification run.
- **WO-2 draft-only verification note (2026-07-30):** the live `capture_daily.py` source list also includes `nws_cli_okc`, `openmeteo_hourly`, station observations, and `kfor_7day`, so the draft packet/template stay aligned with the full capture surface while the hard gate remains the two robot baselines.
- **WO-2 draft-only re-entry (2026-07-31):** Codex confirmed the next safe step is the exact Pi run sheet for the `nws_forecast` + `openmeteo_models` 200 gate, with the manifest/result-note checklist; no external action was taken.
- **WO-2 draft-only run sheet (2026-07-31):** the exact local-only Pi run sheet now exists at `projects/weather-oracle-capture-run-sheet.md`, and it is linked back into the packet/result-note flow.
- **WO-2 draft-only closeout (2026-08-02):** the packet, run sheet, and result-note template now form a complete local-only proof bundle; the only next step is the single Pi capture run and manifest check, with no posting, sending, spending, or service changes.
- **WO-2 draft-only re-entry (2026-08-02):** the lane stays pointed at the single local-only Pi capture proof, and the queue/result-note wording is aligned so the eventual manifest check is easy to audit.
- **WO-2 draft-only run-sheet hardening (2026-08-02):** the local-only Pi run sheet now includes a short common-failure-modes section so the one-shot proof can stop cleanly after the result note.
- **WO-2 public-source recheck (2026-08-04):** the no-login NWS forecast and Open-Meteo baseline URLs behind the capture gate both returned 200 again today, so the draft packet still points at live public inputs rather than a dead reference.
- **WO-2 operator note draft (2026-08-04):** the draft result-note scaffold now includes a terse operator note that names the single next safe action, the exact 200 gate, the local files to update, and the no-posting/no-sending/no-spending/no-service-change safety limits.
- **WO-2 public-source recheck (2026-08-05):** the live no-login NWS forecast and Open-Meteo baseline URLs behind the capture gate both returned 200 again today, so the draft packet still points at current public inputs rather than a stale reference.
- **WO-2 draft preflight snapshot (2026-08-05):** the result-note draft now carries the literal 200 recheck plus the next safe action, so the eventual Pi proof can be recorded without inventing a format on the spot.
- **WO-2 public-source recheck (2026-08-08):** the live no-login NWS forecast and Open-Meteo baseline URLs behind the capture gate both returned 200 again during today’s draft pass, so the draft packet still points at live public inputs rather than a stale reference.
- **WO-2 public-source recheck (2026-08-09):** the live no-login NWS forecast and Open-Meteo baseline URLs behind the capture gate both returned 200 again during today’s draft pass, so the draft packet still points at live public inputs rather than a stale reference.
- **WO-2 public-source recheck (2026-08-09 18:01):** a second live no-login NWS forecast and Open-Meteo gate check still returned 200 for both endpoints, so the draft handoff remains the single local-only Pi capture proof and saved result note.
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
- [x] WO-2 draft-only checkpoint: the one-shot Pi capture verification packet, public source inventory, and reusable result-note template are all in place; the remaining step is the single local capture run.
- [x] WO-2 exact run sheet drafted: the local-only Pi checklist now exists and is linked from the packet/result-note flow.
- [x] WO-2 draft-only re-entry: queue wording, project status, and result-note language all point at the same single local-only Pi capture proof.
- [x] WO-2 first-run result-note draft: a prefilled scaffold now exists for the first proof run so the note can be filled in immediately after capture.
- [x] WO-2 public-source recheck: the live no-login NWS forecast and Open-Meteo baseline URLs behind the gate both returned 200 again, so the packet still references live public inputs.
- [x] WO-2 draft preflight snapshot: the result-note draft now includes the literal 2026-08-05 200 recheck and keeps the lane pointed at the single local-only Pi capture proof.
- [x] WO-2 public-source recheck (2026-08-08): the live no-login NWS forecast and Open-Meteo baseline URLs behind the gate both returned 200 again during today’s draft pass, so the packet still references live public inputs.
- [x] WO-2 draft-only recheck (2026-08-08): the live no-login NWS forecast and Open-Meteo baseline URLs both returned 200 again during today’s draft pass, so the next step remains the single local-only Pi capture proof.
- [x] WO-2 draft-only re-entry (2026-08-08): the result-note draft now carries the current handoff note, keeping the lane pointed at the single local-only Pi capture proof and the immediate post-run fill-in.

## Notes

Prefer free/cheap data sources. Log any API that costs money before using it.
Do not build deeply until a revenue, grant, or portfolio-leverage path is clear.
