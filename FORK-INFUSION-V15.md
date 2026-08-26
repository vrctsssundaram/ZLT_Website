# V15 Fork Pattern Infusion

Date: 26 August 2026

## Purpose

Review the ten most recently forked repositories in `vrctsssundaram` and extract only the interaction, accessibility and information-design patterns that improve the Zepto Logic staging website. V15 deliberately does **not** migrate the website to React, Svelte, Tailwind, Material Web or another framework. The deployed architecture remains static HTML + CSS + vanilla JavaScript.

## Guardrails

- Preserve the V14 light professional semiconductor visual system.
- No dark/black theme surfaces.
- No new customer logos, testimonials, client claims or unapproved commercial claims.
- No framework/runtime dependency added.
- Reimplement patterns natively rather than importing whole libraries.
- Retain current SEO, disclosure, Supabase enquiry and release-QA controls.
- Avoid direct reuse from repositories whose licence or component terms are more restrictive when conceptual reimplementation is sufficient.

## Ten-repository audit

| Recent fork | Upstream / stack | Licence observed | Useful pattern | V15 decision |
| --- | --- | --- | --- | --- |
| `CuoreUI` | CuoreUI.Winforms / C# WinForms | Unlicense; Fluent icon assets separately MIT | Clear control feedback and state visibility | Concept only. Desktop WinForms code is not appropriate for the website. |
| `core` | SVAR Svelte Core | MIT | Lightweight controls, tabs, notifications, sliding sidebar, CSS-variable theming | Reuse the lightweight/stateful-control philosophy only; no Svelte dependency. |
| `web-components` | Vaadin Web Components | Apache-2.0 for core components | Accordion/details, badge, breadcrumbs, form layout, grid, dialogs and strong business-app semantics | Native disclosure, status and form semantics adopted. No Vaadin runtime. |
| `tailgrids` | TailGrids React + Tailwind | MIT | Accordion, badge, breadcrumbs, fields, navigation, table, tabs, toast, responsive/keyboard conventions | Strong source of interaction patterns; native equivalents used. |
| `react` | Untitled UI React + React Aria | MIT for open-source repository components; PRO separately licensed | Neutral enterprise spacing, accessible controls, focus/state behavior | Accessibility and control-state principles adopted; no React migration. |
| `flowbite` | Flowbite / Tailwind + vanilla data-attribute interactions | MIT | Segmented controls, forms, navbar, timeline, modal/disclosure interaction conventions | Native component conventions, evidence continuity and form feedback adopted. |
| `react-bits` | React Bits | MIT + Commons Clause | Restrained micro-interaction ideas, reduced-motion awareness | Concept only. No animation component code copied; V15 keeps motion subtle. |
| `ant-design` | Ant Design / React | MIT | Steps, status/tag language, enterprise hierarchy and progressive disclosure | Five-stage engagement path and standardized status treatment adopted natively. |
| `material-web` | Material Web / Lit Web Components | Apache-2.0 | Accessible text-field state, form affordance and explicit focus/touch behavior | Contact field feedback, focus-visible and live status guidance adopted. |
| `business-website-template` | React + Tailwind business website | MIT | Commercial page sequencing: proposition → proof → capability → CTA | Existing V14 sequencing retained and reinforced; testimonial/client-logo patterns explicitly rejected. |

## Implemented V15 improvements

### IP portfolio

- Accessible segmented category filter with `aria-pressed` state.
- Search field integrated into the same portfolio control surface.
- Live result count (`13 of 13`, `9 of 13`, `4 of 13`) via `role=status` / `aria-live`.
- Native `<details>/<summary>` evaluation-question set covering function/format, target/interface context, decision evidence and evaluation collateral.

### Engineering services

- Existing interactive design-flow nodes converted to real buttons with pressed-state semantics.
- New five-stage semantic engagement path: frame requirement → define scope → build/verify → review evidence → hand off.
- Native disclosure set clarifying current scope, standalone workstreams, NDA sequencing and roadmap boundaries.

### R&D / evidence

- Programme milestone groups receive explicit list/listitem semantics.
- Visual evidence continuity is added without changing claims or programme status.
- Existing maturity labels are standardized as readable status chips.

### Technical enquiry

- Live minimum-context counter for the 40-character technical-description requirement.
- Ready state is communicated with text and a check mark, not color alone.
- `aria-describedby` connects the field help and counter to the textarea.
- Form errors become keyboard-focusable when surfaced.
- Submission progress/fallback messages use the existing live status region.

### Global interaction quality

- Consistent high-contrast `:focus-visible` treatment.
- Standardized status-chip styling.
- Native disclosure component styling.
- Responsive stepper and segmented controls without horizontal overflow.
- Stronger `prefers-reduced-motion` behavior.

## Deliberately not adopted

- React/Svelte/Tailwind/Lit framework migrations.
- ReactBits animated backgrounds, 3D effects or visually dominant motion.
- Material visual identity or Material-shaped components.
- Ant Design visual branding.
- Dark mode or dark surface variants.
- Testimonials, client logos, fictional logos or sponsor/logo strips.
- Carousels, popups or modals without a clear Zepto Logic conversion need.
- Any component that weakens the current static-site performance and deployment model.

## Release safety

Rollback branch before V15 work:

`backup-before-v15-fork-infusion-2026-08-26`

V15 working branch:

`v15-fork-pattern-infusion`

The V15 branch must pass the existing static disclosure/SEO checks plus the expanded Chromium responsive, accessibility, component-interaction and mocked-enquiry tests before merge.