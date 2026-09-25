#!/usr/bin/env python3
"""Fetch a small, public, no-key market activity snapshot.

Personal-use/open-source friendly: uses free public endpoints only, writes a
sanitized JSON file for the local Mission Control dashboard. No trading, no
advice, no secrets.

Config-driven build step (MA-1): the watchlist now comes from
configs/market_watchlist.json. Hard-coded fallbacks are preserved only when the
config file is missing or malformed.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dashboard" / "market_activity.json"
CONFIG = ROOT / "configs" / "market_watchlist.json"

UA = "CommanderMarketActivity/0.1 (+local personal dashboard; no trading)"
TIMEOUT = 18

FALLBACK_ASSETS = [
    {"symbol": "BTC", "coingecko_id": "bitcoin"},
    {"symbol": "ETH", "coingecko_id": "ethereum"},
    {"symbol": "LINK", "coingecko_id": "chainlink"},
    {"symbol": "AAVE", "coingecko_id": "aave"},
    {"symbol": "UNI", "coingecko_id": "uniswap"},
    {"symbol": "MKR", "coingecko_id": "maker"},
    {"symbol": "ONDO", "coingecko_id": "ondo-finance"},
]
FALLBACK_PROTOCOLS = [
    "Chainlink", "Aave", "Uniswap", "MakerDAO", "Lido", "Pendle",
    "Ondo Finance", "Ethena",
]
FALLBACK_GITHUB_REPOS = [
    "smartcontractkit/chainlink",
    "aave/aave-v3-core",
    "Uniswap/v4-core",
    "DefiLlama/dimension-adapters",
    "ethereum/go-ethereum",
]
FALLBACK_THRESHOLDS = {
    "asset_24h_move_pct": 5,
    "protocol_7d_tvl_move_pct": 10,
    "repo_pushed_within_days": 7,
    "trending_top_n": 7,
}


def load_config() -> dict:
    """Read configs/market_watchlist.json when it is present and valid."""
    if not CONFIG.exists():
        return {}
    try:
        raw = json.loads(CONFIG.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(raw, dict):
        return {}
    return raw


def config_text_repr() -> str:
    """Human-friendly note about where the watchlist came from for this run."""
    if not CONFIG.exists():
        return "watchlist source: hard-coded fallback (config file absent)"
    try:
        payload = json.loads(CONFIG.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return "watchlist source: hard-coded fallback (config unreadable)"
    if not isinstance(payload, dict) or not payload:
        return "watchlist source: hard-coded fallback (config empty/invalid)"
    try:
        assets = payload.get("assets") or []
        protocols = payload.get("protocols") or []
        repos = payload.get("github_repos") or []
        return (
            f"watchlist source: configs/market_watchlist.json "
            f"({len(assets)} assets, {len(protocols)} protocols, {len(repos)} repos)"
        )
    except Exception:
        return "watchlist source: hard-coded fallback (config parse error)"


def validate_config(payload: dict) -> tuple[bool, str]:
    """Return (usable, reason)."""

    def is_list_of_strings(value) -> bool:
        return isinstance(value, list) and all(isinstance(item, str) for item in value)

    def is_list_of_asset_rows(value) -> bool:
        if not isinstance(value, list):
            return False
        for row in value:
            if not isinstance(row, dict):
                return False
            if not isinstance(row.get("symbol"), str) or not isinstance(
                row.get("coingecko_id"), str
            ):
                return False
        return True

    assets = payload.get("assets")
    protocols = payload.get("protocols")
    repos = payload.get("github_repos")

    if assets is not None and not is_list_of_asset_rows(assets):
        return False, "config.assets is not a list of {symbol, coingecko_id}"
    if protocols is not None and not is_list_of_strings(protocols):
        return False, "config.protocols is not a list of strings"
    if repos is not None and not is_list_of_strings(repos):
        return False, "config.github_repos is not a list of owner/repo strings"
    return True, ""


def build_config_derived(payload: dict) -> dict:
    """Derive fetcher structures from the validated config file."""

    def is_list_of_asset_rows(value) -> bool:
        return isinstance(value, list) and all(
            isinstance(row, dict) and isinstance(row.get("symbol"), str)
            and isinstance(row.get("coingecko_id"), str)
            for row in value
        )

    def is_list_of_strings(value) -> bool:
        return isinstance(value, list) and all(isinstance(item, str) for item in value)

    assets = payload.get("assets", [])
    protocols = payload.get("protocols", [])
    repos = payload.get("github_repos", [])
    thresholds = payload.get("thresholds", {}) or {}

    use_assets = is_list_of_asset_rows(assets)
    use_protocols = is_list_of_strings(protocols)
    use_repos = is_list_of_strings(repos)

    coin_ids = (
        ",".join(row["coingecko_id"] for row in assets)
        if use_assets and assets
        else ""
    )
    labels = (
        {row["coingecko_id"]: row["symbol"] for row in assets}
        if use_assets
        else {}
    )
    protocol_watch = {name.lower() for name in protocols} if use_protocols else set()
    github_targets = [
        tuple(repo.split("/", 1)) for repo in repos
    ] if use_repos and repos else []

    trending_top_n = int(thresholds.get("trending_top_n", 7) or 7)
    repo_pushed_within_days = int(
        thresholds.get("repo_pushed_within_days", 7) or 7
    )

    return {
        "coin_ids": coin_ids,
        "labels": labels,
        "protocol_watch": protocol_watch,
        "github_targets": github_targets,
        "trending_top_n": trending_top_n,
        "repo_pushed_within_days": repo_pushed_within_days,
        "use_assets": use_assets,
        "use_protocols": use_protocols,
        "use_repos": use_repos,
    }


def coingecko_prices(
    coin_ids: str, labels: dict[str, str]
) -> tuple[list[dict], list[str]]:
    if not coin_ids:
        return [], ["CoinGecko prices skipped: no asset coin IDs configured"]
    url = (
        "https://api.coingecko.com/api/v3/simple/price?"
        + urllib.parse.urlencode(
            {
                "ids": coin_ids,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_market_cap": "true",
                "precision": "full",
            }
        )
    )
    data, err = fetch_json(url)
    if err or not isinstance(data, dict):
        return [], [f"CoinGecko prices unavailable: {err}"]
    assets = []
    for key, label in labels.items():
        row = data.get(key) or {}
        if not row:
            continue
        assets.append(
            {
                "id": key,
                "symbol": label,
                "price_usd": row.get("usd"),
                "change_24h_pct": row.get("usd_24h_change"),
                "market_cap_usd": row.get("usd_market_cap"),
            }
        )
    return assets, []


def coingecko_trending(trending_top_n: int) -> tuple[list[dict], list[str]]:
    data, err = fetch_json("https://api.coingecko.com/api/v3/search/trending")
    if err or not isinstance(data, dict):
        return [], [f"CoinGecko trending unavailable: {err}"]
    limit = max(trending_top_n, 0)
    coins = []
    for item in (data.get("coins") or [])[:limit]:
        coin = item.get("item") or {}
        coins.append(
            {
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "market_cap_rank": coin.get("market_cap_rank"),
                "score": coin.get("score"),
            }
        )
    return coins, []


def defillama_protocols(protocol_watch: set[str]) -> tuple[list[dict], list[str]]:
    if not protocol_watch:
        return [], ["DefiLlama protocols skipped: no protocols configured"]
    data, err = fetch_json("https://api.llama.fi/protocols")
    if err or not isinstance(data, list):
        return [], [f"DefiLlama protocols unavailable: {err}"]
    rows = []
    for proto in data:
        name = str(proto.get("name", ""))
        if name.lower() in protocol_watch:
            rows.append(
                {
                    "name": name,
                    "category": proto.get("category"),
                    "chains": proto.get("chains", [])[:8],
                    "tvl_usd": proto.get("tvl"),
                    "change_1d_pct": proto.get("change_1d"),
                    "change_7d_pct": proto.get("change_7d"),
                    "url": proto.get("url"),
                }
            )
    rows.sort(key=lambda x: x.get("tvl_usd") or 0, reverse=True)
    return rows, []


def github_repo(owner: str, repo: str) -> tuple[dict | None, str | None]:
    data, err = fetch_json(f"https://api.github.com/repos/{owner}/{repo}")
    if err or not isinstance(data, dict):
        return None, err
    return {
        "repo": f"{owner}/{repo}",
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "open_issues": data.get("open_issues_count"),
        "pushed_at": data.get("pushed_at"),
        "description": data.get("description"),
        "url": data.get("html_url"),
    }, None


def github_watch(
    targets: list[tuple[str, str]], repo_pushed_within_days: int
) -> tuple[list[dict], list[str]]:
    repos = []
    warnings = []
    for owner, repo in targets:
        item, err = github_repo(owner, repo)
        if item:
            repos.append(item)
        else:
            warnings.append(f"GitHub {owner}/{repo} unavailable: {err}")
        time.sleep(0.25)
    return repos, warnings


def format_signal(asset: dict) -> str:
    change = asset.get("change_24h_pct")
    if change is None:
        return f"{asset.get('symbol')} price loaded."
    direction = "up" if change >= 0 else "down"
    return f"{asset.get('symbol')} {direction} {abs(change):.1f}% over 24h."


def main() -> None:
    config_payload = load_config()
    usable, reason = validate_config(config_payload)
    if usable and config_payload:
        derived = build_config_derived(config_payload)
        source_note = config_text_repr()
    else:
        derived = {
            "coin_ids": ",".join(row["coingecko_id"] for row in FALLBACK_ASSETS),
            "labels": {row["coingecko_id"]: row["symbol"] for row in FALLBACK_ASSETS},
            "protocol_watch": {name.lower() for name in FALLBACK_PROTOCOLS},
            "github_targets": [
                tuple(repo.split("/", 1)) for repo in FALLBACK_GITHUB_REPOS
            ],
            "trending_top_n": FALLBACK_THRESHOLDS["trending_top_n"],
            "repo_pushed_within_days": FALLBACK_THRESHOLDS["repo_pushed_within_days"],
            "use_assets": True,
            "use_protocols": True,
            "use_repos": True,
        }
        source_note = f"watchlist source: hard-coded fallback ({reason})"

    warnings: list[str] = []
    assets, w = coingecko_prices(
        derived["coin_ids"], derived["labels"]
    )
    warnings += w
    trending, w = coingecko_trending(derived["trending_top_n"])
    warnings += w
    protocols, w = defillama_protocols(derived["protocol_watch"])
    warnings += w
    repos, w = github_watch(
        derived["github_targets"], derived["repo_pushed_within_days"]
    )
    warnings += w

    focus_assets = [a for a in assets if a.get("symbol") in {"LINK", "ETH", "BTC"}]
    signals = [format_signal(a) for a in focus_assets]
    if protocols:
        top = protocols[0]
        signals.append(
            f"Largest watched DeFi protocol by TVL: {top['name']} at ${top.get('tvl_usd', 0):,.0f}."
        )
    if repos:
        recent = sorted(
            repos, key=lambda r: r.get("pushed_at") or "", reverse=True
        )[0]
        signals.append(
            f"Most recently pushed watched repo: {recent['repo']} at {recent.get('pushed_at')}."
        )

    state = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "Personal research dashboard only. Not financial advice, trading advice, or a signal to buy/sell.",
        "sources": ["CoinGecko public API", "DefiLlama public API", "GitHub public API"],
        "watchlist_source": source_note,
        "watchlist": {
            "assets": assets,
            "defi_protocols": protocols,
            "github_repos": repos,
            "trending": trending,
        },
        "signals": signals[:8],
        "warnings": warnings[:12],
        "next_build_step": (
            "RSS feeds and any new thresholds are still deferred in this pass. "
            "When the CI-1 week-smooth reopen condition clears, keep configs/market_watchlist.json "
            "as the source of truth, then add daily snapshots so the tracker shows change over time "
            "instead of latest state only."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, warnings={len(warnings)})")


def fetch_json(url: str) -> tuple[object | None, str | None]:
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        json.JSONDecodeError,
    ) as exc:
        return None, str(exc)[:220]


if __name__ == "__main__":
    main()
