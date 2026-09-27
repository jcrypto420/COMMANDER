# Aave V3 — Comparison Run Note
## 2026-09-06 · draft-only, local compare surface

## Status

Draft-only. This note keeps the compare-only FE-1 handoff small and readable; it does not authorize a new snapshot run.

## Purpose

Provide one reusable local run note for the next literal Aave V3 comparison pass so the operator can stay on the current WETH baseline/follow-up surface without re-deriving the shape.

## Inputs already anchored

- Current handoff: `products/boring-report/scorecard/output/aave-v3-comparison-reentry-note-2026-09-06.md`
- Baseline bundle: `products/boring-report/scorecard/snapshots/2026-08-14/`
- Follow-up bundle: `products/boring-report/scorecard/snapshots/2026-08-16/`
- Asset set: WETH only
- Reusable result-note template: `products/boring-report/scorecard/output/aave-v3-comparison-result-note-template.md`

## Next bounded step

When a fresh verified bundle exists, compare the new bounded asset against the current WETH baseline using the existing verifier shape and literal-delta wording only.

## Local result constraints

- Keep WBTC first until the fresh verified bundle gate is satisfied again.
- Record only literal changes and explicit non-claims.
- No new snapshot run.
- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No heartbeat claim.
- No staleness claim.
- No completeness claim.
- No financial-advice claim.
