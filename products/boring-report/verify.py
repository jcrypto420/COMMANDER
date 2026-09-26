#!/usr/bin/env python3
"""Verify a Boring Report weekly issue against committed snapshots.

Total check: rebuilds the entire report from the committed snapshots using
the one authoritative generator and diffs it line-by-line against the
committed file. Only the generated_at timestamp inside the data block is
exempt. Any other difference — a number, a label, a taxonomy note — fails.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_weekly import build_report  # noqa: E402

GENERATED_AT = re.compile(r'^\s*"generated_at": ".*"$')


def normalize(text: str) -> list[str]:
    return [l for l in text.splitlines() if not GENERATED_AT.match(l)]


def main(path: str) -> int:
    report = Path(path)
    week = report.stem
    committed = normalize(report.read_text())
    rebuilt = normalize(build_report(week))

    if committed == rebuilt:
        print(f'OK {report}')
        return 0

    for i, (a, b) in enumerate(zip(committed, rebuilt), 1):
        if a != b:
            print(f'line {i} differs:\n  committed: {a}\n  rebuilt:   {b}', file=sys.stderr)
    if len(committed) != len(rebuilt):
        print(f'length differs: committed {len(committed)} lines, rebuilt {len(rebuilt)}', file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
