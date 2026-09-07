#!/usr/bin/env python3
"""Deep static QA for V28 boardroom precision and production readiness."""
from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
import sys,re

ROOT=Path(__file__).resolve().parents[1]
PAGES=sorted(ROOT.glob('*.html'))
TOP={'index.html','products.html','services.html','applications.html','research.html','about.html','news.html','careers.html','contact.html'}
BENCH={'winfomi.com','www.winfomi.com','in.micron.com','micron.com','www.micron.com','qualcomm.com','www.qualcomm.com','asml.com','www.asml.com','philips.com','www.philips.com','amd.com','www.amd.com','questglobal.com','www.questglobal.com'}

class Audit(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.assets=[];self.title='';self.desc='';self._title=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a)
  key={'img':'src','script':'src','link':'href'}.get(tag)
  if key and a.get(key):self.assets.append((tag,a[key]))
  if tag=='meta' and str(a.get('name','')).lower()=='description':self.desc=a.get('content','')
  if tag=='title':self._title=True
 def handle_endtag(self,tag):
  if tag=='title':self._title=False
 def handle_data(self,data):
  if self._title:self.title+=data

def local(page,ref):
 ref=unquote((ref or '').strip())
 if not ref or ref.startswith(('#','mailto:','tel:','javascript:','data:')):return None
 u=urlparse(ref)
 if u.scheme or u.netloc:return None
 return (ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (page.parent/u.path).resolve()

def main():
 fail=[];warn=[];titles={};descs={}
 for page in PAGES:
  raw=page.read_text(encoding='utf-8');a=Audit();a.feed(raw)
  dup=[k for k,v in Counter(a.ids).items() if v>1]
  if dup:fail.append(f'{page.name}: duplicate ids — {", ".join(dup)}')
  if page.name in TOP:
   if not a.title.strip():fail.append(f'{page.name}: empty title')
   if not a.desc.strip():fail.append(f'{page.name}: empty description')
   titles.setdefault(a.title.strip(),[]).append(page.name);descs.setdefault(a.desc.strip(),[]).append(page.name)
  for link in a.links:
   href=(link.get('href') or '').strip();u=urlparse(href)
   if href in ('#','') or href.lower().startswith('javascript:'):fail.append(f'{page.name}: placeholder link {href!r}')
   if u.hostname and u.hostname.lower() in BENCH:fail.append(f'{page.name}: benchmark link leaked — {href}')
   if link.get('target')=='_blank' and 'noopener' not in set((link.get('rel') or '').lower().split()):fail.append(f'{page.name}: target=_blank lacks noopener — {href}')
  for tag,ref in a.assets:
   p=local(page,ref)
   if p is not None and not p.exists():fail.append(f'{page.name}: missing {tag} asset — {ref}')
   u=urlparse(ref)
   if u.hostname and u.hostname.lower() in BENCH:fail.append(f'{page.name}: benchmark asset leaked — {ref}')
  if 'href="http://' in raw or "href='http://" in raw:fail.append(f'{page.name}: insecure HTTP link')
  if '<video' in raw.lower():fail.append(f'{page.name}: video remains')
  if re.search(r'<animate(?:transform)?\b',raw,re.I):fail.append(f'{page.name}: SVG animation element remains')
 for title,names in titles.items():
  if title and len(names)>1:fail.append(f'duplicate top-level title across {", ".join(names)} — {title}')
 for desc,names in descs.items():
  if desc and len(names)>1:warn.append(f'duplicate description across {", ".join(names)}')

 budgets={'assets/v16.css':150000,'assets/v27-executive.css':36000,'assets/v28-boardroom.css':36000,'assets/site.js':46000}
 for rel,limit in budgets.items():
  p=ROOT/rel
  if not p.exists():fail.append(f'budget asset missing — {rel}')
  elif p.stat().st_size>limit:fail.append(f'{rel}: {p.stat().st_size} exceeds {limit}')

 home=(ROOT/'index.html').read_text(encoding='utf-8');js=(ROOT/'assets/site.js').read_text(encoding='utf-8');v28=(ROOT/'assets/v28-boardroom.css').read_text(encoding='utf-8')
 for required in ('V28 — BOARDROOM PRECISION','--v28-ink','hero-technical-visual','v28-technical-visual','prefers-reduced-motion'):
  if required not in v28:fail.append(f'V28 stylesheet contract missing — {required}')
 for forbidden in ('tech-marquee','v20-prism-playground','v20-color-rail','v21-constellation','v20-section-nav','v21-signal-canvas','v21-pointer-spark','hero-aurora','v25-frame-word','v25-bauhaus','v25-selfdraw','data-playground','data-constellation'):
  if forbidden in home:fail.append(f'homepage retained spectacle DOM — {forbidden}')
 if home.count('data-v25-theatre')!=1 or home.count('data-v25-step=')!=5:fail.append('engineering path must contain one five-stage theatre')
 if 'hero-technical-visual' not in home:fail.append('homepage static semiconductor visual missing')
 for term in ('Co-creation · Collaboration','Co-opting specialist capability','co-development'):
  if term not in home:fail.append(f'homepage collaboration vocabulary missing — {term}')

 for forbidden in ('v25-experience','zlt_motion_level','safeLocal','heroMedia','sectionMedia','data-hero-film','data-cinematic-video','mobile_call','tel:+919626632233'):
  if forbidden in js:fail.append(f'retired runtime remains — {forbidden}')
 for required in ('V27 Executive Precision runtime','engineeringPath','searchHints','ipExplorer','website-enquiry','site_performance_sample','safeSession'):
  if required not in js:fail.append(f'lean runtime contract missing — {required}')

 about=(ROOT/'about.html').read_text(encoding='utf-8')
 for required in ('Suresh Kuppuswamy','Advanced Management Program (AMP 206)','₹250 crore MoU','3.22-acre site','Agentic Soft Labs','Quantcell’s Accelerator Foundation','The Weight of Intelligence'):
  if required not in about:fail.append(f'about.html: confirmed CEO content missing — {required}')
 if 'id="leadership"' not in about or '"@type":"Person"' not in about:fail.append('about.html: leadership anchor/Person schema missing')

 collaboration={
  'services.html':('Co-creation · Collaboration','Co-opting specialist capability','Co-engineering'),
  'research.html':('Co-creation','Collaboration','co-development','Joint R&amp;D'),
  'applications.html':('Co-create','co-engineering','co-development'),
  'contact.html':('Co-creation / co-development','Co-engineering / specialist capacity','Co-opting specialist engineering capacity')}
 for name,terms in collaboration.items():
  text=(ROOT/name).read_text(encoding='utf-8')
  for term in terms:
   if term not in text:fail.append(f'{name}: collaboration term missing — {term}')

 for page in PAGES:
  if page.name=='contact.html':continue
  raw=page.read_text(encoding='utf-8')
  if re.search(r'(?:96266\s*32233|919626632233|wa\.me/919626632233)',raw):fail.append(f'{page.name}: phone/WhatsApp outside Contact')
 contact=(ROOT/'contact.html').read_text(encoding='utf-8')
 if contact.count('+91 96266 32233')<1:fail.append('contact.html: direct phone missing')
 if contact.count('tel:+919626632233')<1:fail.append('contact.html: direct phone link missing')

 media=ROOT/'assets/media'
 if media.exists() and any(media.iterdir()):fail.append('retired media directory is not empty')
 for retired in ('scripts/generate_v22_media.py','.github/workflows/generate-v22-media.yml'):
  if (ROOT/retired).exists():fail.append(f'retired cinematic pipeline remains — {retired}')
 for required in ('scripts/prepare_production.py','scripts/production_audit.py','PRODUCTION-MIGRATION.md','assets/v28-boardroom.css'):
  if not (ROOT/required).exists():fail.append(f'production-readiness resource missing — {required}')

 print(f'Deep-audited {len(PAGES)} pages.')
 for item in warn:print('WARNING:',item)
 if fail:
  print(f'FAILED: {len(fail)} issue(s)');[print(' -',x) for x in fail];return 1
 print('PASS: V28 boardroom precision, anti-spectacle, phone isolation, leadership, integrity and production-readiness gates clear.')
 return 0
if __name__=='__main__':sys.exit(main())
