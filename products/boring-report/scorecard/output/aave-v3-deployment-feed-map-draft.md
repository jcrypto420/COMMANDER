# Aave V3 — Deployment Feed-Map Draft
## Draft-only packet for the next evidence increment

**Status:** draft-only

This packet now has a concrete bounded fact file: `facts/aave-v3-deployment-feed-map.json`

## Verified source anchor

Official Aave address-book source for Ethereum Aave V3:

- `https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol`

Quoted source anchors from that file:

- `IAaveOracle internal constant ORACLE = IAaveOracle(0x54586bE62E3c3580375aE3723C145253060Ca0C2);`
- `IPoolAddressesProvider internal constant POOL_ADDRESSES_PROVIDER = IPoolAddressesProvider(0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e);`
- `IPool internal constant POOL = IPool(0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2);`

## Bounded fact-file result

- Scope: Ethereum mainnet, preferred asset subset only.
- Raw snapshots: `products/boring-report/scorecard/snapshots/2026-08-14/manifest.json`

| Symbol | Asset | Feed | Decimals | Latest observed updatedAt | Snapshot |
|---|---|---|---:|---:|---|
| WETH | 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 | 0x5424384b256154046e9667ddfaaa5e550145215e | 8 | 1786748675 | products/boring-report/scorecard/snapshots/2026-08-14/rpc-feed-latestRoundData-weth-00.json |

## Draft interpretation

- The deployment-specific map is now concrete for a bounded asset subset: the oracle source is resolved from the Aave address-book anchor, then each selected asset is mapped to its configured feed and latest observed round timestamp.
- This is still not a heartbeat or staleness claim. `facts/aave-v3-deployment-feed-map.json` keeps those fields zero-claim unless a primary source supports them.
- Next step: extend the verifier to hash the new snapshot bundle and reject any uncited deployment claim.

## Safety boundary

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No claim that the map is complete yet.
