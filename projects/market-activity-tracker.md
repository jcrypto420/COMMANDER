# Market Activity Tracker

## Status — 2026-08-25
- **State:** PARKED (`MA-1` blocked) — draft-only config prep underway; reopen after CI-1 loop runs smoothly for a week
- **Last advanced:** 2026-08-25 — config-wiring draft note added for the repo-stored watchlist
- **Next action (on reopen):** wire `configs/market_watchlist.json` into `scripts/fetch_market_activity.py`, then add daily snapshots
- **Waiting on:** reopen condition
- **Draft artifact:** `projects/market-activity-config-wiring-draft.md`

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
