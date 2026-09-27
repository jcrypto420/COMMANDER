#!/usr/bin/env python3
"""V2 layout mockup for THE DAILY MOG — placeholder/sample data only.
Purpose: validate layout + aesthetics before wiring any live data source.
Rendering now lives in daily_mog_layout.py (shared with the live generator,
generate_daily_mog.py) — this file only builds a sample context dict.
"""
import datetime

from daily_mog_layout import (
    render, pick, BABY_TIP_BANK, EPIGRAPH_BANK, WORD_OF_DAY_BANK, ARCANA_BANK,
    HISTORY_QUOTE_BANK,
)

SAMPLE_FEATURE_TITLE = "MARKET NOTES"
SAMPLE_FEATURE_BODY = (
    'Hacker News is buzzing about &#8220;StreetComplete: Fixing '
    'OpenStreetMap, one tiny quest at a time&#8221; (106 pts, 25 comments). '
    "DeFi's biggest mover today is Felix Vaults, up 58.5% to $102.9M locked. "
    "On your board, LINK leads the move, up 8.2% today.")
SAMPLE_TVL_LINE = 'DeFi TVL 10d: $74.0B (&#8722;1.0%)'
SAMPLE_TVL_HISTORY = [70.29, 69.93, 70.40, 69.24, 70.27, 72.65, 74.16, 74.36,
                      74.73, 73.99]  # billions, real 10-day pull

OUT_PATH = "/Users/joshstokesberry/COMMANDER/MORNING_REPORT_v2_mockup.pdf"


def build():
    today = datetime.date(2026, 7, 6)
    day = today.toordinal()

    ctx = {
        "date_str": "Monday, July 6, 2026",
        "generated_at": "6:42:15 AM CT",
        "vol_no": "VOL. 1 &#183; NO. 6",
        "epigraph": pick(EPIGRAPH_BANK, day),
        "sun_text": (
            "Sunrise&nbsp;6:31&nbsp;AM &#183; Sunset&nbsp;8:42&nbsp;PM &#183; "
            "Daylight&nbsp;14h&nbsp;11m&nbsp;(&#8722;2m)"),
        "sun_progress_frac": 0.62,
        "moon_text": ("Waxing&nbsp;Gibbous&nbsp;78% &#183; "
                      "Full&nbsp;moon&nbsp;Jul&nbsp;19 &#183; "
                      "Fall&nbsp;Eq.&nbsp;in&nbsp;78d"),
        "moon_phase_frac": 0.39,
        "ticker_items": [
            ("BTC", "$118,432", True), ("ETH", "$3,812", True),
            ("LINK", "$21.44", False), ("CVX", "$3.87", True),
            ("AERO", "$1.12", False), ("SILVER", "$36.90/oz", True),
            ("OIL (WTI)", "$67.20/bbl", False),
        ],
        "fear_greed_value": 62,
        "fear_greed_label": "GREED",
        "otd_year": "1969",  # SAMPLE — live pull is Wikipedia's "On this
                              # day" feed for today's real calendar date
        "otd_rest": (" NASA's Mariner 6 sends back the first close-up "
                     "images of Mars."),
        "weather_headline": (
            "<b>78°F</b> / 61°F · Partly cloudy, 20% chance of afternoon "
            "storms. Wind SSW 12mph. Feels like a good porch-coffee "
            "morning."),
        "uv_aqi_line": "UV index 6 (moderate) · Air quality: Good (AQI 32)",
        "primoscapes_note": (
            "soil's dry enough for prep work before the afternoon storms "
            "roll in — get the chop-and-drop done early."),
        "fact": ("SAMPLE — live pull, independent 2nd fetch from the same "
                 "random-fact API as the bottom-of-page line."),
        "baby_tip": pick(BABY_TIP_BANK, day),
        "word_of_day": pick(WORD_OF_DAY_BANK, day),
        "news": [
            # kept to ~60 chars each — matches MAX_HEADLINE_CHARS, the real
            # cap get_rss_headline() truncates to, so this sample never shows
            # unrealistically long/untruncated text the live pipeline
            # couldn't actually produce (real bug found 2026-07-09: a longer
            # sample headline here silently broke the one-page stress test)
            ("CRYPTO/TECH", "Onchain RWA issuance crosses $18B, still "
                            "climbing"),
            ("TECH", "New open-source model claims state-of-the-art "
                     "reasoning"),
            ("CRYPTO", "Layer-2 bridge volume hits a new quarterly high"),
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
