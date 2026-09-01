#!/usr/bin/env python3
"""V25 deep static QA: HTML integrity, security hygiene, experience contracts and delivery budgets."""
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
      "assets/v16.css":140000,
      "assets/site.js":75000,
      "assets/media/zlt-hero-semiconductor-journey.webm":30000000,
      "assets/media/zlt-hero-semiconductor-journey.mp4":30000000,
      "assets/media/zlt-hero-semiconductor-journey-mobile.webm":18000000,
      "assets/media/zlt-hero-semiconductor-journey-mobile.mp4":18000000,
    }
    for rel,limit in budgets.items():
        p=ROOT/rel
        if not p.exists(): failures.append(f"budget asset missing: {rel}")
        elif p.stat().st_size>limit: failures.append(f"{rel}: {p.stat().st_size} bytes exceeds budget {limit}")
    for ext in ("webm","mp4"):
        for p in (ROOT/"assets/media").glob(f"zlt-film-*.{ext}"):
            if p.stat().st_size>9000000: failures.append(f"{p.relative_to(ROOT)} exceeds 9 MB section-film budget")

    js=(ROOT/"assets/site.js").read_text(encoding="utf-8")
    if "reduce.matches||saveData){video.pause()" in js: failures.append("Save-Data still blocks explicit section-film opt-in")
    if js.count("/* V23 — benchmark-derived local navigation and review ergonomics. */")!=1:
        failures.append("V23 runtime block must exist exactly once")
    if "active?.scrollIntoView({inline:'nearest',block:'nearest'})" in js:
        failures.append("V23 active chip still uses vertical scrollIntoView and can destabilize controls")
    if "new ResizeObserver(resize).observe(canvas)" in js and "'ResizeObserver'in window" not in js:
        failures.append("ResizeObserver used without compatibility guard")
    home=(ROOT/"index.html").read_text(encoding="utf-8")
    for forbidden in ("data-hero-film-hud","SEMICONDUCTOR JOURNEY","18 SEC · CONCEPTUAL VISUALISATION","ORIGINAL ZEPTO LOGIC MEDIA · ILLUSTRATIVE SEMICONDUCTOR PROCESS SEQUENCE"):
        if forbidden in home: failures.append(f"obsolete explicit hero-film narration remains — {forbidden}")
    for name in ("products.html","services.html","applications.html","research.html"):
        text=(ROOT/name).read_text(encoding="utf-8")
        if "ORIGINAL ZEPTO LOGIC VISUAL" in text or "15 SEC · LOOP" in text:
            failures.append(f"{name}: obsolete explicit film meta remains")
    if home.count('data-v25-theatre')!=1: failures.append("V25 engineering theatre must exist exactly once")
    if home.count('data-v25-step=')!=5: failures.append("V25 engineering theatre must expose exactly five stages")
    if "V25 — ultimate fusion" not in js: failures.append("V25 runtime block missing")
    if "site_performance_sample" not in js: failures.append("V25 local performance telemetry hook missing")
    if "zlt_motion_level" not in js: failures.append("V25 motion preference control missing")
    for page in PAGES:
        raw=page.read_text(encoding="utf-8")
        if 'href="http://' in raw or "href='http://" in raw:
            failures.append(f"{page.name}: insecure HTTP hyperlink present")
    about=(ROOT/"about.html").read_text(encoding="utf-8")
    for required in ("Suresh Kuppuswamy","Advanced Management Program (AMP 206)","₹250 crore MoU","3.22-acre site","Agentic Soft Labs","Quantcell’s Accelerator Foundation","The Weight of Intelligence"):
        if required not in about: failures.append(f"about.html: confirmed CEO profile content missing — {required}")
    if 'id="leadership"' not in about: failures.append("about.html: leadership anchor missing")
    if '"@type":"Person"' not in about: failures.append("about.html: CEO Person structured data missing")
    for retired in (ROOT/"assets/media").glob("zlt-silicon-film*"):
        failures.append(f"retired V19 media still present — {retired.name}")
    for required in ("scripts/prepare_production.py","scripts/production_audit.py"):
        if not (ROOT/required).exists(): failures.append(f"production-readiness script missing — {required}")
    if "safeSession" not in js: failures.append("browser storage hardening wrapper missing")
    if "V26 command palette" not in js: failures.append("V26 command palette runtime missing")
    if "data-v26-text" not in js or "data-v26-contrast" not in js: failures.append("V26 accessibility experience controls missing")

    print(f"Deep-audited {len(PAGES)} pages.")
    for item in warnings: print("WARNING:",item)
    if failures:
        print(f"FAILED: {len(failures)} issue(s)")
        for item in failures: print(" -",item)
        return 1
    print("PASS: V26 deep static integrity, security hygiene, leadership and production-readiness gates clear.")
    return 0

if __name__=="__main__": sys.exit(main())
