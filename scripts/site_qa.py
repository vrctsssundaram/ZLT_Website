#!/usr/bin/env python3
"""V16 release QA for the Zepto Logic staging website."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re, sys, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
HTML_FILES=sorted(ROOT.glob('*.html'))
HOSTS={'zeptologic.com','www.zeptologic.com'}
V16_PAGES={'index.html','products.html','services.html','applications.html','research.html','about.html','news.html','careers.html','contact.html'}
FORBIDDEN_CLAIMS={
 r'\b15\+\s*(?:FPGA[- ]validated\s*)?(?:IP|cores?|blocks?)\b':'legacy 15+ IP-count claim',
 r'\bsilicon[- ]validated\b':'silicon-validation claim',
 r'\bpatent\s+pending\b':'patent-pending claim',
 r'\bTRL[- ]?\d+\b':'public TRL claim',
 r'\bfoundry[- ]ready\b':'foundry-ready claim',
 r'\bDeep\s+Tech\s+Startup\b':'unapproved deep-tech recognition wording',
 r'\bunfiled\s+(?:invention|architecture|IP)':'filing-state disclosure',
}
REJECTED_UI={
 r'class=["\'][^"\']*\bnexus-bar\b':'rejected Nexus relationship bar',
 r'class=["\'][^"\']*\bnexus-console\b':'rejected Nexus opportunity console',
 r'data-audience-choice':'rejected persona-routing control',
 r'class=["\'][^"\']*\becosystem-canvas\b':'rejected ecosystem routing canvas',
 r'class=["\'][^"\']*\bsilicon-workbench\b':'retired Silicon Workbench',
 r'class=["\'][^"\']*\bintent-lab\b':'retired Intent Lab',
 r'\bI am here to\b':'rejected relationship wording',
 r'\bRecommended route\b':'rejected route wording',
 r'\bExplore as\b':'rejected persona wording',
}
SELF_JUSTIFY={
 r'\bnot customer deployment claims\b':'self-justifying deployment disclaimer',
 r'\bso commercial pages can remain focused\b':'self-referential page-placement explanation',
 r'\bstated with their current public status\b':'editorial-status explanation',
 r'\bwhy this route exists\b':'page-purpose narration',
 r'\bpublic disclosure ceiling\b':'internal disclosure-language',
 r'\bpublic benchmark policy\b':'internal publication-language',
 r'\bscope clarity\b':'internal scoping-language',
 r'\bEvaluation questions\b':'runtime FAQ language',
 r'\bTypical engagement path\b':'runtime process narration',
 r'\bprogramme proof\b':'proof-as-argument language',
 r'\bevidence before adjectives\b':'editorial-policy narration',
 r'\bno budget question\b':'smallness / reassurance marketing',
 r'\bdoes not justify building a permanent organisation\b':'smallness marketing',
 r'\btoo focused to justify a new team\b':'smallness marketing',
 r'\bbefore you fund another internal build\b':'defensive internal-build comparison',
}

class PageParser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.refs=[];self.ids=set();self.images=[];self.canonical=None;self.h1_count=0
  self.robots=None;self.theme=None;self.viewport=None;self.lang=None;self.body_class=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if tag=='body':self.body_class=a.get('class','') or ''
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('href'):self.refs.append(('href',a['href']))
  if tag in {'img','script','link'}:
   key='src' if tag in {'img','script'} else 'href'
   if a.get(key):self.refs.append((key,a[key]))
  if tag=='img':self.images.append({'src':a.get('src'),'alt':a.get('alt')})
  if tag=='link' and str(a.get('rel','')).lower()=='canonical':self.canonical=a.get('href')
  if tag=='meta' and str(a.get('name','')).lower()=='robots':self.robots=str(a.get('content','')).lower().replace(' ','')
  if tag=='meta' and str(a.get('name','')).lower()=='theme-color':self.theme=str(a.get('content','')).lower()
  if tag=='meta' and str(a.get('name','')).lower()=='viewport':self.viewport=str(a.get('content','')).lower().replace(' ','')
  if tag=='h1':self.h1_count+=1

def parse_pages():
 out={}
 for path in HTML_FILES:
  p=PageParser();p.feed(path.read_text(encoding='utf-8'));out[path.name]=p
 return out

def local_target(current,ref):
 ref=unquote(ref.strip())
 if not ref or ref.startswith(('mailto:','tel:','javascript:','data:')):return None
 u=urlparse(ref)
 if u.scheme in {'http','https'}:return None
 if not u.path:return current,u.fragment
 return (ROOT/u.path.lstrip('/') if u.path.startswith('/') else (current.parent/u.path).resolve()),u.fragment

def hex_luminance(value):
 v=value.lstrip('#')
 if len(v)==3:v=''.join(c*2 for c in v)
 if len(v)!=6:return 1
 r,g,b=[int(v[i:i+2],16)/255 for i in (0,2,4)]
 def f(c):return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4
 return .2126*f(r)+.7152*f(g)+.0722*f(b)

def main():
 failures=[];warnings=[];parsed=parse_pages()
 if not HTML_FILES:failures.append('No root HTML files found')
 for name,page in parsed.items():
  path=ROOT/name;text=path.read_text(encoding='utf-8')
  if page.lang!='en':failures.append(f'{name}: html lang must be en')
  if page.h1_count!=1:failures.append(f'{name}: expected exactly one <h1>, found {page.h1_count}')
  if name!='404.html' and not page.canonical:failures.append(f'{name}: missing canonical URL')
  if page.canonical:
   c=urlparse(page.canonical)
   if c.scheme!='https' or c.netloc not in HOSTS:failures.append(f'{name}: invalid canonical host/scheme — {page.canonical}')
  if page.robots!='noindex,nofollow':failures.append(f'{name}: staging page must contain static noindex,nofollow')
  if not page.viewport or 'width=device-width' not in page.viewport or 'initial-scale=1' not in page.viewport:failures.append(f'{name}: missing responsive viewport contract')
  for group in (FORBIDDEN_CLAIMS,REJECTED_UI,SELF_JUSTIFY):
   for pattern,reason in group.items():
    if re.search(pattern,text,re.I):failures.append(f'{name}: {reason}')
  if name in V16_PAGES:
   if 'v16' not in page.body_class.split():failures.append(f'{name}: top-level page must use body.v16')
   if 'assets/v16.css' not in text:failures.append(f'{name}: V16 stylesheet missing')
   for href in ['products.html','services.html','applications.html','research.html','about.html','news.html']:
    if href not in text:failures.append(f'{name}: global taxonomy link missing — {href}')
  for image in page.images:
   if image['alt'] is None:failures.append(f"{name}: image missing alt attribute — {image['src']}")
  for kind,ref in page.refs:
   resolved=local_target(path,ref)
   if resolved is None:continue
   target,fragment=resolved
   if target.is_dir():target=target/'index.html'
   if not target.exists():failures.append(f'{name}: broken local {kind} target — {ref}');continue
   if fragment and target.suffix.lower()=='.html':
    target_page=parsed.get(target.name)
    if target_page and fragment not in target_page.ids:failures.append(f'{name}: missing fragment #{fragment} in {target.name}')

 css=ROOT/'assets/v16.css';js=ROOT/'assets/site.js';browser=ROOT/'tests/site.spec.js';workflow=ROOT/'.github/workflows/site-qa.yml'
 if not css.exists():failures.append('assets/v16.css missing')
 else:
  ct=css.read_text(encoding='utf-8')
  for marker in ['Inter','IBM+Plex+Mono','.z-hero','.z-grid4','.z-app-grid','.z-page-hero','.z-news','.z-contact-lines','@media(max-width:980px)','@media(max-width:700px)','prefers-reduced-motion']:
   if marker not in ct:failures.append(f'V16 CSS marker missing — {marker}')
  # V18 intentionally uses dark and high-energy surfaces; browser/Axe QA owns contrast validation.
 if not js.exists():failures.append('assets/site.js missing')
 else:
  st=js.read_text(encoding='utf-8')
  for marker in ['Applications','ip-explorer-tools','technical_enquiry_submitted','website-enquiry','viewportMode','mobile-dock','fp-add-sub','i2c-master']:
   if marker not in st:failures.append(f'V16 runtime marker missing — {marker}')
  for rejected in ['disclosureSection','Evaluation questions','Scope clarity','Typical engagement path','audienceData','nexus_audience_selected','data-audience-choice','ecoData']:
   if rejected in st:failures.append(f'V16 runtime retains explanatory/retired system — {rejected}')
 motion_assets=['zlt-hero-semiconductor-journey.webm','zlt-hero-semiconductor-journey.mp4','zlt-hero-semiconductor-journey-mobile.webm','zlt-hero-semiconductor-journey-mobile.mp4','zlt-hero-semiconductor-journey-poster.jpg','zlt-hero-semiconductor-journey-mobile-poster.jpg','zlt-film-ip.webm','zlt-film-ip.mp4','zlt-film-ip-poster.jpg','zlt-film-engineering.webm','zlt-film-engineering.mp4','zlt-film-engineering-poster.jpg','zlt-film-applications.webm','zlt-film-applications.mp4','zlt-film-applications-poster.jpg','zlt-film-research.webm','zlt-film-research.mp4','zlt-film-research-poster.jpg']
 media_dir=ROOT/'assets/media'
 for asset in motion_assets:
  p=media_dir/asset
  if not p.exists():failures.append(f'V22 cinematic asset missing — {asset}')
  elif p.stat().st_size<20000:failures.append(f'V22 cinematic asset unexpectedly small — {asset}')
 if not (ROOT/'applications.html').exists():failures.append('applications.html missing')
 if not browser.exists():failures.append('tests/site.spec.js missing')
 if not workflow.exists():failures.append('site QA workflow missing')
 robots=ROOT/'robots.txt'
 if not robots.exists():failures.append('robots.txt missing')
 else:
  rt=robots.read_text(encoding='utf-8').lower()
  if 'user-agent: *' not in rt or 'disallow: /' not in rt:failures.append('robots.txt must disallow all crawling on staging')
 sitemap=ROOT/'sitemap.xml'
 if not sitemap.exists():failures.append('sitemap.xml missing')
 else:
  try:
   ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'};tree=ET.parse(sitemap)
   locs=[x.text.strip() for x in tree.findall('sm:url/sm:loc',ns) if x.text];seen=set()
   if 'https://zeptologic.com/applications/' not in locs:failures.append('sitemap.xml: applications URL missing')
   for loc in locs:
    if loc in seen:failures.append(f'sitemap.xml: duplicate URL — {loc}')
    seen.add(loc);u=urlparse(loc)
    if u.scheme!='https' or u.netloc not in HOSTS:failures.append(f'sitemap.xml: non-canonical host/scheme — {loc}');continue
    physical=ROOT/'index.html' if u.path=='/' else ROOT/((u.path.strip('/')+'.html') if u.path.endswith('/') else u.path.lstrip('/'))
    if not physical.exists():failures.append(f'sitemap.xml: URL has no physical page mapping — {loc}')
  except ET.ParseError as exc:failures.append(f'sitemap.xml: XML parse error — {exc}')
 print(f'Checked {len(HTML_FILES)} HTML pages.')
 for w in warnings:print(f'WARNING: {w}')
 if failures:
  print(f'\nFAILED: {len(failures)} issue(s)')
  for item in failures:print(f' - {item}')
  return 1
 print('PASS: V24 high-resolution cinematic media, editorial, staging, taxonomy, disclosure and integrity guardrails clear.')
 return 0

if __name__=='__main__':sys.exit(main())
