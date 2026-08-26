#!/usr/bin/env python3
"""Zero-dependency release QA for the Zepto Logic staging website."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re, sys, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
HTML_FILES=sorted(ROOT.glob('*.html'))
HOSTS={'zeptologic.com','www.zeptologic.com'}
THEME='#f4f0e7'

FORBIDDEN_CLAIMS={
 r'\b15\+\s*(?:FPGA[- ]validated\s*)?(?:IP|cores?|blocks?)\b':'legacy 15+ IP-count claim',
 r'\bsilicon[- ]validated\b':'silicon-validation claim',r'\bpatent\s+pending\b':'patent-pending claim',r'\bTRL[- ]?\d+\b':'public TRL claim',r'\bfoundry[- ]ready\b':'foundry-ready claim',r'\bDeep\s+Tech\s+Startup\b':'unapproved deep-tech recognition wording',r'\bunfiled\s+(?:invention|architecture|IP)':'filing-state disclosure'}
LEGACY_PUBLIC_PATTERNS={
 r'assets/(?:v4|v4-pages|home-v3)\.css':'legacy stylesheet reference',r'class=["\'][^"\']*\bsignal-chamber\b':'legacy signal-chamber component',r'class=["\'][^"\']*\bsignal-topology\b':'legacy topology component',r'class=["\'][^"\']*\bproject-composer\b':'legacy composer component',r'class=["\'][^"\']*\bevidence-tape\b':'legacy evidence-tape component',r'class=["\'][^"\']*\bproblem-atlas\b':'legacy problem-atlas component',r'class=["\'][^"\']*\bcapability-field\b':'legacy capability-field component',r'class=["\'][^"\']*\boffer-ledger\b':'legacy offer-ledger component',r'class=["\'][^"\']*\bevidence-list\b':'legacy evidence-list component',r'class=["\'][^"\']*\bproblem-register\b':'legacy problem-register component',r'class=["\'][^"\']*\btheme-toggle\b':'legacy theme-toggle component',r'class=["\'][^"\']*\bpage-hero\b':'legacy page-hero component',r'class=["\'][^"\']*\bsection-code\b':'legacy section-code component',r'\bZepto Logic at a glance\b':'legacy at-a-glance language',r'>\s*Verified\s*<':'legacy Verified label'}

class PageParser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.refs=[];self.ids=set();self.images=[];self.canonical=None;self.h1_count=0;self.robots=None;self.theme=None;self.viewport=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
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
 target=ROOT/u.path.lstrip('/') if u.path.startswith('/') else (current.parent/u.path).resolve()
 return target,u.fragment

def main():
 failures=[];warnings=[];parsed=parse_pages()
 if not HTML_FILES:failures.append('No root HTML files found')
 for name,page in parsed.items():
  path=ROOT/name;text=path.read_text(encoding='utf-8')
  if page.h1_count!=1:failures.append(f'{name}: expected exactly one <h1>, found {page.h1_count}')
  if name!='404.html' and not page.canonical:failures.append(f'{name}: missing canonical URL')
  if page.canonical:
   c=urlparse(page.canonical)
   if c.scheme!='https' or c.netloc not in HOSTS:failures.append(f'{name}: invalid canonical host/scheme — {page.canonical}')
   physical='/' if name=='index.html' else f'/{name}'
   if c.path not in {physical,physical.removesuffix('.html')+'/'}:warnings.append(f'{name}: canonical path {c.path!r} does not directly correspond to {physical!r}')
  if page.robots!='noindex,nofollow':failures.append(f'{name}: staging page must contain static noindex,nofollow')
  if page.theme!=THEME:failures.append(f'{name}: theme-color must be {THEME}, found {page.theme!r}')
  if not page.viewport or 'width=device-width' not in page.viewport or 'initial-scale=1' not in page.viewport:failures.append(f'{name}: missing responsive viewport contract')
  for pattern,reason in FORBIDDEN_CLAIMS.items():
   if re.search(pattern,text,re.I):failures.append(f'{name}: {reason}')
  for pattern,reason in LEGACY_PUBLIC_PATTERNS.items():
   if re.search(pattern,text,re.I):failures.append(f'{name}: {reason}')
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

 # V9 multi-device responsive contract.
 style=ROOT/'assets/style.css';edge=ROOT/'assets/v9-edge.css';v10=ROOT/'assets/v10-blue.css';js=ROOT/'assets/site.js'
 if not style.exists():failures.append('assets/style.css missing')
 else:
  css=style.read_text(encoding='utf-8')
  required=['@media (min-width:1600px)','@media (max-width:1199px)','@media (max-width:980px)','@media (max-width:760px)','@media (max-width:430px)','scroll-snap-type:x mandatory','.mobile-dock','.listing-row{display:grid','min-height:50px','100dvh','prefers-reduced-motion']
  for marker in required:
   if marker not in css:failures.append(f'V9 responsive CSS marker missing — {marker}')
  if 'Libre Caslon Display' in css or 'Plus Jakarta Sans' in css:failures.append('V8 typography dependency remains in V9 stylesheet')
  if 'Spline Sans' not in css or 'DM Mono' not in css:failures.append('V9 base typography system missing')
 if not edge.exists():failures.append('assets/v9-edge.css missing')

 # V10 premium blue + compact rhythm contract.
 if not v10.exists():failures.append('assets/v10-blue.css missing')
 else:
  blue=v10.read_text(encoding='utf-8')
  for marker in ['--signal:#2563eb','--night:#06172f','Space Grotesk','Inter:wght','statement-band{padding:62px 0}','offer-stage{padding:70px 0}','section{padding:66px 0}','@media (max-width:430px)','mobile-dock a:last-child','linear-gradient(135deg,#1f5fe5,#3478f6)']:
   if marker not in blue:failures.append(f'V10 blue/rhythm marker missing — {marker}')
  for orange in ['#ff4d1f','#ff7a52','#ffede8','#ffd1c5','#fff1ec','#ffd4c8']:
   if orange in blue.lower():failures.append(f'V10 refinement reintroduces orange token — {orange}')
 if not js.exists():failures.append('assets/site.js missing')
 else:
  script=js.read_text(encoding='utf-8')
  for marker in ['mobile-dock','viewportMode','matchMedia(\'(min-width:981px)\')','setMenu(false)','v9-edge.css','v10-blue.css']:
   if marker not in script:failures.append(f'responsive/premium interaction marker missing — {marker}')

 robots=ROOT/'robots.txt'
 if not robots.exists():failures.append('robots.txt missing')
 else:
  rt=robots.read_text(encoding='utf-8').lower()
  if 'user-agent: *' not in rt or 'disallow: /' not in rt:failures.append('robots.txt must disallow all crawling on staging')
 sitemap=ROOT/'sitemap.xml'
 if not sitemap.exists():failures.append('sitemap.xml missing')
 else:
  try:
   ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'};tree=ET.parse(sitemap);locs=[x.text.strip() for x in tree.findall('sm:url/sm:loc',ns) if x.text];seen=set()
   for loc in locs:
    if loc in seen:failures.append(f'sitemap.xml: duplicate URL — {loc}')
    seen.add(loc);u=urlparse(loc)
    if u.scheme!='https' or u.netloc not in HOSTS:failures.append(f'sitemap.xml: non-canonical host/scheme — {loc}');continue
    physical=ROOT/'index.html' if u.path=='/' else ROOT/((u.path.strip('/')+'.html') if u.path.endswith('/') else u.path.lstrip('/'))
    if not physical.exists():failures.append(f'sitemap.xml: URL has no physical page mapping — {loc}')
  except ET.ParseError as exc:failures.append(f'sitemap.xml: XML parse error — {exc}')
 for legacy in ['assets/v4.css','assets/v4-pages.css','assets/home-v3.css']:
  if (ROOT/legacy).exists():failures.append(f'legacy visual asset must be removed — {legacy}')
 print(f'Checked {len(HTML_FILES)} HTML pages.')
 for w in warnings:print(f'WARNING: {w}')
 if failures:
  print(f'\nFAILED: {len(failures)} issue(s)')
  for item in failures:print(f' - {item}')
  return 1
 print(f'PASS: V10 blue-premium, responsive, staging, disclosure and integrity guardrails clear; {len(warnings)} warning(s).')
 return 0

if __name__=='__main__':sys.exit(main())
