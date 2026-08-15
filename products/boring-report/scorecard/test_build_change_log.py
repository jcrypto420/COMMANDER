#!/usr/bin/env python3
"""Behavior test for the bounded Aave deployment baseline pilot."""
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "output"


class ChangeLogPilotTests(unittest.TestCase):
    def test_builds_a_cited_baseline_without_a_false_change_or_staleness_claim(self) -> None:
        result = subprocess.run(
            ["python3", "build_change_log.py"],
            cwd=BASE,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        payload = json.loads((OUT / "aave-v3-change-log-pilot.json").read_text())
        self.assertEqual(payload["artifact_type"], "oracle-collateral-change-log-baseline")
        self.assertEqual(payload["comparison_status"], "baseline_only_no_change_claim")
        self.assertEqual(payload["network"], "Ethereum mainnet")
        self.assertEqual(len(payload["assets"]), 1)
        self.assertEqual(payload["assets"][0]["symbol"], "WETH")
        self.assertEqual(payload["assets"][0]["feed_address"], "0x5424384b256154046e9667ddfaaa5e550145215e")
        self.assertNotIn("stale", json.dumps(payload).lower())

        markdown = (OUT / "aave-v3-change-log-pilot.md").read_text()
        self.assertIn("No prior verified baseline is supplied", markdown)
        self.assertIn("not a heartbeat or staleness determination", markdown)
        self.assertIn("aave-v3-ethereum.sol", markdown)
        self.assertIn("rpc-feed-latestRoundData-weth-00.json", markdown)

        html = (OUT / "aave-v3-change-log-pilot.html").read_text()
        self.assertIn("Aave V3 Oracle &amp; Collateral Change Log", html)
        self.assertIn("baseline only", html)


if __name__ == "__main__":
    unittest.main()
