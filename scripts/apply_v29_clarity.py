#!/usr/bin/env python3
"""Apply V29 executive content clarity across Zepto Logic staging.

Leadership review intent:
- make the company offer obvious in seconds
- use simple semiconductor language
- centre the site on IP, Services and R&D
- expose consultation, lab/prototyping and engagement routes clearly
- retain co-creation, collaboration and co-opting terminology
- remove unnecessary menu and presentation density
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

NAV_ITEMS=[
    ('index.html','Home'),
    ('products.html','IP'),
    ('services.html','Services'),
    ('research.html','R&D'),
    ('about.html','Company'),
    ('contact.html','Contact'),
]

def active_for(page,href):
    return ' aria-current="page"' if page==href else ''

def navigation(page):
    return '<nav class="head-links" aria-label="Primary navigation">'+''.join(
        f'<a{active_for(page,href)} href="{href}">{label}</a>' for href,label in NAV_ITEMS
    )+'</nav>'

def normalize_shell(path,text):
    page=path.name
    if 'assets/v29-clarity.css' not in text:
        text=text.replace('<link rel="icon" sizes="32x32" href="assets/brand/favicon-32.png">','<link rel="stylesheet" href="assets/v29-clarity.css"><link rel="icon" sizes="32x32" href="assets/brand/favicon-32.png">')
    text=re.sub(r'<nav class="head-links" aria-label="Primary navigation">.*?</nav>',navigation(page),text,count=1,flags=re.S)
    text=re.sub(r'<a class="project-link"[^>]*href="contact\.html[^\"]*"[^>]*>.*?</a>','<a class="project-link" href="contact.html">Talk to us</a>',text,count=1,flags=re.S)
    text=text.replace('placeholder="Search IP, engineering, applications or R&amp;D"','placeholder="Search IP, services or R&amp;D"')
    text=text.replace('<h4>Technology</h4>','<h4>Offerings</h4>')
    text=text.replace('>Engineering</a>','>Services</a>')
    return text

HOME_MAIN='''<main id="main">
<section class="z-hero v18-hero v19-hero" data-v18-hero>
  <div class="wrap v29-hero-grid">
    <div class="hero-copy">
      <div class="hero-kicker-row"><div class="eyebrow">Fabless semiconductor design company · Coimbatore, India</div></div>
      <h1>Semiconductor IP. Engineering services. Applied R&amp;D.</h1>
      <p class="lead">We help chip builders and product teams reduce execution risk with reusable FPGA-validated IP, custom digital design, verification, FPGA prototyping and collaborative R&amp;D.</p>
      <div class="actions"><a class="action primary" data-track="home_offerings" href="#offerings">View our offerings →</a><a class="action ghost" data-track="home_contact" href="contact.html">Talk to us</a></div>
      <div class="hero-trust" aria-label="Engineering highlights"><span><b>13</b> FPGA-validated IP blocks</span><span><b>RTL → FPGA</b> connected engineering</span><span><b>India</b> direct technical access</span></div>
    </div>
    <aside class="v29-hero-offer" aria-label="What Zepto Logic offers">
      <header><span>What we offer</span><strong>Three clear ways to engage.</strong></header>
      <a href="products.html"><span class="num">01</span><span><b>Semiconductor IP</b><small>Reusable arithmetic and interface IP.</small></span><span class="arrow">→</span></a>
      <a href="services.html"><span class="num">02</span><span><b>Engineering Services</b><small>Architecture, RTL, verification and FPGA.</small></span><span class="arrow">→</span></a>
      <a href="research.html"><span class="num">03</span><span><b>Applied R&amp;D</b><small>Co-creation for specialised hardware.</small></span><span class="arrow">→</span></a>
    </aside>
  </div>
</section>

<section class="z-section" id="offerings">
  <div class="wrap">
    <div class="z-head"><div><div class="eyebrow">What we do</div><h2>Three core offerings. Clearly defined.</h2></div><p>Start with IP, a focused engineering service or an R&amp;D objective. We keep the scope clear and connect stages only when the programme needs it.</p></div>
    <div class="v29-pillars">
      <a class="v29-pillar" href="products.html"><div class="eyebrow">IP</div><h3>Reusable semiconductor IP</h3><p>13 FPGA-validated soft IP blocks covering floating-point, complex arithmetic and digital interfaces, with source RTL and integration collateral.</p><span class="tail">View IP portfolio →</span></a>
      <a class="v29-pillar" href="services.html"><div class="eyebrow">Services</div><h3>Semiconductor engineering</h3><p>Architecture, synthesizable RTL, UVM verification, lint, CDC/RDC, FPGA implementation, timing closure and board-level proof.</p><span class="tail">View engineering services →</span></a>
      <a class="v29-pillar" href="research.html"><div class="eyebrow">R&amp;D</div><h3>Applied hardware R&amp;D</h3><p>Research-to-hardware work for specialised compute and secure hardware through feasibility, architecture, RTL, verification and FPGA evidence.</p><span class="tail">View R&amp;D →</span></a>
    </div>
  </div>
</section>

<section class="z-section soft" id="services-menu">
  <div class="wrap">
    <div class="z-head"><div><div class="eyebrow">Our offerings</div><h2>A simple menu of what you can engage us for.</h2></div><p>Choose the closest requirement. A technical discussion can narrow the scope, evidence and commercial route.</p></div>
    <div class="v29-offerings">
      <article class="v29-offering"><span class="mark">01</span><div><h3>IP licensing &amp; evaluation</h3><p>Evaluate an FPGA-validated arithmetic or interface core against your device, clock, throughput and integration target.</p></div></article>
      <article class="v29-offering"><span class="mark">02</span><div><h3>Semiconductor consultation</h3><p>Architecture review, IP selection, verification strategy and FPGA planning for a defined technical decision.</p></div></article>
      <article class="v29-offering"><span class="mark">03</span><div><h3>Architecture &amp; RTL design</h3><p>Microarchitecture, datapaths, control, interfaces and synthesizable digital logic for custom hardware functions.</p></div></article>
      <article class="v29-offering"><span class="mark">04</span><div><h3>Design verification</h3><p>Verification planning, SystemVerilog/UVM, assertions, regression, coverage, lint and CDC/RDC engineering.</p></div></article>
      <article class="v29-offering"><span class="mark">05</span><div><h3>FPGA prototyping &amp; validation</h3><p>Implementation, constraints, timing closure, board bring-up and repeatable hardware evidence.</p></div></article>
      <article class="v29-offering"><span class="mark">06</span><div><h3>Collaborative R&amp;D</h3><p>Co-creation and co-development for specialised accelerators, secure compute and research-to-hardware programmes.</p></div></article>
    </div>
    <div class="actions"><a class="action primary" href="services.html">Explore services →</a><a class="action" href="contact.html">Request a consultation</a></div>
  </div>
</section>

<section class="v25-theatre" id="engineering-path" aria-labelledby="engineeringPathTitle" data-v25-theatre>
  <div class="wrap">
    <header class="v25-theatre-head"><div><div class="eyebrow">How we work</div><h2 id="engineeringPathTitle">From requirement to hardware proof.</h2></div><p>A clear technical boundary and reviewable evidence at each stage keep the programme focused.</p></header>
    <div class="v25-theatre-frame">
      <div class="v25-object-stage" data-v25-object-stage aria-hidden="true"><div class="v25-silicon-object" data-v25-object><div class="v25-die-core"><b data-v25-core>SPEC</b><small>digital system</small></div></div><div class="v25-object-readout"><span data-v25-kicker>01 / DEFINE</span><strong data-v25-title>Start with the boundary.</strong><p data-v25-copy>Capture interfaces, clocks, resets, data movement, target platform and the evidence needed for the next engineering decision.</p></div></div>
      <div class="v25-story-side">
        <div class="v25-rail-controls"><div class="v25-story-progress"><span data-v25-progress>01 / 05</span><i aria-hidden="true"><b></b></i></div><div class="v25-arrow-controls" aria-label="Engineering story controls"><button type="button" data-v25-prev aria-label="Previous engineering stage">←</button><button type="button" data-v25-next aria-label="Next engineering stage">→</button></div></div>
        <div class="v25-story-rail" data-v25-rail aria-label="Engineering stages">
          <button class="v25-story-card active" type="button" data-v25-step="define" aria-pressed="true"><span>01 · Define</span><strong>Define the requirement.</strong><small>Interfaces · clocks · resets · target · outcome</small></button>
          <button class="v25-story-card" type="button" data-v25-step="architect" aria-pressed="false"><span>02 · Architect</span><strong>Shape the hardware.</strong><small>Partition · datapath · control · memory</small></button>
          <button class="v25-story-card" type="button" data-v25-step="implement" aria-pressed="false"><span>03 · Implement</span><strong>Build the RTL.</strong><small>SystemVerilog · AXI · arithmetic · integration</small></button>
          <button class="v25-story-card" type="button" data-v25-step="verify" aria-pressed="false"><span>04 · Verify</span><strong>Build evidence.</strong><small>Assertions · regression · coverage · CDC/RDC</small></button>
          <button class="v25-story-card" type="button" data-v25-step="prove" aria-pressed="false"><span>05 · Prove</span><strong>Take it to FPGA.</strong><small>Constraints · timing · bring-up · hardware proof</small></button>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="z-section soft" id="engagement">
  <div class="wrap">
    <div class="z-head"><div><div class="eyebrow">Ways to work together</div><h2>Choose the engagement model that fits your team.</h2></div><p>We support a bounded work package, collaborative development or specialist capability integrated into an existing programme.</p></div>
    <div class="v29-engagement">
      <article><span>Focused work package</span><h3>Give us a defined scope.</h3><p>Use Zepto Logic for a specific IP, RTL, verification or FPGA deliverable with clear acceptance evidence.</p></article>
      <article><span>Co-creation · Collaboration</span><h3>Develop the solution together.</h3><p>Use co-engineering and co-development where architecture and implementation require joint technical iteration.</p></article>
      <article><span>Co-opting specialist capability</span><h3>Extend your existing team.</h3><p>Bring targeted semiconductor engineering capability into an established programme when specialist skills or execution bandwidth are required.</p></article>
    </div>
  </div>
</section>

<section class="z-section" id="why-zepto">
  <div class="wrap">
    <div class="z-head"><div><div class="eyebrow">Why Zepto Logic</div><h2>Small enough for direct access. Technical enough for serious hardware work.</h2></div><p>Our model combines reusable IP with hands-on engineering from Coimbatore, India, using a cost-effective engagement structure without hiding the technical boundary.</p></div>
    <div class="v29-proof"><div><strong>13 IP blocks</strong><span>FPGA-validated reusable soft IP.</span></div><div><strong>Direct access</strong><span>Technical discussion with the engineering team.</span></div><div><strong>RTL → FPGA</strong><span>Connected front-end engineering path.</span></div><div><strong>Flexible engagement</strong><span>Work package, collaboration or co-opting.</span></div></div>
  </div>
</section>

<section class="z-cta"><div class="wrap"><div><div class="eyebrow">Talk to us</div><h2>Have an IP, RTL, verification, FPGA or R&amp;D requirement?</h2><p>Share the technical problem and the outcome you need. We will map it to the right offering.</p></div><div class="actions"><a class="action primary" href="contact.html">Start a technical discussion →</a></div></div></section>
</main>'''

SERVICES_MAIN='''<main id="main">
<section class="z-page-hero"><div class="wrap"><div><div class="eyebrow">Semiconductor engineering services</div><h1>Focused engineering from architecture to FPGA proof.</h1></div><p class="intro">Support a custom silicon or digital hardware programme with architecture, RTL design, verification, IP-quality engineering, FPGA prototyping and technical consultation.</p></div></section>

<section class="z-section" id="services"><div class="wrap"><div class="z-head"><div><div class="eyebrow">What we do</div><h2>Engineering services you can engage directly.</h2></div><p>Start with one service. Connect stages only when continuity improves the engineering result.</p></div><div class="v29-service-list">
<article><span>01</span><h3>Architecture &amp; specification</h3><p>Requirements, partitioning, interfaces, clocks, resets, memory and data movement.</p></article>
<article><span>02</span><h3>RTL design</h3><p>Microarchitecture, datapaths, control and synthesizable SystemVerilog for defined digital functions.</p></article>
<article><span>03</span><h3>Design verification</h3><p>Verification planning, UVM, assertions, regression, coverage, lint and CDC/RDC.</p></article>
<article><span>04</span><h3>FPGA prototyping</h3><p>Implementation, constraints, timing closure, integration and board-level hardware proof.</p></article>
<article><span>05</span><h3>IP quality &amp; reuse readiness</h3><p>RTL quality review, structural checks, synthesis observations and integration-readiness assessment.</p></article>
<article><span>06</span><h3>Custom accelerator engineering</h3><p>Digital hardware implementation for specialised arithmetic, secure compute and research-derived workloads.</p></article>
</div></div></section>

<section class="z-section soft" id="consultation"><div class="wrap"><div class="z-head"><div><div class="eyebrow">Consultation</div><h2>Specialised semiconductor consultation for a defined decision.</h2></div><p>Use a consultation when you need an experienced technical view before committing to a larger implementation programme.</p></div><div class="z-grid4"><div class="z-card"><span class="tag">Architecture</span><h3>Architecture review</h3><p>Review partitioning, interfaces, data movement and implementation assumptions.</p></div><div class="z-card"><span class="tag">IP</span><h3>IP selection</h3><p>Assess whether reusable IP fits the target function and integration context.</p></div><div class="z-card"><span class="tag">Verification</span><h3>Verification strategy</h3><p>Define the evidence, methodology and closure plan needed for the design.</p></div><div class="z-card"><span class="tag">FPGA</span><h3>Prototype planning</h3><p>Plan constraints, platform, timing and hardware validation before implementation.</p></div></div><div class="actions"><a class="action primary" href="contact.html?type=services">Request a consultation →</a></div></div></section>

<section class="z-section" id="lab"><div class="wrap"><div class="z-head"><div><div class="eyebrow">Design &amp; prototyping lab</div><h2>Engineering work backed by FPGA prototyping and validation.</h2></div><p>Our Coimbatore design centre supports semiconductor design, FPGA prototyping, board-level bring-up, validation and secure engineering workflows. Specific platform and equipment needs are matched to the programme scope.</p></div><div class="v29-proof"><div><strong>FPGA implementation</strong><span>Target-device build and integration.</span></div><div><strong>Timing closure</strong><span>Constraints and implementation evidence.</span></div><div><strong>Board bring-up</strong><span>Hardware-level functional validation.</span></div><div><strong>Repeatable proof</strong><span>Documented results for the next decision.</span></div></div></div></section>

<section class="z-section soft" id="engagement"><div class="wrap"><div class="z-head"><div><div class="eyebrow">How to engage</div><h2>Use the commercial model that matches the technical boundary.</h2></div><p>Choose a focused work package, co-creation and collaboration, or co-opt specialist capability into an existing programme.</p></div><div class="v29-engagement"><article><span>Focused work package</span><h3>Defined scope.</h3><p>A bounded deliverable with clear technical acceptance evidence.</p></article><article><span>Co-creation · Collaboration</span><h3>Joint engineering.</h3><p>Co-engineering and co-development for a differentiated solution.</p></article><article><span>Co-opting specialist capability</span><h3>Embedded expertise.</h3><p>Add targeted Zepto Logic capability to an established engineering team or programme.</p></article></div></div></section>

<section class="z-cta"><div class="wrap"><div><div class="eyebrow">Engineering enquiry</div><h2>Tell us what you need to design, verify or prove.</h2></div><div class="actions"><a class="action primary" href="contact.html?type=services">Talk to an engineer →</a></div></div></section>
</main>'''

def replace_main(text,new_main):
    return re.sub(r'<main id="main">.*?</main>',new_main,text,count=1,flags=re.S)

def update_html():
    for path in ROOT.glob('*.html'):
        text=path.read_text(encoding='utf-8')
        text=normalize_shell(path,text)
        if path.name=='index.html':
            text=replace_main(text,HOME_MAIN)
            text=text.replace('<title>Zepto Logic | Semiconductor IP & Engineering</title>','<title>Zepto Logic | Semiconductor IP, Engineering Services & Applied R&D</title>')
            text=text.replace('Zepto Logic provides FPGA-validated semiconductor IP, architecture, RTL, verification, FPGA prototyping and applied hardware R&D from Coimbatore, India.','Zepto Logic provides FPGA-validated semiconductor IP, engineering services, consultation, FPGA prototyping and collaborative applied R&D from Coimbatore, India.')
        elif path.name=='services.html':
            text=replace_main(text,SERVICES_MAIN)
            text=text.replace('<title>RTL, Verification & FPGA Engineering | Zepto Logic</title>','<title>Semiconductor Engineering Services & Consultation | Zepto Logic</title>')
        elif path.name=='products.html':
            text=text.replace('<div class="eyebrow">Semiconductor IP</div><h1>License a proven block instead of rebuilding the function.</h1>','<div class="eyebrow">IP portfolio</div><h1>Reusable semiconductor IP for faster digital hardware development.</h1>')
            text=text.replace('Choose from 13 FPGA-validated soft IP blocks for floating-point, complex arithmetic and serial interfaces. Tell us the target device, clock, throughput, latency and integration context so the evaluation is relevant to your design.','Choose from 13 FPGA-validated soft IP blocks for floating-point, complex arithmetic and digital interfaces. Use our IP to reduce rebuild effort and keep custom engineering focused on what differentiates your system.')
        elif path.name=='research.html':
            text=text.replace('<div class="eyebrow">Applied R&amp;D</div><h1>Turn specialised computation into testable hardware evidence.</h1>','<div class="eyebrow">Applied R&amp;D</div><h1>Collaborative R&amp;D for specialised semiconductor hardware.</h1>')
            text=text.replace('Zepto Logic works on selected algorithms and security-sensitive workloads where architecture, reusable arithmetic, RTL, verification and FPGA proof are needed to evaluate the hardware path.','We co-create hardware solutions for selected algorithms and secure-compute workloads where feasibility, architecture, RTL, verification and FPGA evidence are needed before deeper implementation.')
        elif path.name=='applications.html':
            text=text.replace('<div class="eyebrow">Applications</div><h1>Start with the system problem—not a predefined service.</h1>','<div class="eyebrow">Application systems</div><h1>Map the workload to the right hardware solution.</h1>')
        path.write_text(text,encoding='utf-8')

def update_tests():
    path=ROOT/'tests/site.spec.js'
    text=path.read_text(encoding='utf-8')
    text=re.sub(r"test\('global taxonomy is consistent across top-level pages'.*?\n\n(?=test\('mobile navigation)","test('V29 primary navigation is simple and consistent',async({page})=>{for(const file of KEY_PAGES){await page.goto(`${BASE}/${file}`);const labels=await page.locator('.head-links a').allTextContents();expect(labels,`${file}: navigation`).toEqual(['Home','IP','Services','R&D','Company','Contact'])}});\n\n",text,count=1,flags=re.S)
    text=re.sub(r"test\('V28 hero uses a static precision semiconductor diagram with no video controls'.*?\n\n(?=test\('V27 engineering path)","test('V29 homepage states the offer directly with three engagement routes',async({page})=>{await page.setViewportSize({width:1440,height:900});await page.goto(BASE+'/index.html',{waitUntil:'domcontentloaded'});await expect(page.locator('h1')).toContainText('Semiconductor IP. Engineering services. Applied R&D.');await expect(page.locator('.v29-hero-offer>a')).toHaveCount(3);await expect(page.locator('.v29-pillars>a')).toHaveCount(3);await expect(page.locator('.v29-offering')).toHaveCount(6);await expect(page.locator('video,[data-hero-film],[data-film-toggle],.motion-toggle,.v25-experience')).toHaveCount(0)});\n\n",text,count=1,flags=re.S)
    text=text.replace("await page.locator('[data-v25-next]').click();await expect(page.locator('[data-v25-step=\"implement\"]')).toHaveAttribute('aria-pressed','true')", "await page.keyboard.press('ArrowRight');await expect(page.locator('[data-v25-step=\"implement\"]')).toHaveAttribute('aria-pressed','true')")
    path.write_text(text,encoding='utf-8')

def update_deep_qa():
    path=ROOT/'scripts/deep_qa.py';text=path.read_text(encoding='utf-8')
    text=text.replace('"""Deep static QA for V28 boardroom precision and production readiness."""','"""Deep static QA for V29 executive clarity and production readiness."""')
    text=text.replace("budgets={'assets/v16.css':150000,'assets/v27-executive.css':36000,'assets/v28-boardroom.css':36000,'assets/site.js':46000}","budgets={'assets/v16.css':150000,'assets/v27-executive.css':36000,'assets/v28-boardroom.css':36000,'assets/v29-clarity.css':30000,'assets/site.js':46000}")
    text=text.replace("if 'hero-technical-visual' not in home:fail.append('homepage static semiconductor visual missing')","if 'v29-hero-offer' not in home:fail.append('homepage direct offerings panel missing')\n if home.count('v29-pillar')<3:fail.append('homepage three-pillar offer missing')\n if home.count('v29-offering')<6:fail.append('homepage offering menu incomplete')\n for term in ('Semiconductor consultation','IP licensing &amp; evaluation','Design verification','FPGA prototyping &amp; validation'):\n  if term not in home:fail.append(f'homepage direct offering missing — {term}')")
    text=text.replace("for required in ('scripts/prepare_production.py','scripts/production_audit.py','PRODUCTION-MIGRATION.md','assets/v28-boardroom.css'):","for required in ('scripts/prepare_production.py','scripts/production_audit.py','PRODUCTION-MIGRATION.md','assets/v28-boardroom.css','assets/v29-clarity.css'):")
    text=text.replace("print('PASS: V28 boardroom precision, anti-spectacle, phone isolation, leadership, integrity and production-readiness gates clear.')","print('PASS: V29 executive clarity, simple offerings, phone isolation, leadership, integrity and production-readiness gates clear.')")
    path.write_text(text,encoding='utf-8')

update_html();update_tests();update_deep_qa()
print('Applied V29 executive clarity migration.')
