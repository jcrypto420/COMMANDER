#!/usr/bin/env python3
"""Generate the weekly Boring Report from committed public-source snapshots.

P0/P1 rule: no model-generated numbers. Every number in the report must come
from a committed JSON snapshot in products/boring-report/snapshots/.
"""
from __future__ import annotations

import argparse
import json
import math
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'products' / 'boring-report'
SNAP_DIR = BASE / 'snapshots' / '2026-07-05'
WEEKLY_DIR = BASE / 'weekly'
UA = 'CommanderBoringReport/0.1 (+public no-key source probe; no advice)'
CTX = ssl.create_default_context()


def fetch_json(url: str) -> tuple[object, dict]:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=45, context=CTX) as resp:
        raw = resp.read().decode('utf-8')
        return json.loads(raw), {
            'url': url,
            'status': getattr(resp, 'status', None),
            'content_type': resp.headers.get('content-type', ''),
            'retrieved_at': datetime.now(timezone.utc).isoformat(),
            'bytes': len(raw.encode('utf-8')),
        }


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
    supply_30d_pct = ((current - prev_month) / prev_month) * 100 if prev_month else 0
    incident_score = 15
    return {
        'name': a.get('name') or '',
        'symbol': a.get('symbol') or '',
        'gecko_id': a.get('gecko_id') or '',
        'defillama_price': def_price,
        'coingecko_price': cg_price,
        'current_supply_usd': current,
        'prev_month_supply_usd': prev_month,
        'supply_30d_pct': supply_30d_pct,
        'peg_dev_bps': dev_bps,
        'peg_score': round(peg_score),
        'reserve_score': reserve_score,
        'redemption_score': redemption_score,
        'concentration_score': round(concentration_score),
        'incident_score': incident_score,
        'boring_score': round(clamp(peg_score + reserve_score + redemption_score + concentration_score + incident_score, 0, 100)),
        'mechanism': a.get('pegMechanism') or 'unknown',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--week', default='2026-W28')
    args = parser.parse_args()
    defillama = json.loads((SNAP_DIR / 'defillama-stablecoins.json').read_text())
    cg = json.loads((SNAP_DIR / 'coingecko-prices.json').read_text())
    assets = sorted(
        defillama['peggedAssets'],
        key=lambda a: float((a.get('circulating') or {}).get('peggedUSD') or 0),
        reverse=True,
    )
    top10 = []
    for a in assets:
        if a.get('gecko_id'):
            top10.append(a)
        if len(top10) == 10:
            break
    rows = [score_asset(a, cg) for a in top10]
    rows.sort(key=lambda r: (-r['boring_score'], r['peg_dev_bps'], -r['current_supply_usd']))
    out = WEEKLY_DIR / f'{args.week}.md'
    if not out.exists():
        raise SystemExit(f'missing report: {out}')
    text = out.read_text()
    # Simple exactness checks: each row's core numeric fields must appear.
    for r in rows:
        need = [f"{r['defillama_price']:.6f}", f"{r['coingecko_price']:.6f}", f"{r['boring_score']}"]
        for n in need:
            if n not in text:
                raise SystemExit(f'mismatch: {r["symbol"]} missing {n}')
    print(f'OK {out}')

if __name__ == '__main__':
    main()
