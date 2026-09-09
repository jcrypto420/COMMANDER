#!/usr/bin/env python3
"""Fetch a small, public, no-key market activity snapshot.

Personal-use/open-source friendly: uses free public endpoints only, writes a
sanitized JSON file for the local Mission Control dashboard. No trading, no
advice, no secrets.
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

UA = "CommanderMarketActivity/0.1 (+local personal dashboard; no trading)"
TIMEOUT = 18


def fetch_json(url: str) -> tuple[object | None, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        return None, str(exc)[:220]


def coingecko_prices() -> tuple[list[dict], list[str]]:
    ids = "bitcoin,ethereum,chainlink,aave,uniswap,maker,ondo-finance"
    url = (
        "https://api.coingecko.com/api/v3/simple/price?"
        + urllib.parse.urlencode(
            {
                "ids": ids,
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
    labels = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "chainlink": "LINK",
        "aave": "AAVE",
        "uniswap": "UNI",
        "maker": "MKR",
        "ondo-finance": "ONDO",
    }
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


def coingecko_trending() -> tuple[list[dict], list[str]]:
    data, err = fetch_json("https://api.coingecko.com/api/v3/search/trending")
    if err or not isinstance(data, dict):
        return [], [f"CoinGecko trending unavailable: {err}"]
    coins = []
    for item in (data.get("coins") or [])[:7]:
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


def defillama_protocols() -> tuple[list[dict], list[str]]:
    data, err = fetch_json("https://api.llama.fi/protocols")
    if err or not isinstance(data, list):
        return [], [f"DefiLlama protocols unavailable: {err}"]
    watch = {"chainlink", "aave", "uniswap", "makerdao", "lido", "pendle", "ondo finance", "ethena"}
    rows = []
    for proto in data:
        name = str(proto.get("name", ""))
        if name.lower() in watch:
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


def github_watch() -> tuple[list[dict], list[str]]:
    targets = [
        ("smartcontractkit", "chainlink"),
        ("aave", "aave-v3-core"),
        ("Uniswap", "v4-core"),
        ("DefiLlama", "dimension-adapters"),
        ("ethereum", "go-ethereum"),
    ]
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
    warnings: list[str] = []
    assets, w = coingecko_prices(); warnings += w
    trending, w = coingecko_trending(); warnings += w
    protocols, w = defillama_protocols(); warnings += w
    repos, w = github_watch(); warnings += w

    focus_assets = [a for a in assets if a.get("symbol") in {"LINK", "ETH", "BTC"}]
    signals = [format_signal(a) for a in focus_assets]
    if protocols:
        top = protocols[0]
        signals.append(f"Largest watched DeFi protocol by TVL: {top['name']} at ${top.get('tvl_usd', 0):,.0f}.")
    if repos:
        recent = sorted(repos, key=lambda r: r.get("pushed_at") or "", reverse=True)[0]
        signals.append(f"Most recently pushed watched repo: {recent['repo']} at {recent.get('pushed_at')}.")

    state = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "Personal research dashboard only. Not financial advice, trading advice, or a signal to buy/sell.",
        "sources": ["CoinGecko public API", "DefiLlama public API", "GitHub public API"],
        "watchlist": {
            "assets": assets,
            "defi_protocols": protocols,
            "github_repos": repos,
            "trending": trending,
        },
        "signals": signals[:8],
        "warnings": warnings[:12],
        "next_build_step": "Add saved watchlist config + historical snapshots so this becomes an actually useful open-source tracker, not just a pretty fetch page.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, warnings={len(warnings)})")


if __name__ == "__main__":
    main()
