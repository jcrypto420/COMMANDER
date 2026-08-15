# Aave V3 — Second Observation Checklist
## Draft-only support note

**Status:** draft-only

This note exists to keep the next Aave deployment pass narrow and honest. It does not claim a second observation has been captured yet.

## Goal

Capture one independently verified follow-up snapshot bundle for the same bounded Aave V3 deployment feed-map, then compare it against the current baseline without making any heartbeat, staleness, completeness, or financial-advice claim.

## What must be true before the pass is considered usable

- The new snapshot bundle has its own `manifest.json` with SHA-256 and byte-count checks that pass.
- The oracle source still resolves from the official Aave address-book anchor.
- Each cited asset snapshot reproduces the feed address, decimals, and latest round data from its own hashed RPC reads.
- Any observed difference is reported as a literal configuration delta only.
- If nothing changed, the result stays a baseline comparison with no change claim.

## Exact next verifier shape

- Parameterize the deployment verifier to accept a second snapshot directory alongside the current baseline bundle.
- Re-hash the new bundle before comparing anything.
- Reject any uncited deployment claim immediately.
- Keep the change-log renderer from turning an observation into a heartbeat or staleness statement.

## Current bounded asset set

- WETH only, from the existing 2026-08-14 bundle.

## Boundaries

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No claim that the map is complete.
- No claim that a second observation already exists.
