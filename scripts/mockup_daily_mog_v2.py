#!/usr/bin/env python3
"""V2 layout mockup for THE DAILY MOG — placeholder/sample data only.
Purpose: validate layout + aesthetics before wiring any live data source.
Rendering now lives in daily_mog_layout.py (shared with the live generator,
generate_daily_mog.py) — this file only builds a sample context dict.
"""
import datetime

from daily_mog_layout import (
    render, pick, FACT_BANK, BABY_TIP_BANK, ON_THIS_DAY_BANK, EPIGRAPH_BANK,
    WORD_OF_DAY_BANK, ARCANA_BANK,
)

SAMPLE_FEATURE_TITLE = "FROM THE OBSERVATORY"
SAMPLE_FEATURE_BODY = (
    "<b>Dueling Bands over the Atacama Desert</b><br/>What are these two "
    "bands in the sky? The one on the left is the central band of our own "
    "Milky Way; the fainter one on the right is zodiacal light — sunlight "
    "reflected off comet dust orbiting the Sun. "
    '<font size="8" color="#6B6255">&#8212; NASA Astronomy Picture of the '
    "Day</font>")

OUT_PATH = "/Users/joshstokesberry/COMMANDER/MORNING_REPORT_v2_mockup.pdf"


def build():
    today = datetime.date(2026, 7, 6)
    day = today.toordinal()

    otd_year, otd_rest = pick(ON_THIS_DAY_BANK, day).split(":", 1)

    ctx = {
        "date_str": "Monday, July 6, 2026",
        "vol_no": "VOL. 1 &#183; NO. 6",
        "epigraph": pick(EPIGRAPH_BANK, day),
        "sky_line": (
            "Sunrise 6:31 AM &#183; Sunset 8:42 PM &#183; Daylight 14h 11m "
            "(&#8722;2m) &#183; Moon: Waxing Gibbous 78% &#183; Next full "
            "moon Jul 19"),
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
            ("TECH", "New silicon photonics chip claims 10x data-center "
                     "interconnect efficiency"),
            ("OKC LOCAL", "Scissortail Park announces new native-plant "
                          "demonstration garden this fall"),
        ],
        "decide_title": "Create the TikTok account this weekend?",
        "decide_body": (
            "Handle bebad4good, bio + avatar approved. ~30 min, "
            "credentials stay yours. Publishing cork for the whole "
            "cartoon lab."),
        "feature_title": SAMPLE_FEATURE_TITLE,
        "feature_body": SAMPLE_FEATURE_BODY,
        "arcana": pick(ARCANA_BANK, day),
        "footer_note": (
            "SAMPLE DATA — layout mockup only, nothing above is "
            "live-fetched. No posting · no sending · no spending without "
            "approval."),
    }

    render(ctx, OUT_PATH, pdf_title="THE DAILY MOG — v2 layout mockup (sample data)")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    build()
