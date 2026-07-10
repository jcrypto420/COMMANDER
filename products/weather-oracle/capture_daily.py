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
- KFOR 4Warn broadcast 7-day graphic (JPEG) — the meteorology team's own
  published forecast at a stable URL; numbers extracted at grading time
  (vision pass), the archived image is the receipt.

Every source is independent — one failure never kills the run. The manifest
records status/bytes/sha256 per source; grading must only ever use numbers
traceable to these files.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent
CENTRAL = ZoneInfo('America/Chicago')

API_UA = 'weather-oracle-capture/0.1 (forecast accountability research; stokesberryjosh@gmail.com)'
BROWSER_UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')

# kfor.com 403s plain requests; this fingerprint set gets a 200 (verified
# 2026-07-08). Referer + sec-ch-ua/sec-fetch are the load-bearing headers.
BROWSER_HEADERS = {
    'User-Agent': BROWSER_UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


def ua_headers(ua: str) -> dict:
    return {'User-Agent': ua, 'Accept': '*/*'}

OKC = 'latitude=35.4676&longitude=-97.5164'
OPEN_METEO_URL = ('https://api.open-meteo.com/v1/forecast?' + OKC +
                  '&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max'
                  '&temperature_unit=fahrenheit&timezone=America%2FChicago&forecast_days=3'
                  '&models=ecmwf_ifs025,gfs_seamless')
# Hourly per model — feeds the trust-weighted "today" curve (rain windows,
# gust flags, heat index). HRRR (gfs_hrrr) is the short-range timing model.
OPEN_METEO_HOURLY_URL = (
    'https://api.open-meteo.com/v1/forecast?' + OKC +
    '&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,wind_gusts_10m'
    '&temperature_unit=fahrenheit&timezone=America%2FChicago&forecast_days=3'
    '&models=ecmwf_ifs025,gfs_seamless,gfs_hrrr')

JSON_SOURCES = [
    ('nws_forecast', 'https://api.weather.gov/gridpoints/OUN/97,94/forecast', API_UA),
    ('nws_forecast_hourly', 'https://api.weather.gov/gridpoints/OUN/97,94/forecast/hourly', API_UA),
    ('openmeteo_models', OPEN_METEO_URL, API_UA),
    ('openmeteo_hourly', OPEN_METEO_HOURLY_URL, API_UA),
    ('obs_kokc', 'https://api.weather.gov/stations/KOKC/observations/latest', API_UA),
    ('obs_kpwa', 'https://api.weather.gov/stations/KPWA/observations/latest', API_UA),
    ('obs_ktik', 'https://api.weather.gov/stations/KTIK/observations/latest', API_UA),
    ('obs_koun', 'https://api.weather.gov/stations/KOUN/observations/latest', API_UA),
]

# (name, url, headers-or-None, use_curl). kfor.com's WAF passes curl's
# HTTP/2 + TLS fingerprint but 403s urllib's HTTP/1.1 with identical
# headers (verified 2026-07-08), so that one page fetches via curl.
HTML_SOURCES = [
    ('koco', 'https://www.koco.com/weather', None, False),
    ('news9', 'https://www.news9.com/weather', None, False),
    ('okcfox', 'https://okcfox.com/weather', None, False),
    ('kfor', 'https://kfor.com/weather/', BROWSER_HEADERS, True),
]

# The 4Warn team's actual published 7-day graphic (highs/lows/PoP/wind) —
# the human forecast itself, not a vendor widget.
IMAGE_SOURCES = [
    ('kfor_7day', 'https://media.psg.nexstardigital.net/kfor/weather/7day.jpg', None),
]

CLI_INDEX_URL = 'https://api.weather.gov/products/types/CLI/locations/OKC'


def fetch(url: str, headers: dict) -> tuple[bytes, int, str]:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read(), resp.status, resp.headers.get('Content-Type') or ''


def curl_fetch(url: str, headers: dict) -> tuple[bytes, int, str]:
    cmd = ['curl', '-sS', '-L', '-m', '30', '--compressed',
           '-w', '\n%{http_code}\t%{content_type}']
    for k, v in headers.items():
        cmd += ['-H', f'{k}: {v}']
    result = subprocess.run(cmd + [url], capture_output=True, timeout=45, check=True)
    body, _, trailer = result.stdout.rpartition(b'\n')
    status_s, _, ctype = trailer.decode(errors='replace').partition('\t')
    return body, int(status_s), ctype


def capture(out_dir: Path, name: str, url: str, headers: dict, kind: str,
            use_curl: bool = False, retries: int = 1) -> dict:
    meta = {'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    for attempt in range(1, retries + 1):
        try:
            body, status, ctype = (curl_fetch if use_curl else fetch)(url, headers)
            if status >= 400:
                raise ValueError(f'HTTP {status}')
            meta.update(status=status, content_type=ctype, bytes=len(body),
                        sha256=hashlib.sha256(body).hexdigest())
            if kind == 'html':
                meta['file'] = f'{name}.html.gz'
                (out_dir / meta['file']).write_bytes(gzip.compress(body, 9))
            elif kind == 'image':
                if not ctype.startswith('image/'):
                    raise ValueError(f'expected image, got {ctype}')
                meta['file'] = f'{name}.jpg'
                (out_dir / meta['file']).write_bytes(body)
            else:
                json.loads(body)
                meta['file'] = f'{name}.json'
                (out_dir / meta['file']).write_bytes(body)
            meta.pop('error', None)
            break
        except Exception as e:  # noqa: BLE001 — one bad source must not kill the run
            meta['error'] = f'{type(e).__name__}: {e}'
            if attempt < retries:
                time.sleep(20)  # station WAFs (kfor) block intermittently; one cool-down retry
    return meta


def capture_cli_reports(out_dir: Path) -> dict:
    """Fetch the 2 most recent official CLI daily climate reports for OKC."""
    meta = {'url': CLI_INDEX_URL, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    try:
        body, status, _ = fetch(CLI_INDEX_URL, ua_headers(API_UA))
        index = json.loads(body)
        products = []
        for entry in (index.get('@graph') or [])[:2]:
            pbody, _, _ = fetch(f"https://api.weather.gov/products/{entry['id']}", ua_headers(API_UA))
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
        manifest['sources'][name] = capture(out_dir, name, url, ua_headers(ua), kind='json')
    manifest['sources']['nws_cli_okc'] = capture_cli_reports(out_dir)
    for name, url, hdrs, use_curl in HTML_SOURCES:
        manifest['sources'][name] = capture(out_dir, name, url, hdrs or ua_headers(BROWSER_UA),
                                            kind='html', use_curl=use_curl, retries=2)
    for name, url, hdrs in IMAGE_SOURCES:
        manifest['sources'][name] = capture(out_dir, name, url, hdrs or ua_headers(BROWSER_UA),
                                            kind='image', retries=2)

    (out_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    ok = [n for n, m in manifest['sources'].items() if 'error' not in m]
    failed = [n for n, m in manifest['sources'].items() if 'error' in m]
    print(f'{out_dir.name}: {len(ok)} ok, {len(failed)} failed'
          + (f' ({", ".join(failed)})' if failed else ''))
    # The run is useful iff the robot baselines landed.
    return 0 if 'nws_forecast' in ok and 'openmeteo_models' in ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
