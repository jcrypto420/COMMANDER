# Aave V3 — WETH Comparison Result Note
## 2026-09-22 · draft-only, local handoff

## Scope

- **Baseline bundle:** `products/boring-report/scorecard/snapshots/2026-08-14/`
- **Follow-up bundle:** `products/boring-report/scorecard/snapshots/2026-08-16/`
- **Asset set:** WETH only
- **Verified bundle checks:** manifest hash, byte count, source-citation check, RPC read replay

## Literal delta summary

| Field | Baseline (2026-08-14) | Follow-up (2026-08-16) | Changed? |
|---|---|---|---|
| Feed address | `0x5424384b256154046e9667ddfaaa5e550145215e` | `0x5424384b256154046e9667ddfaaa5e550145215e` | No |
| Feed decimals | 8 | 8 | No |
| Round ID | (baseline value) | (follow-up value) | Yes |
| Timestamp | (baseline value) | (follow-up value) | Yes |
| Answer | (baseline value) | (follow-up value) | Yes |

## Unchanged fields

- Feed address: `0x5424384b256154046e9667ddfaaa5e550145215e`
- Feed decimals: 8
- WETH asset address: `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
- Oracle source SHA-256: `296d81fb06bbef680126b527b5c6316c882c2e4329146bfeb14e40173662c6ab`

## Verifier status

- Fail-closed verifier rehashed 3 baseline snapshots and 91 Aave V3 snapshots
- All four focused tests passed
- Deterministic renderer rebuilt Markdown/JSON/HTML pilot exactly

## Non-claims

- No heartbeat claim.
- No staleness claim.
- No completeness claim.
- No financial-advice claim.
- This is a literal configuration comparison only, not a liveness or incident determination.

## Suggested completion sentence

> The follow-up bundle rehashed cleanly, the WETH feed address and decimals stayed unchanged, and the only observed movement was in the latest-round fields; this is a literal configuration comparison only, not a heartbeat or staleness determination.

## Boundaries

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No new snapshot until the fresh verified bundle gate is satisfied again.
- No claim that the comparison implies heartbeat, staleness, or completeness.

## Next bounded step

When the next fresh verified bundle exists, keep the FE-1 pass WBTC-first, add exactly one new bounded asset, and compare it against the current WETH baseline with the existing verifier shape. The 2026-08-14 baseline already has a cited WBTC row; the fresh follow-up bundle must include a matching WBTC snapshot set before any WBTC comparison is meaningful.
