# Zepto Logic Website 2.0 — V28 Boardroom Precision Candidate

This repository is the controlled staging implementation of Zepto Logic Website 2.0.

- Staging: https://vrctsssundaram.github.io/ZLT_Website/
- Production canonical origin: https://zeptologic.com/

Staging remains separate from production. Source pages retain `noindex,nofollow`; the release workflow builds a separate audited production artifact with indexing enabled.

## V28 design direction

V28 is the boardroom-precision reset following leadership review. The public experience is deliberately white-first, restrained and technical rather than cinematic or cyberpunk.

The visible system is based on:

- white and light-neutral enterprise surfaces
- restrained navy, blue, teal, violet, amber and coral accents
- consistent responsive typography, spacing and top alignment
- original inline semiconductor technical diagrams instead of video
- only very low-amplitude node-opacity motion; disabled under reduced-motion
- concise content hierarchy
- conventional cards, listings and engineering review paths
- a five-stage Define → Architect → Implement → Verify → Prove engineering path
- collaboration language where it reflects a real engagement model: **co-creation, collaboration, co-development, co-engineering and co-opting specialist capability**

Explicitly retired from the public experience:

- cinematic/autoplay hero and domain videos
- user-facing Motion / Full / Calm / Still controls
- user-facing Text Size / Contrast panel
- repeated phone/call UI outside the dedicated Contact page
- neon/cyberpunk full-page colour systems
- prism playground and colour rail
- constellation/signal canvas
- pointer sparks, card tilt and ripple spectacle
- orbiting/faux-3D silicon spectacle and self-drawing signal-path animation
- decorative chapter-dot navigation

## Current capability

- 13 FPGA-validated soft IP blocks
- 9 arithmetic / complex-compute blocks
- 4 digital interface blocks
- architecture, RTL, verification and FPGA engineering routes
- approved CEO leadership profile and structured Person metadata
- Ctrl/Cmd+K and `/` command palette
- simple page-local navigation
- original static/minimal-motion semiconductor SVG diagrams
- Supabase-backed technical enquiry with email fallback
- direct phone and WhatsApp shown only on `contact.html`
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

## Release verification

Every migration candidate must pass:

1. zero-dependency V28 static QA
2. deep integrity, SEO, disclosure, collaboration-language and phone-isolation QA
3. JavaScript syntax validation
4. Chromium functional/accessibility/conversion suite
5. phone portrait and landscape checks
6. tablet portrait and landscape checks
7. laptop and desktop checks
8. 25%, 50%, 75%, 100%, 125%, 150%, 175% and 200% zoom/reflow matrix across all HTML pages
9. internal page and fragment link graph validation
10. absence of retired video/motion/experience UI
11. static technical-SVG contract
12. representative screenshot artifact across devices and zoom extremes
13. Firefox and WebKit cross-browser smoke
14. live enquiry-endpoint CORS checks for staging, `zeptologic.com`, and `www.zeptologic.com`
15. deterministic production package generation
16. V28 production-package audit
17. production-ready artifact creation

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
- copies the active website assets
- adds Apache/LiteSpeed/Hostinger-compatible clean-route rewrites
- adds conservative response-security/cache headers
- writes a release manifest

## URL policy

Production canonicals use clean routes such as `/products/`, `/services/`, `/applications/`, `/research/`, `/about/` and `/contact/`.

The staging source keeps physical `.html` links because GitHub Pages directly serves static files. The generated production package includes rewrite rules so the clean canonical routes resolve to those static files on an Apache/LiteSpeed-style production host.

## Migration policy

Do not overwrite production from an unverified staging checkout. Use the audited `zeptologic-v28-production-ready` workflow artifact from the exact commit that passed the complete release workflow.

Production migration remains a separate controlled action.
