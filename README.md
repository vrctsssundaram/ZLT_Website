# Zepto Logic Website 2.0 — GitHub Pages Staging

This repository is the **trial/staging implementation** of Zepto Logic Website 2.0.

Live staging URL:

https://vrctsssundaram.github.io/ZLT_Website/

Production website:

https://zeptologic.com/

The GitHub Pages site is intentionally separate from production. Changes merged to `main` are used for dry-run review, QA and migration preparation before anything is transferred to the production website repository/hosting environment.

## Website 2.0 objective

The site is structured as a technical buying journey:

**engineering problem → relevant capability → evidence → defined deliverable → qualified technical enquiry**

rather than a passive company brochure.

## Implemented

- Conversion-led homepage with engineering-problem routing
- 13-core FPGA-validated IP catalogue: 9 floating-point + 4 interface cores
- Current front-end VLSI service scopes only
- R&D programme register with exact status labels and protected disclosure boundaries
- Evidence-led newsroom
- Company, Careers, Contact, Privacy and Terms rebuilds
- Qualified technical-enquiry form with static mail fallback
- Light/dark theme, responsive navigation, static site search and analytics hooks
- High-intent landing pages for RTL, verification, FPGA, floating-point IP, IP-quality, cryptographic hardware, research-to-hardware and India design-partner searches
- Sitemap, robots.txt, `.nojekyll` and historical-route 404 fallback
- Automated static QA and JavaScript syntax validation

## Public-claim guardrails

- 13 IP blocks; no legacy 15+ claim
- FPGA-validated; no silicon-validation claim
- No patent-pending or patent-filing-status claim
- No customer-delivery or customer-logo claim without approval
- No public numeric PPA figures until re-characterised
- No current physical-design, production-DFT, analog, packaging or OSAT capability claim
- Government/programme milestones retain their real status: proposed, selected, sanctioned, allotted, evaluation, etc.
- Proprietary architecture, equations and optimisation mechanisms remain non-public
- No third-party logo artwork without written permission

## URL policy

**Production target: clean URLs** such as `/about/`, `/services/`, `/products/`, `/research/` and `/privacy/`.

The staging source uses physical `.html` links because GitHub Pages directly serves the static files. Before migration to production, internal links must be normalised to the clean-path model and historical URLs preserved through server-side 301 redirects/rewrite rules.

## Staging limitations

These do not block the GitHub Pages trial site:

1. Enquiry submission currently uses a mail-client fallback; production requires server-side lead routing and secure upload.
2. Final role-based aliases, phone/WhatsApp/social links and approved leadership assets remain production inputs.
3. Public PPA figures remain withheld until re-characterisation.
4. GTM/GA/Clarity IDs, cookie-consent configuration and Search Console verification remain production setup items.
5. Final legal review remains required before production migration.

## Deployment policy

`main` is the GitHub Pages staging branch. Every staging release should pass the repository QA workflow before being treated as a migration candidate for the production website.
