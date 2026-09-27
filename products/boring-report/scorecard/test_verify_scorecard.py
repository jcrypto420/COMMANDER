#!/usr/bin/env python3
"""Behavior tests for deployment feed-map evidence verification."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from verify_scorecard import EvidenceError, verify_deployment_feed_map

BASE = Path(__file__).resolve().parent
FACT = BASE / "facts" / "aave-v3-deployment-feed-map.json"
SNAPSHOTS = BASE / "snapshots" / "2026-08-14"


class DeploymentFeedMapVerificationTests(unittest.TestCase):
    def test_accepts_the_committed_weth_evidence_bundle(self) -> None:
        verify_deployment_feed_map(FACT, SNAPSHOTS)

    def test_rejects_a_feed_claim_not_returned_by_its_cited_oracle_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied_fact = Path(tmp) / "fact.json"
            fact = json.loads(FACT.read_text())
            fact["assets"][0]["feed_address"] = "0x000000000000000000000000000000000000dead"
            copied_fact.write_text(json.dumps(fact))
            with self.assertRaisesRegex(EvidenceError, "feed_address"):
                verify_deployment_feed_map(copied_fact, SNAPSHOTS)

    def test_full_verifier_accepts_scorecard_and_deployment_evidence(self) -> None:
        from verify_scorecard import main

        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
