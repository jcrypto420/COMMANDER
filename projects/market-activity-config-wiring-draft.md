# Market Activity config wiring draft

## Status

Draft-only support artifact for `MA-1`. 2026-09-23 draft update: refreshed to match the live config and fetcher shape and public-source preflight.

## Why this exists

`configs/market_watchlist.json` holds the editable watchlist source, but `scripts/fetch_market_activity.py` still hard-codes its asset/protocol/repo lists. Next build step: make the fetcher read repo data first, keeping local-only / no-key / no-trading guardrails intact.

## Public-source preflight, 2026-09-23

- **CoinGecko keyless pool:** dynamic ~10–30 calls/min, can 429 under load; free for personal/local use; the fetcher currently makes 2 calls (simple/price + search/trending) with no API key.
- **DefiLlama:** `api.llama.fi/protocols` remains free/public; the fetcher currently makes 1 call.
- **GitHub:** public API with User-Agent header + per-request `sleep(0.25)`; the fetcher currently makes 5 calls.
- **Explicit no-key public-source baseline note:** this preflight confirms the existing fetcher sources are suitable for a local config-wiring pass; no API keys, accounts, or spend are introduced by the config-wiring step.

## Repo fact check

- **Fetcher hard-codes:**
  - CoinGecko IDs string: `'bitcoin,ethereum,chainlink,aave,uniswap,maker,ondo-finance'`
  - Labels dict: bitcoin→BTC, ethereum→ETH, chainlink→LINK, aave→AAVE, uniswap→UNI, maker→MKR, ondo-finance→ONDO
  - DefiLlama watch set: `{'chainlink','aave','uniswap','makerdao','lido','pendle','ondo finance','ethena'}`
  - GitHub targets list of 5 tuples: (smartcontractkit/chainlink, aave/aave-v3-core, Uniswap/v4-core, DefiLlama/dimension-adapters, ethereum/go-ethereum)
  - Trending limit hard-coded to 7
- **Config file already carries:**
  - `assets` array (7 entries, each with `symbol` + `coingecko_id`)
  - `protocols` array (8 entries)
  - `github_repos` array (5 entries in `owner/repo` format)
  - `rss_feeds` array (4 entries with `name` + `url`)
  - `thresholds` object (`asset_24h_move_pct`:5, `protocol_7d_tvl_move_pct`:10, `repo_pushed_within_days`:7, `trending_top_n`:7)
  - `next_build_step` note
- **The config-wiring step maps:**
  - `config.assets` → CoinGecko IDs string + labels dict
  - `config.protocols` → DefiLlama watch set (lowercase normalize)
  - `config.github_repos` → GitHub targets list (split on `/`)
  - `config.thresholds.trending_top_n` → trending limit (fallback 7)
  - `config.thresholds.repo_pushed_within_days` → repo freshness window (fallback 7)
  - `rss_feeds` and any new threshold fields are explicitly deferred in this pass

## Current shape

- Fetcher entrypoint: `npm run market:state` → `python3 scripts/fetch_market_activity.py`
- Output file: `dashboard/market_activity.json`
- Dashboard route: `/market`
- Config source: `configs/market_watchlist.json`

## Next safe build step, concrete

1. Read and parse `configs/market_watchlist.json` at startup.
2. Validate schema: `assets` must be an array of `{symbol, coingecko_id}`; `protocols` must be an array of strings; `github_repos` must be an array of `owner/repo` strings; `rss_feeds` and `thresholds` are optional.
3. Build the CoinGecko IDs comma-string from `config.assets[*].coingecko_id`.
4. Build the labels dict from `config.assets[*]` mapping `coingecko_id` → `symbol`.
5. Build the DefiLlama watch set from `config.protocols`, lowercased.
6. Build the GitHub targets list from `config.github_repos` by splitting each entry on `/` into `(owner, repo)`.
7. Read `trending_top_n` from `config.thresholds.trending_top_n`, fallback 7.
8. Read `repo_pushed_within_days` from `config.thresholds.repo_pushed_within_days`, fallback 7.
9. Keep a hard-coded fallback only if the config file is missing or malformed (use the current hard-coded values as the fallback).
10. Preserve the existing public/no-login source behavior and sanitized output shape (`dashboard/market_activity.json`).
11. Keep all external-facing actions local-only; no posting, sending, payments, wallets, or secrets.
12. Defer RSS feed wiring and any new thresholds to a follow-up draft note; document the deferral explicitly, do not silently drop `rss_feeds` from the config.

## Draft acceptance checks

- `python3 scripts/fetch_market_activity.py` still writes `dashboard/market_activity.json`.
- The generated watchlist assets, protocols, and repos reflect the config file as the source of truth.
- The `/market` dashboard route continues to render without requiring secrets.
- Config-driven vs hard-coded parity is explicit for: assets (IDs + labels), protocols (watch set), GitHub repos (targets list), trending limit, and repo freshness window.
- RSS feeds remain explicitly deferred in this pass (documented, not silently dropped).
- Warnings remain informational only.

## Reopen condition

Stay parked until the CI-1 week-smooth reopen condition is met. When reopened, wire config into the fetcher, then add snapshots so the tracker shows change over time instead of latest state only.
