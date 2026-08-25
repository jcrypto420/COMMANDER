# Aave V3 — Second Observation Checklist
## Draft-only support note

**Status:** draft-only

This note exists to keep the next Aave deployment pass narrow and honest. The second observation bundle has now been captured; this note keeps the comparison step narrow and honest.

## Goal

Capture one independently verified follow-up snapshot bundle for the same bounded Aave V3 deployment feed-map, then compare it against the current baseline without making any heartbeat, staleness, completeness, or financial-advice claim.

## What must be true before the pass is considered usable

- The new snapshot bundle has its own `manifest.json` with SHA-256 and byte-count checks that pass.
- The oracle source still resolves from the official Aave address-book anchor.
- Each cited asset snapshot reproduces the feed address, decimals, and latest round data from its own hashed RPC reads.
- Any observed difference is reported as a literal configuration delta only.
- If nothing changed, the result stays a baseline comparison with no change claim.

## Exact next verifier shape

- Compare the 2026-08-16 snapshot directory alongside the current 2026-08-14 baseline bundle.
- Re-hash the new bundle before comparing anything.
- Reject any uncited deployment claim immediately.
- Keep the change-log renderer from turning an observation into a heartbeat or staleness statement.

## Current bounded asset set

- WETH only, from the 2026-08-14 baseline plus the 2026-08-16 follow-up bundle.

## Boundaries

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No claim that the map is complete.
- No claim that the comparison implies heartbeat, staleness, or completeness.

## Current re-entry note (2026-08-24)

- The follow-up bundle already exists, so the next pass is compare-only against the 2026-08-14 baseline.
- Render only literal configuration differences from the WETH baseline/follow-up pair.
- The local renderer already emits `output/aave-v3-change-log-pilot.md`, `.json`, and `.html`; the focused unit tests pass with the comparison status locked to literal configuration delta only.
- Keep the WBTC-first shortlist as the next bounded-asset plan after the compare, but do not schedule a new snapshot until the fresh verified bundle gate is satisfied again.
