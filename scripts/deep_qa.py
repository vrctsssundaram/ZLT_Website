#!/usr/bin/env python3
"""V23 deep static QA: HTML integrity, external leakage, asset contracts and delivery budgets."""
from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys

ROOT=Path(__file__).resolve().parents[1]
PAGES=sorted(ROOT.glob("*.html"))
ACTIVE={"index.html","products.html","services.html","applications.html","research.html","about.html","news.html","careers.html","contact.html"}
BENCH={"winfomi.com","www.winfomi.com","in.micron.com","micron.com","www.micron.com","qualcomm.com","www.qualcomm.com","asml.com","www.asml.com","philips.com","www.philips.com","amd.com","www.amd.com","questglobal.com","www.questglobal.com"}
ASSET_ATTR={"img":"src","script":"src","link":"href","source":"src","video":"poster"}

class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.assets=[]; self.title=""; self.desc=""; self._title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.append(a["id"])
        if tag=="a" and a.get("href"): self.links.append(a)
        if tag in ASSET_ATTR and a.get(ASSET_ATTR[tag]): self.assets.append((tag,a[ASSET_ATTR[tag]]))
        if tag=="meta" and str(a.get("name","")).lower()=="description": self.desc=a.get("content","")
        if tag=="title": self._title=True
    def handle_endtag(self,tag):
        if tag=="title": self._title=False
    def handle_data(self,data):
        if self._title: self.title+=data

def local_path(page,ref):
    ref=unquote((ref or "").strip())
    if not ref or ref.startswith(("data:","mailto:","tel:","javascript:","#")): return None
    u=urlparse(ref)
    if u.scheme or u.netloc: return None
    return (ROOT/u.path.lstrip("/")) if u.path.startswith("/") else (page.parent/u.path).resolve()

def main():
    failures=[]; warnings=[]; titles={}; descriptions={}
    for page in PAGES:
        a=Audit(); a.feed(page.read_text(encoding="utf-8"))
        dup=[key for key,count in Counter(a.ids).items() if count>1]
        if dup: failures.append(f"{page.name}: duplicate ids: {', '.join(dup)}")
        if page.name in ACTIVE:
            title=a.title.strip(); desc=a.desc.strip()
            if not title: failures.append(f"{page.name}: empty title")
            if not desc: failures.append(f"{page.name}: empty meta description")
            if title: titles.setdefault(title,[]).append(page.name)
            if desc: descriptions.setdefault(desc,[]).append(page.name)
        for link in a.links:
            href=(link.get("href") or "").strip()
            if href=="#" or href.lower().startswith("javascript:"): failures.append(f"{page.name}: placeholder link {href!r}")
            u=urlparse(href)
            if u.hostname and u.hostname.lower() in BENCH: failures.append(f"{page.name}: benchmark-domain link embedded — {href}")
            if link.get("target")=="_blank" and "noopener" not in set((link.get("rel") or "").lower().split()):
                failures.append(f"{page.name}: target=_blank without rel=noopener — {href}")
        for tag,ref in a.assets:
            p=local_path(page,ref)
            if p is not None and not p.exists(): failures.append(f"{page.name}: missing local {tag} asset — {ref}")
            u=urlparse(ref)
            if u.hostname and u.hostname.lower() in BENCH: failures.append(f"{page.name}: benchmark-domain asset embedded — {ref}")
    for title,names in titles.items():
        if len(names)>1: failures.append(f"duplicate top-level title across {', '.join(names)} — {title}")
    for desc,names in descriptions.items():
        if len(names)>1: warnings.append(f"duplicate top-level meta description across {', '.join(names)}")

    budgets={
      "assets/v16.css":120000,
      "assets/site.js":60000,
      "assets/media/zlt-hero-semiconductor-journey.webm":1100000,
      "assets/media/zlt-hero-semiconductor-journey.mp4":1200000,
    }
    for rel,limit in budgets.items():
        p=ROOT/rel
        if not p.exists(): failures.append(f"budget asset missing: {rel}")
        elif p.stat().st_size>limit: failures.append(f"{rel}: {p.stat().st_size} bytes exceeds budget {limit}")
    for ext in ("webm","mp4"):
        for p in (ROOT/"assets/media").glob(f"zlt-film-*.{ext}"):
            if p.stat().st_size>750000: failures.append(f"{p.relative_to(ROOT)} exceeds 750 KB section-film budget")

    js=(ROOT/"assets/site.js").read_text(encoding="utf-8")
    if "reduce.matches||saveData){video.pause()" in js: failures.append("Save-Data still blocks explicit section-film opt-in")
    if "new ResizeObserver(resize).observe(canvas)" in js and "'ResizeObserver'in window" not in js:
        failures.append("ResizeObserver used without compatibility guard")

    print(f"Deep-audited {len(PAGES)} pages.")
    for item in warnings: print("WARNING:",item)
    if failures:
        print(f"FAILED: {len(failures)} issue(s)")
        for item in failures: print(" -",item)
        return 1
    print("PASS: V23 deep static integrity and delivery budgets clear.")
    return 0

if __name__=="__main__": sys.exit(main())
