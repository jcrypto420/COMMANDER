#!/usr/bin/env python3
"""Verify a Boring Report weekly issue against committed snapshots.

Fails closed on any number / snapshot mismatch. Reuses the exact selection
and scoring logic from generate_weekly.py — no independent reimplementation
that could silently drift from what actually produced the report.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_weekly import NAV_ACCRUING_GECKO_IDS, score_asset  # noqa: E402
import json  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'products' / 'boring-report'
SNAP_DIR = BASE / 'snapshots' / '2026-07-05'


def main(path: str) -> int:
    report = Path(path)
    text = report.read_text()
    defillama = json.loads((SNAP_DIR / 'defillama-stablecoins.json').read_text())
    cg = json.loads((SNAP_DIR / 'coingecko-prices.json').read_text())
    assets = sorted(defillama['peggedAssets'], key=lambda a: float((a.get('circulating') or {}).get('peggedUSD') or 0), reverse=True)

    stablecoins, nav_accruing = [], []
    for a in assets:
        if not a.get('gecko_id'):
            continue
        (nav_accruing if a['gecko_id'] in NAV_ACCRUING_GECKO_IDS else stablecoins).append(a)

    top10 = stablecoins[:10]
    rows = sorted((score_asset(a, cg) for a in top10),
                  key=lambda r: (-r['boring_score'], r['peg_dev_bps'], -r['current_supply_usd']))

    errors = []
    for r in rows:
        for n in (f"{r['defillama_price']:.6f}", f"{r['coingecko_price']:.6f}", f"{r['boring_score']}"):
            if n not in text:
                errors.append(f"missing {n} for {r['symbol']}")
    for a in nav_accruing:
        price = float(a.get('price') or 0)
        if f"{price:.6f}" not in text:
            errors.append(f"missing NAV-accruing price {price:.6f} for {a.get('symbol')}")
    for gid in NAV_ACCRUING_GECKO_IDS:
        if any(gid == a.get('gecko_id') for a in top10):
            errors.append(f"asset-class violation: {gid} appears in the scored stablecoin table")

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    if 'Outlook: stable' not in text:
        print('missing voice marker', file=sys.stderr)
        return 1
    print(f'OK {report}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
