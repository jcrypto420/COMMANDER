# Aave V3 — WBTC Snapshot Capture Checklist
## 2026-09-22 · draft-only, operator run sheet

**Status:** draft-only

This checklist is the operator-ready shape for capturing the next verified WBTC snapshot bundle. It does **not** authorize the capture; it only defines the exact bounded shape so the next pass is auditable and reproducible.

## Operator prerequisites

- [ ] Node.js environment available with RPC read access to Ethereum mainnet
- [ ] `ethers` or equivalent RPC client available for `eth_call` queries
- [ ] Write access to `products/boring-report/scorecard/snapshots/<date>/`
- [ ] The official Aave V3 Ethereum source file (`aave-v3-ethereum.sol`) is available and its SHA-256 is `296d81fb06bbef680126b527b5c6316c882c2e4329146bfeb14e40173662c6ab`

## WBTC anchors (from official Aave V3 source)

| Anchor | Value | Source |
|---|---|---|
| WBTC asset address | `0x2260fac5e5542a773db6da181b568c2e2d8d4093` | `WBTC_UNDERLYING` in Aave V3 Ethereum source |
| Expected feed address | `0x5424384b256154046e9667ddfaaa5e550145215e` | Baseline `rpc-source-wbtc-04.json` (to be re-confirmed) |
| Expected decimals | 8 | Baseline `rpc-feed-decimals-wbtc-04.json` (to be re-confirmed) |

## Snapshot capture steps

### Step 1: Capture WBTC asset source

- [ ] RPC method: `asset` on the Aave V3 Pool oracle contract
- [ ] Parameter: WBTC asset address `0x2260fac5e5542a773db6da181b568c2e2d8d4093`
- [ ] Expected: confirm the pool returns a non-zero asset ID for WBTC
- [ ] Write to: `rpc-source-wbtc-XX.json` (where XX is the sequence number for this capture)
- [ ] Content shape: `{ "method": "asset", "address": "<pool-address>", "param": "0x2260fac5e5542a773db6da181b568c2e2d8d4093", "result": "<asset-id>", "timestamp": "<iso-8601>" }`

### Step 2: Capture WBTC feed decimals

- [ ] RPC method: `decimals` on the WBTC feed oracle contract
- [ ] Feed address: confirm from Step 1's source snapshot, expect `0x5424384b256154046e9667ddfaaa5e550145215e`
- [ ] Expected: `8`
- [ ] Write to: `rpc-feed-decimals-wbtc-XX.json`
- [ ] Content shape: `{ "method": "decimals", "address": "<feed-address>", "result": 8, "timestamp": "<iso-8601>" }`

### Step 3: Capture WBTC latestRoundData

- [ ] RPC method: `latestRoundData` on the WBTC feed oracle contract
- [ ] Feed address: same as Step 2
- [ ] Expected fields: `roundId`, `answer`, `startedAt`, `updatedAt`, `answeredInRound`
- [ ] Write to: `rpc-feed-latestRoundData-wbtc-XX.json`
- [ ] Content shape: `{ "method": "latestRoundData", "address": "<feed-address>", "result": { "roundId": <n>, "answer": <price>, "startedAt": <ts>, "updatedAt": <ts>, "answeredInRound": <n> }, "timestamp": "<iso-8601>" }`

### Step 4: Capture oracle source

- [ ] Copy `aave-v3-ethereum.sol` from the official Aave address-book repository
- [ ] Write to: `aave-v3-ethereum.sol`
- [ ] Verify SHA-256: `296d81fb06bbef680126b527b5c6316c882c2e4329146bfeb14e40173662c6ab`

### Step 5: Build manifest

- [ ] Create `manifest.json` with SHA-256 and byte-count entries for every captured file
- [ ] Required entries:
  - `rpc-source-wbtc-XX.json`
  - `rpc-feed-decimals-wbtc-XX.json`
  - `rpc-feed-latestRoundData-wbtc-XX.json`
  - `aave-v3-ethereum.sol`
- [ ] Verify each SHA-256 matches the actual file on disk

### Step 6: Pre-comparison verification

- [ ] Re-hash the fresh bundle; reject if manifest hash or byte counts do not match
- [ ] Confirm WBTC asset address from fresh source snapshot matches `0x2260fac5e5542a773db6da181b568c2e2d8d4093`
- [ ] Confirm WBTC feed address and decimals from fresh snapshots match baseline values
- [ ] If any check fails, reject the bundle and do not proceed to comparison

## Comparison constraints (when fresh bundle lands)

1. Compare only against the 2026-08-14 baseline (`snapshots/2026-08-14/`)
2. Report only literal deltas in latest-round fields (round ID, timestamp, answer)
3. Make **no** heartbeat, staleness, completeness, or financial-advice claim
4. Use the reusable result-note template at `output/aave-v3-comparison-result-note-template.md`

## Boundaries

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No new snapshot until the fresh verified bundle gate is satisfied again.
- No claim that the comparison implies heartbeat, staleness, or completeness.

## Existing reusable handoffs

- Result-note template: `products/boring-report/scorecard/output/aave-v3-comparison-result-note-template.md`
- Filled-in WETH result note: `products/boring-report/scorecard/output/aave-v3-comparison-result-note-2026-09-22.md`
- Second-observation checklist: `products/boring-report/scorecard/output/aave-v3-second-observation-checklist.md`
- WBTC preflight note: `products/boring-report/scorecard/output/aave-v3-wbtc-preflight-note-2026-09-22.md`
- Reentry note: `products/boring-report/scorecard/output/aave-v3-comparison-reentry-note-2026-09-22.md`
