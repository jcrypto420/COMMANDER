#!/usr/bin/env python3
"""Fetch and commit-ready-snapshot the Boring Report public sources.

Writes snapshots/<date>/{defillama-stablecoins.json,coingecko-prices.json,
manifest.json}. Stdlib only so it runs unchanged on the Pi. Every number the
weekly report prints must trace back to files written here.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
UA = 'boring-report-snapshot/0.1 (public data; contact via repo)'

DEFILLAMA_URL = 'https://stablecoins.llama.fi/stablecoins?includePrices=true'

# Everything the report can cover needs a CoinGecko cross-check price:
# top-10 candidates + mechanism-watch set + NAV-accruing funds. An id
# missing here means the report falls back to the DefiLlama price and
# must say so — never silently.
COINGECKO_IDS = [
    'tether', 'usd-coin', 'usds', 'dai', 'usd1-wlfi', 'ethena-usde',
    'global-dollar', 'paypal-usd', 'ripple-usd', 'usdd', 'first-digital-usd',
    'crvusd', 'f-x-protocol-fxusd', 'gho', 'liquity-bold-2',
    'hashnote-usyc', 'blackrock-usd-institutional-digital-liquidity-fund',
    'ondo-us-dollar-yield',
]
COINGECKO_URL = (
    'https://api.coingecko.com/api/v3/simple/price?ids='
    + ','.join(COINGECKO_IDS) + '&vs_currencies=usd&include_last_updated_at=true'
)


def fetch(url: str) -> tuple[bytes, dict]:
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
        meta = {
            'url': url,
            'status': resp.status,
            'content_type': resp.headers.get('Content-Type'),
            'retrieved_at': datetime.now(timezone.utc).isoformat(),
            'bytes': len(body),
        }
    json.loads(body)  # fail loudly if a source returns non-JSON (block page etc.)
    return body, meta


def main() -> int:
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime('%Y-%m-%d')
    snap_dir = BASE / 'snapshots' / date
    snap_dir.mkdir(parents=True, exist_ok=True)

    llama_body, llama_meta = fetch(DEFILLAMA_URL)
    cg_body, cg_meta = fetch(COINGECKO_URL)

    (snap_dir / 'defillama-stablecoins.json').write_bytes(llama_body)
    (snap_dir / 'coingecko-prices.json').write_bytes(cg_body)

    manifest = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_date': date,
        'defillama': llama_meta,
        'coingecko': cg_meta,
        'coingecko_ids_requested': COINGECKO_IDS,
    }
    (snap_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'wrote {snap_dir}/ ({llama_meta["bytes"]} + {cg_meta["bytes"]} bytes)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
