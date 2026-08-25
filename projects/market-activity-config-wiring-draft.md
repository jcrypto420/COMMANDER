# Market Activity config wiring draft

## Status
Draft-only support artifact for `MA-1`.

## Why this exists
`configs/market_watchlist.json` already holds the editable watchlist source, but `scripts/fetch_market_activity.py` still hard-codes its asset/protocol/repo lists. The next build step should make the fetcher read repo data first, while keeping the local-only / no-key / no-trading guardrails intact.

## Current shape
- Fetcher entrypoint: `npm run market:state` → `python3 scripts/fetch_market_activity.py`
- Output file: `dashboard/market_activity.json`
- Dashboard route: `/market`
- Config source: `configs/market_watchlist.json`

## Smallest safe implementation plan
1. Load `configs/market_watchlist.json` at startup.
2. Use config values as the source of truth for:
   - watched assets
   - watched protocols
   - watched GitHub repos
   - RSS feed list
   - thresholds / limits
3. Keep a hard-coded fallback only if the config file is missing or malformed.
4. Preserve existing public/no-login source behavior and sanitized output shape.
5. Keep all external-facing actions local-only; no posting, sending, payments, wallets, or secrets.

## Draft acceptance checks
- `npm run market:state` still writes `dashboard/market_activity.json`.
- The generated JSON reflects config-driven watchlists rather than hard-coded lists.
- The dashboard continues to render on `/market` without requiring secrets.
- Existing warnings remain informational only.

## Reopen condition
Stay parked until the CI-1 week-smooth reopen condition is met. When reopened, wire config into the fetcher, then add snapshots so the tracker shows change over time instead of latest state only.
