# Zepto Logic website — V31

A 24-page static company website for service, consultancy and applied research enquiries.

- GitHub Pages: https://vrctsssundaram.github.io/ZLT_Website/
- Separate production origin: https://zeptologic.com/

## Design and content

Original navy/blue/cyan visual system derived from the existing Zepto Logic logo. Original semiconductor SVG illustration. GSOC informed the visual hierarchy and page structures; iVLSI, Swindon Silicon and CSEM informed navigation and enquiry patterns. No reference-site copy, customer claims, testimonials or third-party brand assets are republished.

The homepage has three introductions rotating every five seconds. Rotation pauses on hover/focus, supports manual pause and respects reduced-motion settings. All content and navigation remain available without animation.

13 application areas reflect the outreach categories, without publishing prospect names or contact lists, implying existing customer relationships, or making sector-certification claims. Service scope, tools, infrastructure, eligibility and commercial terms are established through discussion.

## Maintain

- Page content and shared HTML: `scripts/build_site.py`
- Original illustration generator: `scripts/build_visual.py`
- Active styles: `assets/site-v31.css`
- Navigation, hero, filtering and enquiry: `assets/site-v31.js`
- Existing company logo and approved leadership portrait retained.

Run `npm run build` after changing the page generator. Run `npm run check` for static integrity. Browser tests use `npm ci` and Playwright via Website Release QA.

Earlier design scripts, styles, tests and release notes are historical; V31 pages load only the active stylesheet and runtime. Older white-only/no-motion design instructions are superseded by the requested V31 redesign. The prior disclosure, verified-claim and staging/production separation requirements remain in force.

## Enquiry handling

The form preserves the existing Supabase Edge Function endpoint and payload contract. Success is displayed only after an HTTP success with `ok: true`. Failure retains user input and presents a manual email fallback. No actual enquiry is sent by browser tests: endpoint requests are intercepted. No meeting is automatically booked; the meeting CTA preselects a meeting request on Contact.

## Release and production

CI checks all 24 pages at desktop/mobile widths in Chromium, Firefox and WebKit, core accessibility, navigation, hero controls, enquiry success/failure, and narrow layouts. It builds an audited production artifact only after checks pass.

GitHub Pages publishes this repository as its existing staging website. Staging stays `noindex,nofollow`. The separate production domain is not changed by a repository push.

Build production with `python scripts/prepare_production.py /tmp/zeptologic-production` and audit using `python scripts/production_audit.py /tmp/zeptologic-production`. The package enables indexing, retains non-indexing on 404/status pages, and supports canonical clean URLs on Apache/LiteSpeed. Production migration requires the existing host's deployment access, a backup and verification; see PRODUCTION-MIGRATION.md.
