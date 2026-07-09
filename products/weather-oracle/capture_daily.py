#!/usr/bin/env python3
"""Daily OKC forecast + actuals capture for the weather-oracle MVP.

Run once per evening (cron ~20:30 America/Chicago; Mac: /usr/bin/python3).
Captures, per run, into captures/<YYYY-MM-DD_HHMM>/ (local Central time):

- Robot forecasts, parsed now: NWS gridpoint (OUN/97,94), Open-Meteo
  ECMWF + GFS (daily high/low/PoP, next 3 days).
- Settlement actuals: latest NWS CLI daily climate reports for OKC
  (official high/low) + latest observations for KOKC, KPWA, KTIK, KOUN.
- Human forecasts, archived raw for later parsing: KOCO, News 9, Fox 25,
  KFOR weather pages (gzipped HTML). Parsers come later; history starts now.

Every source is independent — one failure never kills the run. The manifest
records status/bytes/sha256 per source; grading must only ever use numbers
traceable to these files.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent
CENTRAL = ZoneInfo('America/Chicago')

API_UA = 'weather-oracle-capture/0.1 (forecast accountability research; stokesberryjosh@gmail.com)'
BROWSER_UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')

OKC = 'latitude=35.4676&longitude=-97.5164'
OPEN_METEO_URL = ('https://api.open-meteo.com/v1/forecast?' + OKC +
                  '&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max'
                  '&temperature_unit=fahrenheit&timezone=America%2FChicago&forecast_days=3'
                  '&models=ecmwf_ifs025,gfs_seamless')

JSON_SOURCES = [
    ('nws_forecast', 'https://api.weather.gov/gridpoints/OUN/97,94/forecast', API_UA),
    ('openmeteo_models', OPEN_METEO_URL, API_UA),
    ('obs_kokc', 'https://api.weather.gov/stations/KOKC/observations/latest', API_UA),
    ('obs_kpwa', 'https://api.weather.gov/stations/KPWA/observations/latest', API_UA),
    ('obs_ktik', 'https://api.weather.gov/stations/KTIK/observations/latest', API_UA),
    ('obs_koun', 'https://api.weather.gov/stations/KOUN/observations/latest', API_UA),
]

HTML_SOURCES = [
    ('koco', 'https://www.koco.com/weather', BROWSER_UA),
    ('news9', 'https://www.news9.com/weather', BROWSER_UA),
    ('okcfox', 'https://okcfox.com/weather', BROWSER_UA),
    ('kfor', 'https://kfor.com/weather/', BROWSER_UA),  # 403s as of 2026-07-08; keep trying
]

CLI_INDEX_URL = 'https://api.weather.gov/products/types/CLI/locations/OKC'


def fetch(url: str, ua: str) -> tuple[bytes, int, str]:
    req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept': '*/*'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read(), resp.status, resp.headers.get('Content-Type') or ''


def capture(out_dir: Path, name: str, url: str, ua: str, gz: bool) -> dict:
    meta = {'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    try:
        body, status, ctype = fetch(url, ua)
        meta.update(status=status, content_type=ctype, bytes=len(body),
                    sha256=hashlib.sha256(body).hexdigest())
        if gz:
            meta['file'] = f'{name}.html.gz'
            (out_dir / meta['file']).write_bytes(gzip.compress(body, 9))
        else:
            json.loads(body)
            meta['file'] = f'{name}.json'
            (out_dir / meta['file']).write_bytes(body)
    except Exception as e:  # noqa: BLE001 — one bad source must not kill the run
        meta['error'] = f'{type(e).__name__}: {e}'
    return meta


def capture_cli_reports(out_dir: Path) -> dict:
    """Fetch the 2 most recent official CLI daily climate reports for OKC."""
    meta = {'url': CLI_INDEX_URL, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    try:
        body, status, _ = fetch(CLI_INDEX_URL, API_UA)
        index = json.loads(body)
        products = []
        for entry in (index.get('@graph') or [])[:2]:
            pbody, _, _ = fetch(f"https://api.weather.gov/products/{entry['id']}", API_UA)
            products.append(json.loads(pbody))
        meta.update(status=status, file='nws_cli_okc.json', count=len(products))
        (out_dir / 'nws_cli_okc.json').write_text(json.dumps(products, indent=2))
    except Exception as e:  # noqa: BLE001
        meta['error'] = f'{type(e).__name__}: {e}'
    return meta


def main() -> int:
    now_local = datetime.now(CENTRAL)
    out_dir = BASE / 'captures' / now_local.strftime('%Y-%m-%d_%H%M')
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        'captured_at_utc': datetime.now(timezone.utc).isoformat(),
        'captured_at_central': now_local.isoformat(),
        'sources': {},
    }
    for name, url, ua in JSON_SOURCES:
        manifest['sources'][name] = capture(out_dir, name, url, ua, gz=False)
    manifest['sources']['nws_cli_okc'] = capture_cli_reports(out_dir)
    for name, url, ua in HTML_SOURCES:
        manifest['sources'][name] = capture(out_dir, name, url, ua, gz=True)

    (out_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    ok = [n for n, m in manifest['sources'].items() if 'error' not in m]
    failed = [n for n, m in manifest['sources'].items() if 'error' in m]
    print(f'{out_dir.name}: {len(ok)} ok, {len(failed)} failed'
          + (f' ({", ".join(failed)})' if failed else ''))
    # The run is useful iff the robot baselines landed.
    return 0 if 'nws_forecast' in ok and 'openmeteo_models' in ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
