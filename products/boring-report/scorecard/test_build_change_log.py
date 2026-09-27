#!/usr/bin/env python3
"""Behavior test for the bounded Aave deployment comparison pilot."""
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "output"


class ChangeLogPilotTests(unittest.TestCase):
    def test_builds_a_cited_comparison_without_a_false_change_or_staleness_claim(self) -> None:
        result = subprocess.run(
            ["python3", "build_change_log.py"],
            cwd=BASE,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        payload = json.loads((OUT / "aave-v3-change-log-pilot.json").read_text())
        self.assertEqual(payload["artifact_type"], "oracle-collateral-change-log-comparison")
        self.assertEqual(payload["comparison_status"], "literal_config_delta_latest_round_fields_only")
        self.assertEqual(payload["network"], "Ethereum mainnet")
        self.assertEqual(payload["baseline_retrieved_at"], "2026-08-14T23:10:35.353Z")
        self.assertEqual(payload["followup_retrieved_at"], "2026-08-16T23:02:31.643640+00:00")
        self.assertEqual(len(payload["assets"]), 1)
        asset = payload["assets"][0]
        self.assertEqual(asset["symbol"], "WETH")
        self.assertEqual(asset["baseline_feed_address"], "0x5424384b256154046e9667ddfaaa5e550145215e")
        self.assertEqual(asset["followup_feed_address"], "0x5424384b256154046e9667ddfaaa5e550145215e")
        self.assertFalse(asset["feed_address_changed"])
        self.assertFalse(asset["feed_decimals_changed"])
        self.assertEqual(asset["latest_round_id_delta"], 48)
        self.assertEqual(asset["latest_round_timestamp_delta"], 171384)
        self.assertEqual(asset["latest_round_answer_delta"], -1073962092)
        self.assertNotIn("stale", payload["comparison_status"].lower())

        markdown = (OUT / "aave-v3-change-log-pilot.md").read_text()
        self.assertIn("Feed address and decimals stayed unchanged", markdown)
        self.assertIn("only the latest round fields advanced", markdown)
        self.assertIn("literal comparison", markdown)
        self.assertIn("-1073962092", markdown)

        html = (OUT / "aave-v3-change-log-pilot.html").read_text()
        self.assertIn("literal comparison pilot", html)
        self.assertIn("Feed address and decimals stayed unchanged", html)
        self.assertIn("48", html)


if __name__ == "__main__":
    unittest.main()
