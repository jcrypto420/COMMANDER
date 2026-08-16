# Aave V3 — Deployment Feed-Map Run Note

## Status

Draft-only. This local run produced a bounded fact file for a preferred Ethereum mainnet asset subset; it is not a completeness claim.

## Purpose

Turn the official Aave address-book anchor into one bounded fact file with source-cited feed addresses, decimals, and latest observed round timestamps.

## Inputs already anchored

- Official source: `https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol`
- Oracle address: `0x54586bE62E3c3580375aE3723C145253060Ca0C2`
- Pool address provider: `0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e`

## Result

- Created `facts/aave-v3-deployment-feed-map.json` and the 2026-08-16 follow-up fact file `facts/aave-v3-deployment-feed-map-2026-08-16.json`
- Baseline snapshots saved under `products/boring-report/scorecard/snapshots/2026-08-14/`
- Follow-up snapshots saved under `products/boring-report/scorecard/snapshots/2026-08-16/`
- Draft packet refreshed at `products/boring-report/scorecard/output/aave-v3-deployment-feed-map-draft.md`
- Follow-up checklist refreshed at `products/boring-report/scorecard/output/aave-v3-second-observation-checklist.md`

## Observed bounded asset set

- WETH baseline: 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 → 0x5424384b256154046e9667ddfaaa5e550145215e (decimals 8, updatedAt 1786748675)
- WETH follow-up: 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 → 0x5424384b256154046e9667ddfaaa5e550145215e (decimals 8, updatedAt 1786920059)

## Guardrails

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No completeness claim until the fact file is actually built and verified.
