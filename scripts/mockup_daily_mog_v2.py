#!/usr/bin/env python3
"""V2 layout mockup for THE DAILY MOG — placeholder/sample data only.
Purpose: validate layout + aesthetics before wiring any live data source.
Not the production generator — see generate_dispatch.py for that (v1,
currently the approved-so-far baseline while this iterates).
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

# --- palette: warm almanac base, 4 purposeful accents, nothing decorative ---
PAPER = HexColor("#FBF6EC")
INK = HexColor("#241F16")
MUTED = HexColor("#6B6255")
LINE = HexColor("#DDD3BF")
BRAND = HexColor("#4B3F8F")   # masthead / identity only
GREEN = HexColor("#1B7A4D")   # price up / shipped
RED = HexColor("#A3402F")     # price down only
AMBER = HexColor("#B8790A")   # decide accent only
AMBER_BG = HexColor("#FBEBD2")

S = {
    "masthead": ParagraphStyle("mh", fontName="Helvetica-Bold", fontSize=30,
                                textColor=BRAND, leading=32),
    "issue": ParagraphStyle("is", fontName="Helvetica", fontSize=8.5,
                             textColor=MUTED),
    "dateline": ParagraphStyle("dl", fontName="Helvetica-Bold", fontSize=10,
                                textColor=INK, alignment=TA_RIGHT),
    "almanac_line": ParagraphStyle("al", fontName="Helvetica", fontSize=8.5,
                                    textColor=MUTED, alignment=TA_RIGHT, leading=12),
    "ticker": ParagraphStyle("tk", fontName="Courier", fontSize=9,
                              textColor=INK, alignment=TA_CENTER),
    "section_h": ParagraphStyle("sh", fontName="Helvetica-Bold", fontSize=10,
                                 textColor=BRAND, spaceBefore=10, spaceAfter=4,
                                 borderWidth=0),
    "body": ParagraphStyle("b", fontName="Helvetica", fontSize=9.3,
                            textColor=INK, leading=13),
    "body_sm": ParagraphStyle("bs", fontName="Helvetica", fontSize=8.7,
                               textColor=INK, leading=12.5),
    "muted_sm": ParagraphStyle("ms", fontName="Helvetica-Oblique", fontSize=8,
                                textColor=MUTED, leading=11),
    "news_headline": ParagraphStyle("nh", fontName="Helvetica-Bold", fontSize=9.3,
                                     textColor=INK, leading=12.5),
    "news_tag": ParagraphStyle("nt", fontName="Helvetica-Bold", fontSize=7,
                                textColor=BRAND, leading=9),
    "decide_title": ParagraphStyle("dt", fontName="Helvetica-Bold", fontSize=10.5,
                                    textColor=AMBER, leading=13),
    "decide_ctx": ParagraphStyle("dc", fontName="Helvetica", fontSize=8.5,
                                  textColor=INK, leading=12),
    "shipped_label": ParagraphStyle("shl", fontName="Helvetica-Bold", fontSize=7.5,
                                     textColor=MUTED, leading=9),
    "shipped_num": ParagraphStyle("shn", fontName="Helvetica-Bold", fontSize=20,
                                   textColor=GREEN, leading=22),
    "one_liner": ParagraphStyle("ol", fontName="Helvetica-BoldOblique", fontSize=11,
                                 textColor=INK, alignment=TA_CENTER, leading=15),
    "one_liner_tag": ParagraphStyle("olt", fontName="Helvetica", fontSize=7.5,
                                     textColor=MUTED, alignment=TA_CENTER),
    "footer": ParagraphStyle("f", fontName="Helvetica", fontSize=7,
                              textColor=MUTED, leading=10),
}


def box(flowables, bg, border_color, border_side="LINEBEFORE", width=6.9 * inch, pad=10):
    t = Table([[flowables]], colWidths=[width])
    style = [
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), pad + 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]
    if border_side:
        style.append((border_side, (0, 0), (0, -1), 3, border_color))
    t.setStyle(TableStyle(style))
    return t


def ticker_strip():
    items = [
        ("BTC", "$118,432", True), ("ETH", "$3,812", True), ("LINK", "$21.44", False),
        ("CVX", "$3.87", True), ("AERO", "$1.12", False),
        ("SILVER", "$36.90/oz", True), ("OIL (WTI)", "$67.20/bbl", False),
    ]
    cells = []
    for sym, price, up in items:
        arrow = "▲" if up else "▼"
        color = "#1B7A4D" if up else "#A3402F"
        cells.append(Paragraph(
            f'<font face="Helvetica-Bold">{sym}</font> {price} '
            f'<font color="{color}">{arrow}</font>', S["ticker"]))
    t = Table([cells], colWidths=[0.98 * inch] * 7)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def build():
    doc = SimpleDocTemplate(
        "/Users/joshstokesberry/COMMANDER/MORNING_REPORT_v2_mockup.pdf",
        pagesize=letter, leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.5 * inch, bottomMargin=0.45 * inch,
        title="THE DAILY MOG — v2 layout mockup (sample data)")
    e = []

    # masthead
    head = Table([[
        [Paragraph("THE DAILY MOG", S["masthead"]),
         Paragraph("Vol. 1, No. 6 · commander-issued, no subscription required", S["issue"])],
        [Paragraph("Monday, July 6, 2026", S["dateline"]),
         Paragraph("Moon: Waxing Gibbous (78%)<br/>Sunrise 6:31 AM · Sunset 8:42 PM", S["almanac_line"])],
    ]], colWidths=[4.3 * inch, 2.6 * inch])
    head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM")]))
    e.append(head)
    e.append(Spacer(1, 6))
    e.append(HRFlowable(width="100%", thickness=1.6, color=BRAND, spaceAfter=2))
    e.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=8))

    # ticker
    e.append(ticker_strip())
    e.append(Spacer(1, 10))

    # two columns
    left = []
    left.append(Paragraph("WEATHER — OKC", S["section_h"]))
    left.append(Paragraph(
        "<b>78°F</b> / 61°F · Partly cloudy, 20% chance of afternoon storms. "
        "Wind SSW 12mph. Feels like a good porch-coffee morning.", S["body"]))
    left.append(Paragraph(
        "🌱 Primoscapes note: soil's dry enough for prep work before the afternoon storms roll in — "
        "get the chop-and-drop done early.", S["muted_sm"]))
    left.append(Spacer(1, 8))

    left.append(Paragraph("TODAY YOU SHOULD KNOW", S["section_h"]))
    left.append(Paragraph(
        "Chainlink's first mainnet transaction went live May 30, 2019 — the same core "
        "oracle design still secures the majority of DeFi's total value today.", S["body"]))
    left.append(Spacer(1, 8))

    left.append(Paragraph("BABY TIP OF THE DAY", S["section_h"]))
    left.append(Paragraph(
        "Newborns often sleep better swaddled with arms in for the first weeks — the "
        "startle reflex (Moro reflex) can wake them before it fades around 2–4 months.", S["body"]))

    right = []
    right.append(Paragraph("THE MOG DIGEST", S["section_h"]))
    news = [
        ("CRYPTO/TECH", "Onchain RWA issuance crosses $18B as tokenized treasuries keep climbing"),
        ("TECH", "New silicon photonics chip claims 10x data-center interconnect efficiency"),
        ("OKC LOCAL", "Scissortail Park announces new native-plant demonstration garden this fall"),
    ]
    for tag, headline in news:
        right.append(Paragraph(tag, S["news_tag"]))
        right.append(Paragraph(headline, S["news_headline"]))
        right.append(Spacer(1, 5))
    right.append(Spacer(1, 4))

    right.append(Paragraph("DECIDE", S["section_h"]))
    right.append(box([
        Paragraph("Create the TikTok account this weekend?", S["decide_title"]),
        Spacer(1, 2),
        Paragraph("Handle bebad4good, bio + avatar approved. ~30 min, credentials stay yours. "
                  "Publishing cork for the whole cartoon lab.", S["decide_ctx"]),
    ], AMBER_BG, AMBER, width=3.15 * inch, pad=8))
    right.append(Spacer(1, 6))

    ship = Table([[
        Paragraph("SHIPPED<br/>THIS WEEK", S["shipped_label"]),
        Paragraph("5", S["shipped_num"]),
    ]], colWidths=[0.9 * inch, 0.6 * inch])
    ship.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    right.append(ship)

    cols = Table([[left, right]], colWidths=[3.55 * inch, 3.35 * inch])
    cols.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEAFTER", (0, 0), (0, 0), 0.6, LINE),
        ("RIGHTPADDING", (0, 0), (0, 0), 14),
        ("LEFTPADDING", (1, 0), (1, 0), 14),
    ]))
    e.append(cols)
    e.append(Spacer(1, 10))

    e.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=8))
    e.append(Paragraph(
        '"He didn\'t open the ticket — he just watched it. That\'s Support-Bot energy."',
        S["one_liner"]))
    e.append(Paragraph("— Bad Boys, mascot of the day: Astronaut", S["one_liner_tag"]))

    e.append(Spacer(1, 10))
    e.append(HRFlowable(width="100%", thickness=0.4, color=LINE, spaceAfter=4))
    e.append(Paragraph(
        "SAMPLE DATA — layout mockup only, nothing above is live-fetched. "
        "No posting · no sending · no spending without approval.", S["footer"]))

    doc.build(e)
    print("wrote MORNING_REPORT_v2_mockup.pdf")


if __name__ == "__main__":
    build()
