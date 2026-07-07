#!/usr/bin/env python3
"""THE DAILY MOG — live generator.

Fetches every live data point at run time (weather/sun/UV/AQI, crypto +
commodity prices, Fear & Greed, news RSS) and computes the rest locally
(moon phase, daylight trend) — no source, no number, same truth-harness
rule as the Boring Report. Rendering is shared with the mockup via
daily_mog_layout.py so the two can never visually diverge.

Usage: python3 generate_daily_mog.py [out_path]
Default out_path: ~/COMMANDER/THE_DAILY_MOG.pdf

NOTE: this only generates the PDF. It does not print. Printing stays a
separate, explicit step until Josh gives a one-time "yes, auto-print this"
for boot automation (see projects/daily-mog-print-handoff.md).
"""
import datetime
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    # some Python installs (notably python.org builds on macOS) ship without
    # a linked system CA bundle; point at certifi's if available rather than
    # requiring a one-time sudo cert-install step. Harmless no-op elsewhere.
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_mog_layout import (
    render, pick, FACT_BANK, BABY_TIP_BANK, ON_THIS_DAY_BANK, EPIGRAPH_BANK,
    WORD_OF_DAY_BANK, ARCANA_BANK,
)

COMMANDER_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = str(COMMANDER_ROOT / "THE_DAILY_MOG.pdf")  # portable — was
                                                        # hardcoded to a Mac
                                                        # path, would have
                                                        # silently failed on
                                                        # the Pi
GATES_PATH = COMMANDER_ROOT / "gates" / "pending.json"
UA = "DailyMogGenerator/1.0 (+local personal print artifact; no scraping at scale)"
TIMEOUT = 15
OKC_LAT, OKC_LON = 35.4676, -97.5164
MAX_DECIDE_CTX_CHARS = 150
MAX_DECIDE_TITLE_CHARS = 48  # unbounded gate titles could wrap the amber
                              # box to 3 lines in the narrower golden-ratio
                              # column —48 was verified (not guessed) to
                              # hold at 2 lines worst-case via stress test
MAX_HN_CHARS = 55       # HN Top shares its line with "(pts, comments)"
MAX_MOVER_NAME_CHARS = 30

WMO_DESC = {
    0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Foggy",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Rain showers", 82: "Violent rain showers",
    95: "Thunderstorms", 96: "Thunderstorms w/ hail", 99: "Thunderstorms w/ hail",
}


class SourceFailure(Exception):
    """Raised when a data source can't be fetched — caller decides fallback."""


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        raise SourceFailure(str(exc)[:200]) from exc


def fetch_json(url, headers=None):
    try:
        return json.loads(fetch(url, headers).decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise SourceFailure(f"bad JSON: {exc}") from exc


# --- moon phase (computed locally, no API — real synodic-month math) ---
SYNODIC_MONTH = 29.530588861
# a known new moon reference: 2000-01-06 18:14 UTC
_REF_NEW_MOON = datetime.datetime(2000, 1, 6, 18, 14)

MOON_PHASE_NAMES = [
    (0.033, "New Moon"), (0.216, "Waxing Crescent"), (0.283, "First Quarter"),
    (0.467, "Waxing Gibbous"), (0.533, "Full Moon"), (0.716, "Waning Gibbous"),
    (0.783, "Last Quarter"), (0.967, "Waning Crescent"), (1.001, "New Moon"),
]


def moon_phase_fraction(dt):
    """0 = new moon, 0.5 = full moon, approaching 1 = next new moon."""
    days = (dt - _REF_NEW_MOON).total_seconds() / 86400.0
    return (days % SYNODIC_MONTH) / SYNODIC_MONTH


def moon_phase_name(frac):
    for cutoff, name in MOON_PHASE_NAMES:
        if frac < cutoff:
            return name
    return "New Moon"


def moon_illumination_pct(frac):
    return round((1 - math.cos(2 * math.pi * frac)) / 2 * 100)


def next_full_moon(dt):
    frac = moon_phase_fraction(dt)
    days_to_full = ((0.5 - frac) % 1.0) * SYNODIC_MONTH
    target = dt + datetime.timedelta(days=days_to_full)
    return target.date()


# --- weather / sun / UV (Open-Meteo, keyless) ---
def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={OKC_LAT}&longitude={OKC_LON}"
        "&daily=temperature_2m_max,temperature_2m_min,weathercode,sunrise,"
        "sunset,uv_index_max,precipitation_probability_max"
        "&current=temperature_2m,weathercode,wind_speed_10m"
        "&past_days=1&forecast_days=1"
        "&timezone=America%2FChicago&temperature_unit=fahrenheit"
        "&wind_speed_unit=mph"
    )
    data = fetch_json(url)
    daily = data["daily"]
    # past_days=1 + forecast_days=1 → index 0 = yesterday, index 1 = today
    return {
        "network_now": data["current"]["time"],  # America/Chicago local time,
                                                   # per the timezone= param —
                                                   # ground truth independent
                                                   # of the local system clock
        "current_temp": data["current"]["temperature_2m"],
        "wind_mph": data["current"]["wind_speed_10m"],
        "hi": daily["temperature_2m_max"][1],
        "lo": daily["temperature_2m_min"][1],
        "code": daily["weathercode"][1],
        "precip_prob": daily["precipitation_probability_max"][1],
        "uv_max": daily["uv_index_max"][1],
        "sunrise_today": daily["sunrise"][1],
        "sunset_today": daily["sunset"][1],
        "sunrise_yday": daily["sunrise"][0],
        "sunset_yday": daily["sunset"][0],
    }


def get_air_quality():
    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={OKC_LAT}&longitude={OKC_LON}&current=us_aqi"
        "&timezone=America%2FChicago"
    )
    data = fetch_json(url)
    return data["current"]["us_aqi"]


def aqi_label(aqi):
    # short, bounded-length labels only — a long EPA category name here was
    # the difference between one line and an unwanted wrap in testing. This
    # collapses the "sensitive groups" nuance rather than use an unexplained
    # asterisk with no legend on a one-page almanac.
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 200:
        return "Unhealthy"
    return "Hazardous"


def parse_iso(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M")


def daylight_minutes(sunrise_iso, sunset_iso):
    return int((parse_iso(sunset_iso) - parse_iso(sunrise_iso)).total_seconds() // 60)


# --- crypto (CoinGecko, keyless) ---
def get_crypto_prices():
    ids = "bitcoin,ethereum,chainlink,convex-finance,aerodrome-finance"
    url = (
        "https://api.coingecko.com/api/v3/simple/price?ids=" + ids +
        "&vs_currencies=usd&include_24hr_change=true"
    )
    data = fetch_json(url)
    fmt = {
        "bitcoin": ("BTC", lambda p: f"${p:,.0f}"),
        "ethereum": ("ETH", lambda p: f"${p:,.0f}" if p >= 1000 else f"${p:,.2f}"),
        "chainlink": ("LINK", lambda p: f"${p:,.2f}"),
        "convex-finance": ("CVX", lambda p: f"${p:,.2f}"),
        "aerodrome-finance": ("AERO", lambda p: f"${p:,.2f}"),
    }
    items = []
    for key, (sym, fn) in fmt.items():
        row = data[key]
        items.append((sym, fn(row["usd"]), row["usd_24h_change"] >= 0))
    return items


# --- commodities (Yahoo Finance keyless quote endpoint) ---
def get_commodity(symbol, label, decimals=2):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    data = fetch_json(url, headers={"Accept": "application/json"})
    meta = data["chart"]["result"][0]["meta"]
    price = meta["regularMarketPrice"]
    prev = meta.get("previousClose") or meta.get("chartPreviousClose")
    is_up = prev is None or price >= prev
    return (label, f"${price:,.{decimals}f}", is_up)


# --- Fear & Greed (alternative.me, keyless) ---
def get_fear_greed():
    data = fetch_json("https://api.alternative.me/fng/?limit=1")
    row = data["data"][0]
    return int(row["value"]), row["value_classification"]


def truncate_at_word(text, max_chars):
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars - 1]
    last_space = cut.rfind(" ")
    if last_space > max_chars * 0.6:
        cut = cut[:last_space]
    return cut.rstrip() + "…"


_TAG_OR_ENTITY = re.compile(r"<[^>]+>|&\w+;")


def count_words(*texts):
    """Strips reportlab's inline HTML-ish markup before counting, so tags
    and HTML entities (&#183; etc.) don't inflate the reading-time estimate."""
    total = 0
    for t in texts:
        total += len(_TAG_OR_ENTITY.sub(" ", t).split())
    return total


# --- MARKET NOTES: Hacker News top story + DeFiLlama biggest mover + total
# DeFi TVL trend. Each fetched independently so one failing doesn't take
# the other two down with it (same pattern as get_news()). Returns raw data
# — build() turns it into prose, matching the rest of the page's editorial
# voice instead of a "Label: value" spec-sheet (Josh's call, 2026-07-07). ---
def get_hn_top_story():
    """Returns (title, score, comments)."""
    ids = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")
    if not ids:
        raise SourceFailure("HN topstories list was empty")
    item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{ids[0]}.json")
    title = truncate_at_word((item.get("title") or "").strip(), MAX_HN_CHARS)
    if not title:
        raise SourceFailure("HN top item had no title")
    return title, item.get("score", 0), item.get("descendants", 0)


def get_biggest_tvl_mover():
    """Returns (name, change_1d_pct, tvl_dollars)."""
    protocols = fetch_json("https://api.llama.fi/protocols")
    rows = [p for p in protocols
            if p.get("change_1d") is not None and (p.get("tvl") or 0) > 100_000_000]
    if not rows:
        raise SourceFailure("no protocols matched the TVL/change_1d filter")
    rows.sort(key=lambda p: abs(p["change_1d"]), reverse=True)
    top = rows[0]
    name = truncate_at_word(str(top.get("name", "?")), MAX_MOVER_NAME_CHARS)
    return name, top["change_1d"], top.get("tvl") or 0


def get_tvl_history():
    """Returns (caption_html, [10 daily values in $B, oldest-first])."""
    data = fetch_json("https://api.llama.fi/v2/historicalChainTvl")
    if len(data) < 2:
        raise SourceFailure("historicalChainTvl returned too few points")
    last10 = data[-10:]
    values_b = [row["tvl"] / 1_000_000_000 for row in last10]
    today_tvl, yday_tvl = last10[-1]["tvl"], last10[-2]["tvl"]
    change_pct = (today_tvl - yday_tvl) / yday_tvl * 100 if yday_tvl else 0.0
    caption = (f'DeFi TVL 10d: ${today_tvl / 1_000_000_000:,.1f}B '
               f'({change_pct:+.1f}%)')
    return caption, values_b


# --- Decide box: the real top pending Gate Deck item, not a hardcoded
# placeholder — mirrors generate_dispatch.py's pending_gates() logic exactly,
# so this print artifact and the phone dashboard never disagree on what's
# actually pending ---
def get_top_pending_gate():
    if not GATES_PATH.exists():
        return None
    data = json.loads(GATES_PATH.read_text())
    pending = [g for g in data.get("gates", []) if g.get("status") == "pending"]
    if not pending:
        return None
    top = pending[0]
    title = truncate_at_word(top.get("title", "Untitled"), MAX_DECIDE_TITLE_CHARS)
    return title, truncate_at_word(top.get("context", ""), MAX_DECIDE_CTX_CHARS)


# --- news RSS (proper XML scoping to <item>/<entry> — a naive regex over
# every <title> tag grabs the feed's own channel title, not an article) ---
MAX_HEADLINE_CHARS = 70  # bounds column height regardless of how long a
                          # real headline happens to be — chosen so even 3
                          # worst-case headlines stay at 2 wrapped lines each
                          # (part of the one-page defensive check, verified
                          # by the worst-case stress test, not a guess)


def get_rss_headline(url):
    raw = fetch(url)
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise SourceFailure(f"malformed XML: {exc}") from exc
    item = root.find(".//item")
    if item is None:
        item = root.find(".//{http://www.w3.org/2005/Atom}entry")
    if item is None:
        raise SourceFailure("no <item>/<entry> found in feed")
    title_el = item.find("title")
    if title_el is None:
        title_el = item.find("{http://www.w3.org/2005/Atom}title")
    if title_el is None or not (title_el.text or "").strip():
        raise SourceFailure("item had no title text")
    title = title_el.text.strip()
    if len(title) > MAX_HEADLINE_CHARS:
        cut = title[:MAX_HEADLINE_CHARS - 1]
        last_space = cut.rfind(" ")
        if last_space > MAX_HEADLINE_CHARS * 0.6:  # don't chop too aggressively
            cut = cut[:last_space]
        title = cut.rstrip() + "…"
    return title


def get_news(sources_used=None):
    # all crypto/tech, no local news — Josh's call 2026-07-07 after a grim
    # local headline (a death story) showed up on what's meant to be a
    # pleasant morning read. Three distinct outlets so it's not just one
    # source's slant three times over.
    if sources_used is None:
        sources_used = set()
    news = []
    try:
        news.append(("CRYPTO/TECH",
                      get_rss_headline("https://www.coindesk.com/arc/outboundfeeds/rss")))
        sources_used.add("CoinDesk")
    except SourceFailure:
        pass
    try:
        news.append(("TECH", get_rss_headline("https://techcrunch.com/feed/")))
        sources_used.add("TechCrunch")
    except SourceFailure:
        pass
    try:
        news.append(("CRYPTO", get_rss_headline("https://decrypt.co/feed")))
        sources_used.add("Decrypt")
    except SourceFailure:
        pass
    return news


# --- weather-conditioned flavor text (rule-based on real fetched values,
# not fabricated — small decision table, same spirit as the curated banks) ---
def weather_flavor(temp, wind, precip_prob):
    if precip_prob >= 50:
        return "Grab an umbrella if you're stepping out today."
    if temp >= 95:
        return "Stay hydrated — that's real heat, not almanac flavor text."
    if temp <= 40:
        return "Bundle up. Coffee's doing double duty this morning."
    if wind >= 20:
        return "Hang onto your hat out there — wind's up today."
    if 65 <= temp <= 82 and precip_prob < 30:
        return "Feels like a good porch-coffee morning."
    return "An ordinary Oklahoma day — nothing dramatic on the forecast."


def primoscapes_note(precip_prob, temp):
    if precip_prob >= 50:
        return ("rain's coming — good day to check drainage and skip new "
                "transplants until it clears.")
    if temp >= 95:
        return ("heat stress risk for anything newly planted — water "
                "early, before the sun's fully up.")
    if temp <= 40:
        return "cold enough to hold off on tender transplants tonight."
    return ("soil conditions look workable today — decent window for "
             "general bed prep.")


def build():
    start_time = time.monotonic()
    out_path = sys.argv[1] if len(sys.argv) > 1 else OUT_PATH
    warnings = []
    sources_used = set()  # distinct external services that answered this
                            # run — feeds the honest colophon line, not a
                            # fixed/guessed count

    # --- weather / sun / moon / UV / AQI ---
    try:
        wx = get_weather()
        sources_used.add("Open-Meteo")
    except SourceFailure as exc:
        raise SystemExit(f"FATAL: weather source unavailable, refusing to "
                          f"fabricate — {exc}")

    # Ground truth for "now" is the live weather API's own timestamp, not
    # the local system clock. This Pi has no battery-backed RTC — on boot
    # the clock can hold a stale timestamp from before shutdown until NTP
    # corrects it (root cause of the 2026-07-07 bug: it printed "July 6"
    # content on July 7). The systemd unit now also waits on time-sync.target,
    # but this is the belt-and-suspenders fix at the data layer, independent
    # of OS-level ordering ever regressing.
    now = parse_iso(wx["network_now"])
    local_now = datetime.datetime.now()
    clock_trusted = abs((now - local_now).total_seconds()) <= 3600
    if not clock_trusted:
        warnings.append(
            f"local system clock ({local_now.strftime('%Y-%m-%d %H:%M')}) "
            f"disagrees with the live weather source "
            f"({now.strftime('%Y-%m-%d %H:%M')}) by over an hour — used the "
            f"network time for content, but the printed generation "
            f"timestamp below is degraded to minute precision. Check the "
            f"Pi's NTP sync.")
    today = now.date()
    day_ord = today.toordinal()

    # Generation timestamp: Open-Meteo (the "network_now" ground truth used
    # for date/content selection above) only reports minute precision, so
    # showing fake seconds off it would be exactly the kind of fabricated
    # precision this whole project refuses to do. The local system clock
    # DOES have real second precision, and by this point in the boot
    # sequence it should already be NTP-corrected (see configs/daily-mog.
    # service's time-sync.target wait) — so it's used for display, gated on
    # the same cross-check above. If that check ever fails, this honestly
    # degrades to minute precision instead of pretending to be exact.
    generated_at = (local_now.strftime("%-I:%M:%S %p") if clock_trusted
                     else now.strftime("%-I:%M %p") + " (network time)") + " CT"

    daylight_today = daylight_minutes(wx["sunrise_today"], wx["sunset_today"])
    daylight_yday = daylight_minutes(wx["sunrise_yday"], wx["sunset_yday"])
    trend_min = daylight_today - daylight_yday
    trend_str = f"+{trend_min}m" if trend_min >= 0 else f"{trend_min}m"

    moon_frac = moon_phase_fraction(now)
    moon_name = moon_phase_name(moon_frac)
    moon_pct = moon_illumination_pct(moon_frac)
    full_moon_date = next_full_moon(now)

    sunrise_dt = parse_iso(wx["sunrise_today"])
    sunset_dt = parse_iso(wx["sunset_today"])
    sunrise_disp = sunrise_dt.strftime("%-I:%M %p")
    sunset_disp = sunset_dt.strftime("%-I:%M %p")
    daylight_span = (sunset_dt - sunrise_dt).total_seconds()
    sun_progress_frac = ((now - sunrise_dt).total_seconds() / daylight_span
                          if daylight_span > 0 else 0.5)
    sun_progress_frac = max(0.0, min(1.0, sun_progress_frac))  # clamp for a
                                                                 # pre-dawn or
                                                                 # post-dusk run

    sun_text = (
        f"Sunrise {sunrise_disp} &#183; Sunset {sunset_disp} &#183; "
        f"Daylight {daylight_today // 60}h {daylight_today % 60}m ({trend_str})"
    )
    moon_text = (
        f"{moon_name} {moon_pct}% &#183; Next full moon "
        f"{full_moon_date.strftime('%b %-d')}"
    )

    try:
        aqi = get_air_quality()
        aqi_line = f"UV index {wx['uv_max']:.0f} · Air quality: {aqi_label(aqi)} (AQI {aqi})"
    except SourceFailure as exc:
        warnings.append(f"air quality unavailable: {exc}")
        aqi_line = f"UV index {wx['uv_max']:.0f} · Air quality: unavailable today"
    else:
        sources_used.add("Open-Meteo")

    desc = WMO_DESC.get(wx["code"], "Variable conditions")
    weather_headline = (
        f"<b>{wx['hi']:.0f}°F</b> / {wx['lo']:.0f}°F · {desc}, "
        f"{wx['precip_prob']:.0f}% chance of rain. "
        f"Wind {wx['wind_mph']:.0f}mph. "
        f"{weather_flavor(wx['current_temp'], wx['wind_mph'], wx['precip_prob'])}"
    )

    # --- markets ---
    ticker_items = []
    try:
        ticker_items += get_crypto_prices()
        sources_used.add("CoinGecko")
    except SourceFailure as exc:
        warnings.append(f"CoinGecko unavailable: {exc}")
    try:
        ticker_items.append(get_commodity("SI=F", "SILVER"))
        sources_used.add("Yahoo Finance")
    except SourceFailure as exc:
        warnings.append(f"Silver quote unavailable: {exc}")
    try:
        ticker_items.append(get_commodity("CL=F", "OIL (WTI)", decimals=2))
        sources_used.add("Yahoo Finance")
    except SourceFailure as exc:
        warnings.append(f"Oil quote unavailable: {exc}")
    if len(ticker_items) < 7:
        # pad so the 7-column ticker table doesn't break layout when a
        # source drops — visible placeholder, never a silent fake number
        ticker_items += [("—", "n/a", True)] * (7 - len(ticker_items))

    try:
        fg_value, fg_label = get_fear_greed()
        sources_used.add("alternative.me")
    except SourceFailure as exc:
        warnings.append(f"Fear & Greed unavailable: {exc}")
        fg_value, fg_label = 0, "Neutral"

    news = get_news(sources_used)
    if not news:
        warnings.append("all news RSS sources failed")
        news = [("NOTICE", "News sources unavailable this morning.")]

    gate = get_top_pending_gate()
    if gate:
        decide_title, decide_body = gate
    else:
        decide_title, decide_body = "Nothing pending", "Clear runway — no open gate right now."

    # MARKET NOTES: HN + biggest TVL mover, written as prose (matching the
    # rest of the page's editorial voice), each independent so one failing
    # doesn't blank the whole section — same pattern as get_news()
    sentences = []
    try:
        title, score, comments = get_hn_top_story()
        sentences.append(
            f'Hacker News is buzzing about &#8220;{title}&#8221; '
            f'({score} pts, {comments} comments).')
        sources_used.add("Hacker News")
    except SourceFailure as exc:
        warnings.append(f"Hacker News unavailable: {exc}")
    try:
        name, change, tvl = get_biggest_tvl_mover()
        verb = "up" if change >= 0 else "down"
        sentences.append(
            f"DeFi's biggest mover today is {name}, {verb} "
            f'{abs(change):.1f}% to ${tvl / 1_000_000:,.1f}M locked.')
        sources_used.add("DeFiLlama")
    except SourceFailure as exc:
        warnings.append(f"DeFiLlama mover unavailable: {exc}")
    feature_body = (" ".join(sentences) if sentences else
                     "Market Notes is unavailable this morning — sources didn't respond.")

    try:
        tvl_line, tvl_history = get_tvl_history()
        sources_used.add("DeFiLlama")
    except SourceFailure as exc:
        warnings.append(f"DeFi TVL history unavailable: {exc}")
        tvl_line, tvl_history = "DeFi TVL 10d: unavailable today", []

    otd_year, otd_rest = pick(ON_THIS_DAY_BANK, day_ord).split(":", 1)
    fact = pick(FACT_BANK, day_ord)
    baby_tip = pick(BABY_TIP_BANK, day_ord)
    word_of_day = pick(WORD_OF_DAY_BANK, day_ord)
    arcana = pick(ARCANA_BANK, day_ord)
    ps_note = primoscapes_note(wx["precip_prob"], wx["current_temp"])

    # honest reading-time estimate — a real magazine-footer convention,
    # computed from the actual assembled copy (~200 wpm), not guessed
    reading_words = count_words(
        weather_headline, aqi_line, ps_note, fact, baby_tip,
        word_of_day[0], word_of_day[2],
        " ".join(h for _, h in news[:2]), decide_title, decide_body,
        feature_body, tvl_line, arcana[0], arcana[1])
    reading_minutes = max(1, round(reading_words / 200))

    ctx = {
        "date_str": now.strftime("%A, %B %-d, %Y"),
        "generated_at": generated_at,
        "vol_no": "VOL. 1 &#183; NO. " + str((day_ord % 300) + 1),
        "epigraph": pick(EPIGRAPH_BANK, day_ord),
        "sun_text": sun_text,
        "sun_progress_frac": sun_progress_frac,
        "moon_text": moon_text,
        "moon_phase_frac": moon_frac,
        "ticker_items": ticker_items[:7],
        "fear_greed_value": fg_value,
        "fear_greed_label": fg_label,
        "otd_year": otd_year,
        "otd_rest": otd_rest,
        "weather_headline": weather_headline,
        "uv_aqi_line": aqi_line,
        "primoscapes_note": ps_note,
        "fact": fact,
        "baby_tip": baby_tip,
        "word_of_day": word_of_day,
        "news": news[:2],
        "decide_title": decide_title,
        "decide_body": decide_body,
        "feature_title": "MARKET NOTES",
        "feature_body": feature_body,
        "tvl_line": tvl_line,
        "tvl_history": tvl_history,
        "arcana": arcana,
        # colophon: real, measured facts about this run, not boilerplate —
        # replaces the old flat disclaimer line (Josh's call, 2026-07-07:
        # "that disclaimer or whatever is lame ... I want more info")
        "colophon": (
            f"Assembled from {len(sources_used)} live sources in "
            f"{time.monotonic() - start_time:.1f}s &#183; ~{reading_minutes} "
            f"min read"
            + (f" &#183; {len(warnings)} warning(s)" if warnings else "")
        ),
        # trimmed to just the one rule that actually matters here — Josh's
        # call, 2026-07-07: "none of that is necessary" re: the fuller
        # posting/sending/spending disclaimer
        "safety_note": "No posting.",
    }

    render(ctx, out_path)
    print(f"wrote {out_path}")
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)


if __name__ == "__main__":
    build()
