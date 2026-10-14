#!/usr/bin/env python3
"""Content, disclosure, shared-layout and accessibility contract checks."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
for p in R.glob('*.html'):
 s=p.read_text()
 assert 'Skip to content' in s and 'id="main"' in s,p
 assert 'aria-controls="primary-nav"' in s,p
 assert 'meta name="viewport"' in s,p
 assert s.count('<header')==1 and s.count('<footer')==1,p
 assert 'gsoc' not in s.lower() and 'swindon' not in s.lower(),p
 assert 'sundaramss.zeptologic@gmail.com' not in s,p
 assert not re.search(r'@(?:cysic|pixxel|qnulabs|cdot)\.',s),p
js=(R/'assets/site-v31.js').read_text();css=(R/'assets/site-v31.css').read_text()
assert '5000' in js and 'prefers-reduced-motion' in js and 'prefers-reduced-motion' in css
assert 'AbortController' in js and '!r.ok||!out.ok' in js
assert 'setCustomValidity' in js and 'textContent' in js
assert 'false' in js
assert 'setInterval' in js
print('PASS: disclosure boundaries, shared navigation, motion controls and enquiry states')
