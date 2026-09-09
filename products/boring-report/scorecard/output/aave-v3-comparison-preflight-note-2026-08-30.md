# Aave V3 — Comparison Preflight Note
## 2026-08-30 · draft-only support

**Current handoff:** `products/boring-report/scorecard/output/aave-v3-change-log-pilot.md`

**Current compare surface:**
- Baseline bundle: `products/boring-report/scorecard/snapshots/2026-08-14/`
- Follow-up bundle: `products/boring-report/scorecard/snapshots/2026-08-16/`
- Asset set: WETH only

## Preflight rule

Keep the next FE-1 pass literal and narrow:
- compare only the verified bundle contents already on disk
- treat feed address and decimals as literal configuration fields
- treat latest-round fields as observation fields
- do not widen scope to a new snapshot run
- do not authorize publication, payment, account creation, or external send

## Carry-forward note

When a fresh verified bundle does exist, keep the WBTC-first plan queued for the next bounded asset and compare one new asset only against the existing verifier shape.

## Non-claims

- No heartbeat claim.
- No staleness claim.
- No completeness claim.
- No financial-advice claim.
- No new snapshot run.
- No publication.
- No payment.
- No account creation.
- No external send.
