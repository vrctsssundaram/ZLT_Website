#!/usr/bin/env python3
"""Apply the V30 copy cleanup and retire the standalone products/IP page.

Intent:
- use the leadership-approved homepage wording
- remove the standalone products.html route and every live reference to it
- keep Semiconductor IP positioned under the services engagement route
- keep QA and release tooling aligned with the reduced navigation
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def write_if_changed(path: Path, text: str) -> None:
    old = path.read_text(encoding="utf-8")
    if text != old:
        path.write_text(text, encoding="utf-8")


def remove_products_from_list_literals(text: str) -> str:
    # Handles the compact page arrays used by the JS/QA suites without
    # disturbing unrelated IP wording.
    text = text.replace("'products.html',", "")
    text = text.replace(",'products.html'", "")
    text = text.replace('"products.html",', "")
    text = text.replace(',"products.html"', "")
    return text


# 1) Retire the standalone page itself.
products = ROOT / "products.html"
if products.exists():
    products.unlink()


# 2) Update every live HTML shell and the requested homepage copy.
for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")

    if path.name == "index.html":
        text = text.replace(
            "Semiconductor IP. Engineering services. Applied R&amp;D.",
            "Semiconductor IP services and Applied R&amp;D.",
        )
        text = text.replace("Three clear ways to engage.", "Three ways to engage.")
        text = text.replace(
            "Three core offerings. Clearly defined.",
            "Three core offerings.",
        )
        text = text.replace(
            "A simple menu of what you can engage us for.",
            "What you can engage us for.",
        )

    # Remove the dedicated IP item from primary navigation.
    text = re.sub(
        r'<a\b(?=[^>]*\bhref=["\']products\.html["\'])[^>]*>\s*IP\s*</a>',
        "",
        text,
        flags=re.I,
    )

    # Remove the dedicated IP-portfolio item from the footer.
    text = re.sub(
        r'<li>\s*<a\b(?=[^>]*\bhref=["\']products\.html["\'])[^>]*>\s*IP portfolio\s*</a>\s*</li>',
        "",
        text,
        flags=re.I,
    )

    # Any remaining contextual IP cards now resolve through Services rather
    # than to the retired standalone page.
    text = re.sub(
        r'href=(["\'])products\.html(?:[^"\']*)\1',
        r'href=\1services.html\1',
        text,
        flags=re.I,
    )
    text = text.replace("View IP portfolio →", "View semiconductor services →")
    text = text.replace(
        "https://vrctsssundaram.github.io/ZLT_Website/products.html",
        "https://vrctsssundaram.github.io/ZLT_Website/services.html",
    )

    write_if_changed(path, text)


# 3) Remove the route from the sitemap.
sitemap = ROOT / "sitemap.xml"
if sitemap.exists():
    text = sitemap.read_text(encoding="utf-8")
    text = re.sub(
        r'\s*<url><loc>https://zeptologic\.com/products/</loc>.*?</url>\s*',
        "\n  ",
        text,
        flags=re.S,
    )
    write_if_changed(sitemap, text)


# 4) Keep site search useful: IP searches now open Services. Remove the
# page-local IP explorer runtime because the page no longer exists.
site_js = ROOT / "assets/site.js"
if site_js.exists():
    text = site_js.read_text(encoding="utf-8")
    text = text.replace(
        "['Semiconductor IP','products.html','semiconductor IP floating point arithmetic UART SPI I2C license evaluate reusable portfolio']",
        "['Semiconductor IP services','services.html','semiconductor IP floating point arithmetic UART SPI I2C license evaluate reusable services']",
    )
    text = text.replace(
        "navigation, search, IP filtering, contact",
        "navigation, search, contact",
    )
    start = text.find("/* ---------------------------------------------------------------------\n   IP explorer")
    end = text.find("/* ---------------------------------------------------------------------\n   Contact route context")
    if start != -1 and end != -1 and end > start:
        text = text[:start] + text[end:]
    write_if_changed(site_js, text)


# 5) Keep the current V29 migration source from reintroducing the retired
# route if it is run again later.
v29 = ROOT / "scripts/apply_v29_clarity.py"
if v29.exists():
    text = v29.read_text(encoding="utf-8")
    text = text.replace("    ('products.html','IP'),\n", "")
    text = text.replace(
        "Semiconductor IP. Engineering services. Applied R&amp;D.",
        "Semiconductor IP services and Applied R&amp;D.",
    )
    text = text.replace("Three clear ways to engage.", "Three ways to engage.")
    text = text.replace(
        "Three core offerings. Clearly defined.",
        "Three core offerings.",
    )
    text = text.replace(
        "A simple menu of what you can engage us for.",
        "What you can engage us for.",
    )
    text = text.replace('href="products.html"', 'href="services.html"')
    text = text.replace("['Home','IP','Services','R&D','Company','Contact']", "['Home','Services','R&D','Company','Contact']")
    text = text.replace(
        "Semiconductor IP. Engineering services. Applied R&D.",
        "Semiconductor IP services and Applied R&D.",
    )
    # The products-specific branch is obsolete now that the page is retired.
    text = re.sub(
        r"\n        elif path\.name=='products\.html':\n(?:            .*\n)+?(?=        elif path\.name=='research\.html':)",
        "\n",
        text,
    )
    write_if_changed(v29, text)


# 6) Align static QA with the five-item primary navigation and retired page.
site_qa = ROOT / "scripts/site_qa.py"
if site_qa.exists():
    text = site_qa.read_text(encoding="utf-8")
    text = text.replace("'products.html',", "")
    text = text.replace(", 'products.html'", "")
    text = text.replace(
        "for href in ('index.html','products.html','services.html','research.html','about.html','contact.html'):",
        "for href in ('index.html','services.html','research.html','about.html','contact.html'):",
    )
    text = text.replace(
        "Semiconductor IP. Engineering services. Applied R&amp;D.",
        "Semiconductor IP services and Applied R&amp;D.",
    )
    text = text.replace(
        "for name in ('products.html','applications.html','research.html'):",
        "for name in ('applications.html','research.html'):",
    )
    text = text.replace("'ipExplorer',", "")
    write_if_changed(site_qa, text)


deep_qa = ROOT / "scripts/deep_qa.py"
if deep_qa.exists():
    text = deep_qa.read_text(encoding="utf-8")
    text = text.replace("'products.html',", "")
    text = text.replace(", 'products.html'", "")
    text = text.replace("'ipExplorer',", "")
    write_if_changed(deep_qa, text)


# 7) Align browser tests with the retired page.
site_spec = ROOT / "tests/site.spec.js"
if site_spec.exists():
    text = site_spec.read_text(encoding="utf-8")
    text = remove_products_from_list_literals(text)
    text = text.replace(
        "['Home','IP','Services','R&D','Company','Contact']",
        "['Home','Services','R&D','Company','Contact']",
    )
    text = text.replace(
        "Semiconductor IP. Engineering services. Applied R&D.",
        "Semiconductor IP services and Applied R&D.",
    )
    text = re.sub(
        r"\ntest\('IP explorer exposes 9 arithmetic and 4 interface blocks'.*?\n\ntest\('applications page exposes six workload anchors'",
        "\n\ntest('applications page exposes six workload anchors'",
        text,
        flags=re.S,
    )
    text = text.replace('a[href=\\"products.html\\"]', 'a[href=\\"services.html\\"]')
    text = text.replace('/products\\.html/', '/services\\.html/')
    text = text.replace("products.html", "services.html")
    write_if_changed(site_spec, text)


v28_spec = ROOT / "tests/v28-boardroom.spec.js"
if v28_spec.exists():
    text = v28_spec.read_text(encoding="utf-8")
    text = remove_products_from_list_literals(text)
    text = text.replace("['products.html','.v28-visual-ip'],", "")
    text = re.sub(
        r"\n await page\.goto\(`\$\{BASE\}/products\.html`.*?ip-explorer-count'\)\.toHaveText\('4 of 13 blocks'\);",
        "",
        text,
        flags=re.S,
    )
    text = text.replace("products.html", "services.html")
    write_if_changed(v28_spec, text)


cross_spec = ROOT / "tests/cross-browser.spec.js"
if cross_spec.exists():
    text = cross_spec.read_text(encoding="utf-8")
    text = remove_products_from_list_literals(text)
    text = text.replace("products.html", "services.html")
    write_if_changed(cross_spec, text)


# Final migration contract: the public site must not expose products.html.
assert not (ROOT / "products.html").exists(), "products.html still exists"
assert "products.html" not in (ROOT / "index.html").read_text(encoding="utf-8")
assert "products.html" not in (ROOT / "assets/site.js").read_text(encoding="utf-8")
assert "/products/" not in (ROOT / "sitemap.xml").read_text(encoding="utf-8")

home = (ROOT / "index.html").read_text(encoding="utf-8")
for required in (
    "Semiconductor IP services and Applied R&amp;D.",
    "Three ways to engage.",
    "Three core offerings.",
    "What you can engage us for.",
):
    assert required in home, f"homepage copy missing: {required}"

print("Applied V30 homepage copy cleanup and retired products.html.")
