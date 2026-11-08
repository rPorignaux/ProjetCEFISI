"""Générer le catalogue CEFISI depuis l'audit réel des pages et CSS.

Sorties : livrables/inventaire-site-cefisi.docx et .xlsx.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "docs" / "observations"
OUT = ROOT / "livrables"
AUDIT = json.loads((OBS / "site-audit.json").read_text(encoding="utf-8"))
RENDERED = json.loads((OBS / "site-rendered.json").read_text(encoding="utf-8"))
CSS = json.loads((OBS / "site-css.json").read_text(encoding="utf-8"))
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)", re.I)
IMAGE_EXT = re.compile(r"\.(png|jpe?g|gif|webp|avif|svg|ico)$", re.I)

UTILITY = {
    "/": ("Accueil", "Présenter le CEFISI, les formations, les financements et l'accès à la candidature externe."),
    "/notre-approche/": ("Approche pédagogique", "Expliquer l'approche du centre et la préparation aux métiers des systèmes d'information."),
    "/nos-formations/": ("Catalogue des formations", "Présenter les parcours et orienter vers leurs fiches détaillées."),
    "/formation-concepteur-developpeur-informatique/": ("Formation concepteur-développeur", "Décrire la formation de conception et développement d'applications et ses modalités publiées."),
    "/formation-moa-en-si/": ("Formation MOA en SI", "Décrire le parcours de maîtrise d'ouvrage des systèmes d'information."),
    "/chef-de-projet-en-solutions-blockchain/": ("Formation blockchain", "Décrire le parcours de chef de projet en solutions blockchain."),
    "/no-code/": ("Formation CDA / no-code", "Présenter le parcours de conception-développement d'applications avec no-code."),
    "/equipe/": ("Équipe", "Présenter l'équipe et ouvrir les fiches individuelles."),
    "/richard-francois/": ("Portrait — Richard François", "Présenter le parcours de Richard François."),
    "/romain-barcelo/": ("Portrait — Romain Barcelo", "Présenter le parcours de Romain Barcelo."),
    "/christophe-gnaho/": ("Portrait — Christophe Gnaho", "Présenter le parcours de Christophe Gnaho."),
    "/alain-chetcuti/": ("Portrait — Alain Chetcuti", "Présenter le parcours d'Alain Chetcuti."),
    "/yassir-kazar/": ("Portrait — Yassir Kazar", "Présenter le parcours de Yassir Kazar."),
    "/houda-kharmach/": ("Portrait — Houda Kharmach", "Présenter le parcours de Houda Kharmach."),
    "/jean-francois-bonnet/": ("Portrait — Jean-François Bonnet", "Présenter le parcours de Jean-François Bonnet."),
    "/karima-oubekkou/": ("Portrait — Manon Oubekkou", "La page affiche « Manon Oubekkou » ; l'URL conserve « karima-oubekkou » (écart à vérifier)."),
    "/michel-plasse/": ("Portrait — Michel Plasse", "Présenter le parcours de Michel Plasse."),
    "/contactez-nous/": ("Contact et accès", "Indiquer les coordonnées et le plan d'accès au centre."),
    "/certification-qualiopi/": ("Certification Qualiopi", "Présenter le certificat Qualiopi publié par le centre."),
    "/politique-de-confidentialite/": ("Confidentialité", "Informer sur le traitement des données personnelles et les cookies."),
    "/login/": ("Connexion", "Page d'authentification, non explorée."),
    "/tableau-de-bord/": ("Tableau de bord", "Espace de tableau de bord : accès et fonctions internes non vérifiés."),
    "/wiki/": ("Wiki", "Lien vers un wiki ; contenu et accès non vérifiés."),
    "/publier-une-offre-demploi/": ("Publier une offre", "Page liée à la publication d'offres ; accès et fonctionnement non vérifiés."),
    "/tableau-de-bord-des-offres-demploi/": ("Tableau de bord des offres", "Redirige vers la connexion sans authentification."),
    "/offres-demploi/": ("Offres d'emploi", "Redirige vers la connexion sans authentification."),
    "/moa/": ("Article « MOA »", "Redirige vers la connexion sans authentification ; contenu non vérifié."),
    "/category/non-classe/": ("Archive non classée", "Redirige vers la connexion sans authentification ; contenu non vérifié."),
    "/documents-cours/": ("Documents de cours", "Lien de navigation repéré ; accès et contenu non vérifiés."),
    "/documents-direction/": ("Documents de direction", "Lien de navigation repéré ; accès et contenu non vérifiés."),
    "/gestion-des-documents-de-cours/": ("Gestion des documents de cours", "Lien de navigation repéré ; accès et contenu non vérifiés."),
}

ASSET_NAME = {
    "logo-clair.png": "Logo CEFISI — version claire",
    "qualiopi_logo_retrouche.webp": "Logo Qualiopi — pied de page",
    "Picto_datadocke-small.jpg": "Pictogramme Datadock — pied de page",
    "6129291.jpg": "Photo d'un groupe d'étudiants — bannière commune",
    "6129291-800x600.jpg": "Photo d'un groupe d'étudiants — variante de bannière",
    "footer-hero.png": "Image décorative footer-hero du thème",
    "android-chrome-192x192.png": "Icône de site — Android Chrome",
    "cropped-Picto-32x32.png": "Icône de site — 32 × 32",
    "cropped-Picto-192x192.png": "Icône de site — 192 × 192",
    "cropped-Picto-180x180.png": "Icône de site — 180 × 180",
    "image-21-juil-2025-18-06-48-1024x683.png": "Graphique de l'insertion après formation",
    "logo-cpf.jpg": "Logo Compte personnel de formation (CPF)",
    "logo-fongecif.jpg": "Logo Fongecif",
    "logo-france-travail-rvb-carre-coul-positif-150x150.png": "Logo France Travail",
    "logo-ridf-2019-couleur.png": "Logo Région Île-de-France",
    "logo-ridf-2019-couleur-300x110.png": "Logo Région Île-de-France — variante 300 px",
    "logo-ridf-2019-couleur-768x281.png": "Logo Région Île-de-France — variante 768 px",
    "yogosha1-e1789083738170-270x76.png": "Logo Yogosha",
    "logo-afm-telethon-280x50.png": "Logo AFM-Téléthon",
    "3axes-300x173.png": "Schéma des trois axes — variante 300 px",
    "3axes.png": "Schéma des trois axes",
    "Karima-carre.jpg": "Portrait de Manon Oubekkou (nom du fichier différent)",
    "unnamed-2.jpg": "Portrait de Romain Barcelo",
}
PORTRAITS = {
    "richard.francois.jpg": "Richard François",
    "christophe.gnaho_.jpg": "Christophe Gnaho",
    "yassir.kazar_.jpg": "Yassir Kazar",
    "jean-francois.bonnet.jpg": "Jean-François Bonnet",
    "michel.plasse.jpg": "Michel Plasse",
    "alain.chetcuti.jpg": "Alain Chetcuti",
    "houda.kharmach.jpg": "Houda Kharmach",
}


def name_for(url, alt=""):
    filename = Path(urlparse(url).path).name
    if filename in ASSET_NAME:
        return ASSET_NAME[filename]
    if filename in PORTRAITS:
        return f"Portrait de {PORTRAITS[filename]}"
    return alt or f"Fichier {filename}"


def page_label(url):
    return UTILITY.get(urlparse(url).path, (Path(urlparse(url).path).name, "Rôle non vérifié"))[0]


def build_media():
    uses: dict[tuple[str, str], dict] = {}
    for page in AUDIT["pages"].values():
        if page["status"] != "public observé":
            continue
        owner = page["url"]
        for asset in page["assets"]:
            key = owner, asset["url"]
            row = uses.setdefault(key, {"page": owner, "url": asset["url"], "name": name_for(asset["url"], asset["alt"]), "zones": set(), "sources": set(), "alt": set()})
            row["zones"].add(asset["zone"])
            row["sources"].add(asset["source"])
            if asset["alt"]:
                row["alt"].add(asset["alt"])
        rendered = RENDERED.get(owner, {})
        for item in rendered.get("items", []):
            raw_urls = [item.get("src"), item.get("currentSrc")]
            if item.get("srcset"):
                raw_urls.extend(part.strip().split(" ")[0] for part in item["srcset"].split(","))
            raw_urls.extend(CSS_URL.findall(item.get("style") or ""))
            for raw in raw_urls:
                if not raw or raw.startswith("data:"):
                    continue
                url = urljoin(owner, raw)
                if not IMAGE_EXT.search(urlparse(url).path):
                    continue
                key = owner, url
                row = uses.setdefault(key, {"page": owner, "url": url, "name": name_for(url, item.get("alt") or ""), "zones": set(), "sources": set(), "alt": set()})
                row["zones"].add(item.get("zone") or "gabarit")
                row["sources"].add("DOM rendu : " + (item.get("tag") or "élément"))
                if item.get("alt"):
                    row["alt"].add(item["alt"])
    by_url = defaultdict(set)
    for page, url in uses:
        by_url[url].add(page)
    # Les portraits présents sur l'équipe et sur une fiche personnelle
    # restent des médias de ces deux pages : ils ne sont pas génériques.
    common_urls = {url for url, pages in by_url.items() if len(pages) >= 3}
    for row in uses.values():
        for field in ("zones", "sources", "alt"):
            row[field] = "; ".join(sorted(row[field]))
    per_page = sorted((row for row in uses.values() if row["url"] not in common_urls), key=lambda row: (row["page"], row["name"], row["url"]))
    common = []
    for url in sorted(common_urls):
        rows = [row for row in uses.values() if row["url"] == url]
        common.append({"name": name_for(url), "url": url, "first": min(by_url[url]), "pages": len(by_url[url]), "zone": "; ".join(sorted({r["zones"] for r in rows})), "source": "; ".join(sorted({r["sources"] for r in rows})), "page_list": "; ".join(sorted(by_url[url]))})
    return per_page, common, by_url


def add_rows(ws, headings, rows, widths, url_columns=()):
    ws.append(headings)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headings))}{max(2, len(rows)+1)}"
    for row in rows:
        ws.append(row)
    for c in ws[1]:
        c.fill = PatternFill("solid", fgColor="17345C")
        c.font = Font(color="FFFFFF", bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[1].height = 34
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.column in url_columns and isinstance(cell.value, str) and cell.value.startswith("http"):
                cell.hyperlink = cell.value
                cell.font = Font(color="1464A0", underline="single")
    ws.sheet_view.showGridLines = False


def spreadsheet(pages, per_page, common, by_url):
    wb = Workbook()
    ws = wb.active
    ws.title = "Pages"
    rows = []
    for page in pages:
        url = page["url"]
        label, utility = UTILITY.get(urlparse(url).path, (page["title"], "Rôle non vérifié"))
        rows.append([label, url, utility, page["status"], page.get("http"), page.get("final_url", ""), page.get("sitemap", ""), page.get("title", "")])
    for path in ("/documents-cours/", "/documents-direction/", "/gestion-des-documents-de-cours/"):
        url = urljoin("https://www.cefisi.com/", path)
        label, utility = UTILITY[path]
        rows.append([label, url, utility, "Lien de navigation ; non visité", "", "", "hors sitemap", ""])
    add_rows(ws, ["Page", "URL", "Utilité / fonction observée ou présumée", "État de l'audit", "HTTP", "URL après redirection", "Source", "Titre HTML"], rows, [35, 73, 85, 40, 12, 75, 25, 65], (2, 6))
    ws = wb.create_sheet("Médias par page")
    add_rows(ws, ["Page", "URL de la page", "Nom du média", "URL du média", "Zone repérée", "Source dans le code / rendu", "Texte alternatif"], [[page_label(r["page"]), r["page"], r["name"], r["url"], r["zones"], r["sources"], r["alt"]] for r in per_page], [37, 74, 52, 110, 43, 63, 30], (2, 4))
    ws = wb.create_sheet("Éléments communs")
    add_rows(ws, ["Nom / type", "URL du média", "Pages observées (nombre)", "Première page repérée", "Zone dans le gabarit", "Source dans le code / rendu", "Toutes les pages concernées"], [[r["name"], r["url"], r["pages"], r["first"], r["zone"], r["source"], r["page_list"]] for r in common], [50, 105, 20, 70, 42, 70, 110], (2, 4))
    ws = wb.create_sheet("Images en CSS commun")
    add_rows(ws, ["Nom du fichier", "URL du média", "Feuille CSS qui le référence", "Extrait de code", "Statut"], [[name_for(r["url"]), r["url"], r["stylesheet"], r["code_excerpt"], "Référence dans CSS ; affichage non confirmé"] for r in CSS["assets"]], [45, 110, 105, 105, 44], (2, 3))
    ws = wb.create_sheet("Méthode et limites")
    notes = [
        ["Périmètre", "28 URL issues des sitemaps pages/articles/catégorie, plus trois URL de navigation hors sitemap. Les sous-routes génériques de réseau social générées par le thème ne sont pas énumérées individuellement."],
        ["Observation", "20 pages publiques chargées sans authentification ; 4 URL non explorées car a priori privées ; 4 redirections vers la page de connexion. L'inventaire média couvre uniquement les 20 pages chargées."],
        ["Médias", "HTML (images, srcset, arrière-plans inline, icônes et métadonnées) et DOM rendu après défilement. Une même image dans plusieurs sources est regroupée par page et URL ; les variantes de résolution restent des URL distinctes."],
        ["Éléments communs", "Une URL observée sur au moins trois pages publiques est placée dans l'onglet commun. Les portraits de l'équipe partagés avec leur fiche personnelle restent dans les pages respectives."],
        ["CSS", f"{CSS['stylesheets_checked']} feuilles CSS locales chargées sur l'accueil ont été lues ; les images de bibliothèque sont des références de code, pas des images dont l'affichage est prouvé."],
        ["Limite", "Les images d'espaces privés, contenus conditionnels, pages non indexées, images chargées par interactions et ressources externes non capturées ne sont pas garanties couvertes."],
        ["Candidatures", "Le bouton de candidature de l'accueil mène à une plateforme distincte ; son contenu n'est pas inclus dans cet inventaire."],
        ["Droits", "La présence d'une URL d'image ne démontre pas le droit de la reproduire dans une nouvelle charte."],
        ["Audit", f"Dernière collecte du contenu : {AUDIT.get('updated_at','non renseigné')}; CSS : {CSS.get('checked_at','non renseigné')}."]
    ]
    add_rows(ws, ["Sujet", "Note"], notes, [30, 145])
    target = OUT / "inventaire-site-cefisi.xlsx"
    wb.save(target)
    return target, len(rows)


def word(pages, per_page, common, by_url):
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.7)
    sec.left_margin = Cm(2)
    sec.right_margin = Cm(2)
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(9)
    normal.font.color.rgb = RGBColor(34, 48, 70)
    for style in ("Title", "Heading 1", "Heading 2"):
        doc.styles[style].font.color.rgb = RGBColor(25, 55, 94)
    doc.add_heading("Inventaire du site CEFISI", 0)
    doc.add_paragraph("Pages publiques, fonctions et médias — état observé avant proposition de charte et de maquettes.")
    doc.add_paragraph("Site concerné : https://www.cefisi.com/ ; la plateforme distincte de candidatures n'est pas auditée ici.")
    public = sum(p["status"] == "public observé" for p in pages)
    doc.add_paragraph(f"Repérage : {len(pages)} URL de sitemap, {public} pages publiques ouvertes, trois liens supplémentaires trouvés dans la navigation. Les accès réservés ne sont pas explorés.")
    doc.add_heading("1. Pages et fonctions", level=1)
    table = doc.add_table(rows=1, cols=3)
    table.style = "Light Shading Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, text in zip(table.rows[0].cells, ("Page", "Utilité / fonction", "État")):
        c.text = text
    for page in pages:
        label, utility = UTILITY.get(urlparse(page["url"]).path, (page["title"], "Non vérifié"))
        cells = table.add_row().cells
        cells[0].text = label + "\n" + page["url"]
        cells[1].text = utility
        cells[2].text = page["status"]
    for path in ("/documents-cours/", "/documents-direction/", "/gestion-des-documents-de-cours/"):
        label, utility = UTILITY[path]
        cells = table.add_row().cells
        cells[0].text = label + "\n" + urljoin("https://www.cefisi.com/", path)
        cells[1].text = utility
        cells[2].text = "Navigation ; non visité"
    doc.add_paragraph("Observation à vérifier : la fiche située à /karima-oubekkou/ affiche le nom Manon Oubekkou. Ce décalage d'URL et d'intitulé n'est pas corrigé dans l'inventaire.")
    doc.add_heading("2. Médias par page", level=1)
    doc.add_paragraph("Les liens ci-dessous concernent les contenus propres aux pages. Les variantes de taille sont maintenues et les ressources du gabarit commun sont dans la section suivante.")
    for page in pages:
        if page["status"] != "public observé":
            continue
        label = page_label(page["url"])
        doc.add_heading(label, level=2)
        doc.add_paragraph(page["url"])
        assets = [r for r in per_page if r["page"] == page["url"]]
        if not assets:
            doc.add_paragraph("Aucune image propre à cette page relevée hors gabarit commun.")
        for r in assets:
            doc.add_paragraph(r["name"] + " — " + r["zones"], style="List Bullet")
            doc.add_paragraph(r["url"])
    doc.add_heading("3. Images et logos du gabarit commun", level=1)
    doc.add_paragraph("Ces ressources ont été repérées sur plusieurs pages (au moins trois) : leur nombre de pages et leur zone d'apparition figurent dans le classeur détaillé.")
    for r in common:
        doc.add_paragraph(f"{r['name']} — {r['pages']} pages — {r['zone']}", style="List Bullet")
        doc.add_paragraph(r["url"])
    doc.add_heading("4. Ressources d'images référencées dans le CSS", level=1)
    doc.add_paragraph(f"{len(CSS['assets'])} références relevées dans {CSS['stylesheets_checked']} CSS locales chargées par l'accueil : icônes de plugins, contrôles et illustrations d'interface. Leur affichage sur les pages n'est pas établi. Pour les URL et le fichier CSS d'origine de chaque ressource, voir l'onglet « Images en CSS commun » du classeur.")
    doc.add_heading("Méthode et limites", level=1)
    doc.add_paragraph("Sitemaps publics et liens de navigation, lecture de l'HTML, puis contrôle du DOM rendu après défilement. Les références à une même image sont regroupées par page ; les variantes de résolution sont conservées. Les portraits utilisés dans la liste d'équipe et sur une fiche individuelle restent rattachés aux deux pages. Les zones de gabarit sont estimées à partir du DOM et du code source ; elles peuvent demander une vérification visuelle.")
    doc.add_paragraph("Non couvert : images des espaces nécessitant une authentification, pages non indexées et non liées, contenu chargé seulement après interaction, réutilisation juridique des médias. Une URL repérée n'établit pas un droit d'utilisation.")
    target = OUT / "inventaire-site-cefisi.docx"
    doc.save(target)
    return target


def main():
    pages = list(AUDIT["pages"].values())
    if len(pages) != len(AUDIT["seed"]):
        raise RuntimeError("Collecte incomplète : pages et sitemap ne concordent pas")
    if len(RENDERED) != sum(p["status"] == "public observé" for p in pages):
        raise RuntimeError("Contrôle DOM incomplet")
    per_page, common, by_url = build_media()
    OUT.mkdir(parents=True, exist_ok=True)
    xlsx, count_pages = spreadsheet(pages, per_page, common, by_url)
    docx = word(pages, per_page, common, by_url)
    print(json.dumps({"pages": count_pages, "pages_public": len(RENDERED), "media_page_uses": len(per_page), "common_media": len(common), "css_media": len(CSS["assets"]), "xlsx": str(xlsx), "docx": str(docx)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
