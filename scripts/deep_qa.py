#!/usr/bin/env python3
"""Check disclosure boundaries and the shared page and enquiry markup."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

for page in ROOT.glob("*.html"):
    text = page.read_text(encoding="utf-8")
    assert 'href="#main">Skip to content' in text and 'id="main"' in text, page
    assert 'aria-controls="primary-nav"' in text, page
    assert 'meta name="viewport"' in text, page
    assert text.count("<header") == 1 and text.count("<footer") == 1, page
    assert "gsoc" not in text.lower() and "swindon" not in text.lower(), page
    assert "sundaramss.zeptologic@gmail.com" not in text, page
    assert not re.search(r"@(?:cysic|pixxel|qnulabs|cdot)\.", text), page

styles = (ROOT / "assets/site-v31.css").read_text(encoding="utf-8")
contact = (ROOT / "contact.html").read_text(encoding="utf-8")
assert "prefers-reduced-motion: reduce" in styles
assert '<form id="technicalEnquiry" method="post" hidden>' in contact
assert 'id="form-unavailable"' in contact
assert 'id="form-status" role="status"' in contact
assert 'id="contact-contexts" type="application/json"' in contact
print("PASS: disclosure boundaries, reduced motion and enquiry fallback markup")
