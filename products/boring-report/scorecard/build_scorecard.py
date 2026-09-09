#!/usr/bin/env python3
"""Build Oracle Scorecard v0 only from fact files and committed snapshots."""
from __future__ import annotations

import html
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
FACTS = BASE / 'facts'
OUT = BASE / 'output'
VERSION = 'v0.1-evidence-baseline'


def load_facts() -> list[dict]:
    rows = []
    for path in sorted(FACTS.glob('*.json')):
        fact = json.loads(path.read_text())
        if fact.get('artifact_type') == 'deployment-feed-map':
            continue
        total = 0
        for d in fact['dimensions']:
            if not 0 <= d['points'] <= d['max_points']:
                raise ValueError(f'{path}: invalid score for {d["id"]}')
            total += d['points']
            for e in d['evidence']:
                source = ROOT / e['file']
                if not source.is_file():
                    raise FileNotFoundError(f'{path}: missing {e["file"]}')
                if e['quote'] not in source.read_text(errors='replace'):
                    raise ValueError(f'{path}: quote not found in {e["file"]}: {e["quote"]}')
        fact['total'] = total
        rows.append(fact)
    if not rows:
        raise ValueError('no fact files')
    return sorted(rows, key=lambda x: (-x['total'], x['protocol']))


def markdown(rows: list[dict]) -> str:
    lines = [
        '# The Boring Report — Oracle Scorecard v0',
        '## Outlook: evidence-limited',
        '',
        f'- **Version:** {VERSION}',
        '- **Scope:** architecture evidence only. This is not historical incident telemetry, live deployment configuration, financial advice, or a protocol safety guarantee.',
        '- **Rule:** an unknown control receives zero credit; zero incident-evidence points do **not** claim an incident occurred.',
        '- **Truth harness:** `verify_scorecard.py` validates every quoted claim against a committed source snapshot and rebuilds this artifact exactly.',
        '',
        '## Architecture-evidence scores',
        '',
        '| Protocol | Fallback /30 | Liveness /25 | Concentration /25 | Incidents /20 | Total /100 |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for r in rows:
        points = {d['id']: d['points'] for d in r['dimensions']}
        lines.append(f"| {r['protocol']} | {points['fallback_design']} | {points['liveness_controls']} | {points['source_concentration']} | {points['incident_evidence']} | **{r['total']}** |")
    lines += ['', '## Reading this correctly', '', 'A higher number means more documented architecture controls in this deliberately narrow evidence pack—not a conclusion about security, solvency, historical performance, or current deployed configuration. The next increment must add deployment-specific feed maps, heartbeat/round observations, and a sourced incident ledger before any broader claims are made.', '']
    for r in rows:
        lines += [f"## {r['protocol']}", '', f"**Boundary:** {r['scope']}", '']
        for d in r['dimensions']:
            lines += [f"### {d['label']} — {d['points']}/{d['max_points']}", '', d['rationale'], '', '**Evidence**']
            for e in d['evidence']:
                lines.append(f"- `{e['file']}` — “{e['quote']}”")
            lines.append('')
    lines += ['## Source snapshots', '', '- `products/boring-report/scorecard/snapshots/2026-07-27/manifest.json`', '- `products/boring-report/scorecard/snapshots/2026-07-27/chainlink-feeds-mainnet.json` (inventory foundation for the next deployment-specific pass)', '- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol`', '- `products/boring-report/scorecard/snapshots/2026-07-27/morpho-i-oracle.sol`', '']
    return '\n'.join(lines)


def html_page(rows: list[dict]) -> str:
    table = ''.join(f'<tr><td>{html.escape(r["protocol"])}</td>' + ''.join(f'<td>{d["points"]}/{d["max_points"]}</td>' for d in r['dimensions']) + f'<td><strong>{r["total"]}/100</strong></td></tr>' for r in rows)
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>The Boring Report — Oracle Scorecard v0</title><style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:48px auto;padding:0 20px;background:#101316;color:#e8edf2}}h1{{margin-bottom:0}}.sub{{color:#9ba8b5}}table{{border-collapse:collapse;width:100%;margin:28px 0}}td,th{{padding:12px;border-bottom:1px solid #33414d;text-align:left}}th{{color:#9ed5c5}}.note{{border-left:3px solid #d2b56d;padding-left:16px;color:#d9dfe6}}</style><h1>The Boring Report</h1><p class="sub">Oracle Scorecard v0 · Outlook: evidence-limited</p><p class="note">Architecture evidence only. Unknown controls receive zero credit; this is not a protocol safety guarantee or financial advice.</p><table><thead><tr><th>Protocol</th><th>Fallback</th><th>Liveness</th><th>Concentration</th><th>Incidents</th><th>Total</th></tr></thead><tbody>{table}</tbody></table><p class="sub">Generated deterministically from committed facts and source snapshots. See <code>scorecard.md</code> for citations and boundaries.</p></html>'''


def build() -> tuple[str, str, str]:
    rows = load_facts()
    payload = {'version': VERSION, 'protocols': rows}
    return markdown(rows), json.dumps(payload, indent=2) + '\n', html_page(rows) + '\n'


def main() -> int:
    OUT.mkdir(exist_ok=True)
    md, data, page = build()
    (OUT / 'scorecard.md').write_text(md)
    (OUT / 'scorecard.json').write_text(data)
    (OUT / 'scorecard.html').write_text(page)
    print(f'wrote {OUT}/scorecard.md, scorecard.json, scorecard.html')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
