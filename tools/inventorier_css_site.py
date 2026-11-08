"""Relever les URL d'images dans les CSS locaux chargés par l'accueil.

Une référence CSS n'implique pas que l'image est effectivement affichée.
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.cefisi.com/"
OUT = ROOT / "docs" / "observations" / "site-css.json"
URLS = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)
IMAGE = re.compile(r"\.(?:png|jpe?g|gif|webp|avif|ico|svg)(?:$|\?)", re.I)


def fetch(url):
    with urlopen(Request(url, headers={"User-Agent": "CEFISI-project-public-inventory/1.0"}), timeout=18) as response:
        return response.status, response.read(2_000_000)


def main():
    status, page = fetch(BASE)
    if status != 200:
        raise RuntimeError(f"Accueil HTTP {status}")
    doc = html.fromstring(page)
    sheets = list(dict.fromkeys(urljoin(BASE, value) for value in doc.xpath("//link[contains(@rel,'stylesheet')]/@href") if value and urlparse(urljoin(BASE, value)).hostname in {"www.cefisi.com", "cefisi.com"}))
    rows = []
    failures = []
    for stylesheet in sheets:
        try:
            status, content = fetch(stylesheet)
            if status != 200:
                failures.append({"stylesheet": stylesheet, "status": status})
                continue
            text = content.decode("utf-8", "replace")
            for match in URLS.finditer(text):
                raw = match.group(2).strip()
                if raw.startswith("data:"):
                    continue
                image_url = urljoin(stylesheet, raw).split("#", 1)[0]
                if IMAGE.search(urlparse(image_url).path) and not re.search(r"/(?:fonts|webfonts)/", image_url, re.I):
                    rows.append({"url": image_url, "stylesheet": stylesheet, "code_excerpt": " ".join(text[max(0, match.start()-100):match.end()+30].split())[:180]})
            print("CSS", status, len(content), stylesheet)
        except Exception as exc:
            failures.append({"stylesheet": stylesheet, "error": str(exc)[:160]})
            print("CSS FAIL", type(exc).__name__, stylesheet)
        time.sleep(0.6)
    unique = {(r["url"], r["stylesheet"]): r for r in rows}
    OUT.write_text(json.dumps({"source_page": BASE, "checked_at": datetime.now(timezone.utc).isoformat(), "stylesheets_checked": len(sheets), "assets": list(unique.values()), "failures": failures}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("FIN", len(sheets), "CSS ;", len(unique), "références images ;", len(failures), "échecs")


if __name__ == "__main__":
    main()
