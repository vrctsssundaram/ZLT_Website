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
LIGHT_THEME='#f4f0e7';DARK_HOME_THEME='#06111c'
FORBIDDEN_CLAIMS={r'\b15\+\s*(?:FPGA[- ]validated\s*)?(?:IP|cores?|blocks?)\b':'legacy 15+ IP-count claim',r'\bsilicon[- ]validated\b':'silicon-validation claim',r'\bpatent\s+pending\b':'patent-pending claim',r'\bTRL[- ]?\d+\b':'public TRL claim',r'\bfoundry[- ]ready\b':'foundry-ready claim',r'\bDeep\s+Tech\s+Startup\b':'unapproved deep-tech recognition wording',r'\bunfiled\s+(?:invention|architecture|IP)':'filing-state disclosure'}
LEGACY_PUBLIC_PATTERNS={r'assets/(?:v4|v4-pages|home-v3|v9-edge|v10-blue)\.css':'legacy stylesheet reference',r'class=["\'][^"\']*\bsignal-chamber\b':'legacy signal-chamber component',r'class=["\'][^"\']*\bproject-composer\b':'legacy composer component',r'class=["\'][^"\']*\bevidence-tape\b':'legacy evidence-tape component',r'class=["\'][^"\']*\bproblem-atlas\b':'legacy problem-atlas component',r'class=["\'][^"\']*\btheme-toggle\b':'legacy theme-toggle component',r'\bZepto Logic at a glance\b':'legacy at-a-glance language',r'>\s*Verified\s*<':'legacy Verified label'}
REJECTED_UI_PATTERNS={r'class=["\'][^"\']*\bnexus-bar\b':'rejected Nexus relationship bar',r'class=["\'][^"\']*\bnexus-console\b':'rejected Nexus opportunity console',r'data-audience-choice':'rejected persona-routing control',r'class=["\'][^"\']*\becosystem-canvas\b':'rejected Nexus ecosystem canvas',r'\bI am here to\b':'rejected relationship-bar wording',r'\bRecommended route\b':'rejected route-console wording',r'\bExplore as\b':'rejected persona-routing wording'}

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
 return (ROOT/u.path.lstrip('/') if u.path.startswith('/') else (current.parent/u.path).resolve()),u.fragment

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
  expected_theme=DARK_HOME_THEME if name=='index.html' else LIGHT_THEME
  if page.theme!=expected_theme:failures.append(f'{name}: theme-color must be {expected_theme}, found {page.theme!r}')
  if not page.viewport or 'width=device-width' not in page.viewport or 'initial-scale=1' not in page.viewport:failures.append(f'{name}: missing responsive viewport contract')
  for pattern,reason in FORBIDDEN_CLAIMS.items():
   if re.search(pattern,text,re.I):failures.append(f'{name}: {reason}')
  for pattern,reason in LEGACY_PUBLIC_PATTERNS.items():
   if re.search(pattern,text,re.I):failures.append(f'{name}: {reason}')
  for pattern,reason in REJECTED_UI_PATTERNS.items():
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

 base=ROOT/'assets/style.css';v13=ROOT/'assets/v13.css';stature=ROOT/'assets/stature.css';js=ROOT/'assets/site.js';home=ROOT/'index.html';spec=ROOT/'V13-DESIGN-SPEC.md'
 if not base.exists():failures.append('assets/style.css missing')
 if not v13.exists():failures.append('assets/v13.css missing')
 else:
  css=v13.read_text(encoding='utf-8')
  required=['Instrument+Sans','JetBrains+Mono','.hero-v13','.hero-proof','.capability-architecture','.maturity-flow','.stature-section','.proof-spread','@media(max-width:980px)','@media(max-width:760px)','@media(max-width:430px)']
  for marker in required:
   if marker not in css:failures.append(f'V13 CSS marker missing — {marker}')
  for rejected in ['.nexus-bar{display:grid','.nexus-console{display:block','.persona-btn{display']:
   if rejected in css:failures.append(f'V13 CSS re-enables rejected Nexus UI — {rejected}')
 if not stature.exists():failures.append('assets/stature.css missing')
 elif "@import url('v13.css')" not in stature.read_text(encoding='utf-8'):failures.append('stature.css must import v13.css')
 if not js.exists():failures.append('assets/site.js missing')
 else:
  script=js.read_text(encoding='utf-8')
  required=['v13.css','ip-explorer-tools','service-flow','mobile-dock','technical_enquiry_submitted','viewportMode','cdot-samarth-zksnark.html','fp-add-sub','i2c-master']
  for marker in required:
   if marker not in script:failures.append(f'V13 runtime marker missing — {marker}')
  for rejected in ['audienceData','zl_audience=','nexus_audience_selected','data-audience-choice','ecoData','ecosystem_route_selected','insertAdjacentHTML(\'afterend\',\'<div class="nexus-bar']:
   if rejected in script:failures.append(f'V13 runtime retains rejected routing system — {rejected}')
 if home.exists():
  ht=home.read_text(encoding='utf-8')
  for marker in ['class="hero-v13','class="hero-proof','class="signal-strip','class="capability-architecture','class="maturity-flow','class="stature-section','class="proof-spread','cdot-samarth-zksnark.html']:
   if marker not in ht:failures.append(f'V13 homepage marker missing — {marker}')
  for rejected in ['class="nexus-hero','class="nexus-console','class="silicon-workbench','class="intent-lab','data-audience-choice','class="ecosystem-canvas']:
   if rejected in ht:failures.append(f'V13 homepage contains rejected/obsolete interaction — {rejected}')
 if not spec.exists():failures.append('V13 design specification missing')
 for stale in ['assets/v4.css','assets/v4-pages.css','assets/home-v3.css','assets/v9-edge.css','assets/v10-blue.css']:
  if (ROOT/stale).exists():failures.append(f'obsolete visual asset must be removed — {stale}')
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
 print(f'Checked {len(HTML_FILES)} HTML pages.')
 for w in warnings:print(f'WARNING: {w}')
 if failures:
  print(f'\nFAILED: {len(failures)} issue(s)')
  for item in failures:print(f' - {item}')
  return 1
 print(f'PASS: V13 hybrid pre-Nexus responsive, staging, disclosure and integrity guardrails clear; {len(warnings)} warning(s).')
 return 0

if __name__=='__main__':sys.exit(main())
