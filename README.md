# Zepto Logic Technologies website

The static site introduces digital chip design, verification, FPGA prototyping, engineering consultancy and applied research. The homepage uses an original illustration and a fixed introduction. Responsive navigation and service links guide visitors to the relevant project enquiry.

- [GitHub Pages staging site](https://vrctsssundaram.github.io/ZLT_Website/)
- [Separate production website](https://zeptologic.com/)

## Maintain the website

- Shared layouts and page generation in `scripts/build_site.py`
- Service descriptions, application areas and enquiry options in `scripts/site_content.py`
- Active styles and browser interactions in `assets/site-v31.css` and `assets/site-v31.js`
- Image and font sources in `ASSET-MANIFEST.json`

Run `npm run build` after changing the content or templates and commit the generated HTML and sitemap. Run `npm run check` before publishing. The release workflow tests all active pages at desktop and mobile widths in Chromium, Firefox and WebKit, and checks keyboard navigation, accessibility, application search and enquiry handling.

To run the browser suite locally, install dependencies with `npm ci` and `npx playwright install`. Start a static server, set `BASE_URL` to the site path served by it and run `npm test`.

## Solutions

The Solutions page combines application areas and applied research. The previous Applications and Research URLs forward to it and provide direct links when JavaScript is disabled.

## Contact form

The form uses the existing Supabase Edge Function and payload. Application, service and engagement links pass the visitor's selected topic to Contact. A confirmed success clears the form. An unconfirmed delivery keeps the visitor's details and offers an email link. Visitors browsing without JavaScript can use the email address on Contact. Browser tests intercept submission requests.

## Deployment

The default branch publishes the staging site through GitHub Pages. Staging blocks search indexing. The custom domain uses a separate deployment.

To prepare an indexable build for the production host, run `python3 scripts/prepare_production.py /tmp/zeptologic-production` and `python3 scripts/production_audit.py /tmp/zeptologic-production`. The release workflow also prepares an audited production artifact. See [PRODUCTION-MIGRATION.md](PRODUCTION-MIGRATION.md) for the host deployment steps.
