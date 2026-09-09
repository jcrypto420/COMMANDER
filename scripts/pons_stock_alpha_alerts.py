#!/usr/bin/env python3
"""Score Pons v2 stock-paired launches using public, read-only sources.

This is a research monitor, not a trading agent. It never connects a wallet,
signs, trades, recommends a purchase, or labels a wallet profitable without a
verified realized-PnL history source.
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "pons_stock_alpha.json"
DEFAULT_STATE = ROOT / "runtime" / "pons_stock_alpha_state.json"
CHAIN_ID = 4663
EXPLORER = "https://robinhoodchain.blockscout.com/address/"
TIMEOUT_SECONDS = 25
USER_AGENT = "CommanderPonsStockAlpha/0.1 (+personal research; no trading)"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def load_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("alpha config is not an object")
    for key in ("sources", "required_gates", "scoring"):
        if not isinstance(config.get(key), dict):
            raise ValueError(f"alpha config missing {key}")
    return config


def canonical_stock_tokens(payload: Any) -> dict[str, dict[str, str]]:
    assets = payload.get("assets") if isinstance(payload, dict) else payload
    if not isinstance(assets, list):
        raise ValueError("Robinhood assets response is not an array")
    stocks: dict[str, dict[str, str]] = {}
    for asset in assets:
        if not isinstance(asset, dict) or asset.get("status") != "ASSET_STATUS_ACTIVE":
            continue
        deployment = next(
            (entry for entry in asset.get("deployments", []) if isinstance(entry, dict) and entry.get("chainId") == CHAIN_ID),
            None,
        )
        address = deployment.get("contractAddress") if deployment else None
        if isinstance(address, str) and isinstance(asset.get("tokenSymbol"), str) and isinstance(asset.get("tokenName"), str):
            stocks[address.lower()] = {"address": address, "symbol": asset["tokenSymbol"], "name": asset["tokenName"]}
    return stocks


def stock_paired_launches(payload: Any, stocks: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    active = payload.get("active") if isinstance(payload, dict) else None
    items = active.get("items") if isinstance(active, dict) else None
    if not isinstance(items, list):
        raise ValueError("pons launch response missing active.items")
    matches = []
    for launch in items:
        if not isinstance(launch, dict):
            continue
        pair = str(launch.get("pairToken") or "").lower()
        token = launch.get("token")
        factory = launch.get("factory")
        curve_or_pool = launch.get("pool")
        deployer = launch.get("deployer")
        if pair not in stocks or not all(isinstance(item, str) and item for item in (token, factory, curve_or_pool, deployer)):
            continue
        entry = dict(launch)
        entry["stock"] = stocks[pair]
        matches.append(entry)
    return matches


def recent_trade_metrics(token: str, observed_at: datetime, lookback_seconds: float) -> dict[str, Any]:
    """Summarize Pons' indexed public trade feed; never infer wallet PnL."""
    payload = fetch_json(f"https://www.ponsfamily.com/api/pons-v2-market/{token}/trades")
    trades = payload.get("trades") if isinstance(payload, dict) else None
    if not isinstance(trades, list):
        raise ValueError("Pons v2 market trade response is malformed")
    cutoff = observed_at.timestamp() - lookback_seconds
    recent = [trade for trade in trades if isinstance(trade, dict) and float(trade.get("timestamp") or 0) >= cutoff]
    buys = [trade for trade in recent if trade.get("side") == "buy" and isinstance(trade.get("account"), str)]
    sells = [trade for trade in recent if trade.get("side") == "sell"]
    buy_by_wallet: dict[str, int] = {}
    buy_quote = 0
    sell_quote = 0
    for trade in buys:
        wallet = str(trade["account"]).lower()
        amount = int(str(trade.get("quoteAmount") or "0"))
        buy_by_wallet[wallet] = buy_by_wallet.get(wallet, 0) + amount
        buy_quote += amount
    for trade in sells:
        sell_quote += int(str(trade.get("quoteAmount") or "0"))
    gross_quote = buy_quote + sell_quote
    return {
        "recent_trades": len(recent),
        "buy_count": len(buys),
        "sell_count": len(sells),
        "unique_buyers": len(buy_by_wallet),
        "net_buy_ratio": ((buy_quote - sell_quote) / gross_quote) if gross_quote else 0.0,
        "top_buyer_share": (max(buy_by_wallet.values()) / buy_quote) if buy_quote else 1.0,
        "top_buyers": [wallet for wallet, _ in sorted(buy_by_wallet.items(), key=lambda item: item[1], reverse=True)[:3]],
    }


def compact_snapshot(launch: dict[str, Any], observed_at: datetime) -> dict[str, Any]:
    return {
        "observed_at": observed_at.isoformat(),
        "progress": float(launch.get("graduationProgressPct") or 0),
        "market_cap_usd": float(launch.get("marketCapUsd") or 0),
        "latest_buy_at": launch.get("latestBuyAt"),
        "launched_at": launch.get("launchedAt"),
    }


def load_state(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    state = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(state, dict) or not isinstance(state.get("snapshots"), dict) or not isinstance(state.get("alert_scores"), dict):
        raise ValueError("alpha state is malformed")
    return state


def write_state(path: Path, snapshots: dict[str, dict[str, Any]], scores: dict[str, int], observed_at: datetime) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "schema_version": 1,
        "chain_id": CHAIN_ID,
        "updated_at": observed_at.isoformat(),
        "snapshots": snapshots,
        "alert_scores": scores,
    }, indent=2) + "\n", encoding="utf-8")


def score_launch(launch: dict[str, Any], previous: dict[str, Any] | None, trade_metrics: dict[str, Any], config: dict[str, Any], observed_at: datetime) -> tuple[int, float, bool, list[str]]:
    gates = config["required_gates"]
    points = config["scoring"]
    progress = float(launch.get("graduationProgressPct") or 0)
    delta = progress - float(previous.get("progress") or 0) if previous else 0.0
    launched_at = parse_time(launch.get("launchedAt"))
    latest_buy_at = parse_time(launch.get("latestBuyAt"))
    age = (observed_at - launched_at).total_seconds() if launched_at else -1
    buy_age = (observed_at - latest_buy_at).total_seconds() if latest_buy_at else float("inf")
    market_cap = float(launch.get("marketCapUsd") or 0)
    reasons: list[str] = []
    # Eligibility keeps junk out; the score ranks eligible launches instead of
    # awarding the same binary maximum to every threshold-crossing launch.
    score = int(points["official_stock_pair"])
    if age >= float(gates["minimum_age_seconds"]):
        reasons.append("snipe window elapsed")
    progress_points = int(min(progress / float(points["progress_scale_pct"]), 1.0) * float(points["progress_max"]))
    acceleration_points = int(min(max(delta, 0.0) / float(points["progress_acceleration_scale_pct"]), 1.0) * float(points["progress_acceleration_max"]))
    recency_points = int(max(0.0, 1.0 - (buy_age / float(gates["maximum_latest_buy_age_seconds"]))) * float(points["recent_buy_activity_max"]))
    market_cap_points = int(min(market_cap / float(points["market_cap_scale_usd"]), 1.0) * float(points["market_cap_max"]))
    buyer_points = int(min(float(trade_metrics["unique_buyers"]) / float(points["buyer_diversity_scale"]), 1.0) * float(points["buyer_diversity_max"]))
    flow_points = int(min(max(float(trade_metrics["net_buy_ratio"]), 0.0) / float(points["net_buy_flow_scale"]), 1.0) * float(points["net_buy_flow_max"]))
    score += progress_points + acceleration_points + recency_points + market_cap_points + buyer_points + flow_points
    if progress >= float(gates["minimum_progress_pct"]):
        reasons.append(f"progress {progress:.2f}% ({progress_points}/{points['progress_max']})")
    if delta >= float(gates["minimum_progress_delta_pct"]):
        reasons.append(f"+{delta:.2f}pp since prior sample ({acceleration_points}/{points['progress_acceleration_max']})")
    if buy_age <= float(gates["maximum_latest_buy_age_seconds"]):
        reasons.append(f"recent buy activity ({recency_points}/{points['recent_buy_activity_max']})")
    if market_cap >= float(gates["minimum_market_cap_usd"]):
        reasons.append(f"market cap ${market_cap:,.0f} ({market_cap_points}/{points['market_cap_max']})")
    reasons.append(
        f"recent flow: {trade_metrics['buy_count']} buys / {trade_metrics['sell_count']} sells, "
        f"{trade_metrics['unique_buyers']} buyers, net {float(trade_metrics['net_buy_ratio']):+.0%}, "
        f"top buyer {float(trade_metrics['top_buyer_share']):.0%}"
    )
    required = (
        age >= float(gates["minimum_age_seconds"])
        and progress >= float(gates["minimum_progress_pct"])
        and delta >= float(gates["minimum_progress_delta_pct"])
        and buy_age <= float(gates["maximum_latest_buy_age_seconds"])
        and market_cap >= float(gates["minimum_market_cap_usd"])
        and int(trade_metrics["unique_buyers"]) >= int(gates["minimum_recent_buyers"])
        and int(trade_metrics["buy_count"]) >= int(gates["minimum_recent_buys"])
        and float(trade_metrics["net_buy_ratio"]) >= float(gates["minimum_net_buy_ratio"])
        and float(trade_metrics["top_buyer_share"]) <= float(gates["maximum_top_buyer_share"])
    )
    if not required:
        reasons.append("one or more required gates not met")
    return score, delta, required, reasons


def address_line(label: str, value: Any) -> str:
    address = str(value)
    return f"{label}: {address}\n{EXPLORER}{address}"


def render_alert(launch: dict[str, Any], score: int, delta: float, reasons: list[str], trade_metrics: dict[str, Any]) -> str:
    stock = launch["stock"]
    return "\n".join([
        "PONS — SCORED STOCK-PAIR WATCHLIST CANDIDATE",
        f"Score: {score}/100 | {launch.get('symbol', '?')} — {launch.get('name', '?')}",
        f"Paired canonical stock: {stock['symbol']} — {stock['name']}",
        address_line("Launch token", launch["token"]),
        address_line("Canonical stock token", stock["address"]),
        address_line("Pons v2 factory", launch["factory"]),
        address_line("Graduated pool (zero address = pre-graduation; curve address is not exposed by this public feed)", launch["pool"]),
        address_line("Deployer", launch["deployer"]),
        "Recent top buyers (trade concentration, NOT profitability):\n" + "\n".join(
            f"{wallet}\n{EXPLORER}{wallet}" for wallet in trade_metrics["top_buyers"]
        ),
        f"Launch tx: {launch.get('transactionHash', 'unavailable')}",
        f"Launched: {launch.get('launchedAt', 'unavailable')} | block: {launch.get('blockNumber', 'unavailable')}",
        f"Progress: {float(launch.get('graduationProgressPct') or 0):.2f}% | change: +{delta:.2f}pp | market cap: ${float(launch.get('marketCapUsd') or 0):,.2f}",
        "Signals: " + "; ".join(reasons),
        "Missing by design: realized wallet PnL, unique-buyer count, and Fomo social confirmation are not yet verified/indexed.",
        "Research candidate only — no trade recommendation or wallet action.",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--report", action="store_true", help="print health even when no candidate qualifies")
    args = parser.parse_args()
    observed_at = now_utc()
    try:
        config = load_config(args.config)
        stocks = canonical_stock_tokens(fetch_json(config["sources"]["robinhood_active_stock_registry"]))
        launches = stock_paired_launches(fetch_json(config["sources"]["pons_launch_feed"]), stocks)
        state = load_state(args.state)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        print(f"PONS ALPHA WATCH ERROR — {type(exc).__name__}: {str(exc)[:240]}")
        return 1

    snapshots = {} if state is None else state["snapshots"]
    alerted = {} if state is None else state["alert_scores"]
    next_snapshots = dict(snapshots)
    candidates = []
    trade_feed_errors = 0
    gates = config["required_gates"]
    for launch in launches:
        token = str(launch["token"]).lower()
        previous = snapshots.get(token)
        progress = float(launch.get("graduationProgressPct") or 0)
        delta = progress - float(previous.get("progress") or 0) if previous else 0.0
        launched_at = parse_time(launch.get("launchedAt"))
        latest_buy_at = parse_time(launch.get("latestBuyAt"))
        age = (observed_at - launched_at).total_seconds() if launched_at else -1
        buy_age = (observed_at - latest_buy_at).total_seconds() if latest_buy_at else float("inf")
        preliminary = (
            age >= float(gates["minimum_age_seconds"])
            and progress >= float(gates["minimum_progress_pct"])
            and delta >= float(gates["minimum_progress_delta_pct"])
            and buy_age <= float(gates["maximum_latest_buy_age_seconds"])
            and float(launch.get("marketCapUsd") or 0) >= float(gates["minimum_market_cap_usd"])
        )
        if preliminary:
            try:
                metrics = recent_trade_metrics(str(launch["token"]), observed_at, float(gates["trades_lookback_seconds"]))
                score, delta, required, reasons = score_launch(launch, previous, metrics, config, observed_at)
                threshold = int(config["scoring"]["alert_score_minimum"])
                prior_score = int(alerted.get(token, 0))
                if required and score >= threshold and score >= prior_score + 10:
                    candidates.append((launch, score, delta, reasons, metrics))
                    alerted[token] = score
            except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError, urllib.error.HTTPError):
                trade_feed_errors += 1
        next_snapshots[token] = compact_snapshot(launch, observed_at)

    write_state(args.state, next_snapshots, alerted, observed_at)
    if candidates:
        print("\n\n".join(render_alert(*candidate) for candidate in candidates))
    elif args.report:
        phase = "BASELINE" if state is None else "OK"
        print(f"PONS ALPHA WATCH {phase} — {len(launches)} official-stock-paired launches scanned; {len(stocks)} official active stock tokens; no newly qualified candidate; trade-feed errors: {trade_feed_errors}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
