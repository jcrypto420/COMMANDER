#!/usr/bin/env python3
"""Issue Zero — first real scoreboard, robots-only retroactive grading.

Robots (ECMWF/GFS) are gradeable for the past week because Open-Meteo's
previous-runs API preserves what each model predicted the day before.
Stations + NWS start their clock 2026-07-08 (receipts exist only from
capture start — that is the product's whole thesis).

Inputs (this dir): prevruns_hourly.json (fetched 2026-07-08).
Live fetch: NWS CLI climate reports (official highs) — saved alongside.
Outputs: issue_zero.json (all computed numbers) + the HTML artifact.
"""
from __future__ import annotations

import json
import re
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {'User-Agent': 'weather-oracle-capture/0.1 (stokesberryjosh@gmail.com)', 'Accept': '*/*'}

MONTHS = {m: i for i, m in enumerate(
    ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY',
     'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'], 1)}

GRADE_SCALE = [(1.0, 'A'), (1.5, 'A-'), (2.0, 'B+'), (2.5, 'B'), (3.0, 'B-'),
               (3.5, 'C+'), (4.0, 'C'), (5.0, 'D'), (99.0, 'F')]

# Tomorrow's on-record matchup, from tonight's committed captures.
# KFOR numbers vision-read from the archived 4Warn 7-day graphic.
MATCHUP = [
    ('NWS Norman', 101, 15, 'captures/2026-07-08_2012/nws_forecast.json'),
    ('ECMWF (robot)', 100.3, 37, 'captures/2026-07-08_2012/openmeteo_models.json'),
    ('GFS (robot)', 99.4, 8, 'captures/2026-07-08_2012/openmeteo_models.json'),
    ('KFOR 4Warn', 99, 10, 'captures/2026-07-08_2012/kfor_7day.jpg (vision-read)'),
]


def grade(avg_miss: float) -> str:
    for cutoff, letter in GRADE_SCALE:
        if avg_miss <= cutoff:
            return letter
    return 'F'


def model_daily_max() -> dict:
    data = json.loads((HERE / 'prevruns_hourly.json').read_text())
    hourly = data['hourly']
    out = {}
    for key in hourly:
        if key == 'time':
            continue
        model = 'ECMWF' if 'ecmwf' in key else 'GFS'
        per_day = defaultdict(list)
        for t, v in zip(hourly['time'], hourly[key]):
            if v is not None:
                per_day[t[:10]].append(v)
        out[model] = {d: max(vs) for d, vs in per_day.items() if len(vs) >= 18}
    return out


def official_highs() -> dict:
    idx = json.loads(urllib.request.urlopen(
        urllib.request.Request('https://api.weather.gov/products/types/CLI/locations/OKC',
                               headers=UA), timeout=30).read())
    products = []
    for entry in (idx.get('@graph') or [])[:16]:
        p = json.loads(urllib.request.urlopen(
            urllib.request.Request(f"https://api.weather.gov/products/{entry['id']}",
                                   headers=UA), timeout=30).read())
        products.append(p)
    (HERE / 'cli_products.json').write_text(json.dumps(products, indent=2))

    best = {}  # date -> (issuanceTime, high)
    for p in products:
        text = p.get('productText', '')
        m = re.search(r'CLIMATE SUMMARY FOR ([A-Z]+) (\d{1,2}) (\d{4})', text)
        x = re.search(r'MAXIMUM\s+(\d+)', text)
        if not (m and x):
            continue
        date = f'{int(m.group(3)):04d}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}'
        issued = p.get('issuanceTime', '')
        if date not in best or issued > best[date][0]:
            best[date] = (issued, int(x.group(1)))
    return {d: h for d, (_, h) in best.items()}


def main():
    preds = model_daily_max()
    officials = official_highs()

    days = []
    for date in sorted(officials):
        row = {'date': date, 'official_high': officials[date]}
        for model in ('ECMWF', 'GFS'):
            if date in preds.get(model, {}):
                row[model] = round(preds[model][date], 1)
                row[f'{model}_miss'] = round(preds[model][date] - officials[date], 1)
        if 'ECMWF' in row or 'GFS' in row:
            days.append(row)

    scores = {}
    for model in ('ECMWF', 'GFS'):
        misses = [abs(r[f'{model}_miss']) for r in days if f'{model}_miss' in r]
        biases = [r[f'{model}_miss'] for r in days if f'{model}_miss' in r]
        if misses:
            avg = sum(misses) / len(misses)
            scores[model] = {'days': len(misses), 'avg_abs_miss': round(avg, 1),
                             'bias': round(sum(biases) / len(biases), 1), 'grade': grade(avg)}

    result = {
        'issue': 'zero', 'city': 'OKC (Will Rogers, official)',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'grade_scale': GRADE_SCALE, 'days': days, 'scores': scores,
        'matchup_for': '2026-07-09', 'matchup': MATCHUP,
        'provenance': {
            'model_day1_forecasts': 'previous-runs-api.open-meteo.com (prevruns_hourly.json)',
            'official_highs': 'api.weather.gov CLI products (cli_products.json), latest issuance per date',
        },
    }
    (HERE / 'issue_zero.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(scores, indent=2))
    print(f"{len(days)} graded days; officials for: {', '.join(sorted(officials))}")


if __name__ == '__main__':
    main()
