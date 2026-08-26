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
FORBIDDEN_CLAIMS={r'\b15\+\s*(?:FPGA[- ]validated\s*)?(?:IP|cores?|blocks?)\b':'legacy 15+ IP-count claim',r'\bsilicon[- ]validated\b':'silicon-validation claim',r'\bpatent\s+pending\b':'patent-pending claim',r'\bTRL[- ]?\d+\b':'public TRL claim',r'\bfoundry[- ]ready\b':'foundry-ready claim',r'\bDeep\s+Tech\s+Startup\b':'unapproved deep-tech recognition wording',r'\bunfiled\s+(?:invention|architecture|IP)':'filing-state disclosure'}
REJECTED_UI={r'class=["\'][^"\']*\bnexus-bar\b':'rejected Nexus relationship bar',r'class=["\'][^"\']*\bnexus-console\b':'rejected Nexus opportunity console',r'data-audience-choice':'rejected persona-routing control',r'class=["\'][^"\']*\becosystem-canvas\b':'rejected ecosystem routing canvas',r'class=["\'][^"\']*\bsilicon-workbench\b':'retired Silicon Workbench',r'class=["\'][^"\']*\bintent-lab\b':'retired Intent Lab',r'\bI am here to\b':'rejected relationship wording',r'\bRecommended route\b':'rejected route wording',r'\bExplore as\b':'rejected persona wording'}
LEGACY_PUBLIC={r'assets/(?:v4|v4-pages|home-v3|v9-edge|v10-blue|v13)\.css':'retired stylesheet reference',r'class=["\'][^"\']*\bsignal-chamber\b':'legacy signal chamber',r'class=["\'][^"\']*\bproject-composer\b':'legacy composer',r'\bZepto Logic at a glance\b':'legacy at-a-glance language',r'>\s*Verified\s*<':'legacy Verified label'}
SMALLNESS={r'\bno budget question\b':'smallness marketing',r'\bdoes not justify building a permanent organisation\b':'smallness marketing',r'\btoo focused to justify a new team\b':'smallness marketing',r'\bnot a staffing form\b':'defensive staffing language',r'\bnot a generic internship form\b':'defensive careers language',r'\bbefore you fund another internal build\b':'defensive rebuild language',r'\baccessible enough for the focused job\b':'smallness marketing'}
GLOBAL_POSITIONING={r'\bIndian semiconductor IP\b':'India-limiting semiconductor-IP positioning',r'\bIndian-owned semiconductor(?: IP)?\b':'nationality-led semiconductor positioning',r'\bIndigenous semiconductor IP\b':'nationality-led semiconductor-IP positioning',r'\bDomestic semiconductor capability\b':'domestic-only positioning',r'\bDomestic semiconductor engagement\b':'domestic-only engagement positioning',r'\blarger Indian semiconductor ambition\b':'India-limiting company positioning'}
EXECUTIVE_VOICE={r'\bWhat you can engage today\b':'lecture-style commercial heading',r'\bKnow exactly where Zepto Logic can enter your programme\b':'programme-limiting sales narration',r'\bEvaluate the engineering company behind the commercial offer\b':'defensive buyer-qualification narration',r'\bSee the proof before starting the commercial conversation\b':'defensive proof narration',r'\bMove a commercial requirement now\b':'over-scripted commercial instruction',r'\bEach commercial path has a concrete technical output\b':'over-explained commercial path narration',r'\bProgramme proof\b':'generic programme-proof marketing label',r'\bPublic programme evidence\b':'generic programme-evidence marketing label'}

class PageParser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.refs=[];self.ids=set();self.images=[];self.canonical=None;self.h1_count=0;self.robots=None;self.theme=None;self.viewport=None;self.lang=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
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
  if page.theme and page.theme.startswith('#') and hex_luminance(page.theme)<.25:failures.append(f'{name}: dark browser theme-color is prohibited — {page.theme}')
  if not page.viewport or 'width=device-width' not in page.viewport or 'initial-scale=1' not in page.viewport:failures.append(f'{name}: missing responsive viewport contract')
  for group in (FORBIDDEN_CLAIMS,REJECTED_UI,LEGACY_PUBLIC,SMALLNESS,GLOBAL_POSITIONING,EXECUTIVE_VOICE):
   for pattern,reason in group.items():
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

 css_path=ROOT/'assets/style.css';js_path=ROOT/'assets/site.js';home=ROOT/'index.html';spec=ROOT/'V15-DESIGN-SPEC.md';browser_test=ROOT/'tests/site.spec.js';workflow=ROOT/'.github/workflows/site-qa.yml'
 if not css_path.exists():failures.append('assets/style.css missing')
 else:
  css=css_path.read_text(encoding='utf-8')
  required=['Manrope','IBM+Plex+Mono','.hero-v13','.hero-proof','.capability-architecture','.maturity-flow','.stature-section','.proof-spread','.mobile-dock','@media(min-width:1600px)','@media(max-width:1199px)','@media(max-width:980px)','@media(max-width:760px)','@media(max-width:430px)','prefers-reduced-motion']
  for marker in required:
   if marker not in css:failures.append(f'V15 base CSS marker missing — {marker}')
  forbidden_tokens=['--night:','--graphite:','background:var(--ink)','background:var(--ink2)','background:#000','background:#050','background:#06111c','background:#07101d','background:#101820','background:#111a22','background:#0a1728']
  for token in forbidden_tokens:
   if token.lower() in css.lower():failures.append(f'V15 dark-surface token present — {token}')
  for m in re.finditer(r'background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})',css):
   if hex_luminance(m.group(1))<.08:failures.append(f'V15 dark background declaration prohibited — {m.group(0)}')
 if (ROOT/'assets/v13.css').exists():failures.append('assets/v13.css must be removed')
 stature=ROOT/'assets/stature.css'
 if not stature.exists():failures.append('assets/stature.css compatibility file missing')
 else:
  st=stature.read_text(encoding='utf-8')
  if '@import' in st:failures.append('stature.css must not import another visual layer')
  for marker in ['.signal-map','@keyframes v15Trace','.signal-node','prefers-reduced-motion']:
   if marker not in st:failures.append(f'V15 visual marker missing — {marker}')
 if not js_path.exists():failures.append('assets/site.js missing')
 else:
  script=js_path.read_text(encoding='utf-8')
  required=['Start a discussion','Contact →','ip-explorer-tools','service-flow','mobile-dock','technical_enquiry_submitted','viewportMode','cdot-samarth-zksnark.html','fp-add-sub','i2c-master','website-enquiry']
  for marker in required:
   if marker not in script:failures.append(f'V15 runtime marker missing — {marker}')
  for rejected in ['audienceData','nexus_audience_selected','data-audience-choice','ecoData','ecosystem_route_selected','v13.css']:
   if rejected in script:failures.append(f'V15 runtime retains retired system — {rejected}')
 if home.exists():
  ht=home.read_text(encoding='utf-8')
  for marker in ['class="hero-v13','class="hero-proof signal-map','class="signal-strip','class="capability-architecture','class="maturity-flow','class="stature-section','class="proof-spread','cdot-samarth-zksnark.html']:
   if marker not in ht:failures.append(f'V15 homepage marker missing — {marker}')
  for pattern,reason in {r'\b13\s+FPGA[- ]validated':'homepage small-count stature claim',r'\b9\s*\+\s*4\b':'homepage 9+4 stature claim',r'Nine arithmetic (?:IP )?blocks? and four interface (?:IP )?blocks?':'homepage explicit small portfolio decomposition'}.items():
   if re.search(pattern,ht,re.I):failures.append(f'index.html: {reason}')
 if not spec.exists():failures.append('V15 design specification missing')
 if not browser_test.exists():failures.append('tests/site.spec.js missing')
 if not workflow.exists():failures.append('site QA workflow missing')
 else:
  wf=workflow.read_text(encoding='utf-8')
  for marker in ['browser-qa','playwright','responsive-review-screenshots','website-enquiry']:
   if marker not in wf:failures.append(f'Browser QA workflow marker missing — {marker}')
 for stale in ['assets/v4.css','assets/v4-pages.css','assets/home-v3.css','assets/v9-edge.css','assets/v10-blue.css','assets/v13.css']:
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
 print(f'PASS: V15 global-market voice, light visual, responsive, staging, disclosure and integrity guardrails clear; {len(warnings)} warning(s).')
 return 0

if __name__=='__main__':sys.exit(main())
