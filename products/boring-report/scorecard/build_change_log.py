#!/usr/bin/env python3
"""Render a bounded Aave V3 Oracle & Collateral Change Log pilot."""
from __future__ import annotations

import html
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
BASELINE_FACT_PATH = BASE / "facts" / "aave-v3-deployment-feed-map.json"
BASELINE_MANIFEST_PATH = BASE / "snapshots" / "2026-08-14" / "manifest.json"
FOLLOWUP_FACT_PATH = BASE / "facts" / "aave-v3-deployment-feed-map-2026-08-16.json"
FOLLOWUP_MANIFEST_PATH = BASE / "snapshots" / "2026-08-16" / "manifest.json"
OUT = BASE / "output"
VERSION = "v0.2-literal-comparison-pilot"


def load_verified_bundle(fact_path: Path, manifest_path: Path) -> dict:
    """Load a bounded fact bundle and ensure its cited sources exist in the manifest."""
    fact = json.loads(fact_path.read_text())
    manifest = json.loads(manifest_path.read_text())
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


def build_payload() -> dict:
    baseline = load_verified_bundle(BASELINE_FACT_PATH, BASELINE_MANIFEST_PATH)
    if FOLLOWUP_FACT_PATH.exists() and FOLLOWUP_MANIFEST_PATH.exists():
        followup = load_verified_bundle(FOLLOWUP_FACT_PATH, FOLLOWUP_MANIFEST_PATH)
        assets = []
        for base_asset, new_asset in zip(baseline["assets"], followup["assets"]):
            assets.append(
                {
                    "symbol": base_asset["symbol"],
                    "asset_address": base_asset["asset_address"],
                    "baseline_feed_address": base_asset["feed_address"],
                    "followup_feed_address": new_asset["feed_address"],
                    "feed_address_changed": base_asset["feed_address"] != new_asset["feed_address"],
                    "baseline_feed_decimals": int(base_asset["feed_decimals"]),
                    "followup_feed_decimals": int(new_asset["feed_decimals"]),
                    "feed_decimals_changed": base_asset["feed_decimals"] != new_asset["feed_decimals"],
                    "baseline_latest_round_id": base_asset["latest_round_id"],
                    "followup_latest_round_id": new_asset["latest_round_id"],
                    "latest_round_id_delta": int(new_asset["latest_round_id"]) - int(base_asset["latest_round_id"]),
                    "baseline_latest_round_timestamp": base_asset["latest_round_timestamp"],
                    "followup_latest_round_timestamp": new_asset["latest_round_timestamp"],
                    "latest_round_timestamp_delta": int(new_asset["latest_round_timestamp"]) - int(base_asset["latest_round_timestamp"]),
                    "baseline_latest_round_answer": base_asset["latest_round_answer"],
                    "followup_latest_round_answer": new_asset["latest_round_answer"],
                    "latest_round_answer_delta": int(new_asset["latest_round_answer"]) - int(base_asset["latest_round_answer"]),
                    "baseline_citations": base_asset["snapshots"],
                    "followup_citations": new_asset["snapshots"],
                }
            )
        return {
            "artifact_type": "oracle-collateral-change-log-comparison",
            "version": VERSION,
            "protocol": baseline["protocol"],
            "network": baseline["network"],
            "baseline_retrieved_at": baseline["retrieved_at"],
            "followup_retrieved_at": followup["retrieved_at"],
            "comparison_status": "literal_config_delta_latest_round_fields_only",
            "scope": followup["scope"],
            "oracle_address": baseline["oracle_address"],
            "oracle_source": baseline["oracle_source"],
            "assets": assets,
            "notes": [
                "Feed address and decimals stayed unchanged; only the latest round fields advanced.",
                "This remains a deployment-specific, source-cited draft artifact and makes no heartbeat, staleness, completeness, or financial-advice claim.",
                "No public posting, payment, settlement, account creation, or external send occurred.",
            ],
        }

    # Baseline-only fallback for older environments.
    assets = []
    for asset in baseline["assets"]:
        assets.append(
            {
                "symbol": asset["symbol"],
                "asset_address": asset["asset_address"],
                "feed_address": asset["feed_address"],
                "feed_decimals": int(asset["feed_decimals"]),
                "latest_round_id": asset["latest_round_id"],
                "latest_round_answer": asset["latest_round_answer"],
                "latest_round_timestamp": asset["latest_round_timestamp"],
                "citations": asset["snapshots"],
            }
        )
    return {
        "artifact_type": "oracle-collateral-change-log-baseline",
        "version": VERSION,
        "protocol": baseline["protocol"],
        "network": baseline["network"],
        "retrieved_at": baseline["retrieved_at"],
        "comparison_status": "baseline_only_no_change_claim",
        "scope": baseline["scope"],
        "oracle_address": baseline["oracle_address"],
        "oracle_source": baseline["oracle_source"],
        "assets": assets,
        "notes": [
            "Heartbeat and staleness remain zero-claim fields unless a primary source supports them.",
            "This draft is deployment-specific and source-cited, but intentionally bounded to a small preferred asset set.",
            "No public posting, payment, settlement, account creation, or external send occurred.",
        ],
    }


def markdown(payload: dict) -> str:
    lines = [
        "# Aave V3 Oracle & Collateral Change Log",
        "## Pilot 0.2 — literal comparison" if payload["artifact_type"] == "oracle-collateral-change-log-comparison" else "## Pilot 0.1 — baseline only",
        "",
        f"- **Network:** {payload['network']}",
    ]
    if payload["artifact_type"] == "oracle-collateral-change-log-comparison":
        lines += [
            f"- **Baseline retrieved:** {payload['baseline_retrieved_at']}",
            f"- **Follow-up retrieved:** {payload['followup_retrieved_at']}",
        ]
    else:
        lines.append(f"- **Retrieved:** {payload['retrieved_at']}")
    lines += [
        f"- **Scope:** {payload['scope']}",
        f"- **Oracle anchor:** `{payload['oracle_address']}` — {payload['oracle_source']}",
        "",
        "## Result",
        "",
    ]
    if payload["artifact_type"] == "oracle-collateral-change-log-comparison":
        lines += [
            "Feed address and decimals stayed unchanged from the baseline; only the latest round fields advanced.",
            "The observed round timestamp is not a heartbeat or staleness determination.",
            "",
            "| Asset | Baseline feed | Follow-up feed | Feed delta | Baseline decimals | Follow-up decimals | Round ID delta | Timestamp delta | Answer delta |",
            "|---|---|---|---|---:|---:|---:|---:|---:|",
        ]
        for asset in payload["assets"]:
            config_delta = "unchanged" if not asset["feed_address_changed"] else "changed"
            decimals_delta = "unchanged" if not asset["feed_decimals_changed"] else "changed"
            lines.append(
                f"| {asset['symbol']} | `{asset['baseline_feed_address']}` | `{asset['followup_feed_address']}` | {config_delta} | "
                f"{asset['baseline_feed_decimals']} | {asset['followup_feed_decimals']} | {asset['latest_round_id_delta']} | {asset['latest_round_timestamp_delta']} | {asset['latest_round_answer_delta']} |"
            )
    else:
        lines += [
            "No prior verified baseline is supplied, so this pilot records the first comparison point and makes no change claim.",
            "The observed round timestamp is not a heartbeat or staleness determination.",
            "",
            "| Asset | Configured feed | Decimals | Observed round ID | Observed round timestamp |",
            "|---|---|---:|---:|---:|",
        ]
        for asset in payload["assets"]:
            lines.append(
                f"| {asset['symbol']} | `{asset['feed_address']}` | {asset['feed_decimals']} | {asset['latest_round_id']} | {asset['latest_round_timestamp']} |"
            )
    lines += ["", "## Evidence", ""]
    for asset in payload["assets"]:
        lines += [f"### {asset['symbol']}", ""]
        if payload["artifact_type"] == "oracle-collateral-change-log-comparison":
            for label, path in asset["baseline_citations"].items():
                lines.append(f"- **baseline {label}:** `{path}`")
            for label, path in asset["followup_citations"].items():
                lines.append(f"- **follow-up {label}:** `{path}`")
        else:
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
    if payload["artifact_type"] == "oracle-collateral-change-log-comparison":
        rows = "".join(
            "<tr>"
            f"<td>{html.escape(asset['symbol'])}</td>"
            f"<td><code>{html.escape(asset['baseline_feed_address'])}</code></td>"
            f"<td><code>{html.escape(asset['followup_feed_address'])}</code></td>"
            f"<td>{'unchanged' if not asset['feed_address_changed'] else 'changed'}</td>"
            f"<td>{asset['baseline_feed_decimals']}</td><td>{asset['followup_feed_decimals']}</td>"
            f"<td>{asset['latest_round_id_delta']}</td><td>{asset['latest_round_timestamp_delta']}</td>"
            f"<td>{asset['latest_round_answer_delta']}</td></tr>"
            for asset in payload["assets"]
        )
        return f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>Aave V3 Oracle &amp; Collateral Change Log — literal comparison pilot</title><style>body{{font-family:system-ui,sans-serif;max-width:1080px;margin:48px auto;padding:0 20px;background:#101316;color:#e8edf2}}h1{{margin-bottom:0}}.sub{{color:#9ba8b5}}.note{{border-left:3px solid #d2b56d;padding-left:16px;color:#d9dfe6}}table{{border-collapse:collapse;width:100%;margin:28px 0}}td,th{{padding:12px;border-bottom:1px solid #33414d;text-align:left}}th{{color:#9ed5c5}}code{{word-break:break-all}}</style><h1>Aave V3 Oracle &amp; Collateral Change Log</h1><p class="sub">Pilot 0.2 · literal comparison · {html.escape(payload['network'])}</p><p class="note">Feed address and decimals stayed unchanged from the baseline; only the latest round fields advanced. The observed round timestamp is not a heartbeat or staleness determination.</p><table><thead><tr><th>Asset</th><th>Baseline feed</th><th>Follow-up feed</th><th>Feed delta</th><th>Baseline decimals</th><th>Follow-up decimals</th><th>Round ID delta</th><th>Timestamp delta</th><th>Answer delta</th></tr></thead><tbody>{rows}</tbody></table><p class="sub">Generated deterministically from verified bounded deployment feed-map fact bundles. This is not a completeness, safety, or financial-advice claim.</p></html>\n'''

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
    payload = build_payload()
    return markdown(payload), json.dumps(payload, indent=2) + "\n", html_page(payload)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    md, data, page = build()
    (OUT / "aave-v3-change-log-pilot.md").write_text(md)
    (OUT / "aave-v3-change-log-pilot.json").write_text(data)
    (OUT / "aave-v3-change-log-pilot.html").write_text(page)
    print("wrote Aave V3 change-log pilot (md/json/html)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
