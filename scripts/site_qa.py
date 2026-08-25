#!/usr/bin/env python3
"""Zero-dependency QA for the Zepto Logic static website.

Checks the current tree only. It never calls external services and does not deploy.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html"))
HOSTS = {"zeptologic.com", "www.zeptologic.com"}

FORBIDDEN = {
    r"\b15\+\s*(?:FPGA[- ]validated\s*)?(?:IP|cores?|blocks?)\b": "legacy 15+ IP-count claim",
    r"\bsilicon[- ]validated\b": "silicon-validation claim",
    r"\bpatent\s+pending\b": "patent-pending claim",
    r"\bTRL[- ]?\d+\b": "public TRL claim",
    r"\bfoundry[- ]ready\b": "foundry-ready claim",
    r"\bDeep\s+Tech\s+Startup\b": "unapproved deep-tech recognition wording",
    r"\bunfiled\s+(?:invention|architecture|IP)": "filing-state disclosure",
}

class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.images: list[dict[str, str | None]] = []
        self.canonical: str | None = None
        self.title_seen = False
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.refs.append(("href", a["href"]))
        if tag in {"img", "script", "link"}:
            key = "src" if tag in {"img", "script"} else "href"
            if a.get(key):
                self.refs.append((key, a[key]))
        if tag == "img":
            self.images.append({"src": a.get("src"), "alt": a.get("alt")})
        if tag == "link" and str(a.get("rel", "")).lower() == "canonical":
            self.canonical = a.get("href")
        if tag == "title":
            self.title_seen = True
        if tag == "h1":
            self.h1_count += 1


def parse_pages():
    parsed = {}
    for path in HTML_FILES:
        p = PageParser()
        p.feed(path.read_text(encoding="utf-8"))
        parsed[path.name] = p
    return parsed


def local_target(current: Path, ref: str):
    ref = unquote(ref.strip())
    if not ref or ref.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None
    u = urlparse(ref)
    if u.scheme in {"http", "https"}:
        return None
    raw_path = u.path
    if not raw_path:
        return (current, u.fragment)
    if raw_path.startswith("/"):
        target = ROOT / raw_path.lstrip("/")
    else:
        target = (current.parent / raw_path).resolve()
    return (target, u.fragment)


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    parsed = parse_pages()

    if not HTML_FILES:
        failures.append("No root HTML files found")

    # Structural and internal-reference checks.
    for name, page in parsed.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        if page.h1_count != 1:
            failures.append(f"{name}: expected exactly one <h1>, found {page.h1_count}")
        if name != "404.html" and not page.canonical:
            failures.append(f"{name}: missing canonical URL")
        if page.canonical:
            c = urlparse(page.canonical)
            if c.scheme != "https" or c.netloc not in HOSTS:
                failures.append(f"{name}: canonical must use https://zeptologic.com — {page.canonical}")
            physical = "/" if name == "index.html" else f"/{name}"
            if c.path not in {physical, physical.removesuffix(".html") + "/"}:
                warnings.append(f"{name}: canonical path {c.path!r} does not directly correspond to {physical!r}")

        for pattern, reason in FORBIDDEN.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                failures.append(f"{name}: {reason}")

        for image in page.images:
            if image["alt"] is None:
                failures.append(f"{name}: image missing alt attribute — {image['src']}")

        for kind, ref in page.refs:
            resolved = local_target(path, ref)
            if resolved is None:
                continue
            target, fragment = resolved
            # Query/hash-only refs resolve to the current document.
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                failures.append(f"{name}: broken local {kind} target — {ref}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_name = target.name
                target_page = parsed.get(target_name)
                if target_page and fragment not in target_page.ids:
                    failures.append(f"{name}: missing fragment #{fragment} in {target_name}")

    # Sitemap maps clean URLs back to their physical static page.
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        failures.append("sitemap.xml missing")
    else:
        try:
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            tree = ET.parse(sitemap)
            locs = [x.text.strip() for x in tree.findall("sm:url/sm:loc", ns) if x.text]
            seen = set()
            for loc in locs:
                if loc in seen:
                    failures.append(f"sitemap.xml: duplicate URL — {loc}")
                seen.add(loc)
                u = urlparse(loc)
                if u.scheme != "https" or u.netloc not in HOSTS:
                    failures.append(f"sitemap.xml: non-canonical host/scheme — {loc}")
                    continue
                if u.path == "/":
                    physical = ROOT / "index.html"
                elif u.path.endswith("/"):
                    physical = ROOT / (u.path.strip("/") + ".html")
                else:
                    physical = ROOT / u.path.lstrip("/")
                if not physical.exists():
                    failures.append(f"sitemap.xml: URL has no physical page mapping — {loc}")
        except ET.ParseError as exc:
            failures.append(f"sitemap.xml: XML parse error — {exc}")

    # robots.txt is expected for a production-oriented static website.
    robots = ROOT / "robots.txt"
    if not robots.exists():
        warnings.append("robots.txt is not present yet")

    print(f"Checked {len(HTML_FILES)} HTML pages.")
    for w in warnings:
        print(f"WARNING: {w}")
    if failures:
        print(f"\nFAILED: {len(failures)} issue(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print(f"PASS: no blocking integrity/disclosure issues; {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
