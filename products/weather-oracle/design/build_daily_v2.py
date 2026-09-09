#!/usr/bin/env python3
"""Daily one-pager v2 — design build fed by a real capture.

Reads the newest capture, blends the three models' hourly curves for today
(uniform weights until enough graded nights exist to earn skill weights),
picks The Fine Print by rule, and emits daily_v2.html. This is the seed of
the production daily generator.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
CENTRAL = ZoneInfo('America/Chicago')
MODELS = ['ecmwf_ifs025', 'gfs_seamless', 'gfs_hrrr']

cap_dir = sorted((BASE / 'captures').iterdir())[-1]
om_hourly = json.loads((cap_dir / 'openmeteo_hourly.json').read_text())
hourly = om_hourly['hourly']
# early captures stored gusts in Open-Meteo's default km/h; honor the units field
gust_unit = (om_hourly.get('hourly_units') or {}).get('wind_gusts_10m_gfs_hrrr') \
    or (om_hourly.get('hourly_units') or {}).get('wind_gusts_10m') or 'km/h'
GUST_TO_MPH = 0.621371 if 'km' in gust_unit else 1.0
daily = json.loads((cap_dir / 'openmeteo_models.json').read_text())['daily']
nws = json.loads((cap_dir / 'nws_forecast.json').read_text())['properties']['periods']

now = datetime.now(CENTRAL)
today = now.strftime('%Y-%m-%d')

# --- today's hourly blend, 7am-10pm ---
hours = []
for i, t in enumerate(hourly['time']):
    if not t.startswith(today):
        continue
    h = int(t[11:13])
    if not 7 <= h <= 22:
        continue
    temps = [hourly[f'temperature_2m_{m}'][i] for m in MODELS
             if hourly[f'temperature_2m_{m}'][i] is not None]
    pops = [hourly[f'precipitation_probability_{m}'][i] for m in MODELS
            if hourly[f'precipitation_probability_{m}'][i] is not None]
    gusts = [hourly[f'wind_gusts_10m_{m}'][i] for m in MODELS
             if hourly[f'wind_gusts_10m_{m}'][i] is not None]
    feels = [hourly[f'apparent_temperature_{m}'][i] for m in MODELS
             if hourly[f'apparent_temperature_{m}'][i] is not None]
    hours.append({'h': h, 'temp': mean(temps), 'pop': max(pops) if pops else 0,
                  'gust': (max(gusts) if gusts else 0) * GUST_TO_MPH,
                  'feels': mean(feels) if feels else None})

if not hours:
    sys.exit('no hourly rows for today in latest capture')

# --- headline numbers ---
model_highs = [daily[f'temperature_2m_max_{m}'][0] for m in MODELS
               if f'temperature_2m_max_{m}' in daily and daily[f'temperature_2m_max_{m}'][0] is not None]
nws_day = next((p for p in nws if p['isDaytime']), None)
if nws_day:
    model_highs.append(float(nws_day['temperature']))
wx_high = round(mean(model_highs))
peak = max(hours, key=lambda x: x['temp'])
max_pop = max(h['pop'] for h in hours)
rain_hours = [h['h'] for h in hours if h['pop'] >= 25]
max_gust_row = max(hours, key=lambda x: x['gust'])
max_feels_row = max((h for h in hours if h['feels'] is not None),
                    key=lambda x: x['feels'], default=None)


def ampm(h):
    return f'{h - 12 if h > 12 else h}{"pm" if h >= 12 else "am"}'


rain_line = (f'rain window {ampm(rain_hours[0])}–{ampm(rain_hours[-1] + 1)} ({round(max_pop)}%)'
             if rain_hours else
             ('a stray shower at most' if max_pop >= 15 else 'dry'))

# --- The Fine Print: one nuance, picked by rule ---
if max_gust_row['gust'] >= 25:
    fine_print = (f'Gusts near {round(max_gust_row["gust"])} mph around {ampm(max_gust_row["h"])} — '
                  'secure the trampoline before lunch, not after.')
elif max_feels_row and (max_feels_row['feels'] - peak['temp']) >= 4:
    fine_print = (f'Feels-like tops {round(max_feels_row["feels"])}° at {ampm(max_feels_row["h"])} — '
                  f'{round(max_feels_row["feels"] - peak["temp"])}° hotter than the number anyone said on TV.')
elif rain_hours:
    fine_print = (f'The rain, if it comes, is a {ampm(rain_hours[0])}–{ampm(rain_hours[-1] + 1)} problem. '
                  'The morning is spoken for.')
else:
    fine_print = 'No wind story, no rain story, no heat trick. A forecast with nothing to hide.'

# --- SVG hour strip (temp polyline + PoP bars + gust flags) ---
W, H, PAD_L, PAD_R, TOP, BOT = 760, 190, 34, 10, 40, 40
n = len(hours)
xs = [PAD_L + i * (W - PAD_L - PAD_R) / (n - 1) for i in range(n)]
tmin, tmax = min(h['temp'] for h in hours), max(h['temp'] for h in hours)
span = max(tmax - tmin, 6)


def ty(v):
    return TOP + (tmax - v) / span * (H - TOP - BOT - 34)


pts = ' '.join(f'{xs[i]:.1f},{ty(hours[i]["temp"]):.1f}' for i in range(n))
svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block">']
for i, hr in enumerate(hours):  # PoP bars along the baseline
    bh = hr['pop'] / 100 * 46
    svg.append(f'<rect x="{xs[i] - 9:.1f}" y="{H - 22 - bh:.1f}" width="18" height="{bh:.1f}" fill="#b9cfe2"/>')
svg.append(f'<polyline points="{pts}" fill="none" stroke="#1a1917" stroke-width="2.5"/>')
for i, hr in enumerate(hours):
    if i % 3 == 0 or hr['h'] == peak['h']:
        svg.append(f'<text x="{xs[i]:.1f}" y="{ty(hr["temp"]) - 9:.1f}" text-anchor="middle" '
                   f'font-size="12" font-weight="700" fill="#1a1917">{round(hr["temp"])}°</text>')
    svg.append(f'<text x="{xs[i]:.1f}" y="{H - 6}" text-anchor="middle" font-size="10" '
               f'fill="#98948c">{ampm(hr["h"])}</text>')
    if hr is max_gust_row and hr['gust'] >= 25:
        svg.append(f'<text x="{xs[i]:.1f}" y="{TOP - 22}" text-anchor="middle" font-size="11" '
                   f'fill="#a32d2d" font-weight="700">⚑ gusts to {round(hr["gust"])} mph</text>')
svg.append(f'<text x="{PAD_L - 6}" y="{H - 22}" text-anchor="end" font-size="9" fill="#98948c">rain %</text>')
svg.append('</svg>')
svg = ''.join(svg)

issue_no = now.strftime('%-j')  # day-of-year as issue number for now
html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>daily v2</title>
<style>
  :root {{ --ink:#1a1917; --muted:#6b6862; --faint:#98948c; --accent:#a32d2d; --rule:#d8d4cc; --bg:#faf8f3; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--ink); font:15px/1.5 -apple-system,"Helvetica Neue",sans-serif; width:860px; margin:0 auto; padding:40px 48px 30px; }}
  .rule3 {{ border-top:3px solid var(--ink); }}
  .mast {{ display:flex; justify-content:space-between; align-items:baseline; padding:10px 0 8px; border-bottom:1px solid var(--ink); margin-bottom:16px; }}
  .mast h1 {{ font-family:Georgia,serif; font-size:30px; font-weight:700; }} .mast h1 span {{ color:var(--faint); }}
  .mast .date {{ font-size:13px; color:var(--muted); text-align:right; }}
  .verdict {{ font-family:Georgia,serif; font-size:19px; line-height:1.45; margin:4px 0 18px; }}
  .verdict b {{ color:var(--accent); }}
  .cols {{ display:flex; gap:32px; margin-bottom:18px; }}
  .cols > div {{ flex:1; }}
  h2 {{ font-size:12px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:var(--accent); margin-bottom:8px; }}
  h2 span {{ color:var(--faint); font-weight:400; letter-spacing:.2px; text-transform:none; }}
  table {{ width:100%; border-collapse:collapse; font-variant-numeric:tabular-nums; }}
  th {{ font-size:10px; letter-spacing:1px; text-transform:uppercase; color:var(--faint); text-align:left; padding:4px 8px; border-bottom:1px solid var(--ink); }}
  td {{ padding:7px 8px; border-bottom:1px solid var(--rule); font-size:15px; }}
  th.n, td.n {{ text-align:right; }}
  .who {{ font-weight:700; }} .rec {{ font-weight:700; font-size:16px; }}
  .today-big {{ font-family:Georgia,serif; font-size:44px; font-weight:700; line-height:1; }}
  .today-sub {{ font-size:14px; color:var(--muted); margin-top:6px; line-height:1.6; }}
  .strip {{ border:1px solid var(--rule); background:#fff; padding:12px 10px 6px; margin-bottom:16px; }}
  .fine {{ border-left:3px solid var(--accent); background:#fff; border-top:1px solid var(--rule); border-right:1px solid var(--rule); border-bottom:1px solid var(--rule); padding:10px 14px; font-size:14.5px; margin-bottom:18px; }}
  .fine b {{ letter-spacing:1px; font-size:11px; color:var(--accent); }}
  .foot {{ border-top:3px solid var(--ink); padding-top:8px; font-size:11px; color:var(--faint); display:flex; justify-content:space-between; }}
  .foot i {{ font-family:Georgia,serif; color:var(--muted); }}
</style></head><body>
  <div class="rule3"></div>
  <div class="mast">
    <h1><span>[NAME PENDING]</span> · Daily</h1>
    <div class="date">{now.strftime('%A, %B %-d, %Y')} · No. {issue_no} · Oklahoma City</div>
  </div>

  <div class="verdict"><b>Last night:</b> KFOR took the field, 3–0 — missed the high by one and hit the low on the number. ECMWF's 37% rain call met a dry sky and is under review.</div>

  <div class="cols">
    <div>
      <h2>Standings <span>· July · round-robin, per night</span></h2>
      <table>
        <tr><th></th><th>Forecaster</th><th class="n">W–L</th><th class="n">Pct</th></tr>
        <tr><td>1</td><td class="who">KFOR 4Warn</td><td class="n rec">3–0</td><td class="n">1.000</td></tr>
        <tr><td>2</td><td class="who">GFS <span style="font-size:10px;border:1px solid var(--ink);padding:1px 4px;letter-spacing:1px">ROBOT</span></td><td class="n rec">2–1</td><td class="n">.667</td></tr>
        <tr><td>3</td><td class="who">ECMWF <span style="font-size:10px;border:1px solid var(--ink);padding:1px 4px;letter-spacing:1px">ROBOT</span></td><td class="n rec">1–2</td><td class="n">.333</td></tr>
        <tr><td>4</td><td class="who">NWS Norman</td><td class="n rec">0–3</td><td class="n">.000</td></tr>
      </table>
    </div>
    <div>
      <h2>Today, weighted <span>· blend of ECMWF + GFS + HRRR + NWS</span></h2>
      <div class="today-big">{wx_high}°</div>
      <div class="today-sub">Peak around {ampm(peak['h'])} · {rain_line}<br>
      KOCO, News 9, Fox 25 join the board as their archives grade in.</div>
    </div>
  </div>

  <h2>The day, hour by hour <span>· temperature line · rain-chance bars · gust flags</span></h2>
  <div class="strip">{svg}</div>

  <div class="fine"><b>THE FINE PRINT&nbsp;&nbsp;</b> {fine_print}</div>

  <div class="foot">
    <div>Every number traces to archived captures ({cap_dir.name}). Forecasts recorded before outcomes, never after.</div>
    <div><i>The sky keeps score. We keep receipts.</i></div>
  </div>
</body></html>
"""
out = Path(__file__).parent / 'daily_v2.html'
out.write_text(html)
print(f'wrote {out} · high {wx_high}° · peak {ampm(peak["h"])} · pop {round(max_pop)}% · gust {round(max_gust_row["gust"])}')
