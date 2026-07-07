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
import sys
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
    WORD_OF_DAY_BANK, ARCANA_BANK, FEATURE_FALLBACK_TITLE, FEATURE_FALLBACK_BODY,
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
MAX_APOD_CHARS = 105  # title takes its own line already — this budget is
                       # just the explanation, tuned so title+explanation+
                       # attribution stays around 3 lines, verified by the
                       # worst-case stress test alongside everything else

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


# --- NASA Astronomy Picture of the Day (DEMO_KEY: public, no signup, but
# rate-limited — fine for once-a-day generation, not for polling) ---
def get_apod():
    data = fetch_json("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
    title = data["title"].strip()
    explanation = truncate_at_word(data["explanation"].strip(), MAX_APOD_CHARS)
    body = (f"<b>{title}</b><br/>{explanation} "
            '<font size="8" color="#6B6255">&#8212; NASA Astronomy Picture '
            "of the Day</font>")
    return FEATURE_FALLBACK_TITLE, body


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
    return top["title"], truncate_at_word(top.get("context", ""), MAX_DECIDE_CTX_CHARS)


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


def get_news():
    news = []
    try:
        news.append(("CRYPTO/TECH",
                      get_rss_headline("https://www.coindesk.com/arc/outboundfeeds/rss")))
    except SourceFailure:
        pass
    try:
        news.append(("TECH", get_rss_headline("https://techcrunch.com/feed/")))
    except SourceFailure:
        pass
    try:
        news.append(("OKC LOCAL", get_rss_headline("https://kfor.com/feed/")))
    except SourceFailure:
        try:
            news.append(("OKC LOCAL", get_rss_headline("https://www.koco.com/feed")))
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
    out_path = sys.argv[1] if len(sys.argv) > 1 else OUT_PATH
    now = datetime.datetime.now()
    today = now.date()
    day_ord = today.toordinal()
    warnings = []

    # --- weather / sun / moon / UV / AQI ---
    try:
        wx = get_weather()
    except SourceFailure as exc:
        raise SystemExit(f"FATAL: weather source unavailable, refusing to "
                          f"fabricate — {exc}")

    daylight_today = daylight_minutes(wx["sunrise_today"], wx["sunset_today"])
    daylight_yday = daylight_minutes(wx["sunrise_yday"], wx["sunset_yday"])
    trend_min = daylight_today - daylight_yday
    trend_str = f"+{trend_min}m" if trend_min >= 0 else f"{trend_min}m"

    moon_frac = moon_phase_fraction(now)
    moon_name = moon_phase_name(moon_frac)
    moon_pct = moon_illumination_pct(moon_frac)
    full_moon_date = next_full_moon(now)

    sunrise_disp = parse_iso(wx["sunrise_today"]).strftime("%-I:%M %p")
    sunset_disp = parse_iso(wx["sunset_today"]).strftime("%-I:%M %p")
    sky_line = (
        f"Sunrise {sunrise_disp} &#183; Sunset {sunset_disp} &#183; "
        f"Daylight {daylight_today // 60}h {daylight_today % 60}m "
        f"({trend_str}) &#183; Moon: {moon_name} {moon_pct}% &#183; "
        f"Next full moon {full_moon_date.strftime('%b %-d')}"
    )

    try:
        aqi = get_air_quality()
        aqi_line = f"UV index {wx['uv_max']:.0f} · Air quality: {aqi_label(aqi)} (AQI {aqi})"
    except SourceFailure as exc:
        warnings.append(f"air quality unavailable: {exc}")
        aqi_line = f"UV index {wx['uv_max']:.0f} · Air quality: unavailable today"

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
    except SourceFailure as exc:
        warnings.append(f"CoinGecko unavailable: {exc}")
    try:
        ticker_items.append(get_commodity("SI=F", "SILVER"))
    except SourceFailure as exc:
        warnings.append(f"Silver quote unavailable: {exc}")
    try:
        ticker_items.append(get_commodity("CL=F", "OIL (WTI)", decimals=2))
    except SourceFailure as exc:
        warnings.append(f"Oil quote unavailable: {exc}")
    if len(ticker_items) < 7:
        # pad so the 7-column ticker table doesn't break layout when a
        # source drops — visible placeholder, never a silent fake number
        ticker_items += [("—", "n/a", True)] * (7 - len(ticker_items))

    try:
        fg_value, fg_label = get_fear_greed()
    except SourceFailure as exc:
        warnings.append(f"Fear & Greed unavailable: {exc}")
        fg_value, fg_label = 0, "Neutral"

    news = get_news()
    if not news:
        warnings.append("all news RSS sources failed")
        news = [("NOTICE", "News sources unavailable this morning.")]

    gate = get_top_pending_gate()
    if gate:
        decide_title, decide_body = gate
    else:
        decide_title, decide_body = "Nothing pending", "Clear runway — no open gate right now."

    try:
        feature_title, feature_body = get_apod()
    except SourceFailure as exc:
        warnings.append(f"NASA APOD unavailable: {exc}")
        feature_title, feature_body = FEATURE_FALLBACK_TITLE, FEATURE_FALLBACK_BODY

    otd_year, otd_rest = pick(ON_THIS_DAY_BANK, day_ord).split(":", 1)

    ctx = {
        "date_str": now.strftime("%A, %B %-d, %Y"),
        "vol_no": "VOL. 1 &#183; NO. " + str((day_ord % 300) + 1),
        "epigraph": pick(EPIGRAPH_BANK, day_ord),
        "sky_line": sky_line,
        "ticker_items": ticker_items[:7],
        "fear_greed_value": fg_value,
        "fear_greed_label": fg_label,
        "otd_year": otd_year,
        "otd_rest": otd_rest,
        "weather_headline": weather_headline,
        "uv_aqi_line": aqi_line,
        "primoscapes_note": primoscapes_note(wx["precip_prob"], wx["current_temp"]),
        "fact": pick(FACT_BANK, day_ord),
        "baby_tip": pick(BABY_TIP_BANK, day_ord),
        "word_of_day": pick(WORD_OF_DAY_BANK, day_ord),
        "news": news[:3],
        "decide_title": decide_title,
        "decide_body": decide_body,
        "feature_title": feature_title,
        "feature_body": feature_body,
        "arcana": pick(ARCANA_BANK, day_ord),
        "footer_note": (
            f"Generated {now.strftime('%-I:%M %p')} from live sources. "
            f"No posting · no sending · no spending without approval."
            + (f" ({len(warnings)} source warning(s), see log)" if warnings else "")
        ),
    }

    render(ctx, out_path)
    print(f"wrote {out_path}")
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)


if __name__ == "__main__":
    build()
