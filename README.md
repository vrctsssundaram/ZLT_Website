# Zepto Logic Website 2.0 — Draft Review

> **DO NOT MERGE TO `main` OR DEPLOY AS PRODUCTION YET.**
>
> This branch is the isolated Website 2.0 conversion-led rebuild. The current production/GitHub Pages baseline remains on `main` until final approvals and deployment dependencies are cleared.

## Branch

`website-2.0-conversion-rebuild`

Draft review PR: https://github.com/vrctsssundaram/ZLT_Website/pull/1

## Read-only branch preview

Development renderer (third-party, read-only; it does not deploy or modify production):

https://raw.githack.com/vrctsssundaram/ZLT_Website/website-2.0-conversion-rebuild/index.html

Use the preview only for visual/navigation review. RawGitHack is not a production host and may briefly cache branch changes.

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
- Updated sitemap and historical-route 404 fallback
- Automated zero-dependency static QA on every Website 2.0 push/PR change

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

## Review matrix

### Desktop
- Header/nav alignment at 1280–1440 px
- Hero hierarchy and CTA prominence
- Table/ledger readability on Products and Services
- R&D status-label clarity
- Contact form validation and mail fallback
- Light/dark theme contrast

### Mobile
- 320, 375 and 430 px widths
- Menu open/close and tap targets
- No horizontal overflow in spec/evidence rows
- CTA stacking
- Form field sizing and keyboard-safe inputs

### Functional
- All navigation links
- Search results and intent-page routing
- Product-family filters
- Query-string form prefill
- Theme persistence
- 404 historical-route fallback
- Privacy/Terms links

### Content / disclosure
- Capability wording vs current operating reality
- Government/programme status wording
- No confidential or proprietary implementation detail
- Leadership and partner references require final approval before launch

## URL policy — resolved

**Production target: clean URLs** such as `/about/`, `/services/`, `/products/`, `/research/` and `/privacy/`.

The current public site is already indexed on this clean-path model, so Website 2.0 keeps clean canonical URLs and clean sitemap locations.

The source files retain `.html` hrefs temporarily because the read-only GitHub branch preview requires direct physical-file navigation. Before production launch:

1. verify the production host's `.html` → clean-path redirect/rewrite behaviour;
2. normalize internal navigation/search links to the clean URLs so users and crawlers do not incur unnecessary redirects; and
3. preserve server-side 301 mappings for historical/renamed routes.

This is a deployment-normalisation task, not an unresolved SEO architecture decision.

## Open launch blockers

1. Final approved leadership copy and portraits
2. Approved role-based contact aliases
3. Production server-side lead routing and secure file upload
4. Final legal review and analytics consent implementation
5. GTM/GA/Clarity production IDs and Search Console verification
6. Final approved office/lab/event/leadership images
7. Public PPA data only after re-characterisation
8. Verified production redirect/rewrite rules and final internal-link normalization

## Deployment rule

No production deployment, domain cutover, `main` merge, DNS change or GitHub Pages source change should occur from this branch until the draft PR is explicitly approved for launch.
