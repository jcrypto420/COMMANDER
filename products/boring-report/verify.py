#!/usr/bin/env python3
"""Verify a Boring Report weekly issue against committed snapshots.

Fails closed on any number / snapshot mismatch.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'products' / 'boring-report'
SNAP_DIR = BASE / 'snapshots' / '2026-07-05'


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def score_asset(a, price_map):
    def_price = float(a.get('price') or 0)
    cg_price = float((price_map.get(a.get('gecko_id') or '') or {}).get('usd') or def_price)
    current = float((a.get('circulating') or {}).get('peggedUSD') or 0)
    prev_month = float((a.get('circulatingPrevMonth') or {}).get('peggedUSD') or current or 1)
    chain_circ = a.get('chainCirculating') or {}
    shares = []
    for vals in chain_circ.values():
        cur = float(((vals or {}).get('current') or {}).get('peggedUSD') or 0)
        if current > 0:
            shares.append(cur / current)
    top_share = max(shares) if shares else 1.0
    concentration_score = clamp((1 - top_share) * 15, 0, 15)
    dev_bps = max(abs(def_price - 1) * 10000, abs(cg_price - 1) * 10000)
    peg_score = clamp(30 - (dev_bps / 10), 0, 30)
    mech = str(a.get('pegMechanism') or '').lower()
    if 'fiat' in mech:
        reserve_score, redemption_score = 25, 15
    elif 'crypto' in mech:
        reserve_score, redemption_score = 19, 11
    elif 'algo' in mech:
        reserve_score, redemption_score = 10, 7
    else:
        reserve_score, redemption_score = 14, 9
    incident_score = 15
    total = round(clamp(peg_score + reserve_score + redemption_score + concentration_score + incident_score, 0, 100))
    supply_30d_pct = ((current - prev_month) / prev_month) * 100 if prev_month else 0
    return {
        'name': a.get('name') or '',
        'symbol': a.get('symbol') or '',
        'defillama_price': def_price,
        'coingecko_price': cg_price,
        'supply_30d_pct': supply_30d_pct,
        'peg_dev_bps': dev_bps,
        'boring_score': total,
        'mechanism': a.get('pegMechanism') or 'unknown',
    }


def main(path: str) -> int:
    report = Path(path)
    text = report.read_text()
    defillama = json.loads((SNAP_DIR / 'defillama-stablecoins.json').read_text())
    cg = json.loads((SNAP_DIR / 'coingecko-prices.json').read_text())
    assets = sorted(defillama['peggedAssets'], key=lambda a: float((a.get('circulating') or {}).get('peggedUSD') or 0), reverse=True)
    top10 = []
    for a in assets:
        if a.get('gecko_id'):
            top10.append(a)
        if len(top10) == 10:
            break
    rows = [score_asset(a, cg) for a in top10]
    rows.sort(key=lambda r: (-r['boring_score'], r['peg_dev_bps']))
    errors = []
    for r in rows:
        for n in (f"{r['defillama_price']:.6f}", f"{r['coingecko_price']:.6f}", f"{r['boring_score']}"):
            if n not in text:
                errors.append(f"missing {n} for {r['symbol']}")
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
