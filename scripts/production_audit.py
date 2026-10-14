#!/usr/bin/env python3
from pathlib import Path
import sys
from site_qa import check,Page
R=Path(sys.argv[1]).resolve();check(R,production=True)
for f in R.glob('*.html'):
 p=Page();p.feed(f.read_text())
 if f.name in ('404.html','enquiry-received.html'):assert 'noindex' in p.robots[0]
 else:assert 'noindex' not in p.robots[0] and 'index' in p.robots[0]
 assert 'href="assets/' not in f.read_text(),'Production asset routes must be root relative'
assert (R/'.htaccess').exists()
assert 'Disallow: /' not in (R/'robots.txt').read_text()
print('PASS: production indexing, clean-route assets and host configuration')
