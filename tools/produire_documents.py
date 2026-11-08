"""Génère les livrables Word et PDF à partir des notes locales.

Prérequis : python-docx, reportlab. Aucun accès réseau.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "livrables" / "01-cadrage"
OUT.mkdir(parents=True, exist_ok=True)
NAVY, BLUE, PALE, INK, MUTED = "12304A", "1685B4", "EAF5FA", "183346", "587184"
FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("CEFISI", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("CEFISI-Bold", str(FONT_DIR / "arialbd.ttf")))
pdfmetrics.registerFontFamily("CEFISI", normal="CEFISI", bold="CEFISI-Bold")


def plain(text: str) -> str:
    return text.replace("**", "").replace("`", "").strip()


def hexcolor(value: str):
    return colors.HexColor("#" + value)


def shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def setup_word(doc: Document, wide: bool = False) -> None:
    section = doc.sections[0]
    if wide:
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width, section.page_height = Cm(29.7), Cm(21)
    section.top_margin = Cm(1.6)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(1.7)
    section.right_margin = Cm(1.7)
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_after = Pt(5)
    for name, size in [("Title", 23), ("Heading 1", 12.5)]:
        style = doc.styles[name]
        style.font.name = "Aptos Display"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(NAVY)
        style.paragraph_format.space_before = Pt(11)
        style.paragraph_format.space_after = Pt(5)
    footer = section.footer.paragraphs[0]
    footer.text = "CEFISI  •  Document de travail  •  Mattéo · Romain · Tim"
    footer.style = normal
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in footer.runs:
        run.font.size = Pt(7)
        run.font.color.rgb = RGBColor.from_string(MUTED)


def pdf_styles():
    return {
        "body": ParagraphStyle("body", fontName="CEFISI", fontSize=9.3, leading=14,
            textColor=hexcolor(INK), spaceAfter=7),
        "title": ParagraphStyle("title", fontName="CEFISI-Bold", fontSize=21, leading=25,
            textColor=hexcolor(NAVY), spaceAfter=13),
        "h1": ParagraphStyle("h1", fontName="CEFISI-Bold", fontSize=12, leading=16,
            textColor=hexcolor(BLUE), spaceBefore=10, spaceAfter=6),
        "small": ParagraphStyle("small", fontName="CEFISI", fontSize=8.4, leading=12,
            textColor=hexcolor(INK), spaceAfter=5),
    }


def pdf_footer(c, document):
    w, _ = document.pagesize
    c.setStrokeColor(hexcolor("D7E8EF"))
    c.line(42, 38, w - 42, 38)
    c.setFillColor(hexcolor(MUTED))
    c.setFont("CEFISI", 7)
    c.drawString(42, 25, "CEFISI  •  Document de travail  •  Mattéo · Romain · Tim")
    c.drawRightString(w - 42, 25, str(document.page))


def markdown_lines(path: Path):
    return path.read_text(encoding="utf-8").splitlines()


def make_note():
    lines = markdown_lines(ROOT / "docs/cadrage/note-de-cadrage-v1.md")
    doc = Document()
    setup_word(doc)
    styles = pdf_styles()
    story = []
    for line in lines:
        if not line.strip():
            continue
        if line.startswith("# "):
            title = plain(line[2:])
            doc.add_paragraph(title, "Title")
            story.append(Paragraph(escape(title), styles["title"]))
        elif line.startswith("## "):
            heading = plain(line[3:])
            doc.add_paragraph(heading, "Heading 1")
            story.append(Paragraph(escape(heading), styles["h1"]))
        else:
            p = doc.add_paragraph(style="Normal")
            text = plain(line)
            if line.startswith("- "):
                p.style = "List Bullet"
                text = plain(line[2:])
                story.append(Paragraph("• " + escape(text), styles["small"]))
            elif re.match(r"\d+\. ", line):
                story.append(Paragraph(escape(text), styles["small"]))
            else:
                story.append(Paragraph(escape(text), styles["body"]))
            p.add_run(text)
    doc.save(OUT / "note-de-cadrage-v1.docx")
    pdf = SimpleDocTemplate(str(OUT / "note-de-cadrage-v1.pdf"), pagesize=A4,
        leftMargin=45, rightMargin=45, topMargin=42, bottomMargin=50,
        title="CEFISI — Note de cadrage V1", author="Mattéo, Romain, Tim")
    pdf.build(story, onFirstPage=pdf_footer, onLaterPages=pdf_footer)


def load_cards():
    lines = markdown_lines(ROOT / "docs/pilotage/suivi.md")
    cards = []
    for line in lines:
        if not line.startswith("| ") or line.startswith("|---") or line.startswith("| Livrable"):
            continue
        parts = [x.strip() for x in line.strip("| ").split("|")]
        if len(parts) == 4:
            cards.append(dict(title=parts[0], state=parts[1], owner=parts[2], next=parts[3]))
    assert len(cards) == 6, f"Attendu : 6 livrables ; obtenu : {len(cards)}"
    return cards


def word_card(cell, card):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    r = p.add_run(card["title"])
    r.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor.from_string(NAVY)
    for text in (card["next"], "Responsable : " + card["owner"]):
        p = cell.add_paragraph(text)
        p.paragraph_format.space_after = Pt(4)
        for run in p.runs:
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor.from_string(MUTED if text.startswith("Responsable") else INK)


def make_board_word(cards):
    doc = Document()
    setup_word(doc, wide=True)
    doc.add_paragraph("TABLEAU DE SUIVI", "Subtitle")
    doc.add_paragraph("Refonte du site CEFISI", "Title")
    doc.add_paragraph("6 livrables  ·  4 à préparer  ·  1 suivi évolutif  ·  1 à relire  ·  Responsables à définir")
    p = doc.add_paragraph("Vue Kanban — aucun calendrier détaillé fixé avant validation collective.")
    p.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
    table = doc.add_table(rows=2, cols=3)
    table.autofit = False
    for i, width in enumerate((Cm(8.6), Cm(8.6), Cm(8.6))):
        table.columns[i].width = width
    groups = [cards[1:5], cards[5:], cards[:1]]
    for idx, (label, group) in enumerate(zip(("À PRÉPARER  /  4", "SUIVI CONTINU  /  1", "À RELIRE  /  1"), groups)):
        header = table.cell(0, idx)
        shade(header, NAVY if idx == 0 else (BLUE if idx == 1 else "3F6C7C"))
        hp = header.paragraphs[0]
        hr = hp.add_run(label)
        hr.bold = True
        hr.font.size = Pt(10)
        hr.font.color.rgb = RGBColor(255, 255, 255)
        cell = table.cell(1, idx)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        shade(cell, "F1F7FA" if idx == 0 else ("F7FAFB" if idx == 1 else "EEF6F4"))
        cell.paragraphs[0].text = ""
        if not group:
            cell.add_paragraph("Aucune tâche démarrée — état à mettre à jour ensemble.")
        for card in group:
            word_card(cell, card)
    doc.add_paragraph("À confirmer : répartition Mattéo / Romain / Tim, dates et formats de remise.")
    doc.save(OUT / "suivi-kanban-v1.docx")


def draw_board_pdf(cards):
    path = OUT / "suivi-kanban-v1.pdf"
    c = canvas.Canvas(str(path), pagesize=landscape(A4))
    width, height = landscape(A4)
    c.setTitle("CEFISI — Tableau de suivi Kanban V1")
    c.setFillColor(hexcolor(NAVY))
    c.rect(0, height - 130, width, 130, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("CEFISI-Bold", 11)
    c.drawString(36, height - 37, "CEFISI  /  PROJET WEB")
    c.setFont("CEFISI-Bold", 27)
    c.drawString(36, height - 79, "Tableau de suivi")
    c.setFont("CEFISI", 10)
    c.drawString(36, height - 104, "Vue Kanban  •  Mattéo · Romain · Tim  •  Version de travail")
    c.setFillColor(hexcolor(MUTED))
    c.setFont("CEFISI", 9)
    c.drawString(36, height - 152, "6 livrables     4 à préparer     1 suivi évolutif     1 à relire")
    c.drawRightString(width - 36, height - 152, "Responsables et échéances à définir")
    x0, gutter = 36, 13
    col_w = (width - 72 - gutter * 2) / 3
    top, bottom = height - 165, 60
    groups = [cards[1:5], cards[5:], cards[:1]]
    headers = [("À PRÉPARER", NAVY), ("SUIVI CONTINU", BLUE), ("À RELIRE", "3F6C7C")]
    st = ParagraphStyle("card", fontName="CEFISI", fontSize=8, leading=11, textColor=hexcolor(INK))
    for idx, (group, (label, color)) in enumerate(zip(groups, headers)):
        x = x0 + idx * (col_w + gutter)
        c.setFillColor(hexcolor("F2F7F9"))
        c.roundRect(x, bottom, col_w, top - bottom, 10, stroke=0, fill=1)
        c.setFillColor(hexcolor(color))
        c.roundRect(x, top - 36, col_w, 36, 8, stroke=0, fill=1)
        c.rect(x, top - 36, col_w, 8, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("CEFISI-Bold", 10)
        c.drawString(x + 13, top - 23, label)
        c.drawRightString(x + col_w - 13, top - 23, str(len(group)))
        y = top - 48
        if not group:
            c.setFillColor(hexcolor(MUTED))
            c.setFont("CEFISI", 9)
            c.drawString(x + 13, y - 20, "Aucune tâche démarrée.")
        for card in group:
            card_h = 59 if idx == 0 else 94
            c.setFillColor(colors.white)
            c.roundRect(x + 9, y - card_h, col_w - 18, card_h, 7, stroke=0, fill=1)
            c.setFillColor(hexcolor(BLUE))
            c.roundRect(x + 9, y - card_h, 3, card_h, 1, stroke=0, fill=1)
            c.setFillColor(hexcolor(NAVY))
            c.setFont("CEFISI-Bold", 10)
            c.drawString(x + 20, y - 17, card["title"][:39])
            para = Paragraph(escape(card["next"]), st)
            _, h = para.wrap(col_w - 42, 38)
            para.drawOn(c, x + 20, y - 24 - h)
            c.setFillColor(hexcolor(MUTED))
            c.setFont("CEFISI", 7.5)
            c.drawString(x + 20, y - card_h + 8, "Responsable : " + card["owner"])
            y -= card_h + 4
        assert y >= bottom - 2, "Cartes hors de la page"
    c.setStrokeColor(hexcolor("D7E8EF"))
    c.line(36, 48, width - 36, 48)
    c.setFillColor(hexcolor(MUTED))
    c.setFont("CEFISI", 8)
    c.drawString(36, 32, "À confirmer ensemble : répartition, dates et formats de remise.")
    c.drawRightString(width - 36, 32, "CEFISI  •  1 / 1")
    c.save()


def make_journal_word():
    lines = markdown_lines(ROOT / "docs/observations/journal.md")
    doc = Document()
    setup_word(doc, wide=True)
    doc.add_paragraph("Journal d’observations", "Title")
    doc.add_paragraph("Distinguer les constats vérifiés, les retours du groupe et les hypothèses. Ne pas confondre un échec de l’outil de navigation avec une panne du site.")
    for line in lines:
        if not line.startswith("| OBS-"):
            continue
        parts = [x.strip() for x in line.strip("| ").split("|")]
        if len(parts) != 5:
            continue
        doc.add_paragraph(parts[0] + "  ·  " + parts[1], "Heading 1")
        for label, value in zip(("Source", "Constat", "Statut / suite"), parts[2:]):
            p = doc.add_paragraph()
            r = p.add_run(label + " : ")
            r.bold = True
            p.add_run(plain(value))
    doc.add_paragraph("À compléter lors des visites", "Heading 1")
    doc.add_paragraph("Pour chaque nouvelle observation : date et heure, URL, appareil, navigateur, état de connexion, résultat exact, capture éventuelle, vérification suivante.")
    doc.save(OUT / "journal-observations-v1.docx")


if __name__ == "__main__":
    cards = load_cards()
    make_note()
    make_board_word(cards)
    draw_board_pdf(cards)
    make_journal_word()
    for path in sorted(OUT.iterdir()):
        print(path.name, path.stat().st_size, "octets")
