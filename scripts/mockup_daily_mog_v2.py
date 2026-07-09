#!/usr/bin/env python3
"""V2 layout mockup for THE DAILY MOG — placeholder/sample data only.
Purpose: validate layout + aesthetics before wiring any live data source.
Rendering now lives in daily_mog_layout.py (shared with the live generator,
generate_daily_mog.py) — this file only builds a sample context dict.
"""
import datetime

from daily_mog_layout import (
    render, pick, FACT_BANK, BABY_TIP_BANK, ON_THIS_DAY_BANK, EPIGRAPH_BANK,
    WORD_OF_DAY_BANK, ARCANA_BANK, HISTORY_QUOTE_BANK,
)

SAMPLE_FEATURE_TITLE = "MARKET NOTES"
SAMPLE_FEATURE_BODY = (
    'Hacker News is buzzing about &#8220;StreetComplete: Fixing '
    'OpenStreetMap, one tiny quest at a time&#8221; (106 pts, 25 comments). '
    "DeFi's biggest mover today is Felix Vaults, up 58.5% to $102.9M locked.")
SAMPLE_TVL_LINE = 'DeFi TVL 10d: $74.0B (&#8722;1.0%)'
SAMPLE_TVL_HISTORY = [70.29, 69.93, 70.40, 69.24, 70.27, 72.65, 74.16, 74.36,
                      74.73, 73.99]  # billions, real 10-day pull

OUT_PATH = "/Users/joshstokesberry/COMMANDER/MORNING_REPORT_v2_mockup.pdf"


def build():
    today = datetime.date(2026, 7, 6)
    day = today.toordinal()

    otd_year, otd_rest = pick(ON_THIS_DAY_BANK, day).split(":", 1)

    ctx = {
        "date_str": "Monday, July 6, 2026",
        "generated_at": "6:42:15 AM CT",
        "vol_no": "VOL. 1 &#183; NO. 6",
        "epigraph": pick(EPIGRAPH_BANK, day),
        "sun_text": (
            "Sunrise 6:31 AM &#183; Sunset 8:42 PM &#183; Daylight 14h 11m "
            "(&#8722;2m)"),
        "sun_progress_frac": 0.62,
        "moon_text": ("Waxing Gibbous 78% &#183; Full moon Jul 19 "
                      "&#183; Fall Eq. in 78d"),
        "moon_phase_frac": 0.39,
        "ticker_items": [
            ("BTC", "$118,432", True), ("ETH", "$3,812", True),
            ("LINK", "$21.44", False), ("CVX", "$3.87", True),
            ("AERO", "$1.12", False), ("SILVER", "$36.90/oz", True),
            ("OIL (WTI)", "$67.20/bbl", False),
        ],
        "fear_greed_value": 62,
        "fear_greed_label": "GREED",
        "otd_year": otd_year,
        "otd_rest": otd_rest,
        "weather_headline": (
            "<b>78°F</b> / 61°F · Partly cloudy, 20% chance of afternoon "
            "storms. Wind SSW 12mph. Feels like a good porch-coffee "
            "morning."),
        "uv_aqi_line": "UV index 6 (moderate) · Air quality: Good (AQI 32)",
        "primoscapes_note": (
            "soil's dry enough for prep work before the afternoon storms "
            "roll in — get the chop-and-drop done early."),
        "fact": pick(FACT_BANK, day),
        "baby_tip": pick(BABY_TIP_BANK, day),
        "word_of_day": pick(WORD_OF_DAY_BANK, day),
        "news": [
            ("CRYPTO/TECH", "Onchain RWA issuance crosses $18B as tokenized "
                            "treasuries keep climbing"),
            ("TECH", "A new open-source model claims state-of-the-art "
                     "results on long-context reasoning benchmarks"),
        ],
        "decide_title": "Create the TikTok account this weekend?",
        "feature_title": SAMPLE_FEATURE_TITLE,
        "feature_body": SAMPLE_FEATURE_BODY,
        "tvl_line": SAMPLE_TVL_LINE,
        "tvl_history": SAMPLE_TVL_HISTORY,
        "arcana": pick(ARCANA_BANK, day),
        "market_cap": "$2.28T",
        "btc_dominance": "56.1%",
        "random_fact": "SAMPLE DATA — not a real run, nothing here was fetched.",
        "history_quote": pick(HISTORY_QUOTE_BANK, day),
        "signals_items": [
            ("SATS/$", "1,572", None),
            ("HALVING", "~645d", None),
            ("GWEI", "0.07", None),
        ],
    }

    render(ctx, OUT_PATH, pdf_title="THE DAILY MOG — v2 layout mockup (sample data)")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    build()
