"""Inventaire prudent des pages publiques de cefisi.com et de leurs médias.

Usage : python tools/inventorier_site.py --start 0 --count 10
Les pages non publiques restent listées mais ne sont pas visitées. Les résultats
sont repris par URL dans docs/observations/site-audit.json après chaque page.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "docs" / "observations" / "site-audit.json"
SITEMAPS = ["page-sitemap.xml", "post-sitemap.xml", "category-sitemap.xml"]
BASE = "https://www.cefisi.com/"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
MEDIA_EXT = re.compile(r"\.(?:png|jpe?g|gif|webp|svg|avif|ico)(?:$|\?)", re.I)
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)
PRIVATE_PATHS = re.compile(r"/(?:login|tableau-de-bord|wiki|publier-une-offre-demploi|gestion-des-documents|documents-|profile|messages|groups|members|friends|wp-admin|wp-login)(?:/|$)", re.I)
USER_AGENT = "CEFISI-project-public-inventory/1.0"


def fetch(url: str):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xml;q=0.9,*/*;q=0.8"})
    try:
        with urlopen(request, timeout=18) as response:
            return response.status, response.geturl(), response.read(3_000_000), response.headers.get("Content-Type", "")
    except HTTPError as exc:
        return exc.code, exc.geturl(), b"", ""
    except (URLError, TimeoutError, OSError) as exc:
        return None, url, str(exc).encode(), ""


def clean_url(url: str, base: str) -> str | None:
    if not url or url.startswith(("data:", "blob:", "javascript:", "#")):
        return None
    absolute = urljoin(base, url.strip())
    parsed = urlparse(absolute)
    if parsed.scheme not in {"https", "http"}:
        return None
    return urlunparse(parsed._replace(fragment=""))


def site_urls():
    urls: dict[str, dict] = {}
    for sitemap in SITEMAPS:
        status, final, data, _ = fetch(urljoin(BASE, sitemap))
        if status != 200:
            print("SITEMAP_ERROR", sitemap, status)
            continue
        tree = ET.fromstring(data)
        for item in tree.findall("s:url", NS):
            url = item.findtext("s:loc", default="", namespaces=NS)
            images = [e.text for e in item.findall(".//{http://www.google.com/schemas/sitemap-image/1.1}loc") if e.text]
            urls[url] = {"url": url, "sitemap": sitemap, "sitemap_images": images, "lastmod": item.findtext("s:lastmod", default="", namespaces=NS)}
        time.sleep(0.7)
    return urls


def location(element):
    for n in [element, *element.iterancestors()]:
        tag = str(n.tag).lower()
        terms = ((n.get("id") or "") + " " + (n.get("class") or "")).lower()
        if tag == "header" or re.search(r"\b(?:header|topbar|main-menu|site-logo)\b", terms):
            return "en-tête / navigation"
        if tag == "footer" or re.search(r"\b(?:footer|copyright)\b", terms):
            return "pied de page"
        if tag == "main" or re.search(r"\b(?:entry-content|page-content|vc_row|post-content)\b", terms):
            return "contenu de page"
    return "gabarit / zone non identifiée"


def extract_assets(doc, page_url):
    found = []
    def add(raw, elem, source, alt=""):
        url = clean_url(raw, page_url)
        if not url or not MEDIA_EXT.search(urlparse(url).path):
            return
        found.append({"url": url, "source": source, "zone": location(elem), "alt": (alt or "").strip()[:160], "dom": elem.getroottree().getpath(elem)[:260]})
    for elem in doc.xpath("//img|//source"):
        alt = elem.get("alt", "")
        for attr in ("src", "data-src", "data-lazy-src", "data-original"):
            if elem.get(attr):
                add(elem.get(attr), elem, f"balise {elem.tag} / {attr}", alt)
        for attr in ("srcset", "data-srcset"):
            if elem.get(attr):
                for candidate in elem.get(attr).split(","):
                    add(candidate.strip().split(" ")[0], elem, f"balise {elem.tag} / {attr}", alt)
    for elem in doc.xpath("//*[@style]"):
        for _, raw in CSS_URL.findall(elem.get("style", "")):
            add(raw, elem, "style inline / url()")
    for elem in doc.xpath("//style"):
        for _, raw in CSS_URL.findall(elem.text or ""):
            add(raw, elem, "balise style / url()")
    for elem in doc.xpath("//link[@href]|//meta[@content]"):
        rel = (elem.get("rel") or "").lower()
        prop = (elem.get("property") or "").lower()
        if "icon" in rel:
            add(elem.get("href"), elem, "icône du document")
        if prop in ("og:image", "twitter:image"):
            add(elem.get("content"), elem, "métadonnée sociale")
    # Dédupliquer les occurrences strictement identiques au même emplacement.
    unique = {}
    for row in found:
        unique[(row["url"], row["source"], row["zone"], row["dom"])] = row
    return list(unique.values())


def analyse(entry):
    url = entry["url"]
    if PRIVATE_PATHS.search(urlparse(url).path):
        return {**entry, "status": "non visité : accès / administration potentiels", "http": None, "title": "", "headings": [], "excerpt": "", "assets": [], "links": []}
    status, final, data, content_type = fetch(url)
    result = {**entry, "status": "erreur", "http": status, "final_url": final, "title": "", "headings": [], "excerpt": "", "assets": [], "links": []}
    if status != 200 or "html" not in content_type.lower():
        result["status"] = f"HTTP {status} / {content_type}" if status else "échec réseau"
        return result
    if urlparse(final).hostname not in {"www.cefisi.com", "cefisi.com"}:
        result["status"] = "redirection hors domaine"
        return result
    try:
        doc = html.fromstring(data, base_url=final)
    except Exception as exc:
        result["status"] = f"HTML illisible : {type(exc).__name__}"
        return result
    title = " ".join(doc.xpath("string(//title)").split())
    headings = [" ".join(n.text_content().split())[:180] for n in doc.xpath("//h1|//h2|//h3")]
    body = doc.xpath("//main|//*[contains(concat(' ',normalize-space(@class),' '),' entry-content ')]")
    excerpt = " ".join((body[0] if body else doc).text_content().split())[:700]
    login_form = bool(doc.xpath("//form[contains(translate(@action,'LOGIN','login'),'login')]|//input[@type='password']"))
    result.update({"status": "connexion requise" if login_form else "public observé", "title": title, "headings": headings[:20], "excerpt": excerpt, "assets": extract_assets(doc, final) if not login_form else [], "links": []})
    for raw in doc.xpath("//a[@href]/@href"):
        dest = clean_url(raw, final)
        if dest and urlparse(dest).hostname in {"www.cefisi.com", "cefisi.com"} and not re.search(r"\.(?:pdf|docx?|jpe?g|png|gif|webp|svg|zip|ics)(?:$|\?)", urlparse(dest).path, re.I):
            result["links"].append(dest)
    result["links"] = sorted(set(result["links"]))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()
    seed = site_urls()
    old = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {"pages": {}, "seed": {}}
    old["seed"] = seed
    urls = list(seed)
    for idx in range(args.start, min(args.start + args.count, len(urls))):
        url = urls[idx]
        if url in old["pages"]:
            print(idx, "SKIP", url)
            continue
        page = analyse(seed[url])
        old["pages"][url] = page
        old["updated_at"] = datetime.now(timezone.utc).isoformat()
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8")
        print(idx, page["status"], len(page["assets"]), url)
        if page["http"] in (403, 429):
            print("STOP : accès limité, ne pas insister")
            break
        time.sleep(1.3)
    print("PAGES", len(old["pages"]), "/", len(seed))


if __name__ == "__main__":
    main()
