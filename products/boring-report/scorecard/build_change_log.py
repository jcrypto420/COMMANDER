#!/usr/bin/env python3
"""Render a bounded Aave V3 Oracle & Collateral Change Log baseline pilot."""
from __future__ import annotations

import html
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FACT_PATH = BASE / "facts" / "aave-v3-deployment-feed-map.json"
MANIFEST_PATH = BASE / "snapshots" / "2026-08-14" / "manifest.json"
OUT = BASE / "output"
VERSION = "v0.1-baseline-pilot"


def load_verified_baseline() -> dict:
    """Load the bounded fact and ensure its cited sources exist in the manifest."""
    fact = json.loads(FACT_PATH.read_text())
    manifest = json.loads(MANIFEST_PATH.read_text())
    if fact.get("artifact_type") != "deployment-feed-map":
        raise ValueError("expected a deployment-feed-map fact")
    assets = fact.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("expected a non-empty bounded asset set")
    for asset in assets:
        refs = asset.get("snapshots", {})
        for name in ("source", "asset_source", "feed_decimals", "feed_latest_round_data"):
            path = Path(refs.get(name, ""))
            if path.name not in manifest.get("sources", {}):
                raise ValueError(f"missing manifest citation for {name}")
    return fact


def build_payload(fact: dict) -> dict:
    assets = []
    for asset in fact["assets"]:
        assets.append({
            "symbol": asset["symbol"],
            "asset_address": asset["asset_address"],
            "feed_address": asset["feed_address"],
            "feed_decimals": int(asset["feed_decimals"]),
            "latest_round_id": asset["latest_round_id"],
            "latest_round_answer": asset["latest_round_answer"],
            "latest_round_timestamp": asset["latest_round_timestamp"],
            "citations": asset["snapshots"],
        })
    return {
        "artifact_type": "oracle-collateral-change-log-baseline",
        "version": VERSION,
        "protocol": fact["protocol"],
        "network": fact["network"],
        "retrieved_at": fact["retrieved_at"],
        "comparison_status": "baseline_only_no_change_claim",
        "scope": fact["scope"],
        "oracle_address": fact["oracle_address"],
        "oracle_source": fact["oracle_source"],
        "assets": assets,
    }


def markdown(payload: dict) -> str:
    lines = [
        "# Aave V3 Oracle & Collateral Change Log",
        "## Pilot 0.1 — baseline only",
        "",
        f"- **Network:** {payload['network']}",
        f"- **Retrieved:** {payload['retrieved_at']}",
        f"- **Scope:** {payload['scope']}",
        f"- **Oracle anchor:** `{payload['oracle_address']}` — {payload['oracle_source']}",
        "",
        "## Result",
        "",
        "No prior verified baseline is supplied, so this pilot records the first comparison point and makes no change claim.",
        "The observed round timestamp is not a heartbeat or staleness determination.",
        "",
        "| Asset | Configured feed | Decimals | Observed round ID | Observed round timestamp |",
        "|---|---|---:|---:|---:|",
    ]
    for asset in payload["assets"]:
        lines.append(
            f"| {asset['symbol']} | `{asset['feed_address']}` | {asset['feed_decimals']} | "
            f"{asset['latest_round_id']} | {asset['latest_round_timestamp']} |"
        )
    lines += ["", "## Evidence", ""]
    for asset in payload["assets"]:
        lines += [f"### {asset['symbol']}", ""]
        for label, path in asset["citations"].items():
            lines.append(f"- **{label}:** `{path}`")
        lines.append("")
    lines += [
        "## Boundaries",
        "",
        "- Bounded deployment evidence only; the asset set is not complete.",
        "- No public posting, payment, settlement, account creation, or external send occurred.",
        "- Re-run `python3 verify_scorecard.py` before consuming this pilot; it hashes the source bundle and reproduces the cited deployment claims.",
        "",
    ]
    return "\n".join(lines)


def html_page(payload: dict) -> str:
    rows = "".join(
        "<tr>"
        f"<td>{html.escape(asset['symbol'])}</td>"
        f"<td><code>{html.escape(asset['feed_address'])}</code></td>"
        f"<td>{asset['feed_decimals']}</td><td>{asset['latest_round_id']}</td>"
        f"<td>{asset['latest_round_timestamp']}</td></tr>"
        for asset in payload["assets"]
    )
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>Aave V3 Oracle &amp; Collateral Change Log — baseline pilot</title><style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:48px auto;padding:0 20px;background:#101316;color:#e8edf2}}h1{{margin-bottom:0}}.sub{{color:#9ba8b5}}.note{{border-left:3px solid #d2b56d;padding-left:16px;color:#d9dfe6}}table{{border-collapse:collapse;width:100%;margin:28px 0}}td,th{{padding:12px;border-bottom:1px solid #33414d;text-align:left}}th{{color:#9ed5c5}}code{{word-break:break-all}}</style><h1>Aave V3 Oracle &amp; Collateral Change Log</h1><p class="sub">Pilot 0.1 · baseline only · {html.escape(payload['network'])}</p><p class="note">No prior verified baseline is supplied, so this issue makes no change claim. The observed round timestamp is not a heartbeat or staleness determination.</p><table><thead><tr><th>Asset</th><th>Configured feed</th><th>Decimals</th><th>Observed round ID</th><th>Observed round timestamp</th></tr></thead><tbody>{rows}</tbody></table><p class="sub">Generated deterministically from a verified bounded deployment feed-map fact file. This is not a completeness, safety, or financial-advice claim.</p></html>\n'''


def build() -> tuple[str, str, str]:
    payload = build_payload(load_verified_baseline())
    return markdown(payload), json.dumps(payload, indent=2) + "\n", html_page(payload)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    md, data, page = build()
    (OUT / "aave-v3-change-log-pilot.md").write_text(md)
    (OUT / "aave-v3-change-log-pilot.json").write_text(data)
    (OUT / "aave-v3-change-log-pilot.html").write_text(page)
    print("wrote Aave V3 change-log baseline pilot (md/json/html)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
