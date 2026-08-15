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
DEPLOYMENT_SNAPSHOTS = BASE / 'snapshots' / '2026-08-14'
DEPLOYMENT_FACT = BASE / 'facts' / 'aave-v3-deployment-feed-map.json'
OUTPUT = BASE / 'output'


class EvidenceError(ValueError):
    """A deployment statement cannot be reproduced from its cited snapshots."""


def verify_snapshot_manifest(snapshot_dir: Path) -> dict:
    manifest = json.loads((snapshot_dir / 'manifest.json').read_text())
    sources = manifest.get('sources')
    if not isinstance(sources, dict) or not sources:
        raise EvidenceError(f'{snapshot_dir}: no manifest sources')
    for name, meta in sources.items():
        payload = (snapshot_dir / name).read_bytes()
        if hashlib.sha256(payload).hexdigest() != meta.get('sha256'):
            raise EvidenceError(f'snapshot hash: {name}')
        if len(payload) != meta.get('bytes'):
            raise EvidenceError(f'snapshot byte count: {name}')
        if meta.get('status') != 200:
            raise EvidenceError(f'snapshot status: {name} = {meta.get("status")}')
    return manifest


def _address(value: object, field: str) -> str:
    if not isinstance(value, str) or len(value) != 42 or not value.startswith('0x'):
        raise EvidenceError(f'{field}: expected an EVM address')
    try:
        int(value[2:], 16)
    except ValueError as exc:
        raise EvidenceError(f'{field}: malformed EVM address') from exc
    return value.lower()


def _integer(value: object, field: str) -> int:
    try:
        parsed = int(str(value))
    except (TypeError, ValueError) as exc:
        raise EvidenceError(f'{field}: expected an integer') from exc
    if parsed < 0:
        raise EvidenceError(f'{field}: must be non-negative')
    return parsed


def _rpc_snapshot(snapshot_dir: Path, name: object, manifest: dict) -> dict:
    if not isinstance(name, str):
        raise EvidenceError('snapshot reference: expected a path')
    path = Path(name)
    if path.name != name.rsplit('/', 1)[-1] or path.name not in manifest['sources']:
        raise EvidenceError(f'snapshot reference: not in manifest: {name}')
    return json.loads((snapshot_dir / path.name).read_text())


def _rpc_result(snapshot: dict, *, to: str, data: str, field: str) -> str:
    request = snapshot.get('request', {})
    params = request.get('params', [])
    call = params[0] if params else {}
    if request.get('method') != 'eth_call' or str(call.get('to', '')).lower() != to:
        raise EvidenceError(f'{field}: cited snapshot calls a different contract')
    if str(call.get('data', '')).lower() != data:
        raise EvidenceError(f'{field}: cited snapshot calls a different method')
    result = snapshot.get('response', {}).get('result')
    if not isinstance(result, str) or not result.startswith('0x'):
        raise EvidenceError(f'{field}: cited snapshot has no hex result')
    return result[2:].lower()


def verify_deployment_feed_map(fact_path: Path = DEPLOYMENT_FACT, snapshot_dir: Path = DEPLOYMENT_SNAPSHOTS) -> None:
    """Fail closed unless every Aave feed-map claim reproduces from hashed reads."""
    manifest = verify_snapshot_manifest(snapshot_dir)
    fact = json.loads(fact_path.read_text())
    if fact.get('protocol') != 'Aave V3' or fact.get('network') != 'Ethereum mainnet':
        raise EvidenceError('fact scope: expected Aave V3 on Ethereum mainnet')
    oracle = _address(fact.get('oracle_address'), 'oracle_address')
    source_name = 'aave-v3-ethereum.sol'
    source_meta = manifest['sources'].get(source_name, {})
    if fact.get('oracle_source') != source_meta.get('url'):
        raise EvidenceError('oracle_source: does not match the cited source snapshot')
    if oracle not in (snapshot_dir / source_name).read_text().lower():
        raise EvidenceError('oracle_address: absent from the cited source snapshot')
    assets = fact.get('assets')
    if not isinstance(assets, list) or not assets:
        raise EvidenceError('assets: expected a non-empty bounded map')
    for asset in assets:
        if not isinstance(asset, dict):
            raise EvidenceError('asset: expected an object')
        symbol = asset.get('symbol')
        if not isinstance(symbol, str) or not symbol:
            raise EvidenceError('symbol: required')
        asset_address = _address(asset.get('asset_address'), 'asset_address')
        feed_address = _address(asset.get('feed_address'), 'feed_address')
        refs = asset.get('snapshots')
        if not isinstance(refs, dict):
            raise EvidenceError('snapshots: required')
        source = _rpc_snapshot(snapshot_dir, refs.get('asset_source'), manifest)
        source_result = _rpc_result(source, to=oracle, data='0x92bf2be0' + asset_address[2:].rjust(64, '0'), field='feed_address')
        if source_result[-40:] != feed_address[2:]:
            raise EvidenceError('feed_address: does not match the cited oracle response')
        decimals = _rpc_snapshot(snapshot_dir, refs.get('feed_decimals'), manifest)
        decimals_result = _rpc_result(decimals, to=feed_address, data='0x313ce567', field='feed_decimals')
        if int(decimals_result, 16) != _integer(asset.get('feed_decimals'), 'feed_decimals'):
            raise EvidenceError('feed_decimals: does not match the cited feed response')
        round_data = _rpc_snapshot(snapshot_dir, refs.get('feed_latest_round_data'), manifest)
        words = _rpc_result(round_data, to=feed_address, data='0xfeaf968c', field='latest_round_data')
        if len(words) != 64 * 5:
            raise EvidenceError('latest_round_data: expected five ABI words')
        observed = [int(words[index:index + 64], 16) for index in range(0, len(words), 64)]
        claimed = [_integer(asset.get('latest_round_id'), 'latest_round_id'), _integer(asset.get('latest_round_answer'), 'latest_round_answer'), _integer(asset.get('latest_round_timestamp'), 'latest_round_timestamp')]
        if [observed[0], observed[1], observed[3]] != claimed or observed[3] == 0:
            raise EvidenceError('latest_round_data: does not match the cited feed response')


def main() -> int:
    try:
        manifest = verify_snapshot_manifest(SNAPSHOTS)
        verify_deployment_feed_map()
        # load_facts validates every evidence quote and score bound against snapshots.
        rows = load_facts()
        if not rows:
            raise EvidenceError('no protocol facts')
        expected = build()
        names = ('scorecard.md', 'scorecard.json', 'scorecard.html')
        for name, rebuilt in zip(names, expected):
            committed = (OUTPUT / name).read_text()
            if committed != rebuilt:
                raise EvidenceError(f'generated output drift: {name}')
    except (EvidenceError, FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f'FAIL {exc}', file=sys.stderr)
        return 1
    print(f'OK oracle scorecard: {len(rows)} protocol fact files; {len(manifest["sources"])} baseline and {len(json.loads((DEPLOYMENT_SNAPSHOTS / "manifest.json").read_text())["sources"])} Aave snapshots hashed; generated outputs exact; deployment claims reproduced')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
