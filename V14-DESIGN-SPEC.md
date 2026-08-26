# V14 — Light Global Commercial System

## Position

Zepto Logic should present as an Indian semiconductor IP and engineering company with global commercial accessibility. The website exists to convert qualified technical visitors into IP evaluations, engineering discussions, R&D collaborations and strategic business conversations while preserving factual and disclosure boundaries.

## Visual contract

- No black, charcoal, navy or other dark theme/background surfaces.
- Dark values are reserved for text and fine line work.
- Primary surfaces: white, clean neutral gray, silver and warm-neutral white.
- Accents: controlled saturated cobalt, teal and restrained metallic gold; no pastel palette.
- Manrope for primary typography and IBM Plex Mono for engineering metadata.
- Light, technical grid/line details may be used at low opacity; they must not become dark panels.
- Real programme photography is preferred over decorative stock imagery.
- One authoritative visual source: `assets/style.css`; `assets/stature.css` remains only as a compatibility file for older HTML links.

## Commercial contract

The site should repeatedly make the next business action clear without behaving like a pop-up funnel or persona router.

Priority actions:
1. Evaluate / license semiconductor IP.
2. Discuss a defined architecture, RTL, verification or FPGA requirement.
3. Explore applied R&D / research-to-hardware work.
4. Begin a strategic or institutional technical discussion.

Every major page should first provide useful technical context or proof, then present the relevant ask. The header always offers `Discuss your requirement`; mobile offers `Call` and `Send requirement`.

## Content hierarchy

1. Company mission and indigenous semiconductor identity.
2. Commercially available IP and engineering capability.
3. Public programme and institutional proof.
4. Applied R&D and capability development.
5. Strategic roadmap with explicit maturity boundaries.
6. Direct technical/commercial action.

## Capability truth boundary

- Commercial now: 13 FPGA-validated soft IP blocks; architecture/microarchitecture; RTL; UVM/coverage; lint; CDC/RDC; FPGA prototyping; IP packaging/readiness.
- Scoped: selected formal work, ASIC synthesis, low-power verification, post-silicon validation advisory.
- Capability development / R&D: STA development, DFT/ATPG/MBIST/LBIST development, specialised crypto/PQC/secure-processing hardware.
- Strategic roadmap: physical implementation expansion, analog/mixed-signal capability development, package/test/OSAT concepts, planned Sulur VLSI design campus.

Roadmap items must never be presented as current production services.

## Release testing contract

V14 is not releasable unless both static and browser QA pass.

Browser checks cover:
- compact phone, phone, large phone, tablet, laptop, desktop and wide desktop viewports;
- horizontal overflow;
- visible dark-background detection using computed CSS;
- image loading;
- mobile navigation;
- search interaction;
- IP filtering (9 arithmetic + 4 interface);
- contact query-string prefill;
- free-email and minimum-context validation;
- mocked successful enquiry submission and thank-you redirect without creating a real lead;
- 44px important touch targets on mobile;
- serious/critical WCAG 2.2 accessibility smoke tests;
- responsive screenshots uploaded as CI artifacts.

The live Supabase enquiry endpoint is checked only with an OPTIONS/CORS request in CI so testing never contaminates the real enquiry table.
