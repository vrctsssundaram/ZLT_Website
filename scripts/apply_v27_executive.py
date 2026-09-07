#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

# 1) Activate the executive precision stylesheet across all HTML pages.
for page in ROOT.glob('*.html'):
    text=page.read_text(encoding='utf-8')
    link='<link rel="stylesheet" href="assets/v27-executive.css">'
    if link not in text:
        text=text.replace('<link rel="stylesheet" href="assets/v16.css">','<link rel="stylesheet" href="assets/v16.css">'+link)
    text=text.replace('<meta name="theme-color" content="#07162f">','<meta name="theme-color" content="#ffffff">')
    page.write_text(text,encoding='utf-8')

# 2) Simplify the homepage: remove decorative/Matrix-style spectacle layers.
index=ROOT/'index.html'
text=index.read_text(encoding='utf-8')

# Remove ticker.
text=re.sub(r'<section class="tech-marquee"[\s\S]*?</section>\s*','',text,count=1)
# Remove interactive playground, colour rail and constellation completely.
text=re.sub(r'<section class="v20-prism-playground"[\s\S]*?</section>\s*(?=<section class="v20-color-rail")','',text,count=1)
text=re.sub(r'<section class="v20-color-rail"[\s\S]*?</section>\s*','',text,count=1)
text=re.sub(r'<section class="v21-constellation"[\s\S]*?</section>\s*(?=<section class="z-section buyer-routes)','',text,count=1)

# Remove aurora/live-pulse language from the hero and tighten the proposition.
text=re.sub(r'<div class="hero-aurora"[\s\S]*?</div>\s*','',text,count=1)
text=text.replace('<div class="hero-kicker-row"><div class="eyebrow">Semiconductor IP · RTL · Verification · FPGA · Secure Compute</div><span class="live-pill"><i></i> Design → Verify → Prove</span><button class="motion-toggle" type="button" data-film-toggle aria-pressed="false"><span aria-hidden="true">Ⅱ</span> Pause motion</button></div>',
'<div class="hero-kicker-row"><div class="eyebrow">Fabless semiconductor design · Coimbatore, India</div><button class="motion-toggle" type="button" data-film-toggle aria-pressed="false"><span aria-hidden="true">Ⅱ</span> Pause film</button></div>')
text=text.replace('<h1><span>From silicon idea</span><span class="gradient-text">to verified hardware.</span></h1>',
'<h1><span>Semiconductor IP and engineering.</span> <span class="gradient-text">From architecture to FPGA proof.</span></h1>')
text=text.replace('License FPGA-validated semiconductor IP or bring us the architecture, RTL, verification or FPGA challenge that is holding your programme back. Zepto Logic connects reusable building blocks with direct engineering execution.',
'Zepto Logic develops reusable digital IP and delivers architecture, RTL, verification and FPGA engineering for advanced electronic systems. Engage us for a defined block, a co-creation workstream, technical collaboration or specialist capability within an existing programme.')
text=text.replace('Start a technical conversation →','Discuss a requirement →',1)

# Remove the hidden duplicate route panel from the hero; the page presents one clear route architecture below.
text=re.sub(r'<aside class="z-hero-side hero-stage"[\s\S]*?</aside>\s*','',text,count=1)

# Replace the six-card buyer-route grid with four precise engagement outcomes.
pattern=r'<section class="z-section buyer-routes spectrum-section">[\s\S]*?</section>\s*(?=<section class="z-section technology-section")'
replacement='''<section class="z-section buyer-routes spectrum-section"><div class="wrap"><div class="z-head"><div><div class="eyebrow">How we engage</div><h2>Start with the engineering outcome.</h2></div><p>Choose the relationship model that matches the programme. Zepto Logic can provide reusable IP, execute a bounded engineering work package, co-create and collaborate with an existing team, or co-opt specialist capability into a longer programme.</p></div><div class="z-grid4"><a class="z-card" href="products.html"><span class="tag">Reuse</span><h3>License validated semiconductor IP</h3><p>Start from an existing arithmetic or interface block when rebuilding the function adds no differentiation.</p><span class="tail">Explore 13 IP blocks →</span></a><a class="z-card" href="services.html"><span class="tag">Execute</span><h3>Commission a defined engineering workstream</h3><p>Architecture, RTL, verification and FPGA implementation around a clear technical boundary and deliverable.</p><span class="tail">Explore engineering →</span></a><a class="z-card" href="contact.html?type=research"><span class="tag">Co-creation · Collaboration</span><h3>Develop differentiated hardware together</h3><p>Work jointly on architecture, specialised accelerators, secure compute or applied R&amp;D where iteration matters.</p><span class="tail">Discuss co-creation →</span></a><a class="z-card" href="contact.html?type=partnership"><span class="tag">Co-opting</span><h3>Bring specialist capability into the programme</h3><p>Co-opt focused semiconductor engineering capacity into an existing team when continuity, expertise or execution bandwidth is required.</p><span class="tail">Discuss partnership →</span></a></div></div></section>'''
text=re.sub(pattern,replacement,text,count=1)

# Tighten duplicated wording in remaining sections.
text=text.replace('Choose the shortest credible path to implementation.','A focused path from requirement to implementation.')
text=text.replace('Reuse a validated block where it fits. Commission custom engineering only where your system needs something different. The goal is a technically defensible path from requirement to integration evidence.',
'Reuse validated IP where it fits; apply custom engineering only where the system requires differentiation. Architecture, verification and FPGA evidence remain connected to the same technical objective.')
text=text.replace('Tell us where the hardware has to work.','Apply the engineering to the system context.')
text=text.replace('The same IP and engineering base can be applied across embedded platforms, numerical datapaths, secure systems, networking functions and accelerator-oriented designs.',
'The same IP and engineering base supports numerical compute, embedded control, secure systems, communications and specialised accelerators.')
text=text.replace('Co-develop hardware where off-the-shelf IP is not enough.','Co-create specialised hardware where standard IP is not enough.')
text=text.replace('Current work spans cryptographic acceleration, modular arithmetic, post-quantum accelerator elements, secure processing and specialised digital architectures.',
'Applied R&D focuses on cryptographic acceleration, modular arithmetic, post-quantum hardware elements, secure processing and specialised digital architectures.')
text=text.replace('Technical access before commercial complexity.','Direct engineering access with clear programme boundaries.')
text=text.replace('Early conversations can stay non-confidential. Once the scope is relevant, protected detail can move through an NDA and a defined evaluation or engineering workstream.',
'Start with non-confidential technical context. Move protected RTL, architecture or invention detail under NDA once the workstream is defined.')
text=text.replace('Go deeper without losing the system context.','Technical depth, organised by engineering need.')
text=text.replace('Move from the portfolio into implementation methods, verification, FPGA proof, IP-readiness review and public programme evidence through focused technical routes.',
'Use focused technical routes for IP, RTL, verification, FPGA implementation, IP-readiness review and public programme evidence.')
text=text.replace('Send the requirement. We will route it to the right technical path.','Bring the requirement. We will define the right technical path.')

index.write_text(text,encoding='utf-8')

# 3) Update QA to reflect the restrained visual system.
test=ROOT/'tests'/'site.spec.js'
if test.exists():
    t=test.read_text(encoding='utf-8')
    t=t.replace("await expect(page.locator('.tech-marquee')).toBeVisible();","await expect(page.locator('.tech-marquee,.v20-prism-playground,.v20-color-rail,.v21-constellation')).toHaveCount(0);")
    t=t.replace("const animation=await page.locator('.marquee-track').evaluate(e=>getComputedStyle(e).animationName);expect(animation).toBe('none');","")
    t=t.replace("const railAnim=await page.locator('.v20-color-track').evaluate(e=>getComputedStyle(e).animationName);expect(railAnim).toBe('none');","")
    # Executive-precision contract.
    anchor="test('V19 original hero film is local, silent and user-controllable'"
    if "V27 executive precision removes Matrix-style spectacle" not in t and anchor in t:
        pos=t.index(anchor)
        extra="test('V27 executive precision removes Matrix-style spectacle',async({page})=>{await page.setViewportSize({width:1440,height:900});await page.goto(`${BASE}/index.html`,{waitUntil:'domcontentloaded'});await expect(page.locator('link[href=\"assets/v27-executive.css\"]')).toHaveCount(1);await expect(page.locator('.tech-marquee,.v20-prism-playground,.v20-color-rail,.v21-constellation')).toHaveCount(0);await expect(page.locator('.hero-aurora,.live-pill')).toHaveCount(0);await expect(page.locator('.buyer-routes .z-card')).toHaveCount(4);const text=await page.locator('.buyer-routes').innerText();for(const phrase of ['Co-creation','Collaboration','Co-opting'])expect(text).toContain(phrase);const head=await page.locator('.site-head').evaluate(e=>getComputedStyle(e).backgroundColor);expect(head).toBe('rgba(255, 255, 255, 0.98)')});\n"
        t=t[:pos]+extra+t[pos:]
    test.write_text(t,encoding='utf-8')

print('Applied V27 executive precision cleanup.')
