#!/usr/bin/env python3
"""V27 deep static QA: integrity, security, executive visual contracts and delivery budgets."""
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
        self.ids=[];self.links=[];self.assets=[];self.title="";self.desc="";self._title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):self.ids.append(a["id"])
        if tag=="a" and a.get("href"):self.links.append(a)
        if tag in ASSET_ATTR and a.get(ASSET_ATTR[tag]):self.assets.append((tag,a[ASSET_ATTR[tag]]))
        if tag=="meta" and str(a.get("name","")).lower()=="description":self.desc=a.get("content","")
        if tag=="title":self._title=True
    def handle_endtag(self,tag):
        if tag=="title":self._title=False
    def handle_data(self,data):
        if self._title:self.title+=data

def local_path(page,ref):
    ref=unquote((ref or "").strip())
    if not ref or ref.startswith(("data:","mailto:","tel:","javascript:","#")):return None
    u=urlparse(ref)
    if u.scheme or u.netloc:return None
    return (ROOT/u.path.lstrip("/")) if u.path.startswith("/") else (page.parent/u.path).resolve()

def main():
    failures=[];warnings=[];titles={};descriptions={}
    for page in PAGES:
        raw=page.read_text(encoding="utf-8")
        a=Audit();a.feed(raw)
        dup=[key for key,count in Counter(a.ids).items() if count>1]
        if dup:failures.append(f"{page.name}: duplicate ids: {', '.join(dup)}")
        if page.name in ACTIVE:
            title=a.title.strip();desc=a.desc.strip()
            if not title:failures.append(f"{page.name}: empty title")
            if not desc:failures.append(f"{page.name}: empty meta description")
            if title:titles.setdefault(title,[]).append(page.name)
            if desc:descriptions.setdefault(desc,[]).append(page.name)
            if 'class="v16' not in raw:failures.append(f"{page.name}: V16/V27 base body class missing")
        for link in a.links:
            href=(link.get("href") or "").strip()
            if href=="#" or href.lower().startswith("javascript:"):failures.append(f"{page.name}: placeholder link {href!r}")
            u=urlparse(href)
            if u.hostname and u.hostname.lower() in BENCH:failures.append(f"{page.name}: benchmark-domain link embedded — {href}")
            if link.get("target")=="_blank" and "noopener" not in set((link.get("rel") or "").lower().split()):failures.append(f"{page.name}: target=_blank without rel=noopener — {href}")
        for tag,ref in a.assets:
            p=local_path(page,ref)
            if p is not None and not p.exists():failures.append(f"{page.name}: missing local {tag} asset — {ref}")
            u=urlparse(ref)
            if u.hostname and u.hostname.lower() in BENCH:failures.append(f"{page.name}: benchmark-domain asset embedded — {ref}")
        if 'href="http://' in raw or "href='http://" in raw:failures.append(f"{page.name}: insecure HTTP hyperlink present")
    for title,names in titles.items():
        if len(names)>1:failures.append(f"duplicate top-level title across {', '.join(names)} — {title}")
    for desc,names in descriptions.items():
        if len(names)>1:warnings.append(f"duplicate top-level meta description across {', '.join(names)}")

    budgets={
      "assets/v16.css":140000,
      "assets/v27-executive.css":32000,
      "assets/site.js":52000,
      "assets/media/zlt-hero-semiconductor-journey.webm":30000000,
      "assets/media/zlt-hero-semiconductor-journey.mp4":30000000,
      "assets/media/zlt-hero-semiconductor-journey-mobile.webm":18000000,
      "assets/media/zlt-hero-semiconductor-journey-mobile.mp4":18000000,
    }
    for rel,limit in budgets.items():
        p=ROOT/rel
        if not p.exists():failures.append(f"budget asset missing: {rel}")
        elif p.stat().st_size>limit:failures.append(f"{rel}: {p.stat().st_size} bytes exceeds budget {limit}")
    for ext in ("webm","mp4"):
        for p in (ROOT/"assets/media").glob(f"zlt-film-*.{ext}"):
            if p.stat().st_size>9000000:failures.append(f"{p.relative_to(ROOT)} exceeds 9 MB section-film budget")

    home=(ROOT/"index.html").read_text(encoding="utf-8")
    js=(ROOT/"assets/site.js").read_text(encoding="utf-8")
    stature=(ROOT/"assets/stature.css").read_text(encoding="utf-8")
    v27=(ROOT/"assets/v27-executive.css").read_text(encoding="utf-8") if (ROOT/"assets/v27-executive.css").exists() else ""

    if "@import url('v27-executive.css')" not in stature:failures.append("V27 executive stylesheet is not imported globally")
    for required in ("V27 — EXECUTIVE PRECISION","--v27-navy","Matrix/cyberpunk","v20-prism-playground","v21-constellation"):
        if required not in v27:failures.append(f"V27 executive visual contract missing — {required}")

    # The CEO-approved V27 homepage must not contain the retired spectacle DOM.
    for forbidden in (
      "tech-marquee","v20-prism-playground","v20-color-rail","v21-constellation",
      "v20-section-nav","v21-signal-canvas","v21-pointer-spark","hero-aurora",
      "v25-frame-word","v25-bauhaus","v25-selfdraw","data-playground","data-constellation"
    ):
        if forbidden in home:failures.append(f"V27 homepage retained Matrix/spectacle element — {forbidden}")
    if 'class="v16 v20"' in home or 'class="v16 v21"' in home:failures.append("V27 homepage still opts into spectacle body classes")
    if home.count('data-v25-theatre')!=1:failures.append("V27 engineering path must exist exactly once")
    if home.count('data-v25-step=')!=5:failures.append("V27 engineering path must expose exactly five stages")
    if home.count('data-hero-film')!=1:failures.append("V27 must retain exactly one supporting hero film")
    for required in ("Co-creation · Collaboration","Co-opting specialist capability","co-development"):
        if required not in home:failures.append(f"homepage collaboration vocabulary missing — {required}")

    # Spectacle runtime must be gone, not merely hidden by CSS.
    for forbidden in ("v21Spectacle","capability_playground_selected","v20-section-nav","v21-pointer-spark","wireSignalCanvas","v20-ripple","v20-tilt"):
        if forbidden in js:failures.append(f"retired spectacle runtime remains — {forbidden}")
    for required in ("V27 Executive Precision runtime","site_performance_sample","zlt_motion_level","safeSession","safeLocal","engineeringPath","searchHints","ipExplorer"):
        if required not in js:failures.append(f"V27 runtime contract missing — {required}")
    if "new ResizeObserver" in js:failures.append("V27 lean runtime unexpectedly retains ResizeObserver spectacle machinery")

    for forbidden in ("data-hero-film-hud","SEMICONDUCTOR JOURNEY","18 SEC · CONCEPTUAL VISUALISATION","ORIGINAL ZEPTO LOGIC MEDIA · ILLUSTRATIVE SEMICONDUCTOR PROCESS SEQUENCE"):
        if forbidden in home:failures.append(f"obsolete explicit hero-film narration remains — {forbidden}")
    for name in ("products.html","services.html","applications.html","research.html"):
        text=(ROOT/name).read_text(encoding="utf-8")
        if "ORIGINAL ZEPTO LOGIC VISUAL" in text or "15 SEC · LOOP" in text:failures.append(f"{name}: obsolete explicit film meta remains")

    about=(ROOT/"about.html").read_text(encoding="utf-8")
    for required in ("Suresh Kuppuswamy","Advanced Management Program (AMP 206)","₹250 crore MoU","3.22-acre site","Agentic Soft Labs","Quantcell’s Accelerator Foundation","The Weight of Intelligence"):
        if required not in about:failures.append(f"about.html: confirmed CEO profile content missing — {required}")
    if 'id="leadership"' not in about:failures.append("about.html: leadership anchor missing")
    if '"@type":"Person"' not in about:failures.append("about.html: CEO Person structured data missing")

    collaboration={
      "services.html":("Co-creation · Collaboration","Co-opting specialist capability","Co-engineering"),
      "research.html":("Co-creation","Collaboration","co-development","Joint R&amp;D"),
      "applications.html":("Co-create","co-engineering","co-development"),
      "contact.html":("Co-creation / co-development","Co-engineering / specialist capacity","Co-opting specialist engineering capacity"),
    }
    for name,terms in collaboration.items():
        text=(ROOT/name).read_text(encoding="utf-8")
        for term in terms:
            if term not in text:failures.append(f"{name}: required collaboration vocabulary missing — {term}")

    for retired in (ROOT/"assets/media").glob("zlt-silicon-film*"):failures.append(f"retired V19 media still present — {retired.name}")
    for required in ("scripts/prepare_production.py","scripts/production_audit.py","PRODUCTION-MIGRATION.md"):
        if not (ROOT/required).exists():failures.append(f"production-readiness resource missing — {required}")

    print(f"Deep-audited {len(PAGES)} pages.")
    for item in warnings:print("WARNING:",item)
    if failures:
        print(f"FAILED: {len(failures)} issue(s)")
        for item in failures:print(" -",item)
        return 1
    print("PASS: V27 executive precision, anti-spectacle, integrity, leadership and production-readiness gates clear.")
    return 0

if __name__=="__main__":sys.exit(main())
