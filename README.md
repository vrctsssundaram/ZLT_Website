# Zepto Logic Website 2.0 — V27 Executive Precision Candidate

This repository is the controlled staging implementation of Zepto Logic Website 2.0.

- Staging: https://vrctsssundaram.github.io/ZLT_Website/
- Production canonical origin: https://zeptologic.com/

The staging branch remains intentionally separate from production. Source pages retain `noindex,nofollow`; the release workflow creates a separate audited production artifact with indexing enabled.

## V27 design direction

V27 is a deliberate executive reset following leadership review. The website no longer uses the earlier cyberpunk / Matrix-like spectacle language.

The visible system is now based on:

- white and light-neutral enterprise surfaces
- restrained navy/blue technical accents
- consistent typography, spacing and alignment
- high-resolution semiconductor media used as supporting evidence rather than a full-screen atmosphere
- concise content hierarchy and fewer overlapping explanations
- purposeful interaction only
- a five-stage Define → Architect → Implement → Verify → Prove engineering path
- collaboration language used where it reflects a real engagement model: **co-creation, collaboration, co-development, co-engineering and co-opting specialist capability**

Explicitly retired from the default experience:

- neon/cyberpunk full-page colour systems
- prism playground
- animated colour rail
- constellation and signal-canvas experience
- pointer sparks, card tilt and ripple spectacle
- chapter-dot navigation
- decorative faux-3D silicon object, orbit geometry, self-drawing signal path and Bauhaus motion

## Current product and interaction capability

- 13 FPGA-validated soft IP blocks
- 9 arithmetic / complex-compute blocks
- 4 digital interface blocks
- architecture, RTL, verification and FPGA engineering routes
- approved CEO leadership profile and structured Person metadata
- Ctrl/Cmd+K and `/` command palette
- simple page-local navigation
- Full / Calm / Still motion control
- Default / Larger text control
- Standard / High contrast control
- reduced-motion and Save-Data support
- high-resolution local hero and technical domain films
- Supabase-backed technical enquiry with email fallback
- local performance instrumentation
- deterministic production-package builder and migration audit

## Public-claim guardrails

- 13 FPGA-validated soft IP blocks
- no silicon-validation claim
- no unsupported customer-deployment/customer-logo claim
- no public numeric PPA figures until approved/re-characterised
- research, grants, land, MoU and future-infrastructure statements retain explicit status language
- proprietary implementation mechanisms remain non-public
- no third-party logo artwork without written permission
- fabrication/manufacturing imagery is illustrative industry context and does not represent an owned wafer fab

## Release verification

Every migration candidate must pass:

1. zero-dependency static QA
2. V27 anti-spectacle / executive-precision static contract
3. deep integrity, SEO, disclosure and asset-budget QA
4. JavaScript syntax validation
5. Chromium multi-device functional/accessibility/conversion suite
6. explicit Matrix/cyberpunk-removal assertions
7. responsive typography, overflow and background checks
8. Firefox and WebKit cross-browser smoke
9. live enquiry-endpoint CORS checks for staging, `zeptologic.com`, and `www.zeptologic.com`
10. deterministic production package generation
11. production-package audit
12. production-ready artifact creation

The release workflow is `.github/workflows/site-qa.yml`.

## Production packaging

Run locally:

```bash
python scripts/prepare_production.py dist-production
python scripts/production_audit.py dist-production
```

The production builder does **not** mutate staging. It:

- changes public pages from staging `noindex,nofollow` to production indexing directives
- keeps `404.html` and `enquiry-received.html` non-indexable
- creates production `robots.txt`
- copies active website assets
- adds Apache/LiteSpeed/Hostinger-compatible clean-route rewrites
- adds conservative response-security/cache headers
- writes a release manifest

## URL policy

Production canonicals use clean routes such as `/products/`, `/services/`, `/applications/`, `/research/`, `/about/` and `/contact/`.

The staging source keeps physical `.html` links because GitHub Pages directly serves static files. The generated production package includes rewrite rules so the clean canonical routes resolve to those static files on an Apache/LiteSpeed-style production host.

## Migration policy

Do not overwrite production from an unverified staging checkout. Use the audited `zeptologic-production-ready` workflow artifact or regenerate it from a release commit that has passed the complete QA workflow.

Production migration remains a separate controlled action.
