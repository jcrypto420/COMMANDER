# Aave V3 — Deployment Feed-Map Draft
## Draft-only packet for the next evidence increment

**Status:** draft-only

This packet does not claim a verified deployment feed map yet. It only pins the next safe evidence step for the Boring Report scorecard: turn the Aave V3 architecture baseline into a traceable deployment-specific fact file with source-cited oracle/feed addresses and freshness observations.

## Verified source anchor

Official Aave address-book source for Ethereum Aave V3:

- `https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol`

Quoted source anchors from that file:

- `IAaveOracle internal constant ORACLE = IAaveOracle(0x54586bE62E3c3580375aE3723C145253060Ca0C2);`
- `IPoolAddressesProvider internal constant POOL_ADDRESSES_PROVIDER = IPoolAddressesProvider(0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e);`
- `IPool internal constant POOL = IPool(0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2);`

Interpretation:

- The Oracle address is sourceable from an official Aave-maintained address-book file.
- That source is enough to anchor the next fact file, but not enough to claim feed-level liveness or staleness.

## What the eventual fact file must capture

1. Exact deployed oracle address, with source URL and retrieval timestamp.
2. Bounded asset set covered by the deployment-specific pass.
3. Configured feed address for each asset.
4. Decimals for each feed.
5. Latest observed round data / timestamp for each feed.
6. Raw snapshot path for every fetched response.
7. Explicit zero-claim boundary on heartbeat/staleness unless a primary source supports it.

## Draft packet shape for the eventual fact file

```json
{
  "protocol": "Aave V3",
  "network": "Ethereum mainnet",
  "oracle_address": "0x54586bE62E3c3580375aE3723C145253060Ca0C2",
  "oracle_source": "https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol",
  "retrieved_at": "TBD",
  "assets": [
    {
      "symbol": "TBD",
      "feed_address": "TBD",
      "decimals": "TBD",
      "latest_round_timestamp": "TBD",
      "snapshot_path": "TBD"
    }
  ],
  "notes": [
    "No heartbeat or staleness claim without a cited primary source.",
    "No source diversity claim without the configured feed set being enumerated."
  ]
}
```

## Immediate next step

Use this draft to build the first bounded Aave V3 deployment/feed-map fact file from official/public sources, then wire the verifier to reject any uncited deployment claim.

## Safety boundary

- No public posting.
- No payment or settlement.
- No account creation.
- No external send.
- No claim that the map is complete yet.
