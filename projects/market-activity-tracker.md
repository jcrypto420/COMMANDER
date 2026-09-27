# Market Activity Tracker

## Status — 2026-09-26
- **State:** PARKED (`MA-1` blocked) — config-wiring step implemented and smoke-tested; daily-snapshots design drafted; reopen after CI-1 loop runs smoothly for a week
- **Last advanced:** 2026-09-26 — new daily-snapshots design note `projects/market-activity-snapshots-draft.md` written; converts the vague "add daily snapshots" next action into a concrete, build-ready design (Option A: single capped history file, fetcher history-write first, then `/market` change-vs-yesterday panel)
- **Next action (on reopen):** implement the fetcher history-write step in `scripts/fetch_market_activity.py` (write `dashboard/market_activity_history.json` with `latest` + capped `snapshots[]` array), verify with a live run, then add a small `/market` "change vs yesterday" panel
- **Waiting on:** reopen condition (CI-1 week-smooth)
- **Draft artifacts:** `projects/market-activity-config-wiring-draft.md` (config-wiring, current — step implemented), `projects/market-activity-snapshots-draft.md` (daily-snapshots design, new 2026-09-26)

## Why this replaces the current angle

Josh does not want a service-offer-first crypto research angle right now. Better move: build a useful personal market activity dashboard that Josh actually wants, then open-source it if it becomes broadly useful.

## Product thesis

A local-first crypto/data-infrastructure market activity cockpit for researchers who want awareness without doom-scrolling or pretending every chart is a trade.

It should answer:

- What moved?
- What changed on-chain / in DeFi?
- Which projects/repos are active?
- What narratives are heating up?
- What deserves deeper reading today?

## Guardrails

- Personal research only; not financial advice.
- No automated trading.
- No wallet connections in v0.
- No paid APIs until Josh explicitly approves.
- No secrets committed.
- Open-source-friendly: public no-key data sources first.

## v0 built today

- Fetch script: `scripts/fetch_market_activity.py`
- Data artifact: `dashboard/market_activity.json`
- Dashboard route: `/market`
- Main Mission Control link: “Market activity tracker” card
- npm command: `npm run market:state`

Current public sources:

- CoinGecko public API: watched asset prices + trending coins
- DefiLlama public API: watched protocol TVL/activity
- GitHub public API: watched repo pulse

Initial watchlist:

- Assets: BTC, ETH, LINK, AAVE, UNI, MKR, ONDO
- Protocols: Chainlink, Aave, Uniswap, MakerDAO, Lido, Pendle, Ondo Finance, Ethena where available from DefiLlama
- Repos: smartcontractkit/chainlink, aave/aave-v3-core, Uniswap/v4-core, DefiLlama/dimension-adapters, ethereum/go-ethereum

## Next useful build step

- Wire `configs/market_watchlist.json` into the fetcher so watchlists become repo-editable without touching Python/JS.
- Then add daily snapshots so the dashboard shows change over time, not just latest state.

Draft-only prep note: `configs/market_watchlist.json` now exists as the repo-stored watchlist source, so the next code step can wire the fetcher to config instead of hard-coded lists.

## Open-source shape

Potential name later: `market-activity-cockpit` or `signal-cockpit`.

Open-source README should promise:

- local-first
- no keys required for v0
- no trading
- no advice
- configurable watchlists
- researcher workflow, not degen dopamine

## Approval / decision phrases

- `KEEP MARKET TRACKER DIRECTION` — make this the main build lane.
- `ADD MARKET WATCHLIST CONFIG` — implement editable watchlist config + daily snapshots.
- `PAUSE MARKET TRACKER` — keep the artifact but return to previous sprint work.
