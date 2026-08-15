# Aave V3 Oracle & Collateral Change Log
## Pilot 0.1 — baseline only

- **Network:** Ethereum mainnet
- **Retrieved:** 2026-08-14T23:10:35.353Z
- **Scope:** Bounded deployment feed-map fact file for a small preferred asset set on Ethereum mainnet; not a completeness claim.
- **Oracle anchor:** `0x54586bE62E3c3580375aE3723C145253060Ca0C2` — https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol

## Result

No prior verified baseline is supplied, so this pilot records the first comparison point and makes no change claim.
The observed round timestamp is not a heartbeat or staleness determination.

| Asset | Configured feed | Decimals | Observed round ID | Observed round timestamp |
|---|---|---:|---:|---:|
| WETH | `0x5424384b256154046e9667ddfaaa5e550145215e` | 8 | 36893488147419126011 | 1786748675 |

## Evidence

### WETH

- **source:** `products/boring-report/scorecard/snapshots/2026-08-14/aave-v3-ethereum.sol`
- **asset_source:** `products/boring-report/scorecard/snapshots/2026-08-14/rpc-source-weth-00.json`
- **feed_decimals:** `products/boring-report/scorecard/snapshots/2026-08-14/rpc-feed-decimals-weth-00.json`
- **feed_latest_round_data:** `products/boring-report/scorecard/snapshots/2026-08-14/rpc-feed-latestRoundData-weth-00.json`

## Boundaries

- Bounded deployment evidence only; the asset set is not complete.
- No public posting, payment, settlement, account creation, or external send occurred.
- Re-run `python3 verify_scorecard.py` before consuming this pilot; it hashes the source bundle and reproduces the cited deployment claims.
