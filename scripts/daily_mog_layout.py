#!/usr/bin/env python3
"""THE DAILY MOG — shared layout + curated content banks.

Single source of truth for rendering, used by both the sample-data mockup
(mockup_daily_mog_v2.py) and the live generator (generate_daily_mog.py), so
the two can never visually diverge — same lesson as v1's shared data-parse
for MORNING_REPORT.md/.pdf.

render(ctx, out_path) takes a fully-populated context dict (see the two
callers for the exact shape) and builds the one-page PDF. This module has
no knowledge of where the data came from — sample or live.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER

# --- content banks: small, curated, auditable — rotates daily via pick(),
# never freshly improvised at generation time (same pattern for every bank) ---
FACT_BANK = [
    "Before “smart” contracts could see prices, weather, or scores, they "
    "were blind to the outside world. Chainlink's first mainnet oracle call "
    "landed May 30, 2019 — the same design still prices most of DeFi today.",
    "Oklahoma tallgrass prairie species send roots down 10-15 feet, which is "
    "why native plantings like Scissortail's new garden shrug off droughts "
    "that kill imported lawn grass in weeks.",
    "“Instant” bank transfers ran on 1970s plumbing until recently — "
    "FedNow, the Fed's real-time payment rail, didn't launch until 2023, "
    "over 50 years after Fedwire.",
    "Redbud trees, common in OKC yards, fix nitrogen in the soil around "
    "them — old farmers planted them as a free signal that the ground "
    "underneath was good for a garden.",
]

BABY_TIP_BANK = [
    "The Moro reflex makes newborns startle and fling their arms — often "
    "enough to wake themselves up. Swaddling with arms in, not just legs, "
    "blocks the flail. It fades on its own by 2-4 months.",
    "A newborn's stomach holds about a marble's worth at birth, a cherry's "
    "worth by day 3. Frequent small feeds aren't a feeding problem — that's "
    "just the actual size of the tank.",
    "Newborn vision favors sharp black-and-white contrast over soft colors "
    "for the first few months — their eyes can't resolve subtle color "
    "differences yet, so bold patterns are what actually gets noticed.",
    "White noise works on babies because the womb was loud — closer to a "
    "running vacuum than a lullaby. Quiet isn't naturally soothing to a "
    "newborn; it's a preference they learn later.",
]

# real, checkable historical notes — same curated-bank pattern, not fetched
ON_THIS_DAY_BANK = [
    "1785: The Continental Congress adopts the dollar as the United "
    "States' standard unit of currency.",
    "1928: The first color motion picture, Walt Disney's 'Flowers and "
    "Trees,' begins production.",
    "1957: Althea Gibson becomes the first Black athlete to win a "
    "Wimbledon singles title.",
    "2016: The FDA approves the first artificial pancreas device for "
    "type 1 diabetes.",
]

# masthead epigraph — the paper's own voice, a daily creed. Short, confident,
# builder-coded; no attribution (this is identity, not a quote).
EPIGRAPH_BANK = [
    "Small edges, stacked daily.",
    "Make something today that outlives the day.",
    "The quiet work compounds.",
    "Build in the morning; the world argues after lunch.",
    "Fortune favors the finished.",
    "Ideas are cheap. Mornings are not.",
    "Print it, ship it, prove it.",
]

# word of the day — real, checkable; a mix of useful and delightful-rare
WORD_OF_DAY_BANK = [
    ("Sisu", "Finnish noun", "Extraordinary grit that shows up after the "
     "normal kind runs out — resolve in the face of odds that should have "
     "ended the effort already."),
    ("Apricity", "archaic noun", "The warmth of the sun in winter."),
    ("Sonder", "noun", "The dawning awareness that every stranger is living "
     "a life as vivid and tangled as your own."),
    ("Eucatastrophe", "noun", "A sudden turn toward good that rescues a story "
     "from ruin — coined by J.R.R. Tolkien for the moment hope breaks "
     "through."),
]

# sub rosa — the arcane/philosophical inscription. Real, attributed lines from
# the old esoteric + wisdom traditions (hermetic, alchemical, Stoic, Taoist,
# Heraclitus, Rumi, Delphic). Deliberately a MIX of short deadpan hits and
# longer, weightier passages so the closing seal reads differently each morning.
ARCANA_BANK = [
    ("Nature loves to hide.", "Heraclitus, c. 500 BC"),
    ("What you seek is seeking you.", "Rumi"),
    ("As above, so below.", "The Emerald Tablet"),
    ("Sell your cleverness and buy bewilderment.", "Rumi"),
    ("The soul becomes dyed with the color of its thoughts.",
     "Marcus Aurelius, Meditations"),
    ("No man ever steps in the same river twice — for it is not the same "
     "river, and he is not the same man.", "Heraclitus"),
    ("Know thyself — and nothing in excess.",
     "inscribed at the Temple of Apollo, Delphi"),
    ("We suffer more often in imagination than in reality.",
     "Seneca, Letters to Lucilius"),
    ("The impediment to action advances action. What stands in the way "
     "becomes the way.", "Marcus Aurelius, Meditations"),
    ("Knowing others is intelligence; knowing yourself is true wisdom. "
     "Mastering others is strength; mastering yourself is true power.",
     "Lao Tzu, Tao Te Ching"),
    ("Visit the interior of the earth, and by rectification thou shalt find "
     "the hidden stone.", "the alchemists' VITRIOL formula"),
    ("All things are poison, and nothing is without poison — only the dose "
     "makes a thing not a poison.", "Paracelsus, 1538"),
    ("Yesterday I was clever, so I wanted to change the world. Today I am "
     "wise, so I am changing myself.", "Rumi"),
]

# fallback only — used when the live feature source (e.g. NASA APOD) can't
# be reached; an honest "unavailable" beats a fabricated substitute
FEATURE_FALLBACK_TITLE = "FROM THE OBSERVATORY"
FEATURE_FALLBACK_BODY = (
    "Today's featured pick is unavailable right now — the source didn't "
    "respond. Nothing shown here is ever invented to fill the gap."
)


def pick(bank, day_ordinal, salt=0):
    """Deterministic daily rotation, not per-run randomness: the same
    calendar day always yields the same pick, so regenerating twice in one
    morning (e.g. two Pi boots) shows the same content, and it's auditable
    (you can predict tomorrow's index)."""
    return bank[(day_ordinal + salt) % len(bank)]


# --- palette: warm almanac base, 4 purposeful accents, nothing decorative ---
PAPER = HexColor("#FBF6EC")
INK = HexColor("#241F16")
MUTED = HexColor("#6B6255")
LINE = HexColor("#DDD3BF")
RULE = HexColor("#C4B89F")    # slightly darker hairline for header underlines
BRAND = HexColor("#4B3F8F")   # masthead / identity only
GREEN = HexColor("#1B7A4D")   # price up / index reading "greed" side
RED = HexColor("#A3402F")     # price down / index reading "fear" side
AMBER = HexColor("#B8790A")   # decide accent only
AMBER_BG = HexColor("#FBEBD2")

FEAR_GREED_COLOR = {
    "EXTREME FEAR": "#A3402F", "FEAR": "#A3402F",
    "NEUTRAL": "#6B6255",
    "GREED": "#1B7A4D", "EXTREME GREED": "#1B7A4D",
}

# Typographic system: serif (Times) for everything that reads as editorial —
# nameplate, body, headlines, pull-quote — for authentic newspaper/almanac
# feel. Sans (Helvetica) reserved for kickers, data strips, and fine print,
# so the two roles stay visually distinct.
S = {
    "masthead": ParagraphStyle("mh", fontName="Times-Bold", fontSize=42,
                                textColor=BRAND, leading=44, alignment=TA_CENTER),
    "epigraph": ParagraphStyle("ep", fontName="Times-Italic", fontSize=11.5,
                               textColor=INK, leading=14, alignment=TA_CENTER),
    "wod_term": ParagraphStyle("wt", fontName="Times-Bold", fontSize=12,
                               textColor=INK, leading=14),
    "folio_side": ParagraphStyle("fs", fontName="Helvetica-Bold", fontSize=7.5,
                                  textColor=MUTED, leading=10),
    "folio_center": ParagraphStyle("fc", fontName="Times-Bold", fontSize=9.5,
                                    textColor=INK, alignment=TA_CENTER, leading=11),
    "almanac_line": ParagraphStyle("al", fontName="Times-Roman", fontSize=8.7,
                                    textColor=MUTED, alignment=TA_CENTER, leading=12.5),
    "ticker": ParagraphStyle("tk", fontName="Helvetica", fontSize=8,
                              textColor=INK, alignment=TA_CENTER, leading=10.5),
    "section_h": ParagraphStyle("sh", fontName="Helvetica-Bold", fontSize=9.5,
                                 textColor=BRAND, spaceBefore=13, spaceAfter=2),
    "body": ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5,
                            textColor=INK, leading=15),
    "body_sm": ParagraphStyle("bs", fontName="Times-Roman", fontSize=9.5,
                               textColor=INK, leading=13.5),
    "muted_sm": ParagraphStyle("ms", fontName="Times-Italic", fontSize=9,
                                textColor=MUTED, leading=12.5),
    "news_headline": ParagraphStyle("nh", fontName="Times-Bold", fontSize=11,
                                     textColor=INK, leading=13.5),
    "news_tag": ParagraphStyle("nt", fontName="Helvetica-Bold", fontSize=7,
                                textColor=BRAND, leading=9.5),
    "decide_title": ParagraphStyle("dt", fontName="Times-Bold", fontSize=11.5,
                                    textColor=AMBER, leading=14),
    "decide_ctx": ParagraphStyle("dc", fontName="Times-Roman", fontSize=9.7,
                                  textColor=INK, leading=13.5),
    "index_line": ParagraphStyle("il", fontName="Helvetica", fontSize=8.7,
                                  textColor=INK, alignment=TA_CENTER, leading=11),
    "otd_line": ParagraphStyle("otd", fontName="Times-Italic", fontSize=8.7,
                                textColor=MUTED, alignment=TA_CENTER, leading=11.5),
    "arcana_kicker": ParagraphStyle("ak", fontName="Helvetica-Bold", fontSize=8,
                                     textColor=BRAND, alignment=TA_CENTER, leading=12),
    "arcana_quote": ParagraphStyle("aq", fontName="Times-Italic", fontSize=13,
                                    textColor=INK, alignment=TA_CENTER, leading=17),
    "arcana_attr": ParagraphStyle("aa", fontName="Helvetica", fontSize=7.7,
                                   textColor=MUTED, alignment=TA_CENTER, leading=10),
    "footer": ParagraphStyle("f", fontName="Helvetica", fontSize=7,
                              textColor=MUTED, leading=10),
}


def sec(title):
    """Section header (sans kicker) + hairline rule beneath — the newspaper
    section-divider look. Returns a list to extend a column's flowables."""
    return [Paragraph(title, S["section_h"]),
            HRFlowable(width="100%", thickness=0.5, color=RULE,
                       spaceBefore=1, spaceAfter=6)]


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


def ticker_strip(items):
    """items: list of (symbol, price_str, is_up) tuples, exactly 7 for the
    layout to balance. Every item stacks symbol atop price+arrow — uniform,
    so nothing wraps differently just because one string is longer."""
    cells = []
    for sym, price, up in items:
        arrow = "▲" if up else "▼"
        color = "#1B7A4D" if up else "#A3402F"
        cells.append(Paragraph(
            f'<font face="Helvetica-Bold" size="8">{sym}</font><br/>'
            f'<font face="Courier" size="8">{price} '
            f'<font color="{color}">{arrow}</font></font>', S["ticker"]))
    t = Table([cells], colWidths=[0.98 * inch] * 7)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def render(ctx, out_path, pdf_title="THE DAILY MOG"):
    """ctx keys (all required):
    date_str, vol_no, epigraph, sky_line, ticker_items,
    fear_greed_value, fear_greed_label, otd_year, otd_rest,
    weather_headline, uv_aqi_line, primoscapes_note, fact, baby_tip,
    word_of_day (term, pos, definition), news (list of (tag, headline)),
    decide_title, decide_body, feature_title, feature_body, arcana (quote, source),
    footer_note
    """
    doc = SimpleDocTemplate(
        out_path, pagesize=letter, leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.5 * inch, bottomMargin=0.45 * inch, title=pdf_title)
    e = []

    # --- masthead: centered nameplate, classic newspaper folio treatment ---
    e.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=8))
    e.append(Paragraph("THE DAILY MOG", S["masthead"]))
    e.append(Spacer(1, 3))
    # epigraph flanked by floral ornaments matching the SUB ROSA seal, so the
    # masthead and the footer rhyme — top and bottom of the page echo
    orn = '<font face="ZapfDingbats" size="9" color="#4B3F8F">&#10086;</font>'
    e.append(Paragraph(
        f'{orn}&nbsp;&nbsp;&#8220;{ctx["epigraph"]}&#8221;&nbsp;&nbsp;{orn}',
        S["epigraph"]))
    e.append(Spacer(1, 8))

    folio = Table([[
        Paragraph("OKLAHOMA CITY, OKLA.", S["folio_side"]),
        Paragraph(ctx["date_str"], S["folio_center"]),
        Paragraph(ctx["vol_no"], ParagraphStyle(
            "fsr", parent=S["folio_side"], alignment=TA_RIGHT)),
    ]], colWidths=[2.3 * inch, 2.3 * inch, 2.3 * inch])
    folio.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (0, 0), (-1, 0), 1.4, BRAND),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    e.append(folio)
    e.append(Spacer(1, 6))

    e.append(Paragraph(ctx["sky_line"], S["almanac_line"]))
    e.append(Spacer(1, 8))

    e.append(ticker_strip(ctx["ticker_items"]))
    e.append(Spacer(1, 5))
    fg_color = FEAR_GREED_COLOR.get(ctx["fear_greed_label"].upper(), "#6B6255")
    e.append(Paragraph(
        f'<font face="Helvetica-Bold">CRYPTO FEAR &amp; GREED:</font> '
        f'{ctx["fear_greed_value"]} &#183; '
        f'<font color="{fg_color}"><b>{ctx["fear_greed_label"].upper()}</b></font>',
        S["index_line"]))
    e.append(Spacer(1, 6))
    e.append(Paragraph(
        f'ON THIS DAY &#8212; <b>{ctx["otd_year"]}</b>:{ctx["otd_rest"]}',
        S["otd_line"]))
    e.append(Spacer(1, 10))

    # two columns
    left = []
    left += sec("WEATHER — OKC")
    left.append(Paragraph(ctx["weather_headline"], S["body"]))
    left.append(Spacer(1, 3))
    left.append(Paragraph(ctx["uv_aqi_line"], S["muted_sm"]))
    left.append(Spacer(1, 3))
    left.append(Paragraph(
        f'<b>Primoscapes note:</b> {ctx["primoscapes_note"]}', S["muted_sm"]))

    left += sec("WORTH KNOWING")
    left.append(Paragraph(ctx["fact"], S["body"]))

    left += sec("BABY TIP")
    left.append(Paragraph(ctx["baby_tip"], S["body"]))

    wod_term, wod_pos, wod_def = ctx["word_of_day"]
    left += sec("WORD OF THE DAY")
    left.append(Paragraph(
        f'{wod_term}  <font face="Times-Italic" color="#6B6255" size="9">'
        f'&#183; {wod_pos}</font>', S["wod_term"]))
    left.append(Spacer(1, 2))
    left.append(Paragraph(wod_def, S["body"]))

    right = []
    right += sec("THE MOG DIGEST")
    news = ctx["news"]
    for i, (tag, headline) in enumerate(news):
        right.append(Paragraph(tag, S["news_tag"]))
        right.append(Paragraph(headline, S["news_headline"]))
        if i < len(news) - 1:
            right.append(HRFlowable(width="100%", thickness=0.4, color=LINE,
                                    spaceBefore=6, spaceAfter=6))
    right.append(Spacer(1, 4))

    right += sec("DECIDE")
    right.append(box([
        Paragraph(ctx["decide_title"], S["decide_title"]),
        Spacer(1, 2),
        Paragraph(ctx["decide_body"], S["decide_ctx"]),
    ], AMBER_BG, AMBER, width=3.15 * inch, pad=8))

    right += sec(ctx["feature_title"])
    right.append(Paragraph(ctx["feature_body"], S["body"]))

    cols = Table([[left, right]], colWidths=[3.55 * inch, 3.35 * inch])
    cols.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEAFTER", (0, 0), (0, 0), 0.6, LINE),
        ("RIGHTPADDING", (0, 0), (0, 0), 14),
        ("LEFTPADDING", (1, 0), (1, 0), 14),
    ]))
    e.append(cols)
    e.append(Spacer(1, 12))

    # --- SUB ROSA: full-width arcane inscription, the page's closing seal ---
    arc_quote, arc_src = ctx["arcana"]
    e.append(HRFlowable(width="100%", thickness=1.2, color=BRAND, spaceAfter=1.5))
    e.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=7))
    e.append(Paragraph(
        '<font face="ZapfDingbats" size="8">&#10086;</font>&nbsp;&nbsp;&nbsp;'
        'S U B &nbsp; R O S A'
        '&nbsp;&nbsp;&nbsp;<font face="ZapfDingbats" size="8">&#10086;</font>',
        S["arcana_kicker"]))
    e.append(Spacer(1, 4))
    e.append(Paragraph(f"&#8220;{arc_quote}&#8221;", S["arcana_quote"]))
    e.append(Spacer(1, 3))
    e.append(Paragraph(f"&#8212; {arc_src}", S["arcana_attr"]))
    e.append(Spacer(1, 8))

    e.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=4))
    e.append(Paragraph(ctx["footer_note"], S["footer"]))

    doc.build(e)
