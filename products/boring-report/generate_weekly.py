#!/usr/bin/env python3
"""Generate the weekly Boring Report from committed public-source snapshots.

P0/P1 rule: no model-generated numbers. Every number in the report must come
from a committed JSON snapshot in products/boring-report/snapshots/.

This is the single authoritative generator — the .md it writes is exactly what
verify.py checks. No separate/undocumented scoring logic anywhere else.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = 'products/boring-report'
SNAP_SUBDIR = 'snapshots/2026-07-05'
SNAP_DIR = ROOT / BASE / SNAP_SUBDIR
WEEKLY_DIR = ROOT / BASE / 'weekly'

# Known tokenized cash-equivalent / NAV-accruing funds (classified by known
# fund identity, not by a price threshold — accrual mechanics vary: some
# accrue via rising unit price like USYC/USDY, others via a fixed $1 unit
# price with growing unit count like BUIDL. A price-only heuristic would
# misclassify one or the other. These are NOT $1-peg stablecoins and are
# never scored on peg deviation.
NAV_ACCRUING_GECKO_IDS = {
    'hashnote-usyc': 'Circle USYC',
    'blackrock-usd-institutional-digital-liquidity-fund': 'BlackRock USD (BUIDL)',
    'ondo-us-dollar-yield': 'Ondo US Dollar Yield (USDY)',
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
    incident_score = 15  # neutral v0 default until an incident ledger exists; never model-invented
    total = round(clamp(peg_score + reserve_score + redemption_score + concentration_score + incident_score, 0, 100))
    supply_30d_pct = ((current - prev_month) / prev_month) * 100 if prev_month else 0
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
        'boring_score': total,
        'mechanism': a.get('pegMechanism') or 'unknown',
    }


def build_report(week: str) -> str:
    defillama = json.loads((SNAP_DIR / 'defillama-stablecoins.json').read_text())
    cg = json.loads((SNAP_DIR / 'coingecko-prices.json').read_text())
    assets = sorted(
        defillama['peggedAssets'],
        key=lambda a: float((a.get('circulating') or {}).get('peggedUSD') or 0),
        reverse=True,
    )

    stablecoins, nav_accruing = [], []
    for a in assets:
        if not a.get('gecko_id'):
            continue
        (nav_accruing if a['gecko_id'] in NAV_ACCRUING_GECKO_IDS else stablecoins).append(a)

    top10 = stablecoins[:10]
    rows = sorted((score_asset(a, cg) for a in top10),
                  key=lambda r: (-r['boring_score'], r['peg_dev_bps'], -r['current_supply_usd']))
    nav_rows = [score_asset(a, cg) for a in nav_accruing]

    lines = []
    lines.append('# The Boring Report — Weekly')
    lines.append('## Outlook: stable')
    lines.append('')
    lines.append(f'- **Week:** {week}')
    lines.append('- **Methodology:** PRD §5 v1, implemented from committed snapshots only')
    lines.append('- **Truth harness:** PRD §7; verify.py fails on any number/snapshot mismatch')
    lines.append('- **Data budget:** $0; public sources only')
    lines.append('')
    lines.append('## Source snapshots')
    for f in ('defillama-stablecoins.json', 'coingecko-prices.json', 'manifest.json'):
        lines.append(f'- `{BASE}/{SNAP_SUBDIR}/{f}`')
    lines.append('')
    lines.append('## Top 10 stablecoins')
    lines.append('')
    lines.append('| Rank | Asset | Mechanism | DefiLlama price | CoinGecko price | 30d supply change | Peg dev | Boring score |')
    lines.append('|---|---|---|---:|---:|---:|---:|---:|')
    for i, r in enumerate(rows, 1):
        cg_disp = f"{r['coingecko_price']:.6f}" if r['coingecko_price'] else 'n/a'
        lines.append(
            f"| {i} | {r['symbol']} — {r['name']} | {r['mechanism']} | {r['defillama_price']:.6f} | "
            f"{cg_disp} | {r['supply_30d_pct']:.2f}% | {r['peg_dev_bps']:.1f} bps | {r['boring_score']} |"
        )
    lines.append('')
    lines.append('## Tokenized cash-equivalents (NOT scored on peg deviation)')
    lines.append('')
    lines.append('These are yield-bearing / NAV-accruing tokenized funds, not $1-peg stablecoins.')
    lines.append('A price above $1 is accrual by design, not a depeg — scoring them on peg')
    lines.append('deviation would be methodologically wrong, so they get their own table until')
    lines.append('a NAV-tracking benchmark exists (tracked as a v1.1 methodology extension).')
    lines.append('')
    lines.append('| Asset | DefiLlama price | Note |')
    lines.append('|---|---:|---|')
    for a in nav_accruing:
        name = NAV_ACCRUING_GECKO_IDS[a['gecko_id']]
        price = float(a.get('price') or 0)
        lines.append(f"| {name} | {price:.6f} | tokenized cash-equivalent fund, not ranked |")
    lines.append('')
    lines.append('## Score method, v1 interpretation')
    lines.append('- **Peg stability (0–30):** worst of DefiLlama vs CoinGecko deviation from $1, scaled linearly at 10 points per 100 bps.')
    lines.append('- **Reserve / mechanism quality (0–25):** fiat-backed > crypto-backed > algorithmic/other, based on `pegMechanism` in the snapshot.')
    lines.append("- **Redemption clarity (0–15):** same snapshot-derived mechanism proxy, kept separate to preserve the PRD's draft rubric structure.")
    lines.append("- **Concentration / custody structure (0–15):** inverse of the largest chain's share of circulating supply in the DefiLlama snapshot.")
    lines.append('- **Incident history (0–15):** neutral 15 in v0 until an incident ledger is added; no incidents are model-invented.')
    lines.append('- **Asset-class filter:** tokenized cash-equivalent funds (BUIDL, USYC, USDY) are classified by known fund identity and excluded from peg scoring — see the table above.')
    lines.append('')
    lines.append('## Methodology note')
    lines.append('This v0 is intentionally boring: every figure in the table traces to one of the committed JSON snapshots above. The report is not allowed to exceed the source snapshots. No source snapshot, no number.')
    lines.append('')

    data_block = {
        'week': week,
        'rows': rows,
        'nav_accruing': nav_rows,
        'snapshots': [f'{BASE}/{SNAP_SUBDIR}/{f}' for f in
                      ('defillama-stablecoins.json', 'coingecko-prices.json', 'manifest.json')],
        'generated_at': datetime.now(timezone.utc).isoformat(),
    }
    lines.append('<!-- BORING_REPORT_DATA')
    lines.append(json.dumps(data_block, indent=2))
    lines.append('-->')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--week', default='2026-W28')
    args = parser.parse_args()
    out = WEEKLY_DIR / f'{args.week}.md'
    out.write_text(build_report(args.week))
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
