# Aave V3 — Next Asset Shortlist Draft
## Draft-only support note

**Status:** draft-only

This note keeps the next bounded Aave V3 expansion concrete while the current comparison remains WETH-only and zero-claim. It does **not** authorize a new snapshot run yet.

## Verified source anchors

- Official Aave V3 Ethereum source: `https://raw.githubusercontent.com/aave/aave-address-book/main/src/AaveV3Ethereum.sol`
- The official source includes both `WBTC_UNDERLYING` and `USDC_UNDERLYING` constants.
- The repo already has public Chainlink snapshot coverage for both candidate families:
  - WBTC: Proof of Reserves plus WBTC/BTC reference feed evidence in `products/boring-report/scorecard/snapshots/2026-07-27/chainlink-feeds-mainnet.json`
  - USDC: USDC/USD and USDC/ETH reference feed evidence in the same snapshot bundle

## Draft ranking

1. **WBTC first**
   - Clear second-asset contrast after WETH.
   - Existing public feed/PoR evidence makes the draft easier to keep bounded and reproducible.
   - Adds a different risk shape than the current ETH-only map without widening the scope too much.

2. **USDC second**
   - Very visible and well-supported public feed coverage.
   - Good fallback if the next pass needs a more stablecoin-adjacent comparison set.
   - Keep it as the next option, not the first expansion, so the map does not turn into a generic feed dump.

## Draft-only next step

When a fresh verified snapshot lands, add **one** new bounded asset only, starting with WBTC, then compare it against the current WETH baseline with the existing verifier shape.

## Re-entry checklist

When the fresh bundle exists, keep the pass narrow:

1. Re-hash the new bundle first.
2. Add exactly one new bounded asset: WBTC.
3. Compare WBTC against the current WETH baseline with the existing verifier shape.
4. Keep publication, payment, account creation, and any wider asset sweep gated.

## Boundaries

- No heartbeat claim.
- No staleness claim.
- No completeness claim.
- No publication.
- No payment.
- No account creation.
- No external send.
- No new snapshot until the fresh verified bundle exists.

## Draft re-entry note (2026-08-23)

- Keep **WBTC first** as the next bounded asset and do not widen the scope beyond one new asset.
- Wait for a fresh verified bundle; then compare it against the current WETH baseline with the existing verifier shape.
- Keep publication, payment, account creation, and any new snapshot run gated until that bundle exists.
