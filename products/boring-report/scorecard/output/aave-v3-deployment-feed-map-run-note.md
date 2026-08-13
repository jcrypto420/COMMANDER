# Aave V3 — Deployment Feed-Map Run Note

## Status

Draft-only. This is a local run note for the next evidence increment; it is not a claim that the deployment feed map is complete.

## Purpose

Turn the official Aave address-book anchor into one bounded fact file with source-cited feed addresses, decimals, and latest observed round timestamps.

## Inputs already anchored

- Official source: `https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol`
- Oracle address: `0x54586bE62E3c3580375aE3723C145253060Ca0C2`
- Pool address provider: `0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e`

## Next local-only steps

1. Use the oracle address as the scope boundary for the fact file.
2. Enumerate the asset/feed pairs that the deployment actually exposes.
3. Capture the feed address, decimals, and latest round metadata for each asset.
4. Save a raw snapshot path for every fetched response.
5. Reject any heartbeat or staleness claim unless a primary source supports it.
6. Stop if a field would be uncited or if the deployment scope is still ambiguous.

## Output shape target

The resulting fact file should be small, bounded, and citation-first:

- protocol
- network
- oracle address + source URL
- retrieved_at timestamp
- asset rows with feed address, decimals, latest round timestamp, snapshot path
- notes that explicitly keep heartbeat/staleness at zero unless supported

## Guardrails

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No completeness claim until the fact file is actually built and verified.