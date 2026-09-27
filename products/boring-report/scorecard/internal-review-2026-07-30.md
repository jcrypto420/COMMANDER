# Oracle Scorecard v0 — Internal Review
## 2026-07-30 · evidence-baseline acceptance note

## Verification result

`python3 verify_scorecard.py` passed locally on 2026-07-30:

> OK oracle scorecard: 2 protocol fact files; 3 hashed source snapshots; generated outputs exact

The verifier confirms that the committed facts, quoted source evidence, snapshot hashes, and rendered Markdown/JSON/HTML outputs agree exactly.

## What is safe to say

- This is a **source-backed architecture-evidence baseline**, not a safety rating or financial advice.
- Aave V3 receives **40/100** only for documented adapter-level fallback and partial source-concentration evidence.
- Morpho Blue receives **0/100** because its generic oracle interface establishes no fallback, freshness, source-diversity, or incident evidence.
- Zero points for liveness or incidents mean **evidence is absent from this pack**; they do not assert an outage or incident occurred.

## Review decision

**Accept v0 internally as the fail-closed evidence baseline. Do not broaden claims or publish it.**

The scorecard is useful now as a reproducible research scaffold. It is not ready to compare live deployed protocol risk, because the evidence pack does not yet establish deployment configuration, observed update timing, or incident history.

## Next evidence increment — Aave V3 deployment map

Build one traceable Aave V3 mainnet feed-map fact file before adding protocols or changing scores:

1. Record the exact deployed oracle address and source of that address.
2. Map a bounded asset set to configured price-feed addresses, with snapshot paths and retrieval timestamps.
3. For every Chainlink feed, record the feed address, decimals, and the latest observed round timestamp; preserve raw responses/snapshots.
4. Keep any heartbeat/staleness conclusion at zero unless a primary source explicitly supplies the threshold or observed history supports it.
5. Extend `verify_scorecard.py` so it re-hashes the new snapshots and rejects unmapped or uncited deployment claims.

Only after that map is verified should the liveness and concentration dimensions be reconsidered. A sourced incident ledger remains a separate required layer.
