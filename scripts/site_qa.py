#!/usr/bin/env python3
"""Release integrity checks for the V31 service-led site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
import re,json,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[];self.h1=0;self.canonical=[];self.robots=[];self.alt=[];self.lang=None;self.title=False
 def handle_starttag(self,t,at):
  a=dict(at)
  if t=='html':self.lang=a.get('lang')
  if t=='h1':self.h1+=1
  if t=='title':self.title=True
  if a.get('id'):self.ids.append(a['id'])
  if t=='img':self.alt.append(a.get('alt'))
  if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'));return
  if t=='meta' and a.get('name')=='robots':self.robots.append(a.get('content'))
  k={'a':'href','link':'href','script':'src','img':'src'}.get(t)
  if k and a.get(k):self.refs.append(a[k])
def check(root,production=False):
 failures=[];pages={}
 for f in root.glob('*.html'):
  p=Page();p.feed(f.read_text());pages[f.name]=p
 for name,p in pages.items():
  raw=(root/name).read_text()
  if p.h1!=1:failures.append(f'{name}: expected one H1')
  if p.lang!='en' or not p.title:failures.append(f'{name}: title/language missing')
  if len(p.ids)!=len(set(p.ids)):failures.append(f'{name}: duplicate IDs')
  if None in p.alt:failures.append(f'{name}: missing image alt')
  if len(p.canonical)!=1 or not p.canonical[0].startswith('https://zeptologic.com/'):failures.append(f'{name}: canonical missing')
  if not p.robots or (not production and p.robots!=['noindex,nofollow']):failures.append(f'{name}: invalid staging robots')
  if 'assets/site-v31.css' not in raw or 'assets/site-v31.js' not in raw:failures.append(f'{name}: current assets missing')
  if name!='contact.html' and 'tel:' in raw:failures.append(f'{name}: phone outside contact')
  for pattern in [r'\bsilicon[- ]validated\b',r'\bfoundry[- ]ready\b',r'\bguaranteed\b',r'\bpatent[- ]pending\b',r'\btrusted by\b',r'\bISO[- ]?\d{4,5}\b']:
   if re.search(pattern,raw,re.I):failures.append(f'{name}: unsupported claim {pattern}')
  for ref in p.refs:
   u=urlparse(ref)
   if u.scheme or u.netloc:continue
   f=unquote(u.path).lstrip('/') or name
   target=root/f
   if target.is_dir():target=target/'index.html'
   if not target.exists():failures.append(f'{name}: missing {ref}');continue
   if u.fragment and target.name in pages and unquote(u.fragment) not in pages[target.name].ids:failures.append(f'{name}: missing anchor {ref}')
 apps=json.loads((root/'assets/applications.json').read_text())
 if len(apps)!=13:failures.append('Exactly 13 application areas required')
 for app in apps:
  if app['id'] not in pages['applications.html'].ids:failures.append(f'Missing application {app["id"]}')
 urls={n.text for n in ET.parse(root/'sitemap.xml').getroot().iter() if n.tag.endswith('loc')}
 expected={p.canonical[0] for n,p in pages.items() if n not in ['404.html','enquiry-received.html']}
 if urls!=expected:failures.append('Sitemap/canonical mismatch')
 if failures:print('\n'.join(failures));raise SystemExit(1)
 print(f'PASS: {len(pages)} pages, 13 areas, local links, anchors, metadata and claim checks')
if __name__=='__main__':check(ROOT)
