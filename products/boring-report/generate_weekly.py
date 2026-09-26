#!/usr/bin/env python3
"""Generate the weekly Boring Report from committed public-source snapshots.

Rules (PRD §3/§7 + methodology v1.1, Gate 1 correction 2026-07-08):
- No model-generated numbers. Every number traces to a committed snapshot.
- Single authoritative generator: verify.py rebuilds this exact output and
  diffs it against the committed report. Any drift fails the build.
- Mechanism facts (class, note, falsifiable line) are a curated fact table
  below — qualitative, sourced from protocol documentation, and versioned
  here so scoring can never silently diverge from the published taxonomy.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = 'products/boring-report'
SNAP_SUBDIR = 'snapshots/2026-07-08'
SNAP_DIR = ROOT / BASE / SNAP_SUBDIR
WEEKLY_DIR = ROOT / BASE / 'weekly'

METHODOLOGY_VERSION = 'v1.1'

# ---------------------------------------------------------------------------
# Mechanism taxonomy (methodology v1.1)
#
# Solvency model (0-25) and redemption clarity (0-15) are assigned per
# mechanism CLASS, not per DefiLlama's binary fiat/crypto tag. The matrix is
# published in every issue; changing a number here is a methodology change
# and requires a Josh gate.
# ---------------------------------------------------------------------------
CLASSES = {
    'fiat-custodial': {
        'label': 'fiat custodial',
        'solvency': 23, 'redemption': 13,
        'explain': 'Issuer holds cash and short-dated Treasuries with custodians; '
                   'redemption is direct with the issuer, KYC-gated. The live risks '
                   'are custodial, banking-rail, and attestation quality — not market structure.',
    },
    'hybrid-cdp-rwa': {
        'label': 'hybrid CDP + RWA',
        'solvency': 20, 'redemption': 12,
        'explain': 'Overcollateralized crypto vaults plus substantial real-world-asset and '
                   'fiat-stablecoin reserves; peg held by PSM-style swap modules while they stay funded.',
    },
    'cdp-hard-liquidation': {
        'label': 'CDP (hard liquidation)',
        'solvency': 19, 'redemption': 12,
        'explain': 'Minted against surplus crypto collateral; solvency defended by '
                   'one-shot liquidations when positions breach their threshold.',
    },
    'cdp-soft-liquidation': {
        'label': 'CDP (soft liquidation)',
        'solvency': 19, 'redemption': 12,
        'explain': "Curve's LLAMMA design: collateral converts to stablecoin gradually across "
                   'a price band instead of one-shot liquidation — gentler in chop, still '
                   'exposed to gap moves.',
    },
    'cdp-immutable': {
        'label': 'CDP (immutable)',
        'solvency': 20, 'redemption': 12,
        'explain': 'Liquity-style immutable contracts: ETH/LST collateral, user-set rates, '
                   'a stability pool absorbs liquidations. No admin keys to misuse, '
                   'and none to fix anything either.',
    },
    'delta-neutral-synthetic': {
        'label': 'delta-neutral synthetic',
        'solvency': 14, 'redemption': 10,
        'explain': 'Staked crypto collateral hedged with short perpetual futures. Solvency '
                   'rides on funding rates staying tolerable and hedging venues staying open; '
                   'mint/redeem runs through whitelisted market makers.',
    },
    'leveraged-split': {
        'label': 'leveraged split',
        'solvency': 14, 'redemption': 10,
        'explain': 'Collateral exposure split into a stable tranche and a leveraged tranche '
                   '(f(x) design); the leveraged side absorbs volatility for as long as '
                   'someone wants to hold it.',
    },
    'issuer-managed-crypto': {
        'label': 'issuer-managed crypto',
        'solvency': 10, 'redemption': 8,
        'explain': 'Issuer-managed crypto collateral pool; reserve reporting is '
                   'issuer-published rather than independently attested in our sources.',
    },
    'unclassified': {
        'label': 'unclassified',
        'solvency': 12, 'redemption': 8,
        'explain': 'No fact-file entry yet. Scored conservatively and flagged; a mechanism '
                   'fact-file entry is required before this asset can score above the floor.',
    },
}

# Per-asset facts: mechanism class + the falsifiable "what would make this
# less boring" line the PRD requires for every score.
MECHANISM_FACTS = {
    'tether': ('fiat-custodial', 'a delayed or qualified reserve attestation.'),
    'usd-coin': ('fiat-custodial', 'attestation gaps or a repeat of banking-partner contagion.'),
    'usd1-wlfi': ('fiat-custodial', 'attestation cadence slipping or reserves drifting from T-bills.'),
    'global-dollar': ('fiat-custodial', 'attestation gaps or redemption friction across partner venues.'),
    'paypal-usd': ('fiat-custodial', 'attestation gaps or issuer policy changes to freeze/redeem rules.'),
    'ripple-usd': ('fiat-custodial', 'attestation gaps or concentration in redemption rails.'),
    'first-digital-usd': ('fiat-custodial', 'attestation opacity or banking-rail concentration.'),
    'dai': ('hybrid-cdp-rwa', 'RWA counterparty impairment or PSM buffer depletion.'),
    'usds': ('hybrid-cdp-rwa', 'RWA counterparty impairment or governance-driven collateral drift.'),
    'ethena-usde': ('delta-neutral-synthetic', 'sustained negative funding or a hedging-venue failure.'),
    'usdd': ('issuer-managed-crypto', 'already less boring: no independent attestation of the collateral pool in our sources.'),
    'crvusd': ('cdp-soft-liquidation', "a collateral crash faster than LLAMMA's band can rebalance."),
    'f-x-protocol-fxusd': ('leveraged-split', 'leveraged-tranche demand evaporating, leaving the stable side unbuffered.'),
    'gho': ('cdp-hard-liquidation', 'a liquidation cascade on Aave or a facilitator misconfiguration.'),
    'liquity-bold-2': ('cdp-immutable', 'stability-pool depletion during an LST depeg.'),
}

# Mechanism watch: curated, structurally distinct solvency designs that sit
# below the top-10 supply cutoff. Criterion: distinct mechanism class,
# >= $25M circulating, re-reviewed when the taxonomy changes.
MECHANISM_WATCH = ['crvusd', 'f-x-protocol-fxusd', 'gho', 'liquity-bold-2']

# Tokenized cash-equivalent / NAV-accruing funds (classified by known fund
# identity, not price threshold — accrual mechanics vary). Never peg-scored.
NAV_ACCRUING_GECKO_IDS = {
    'hashnote-usyc': 'Circle USYC',
    'blackrock-usd-institutional-digital-liquidity-fund': 'BlackRock USD (BUIDL)',
    'ondo-us-dollar-yield': 'Ondo US Dollar Yield (USDY)',
}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def classify(gecko_id: str) -> tuple[str, str]:
    return MECHANISM_FACTS.get(gecko_id, ('unclassified', 'unclassified — fact-file entry required.'))


def score_asset(a, price_map):
    gecko_id = a.get('gecko_id') or ''
    def_price_raw = a.get('price')
    cg_entry = price_map.get(gecko_id) or {}
    cg_price_raw = cg_entry.get('usd')

    # Price fallback is allowed but never silent: the report prints which
    # source(s) actually priced the asset.
    def_price = float(def_price_raw) if def_price_raw else 0.0
    cg_price = float(cg_price_raw) if cg_price_raw else 0.0
    if not def_price and not cg_price:
        raise ValueError(f'no price from either source for {gecko_id}')
    price_sources = ('both' if def_price and cg_price
                     else 'defillama-only' if def_price else 'coingecko-only')

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

    devs = [abs(p - 1) * 10000 for p in (def_price, cg_price) if p]
    dev_bps = max(devs)
    peg_score = clamp(30 - (dev_bps / 10), 0, 30)

    cls_key, less_boring_if = classify(gecko_id)
    cls = CLASSES[cls_key]
    solvency_score, redemption_score = cls['solvency'], cls['redemption']
    incident_score = 15  # neutral until the incident ledger exists; never model-invented

    total = round(clamp(peg_score + solvency_score + redemption_score + concentration_score + incident_score, 0, 100))
    supply_30d_pct = ((current - prev_month) / prev_month) * 100 if prev_month else 0
    return {
        'name': a.get('name') or '',
        'symbol': a.get('symbol') or '',
        'gecko_id': gecko_id,
        'mechanism_class': cls_key,
        'mechanism_label': cls['label'],
        'less_boring_if': less_boring_if,
        'defillama_price': def_price,
        'coingecko_price': cg_price,
        'price_sources': price_sources,
        'current_supply_usd': current,
        'prev_month_supply_usd': prev_month,
        'supply_30d_pct': supply_30d_pct,
        'peg_dev_bps': dev_bps,
        'peg_score': round(peg_score),
        'solvency_score': solvency_score,
        'redemption_score': redemption_score,
        'concentration_score': round(concentration_score),
        'incident_score': incident_score,
        'boring_score': total,
    }


def fmt_price(v: float) -> str:
    return f'{v:.6f}' if v else 'n/a'


def fmt_supply(v: float) -> str:
    return f'${v / 1e9:.1f}B' if v >= 1e9 else f'${v / 1e6:.0f}M'


def summary_row(rank, r) -> str:
    return (f"| {rank} | {r['symbol']} — {r['name']} | {r['mechanism_label']} | {fmt_supply(r['current_supply_usd'])} | "
            f"{r['supply_30d_pct']:+.2f}% | {r['peg_dev_bps']:.1f} bps | {r['boring_score']} |")


def component_row(r) -> str:
    cg = fmt_price(r['coingecko_price']) if r['price_sources'] != 'defillama-only' else 'n/a'
    dl = fmt_price(r['defillama_price']) if r['price_sources'] != 'coingecko-only' else 'n/a'
    return (f"| {r['symbol']} | {dl} | {cg} | {r['peg_score']} | {r['solvency_score']} | "
            f"{r['redemption_score']} | {r['concentration_score']} | {r['incident_score']} | {r['boring_score']} |")


def sort_rows(rows):
    return sorted(rows, key=lambda r: (-r['boring_score'], r['peg_dev_bps'], -r['current_supply_usd']))


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

    top10_assets = stablecoins[:10]
    top10_ids = {a['gecko_id'] for a in top10_assets}
    watch_assets = [a for a in stablecoins if a['gecko_id'] in MECHANISM_WATCH and a['gecko_id'] not in top10_ids]

    rows = sort_rows([score_asset(a, cg) for a in top10_assets])
    watch_rows = sort_rows([score_asset(a, cg) for a in watch_assets])
    nav_rows = [score_asset(a, cg) for a in nav_accruing]
    all_scored = rows + watch_rows
    classes_used = []
    for r in all_scored:
        if r['mechanism_class'] not in classes_used:
            classes_used.append(r['mechanism_class'])

    lines = []
    lines.append('# The Boring Report — Weekly')
    lines.append('## Outlook: stable')
    lines.append('')
    lines.append(f'- **Week:** {week}')
    lines.append(f'- **Methodology:** {METHODOLOGY_VERSION} (Gate 1 revision, 2026-07-08) — see the matrix below; PRD §5')
    lines.append('- **Truth harness:** verify.py rebuilds this report from the committed snapshots and diffs it; any mismatch fails the build')
    lines.append('- **Data budget:** $0; public sources only')
    lines.append('')
    lines.append('## Source snapshots')
    for f in ('defillama-stablecoins.json', 'coingecko-prices.json', 'manifest.json'):
        lines.append(f'- `{BASE}/{SNAP_SUBDIR}/{f}`')
    lines.append('')
    lines.append('## Top 10 stablecoins by circulating supply')
    lines.append('')
    lines.append('| Rank | Asset | Mechanism | Supply | 30d supply | Peg dev | Boring score |')
    lines.append('|---|---|---|---:|---:|---:|---:|')
    for i, r in enumerate(rows, 1):
        lines.append(summary_row(i, r))
    lines.append('')
    lines.append('## Mechanism watch')
    lines.append('')
    lines.append('Curated, not ranked by size: structurally distinct solvency designs below the')
    lines.append('top-10 supply cutoff (criterion: distinct mechanism class, ≥$25M circulating).')
    lines.append('Same rubric, same truth harness — small supply is not a scoring excuse.')
    lines.append('')
    lines.append('| Asset | Mechanism | Supply | 30d supply | Peg dev | Boring score |')
    lines.append('|---|---|---:|---:|---:|---:|')
    for r in watch_rows:
        lines.append(f"| {r['symbol']} — {r['name']} | {r['mechanism_label']} | {fmt_supply(r['current_supply_usd'])} | "
                     f"{r['supply_30d_pct']:+.2f}% | {r['peg_dev_bps']:.1f} bps | {r['boring_score']} |")
    lines.append('')
    lines.append('## Score components (full breakdown, both tables)')
    lines.append('')
    lines.append('| Asset | DefiLlama | CoinGecko | Peg /30 | Solvency /25 | Redemption /15 | Concentration /15 | Incidents /15 | Total |')
    lines.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for r in all_scored:
        lines.append(component_row(r))
    lines.append('')
    lines.append('## Mechanism taxonomy (plain language)')
    lines.append('')
    for key in classes_used:
        lines.append(f"- **{CLASSES[key]['label']}** — {CLASSES[key]['explain']}")
    lines.append('')
    lines.append('## What would make each less boring')
    lines.append('')
    for r in all_scored:
        lines.append(f"- **{r['symbol']}:** {r['less_boring_if']}")
    lines.append('')
    lines.append('## Tokenized cash-equivalents (NOT scored on peg deviation)')
    lines.append('')
    lines.append('These are yield-bearing / NAV-accruing tokenized funds, not $1-peg stablecoins.')
    lines.append('A price above $1 is accrual by design, not a depeg — scoring them on peg')
    lines.append('deviation would be methodologically wrong, so they get their own table until')
    lines.append('a NAV-tracking benchmark exists (still tracked as a methodology extension).')
    lines.append('')
    lines.append('| Asset | DefiLlama price | Note |')
    lines.append('|---|---:|---|')
    for a in nav_accruing:
        name = NAV_ACCRUING_GECKO_IDS[a['gecko_id']]
        price = float(a.get('price') or 0)
        lines.append(f"| {name} | {price:.6f} | tokenized cash-equivalent fund, not ranked |")
    lines.append('')
    lines.append(f'## Score method, {METHODOLOGY_VERSION}')
    lines.append('')
    lines.append('- **Peg stability (0–30):** worst deviation from $1 across available price sources (DefiLlama, CoinGecko), scaled linearly at 10 points per 100 bps. Assets priced by only one source are marked n/a in the other column — the fallback is never silent.')
    lines.append('- **Solvency model (0–25) and redemption clarity (0–15):** assigned per mechanism class from the published matrix below — not from DefiLlama\'s binary fiat/crypto tag. Changing the matrix is a methodology change and requires a gate.')
    lines.append("- **Concentration / custody structure (0–15):** inverse of the largest chain's share of circulating supply in the DefiLlama snapshot.")
    lines.append('- **Incident history (0–15):** neutral 15 until the incident ledger exists; no incidents are model-invented.')
    lines.append('- **Asset-class filter:** tokenized cash-equivalent funds (BUIDL, USYC, USDY) are classified by known fund identity and excluded from peg scoring.')
    lines.append('')
    lines.append('| Mechanism class | Solvency /25 | Redemption /15 |')
    lines.append('|---|---:|---:|')
    for key, c in CLASSES.items():
        lines.append(f"| {c['label']} | {c['solvency']} | {c['redemption']} |")
    lines.append('')
    lines.append('## Methodology note')
    lines.append('Every figure above traces to the committed JSON snapshots listed at the top; verify.py rebuilds this report from those snapshots and fails on any difference. Mechanism classes and notes are a curated fact table in the generator, versioned with the methodology. The report is not allowed to exceed its sources.')
    lines.append('')

    data_block = {
        'week': week,
        'methodology': METHODOLOGY_VERSION,
        'rows': rows,
        'mechanism_watch': watch_rows,
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
