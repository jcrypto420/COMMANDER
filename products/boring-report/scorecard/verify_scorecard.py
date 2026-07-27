#!/usr/bin/env python3
"""Fail-closed verifier for the Oracle Scorecard v0 evidence artifact."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(BASE))
from build_scorecard import build, load_facts  # noqa: E402

DATE = '2026-07-27'
SNAPSHOTS = BASE / 'snapshots' / DATE
OUTPUT = BASE / 'output'


def main() -> int:
    manifest = json.loads((SNAPSHOTS / 'manifest.json').read_text())
    for name, meta in manifest['sources'].items():
        payload = (SNAPSHOTS / name).read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        if actual != meta['sha256']:
            print(f'FAIL snapshot hash: {name}', file=sys.stderr)
            return 1
        if meta['status'] != 200:
            print(f'FAIL snapshot status: {name} = {meta["status"]}', file=sys.stderr)
            return 1

    # load_facts validates every evidence quote and score bound against snapshots.
    rows = load_facts()
    if not rows:
        print('FAIL no protocol facts', file=sys.stderr)
        return 1
    expected = build()
    names = ('scorecard.md', 'scorecard.json', 'scorecard.html')
    for name, rebuilt in zip(names, expected):
        committed = (OUTPUT / name).read_text()
        if committed != rebuilt:
            print(f'FAIL generated output drift: {name}', file=sys.stderr)
            return 1
    print(f'OK oracle scorecard: {len(rows)} protocol fact files; {len(manifest["sources"])} hashed source snapshots; generated outputs exact')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
