#!/usr/bin/env python3
"""Zero-dependency release QA for the V29 executive-clarity staging site."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
import re,sys,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
HTML_FILES=sorted(ROOT.glob('*.html'))
HOSTS={'zeptologic.com','www.zeptologic.com'}
TOP={'index.html','services.html','applications.html','research.html','about.html','news.html','careers.html','contact.html'}
FORBIDDEN_CLAIMS={
 r'\b15\+\s*(?:FPGA[- ]validated\s*)?(?:IP|cores?|blocks?)\b':'legacy 15+ IP-count claim',
 r'\bsilicon[- ]validated\b':'silicon-validation claim',r'\bpatent\s+pending\b':'patent-pending claim',
 r'\bTRL[- ]?\d+\b':'public TRL claim',r'\bfoundry[- ]ready\b':'foundry-ready claim'
}
RETIRED_UI=('v20-prism-playground','v21-constellation','v20-color-rail','v25-experience','motion-toggle','data-hero-film','data-cinematic-video','data-cinematic-toggle')
PHONE_TOKENS=('96266 32233','919626632233','tel:+919626632233','wa.me/919626632233')

class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.ids=set();self.refs=[];self.images=[];self.canonical=None;self.h1=0;self.robots=None;self.viewport=None;self.lang=None;self.body=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if tag=='body':self.body=a.get('class','') or ''
  if a.get('id'):self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='a' and a.get('href'):self.refs.append(('href',a['href']))
  if tag in {'img','script','link'}:
   key='src' if tag in {'img','script'} else 'href'
   if a.get(key):self.refs.append((key,a[key]))
  if tag=='img':self.images.append((a.get('src'),a.get('alt')))
  if tag=='link' and str(a.get('rel','')).lower()=='canonical':self.canonical=a.get('href')
  if tag=='meta' and str(a.get('name','')).lower()=='robots':self.robots=str(a.get('content','')).lower().replace(' ','')
  if tag=='meta' and str(a.get('name','')).lower()=='viewport':self.viewport=str(a.get('content','')).lower().replace(' ','')

def local_target(current,ref):
 ref=unquote((ref or '').strip())
 if not ref or ref.startswith(('mailto:','tel:','javascript:','data:','#')):return None
 u=urlparse(ref)
 if u.scheme or u.netloc:return None
 target=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (current.parent/u.path).resolve()
 return target,u.fragment

def main():
 fail=[];parsed={}
 for path in HTML_FILES:
  p=Page();p.feed(path.read_text(encoding='utf-8'));parsed[path.name]=p
 if not HTML_FILES:fail.append('No HTML pages found')
 for path in HTML_FILES:
  name=path.name;raw=path.read_text(encoding='utf-8');p=parsed[name]
  if p.lang!='en':fail.append(f'{name}: html lang must be en')
  if p.h1!=1:fail.append(f'{name}: expected exactly one h1, found {p.h1}')
  if name!='404.html' and not p.canonical:fail.append(f'{name}: canonical missing')
  if p.canonical:
   u=urlparse(p.canonical)
   if u.scheme!='https' or u.netloc not in HOSTS:fail.append(f'{name}: invalid canonical {p.canonical}')
  if p.robots!='noindex,nofollow':fail.append(f'{name}: staging must remain noindex,nofollow')
  if not p.viewport or 'width=device-width' not in p.viewport or 'initial-scale=1' not in p.viewport:fail.append(f'{name}: responsive viewport contract missing')
  if name in TOP:
   if 'v16' not in p.body.split():fail.append(f'{name}: body.v16 missing')
   for sheet in ('assets/v16.css','assets/v27-executive.css','assets/v28-boardroom.css','assets/v29-clarity.css'):
    if sheet not in raw:fail.append(f'{name}: stylesheet missing — {sheet}')
   for href in ('index.html','services.html','research.html','about.html','contact.html'):
    if href not in raw:fail.append(f'{name}: primary route missing — {href}')
  for pattern,reason in FORBIDDEN_CLAIMS.items():
   if re.search(pattern,raw,re.I):fail.append(f'{name}: {reason}')
  if '<video' in raw.lower():fail.append(f'{name}: video element remains')
  if re.search(r'<animate(?:transform)?\b',raw,re.I):fail.append(f'{name}: SVG SMIL animation remains')
  for token in RETIRED_UI:
   if token in raw:fail.append(f'{name}: retired UI remains — {token}')
  if name!='contact.html':
   for token in PHONE_TOKENS:
    if token in raw:fail.append(f'{name}: phone/WhatsApp leaked outside Contact — {token}')
  for src,alt in p.images:
   if alt is None:fail.append(f'{name}: image missing alt — {src}')
  for kind,ref in p.refs:
   resolved=local_target(path,ref)
   if resolved is None:continue
   target,frag=resolved
   if target.is_dir():target=target/'index.html'
   if not target.exists():fail.append(f'{name}: broken local {kind} target — {ref}');continue
   if frag and target.suffix.lower()=='.html':
    target_page=parsed.get(target.name)
    if target_page and frag not in target_page.ids:fail.append(f'{name}: missing #{frag} in {target.name}')

 contact=(ROOT/'contact.html').read_text(encoding='utf-8')
 if '+91 96266 32233' not in contact or 'tel:+919626632233' not in contact:fail.append('contact.html: approved direct phone missing')
 home=(ROOT/'index.html').read_text(encoding='utf-8')
 for required in ('Semiconductor IP services and Applied R&amp;D.','v29-hero-offer','v29-pillars','v29-offerings','Semiconductor consultation','Design verification','FPGA prototyping &amp; validation'):
  if required not in home:fail.append(f'index.html: V29 direct-offering contract missing — {required}')
 if home.count('v29-pillar')<3:fail.append('index.html: three core offering pillars missing')
 if home.count('v29-offering')<6:fail.append('index.html: six-item offering menu incomplete')
 services=(ROOT/'services.html').read_text(encoding='utf-8')
 for required in ('Consultation','Design &amp; prototyping lab','Architecture &amp; specification','Design verification','FPGA prototyping'):
  if required not in services:fail.append(f'services.html: direct service contract missing — {required}')
 for name in ('applications.html','research.html'):
  if 'v28-technical-visual' not in (ROOT/name).read_text(encoding='utf-8'):fail.append(f'{name}: supporting technical visual missing')
 for term in ('Co-creation','Collaboration','Co-opting'):
  if term not in home:fail.append(f'index.html: required collaboration term missing — {term}')

 js=(ROOT/'assets/site.js').read_text(encoding='utf-8') if (ROOT/'assets/site.js').exists() else ''
 for forbidden in ('v25-experience','data-hero-film','data-cinematic-video','tel:+919626632233','saveData','heroMedia','sectionMedia'):
  if forbidden in js:fail.append(f'assets/site.js: retired runtime remains — {forbidden}')
 for needed in ('engineeringPath','website-enquiry','searchHints','site_performance_sample'):
  if needed not in js:fail.append(f'assets/site.js: required runtime missing — {needed}')

 media=ROOT/'assets/media'
 if media.exists() and any(media.iterdir()):fail.append('assets/media: retired cinematic assets remain')
 for retired in ('scripts/generate_v22_media.py','.github/workflows/generate-v22-media.yml'):
  if (ROOT/retired).exists():fail.append(f'retired media pipeline remains — {retired}')
 for required in ('assets/v28-boardroom.css','assets/v29-clarity.css','scripts/prepare_production.py','scripts/production_audit.py','tests/site.spec.js','.github/workflows/site-qa.yml'):
  if not (ROOT/required).exists():fail.append(f'required release resource missing — {required}')

 robots=ROOT/'robots.txt'
 if not robots.exists() or 'disallow: /' not in robots.read_text(encoding='utf-8').lower():fail.append('staging robots.txt must disallow all')
 sitemap=ROOT/'sitemap.xml'
 if sitemap.exists():
  try:
   ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'};root=ET.parse(sitemap).getroot();locs=[e.text.strip() for e in root.findall('s:url/s:loc',ns) if e.text]
   if len(locs)!=len(set(locs)):fail.append('sitemap.xml: duplicate URLs')
   for loc in locs:
    u=urlparse(loc)
    if u.scheme!='https' or u.netloc not in HOSTS:fail.append(f'sitemap.xml: invalid canonical origin — {loc}')
  except ET.ParseError as exc:fail.append(f'sitemap.xml: XML error — {exc}')
 else:fail.append('sitemap.xml missing')

 print(f'Checked {len(HTML_FILES)} HTML pages.')
 if fail:
  print(f'FAILED: {len(fail)} issue(s)');[print(' -',x) for x in fail];return 1
 print('PASS: V29 executive clarity, direct offerings, phone isolation, no-media contract, links, claims and staging guardrails clear.')
 return 0
if __name__=='__main__':sys.exit(main())
