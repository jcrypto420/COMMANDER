# Aave V3 — WBTC-First Snapshot Preflight Note
## 2026-09-22 · draft-only, local handoff

## Status

Draft-only. This note defines the exact bounded snapshot capture shape for the next WBTC-first Aave V3 comparison pass. It does **not** authorize a new snapshot run; it only keeps the next pass concrete and auditable.

## Why WBTC first

- The 2026-08-14 baseline already has a fully cited WBTC row (`rpc-source-wbtc-04.json`, `rpc-feed-decimals-wbtc-04.json`, `rpc-feed-latestRoundData-wbtc-04.json`).
- WBTC adds a different risk shape than WETH (wrapped BTC vs ETH) without widening the scope beyond one new asset.
- A fresh WBTC follow-up snapshot is the only missing piece before a WBTC-vs-baseline comparison is meaningful.

## Exact snapshot capture shape for the fresh WBTC bundle

When the fresh verified bundle is captured, it must include at minimum the following for WBTC:

| Snapshot file | RPC method | Purpose | Baseline reference |
|---|---|---|---|
| `rpc-source-wbtc-XX.json` | `asset` | Confirms the Aave V3 pool's asset address for WBTC | `snapshots/2026-08-14/rpc-source-wbtc-04.json` |
| `rpc-feed-decimals-wbtc-XX.json` | `decimals` on the feed oracle | Confirms feed decimals for WBTC | `snapshots/2026-08-14/rpc-feed-decimals-wbtc-04.json` |
| `rpc-feed-latestRoundData-wbtc-XX.json` | `latestRoundData` on the feed oracle | Captures the latest round ID, timestamp, and answer for WBTC | `snapshots/2026-08-14/rpc-feed-latestRoundData-wbtc-04.json` |

The bundle must also include:
- `aave-v3-ethereum.sol` — the official oracle source (same SHA-256 as the baseline: `296d81fb06bbef680126b527b5c6316c882c2e4329146bfeb14e40173662c6ab`)
- `manifest.json` — with SHA-256 and byte-count entries for every captured file

## WBTC asset and feed anchors (from the official Aave V3 source)

- WBTC asset address: `0x2260fac5e5542a773db6da181b568c2e2d8d4093` (from `WBTC_UNDERLYING` in the Aave V3 Ethereum source)
- WBTC feed: to be confirmed from the fresh `rpc-source-wbtc-XX.json` and matched against the baseline feed
- Expected baseline WBTC feed: `0x5424384b256154046e9667ddfaaa5e550145215e` (decimals 8) — to be re-confirmed against the fresh source snapshot

## Comparison constraints (when the fresh bundle lands)

1. Re-hash the fresh bundle first; reject if the manifest hash or byte counts do not match.
2. Confirm the WBTC asset address from the fresh source snapshot matches `0x2260fac5e5542a773db6da181b568c2e2d8d4093`.
3. Confirm the WBTC feed address and decimals from the fresh snapshots match the baseline values.
4. Report only literal deltas in the latest-round fields (round ID, timestamp, answer) as a configuration comparison.
5. Make no heartbeat, staleness, completeness, or financial-advice claim from the observed timestamps or deltas.

## Existing reusable handoffs

- Result-note template: `products/boring-report/scorecard/output/aave-v3-comparison-result-note-template.md`
- Second-observation checklist: `products/boring-report/scorecard/output/aave-v3-second-observation-checklist.md`
- Reentry note: `products/boring-report/scorecard/output/aave-v3-comparison-reentry-note-2026-09-22.md`
- Deployment feed-map run note: `products/boring-report/scorecard/output/aave-v3-deployment-feed-map-run-note.md`

## Boundaries

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No new snapshot until the fresh verified bundle gate is satisfied again.
- No claim that the comparison implies heartbeat, staleness, or completeness.
