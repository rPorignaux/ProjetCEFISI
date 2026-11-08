"""Télécharger localement les médias publics inventoriés sur cefisi.com.

Crée médias/pages, communs, css et un manifeste de provenance. Aucun
contenu authentifié n'est téléchargé par ce script. Ne pas publier ces copies
sans vérification des droits de réutilisation.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import time
import unicodedata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from PIL import Image

from produire_inventaire_site import CSS, ROOT, build_media, name_for

DEST = ROOT / "medias" / "site-actuel"
MAX_BYTES = 12_000_000
FIELDS = ["classement", "page_ou_css", "zone", "nom", "url_source", "fichier_local", "etat", "http", "octets", "sha256", "type_contenu"]


def slug(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:70] or "media"


def filename(url: str, label: str) -> str:
    extension = Path(urlparse(url).path).suffix.lower()
    return f"{slug(label)}-{hashlib.sha256(url.encode()).hexdigest()[:8]}{extension}"


def css_group(url: str) -> str:
    path = urlparse(url).path
    match = re.search(r"/wp-content/plugins/([^/]+)/", path)
    if match:
        return "plugin-" + slug(match.group(1))
    match = re.search(r"/wp-content/themes/([^/]+)/", path)
    if match:
        return "theme-" + slug(match.group(1))
    return "wordpress-core"


def common_group(zone: str, url: str) -> str:
    if "footer" in url.lower() or "pied de page" in zone:
        return "pied-de-page"
    if "icon" in url.lower() or "picto" in url.lower() or "android-chrome" in url.lower():
        return "icones-site"
    if "en-tête" in zone:
        return "en-tete-bannieres"
    return "gabarit"


def validated_download(url: str):
    req = Request(url, headers={"User-Agent": "CEFISI-project-public-inventory/1.0", "Accept": "image/*,*/*;q=0.8"})
    try:
        with urlopen(req, timeout=20) as response:
            status = response.status
            final = response.geturl()
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
            data = response.read(MAX_BYTES + 1)
    except HTTPError as exc:
        return None, exc.code, "", f"HTTP {exc.code}"
    except (URLError, TimeoutError, OSError) as exc:
        return None, None, "", f"réseau : {type(exc).__name__}"
    if urlparse(final).hostname not in {"www.cefisi.com", "cefisi.com"}:
        return None, status, content_type, "redirection hors du site"
    if len(data) > MAX_BYTES:
        return None, status, content_type, "image > 12 Mo"
    extension = Path(urlparse(url).path).suffix.lower()
    try:
        if extension == ".svg":
            root = ElementTree.fromstring(data)
            if root.tag.rsplit("}", 1)[-1].lower() != "svg":
                raise ValueError("SVG inattendu")
        else:
            with Image.open(io.BytesIO(data)) as image:
                image.verify()
    except (ValueError, OSError, ElementTree.ParseError) as exc:
        return None, status, content_type, f"données non reconnues comme image : {type(exc).__name__}"
    return data, status, content_type, "téléchargé"


def list_jobs():
    per_page, common, _ = build_media()
    jobs = []
    for item in per_page:
        page_slug = urlparse(item["page"]).path.strip("/") or "accueil"
        jobs.append({"kind": "page", "context": item["page"], "zone": item["zones"], "label": item["name"], "url": item["url"], "relative": Path("pages") / slug(page_slug) / filename(item["url"], item["name"])})
    for item in common:
        jobs.append({"kind": "commun", "context": item["page_list"], "zone": item["zone"], "label": item["name"], "url": item["url"], "relative": Path("communs") / common_group(item["zone"], item["url"]) / filename(item["url"], item["name"])})
    for item in CSS["assets"]:
        jobs.append({"kind": "css-reference", "context": item["stylesheet"], "zone": "CSS chargé sur l'accueil ; affichage non confirmé", "label": name_for(item["url"]), "url": item["url"], "relative": Path("css") / css_group(item["stylesheet"]) / filename(item["url"], name_for(item["url"]))})
    return jobs


def write_manifest(rows):
    DEST.mkdir(parents=True, exist_ok=True)
    with (DEST / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    (DEST / "bilan.json").write_text(json.dumps({"total_references": len(rows), "downloaded_or_copied": sum(r["etat"] in {"téléchargé", "copié", "déjà présent"} for r in rows), "failures": [r for r in rows if r["etat"] not in {"téléchargé", "copié", "déjà présent"}]}, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    jobs = list_jobs()
    try:
        with urlopen(Request("https://www.cefisi.com/", headers={"User-Agent": "CEFISI-project-public-inventory/1.0"}), timeout=8) as response:
            if response.status != 200:
                raise RuntimeError(f"Accueil HTTP {response.status}")
    except (URLError, TimeoutError, OSError) as exc:
        raise SystemExit(f"Site indisponible : téléchargement interrompu avant de poursuivre ({type(exc).__name__})") from exc
    cache: dict[str, tuple[Path, int, str, str]] = {}
    rows = []
    consecutive_network_failures = 0
    for idx, job in enumerate(jobs, 1):
        target = DEST / job["relative"]
        url = job["url"]
        state = ""
        status = None
        content_type = ""
        if url in cache:
            source, status, content_type, digest = cache[url]
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == digest:
                state = "déjà présent"
            else:
                shutil.copyfile(source, target)
                state = "copié"
        elif target.exists():
            data = target.read_bytes()
            try:
                if target.suffix.lower() == ".svg":
                    if ElementTree.fromstring(data).tag.rsplit("}", 1)[-1].lower() != "svg":
                        raise ValueError("SVG inattendu")
                else:
                    with Image.open(io.BytesIO(data)) as image:
                        image.verify()
                digest = hashlib.sha256(data).hexdigest()
                status, content_type, state = 200, "image locale vérifiée", "déjà présent"
                cache[url] = target, status, content_type, digest
            except (ValueError, OSError, ElementTree.ParseError):
                digest, state = "", "fichier local illisible ; non écrasé"
        else:
            data, status, content_type, state = validated_download(url)
            if data is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                temporary = target.with_suffix(target.suffix + ".part")
                temporary.write_bytes(data)
                temporary.replace(target)
                digest = hashlib.sha256(data).hexdigest()
                cache[url] = target, status, content_type, digest
            else:
                digest = ""
            time.sleep(1.5)
        rows.append({"classement": job["kind"], "page_ou_css": job["context"], "zone": job["zone"], "nom": job["label"], "url_source": url, "fichier_local": job["relative"].as_posix() if target.exists() else "", "etat": state, "http": status or "", "octets": target.stat().st_size if target.exists() else "", "sha256": digest, "type_contenu": content_type})
        write_manifest(rows)
        if idx % 15 == 0 or state not in {"téléchargé", "copié", "déjà présent"}:
            print(idx, "/", len(jobs), state, job["relative"])
        consecutive_network_failures = consecutive_network_failures + 1 if state.startswith("réseau :") else 0
        if status in {403, 429}:
            print("ARRÊT : limite d'accès distante", status)
            break
        if consecutive_network_failures >= 2:
            print("ARRÊT : échecs réseau consécutifs")
            break
    print(json.dumps({"references_processed": len(rows), "references_expected": len(jobs), "unique_url_downloads": len(cache), "failures": sum(r["etat"] not in {"téléchargé", "copié", "déjà présent"} for r in rows), "manifest": str(DEST / "manifest.csv")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
