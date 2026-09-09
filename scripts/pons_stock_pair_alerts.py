#!/usr/bin/env python3
"""Alert on new pons launches paired with canonical Robinhood Stock Tokens.

The pons launch feed supplies candidate launches. Every pair token is cross-checked
against Robinhood's official Stock Token registry before alerting. This is a
read-only research monitor: it never connects a wallet, signs, trades, or
recommends a trade.
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CHAIN_ID = 4663
PONS_URL = (
    "https://www.ponsfamily.com/api/pons-launches?explore=1&sort=newest&age=all"
    "&page=1&pageSize=100&graduatedPage=1&graduatedPageSize=10&includeGraduated=0&version=all&v=22"
)
ROBINHOOD_ASSETS_URL = "https://api.robinhood.com/rhj/assets"
EXPLORER = "https://robinhoodchain.blockscout.com/address/"
TIMEOUT_SECONDS = 25
USER_AGENT = "CommanderPonsStockPairAlerts/0.1 (+personal research; no trading)"
DEFAULT_STATE = Path(__file__).resolve().parents[1] / "runtime" / "pons_stock_pairs.json"


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def canonical_stock_tokens(payload: Any) -> dict[str, dict[str, str]]:
    assets = payload.get("assets") if isinstance(payload, dict) else payload
    if not isinstance(assets, list):
        raise ValueError("Robinhood assets response is not an array")
    stocks: dict[str, dict[str, str]] = {}
    for asset in assets:
        if not isinstance(asset, dict) or asset.get("status") != "ASSET_STATUS_ACTIVE":
            continue
        deployment = next(
            (item for item in asset.get("deployments", []) if isinstance(item, dict) and item.get("chainId") == CHAIN_ID),
            None,
        )
        address = deployment.get("contractAddress") if deployment else None
        symbol = asset.get("tokenSymbol")
        name = asset.get("tokenName")
        if all(isinstance(value, str) and value for value in (address, symbol, name)):
            stocks[address.lower()] = {"address": address, "symbol": symbol, "name": name}
    return stocks


def stock_paired_launches(payload: Any, stocks: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    active = payload.get("active") if isinstance(payload, dict) else None
    items = active.get("items") if isinstance(active, dict) else None
    if not isinstance(items, list):
        raise ValueError("pons launches response has no active.items array")
    matches = []
    for launch in items:
        if not isinstance(launch, dict):
            continue
        pair_token = str(launch.get("pairToken") or "").lower()
        token = launch.get("token")
        factory = launch.get("factory")
        deployer = launch.get("deployer")
        if pair_token not in stocks or not all(isinstance(value, str) and value for value in (token, factory, deployer)):
            continue
        enriched = dict(launch)
        enriched["stock"] = stocks[pair_token]
        matches.append(enriched)
    return matches


def load_state(path: Path) -> tuple[set[str], set[str]] | None:
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    seen = payload.get("seen_launch_tokens") if isinstance(payload, dict) else None
    alerted = payload.get("alerted_launch_tokens") if isinstance(payload, dict) else None
    if not isinstance(seen, list) or not isinstance(alerted, list):
        raise ValueError("state file is malformed")
    if not all(isinstance(item, str) for item in seen + alerted):
        raise ValueError("state file is malformed")
    return set(seen), set(alerted)


def write_state(path: Path, seen: set[str], alerted: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 2,
        "chain_id": CHAIN_ID,
        "pons_source": PONS_URL,
        "official_stock_registry": ROBINHOOD_ASSETS_URL,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "seen_launch_tokens": sorted(seen)[-5000:],
        "alerted_launch_tokens": sorted(alerted)[-5000:],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def address_line(label: str, address: str) -> str:
    return f"{label}: {address}\n{EXPLORER}{address}"


def alert(launch: dict[str, Any]) -> str:
    stock = launch["stock"]
    quote = launch.get("quoteAsset") or {}
    lines = [
        "PONS — NEW CANONICAL STOCK-PAIRED LAUNCH",
        f"{launch.get('symbol', '?')} — {launch.get('name', '?')}",
        f"Paired stock: {stock['symbol']} — {stock['name']}",
        address_line("Launch token", str(launch["token"])),
        address_line("Canonical stock token", stock["address"]),
        address_line("Pons factory", str(launch["factory"])),
        address_line("Deployer", str(launch["deployer"])),
        f"Launch tx: {launch.get('transactionHash', 'unavailable')}",
        f"Launched: {launch.get('launchedAt', 'unavailable')} | block: {launch.get('blockNumber', 'unavailable')}",
        f"Quote reported by pons: {quote.get('symbol', '?')} | progress: {launch.get('graduationProgressPct', '?')}%",
        "Cross-check: pair address appears in Robinhood's official active Stock Token registry.",
        "Research signal only — not trading advice.",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--report", action="store_true", help="print monitor health even when there is no new matching launch")
    parser.add_argument(
        "--min-progress",
        type=float,
        default=5.0,
        help="minimum pons-reported graduation progress to alert (default: 5.0)",
    )
    args = parser.parse_args()
    try:
        stocks = canonical_stock_tokens(fetch_json(ROBINHOOD_ASSETS_URL))
        launches = stock_paired_launches(fetch_json(PONS_URL), stocks)
        state = load_state(args.state)
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        print(f"PONS STOCK-PAIR WATCH ERROR — {type(exc).__name__}: {str(exc)[:240]}")
        return 1

    current_tokens = {str(launch["token"]).lower() for launch in launches}
    if state is None:
        baseline_alerted = {
            str(launch["token"]).lower()
            for launch in launches
            if float(launch.get("graduationProgressPct") or 0) >= args.min_progress
        }
        write_state(args.state, current_tokens, baseline_alerted)
        if args.report:
            print(f"PONS STOCK-PAIR WATCH BASELINE — {len(launches)} matching launch(es) in the current 100-launch window; {len(stocks)} official active stock tokens validated; alert threshold {args.min_progress:g}% progress.")
        return 0

    seen, alerted = state
    qualified = [
        launch
        for launch in launches
        if float(launch.get("graduationProgressPct") or 0) >= args.min_progress
        and str(launch["token"]).lower() not in alerted
    ]
    qualified_tokens = {str(launch["token"]).lower() for launch in qualified}
    write_state(args.state, seen | current_tokens, alerted | qualified_tokens)
    if qualified:
        print("\n\n".join(alert(launch) for launch in sorted(qualified, key=lambda item: str(item.get("launchedAt", "")))))
    elif args.report:
        print(f"PONS STOCK-PAIR WATCH OK — {len(stocks)} official active stock tokens; no unalerted stock-paired launch at or above {args.min_progress:g}% progress in the current 100-launch window.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
