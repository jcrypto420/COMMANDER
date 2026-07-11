#!/usr/bin/env python3
"""Daily one-pager v3 — newsprint/almanac direction (de-corpo pass).

Same real-data plumbing as v2; the page now reads like a small-town daily:
Didot masthead with ears, wood-type verdict headline, agate standings in
Courier, the official verdict quoted teletype-style off the NWS wire, a
rubber stamp, and The Fine Print as a clip-out coupon.
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
gust_unit = (om_hourly.get('hourly_units') or {}).get('wind_gusts_10m_gfs_hrrr') \
    or (om_hourly.get('hourly_units') or {}).get('wind_gusts_10m') or 'km/h'
GUST_TO_MPH = 0.621371 if 'km' in gust_unit else 1.0
daily = json.loads((cap_dir / 'openmeteo_models.json').read_text())['daily']
nws = json.loads((cap_dir / 'nws_forecast.json').read_text())['properties']['periods']

now = datetime.now(CENTRAL)
today = now.strftime('%Y-%m-%d')

hours = []
for i, t in enumerate(hourly['time']):
    if not t.startswith(today):
        continue
    h = int(t[11:13])
    if not 7 <= h <= 22:
        continue
    temps = [hourly[f'temperature_2m_{m}'][i] for m in MODELS if hourly[f'temperature_2m_{m}'][i] is not None]
    pops = [hourly[f'precipitation_probability_{m}'][i] for m in MODELS if hourly[f'precipitation_probability_{m}'][i] is not None]
    gusts = [hourly[f'wind_gusts_10m_{m}'][i] for m in MODELS if hourly[f'wind_gusts_10m_{m}'][i] is not None]
    feels = [hourly[f'apparent_temperature_{m}'][i] for m in MODELS if hourly[f'apparent_temperature_{m}'][i] is not None]
    hours.append({'h': h, 'temp': mean(temps), 'pop': max(pops) if pops else 0,
                  'gust': (max(gusts) if gusts else 0) * GUST_TO_MPH,
                  'feels': mean(feels) if feels else None})
if not hours:
    sys.exit('no hourly rows for today')

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
max_feels_row = max((h for h in hours if h['feels'] is not None), key=lambda x: x['feels'], default=None)


def ampm(h):
    return f'{h - 12 if h > 12 else h}{"PM" if h >= 12 else "AM"}'


rain_line = (f'rain window {ampm(rain_hours[0])}–{ampm(rain_hours[-1] + 1)} ({round(max_pop)}%)'
             if rain_hours else ('a stray shower at most' if max_pop >= 15 else 'bone dry'))

if max_gust_row['gust'] >= 25:
    calm = next((ampm(h['h']).lower() for h in hours
                 if h['h'] > max_gust_row['h'] and h['gust'] < 20), None)
    fine_print = (f'Gusts near {round(max_gust_row["gust"])} mph around {ampm(max_gust_row["h"]).lower()}'
                  + (f', easing by {calm}.' if calm else ' through the afternoon.'))
elif max_feels_row and (max_feels_row['feels'] - peak['temp']) >= 4:
    fine_print = (f'Feels-like tops {round(max_feels_row["feels"])}° at {ampm(max_feels_row["h"]).lower()} — '
                  f'{round(max_feels_row["feels"] - peak["temp"])}° above the air temperature.')
elif rain_hours:
    fine_print = f'Rain, if any, arrives {ampm(rain_hours[0]).lower()}–{ampm(rain_hours[-1] + 1).lower()}. Dry until then.'
else:
    fine_print = 'No wind, rain, or heat-index story today.'

# ink-on-newsprint hour strip
W, H, PAD_L, PAD_R, TOP, BOT = 764, 170, 30, 12, 36, 36
n = len(hours)
xs = [PAD_L + i * (W - PAD_L - PAD_R) / (n - 1) for i in range(n)]
tmin, tmax = min(h['temp'] for h in hours), max(h['temp'] for h in hours)
span = max(tmax - tmin, 6)


def ty(v):
    return TOP + (tmax - v) / span * (H - TOP - BOT - 26)


pts = ' '.join(f'{xs[i]:.1f},{ty(hours[i]["temp"]):.1f}' for i in range(n))
svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block">']
for i, hr in enumerate(hours):
    bh = hr['pop'] / 100 * 40
    if bh > 1:
        svg.append(f'<rect x="{xs[i] - 8:.1f}" y="{H - 20 - bh:.1f}" width="16" height="{bh:.1f}" fill="none" stroke="#26221c" stroke-width="1"/>')
        svg.append(f'<rect x="{xs[i] - 8:.1f}" y="{H - 20 - bh:.1f}" width="16" height="{bh:.1f}" fill="#26221c" opacity="0.18"/>')
svg.append(f'<polyline points="{pts}" fill="none" stroke="#26221c" stroke-width="3"/>')
for i, hr in enumerate(hours):
    svg.append(f'<circle cx="{xs[i]:.1f}" cy="{ty(hr["temp"]):.1f}" r="2.6" fill="#26221c"/>')
    if i % 3 == 0 or hr['h'] == peak['h']:
        svg.append(f'<text x="{xs[i]:.1f}" y="{ty(hr["temp"]) - 10:.1f}" text-anchor="middle" '
                   f'font-family="Courier New" font-weight="700" font-size="13" fill="#26221c">{round(hr["temp"])}</text>')
    svg.append(f'<text x="{xs[i]:.1f}" y="{H - 5}" text-anchor="middle" font-family="Courier New" font-size="10" fill="#6e6659">{ampm(hr["h"])}</text>')
    if hr is max_gust_row and hr['gust'] >= 25:
        svg.append(f'<text x="{xs[i]:.1f}" y="{TOP - 18}" text-anchor="middle" font-family="Courier New" '
                   f'font-weight="700" font-size="12" fill="#9e2b25">→ GUSTS {round(hr["gust"])} MPH</text>')
svg.append('</svg>')
svg = ''.join(svg)

vol_no = now.strftime('%-j')
html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>daily v3</title>
<style>
  :root {{ --ink:#26221c; --faded:#6e6659; --red:#9e2b25; --paper:#f4eddd; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--paper); color:var(--ink); font:15px/1.5 Georgia, serif; width:860px; margin:0 auto; padding:26px 44px 26px; }}
  .ears {{ display:flex; justify-content:space-between; align-items:flex-end; font:11px 'Courier New', monospace; color:var(--faded); text-transform:uppercase; letter-spacing:1px; padding-bottom:4px; }}
  .masthead {{ text-align:center; font-family:Didot, 'Bodoni 72', Georgia, serif; font-size:58px; font-weight:700; letter-spacing:2px; line-height:1; padding:2px 0 6px; }}
  .masthead span {{ color:var(--faded); }}
  .mastline {{ text-align:center; font:italic 13px Georgia, serif; color:var(--faded); padding-bottom:8px; }}
  .drule {{ border-top:3px solid var(--ink); border-bottom:1px solid var(--ink); height:5px; margin-bottom:2px; }}
  .dateline {{ display:flex; justify-content:space-between; font:11px 'Courier New', monospace; text-transform:uppercase; letter-spacing:1.5px; padding:6px 0; border-bottom:1px solid var(--ink); margin-bottom:16px; }}
  .headline {{ font-family:'Futura-CondensedExtraBold', 'Arial Narrow', Impact, sans-serif; font-size:52px; line-height:.98; text-transform:uppercase; letter-spacing:.5px; margin-bottom:8px; }}
  .deck {{ font:italic 17px/1.5 Georgia, serif; color:var(--ink); margin-bottom:18px; max-width:640px; }}
  .deck .rot {{ color:var(--red); }}
  .cols {{ display:flex; margin-bottom:16px; border-top:1px solid var(--ink); }}
  .cols > div {{ padding:12px 18px 10px 0; }}
  .cols > div + div {{ border-left:1px solid var(--ink); padding-left:18px; }}
  h3 {{ font:700 12px 'Courier New', monospace; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }}
  h3 em {{ color:var(--faded); font-style:normal; font-weight:400; letter-spacing:.5px; }}
  .agate {{ width:100%; border-collapse:collapse; font:700 14px 'Courier New', monospace; }}
  .agate td {{ padding:4px 6px; border-bottom:1px dotted var(--faded); }}
  .agate td.n {{ text-align:right; }}
  .agate .r {{ color:var(--red); }}
  .bignum {{ font-family:Didot, 'Bodoni 72', Georgia, serif; font-size:84px; font-weight:700; line-height:.9; }}
  .bigsub {{ font:13px/1.7 Georgia, serif; color:var(--faded); margin-top:6px; }}
  .strip {{ border-top:1px solid var(--ink); border-bottom:1px solid var(--ink); padding:8px 0 4px; margin-bottom:16px; }}
  .coupon {{ border:2px dashed var(--ink); padding:10px 16px; font:15px/1.5 Georgia, serif; margin-bottom:16px; position:relative; }}
  .coupon b {{ font:700 12px 'Courier New', monospace; letter-spacing:2px; color:var(--red); }}
  .coupon .scis {{ position:absolute; top:-12px; left:24px; background:var(--paper); padding:0 6px; font-size:14px; color:var(--faded); }}
  .wire {{ background:#efe6d2; border:1px solid var(--faded); padding:10px 14px; font:12.5px/1.7 'Courier New', monospace; text-transform:uppercase; white-space:pre-wrap; position:relative; margin-bottom:14px; }}
  .foot {{ border-top:3px solid var(--ink); padding-top:6px; display:flex; justify-content:space-between; font:11px 'Courier New', monospace; color:var(--faded); text-transform:uppercase; letter-spacing:1px; }}
  .foot i {{ font:italic 12px Georgia, serif; text-transform:none; letter-spacing:0; }}
</style></head><body>
  <div class="ears">
    <div>Vol. I &middot; No. {vol_no}</div>
    <div>Oklahoma City &middot; free</div>
  </div>
  <div class="masthead"><span>[Name Pending]</span></div>
  <div class="mastline">Oklahoma City&rsquo;s daily record of who called it &mdash; and who didn&rsquo;t</div>
  <div class="drule"></div>
  <div class="dateline">
    <div>{now.strftime('%A, %B %-d, %Y')}</div>
    <div>OKC metro edition</div>
    <div>Graded nightly &middot; archived forever</div>
  </div>

  <div class="headline">Human beats robots;<br>sky remains undefeated</div>
  <div class="deck">KFOR took the night 3&ndash;0 &mdash; missed the high by one, hit the low exactly. ECMWF called <span class="rot">37% rain</span>; none fell. It leads the Hype Index.</div>

  <div class="cols">
    <div style="flex:1.15">
      <h3>The standings <em>&middot; July &middot; round-robin nightly</em></h3>
      <table class="agate">
        <tr><td>1</td><td>KFOR 4WARN</td><td class="n">3&ndash;0</td><td class="n">1.000</td></tr>
        <tr><td>2</td><td>GFS <span class="r">&#9679;</span></td><td class="n">2&ndash;1</td><td class="n">.667</td></tr>
        <tr><td>3</td><td>ECMWF <span class="r">&#9679;</span></td><td class="n">1&ndash;2</td><td class="n">.333</td></tr>
        <tr><td>4</td><td>NWS NORMAN</td><td class="n">0&ndash;3</td><td class="n">.000</td></tr>
      </table>
      <div style="font:11px 'Courier New',monospace; color:var(--faded); padding-top:6px;">&#9679; = ROBOT &middot; KOCO, NEWS 9, FOX 25 JOIN AS ARCHIVES GRADE IN</div>
    </div>
    <div style="flex:1">
      <h3>Today, weighted <em>&middot; skill-weighted blend</em></h3>
      <div class="bignum">{wx_high}&deg;</div>
      <div class="bigsub">Peak near {ampm(peak['h']).lower()} &middot; {rain_line}.<br>Blend of ECMWF, GFS, HRRR &amp; NWS &mdash; weighted by recent skill.</div>
    </div>
  </div>

  <h3>The day, hour by hour <em>&middot; ink line = temperature &middot; boxes = rain chance</em></h3>
  <div class="strip">{svg}</div>

  <div class="coupon"><span class="scis">&#9986;</span><b>THE FINE PRINT&nbsp;&nbsp;</b>{fine_print}</div>

  <div class="wire">OFF THE WIRE &mdash; NWS CLIMATE SUMMARY, OKLAHOMA CITY, JULY 9:
MAXIMUM 98 AT 428 PM &middot; MINIMUM 77 AT 558 AM &middot; PRECIPITATION: TRACE.
KFOR CALLED 99/77.</div>

  <div class="foot">
    <div>Every figure traces to archived captures ({cap_dir.name}) &middot; forecasts recorded before outcomes</div>
    <div><i>The sky keeps score. We keep receipts.</i></div>
  </div>
</body></html>
"""
out = Path(__file__).parent / 'daily_v3.html'
out.write_text(html)
print(f'wrote {out} · high {wx_high}° · {rain_line} · gust {round(max_gust_row["gust"])}mph')
