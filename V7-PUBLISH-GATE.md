# V7 publishing gate

This file is an internal release checklist for the Zepto Logic website staging branch. Do not copy unverified values from this file into public website copy.

## Blocked factual claims — evidence required before publication

- [ ] **Licensable / shipped IP core count** — resolve the conflict between the current official site (11 shipped / 15+ pipeline) and the V6 staging catalogue (13). For every core counted as shipped/licensable, retain: RTL source, testbench or verification collateral, FPGA validation evidence, current delivery status and an internal owner.
- [ ] **3,800 sq ft operating design floor** — verify against the current TICEL lease / occupancy record before restoring the figure.
- [ ] **Leadership roster** — exact names and exact current titles approved by management.
- [ ] **CEO profile** — standalone approval from Suresh Kuppuswamy before publication.
- [ ] **Engineering-team statistics** — headcount, discipline mix, average experience and education base must be supported by current HR records.
- [ ] **Landing-page technical owner** — named owner and title for each technical route; do not publish a name merely to humanise the page.
- [ ] **Response-time commitment** — publish only after the monitored inbox, ownership rota and escalation process can meet the stated SLA.
- [ ] **PPA figures** — named IP version, named FPGA/device, tool/version, constraints, configuration, resource utilisation, Fmax and latency must be reproducible.
- [ ] **Case studies** — customer/programme permission or a legally safe anonymisation review required before publication.
- [ ] **Academic / institutional quotations** — written approval from the named person/institution required.
- [ ] **WhatsApp** — confirm +91 96266 32233 is the active business WhatsApp number before production migration.
- [ ] **engineering@zeptologic.com** — verify mailbox exists and is monitored before publishing.
- [ ] **Scheduler / booking URL** — verify owner, calendar and availability before publishing.

## Facts currently safe to state

- Zepto Logic Technologies Private Limited; incorporated in 2018.
- Corporate / engineering location: TICEL Bio Park, Coimbatore, Tamil Nadu, India.
- DPIIT Startup recognition: DIPP147498. Do **not** call this “Deep Tech recognition.”
- Published business phone: +91 96266 32233.
- Published email: info@zeptologic.com.
- C-DOT Samarth Cohort-II: selected among final five from more than 100 applicants; Stage-II grant awarded; Demo Day 12 March 2026 in New Delhi.
- Government of Tamil Nadu MoU: proposed investment commitment of **₹250 crore**; do not describe it as completed investment.
- TNRPF University Research Park grant: sanctioned; fund release awaited.
- Varapatti Defence Industrial Park, Sulur: 3.22 acres allotted; development pending.

## Staging-only controls

- [ ] All staging HTML pages carry `noindex,nofollow`.
- [ ] `robots.txt` blocks crawling on staging.
- [ ] Remove staging noindex/robots block only as part of the controlled migration to `zeptologic.com`.

## Conversion infrastructure gate

The current V6 enquiry flow is a `mailto:` preparation flow, not a server-side web form.

Before describing it as a submitted web form, confirm all of the following:

- [ ] HTTPS POST endpoint
- [ ] input validation and spam / bot protection
- [ ] persistent lead record
- [ ] delivery to a monitored inbox / CRM
- [ ] thank-you route after confirmed server acceptance
- [ ] autoresponder
- [ ] conversion event
- [ ] privacy / retention handling

Until then, visitor copy must say **Prepare technical email**, not imply that the website has received the enquiry.
