# Pons / Robinhood Chain alpha filter — read-only design

## Status

Implemented as a private Telegram watchlist monitor on 2026-09-02. It is a research filter, never a trading agent or recommendation engine.

## Verified source model

- **Pons v2 launch feed:** the current active-launch response supplies launch token, Pons factory, deployer, paired asset, progress, market cap, latest buy time, launch transaction/block, and graduated pool when one exists.
- **Robinhood official registry:** a pair is eligible only when its exact `pairToken` contract is an active Robinhood Stock Token on Robinhood Chain (`4663`). A ticker or token name never qualifies on its own.
- **Pons v2 protocol docs:** a custom-pair launch uses that asset for the curve, graduation threshold, and post-graduation Uniswap v4 pool. Pons' opening buy tax decays for five seconds; this monitor excludes launches younger than two minutes, not because two minutes makes them safe, but to avoid alerting during the documented opening window.

## Implemented gates

A new launch alerts only after two snapshots show all of the following:

| Gate | Threshold | Why it exists |
|---|---:|---|
| Exact official stock pair | required | Blocks ticker/name imitations. |
| Launch age | >= 120 seconds | Avoids the documented initial anti-snipe window and index lag. |
| Curve progress | >= 10% | Removes untouched launches. Graduation is **not** a quality claim. |
| Progress acceleration | >= +3 percentage points since prior 5-minute sample | Measures observed demand progression, not a single static value. |
| Last observed buy | <= 5 minutes old | Removes stalled curves. |
| Reported market cap | >= $5,000 | Removes trivial low-activity launches. |
| Recent distinct buyers | >= 4 in Pons' 15-minute indexed trade window | Blocks single-wallet or tiny-participant flow. |
| Recent buys | >= 6 in the same window | Requires repeated observed participation. |
| Net quote flow | >= +25% buy-skew | Rejects sell-dominant flow. |
| Largest buyer share | <= 70% of recent buy quote volume | Flags one-wallet concentration; it cannot prove wallet ownership links. |

A candidate must clear every gate, then is *ranked* on a 0–100 continuous score:
- 20 points: exact official contract match;
- 0–15: graduation progress, reaching full points at 50%;
- 0–20: progress acceleration, reaching full points at +10 percentage points per sample;
- 0–10: recency of the latest buy, decaying to zero at five minutes;
- 0–10: reported market cap, reaching full points at $25,000;
- 0–10: buyer diversity, reaching full points at 10 recent buyers;
- 0–15: net buy flow, reaching full points at +75% buy-skew.

The alert threshold is **70/100**. This prevents threshold-crossing launches from all receiving the same maximum score.

## Alert contents

Every candidate prints:
- launch-token contract and explorer URL;
- canonical Robinhood stock-token contract and explorer URL;
- Pons v2 factory contract, deployer wallet, launch transaction/block/time;
- graduated pool contract when the public launch feed exposes one (the zero address explicitly means pre-graduation; this feed does not expose the curve address);
- current progress, observed progress delta, market cap, and the literal gates cleared;
- recent buy/sell counts, unique buyers, net-flow skew, top-buyer concentration, and up to three top-buyer wallet addresses from Pons' indexed trade feed (explicitly **not** labeled profitable).

## Deliberately not claimed or scored

| Signal | Status | Reason |
|---|---|---|
| Realized wallet PnL / "top traders" | unavailable | A buy size or wallet balance does not establish profitability. This needs complete historical buys, sells, transfers, cost basis, and valuation reconstruction from indexed CurveBuy/CurveSell events. |
| Unique buyers / basic concentration | implemented, bounded | Pons' public v2 per-token trade feed provides recent buyer accounts. It supports participant count, net-flow and dominant-wallet checks, but not beneficial-ownership/cabal attribution. |
| Deployer win rate | unavailable | Needs a complete creator-to-prior-launch history plus outcome rules. |
| Fomo social confirmation | unavailable | Fomo publicly advertises a leaderboard, trader feed, and alerts, but its Robinhood Chain/Pons coverage plus an authorized export/API have not been verified. It will not be scraped or treated as source of truth. |

## Next valid upgrade

Add a read-only indexed event source for Pons v2 `CurveBuy` / `CurveSell` events, then calculate: distinct buyers, net quote flow, buyer-repeat behavior, and *separately labelled* realized PnL for wallets with enough complete history. Do not add auto-trading. Fomo may be an optional confirmation field only after documented coverage and permitted data access are proven.

## Runtime

- Config: `configs/pons_stock_alpha.json`
- Monitor: `scripts/pons_stock_alpha_alerts.py`
- State: ignored local path `runtime/pons_stock_alpha_state.json`
- Cadence: five minutes; silent when no new threshold-qualified candidate.
