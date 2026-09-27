#!/usr/bin/env python3
"""Alert only when Robinhood Chain's official stock-token registry changes.

Uses Robinhood's public, read-only /rhj/assets endpoint. It never connects a
wallet, signs, trades, makes a recommendation, or sends Telegram directly.
A scheduler may deliver this program's non-empty stdout as an alert.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ASSETS_URL = "https://api.robinhood.com/rhj/assets"
CHAIN_ID = 4663
TIMEOUT_SECONDS = 20
USER_AGENT = "CommanderRobinhoodChainAlerts/0.1 (+personal research; no trading)"
DEFAULT_STATE = Path(__file__).resolve().parents[1] / "runtime" / "rh_chain_stock_assets.json"


def fetch_assets() -> list[dict[str, Any]]:
    request = urllib.request.Request(
        ASSETS_URL,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        payload = json.loads(response.read().decode("utf-8"))
    assets = payload.get("assets") if isinstance(payload, dict) else payload
    if not isinstance(assets, list):
        raise ValueError("official assets response is not an array")
    return [asset for asset in assets if isinstance(asset, dict)]


def canonical_assets(assets: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for asset in assets:
        if asset.get("status") != "ASSET_STATUS_ACTIVE":
            continue
        deployment = next(
            (
                item
                for item in asset.get("deployments", [])
                if isinstance(item, dict) and item.get("chainId") == CHAIN_ID
            ),
            None,
        )
        address = deployment.get("contractAddress") if deployment else None
        symbol = asset.get("tokenSymbol")
        name = asset.get("tokenName")
        asset_id = asset.get("id")
        if not all(isinstance(value, str) and value for value in (address, symbol, name, asset_id)):
            continue
        result[address.lower()] = {"id": asset_id, "symbol": symbol, "name": name, "address": address}
    return result


def load_state(path: Path) -> dict[str, dict[str, str]] | None:
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    assets = payload.get("assets") if isinstance(payload, dict) else None
    if not isinstance(assets, dict):
        raise ValueError("state file is malformed")
    return assets


def write_state(path: Path, assets: dict[str, dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "source": ASSETS_URL,
        "chain_id": CHAIN_ID,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "assets": assets,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def message(new_assets: list[dict[str, str]]) -> str:
    lines = [f"RH CHAIN — {len(new_assets)} NEW ACTIVE STOCK TOKEN{'S' if len(new_assets) != 1 else ''}"]
    for asset in new_assets:
        lines.append(f"• {asset['symbol']} — {asset['name']}\n  {asset['address']}")
    lines += [f"Source: {ASSETS_URL}", "Registry event only — not trading advice."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--report", action="store_true", help="print a current read-only health summary")
    args = parser.parse_args()

    try:
        current = canonical_assets(fetch_assets())
        previous = load_state(args.state)
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        print(f"RH CHAIN WATCH ERROR — {type(exc).__name__}: {str(exc)[:240]}")
        return 1

    write_state(args.state, current)
    if previous is None:
        if args.report:
            print(f"RH CHAIN WATCH BASELINE — {len(current)} active stock tokens on chain {CHAIN_ID}. Future additions alert here.")
        return 0

    additions = [asset for key, asset in current.items() if key not in previous]
    if additions:
        print(message(sorted(additions, key=lambda asset: (asset["symbol"], asset["address"]))))
    elif args.report:
        print(f"RH CHAIN WATCH OK — {len(current)} active stock tokens; no additions since the last run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
