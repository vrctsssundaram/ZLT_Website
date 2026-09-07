#!/usr/bin/env python3
"""Apply the V28 boardroom-precision cleanup to the staging source tree.

The migration removes obsolete cinematic/motion UI, removes public phone exposure
outside the dedicated Contact page, replaces video with original inline technical
SVG diagrams, links the V28 white-first design layer, and retires unused media.
"""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
PHONE_TEXT='+91 96266 32233'
PHONE_HREF='tel:+919626632233'
WHATSAPP='https://wa.me/919626632233'

TRACE_COLORS=['blue','teal','violet','amber','coral']

def technical_svg(kind='system', hero=False):
    # Pure inline SVG: no SMIL/JS animation. A few node opacities are gently
    # modulated by CSS and disappear under prefers-reduced-motion.
    if kind=='ip':
        traces=[(110,300,270,300,'blue'),(470,300,650,300,'teal'),(370,135,370,220,'violet'),(370,380,370,485,'amber')]
        blocks=[(292,240,156,120)]
    elif kind=='engineering':
        traces=[(95,180,250,180,'blue'),(250,180,360,300,'teal'),(360,300,505,300,'violet'),(505,300,660,410,'amber')]
        blocks=[(150,135,100,90),(310,255,100,90),(455,255,100,90),(610,365,100,90)]
    elif kind=='applications':
        traces=[(130,170,365,300,'blue'),(365,300,610,150,'teal'),(365,300,630,425,'violet'),(365,300,130,440,'amber')]
        blocks=[(320,255,100,90)]
    elif kind=='research':
        traces=[(115,390,265,315,'blue'),(265,315,375,180,'violet'),(375,180,500,315,'teal'),(500,315,650,390,'amber')]
        blocks=[(318,260,114,96)]
    else:
        traces=[(95,300,270,300,'blue'),(470,300,655,300,'teal'),(370,115,370,225,'violet'),(370,375,370,500,'amber'),(255,185,310,245,'coral')]
        blocks=[(292,240,156,120)]
    parts=[]
    parts.append('<svg viewBox="0 0 760 600" role="img" aria-label="Illustrative semiconductor die and signal-path diagram" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<circle class="v28-svg-wafer" cx="380" cy="300" r="235"/>')
    for r in (190,145,100):
        parts.append(f'<circle class="v28-svg-grid" cx="380" cy="300" r="{r}"/>')
    for x in range(190,571,38):
        parts.append(f'<path class="v28-svg-grid" d="M{x} 120 V480"/>')
    for y in range(150,451,38):
        parts.append(f'<path class="v28-svg-grid" d="M190 {y} H570"/>')
    for x,y,w,h in blocks:
        parts.append(f'<rect class="v28-svg-chip" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>')
        inset=18
        parts.append(f'<rect class="v28-svg-core" x="{x+inset}" y="{y+inset}" width="{w-2*inset}" height="{h-2*inset}" rx="7"/>')
    for i,(x1,y1,x2,y2,color) in enumerate(traces):
        mx=(x1+x2)//2
        parts.append(f'<path class="v28-svg-trace {color}" d="M{x1} {y1} H{mx} V{y2} H{x2}"/>')
        cls='v28-svg-spark '+('s2' if i%3==1 else 's3' if i%3==2 else '')
        parts.append(f'<circle class="v28-svg-node {color} {cls}" cx="{x2}" cy="{y2}" r="8"/>')
    # quiet corner registration marks communicate precision without sci-fi grids
    parts.append('<path class="v28-svg-grid" d="M120 110 h42 M120 110 v42 M640 110 h-42 M640 110 v42 M120 490 h42 M120 490 v-42 M640 490 h-42 M640 490 v-42"/>')
    parts.append('</svg>')
    klass='hero-technical-visual' if hero else f'v28-technical-visual v28-visual-{kind}'
    return f'<div class="{klass}" aria-hidden="true">'+''.join(parts)+'</div>'

def remove_global_phone(html, keep_contact_direct=False):
    # Header phone appears immediately inside head-actions.
    html=re.sub(r'(<div class="head-actions">)\s*<a href="tel:\+919626632233">\+91 96266 32233</a>',r'\1',html)
    # Footer phone / WhatsApp should never be global repeated contact data.
    def clean_foot(m):
        inner=m.group(1)
        inner=re.sub(r'<a href="tel:\+919626632233">\+91 96266 32233</a>','',inner)
        inner=re.sub(r'<a href="https://wa\.me/919626632233"[^>]*>WhatsApp →</a>','',inner)
        return '<div class="foot-contact">'+inner+'</div>'
    html=re.sub(r'<div class="foot-contact">(.*?)</div>',clean_foot,html,flags=re.S)
    if not keep_contact_direct:
        html=re.sub(r'<a href="tel:\+919626632233">\+91 96266 32233</a>','',html)
        html=re.sub(r'<a href="https://wa\.me/919626632233"[^>]*>.*?</a>','',html,flags=re.S)
        html=html.replace('"telephone":"+91 96266 32233",','').replace(',"telephone":"+91 96266 32233"','')
    return html

def transform_html(path):
    text=path.read_text(encoding='utf-8')
    is_contact=path.name=='contact.html'
    text=remove_global_phone(text,keep_contact_direct=is_contact)
    if 'assets/v28-boardroom.css' not in text:
        text=text.replace('<link rel="stylesheet" href="assets/v27-executive.css">','<link rel="stylesheet" href="assets/v27-executive.css"><link rel="stylesheet" href="assets/v28-boardroom.css">')
    # Remove any explicit film/motion control left in source.
    text=re.sub(r'<button class="motion-toggle"[^>]*>.*?</button>','',text,flags=re.S)
    text=re.sub(r'<button class="v22-film-toggle"[^>]*>.*?</button>','',text,flags=re.S)
    # Home cinematic video -> static precision semiconductor illustration.
    if path.name=='index.html':
        text=re.sub(r'<div class="hero-film" aria-hidden="true">.*?</div>\s*<div class="wrap">',technical_svg('system',hero=True)+'\n  <div class="wrap">',text,flags=re.S,count=1)
    # Domain cinematic video stage -> page-relevant technical diagram.
    kind_map={'products.html':'ip','services.html':'engineering','applications.html':'applications','research.html':'research'}
    kind=kind_map.get(path.name)
    if kind:
        text=re.sub(r'<div class="v22-film-stage" data-film-stage>.*?<div class="v22-film-copy">',technical_svg(kind)+'\n<div class="v22-film-copy">',text,flags=re.S,count=1)
        chips={
          'ip':['Source RTL','Verification','Integration guidance','Synthesis evidence'],
          'engineering':['Architecture','RTL implementation','Verification','FPGA proof'],
          'applications':['Workload','Interfaces','Compute path','System context'],
          'research':['Feasibility','Architecture','RTL evidence','FPGA evidence']
        }[kind]
        text=re.sub(r'<div class="v22-film-chips">.*?</div>','<div class="v22-film-chips">'+''.join(f'<span>{x}</span>' for x in chips)+'</div>',text,flags=re.S,count=1)
    # There should be no video or SMIL animation after this migration.
    text=re.sub(r'<video\b.*?</video>','',text,flags=re.S)
    text=re.sub(r'<animate(?:Transform)?\b.*?</animate(?:Transform)?>','',text,flags=re.S)
    path.write_text(text,encoding='utf-8')

def replace_test(src,name,replacement):
    marker="test('"+name+"'"
    start=src.find(marker)
    if start<0:
        return src
    nxt=src.find("\ntest('",start+len(marker))
    if nxt<0:
        nxt=len(src)
    return src[:start]+replacement.rstrip()+"\n\n"+src[nxt+1:]

for page in ROOT.glob('*.html'):
    transform_html(page)

# Runtime cleanup: remove all film/experience systems and phone Call dock.
js_path=ROOT/'assets/site.js'
js=js_path.read_text(encoding='utf-8')
js=js.replace('routing, media lifecycle, engineering stages, accessibility controls,\n   performance sampling and light reveal/navigation ergonomics.', 'routing, engineering stages, responsive navigation,\n   performance sampling and light reveal/navigation ergonomics.')
js=js.replace("document.body.classList.add('page-'+page,'v27');","document.body.classList.add('page-'+page,'v27','v28');")
js=js.replace("document.documentElement.classList.add('v27');","document.documentElement.classList.add('v27','v28');")
js=re.sub(r"const safeLocal=.*?;\n",'',js,count=1)
js=re.sub(r"const saveData=.*?;\n",'',js,count=1)
start=js.find('/* ---------------------------------------------------------------------\n   Media lifecycle')
end=js.find('/* ---------------------------------------------------------------------\n   Quick mobile contact',start)
if start>=0 and end>start:
    js=js[:start]+"/* ---------------------------------------------------------------------\n   Static technical visuals require no media or motion-control runtime.\n   --------------------------------------------------------------------- */\n\n"+js[end:]
js=js.replace("if(!$('.mobile-dock'))document.body.insertAdjacentHTML('beforeend','<div class=\"mobile-dock\" aria-label=\"Quick contact\"><a href=\"tel:+919626632233\" data-track=\"mobile_call\">Call</a><a href=\"contact.html\" data-track=\"mobile_enquire\">Start enquiry →</a></div>');","if(!$('.mobile-dock'))document.body.insertAdjacentHTML('beforeend','<div class=\"mobile-dock\" aria-label=\"Quick enquiry\"><a href=\"contact.html\" data-track=\"mobile_enquire\">Start enquiry →</a></div>');")
js_path.write_text(js,encoding='utf-8')

# Update existing browser contracts that explicitly expected retired video/UI.
test_path=ROOT/'tests/site.spec.js'
tests=test_path.read_text(encoding='utf-8')
tests=replace_test(tests,'V27 retains high-resolution hero film as a supporting visual',"""test('V28 hero uses a static precision semiconductor diagram with no video controls',async({page})=>{await page.setViewportSize({width:1440,height:900});await page.goto(BASE+'/index.html',{waitUntil:'domcontentloaded'});await expect(page.locator('video,[data-hero-film],[data-film-toggle]')).toHaveCount(0);const visual=page.locator('.hero-technical-visual');await expect(visual).toBeVisible();await expect(visual.locator('svg')).toHaveCount(1);await expect(visual.locator('.v28-svg-chip')).toHaveCount(1);await expect(page.locator('.motion-toggle,.v25-experience')).toHaveCount(0)});""")
tests=replace_test(tests,'domain films remain local and visually subordinate',"""test('domain visual bands use static relevant technical SVGs',async({page})=>{for(const file of ['products.html','services.html','applications.html','research.html']){await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});await expect(page.locator('video,[data-cinematic-video],[data-cinematic-toggle]')).toHaveCount(0);const visual=page.locator('.v28-technical-visual');await expect(visual).toHaveCount(1);await expect(visual.locator('svg')).toHaveCount(1)}});""")
tests=replace_test(tests,'reduced motion pauses media and leaves all content available',"""test('reduced motion leaves all static content available',async({browser})=>{const context=await browser.newContext({viewport:{width:1440,height:900},reducedMotion:'reduce'});const page=await context.newPage();await page.goto(BASE+'/index.html',{waitUntil:'domcontentloaded'});await expect(page.locator('.hero-copy')).toBeVisible();await expect(page.locator('video,.v25-experience,.motion-toggle')).toHaveCount(0);const hidden=await page.locator('.reveal-v18').evaluateAll(es=>es.filter(e=>getComputedStyle(e).opacity==='0').length);expect(hidden).toBe(0);await context.close()});""")
tests=replace_test(tests,'Save-Data starts section film paused but permits explicit opt-in',"""test('Save-Data has no film subsystem to manage',async({browser})=>{const context=await browser.newContext({viewport:{width:1440,height:900}});await context.addInitScript(()=>{Object.defineProperty(navigator,'connection',{configurable:true,value:{saveData:true}})});const page=await context.newPage();await page.goto(`${BASE}/products.html`,{waitUntil:'domcontentloaded'});await expect(page.locator('video,[data-cinematic-toggle],.v25-experience')).toHaveCount(0);await expect(page.locator('.v28-technical-visual')).toBeVisible();await context.close()});""")
tests=replace_test(tests,'experience control supports full calm still text and contrast preferences',"""test('retired Experience Motion Text Contrast controls are absent from UI',async({page})=>{await page.goto(BASE+'/index.html',{waitUntil:'domcontentloaded'});await expect(page.locator('.v25-experience,.v25-experience-toggle,[data-v25-level],[data-v26-text],[data-v26-contrast]')).toHaveCount(0);await expect(page.locator('body')).not.toContainText('Motion disabled')});""")
tests=replace_test(tests,'site remains functional when Web Storage is unavailable',"""test('site remains functional when Web Storage is unavailable',async({browser})=>{const context=await browser.newContext({viewport:{width:1440,height:900}});await context.addInitScript(()=>{for(const name of ['localStorage','sessionStorage']){try{const s=window[name];s.getItem=()=>{throw new DOMException('blocked','SecurityError')};s.setItem=()=>{throw new DOMException('blocked','SecurityError')};s.removeItem=()=>{throw new DOMException('blocked','SecurityError')}}catch(_){}}});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(BASE+'/index.html',{waitUntil:'domcontentloaded'});await expect(page.locator('h1')).toBeVisible();await expect(page.locator('.v25-experience')).toHaveCount(0);await page.locator('.search-button').click();await expect(page.locator('.search-dialog')).toHaveClass(/open/);expect(errors).toEqual([]);await context.close()});""")
tests=replace_test(tests,'cinematic media decodes at intended duration and resolution',"""test('no cinematic media remains in the rendered website',async({page})=>{for(const file of KEY_PAGES){await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});await expect(page.locator('video,source[data-media],.motion-toggle,.v22-film-toggle')).toHaveCount(0)}});""")
tests=replace_test(tests,'mobile hero selects portrait high-resolution source',"""test('mobile hero static visual fits without clipping',async({page})=>{await page.setViewportSize({width:390,height:844});await page.goto(`${BASE}/index.html`,{waitUntil:'domcontentloaded'});const visual=page.locator('.hero-technical-visual');await expect(visual).toBeVisible();const b=await visual.boundingBox();expect(b.x).toBeGreaterThanOrEqual(0);expect(b.x+b.width).toBeLessThanOrEqual(390.5);await expect(visual.locator('svg')).toHaveCount(1)});""")
# Screenshot capture no longer needs to pause videos or force a motion preference.
tests=tests.replace("document.body.classList.add('v25-motion-still');document.querySelectorAll('video').forEach(v=>v.pause());","")
test_path.write_text(tests,encoding='utf-8')

# Remove media assets/generator and obsolete application workflow.
for p in (ROOT/'assets/media').glob('*') if (ROOT/'assets/media').exists() else []:
    if p.is_file(): p.unlink()
media_dir=ROOT/'assets/media'
if media_dir.exists() and not any(media_dir.iterdir()): media_dir.rmdir()
for rel in ['scripts/generate_v22_media.py','.github/workflows/generate-v22-media.yml','.github/workflows/apply-v27-executive.yml']:
    p=ROOT/rel
    if p.exists(): p.unlink()

# Reconcile asset manifest to current production candidate.
manifest_path=ROOT/'ASSET-MANIFEST.json'
if manifest_path.exists():
    data=json.loads(manifest_path.read_text(encoding='utf-8'))
    data['version']='v28-boardroom-precision'
    data['status']='staging-release-candidate'
    data['active_media']=[]
    data['current_ui_features']=[
      'White-first executive semiconductor visual system',
      'Original inline static/minimal-motion semiconductor diagrams',
      'Five-stage engineering review path',
      '13-block FPGA-validated IP explorer',
      'Ctrl/Cmd+K technical command palette',
      'Responsive page-local navigation',
      'Keyboard and reduced-motion accessibility',
      'Supabase-backed technical enquiry with email fallback',
      'Local performance dataLayer instrumentation',
      'Production-package and migration-readiness automation'
    ]
    data['retired_assets']=['V19/V22/V24 cinematic video assets and generators','V25/V26 user-facing Experience/Motion control','Mobile Call dock']
    manifest_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

print('V28 boardroom-precision migration applied.')
