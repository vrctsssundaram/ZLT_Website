# Zepto Logic Website 2.0 — V26 Staging & Production Candidate

This repository is the controlled staging implementation of Zepto Logic Website 2.0.

- Staging: https://vrctsssundaram.github.io/ZLT_Website/
- Production canonical origin: https://zeptologic.com/

The staging branch remains intentionally separate from production. Source pages retain `noindex,nofollow`; the release workflow creates a separate audited production artifact with indexing enabled.

## Current experience

The site combines a technical buying journey with a cinematic semiconductor design system:

**requirement → relevant capability → engineering evidence → defined technical route → qualified enquiry**

Current V26 features include:

- 64-second adaptive semiconductor cinematic hero with desktop/mobile encodes
- 13 FPGA-validated soft IP blocks
- five-stage interactive engineering theatre: Define → Architect → Implement → Verify → Prove
- capability playground and engineering constellation
- page-local technical navigation
- Ctrl/Cmd+K and `/` command palette
- Full / Calm / Still motion control
- Default / Larger text control
- Standard / High contrast control
- reduced-motion and Save-Data handling
- local performance instrumentation hooks
- responsive mobile, tablet, desktop and wide-screen layouts
- approved CEO leadership profile and structured Person metadata
- Supabase-backed technical enquiry submission with email fallback
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
2. deep integrity, SEO, disclosure and asset-budget QA
3. JavaScript syntax validation
4. Chromium multi-device functional/accessibility/conversion suite
5. Firefox and WebKit cross-browser smoke
6. live enquiry-endpoint CORS checks for staging, `zeptologic.com`, and `www.zeptologic.com`
7. deterministic production package generation
8. production-package audit
9. production-ready artifact creation

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
- copies only active website assets
- adds Apache/LiteSpeed/Hostinger-compatible clean-route rewrites
- adds conservative response-security/cache headers
- writes a release manifest

## URL policy

Production canonicals use clean routes such as:

- `/products/`
- `/services/`
- `/applications/`
- `/research/`
- `/about/`
- `/contact/`

The staging source keeps physical `.html` links because GitHub Pages directly serves static files. The generated production package includes rewrite rules so the clean canonical routes resolve to those static files on an Apache/LiteSpeed-style production host.

## Migration policy

Do not overwrite production from an unverified staging checkout. Use the audited `zeptologic-production-ready` workflow artifact or regenerate it from a release commit that has passed the complete QA workflow.

Production migration remains a separate controlled action.
