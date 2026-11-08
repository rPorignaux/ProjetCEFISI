"""Générer le dossier de conception CEFISI (Word + PDF) depuis sa source Markdown.

Source   : docs/cadrage/dossier-de-conception-v1.md
Sorties  : livrables/dossier-de-conception-v1.docx et .pdf

Le parseur couvre volontairement un sous-ensemble strict : titres (#, ##, ###),
paragraphes, listes à puces, tableaux pipes et gras inline (**texte**).

La table des matières est construite à partir des titres de niveau 2 et 3.
Le PDF la complète par les numéros de page : une première passe enregistre la
page de chaque titre, la seconde écrit la table définitive. Les lignes étant
identiques d'une passe à l'autre, la pagination ne bouge pas.
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "cadrage" / "dossier-de-conception-v1.md"
OUT = ROOT / "livrables" / "02-conception"
OUT.mkdir(exist_ok=True)
NAME = "dossier-de-conception-v1"

NAVY, BLUE, PALE, INK, MUTED, LINE = "12304A", "1685B4", "EAF5FA", "183346", "587184", "D7E8EF"
FOOTER = "CEFISI  •  Dossier de conception V1  •  Mattéo · Romain · Tim"
FONT_DIR = Path("C:/Windows/Fonts")
ID_COL = re.compile(r"^(F|T|NF)-\d+$")

pdfmetrics.registerFont(TTFont("CEFISI", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("CEFISI-Bold", str(FONT_DIR / "arialbd.ttf")))
pdfmetrics.registerFontFamily("CEFISI", normal="CEFISI", bold="CEFISI-Bold")


# ── lecture de la source ──────────────────────────────────────────────────────
def parse_blocks(text: str):
    blocks, i, lines = [], 0, text.splitlines()
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        if line.startswith("### "):
            blocks.append(("h2", line[4:].strip()))
        elif line.startswith("## "):
            blocks.append(("h1", line[3:].strip()))
        elif line.startswith("# "):
            blocks.append(("title", line[2:].strip()))
        elif line.startswith("- "):
            blocks.append(("bullet", line[2:].strip()))
        else:
            blocks.append(("p", line.strip()))
        i += 1
    return blocks


def plain(text: str) -> str:
    return text.replace("**", "").replace("`", "")


def runs_of(text: str):
    """Découpe « a **b** c » en [(texte, gras)]."""
    text = text.replace("`", "")
    out, pos = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*", text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False))
        out.append((m.group(1), True))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False))
    return out or [(text, False)]


def headings_of(blocks):
    """(niveau, titre) dans l'ordre, niveau 1 pour ##, 2 pour ###."""
    return [(1 if kind == "h1" else 2, plain(value))
            for kind, value in blocks if kind in ("h1", "h2")]


# ── Word ─────────────────────────────────────────────────────────────────────
def shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def word_toc(doc, headings) -> None:
    """Sommaire statique : Word n'a pas encore paginé, donc pas de numéros."""
    title = doc.add_paragraph("Table des matières", "Heading 1")
    title.paragraph_format.space_before = Pt(6)
    usable = Cm(17.6)
    for level, text in headings:
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.left_indent = Cm(0.0 if level == 1 else 0.7)
        p.paragraph_format.tab_stops.add_tab_stop(usable, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        run = p.add_run(text)
        run.font.size = Pt(9.5 if level == 1 else 8.8)
        run.bold = level == 1
        run.font.color.rgb = RGBColor.from_string(NAVY if level == 1 else INK)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def word_document(blocks):
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(1.6)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(1.7)
    section.right_margin = Cm(1.7)
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_after = Pt(5)
    for name, size, color in (("Title", 23, NAVY), ("Heading 1", 12.5, BLUE), ("Heading 2", 10.5, NAVY)):
        style = doc.styles[name]
        style.font.name = "Aptos Display"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(11)
        style.paragraph_format.space_after = Pt(5)
    footer = section.footer.paragraphs[0]
    footer.text = FOOTER
    footer.style = normal
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in footer.runs:
        run.font.size = Pt(7)
        run.font.color.rgb = RGBColor.from_string(MUTED)

    inserted = False
    for kind, value in blocks:
        if kind == "h1" and not inserted:
            word_toc(doc, headings_of(blocks))
            inserted = True
        if kind == "title":
            doc.add_paragraph(plain(value), "Title")
        elif kind == "h1":
            doc.add_paragraph(plain(value), "Heading 1")
        elif kind == "h2":
            doc.add_paragraph(plain(value), "Heading 2")
        elif kind == "bullet":
            p = doc.add_paragraph(style="List Bullet")
            for text, bold in runs_of(value):
                r = p.add_run(text)
                r.bold = bold
        elif kind == "p":
            p = doc.add_paragraph(style="Normal")
            for text, bold in runs_of(value):
                r = p.add_run(text)
                r.bold = bold
        elif kind == "table":
            rows = value
            if not rows:
                continue
            cols = len(rows[0])
            table = doc.add_table(rows=0, cols=cols)
            table.style = "Table Grid"
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            usable = 17.6
            widths = [1.0] * cols
            if ID_COL.match(rows[0][0] or ""):
                widths[0] = 0.5
            if cols >= 3:
                widths[1] = 1.3
            total = sum(widths)
            widths = [Cm(usable * w / total) for w in widths]
            for r_idx, row in enumerate(rows):
                cells = table.add_row().cells
                for c_idx, text in enumerate(row[:cols]):
                    cell = cells[c_idx]
                    cell.width = widths[c_idx]
                    p = cell.paragraphs[0]
                    p.text = ""
                    p.paragraph_format.space_after = Pt(1)
                    for chunk, bold in runs_of(text):
                        run = p.add_run(chunk)
                        run.font.size = Pt(7.6)
                        run.bold = bold or r_idx == 0
                        run.font.color.rgb = RGBColor.from_string("FFFFFF" if r_idx == 0 else INK)
                    if r_idx == 0:
                        shade(cell, NAVY)
                    elif r_idx % 2 == 0:
                        shade(cell, "F4F8FB")
                if r_idx == 0:
                    for cell in cells:
                        for p in cell.paragraphs:
                            p.paragraph_format.space_before = Pt(2)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
    doc.save(OUT / f"{NAME}.docx")


# ── PDF ──────────────────────────────────────────────────────────────────────
class PageMark(Flowable):
    """Note la page où se trouve un titre, pour la table des matières."""

    def __init__(self, store: dict, key: int):
        super().__init__()
        self.store, self.key = store, key
        self.width, self.height = 0, 0.1

    def draw(self):
        self.store[self.key] = self.canv.getPageNumber()


def pdf_styles():
    return {
        "title": ParagraphStyle("t", fontName="CEFISI-Bold", fontSize=20, leading=24,
                                textColor=colors.HexColor("#" + NAVY), spaceAfter=12),
        "h1": ParagraphStyle("h1", fontName="CEFISI-Bold", fontSize=12, leading=15,
                             textColor=colors.HexColor("#" + BLUE), spaceBefore=12, spaceAfter=6),
        "h2": ParagraphStyle("h2", fontName="CEFISI-Bold", fontSize=9.8, leading=13,
                             textColor=colors.HexColor("#" + NAVY), spaceBefore=9, spaceAfter=4),
        "body": ParagraphStyle("b", fontName="CEFISI", fontSize=8.8, leading=12.6,
                               textColor=colors.HexColor("#" + INK), spaceAfter=6),
        "bullet": ParagraphStyle("u", fontName="CEFISI", fontSize=8.6, leading=12,
                                 textColor=colors.HexColor("#" + INK), leftIndent=11,
                                 bulletIndent=2, spaceAfter=3),
        "cell": ParagraphStyle("c", fontName="CEFISI", fontSize=6.9, leading=9.2,
                               textColor=colors.HexColor("#" + INK)),
        "head": ParagraphStyle("h", fontName="CEFISI-Bold", fontSize=6.9, leading=9.2,
                               textColor=colors.white),
        "toc1": ParagraphStyle("t1", fontName="CEFISI-Bold", fontSize=8.6, leading=12,
                               textColor=colors.HexColor("#" + NAVY), spaceAfter=1),
        "toc2": ParagraphStyle("t2", fontName="CEFISI", fontSize=8.2, leading=11,
                               textColor=colors.HexColor("#" + INK), leftIndent=10, spaceAfter=1),
        "tocn": ParagraphStyle("tn", fontName="CEFISI", fontSize=8.2, leading=11,
                               textColor=colors.HexColor("#" + MUTED), alignment=2),
    }


def inline(text: str) -> str:
    parts = []
    for chunk, bold in runs_of(text):
        chunk = escape(chunk)
        parts.append(f"<b>{chunk}</b>" if bold else chunk)
    return "".join(parts)


def pdf_toc(headings, pages, styles):
    data = []
    for idx, (level, text) in enumerate(headings):
        style = styles["toc1"] if level == 1 else styles["toc2"]
        num = pages.get(idx)
        data.append([Paragraph(inline(text), style),
                     Paragraph(str(num) if num else "", styles["tocn"])])
    width = A4[0] - 2 * 1.25 * cm
    table = Table(data, colWidths=[width - 1.6 * cm, 1.6 * cm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    return [Paragraph("Table des matières", styles["h1"]), Spacer(1, 2), table, Spacer(1, 6)]


def pdf_story(blocks, styles, pages=None, marks=None):
    story, inserted = [], False
    headings = headings_of(blocks)
    index = 0
    for kind, value in blocks:
        if kind == "h1" and not inserted:
            story += pdf_toc(headings, pages or {}, styles)
            story.append(PageBreak())
            inserted = True
        if kind in ("h1", "h2") and marks is not None:
            story.append(PageMark(marks, index))
            index += 1
        if kind == "title":
            story.append(Paragraph(inline(value), styles["title"]))
        elif kind == "h1":
            story.append(Paragraph(inline(value), styles["h1"]))
        elif kind == "h2":
            story.append(Paragraph(inline(value), styles["h2"]))
        elif kind == "bullet":
            story.append(Paragraph(inline(value), styles["bullet"], bulletText="•"))
        elif kind == "p":
            story.append(Paragraph(inline(value), styles["body"]))
        elif kind == "table":
            rows = value
            if not rows:
                continue
            cols = len(rows[0])
            data = []
            for r_idx, row in enumerate(rows):
                style = styles["head"] if r_idx == 0 else styles["cell"]
                data.append([Paragraph(inline(c), style) for c in row[:cols]])
            width = A4[0] - 2 * 1.25 * cm
            weights = [1.0] * cols
            if ID_COL.match(rows[0][0] or ""):
                weights[0] = 0.5
            if cols >= 3:
                weights[1] = 1.3
            total = sum(weights)
            widths = [width * w / total for w in weights]
            table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
            style_cmds = [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#" + LINE)),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#" + NAVY)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
                ("TOPPADDING", (0, 0), (-1, -1), 2.6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8),
            ]
            for r_idx in range(1, len(data)):
                if r_idx % 2 == 0:
                    style_cmds.append(("BACKGROUND", (0, r_idx), (-1, r_idx), colors.HexColor("#F4F8FB")))
            table.setStyle(TableStyle(style_cmds))
            story.append(KeepTogether(table) if len(data) <= 8 else table)
            story.append(Spacer(1, 7))
    return story


def pdf_footer(canvas, doc):
    width, _ = doc.pagesize
    canvas.setStrokeColor(colors.HexColor("#" + LINE))
    canvas.line(36, 30, width - 36, 30)
    canvas.setFillColor(colors.HexColor("#" + MUTED))
    canvas.setFont("CEFISI", 6.8)
    canvas.drawString(36, 19, FOOTER)
    canvas.drawRightString(width - 36, 19, str(doc.page))


def pdf_document(blocks):
    styles = pdf_styles()
    target = OUT / f"{NAME}.pdf"

    def build(path, pages, marks):
        doc = SimpleDocTemplate(str(path), pagesize=A4,
                                leftMargin=1.25 * cm, rightMargin=1.25 * cm,
                                topMargin=1.5 * cm, bottomMargin=1.6 * cm,
                                title="CEFISI — Dossier de conception V1",
                                author="Mattéo, Romain, Tim")
        doc.build(pdf_story(blocks, styles, pages, marks),
                  onFirstPage=pdf_footer, onLaterPages=pdf_footer)

    marks: dict = {}
    temp = OUT / f"{NAME}.pdf.brouillon"
    build(temp, {}, marks)
    build(target, marks, None)
    temp.unlink(missing_ok=True)
    return len(marks)


# ── contrôles ────────────────────────────────────────────────────────────────
def check(blocks) -> dict:
    ids = []
    for kind, value in blocks:
        if kind != "table":
            continue
        for row in value:
            if row and ID_COL.match(row[0] or ""):
                ids.append(row[0])
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    assert not dupes, f"Identifiants dupliqués : {dupes}"
    f = [i for i in ids if i.startswith("F-")]
    t = [i for i in ids if i.startswith("T-")]
    nf = [i for i in ids if i.startswith("NF-")]
    assert len(f) == len(set(f)) and len(f) >= 20, f"Fonctionnalités : {len(f)}"
    for prefix, values in (("F", f), ("T", t), ("NF", nf)):
        numbers = sorted(int(v.split("-")[1]) for v in values)
        expected = list(range(1, len(numbers) + 1))
        assert numbers == expected, f"{prefix} non contigu : {numbers}"
    return {"fonctionnalites": len(f), "difficultes": len(t), "exigences_nf": len(nf),
            "scores_stack": check_scores_stack(blocks)}


def check_scores_stack(blocks) -> list[int]:
    """Vérifie que les totaux du classement 8.6 valent bien les points de 8.3."""
    points = None
    annonces = None
    for kind, value in blocks:
        if kind != "table" or not value:
            continue
        entete = value[0]
        if entete[0] == "Réf" and len(entete) >= 6 and entete[2].startswith("A"):
            points = [0] * (len(entete) - 2)
            for row in value[1:]:
                if not re.fullmatch(r"P\d+", row[0] or ""):
                    continue
                for i, cell in enumerate(row[2:2 + len(points)]):
                    points[i] += cell.count("●")
        if entete[0] == "Option" and "Points de facilité" in entete:
            annonces = [int(re.match(r"(\d+)", row[1]).group(1)) for row in value[1:]
                        if re.match(r"\d+", row[1] or "")]
    if points is None or annonces is None:
        return []
    assert points == annonces, f"Classement 8.6 ({annonces}) incohérent avec le tableau 8.3 ({points})"
    return points


def main():
    blocks = parse_blocks(SOURCE.read_text(encoding="utf-8"))
    stats = check(blocks)
    headings = headings_of(blocks)
    word_document(blocks)
    marked = pdf_document(blocks)
    docx = OUT / f"{NAME}.docx"
    pdf = OUT / f"{NAME}.pdf"
    print("blocs:", len(blocks))
    print("sommaire:", len(headings), "entrees •", marked, "titres pagines")
    print("contrôles:", stats)
    print("docx:", docx, docx.stat().st_size, "octets")
    print("pdf :", pdf, pdf.stat().st_size, "octets")


if __name__ == "__main__":
    main()
