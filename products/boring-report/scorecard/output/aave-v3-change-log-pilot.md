# Aave V3 Oracle & Collateral Change Log
## Pilot 0.2 — literal comparison

- **Network:** Ethereum mainnet
- **Baseline retrieved:** 2026-08-14T23:10:35.353Z
- **Follow-up retrieved:** 2026-08-16T23:02:31.643640+00:00
- **Scope:** Second bounded deployment feed-map observation for the same preferred asset subset on Ethereum mainnet; not a completeness claim.
- **Oracle anchor:** `0x54586bE62E3c3580375aE3723C145253060Ca0C2` — https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol

## Result

Feed address and decimals stayed unchanged from the baseline; only the latest round fields advanced.
The observed round timestamp is not a heartbeat or staleness determination.

| Asset | Baseline feed | Follow-up feed | Feed delta | Baseline decimals | Follow-up decimals | Round ID delta | Timestamp delta | Answer delta |
|---|---|---|---|---:|---:|---:|---:|---:|
| WETH | `0x5424384b256154046e9667ddfaaa5e550145215e` | `0x5424384b256154046e9667ddfaaa5e550145215e` | unchanged | 8 | 8 | 48 | 171384 | -1073962092 |

## Evidence

### WETH

- **baseline source:** `products/boring-report/scorecard/snapshots/2026-08-14/aave-v3-ethereum.sol`
- **baseline asset_source:** `products/boring-report/scorecard/snapshots/2026-08-14/rpc-source-weth-00.json`
- **baseline feed_decimals:** `products/boring-report/scorecard/snapshots/2026-08-14/rpc-feed-decimals-weth-00.json`
- **baseline feed_latest_round_data:** `products/boring-report/scorecard/snapshots/2026-08-14/rpc-feed-latestRoundData-weth-00.json`
- **follow-up source:** `products/boring-report/scorecard/snapshots/2026-08-16/aave-v3-ethereum.sol`
- **follow-up asset_source:** `products/boring-report/scorecard/snapshots/2026-08-16/rpc-source-weth-01.json`
- **follow-up feed_decimals:** `products/boring-report/scorecard/snapshots/2026-08-16/rpc-feed-decimals-weth-01.json`
- **follow-up feed_latest_round_data:** `products/boring-report/scorecard/snapshots/2026-08-16/rpc-feed-latestRoundData-weth-01.json`

## Boundaries

- Bounded deployment evidence only; the asset set is not complete.
- No public posting, payment, settlement, account creation, or external send occurred.
- Re-run `python3 verify_scorecard.py` before consuming this pilot; it hashes the source bundle and reproduces the cited deployment claims.
