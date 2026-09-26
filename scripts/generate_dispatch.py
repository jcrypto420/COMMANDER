#!/usr/bin/env python3
"""Generate the daily dispatch — one data source, two outputs:
MORNING_REPORT.md (compact, phone-screen) and MORNING_REPORT.pdf (designed,
print-ready). Never let the two formats diverge — same parse, two renders.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LANES_TO_SHOW = [
    ("Career/Income (CI-1)", "NOW.md"),  # special-cased below
    ("Bad Boys cartoon lab", "projects/badboys-cartoon-lab.md"),
    ("Primoscapes (PS-1)", "projects/primoscapes.md"),
    ("The Boring Report", "projects/boring-report-prd.md"),
]


def read(path: str) -> str:
    p = ROOT / path
    return p.read_text() if p.exists() else ""


def first_status_state(text: str) -> str | None:
    m = re.search(r"^## Status\s*—.*?\n((?:.*\n)*?)(?=\n##|\Z)", text, re.M)
    if not m:
        return None
    block = m.group(1)
    s = re.search(r"\*\*State:\*\*\s*(.+)", block)
    return s.group(1).strip() if s else None


def shipped_count(now_text: str, log_text: str) -> tuple[int, int]:
    m = re.search(r"SMASHED:\s*(\d+)", now_text) or re.search(r"SHIPPED\s*=\s*(\d+)", now_text)
    shipped = int(m.group(1)) if m else 0
    t = re.search(r"one submitted application|target of (\d+)|success:\s*(\d+)", now_text, re.I)
    target = 1
    if t and t.lastindex:
        for g in t.groups():
            if g and g.isdigit():
                target = int(g)
    return shipped, target


def active_focus(now_text: str) -> str:
    m = re.search(r"\*\*Active focus:\*\*\s*(.+?)(?:\n\n|\Z)", now_text, re.S)
    if not m:
        return "See NOW.md"
    text = " ".join(m.group(1).split())
    if len(text) <= 220:
        return text
    cut = text[:220].rsplit(" ", 1)[0]
    return cut + "…"


def pending_gates() -> list[dict]:
    p = ROOT / "gates" / "pending.json"
    if not p.exists():
        return []
    data = json.loads(p.read_text())
    return [g for g in data.get("gates", []) if g.get("status") == "pending"]


def build_data() -> dict:
    now_text = read("NOW.md")
    log_text = read("logs/daily_progress.md")
    shipped, target = shipped_count(now_text, log_text)

    lanes = []
    for label, path in LANES_TO_SHOW:
        if path == "NOW.md":
            continue
        state = first_status_state(read(path))
        if state:
            lanes.append((label, state[:160] + ("…" if len(state) > 160 else "")))

    return {
        "date": datetime.now().strftime("%A, %B %-d, %Y"),
        "focus": active_focus(now_text),
        "shipped": shipped,
        "target": target,
        "lanes": lanes,
        "gates": pending_gates(),
    }


def render_markdown(d: dict) -> str:
    lines = []
    lines.append(f"# COMMANDER — Daily Dispatch — {d['date']}")
    lines.append("")
    lines.append(f"**Shipped this week: {d['shipped']}** (target: {d['target']})")
    lines.append(f"**Focus:** {d['focus']}")
    if d["gates"]:
        top = d["gates"][0]
        lines.append(f"**Decide:** {top['title']}")
    else:
        lines.append("**Decide:** nothing pending — clear runway")
    lines.append(f"**Open:** [Gate Deck](http://192.168.1.189:3011/gate-deck) · [Library](http://192.168.1.189:3011/docs)")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_pdf(d: dict, out_path: Path) -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    HRFlowable, Table, TableStyle)
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT

    INK = HexColor("#161616")
    MUTED = HexColor("#666666")
    LINE = HexColor("#DADADA")
    BRAND = HexColor("#4B3F8F")
    GREEN = HexColor("#1B7A4D")
    AMBER = HexColor("#B8790A")
    AMBER_BG = HexColor("#FFF7E8")

    S = {
        "brand": ParagraphStyle("brand", fontName="Helvetica-Bold", fontSize=22,
                                 textColor=BRAND, leading=24, tracking=1),
        "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=10,
                               textColor=MUTED, alignment=TA_RIGHT),
        "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8.5,
                                 textColor=MUTED, leading=11),
        "shipped_num": ParagraphStyle("shn", fontName="Helvetica-Bold", fontSize=34,
                                       textColor=GREEN, leading=36),
        "shipped_target": ParagraphStyle("sht", fontName="Helvetica", fontSize=10,
                                          textColor=MUTED),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5,
                             textColor=INK, spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("b", fontName="Helvetica", fontSize=10,
                                textColor=INK, leading=14),
        "lane_name": ParagraphStyle("ln", fontName="Helvetica-Bold", fontSize=9.5,
                                     textColor=INK, leading=13),
        "lane_state": ParagraphStyle("ls", fontName="Helvetica", fontSize=9.5,
                                      textColor=INK, leading=13),
        "decision_title": ParagraphStyle("dt", fontName="Helvetica-Bold", fontSize=11,
                                          textColor=AMBER, leading=14),
        "decision_ctx": ParagraphStyle("dc", fontName="Helvetica", fontSize=9,
                                        textColor=INK, leading=12.5),
        "footer": ParagraphStyle("f", fontName="Helvetica", fontSize=8,
                                  textColor=MUTED, leading=11),
    }

    def amber_box(flowables):
        t = Table([[flowables]], colWidths=[6.5 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG),
            ("LINEBEFORE", (0, 0), (0, -1), 3, AMBER),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        return t

    doc = SimpleDocTemplate(str(out_path), pagesize=letter,
                             leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                             topMargin=0.65 * inch, bottomMargin=0.6 * inch,
                             title=f"COMMANDER Daily Dispatch — {d['date']}")
    e = []

    header = Table([[Paragraph("COMMANDER", S["brand"]),
                      Paragraph(f"Daily Dispatch<br/>{d['date']}", S["sub"])]],
                    colWidths=[3.5 * inch, 3.0 * inch])
    header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM")]))
    e.append(header)
    e.append(Spacer(1, 4))
    e.append(HRFlowable(width="100%", thickness=1.5, color=BRAND, spaceAfter=12))

    e.append(Paragraph("SHIPPED THIS WEEK", S["label"]))
    e.append(Spacer(1, 2))
    score = Table([[
        Paragraph(str(d["shipped"]), S["shipped_num"]),
        Paragraph(
            f"target: {d['target']}<br/>things that left the building —<br/>drafts and commits don't count",
            S["shipped_target"]),
    ]], colWidths=[1.0 * inch, 5.5 * inch])
    score.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
    ]))
    e.append(score)
    e.append(Spacer(1, 10))

    e.append(Paragraph("FOCUS", S["label"]))
    e.append(Paragraph(d["focus"], S["body"]))

    if d["lanes"]:
        e.append(Paragraph("LANES", S["h"]))
        rows = []
        for name, state in d["lanes"]:
            rows.append([Paragraph(name, S["lane_name"]), Paragraph(state, S["lane_state"])])
        lt = Table(rows, colWidths=[1.6 * inch, 4.9 * inch])
        lt.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
        ]))
        e.append(lt)

    e.append(Spacer(1, 12))
    e.append(Paragraph("DECIDE", S["h"]))
    if d["gates"]:
        for g in d["gates"][:3]:
            box_content = [
                Paragraph(g["title"], S["decision_title"]),
                Spacer(1, 3),
                Paragraph(g.get("context", ""), S["decision_ctx"]),
            ]
            e.append(amber_box(box_content))
            e.append(Spacer(1, 8))
    else:
        e.append(Paragraph("Nothing pending — clear runway.", S["body"]))

    e.append(Spacer(1, 16))
    e.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=6))
    e.append(Paragraph(
        "No posting · no sending · no spending · no secrets without approval. "
        "Open Gate Deck: 192.168.1.189:3011/gate-deck — Library: /docs",
        S["footer"]))

    doc.build(e)


def main():
    d = build_data()
    (ROOT / "MORNING_REPORT.md").write_text(render_markdown(d))
    render_pdf(d, ROOT / "MORNING_REPORT.pdf")
    print(f"wrote MORNING_REPORT.md and MORNING_REPORT.pdf — shipped={d['shipped']}, gates={len(d['gates'])}")


if __name__ == "__main__":
    main()
