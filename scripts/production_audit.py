#!/usr/bin/env python3
"""Audit the generated V28 production package before migration/deployment."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
import sys,re,xml.etree.ElementTree as ET

DEST=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('dist-production').resolve()
KEEP_NOINDEX={'404.html','enquiry-received.html'}
PHONE_RE=re.compile(r'(?:96266\s*32233|919626632233|wa\.me/919626632233)')
fail=[]

class A(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.canonical=[];self.robots=[];self.assets=[];self.ids=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if d.get('id'):self.ids.append(d['id'])
  if tag=='link' and str(d.get('rel','')).lower()=='canonical':self.canonical.append(d.get('href',''))
  if tag=='meta' and str(d.get('name','')).lower()=='robots':self.robots.append(d.get('content',''))
  if tag=='a' and d.get('href'):self.links.append(d['href'])
  attr={'img':'src','script':'src','link':'href'}.get(tag)
  if attr and d.get(attr):self.assets.append(d[attr])

def local(page,ref):
 ref=unquote(ref or '')
 if not ref or ref.startswith(('#','mailto:','tel:','data:','javascript:')):return None
 u=urlparse(ref)
 if u.scheme or u.netloc:return None
 return (DEST/u.path.lstrip('/')) if u.path.startswith('/') else (page.parent/u.path).resolve()

pages=sorted(DEST.glob('*.html'))
if not pages:fail.append('no HTML pages in production package')
for page in pages:
 text=page.read_text(encoding='utf-8');a=A();a.feed(text)
 if len(a.canonical)!=1:fail.append(f'{page.name}: expected exactly one canonical')
 elif not a.canonical[0].startswith('https://zeptologic.com/'):fail.append(f'{page.name}: non-production canonical {a.canonical[0]}')
 robots=','.join(a.robots).lower()
 if page.name in KEEP_NOINDEX:
  if 'noindex' not in robots:fail.append(f'{page.name}: must remain noindex')
 else:
  if 'noindex' in robots or 'index' not in robots:fail.append(f'{page.name}: production indexing directive invalid')
 if len(a.ids)!=len(set(a.ids)):fail.append(f'{page.name}: duplicate IDs')
 for ref in a.assets:
  p=local(page,ref)
  if p is not None and not p.exists():fail.append(f'{page.name}: missing asset {ref}')
 for href in a.links:
  if href.startswith('http://'):fail.append(f'{page.name}: insecure HTTP link {href}')
 for bad in ('vrctsssundaram.github.io','sundaramss.fun','localhost','127.0.0.1'):
  if bad in text:fail.append(f'{page.name}: staging/development host leaked — {bad}')
 if '<video' in text.lower():fail.append(f'{page.name}: video leaked into production package')
 if re.search(r'<animate(?:transform)?\b',text,re.I):fail.append(f'{page.name}: SVG animation element leaked')
 if any(x in text for x in ('v25-experience','motion-toggle','data-cinematic-toggle','data-hero-film')):fail.append(f'{page.name}: retired motion/experience UI leaked')
 if page.name!='contact.html' and PHONE_RE.search(text):fail.append(f'{page.name}: phone/WhatsApp leaked outside Contact')

contact=(DEST/'contact.html').read_text(encoding='utf-8') if (DEST/'contact.html').exists() else ''
if '+91 96266 32233' not in contact or 'tel:+919626632233' not in contact:fail.append('contact.html: approved direct phone missing')
if 'assets/v28-boardroom.css' not in (DEST/'index.html').read_text(encoding='utf-8'):fail.append('index.html: V28 stylesheet missing')
if 'hero-technical-visual' not in (DEST/'index.html').read_text(encoding='utf-8'):fail.append('index.html: static technical hero visual missing')

robots=(DEST/'robots.txt').read_text(encoding='utf-8') if (DEST/'robots.txt').exists() else ''
if 'Disallow: /' in robots:fail.append('production robots.txt still blocks crawling')
if 'Sitemap: https://zeptologic.com/sitemap.xml' not in robots:fail.append('production robots.txt missing sitemap')
if not (DEST/'.htaccess').exists():fail.append('production .htaccess missing')

try:
 root=ET.parse(DEST/'sitemap.xml').getroot();ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'};urls={el.text.strip() for el in root.findall('s:url/s:loc',ns) if el.text};expected=set()
 for page in pages:
  if page.name in KEEP_NOINDEX:continue
  a=A();a.feed(page.read_text(encoding='utf-8'))
  if a.canonical:expected.add(a.canonical[0])
 missing=expected-urls;extra=urls-expected
 if missing:fail.append('sitemap missing canonicals: '+', '.join(sorted(missing)))
 if extra:fail.append('sitemap has non-page canonicals: '+', '.join(sorted(extra)))
except Exception as exc:fail.append(f'sitemap parse failed: {exc}')

media=DEST/'assets/media'
if media.exists() and any(media.iterdir()):fail.append('retired cinematic media copied into production package')
js=(DEST/'assets/site.js').read_text(encoding='utf-8') if (DEST/'assets/site.js').exists() else ''
for forbidden in ('v25-experience','heroMedia','sectionMedia','tel:+919626632233','data-hero-film'):
 if forbidden in js:fail.append(f'production JS retains retired runtime — {forbidden}')

if fail:
 print(f'FAILED: {len(fail)} production-readiness issue(s)');[print(' -',x) for x in fail];raise SystemExit(1)
print(f'PASS: V28 production package ready — {len(pages)} HTML pages, clean routes, security headers, no-media UI, phone isolation and asset integrity verified.')
