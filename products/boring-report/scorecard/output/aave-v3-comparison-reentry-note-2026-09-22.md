# Aave V3 — Comparison Re-entry Note
## 2026-09-22 · draft-only, local handoff

## Scope

- **Current handoff:** `products/boring-report/scorecard/output/aave-v3-change-log-pilot.md`
- **Comparison baseline:** `products/boring-report/scorecard/snapshots/2026-08-14/` (WETH + WBTC + USDT + USDC + DAI + sUSD + wstETH subset)
- **Comparison follow-up:** `products/boring-report/scorecard/snapshots/2026-08-16/` (WETH only)
- **Asset set:** WETH only for the completed comparison; WBTC first queued for the next bounded asset

## Re-entry status

The compare-only pilot remains the current literal-comparison surface after the 2026-09-22 local verification pass. The verifier rehashed 3 baseline and 91 Aave snapshots and confirmed generated outputs remain exact; the four focused tests passed.

The completed WETH comparison (2026-08-14 baseline vs 2026-08-16 follow-up) still shows the feed address and decimals stayed unchanged; the only observed movement was in the latest-round fields. This is a literal configuration comparison only, not a heartbeat or staleness determination.

This note does **not** authorize a new snapshot run. It only keeps the next draft pass narrow and readable for Josh.

## What is already anchored

- Official Aave V3 Ethereum source: `https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol`
- Oracle address: `0x54586bE62E3c3580375aE3723C145253060Ca0C2`
- WETH asset: `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
- WETH feed: `0x5424384b256154046e9667ddfaaa5e550145215e` (decimals 8)
- Baseline WBTC snapshots already exist in `snapshots/2026-08-14/`:
  - `rpc-source-wbtc-04.json`
  - `rpc-feed-decimals-wbtc-04.json`
  - `rpc-feed-latestRoundData-wbtc-04.json`
- Reusable result-note template: `products/boring-report/scorecard/output/aave-v3-comparison-result-note-template.md`

## Next bounded step

When the next fresh verified bundle exists, keep the FE-1 pass WBTC-first, add exactly one new bounded asset, and compare it against the current WETH baseline with the existing verifier shape. The 2026-08-14 baseline already has a cited WBTC row; the fresh follow-up bundle must include a matching WBTC snapshot set before any WBTC comparison is meaningful.

## Non-claims / gates

- No heartbeat claim.
- No staleness claim.
- No completeness claim.
- No publication.
- No payment.
- No account creation.
- No external send.
- No new snapshot until the fresh verified bundle exists.
