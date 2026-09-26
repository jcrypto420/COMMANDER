#!/usr/bin/env python3
"""Fetch public source snapshots for the Oracle Scorecard v0 (stdlib-only)."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
DATE = '2026-07-27'
OUT = BASE / 'snapshots' / DATE
UA = 'boring-report-scorecard/0.1 (public-source snapshot)'
SOURCES = {
    'chainlink-feeds-mainnet.json': 'https://reference-data-directory.vercel.app/feeds-mainnet.json',
    'aave-oracle.sol': 'https://raw.githubusercontent.com/aave/aave-v3-core/master/contracts/misc/AaveOracle.sol',
    'morpho-i-oracle.sol': 'https://raw.githubusercontent.com/morpho-org/morpho-blue/main/src/interfaces/IOracle.sol',
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {'retrieved_at': datetime.now(timezone.utc).isoformat(), 'sources': {}}
    for name, url in SOURCES.items():
        request = Request(url, headers={'User-Agent': UA})
        with urlopen(request, timeout=30) as response:
            body = response.read()
            meta = {'url': url, 'status': response.status, 'content_type': response.headers.get('Content-Type')}
        if name.endswith('.json'):
            json.loads(body)
        path = OUT / name
        path.write_bytes(body)
        meta.update({'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()})
        manifest['sources'][name] = meta
        print(f'wrote {path} ({meta["status"]}, {meta["bytes"]} bytes)')
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'wrote {OUT / "manifest.json"}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
