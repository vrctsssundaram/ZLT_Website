#!/usr/bin/env python3
"""Generate the static Zepto Logic website with shared layouts and navigation."""

from html import escape
import json
import re
from pathlib import Path

from site_content import APPLICATIONS, DETAILS, ENQUIRY_TYPES, MODELS, SERVICES

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://zeptologic.com"
COMPANY = "Zepto Logic Technologies Private Limited"
EMAIL = "info@zeptologic.com"
RELEASE = "20261124"
LEGACY_SOLUTIONS = {"applications", "research"}
STAGING_PREFIX = "/ZLT_Website/"
UTILITY = {"404", "enquiry-received", "privacy", "terms"}
ICONS = {
    "arrow": '<path d="M4.5 12h14m-6-6 6 6-6 6"/>',
    "down": '<path d="M12 4.5v14m-6-6 6 6 6-6"/>',
    "chevron": '<path d="m7 10 5 5 5-5"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3m6-3v3M9 18v3m6-3v3M3 9h3m-3 6h3m12-6h3m-3 6h3"/><rect x="9.5" y="9.5" width="5" height="5" rx=".6"/>',
    "check": '<path d="M8 5h12v14H4V9m4 3 2.5 2.5L16 9M4 5h.01"/>',
    "board": '<rect x="3" y="5" width="18" height="14" rx="2"/><rect x="7" y="9" width="6" height="6" rx="1"/><path d="M17 9h1m-1 3h1m-1 3h1"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m16.5 7.5-2.7 6.3-6.3 2.7 2.7-6.3 6.3-2.7Z"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Zm-9 9 9 5 9-5m-18 4 9 5 9-5"/>',
    "orbit": '<circle cx="12" cy="12" r="2"/><ellipse cx="12" cy="12" rx="10" ry="5" transform="rotate(-38 12 12)"/>',
    "signal": '<path d="M3 12h4l2.5-6 4 12 2.5-6h5"/>',
    "shield": '<path d="M12 3 4 6v5c0 4.6 3.1 7.7 8 10 4.9-2.3 8-5.4 8-10V6l-8-3Zm-3 9 2 2 4-4"/>',
    "network": '<circle cx="5" cy="12" r="2"/><circle cx="18" cy="5" r="2"/><circle cx="18" cy="19" r="2"/><path d="m7 11 9-5m-9 7 9 5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "phone": '<path d="M5 3h4l2 5-3 2c1.2 2.5 3.5 4.8 6 6l2-3 5 2v4a2 2 0 0 1-2 2C10.2 21 3 13.8 3 5a2 2 0 0 1 2-2Z"/>',
    "pin": '<path d="M19 10c0 4.5-7 10-7 10S5 14.5 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2"/>',
}
SERVICE_LINKS = [(slug, title) for slug, title, _, _ in SERVICES]
COMPANY_LINKS = [
    ("about", "About Zepto Logic"),
    ("ecosystem", "Partnerships"),
    ("news", "Engineering guides"),
]
GROUPS = {
    "services": {"services", "engagement-models", *DETAILS}
    - {"research-to-hardware", "cryptographic-hardware-acceleration", "semiconductor-design-partner-india"},
    "research": {"research", "research-to-hardware", "cryptographic-hardware-acceleration", "cdot-samarth-zksnark"},
    "about": {"about", "ecosystem", "news", "semiconductor-design-partner-india"},
}
PAGES = []


def icon(name, css=""):
    return (
        f'<svg class="icon {css}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false">{ICONS[name]}</svg>'
    )


def link(label, url, css="button", arrow="arrow"):
    return f'<a class="{css}" href="{escape(url)}">{escape(label)}{icon(arrow)}</a>'


def brand():
    return """<a class="brand" href="index.html" aria-label="Zepto Logic home">
        <img src="assets/brand/zepto-mark.webp" width="40" height="40" alt="">
        <span>Zepto Logic <small>TECHNOLOGIES</small></span>
    </a>"""


def navigation(current):
    def nav_link(slug, name, active=False):
        state = ' aria-current="page"' if current == slug else ""
        active_class = ' class="nav-active"' if active else ""
        return f'<a href="{slug}.html"{state}{active_class}>{escape(name)}</a>'

    def group(slug, name, items):
        group_link = nav_link(slug, name, current in GROUPS[slug])
        menu = "".join(nav_link(path, title) for path, title in items)
        return f"""<div class="nav-group">
            <div class="nav-line">{group_link}
                <button class="nav-disclosure" type="button" aria-label="More {name.lower()} pages"
                    aria-controls="{slug}-menu" aria-expanded="false" hidden>{icon("chevron")}</button>
            </div>
            <div id="{slug}-menu" class="nav-dropdown" hidden>{menu}</div>
        </div>"""

    return f"""<header class="site-header">
        <div class="header-inner">
            {brand()}
            <nav id="primary-nav" aria-label="Primary navigation">
                {group("services", "Services", [*SERVICE_LINKS, ("engagement-models", "Ways to work with us")])}
                {nav_link("solutions", "Solutions", current in GROUPS["research"])}
                {group("about", "Company", COMPANY_LINKS[1:])}
                {nav_link("careers", "Careers")}
            </nav>
            <a class="button header-contact" href="contact.html"{' aria-current="page"' if current == "contact" else ""}>Contact{icon("arrow")}</a>
            <button class="menu-toggle" type="button" aria-label="Open navigation"
                aria-controls="primary-nav" aria-expanded="false" hidden><span></span><span></span></button>
        </div>
    </header>"""


def footer():
    return f"""<footer class="site-footer">
        <div class="wrap footer-grid">
            <div class="footer-brand">
                {brand()}
                <p>Semiconductor design, verification and FPGA engineering. Based in Coimbatore, India.</p>
                <a href="mailto:{EMAIL}">{EMAIL}</a>
            </div>
            <div><h2>Engineering</h2>
                <a href="services.html">Services</a>
                <a href="solutions.html">Solutions</a>
                <a href="engagement-models.html">Ways to work with us</a>
            </div>
            <div><h2>Company</h2>
                <a href="about.html">About us</a>
                <a href="ecosystem.html">Partnerships</a>
                <a href="news.html">Engineering guides</a>
                <a href="careers.html">Careers</a>
            </div>
            <div><h2>Office</h2>
                <address>TICEL Bio Park<br>Coimbatore, Tamil Nadu 641046<br>India</address>
                <a href="contact.html#office">Contact details</a>
            </div>
        </div>
        <div class="wrap footer-bottom">
            <p>© <span data-year>2026</span> {COMPANY}</p>
            <div><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="#top">Back to top ↑</a></div>
        </div>
    </footer>"""


def canonical(slug):
    return f"{ORIGIN}/" if slug == "index" else f"{ORIGIN}/{slug}/"


def write_page(slug, title, description, body, contact=True):
    PAGES.append(slug)
    title = f"{title} | Zepto Logic Technologies"
    url = canonical("solutions" if slug in LEGACY_SOLUTIONS else slug)
    schema = ""
    if slug == "index":
        organization = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": COMPANY,
            "url": url,
            "email": EMAIL,
            "logo": f"{ORIGIN}/assets/brand/zepto-logo.png",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Coimbatore",
                "addressRegion": "Tamil Nadu",
                "postalCode": "641046",
                "addressCountry": "IN",
            },
        }
        schema = f'<script type="application/ld+json">{json.dumps(organization)}</script>'
    closing = contact_band() if contact and slug not in UTILITY else ""
    markup = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(description)}">
    <meta name="robots" content="noindex,nofollow">
    <meta name="theme-color" content="#e5f5fb">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Zepto Logic Technologies">
    <meta property="og:title" content="{escape(title)}">
    <meta property="og:description" content="{escape(description)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{ORIGIN}/assets/brand/og-image.jpg">
    <meta property="og:image:alt" content="Zepto Logic Technologies semiconductor engineering">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="assets/brand/favicon-32.png">
    <link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png">
    <link rel="preload" href="assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="assets/site-v31.css?v={RELEASE}{"-logo" if slug == "index" else ""}">
    <script defer src="assets/site-v31.js?v={RELEASE}"></script>
    {schema}
</head>
<body id="top" class="page-{slug}">
    <a class="skip" href="#main">Skip to content</a>
    {navigation(slug)}
    <main id="main" tabindex="-1">
        {body}
        {closing}
    </main>
    {footer()}
</body>
</html>
"""
    # Pages serves this file at missing URLs of any depth.
    if slug == "404":
        markup = re.sub(
            r'(href|src)="(?!https?:|mailto:|tel:|/|#)([^"]+)"',
            lambda match: f'{match[1]}="{STAGING_PREFIX}{match[2]}"',
            markup,
        )
    markup = "\n".join(line.rstrip() for line in markup.splitlines()) + "\n"
    (ROOT / f"{slug}.html").write_text(markup, encoding="utf-8")


def hero(title, description, parent=None, label=None, actions="", aside=""):
    hierarchy = ""
    if parent:
        label_text, url = parent
        hierarchy = f'<a href="{url}">{escape(label_text)}</a><span aria-hidden="true">/</span>'
    state = escape(label or title)
    grid = " subhero-grid" if aside else ""
    return f"""<section class="subhero">
        <div class="wrap{grid}">
            <div>
                <nav class="breadcrumbs" aria-label="Breadcrumb">
                    <a href="index.html">Home</a><span aria-hidden="true">/</span>{hierarchy}
                    <span aria-current="page">{state}</span>
                </nav>
                <h1>{escape(title)}</h1>
                <p class="lead">{escape(description)}</p>
                {f'<div class="actions">{actions}</div>' if actions else ""}
            </div>
            {aside}
        </div>
    </section>"""


def section(body, css="", anchor=""):
    identity = f' id="{anchor}"' if anchor else ""
    return f'<section class="section {css}"{identity}><div class="wrap">{body}</div></section>'


def heading(title, description="", action=""):
    detail = f"<p>{escape(description)}</p>" if description else ""
    return f'<div class="section-heading"><div><h2>{escape(title)}</h2>{detail}</div>{action}</div>'


def card(title, url, symbol, description):
    return f"""<a class="card" href="{escape(url)}">
        <span class="card-icons"><span class="icon-tile">{icon(symbol)}</span><span class="card-arrow">{icon("arrow")}</span></span>
        <h3>{escape(title)}</h3><p>{escape(description)}</p>
    </a>"""


def service_cards(items=SERVICES):
    return '<div class="card-grid">' + "".join(
        card(title, f"{slug}.html", symbol, description)
        for slug, title, symbol, description in items
    ) + "</div>"


def blocks(items, css="info-grid"):
    return f'<div class="{css}">' + "".join(
        f"<article><h3>{escape(title)}</h3><p>{escape(description)}</p></article>"
        for title, description in items
    ) + "</div>"


def check_list(items):
    return '<ul class="check-list">' + "".join(
        f'<li>{escape(item)}</li>' for item in items
    ) + "</ul>"


def contact_band():
    return f"""<section class="contact-band">
        <div class="wrap contact-band-inner">
            <div><h2>Tell us about your project.</h2>
                <p>Share what you’re building, your current stage and where you need support.</p></div>
            {link("Discuss a project", "contact.html", "button")}
        </div>
    </section>"""


def models_grid():
    return '<div class="models-grid">' + "".join(
        f"""<a href="engagement-models.html#{key}">
            <span><strong>{escape(title)}</strong><span>{escape(description)}</span></span>{icon("arrow")}
        </a>"""
        for key, title, description, _ in MODELS
    ) + "</div>"


def write_home():
    shortcuts = [
        ("Design & verification", "services.html", "chip"),
        ("FPGA prototypes", "fpga-prototyping-services.html", "board"),
        ("Engineering reviews", "consultancy.html", "compass"),
        ("Research partnerships", "solutions.html#research", "orbit"),
    ]
    quick_links = "".join(
        f'<a href="{url}">{icon(symbol)}<span>{escape(title)}</span>{icon("arrow", "quick-arrow")}</a>'
        for title, url, symbol in shortcuts
    )
    body = f"""<section class="home-hero">
        <div class="wrap">
            <div class="hero-layout">
                <div class="hero-copy">
                    <p class="eyebrow"><span></span> Semiconductor engineering · Coimbatore, India</p>
                    <h1>Chip design,<br>from concept<br><em>to prototype.</em></h1>
                    <p class="lead">We help teams worldwide design digital chips, verify their behaviour and test them on reprogrammable FPGA hardware.</p>
                    <div class="actions">
                        {link("Discuss a project", "contact.html")}
                        {link("Explore services", "#section-2", "button button-outline", "down")}
                    </div>
                </div>
                <figure class="hero-image">
                    <picture>
                        <source media="(max-width: 600px)" srcset="assets/brand/zepto-hero-small.webp">
                        <img src="assets/brand/zepto-hero.webp" width="1000" height="1000"
                            alt="Zepto Logic logo" fetchpriority="high">
                    </picture>
                </figure>
            </div>
            <nav class="quick-paths" aria-label="Explore our work">
                {quick_links}
            </nav>
        </div>
    </section>"""
    body += section(
        '<span id="section-2" class="anchor-alias"></span>'
        + heading(
            "Engineering services",
            "Bring us a specification, a design that needs testing or a block you need running on hardware.",
            link("View all services", "services.html", "text-link"),
        )
        + service_cards(SERVICES[:3]),
        anchor="introduction",
    )
    selected = ("compute", "security", "edge-ai", "industrial", "networks", "instrumentation")
    areas = "".join(
        f'<a href="solutions.html#{slug}">{icon(symbol)}<span>{escape(title)}</span>{icon("arrow")}</a>'
        for slug, title, symbol, _, _ in APPLICATIONS if slug in selected
    )
    body += section(f"""<div class="split">
        <div>
            <h2>Where we can help</h2>
            <p class="section-lead">Find examples of the hardware design, testing and integration work you can discuss with our team.</p>
            {link("Explore solutions", "solutions.html", "button button-outline")}
        </div>
        <div class="application-links">{areas}</div>
    </div>""", "section-ink", "section-3")
    body += section(
        heading(
            "Ways to work with us",
            "Start with the kind of support your team needs. We’ll agree the scope, deliverables and review points before work starts.",
        ) + models_grid(),
        "section-soft", "section-4",
    )
    write_page(
        "index", "Semiconductor design, verification & FPGA services",
        "Zepto Logic Technologies helps global teams with digital chip design, design verification, FPGA prototyping, IP integration and applied research from Coimbatore, India.",
        body,
    )


def choice_explorer(key, label, choices):
    buttons = "".join(
        f'<button type="button" aria-pressed="false" aria-controls="{key}-{i}">'
        f'{icon(symbol)}<span>{escape(name)}</span></button>'
        for i, (name, symbol, *_rest) in enumerate(choices)
    )
    panels = "".join(
        f'<article id="{key}-{i}" class="choice-result"><h3>{escape(title)}</h3>'
        f'<p>{escape(description)}</p>{link(action, url, "text-link")}</article>'
        for i, (_name, _symbol, title, description, action, url) in enumerate(choices)
    )
    return (f'<div class="choice-explorer {key}" data-choice-explorer>'
            f'<div class="choice-controls" role="group" aria-label="{escape(label)}" hidden>{buttons}</div>'
            f'<div class="choice-results" aria-live="polite">{panels}</div></div>')


def write_services():
    body = hero(
        "Semiconductor engineering services",
        "Get help defining a digital chip, building and testing its logic, or bringing a design up on FPGA hardware.",
        label="Services",
        actions=link("Discuss a project", "contact.html")
        + link("See engineering services", "#engineering-services", "button button-outline", "down"),
    )
    body += section(
        heading("Find support for your project stage")
        + choice_explorer("project-stages", "Project stage", (
            ("Planning", "compass", "Assess feasibility", "Compare design options and identify constraints before committing to a build.", "Explore consultancy", "consultancy.html"),
            ("Designing", "chip", "Define and build digital logic", "Bring your requirements or interfaces and discuss architecture, RTL and integration.", "Explore chip design", "rtl-design-services.html"),
            ("Verifying", "check", "Check design behaviour", "Discuss a verification plan, simulation, debugging or coverage reviews.", "Explore verification", "verification-coverage-closure.html"),
            ("Prototyping", "board", "Run a design on hardware", "Discuss platform selection, implementation and testing on an FPGA board.", "Explore FPGA prototyping", "fpga-prototyping-services.html"),
        )), "section-soft", "project-stages",
    )
    body += section(
        heading("Where do you need support?", "Choose the work you need done or start with a technical review.")
        + service_cards(), anchor="engineering-services",
    )
    body += section(
        heading("Specialist engineering", "Explore more specific requirements in digital arithmetic, security or distributed teams.")
        + '<div class="card-grid">'
        + card("Floating-point & digital IP", "floating-point-ip.html", "layers",
               "Discuss arithmetic blocks, data formats and hardware interfaces.")
        + card("Cryptographic hardware", "cryptographic-hardware-acceleration.html", "shield",
               "Discuss digital design, integration or prototype evaluation for security hardware.")
        + card("Work with a team in India", "semiconductor-design-partner-india.html", "network",
               "Plan handovers, tools and reviews with our Coimbatore engineering team.")
        + "</div>", "section-soft",
    )
    write_page(
        "services", "Semiconductor engineering services",
        "Digital chip architecture and RTL design, simulation and verification, FPGA prototypes, engineering consultancy and semiconductor IP integration.",
        body,
    )


def write_details():
    for slug, (title, description, scope, share) in DETAILS.items():
        if slug in GROUPS["research"]:
            parent = ("Solutions", "solutions.html#research")
        elif slug in GROUPS["about"]:
            parent = ("Company", "about.html")
        else:
            parent = ("Services", "services.html")
        enquiry = f"contact.html?service={slug}"
        body = hero(title, description, parent, actions=link("Ask about this service", enquiry))
        body += section(heading("What we can help with") + blocks(scope), anchor="scope")
        body += section(f"""<div class="split">
            <div><h2>What to share when you contact us</h2>
                <p class="section-lead">A short, non-confidential description is enough to start.</p></div>
            <div>{check_list(share)}{link("Start an enquiry", enquiry, "text-link")}</div>
        </div>""", "section-soft", "what-to-share")
        write_page(slug, title, description, body, contact=False)


def write_solutions():
    body = hero(
        "Semiconductor solutions",
        "Find where our hardware engineering fits your product, or work with us to take a research idea into hardware.",
        label="Solutions",
        actions=link("Explore application areas", "#application-search-section", "button", "down")
        + link("Explore research collaboration", "#research", "button button-outline", "down"),
    )
    areas = "".join(
        f'<a href="#{slug}">{escape(title)}</a>' for slug, title, _, _, _ in APPLICATIONS
    )
    body += section(f"""<div class="application-tools" id="application-search-section">
        <h2>Find your application area</h2>
        <div id="search-controls" hidden>
            <label for="application-search">Find an application area</label>
            <input type="search" id="application-search" placeholder="Try telecom, robotics or research" autocomplete="off">
            <label for="application-group">Technology focus</label>
            <select id="application-group">
                <option value="">All areas</option>
                <option value="compute">Computing &amp; security</option>
                <option value="systems">Devices &amp; infrastructure</option>
                <option value="research">Research &amp; collaboration</option>
            </select>
            <p id="application-count" role="status">{len(APPLICATIONS)} application areas</p>
        </div>
        <nav class="application-index" aria-label="Jump to an application area">{areas}</nav>
    </div>""", "section-soft section-tight")
    categories = {
        "compute": {"compute", "security", "edge-ai", "financial", "processors"},
        "systems": {"industrial", "autonomous", "space", "networks", "instrumentation"},
        "research": {"quantum", "engineering", "institutions"},
    }
    focus = {slug: group for group, slugs in categories.items() for slug in slugs}
    listing = "".join(
        f"""<article class="application-row" id="{slug}" data-focus="{focus[slug]}" data-application="{escape(f'{title} {example} {search_terms}')}">
            <span class="icon-tile">{icon(symbol)}</span>
            <div><h2>{escape(title)}</h2><p>{escape(example)}</p></div>
            {link("Discuss this area", f"contact.html?area={slug}", "text-link")}
        </article>"""
        for slug, title, symbol, example, search_terms in APPLICATIONS
    )
    body += section(f"""<div id="application-list">{listing}</div>
        <p id="no-applications" hidden>No matching areas. Try a different term or browse the links above.</p>""",
        "section-tight")
    body += research_section()
    write_page(
        "solutions", "Semiconductor solutions & applied research",
        "Explore semiconductor applications, feasibility studies, FPGA prototypes and applied research collaboration.",
        body,
    )


def write_legacy_solutions():
    for slug, title, target in (
        ("applications", "Application areas", "application-search-section"),
        ("research", "Applied research", "research"),
    ):
        path = f"solutions.html#{target}"
        body = hero(
            title, "Explore this topic on the Solutions page.",
            actions=link("Go to Solutions", path),
        )
        body += f'<span data-solutions-redirect="{target}" hidden></span>'
        if slug == "applications":
            links = "".join(f'<a href="solutions.html#{area}">{escape(label)}</a>'
                            for area, label, *_ in APPLICATIONS)
            body += section(f'<nav class="application-index" aria-label="Application areas">{links}</nav>')
        write_page(slug, title, "Continue to Zepto Logic’s Solutions page.", body, contact=False)



def write_engagement():
    body = hero(
        "Ways to work with us",
        "Choose a focused review, a specific deliverable, joint development or ongoing engineering support.",
        label="Working with Zepto",
        actions=link("Request an introductory call", "contact.html?type=meeting"),
    )
    body += section('<div class="engagement-grid">' + "".join(
        f"""<article class="engagement-card" id="{key}">
            <h2>{escape(title)}</h2><p>{escape(description)}</p><p>{escape(start)}</p>
            {link("Discuss this approach", f"contact.html?model={key}", "text-link")}
        </article>"""
        for key, title, description, start in MODELS
    ) + "</div>")
    body += section(
        heading("What we agree before work starts")
        + blocks((
            ("Scope & deliverables", "What we’ll build, review or test and how you’ll assess the results."),
            ("Tools & access", "The tools, environments, confidentiality arrangements and other requirements for the work."),
            ("Schedule & terms", "Milestones, review dates, responsibilities and commercial terms."),
        )), "section-soft",
    )
    write_page(
        "engagement-models", "Semiconductor engineering engagement models",
        "Work with Zepto Logic through a technical review, defined project, joint development or ongoing semiconductor engineering support.",
        body,
    )


def research_section():
    body = section(
        heading("From research question to hardware", "For technology teams, universities and research labs exploring a hardware idea.")
        + '<div class="card-grid">'
        + card("Feasibility studies", "consultancy.html", "compass",
               "Identify constraints, compare options and agree what you need to learn first.")
        + card("Hardware prototypes", "research-to-hardware.html", "board",
               "Turn a research idea into a testable implementation with a plan for evaluating it.")
        + card("Joint research projects", "engagement-models.html#collaboration", "orbit",
               "Agree research goals, responsibilities and how the teams will review results.")
        + "</div>", "research-section", "research",
    )
    body += section(f"""<div class="split">
        <div><h2>Research topics</h2>
        <p class="section-lead">We can discuss the hardware requirements and evaluation plan for your area of research.</p></div>
        <div>{check_list(("Cryptographic hardware and post-quantum security",
                          "Digital accelerators and processing on embedded devices",
                          "Control, readout and measurement electronics"))}
        {link("Discuss research collaboration", "contact.html?type=research")}</div>
    </div>""", "section-soft")
    return body


def write_company():
    facts = """<dl class="company-facts">
        <div><dt>Established</dt><dd>2018</dd></div>
        <div><dt>Engineering centre</dt><dd>Coimbatore, India</dd></div>
        <div><dt>Corporate identification number</dt><dd>U74999TZ2018PTC031390</dd></div>
    </dl>"""
    body = hero(
        "About Zepto Logic",
        f"{COMPANY} is a semiconductor engineering company based in Coimbatore, India.",
        aside=facts,
    )
    body += section(f"""<div class="split">
        <div><h2>Design and development support</h2></div>
        <div class="prose">
            <p>We work with product companies, engineering teams and research groups on digital chip design, verification, FPGA prototypes and applied research.</p>
            <p>We’re a fabless design company. Our work focuses on the design and validation of chips and digital hardware.</p>
            {link("See our services", "services.html", "text-link")}
        </div>
    </div>""")
    body += section(
        heading("How we work with your team")
        + choice_explorer("working-principles", "Working principles", (
            ("Clarity", "compass", "Agree what success looks like", "Define the scope, interfaces, ownership and review criteria with your team.", "See ways to work with us", "engagement-models.html"),
            ("Evidence", "check", "Make results reviewable", "Agree which simulation results, measurements or prototype tests will inform the next decision.", "See verification services", "verification-coverage-closure.html"),
            ("Collaboration", "network", "Plan the handover together", "Agree how teams share progress, resolve open questions and hand over design or test material.", "Explore partnerships", "ecosystem.html"),
            ("Confidentiality", "shield", "Set the terms for sharing", "Start with a short project description and agree confidentiality arrangements before exchanging details.", "Discuss a project", "contact.html"),
        )), "section-soft", "how-we-work",
    )
    body += section("""<div class="leadership">
        <img src="assets/people/suresh-kuppuswamy.jpg" width="480" height="560" loading="lazy" alt="Suresh Kuppuswamy">
        <div>
            <p class="eyebrow">Leadership</p>
            <h2>Suresh Kuppuswamy</h2>
            <p class="role">Co-Founder, Managing Director &amp; Chief Executive Officer</p>
            <p>Suresh’s leadership experience spans technology services, financial infrastructure, enterprise transformation and corporate strategy.</p>
            <p>His career includes responsibilities across India, Europe and the Middle East, with organisations including Tata Consultancy Services, IBM, CAMS/SSPL, Adrenalin eSystems and the Sakthi Group.</p>
            <p>He is a Harvard Business School Advanced Management Program alumnus and holds a B.E. in Computer Science &amp; Engineering from Coimbatore Institute of Technology.</p>
        </div>
    </div>""", "section-soft", "leadership")
    write_page(
        "about", "About Zepto Logic",
        "Meet Zepto Logic Technologies Private Limited, a fabless semiconductor engineering and applied research company in Coimbatore, India.",
        body,
    )

    partnerships = hero(
        "Engineering & research partnerships",
        "Work with our team on a shared engineering task, a research project or a prototype.",
        ("Company", "about.html"), label="Partnerships",
        actions=link("Discuss a partnership", "contact.html?type=partnership"),
    ) + section(
        heading("Who we work with")
        + blocks((
            ("Product teams", "Add support for a particular design, verification task or prototype."),
            ("Design houses & integrators", "Scope a defined engineering task or work alongside your technical team."),
            ("Universities & research labs", "Plan a feasibility study, test an idea in hardware or explore how to develop a prototype together."),
        )),
    )
    write_page("ecosystem", "Engineering & research partnerships",
               "Explore chip design, shared development and research collaborations with Zepto Logic Technologies.", partnerships)

    guides = hero(
        "Engineering guides",
        "Practical questions to ask when you need outside support for a hardware project.",
        ("Company", "about.html"),
    ) + section(
        heading("Start with your project")
        + '<div class="card-grid">'
        + card("Write a project brief", "contact.html#what-to-include", "check",
               "Summarise the goal, the current stage and the support you need.")
        + card("Choose how to work together", "engagement-models.html", "network",
               "Compare a technical review, a defined project, joint development and ongoing support.")
        + card("Plan a hardware trial", "research-to-hardware.html", "board",
               "Define what the prototype should demonstrate and how you will evaluate it.")
        + "</div>",
    )
    write_page("news", "Engineering guides",
               "Guidance on scoping semiconductor engineering work, choosing a working model and planning hardware trials.", guides)


def write_careers():
    apply = f"mailto:{EMAIL}?subject=Career%20enquiry%20-%20Zepto%20Logic"
    body = hero(
        "Careers & internships",
        "Introduce yourself if you’re interested in digital chip design, verification, FPGA engineering or applied research.",
        label="Careers", actions=link("Email your profile", apply),
    )
    body += section(
        heading("Areas of work")
        + blocks((
            ("Design & architecture", "Read specifications, design digital logic and document how blocks and interfaces work."),
            ("Verification & FPGA", "Check designs in simulation, debug failures and evaluate designs on FPGA boards."),
            ("Applied research", "Investigate hardware ideas through reading, implementation, testing and documentation."),
        )),
    )
    body += section(f"""<div class="split">
        <div><h2>Introduce yourself</h2><p class="section-lead">We review profiles as project and hiring needs arise.</p></div>
        <div>{check_list(("Send your résumé and the role or internship you’re interested in.",
                          "Include relevant projects, code samples or a portfolio if available.",
                          "For internships, share your course, expected graduation date and availability."))}
        {link("Email your profile", apply, "text-link")}</div>
    </div>""", "section-soft")
    write_page(
        "careers", "Careers & internships",
        "Contact Zepto Logic Technologies about digital design, design verification, FPGA engineering, applied research and internships.",
        body, contact=False,
    )


def write_contact():
    options = "".join(
        f'<option value="{escape(value)}">{escape(label)}</option>' for value, label in ENQUIRY_TYPES
    )
    types = {
        "meeting": "Schedule a meeting",
        "research": "Research collaboration",
        "partnership": "Supplier / partnership discussion",
    }
    contextual = {
        "area": {row[0]: row[1] for row in APPLICATIONS},
        "model": {row[0]: row[1] for row in MODELS},
        "service": {**{slug: details[0] for slug, details in DETAILS.items()}, **dict(SERVICE_LINKS)},
        "types": types,
    }
    context_json = json.dumps(contextual).replace("<", "\\u003c")
    body = hero(
        "Contact Zepto Logic",
        "Tell us what you’re building or ask for an introductory call. Start with a short, non-confidential description.",
        label="Contact",
    )
    body += section(f"""<div class="contact-layout">
        <div>
            <div class="contact-details" id="office">
                <h2>Contact details</h2>
                <div class="contact-item"><span class="icon-tile">{icon("mail")}</span>
                    <div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
                <div class="contact-item"><span class="icon-tile">{icon("phone")}</span>
                    <div><strong>Phone</strong><a href="tel:+919626632233">+91 96266 32233</a></div></div>
                <div class="contact-item"><span class="icon-tile">{icon("pin")}</span>
                    <div><strong>Engineering office</strong><address>TICEL Bio Park Ltd, M:503, 5th Floor<br>
                    Maruthamalai Road, Somayampalayam<br>Coimbatore, Tamil Nadu 641046, India</address></div></div>
            </div>
            <div class="contact-brief" id="what-to-include">
                <h2>What to include</h2>
                {check_list(("What you want to build or test", "How far the project has progressed", "Where your team needs help"))}
                <p>For jobs and internships, visit our <a href="careers.html">Careers page</a>.</p>
            </div>
        </div>
        <div class="enquiry-panel">
            <h2>Send a project enquiry</h2>
            <form id="technicalEnquiry" method="post" hidden>
                <p id="enquiry-context" class="form-context" hidden></p>
                <p class="field-note">Fields marked * are required.</p>
                <fieldset class="form-grid" id="enquiry-fields" aria-label="Project enquiry details">
                    <div class="field">
                        <label for="name">Name *</label>
                        <input id="name" name="name" autocomplete="name" maxlength="120" required>
                    </div>
                    <div class="field">
                        <label for="email">Work email *</label>
                        <input type="email" id="email" name="email" autocomplete="email" maxlength="254" required>
                    </div>
                    <div class="field">
                        <label for="company">Company or institution *</label>
                        <input id="company" name="company" autocomplete="organization" maxlength="180" required>
                    </div>
                    <div class="field">
                        <label for="country">Country</label>
                        <input id="country" name="country" autocomplete="country-name" maxlength="100">
                    </div>
                    <div class="field full">
                        <label for="projectType">What would you like to discuss? *</label>
                        <select id="projectType" name="projectType" required>{options}</select>
                    </div>
                    <div class="field full">
                        <label for="description">A brief project description *</label>
                        <textarea id="description" name="description" rows="5" minlength="40" maxlength="6000"
                            aria-describedby="description-help" required></textarea>
                        <p class="field-note" id="description-help">At least 40 characters. Keep your first message non-confidential.</p>
                    </div>
                    <div class="hp-field" aria-hidden="true">
                        <label for="website">Website</label>
                        <input id="website" name="website" tabindex="-1" autocomplete="off">
                    </div>
                    <label class="check full"><input type="checkbox" name="nda">
                        <span>I’d like to discuss a confidentiality agreement before sharing details.</span></label>
                    <label class="check full"><input type="checkbox" name="consent" required>
                        <span>I agree that Zepto Logic may use my information to respond to this enquiry. See the <a href="privacy.html">Privacy Notice</a>. *</span></label>
                </fieldset>
                <button class="button button-primary-dark" type="submit"><span>Send enquiry</span>{icon("arrow")}</button>
                <p id="form-status" role="status" aria-live="polite"></p>
                <div id="email-fallback" hidden>
                    {link("Open your email app", f"mailto:{EMAIL}", css="text-link").replace('<a ', '<a id="fallback-link" ', 1)}
                </div>
            </form>
            <p id="form-unavailable">You can send your project enquiry to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
            <script id="contact-contexts" type="application/json">{context_json}</script>
        </div>
    </div>""", "section-contact")
    faqs = (
        ("Can you work with a team based outside India?",
         "Yes. Tell us your location, time zone and project needs so we can discuss working hours, communication and reviews."),
        ("Can I ask for a call before sharing requirements?",
         "Yes. Select “Request an introductory call” and suggest a few times and your time zone. We’ll reply to agree a time."),
        ("Can we arrange an NDA?",
         "Select the confidentiality option when you enquire. You can share detailed material once both teams have agreed the appropriate arrangements."),
    )
    body += section(
        heading("Frequently asked questions")
        + '<div class="faq-list">'
        + "".join(f'<details><summary>{escape(q)}{icon("chevron")}</summary><p>{escape(a)}</p></details>' for q, a in faqs)
        + "</div>", "section-soft",
    )
    write_page(
        "contact", "Contact Zepto Logic",
        "Contact Zepto Logic Technologies in Coimbatore, India, to discuss a semiconductor design project, verification, FPGA prototypes or research.",
        body, contact=False,
    )


def write_other_pages():
    body = hero(
        "Research programme enquiries",
        "For information about a specific research or institutional project, contact our team with the programme name and your question.",
        ("Solutions", "solutions.html#research"), label="Programme enquiries",
        actions=link("Contact research team", "contact.html?type=research") + link("Explore applied research", "solutions.html#research", "button button-outline"),
    )
    write_page("cdot-samarth-zksnark", "Research programme enquiries",
               "Ask Zepto Logic Technologies about a research or institutional programme.", body, contact=False)
    body = hero(
        "Enquiry status",
        "The contact form shows a confirmation when your enquiry is received. If you need to try again or reach us by email, return to Contact.",
        actions=link("Return to contact", "contact.html"),
    )
    write_page("enquiry-received", "Enquiry status", "Find contact information and enquiry status help.", body)
    body = hero(
        "Page not found",
        "The link may have changed. Go to the homepage or browse our engineering services.",
        label="404",
        actions=link("Back to home", "index.html") + link("Browse services", "services.html", "button button-outline"),
    )
    write_page("404", "Page not found", "Find services and contact information for Zepto Logic Technologies.", body)
    privacy = (
        ("Information you provide", "The enquiry form asks for your name, email, organisation and message. Country and confidentiality preference are optional. Keep your first enquiry free of confidential designs, sensitive personal information and protected implementation details."),
        ("How we use information", f"{COMPANY} uses the information you provide to respond to your enquiry and discuss a potential engagement."),
        ("Hosting and delivery", "The website sends enquiries through a Supabase-hosted service. Our hosting and enquiry providers may process technical information to serve the website and handle requests. The site offers an email option when form delivery cannot be confirmed."),
        ("Cookies and caching", "This website does not set advertising or analytics cookies. Submitting an enquiry does not subscribe you to a marketing list. Your browser may cache site assets. Third-party websites linked from this site have their own practices."),
        ("Your choices", f"To ask about information you provided, or to request a correction or deletion, email {EMAIL}. Contact us to ask about retention or other applicable obligations."),
    )
    terms = (
        ("Website information", "This website describes areas for engineering services, consultancy and research. Specific work, availability and terms are agreed for each engagement."),
        ("Engagements", "Scope, standards, resources, tools, infrastructure, eligibility and pricing are reviewed for each proposed engagement. Work proceeds under separately agreed terms."),
        ("Application areas", "The examples on this site describe possible uses for our engineering services. Ask us about the requirements and criteria that apply to your project."),
        ("Confidentiality and intellectual property", "Share non-confidential information initially. Access, confidentiality, ownership, licensing and use of project information should be agreed through the engagement process."),
        ("External links and questions", f"External websites are managed by their operators. For questions about this website or a potential engagement, email {EMAIL}."),
    )
    for slug, title, entries in [("privacy", "Privacy Notice", privacy), ("terms", "Website Terms", terms)]:
        text = "".join(f"<h2>{escape(t)}</h2><p>{escape(p)}</p>" for t, p in entries)
        body = hero(title, f"Website information for {COMPANY}.")
        body += section(f'<div class="legal prose">{text}</div>')
        write_page(slug, title, f"{title} for the Zepto Logic Technologies website.", body)


def main():
    write_home()
    write_services()
    write_details()
    write_solutions()
    write_legacy_solutions()
    write_engagement()
    write_company()
    write_careers()
    write_contact()
    write_other_pages()
    urls = "\n".join(
        f"    <url><loc>{canonical(slug)}</loc></url>"
        for slug in PAGES if slug not in {"404", "enquiry-received", *LEGACY_SOLUTIONS}
    )
    (ROOT / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""", encoding="utf-8")
    (ROOT / "assets/applications.json").write_text(
        json.dumps([{"id": row[0], "title": row[1]} for row in APPLICATIONS], indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built {len(PAGES)} pages and {len(APPLICATIONS)} application areas.")


if __name__ == "__main__":
    main()
