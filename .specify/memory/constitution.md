<!--
SYNC IMPACT REPORT
- Version change: 2.0.0 -> 2.1.0
- Modified principles: None (Principles I-IV preserved)
- Added sections / principles:
  - Added Principle: V. Design System & Brand Identity Compliance (NON-NEGOTIABLE) enforcing `igreja_onda_ui_brand_guidelines.md` across all UI and frontend work
  - Updated Platform Constraints: Added UI & Styling Framework guidelines enforcing the official design tokens and Tailwind setup
  - Updated Quality Gates: Added UI & Brand Compliance Check and updated Constitutional Compliance Review
  - Updated Governance: Added brand/UI guideline compliance to merge enforcement
- Removed sections / principles: None
- Follow-up TODOs: None
-->

# GD Manager Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)
Test-Driven Development (TDD) is mandatory across all domain logic, services, data operations,
and critical UI interactions. Developers MUST strictly follow the Red-Green-Refactor cycle:
- **Red**: Tests MUST be written before writing implementation code and MUST fail initially.
- **Green**: Write only the minimal production code necessary to make the tests pass.
- **Refactor**: Clean up and optimize the implementation while keeping all tests passing.
No feature, bug fix, or refactor may be merged without automated tests validating its behavior.
Test suites MUST execute quickly, deterministically, and without dependency on unmocked
external networks.
*Rationale*: TDD guarantees software correctness, prevents regressions, guides clean decoupled
design, and provides living documentation of domain requirements.

### II. Progressive Web App (PWA) & Multiplatform First
The GD Manager application MUST be built as a responsive Progressive Web App (PWA) delivering a
first-class user experience across Android, iOS, and PC (Desktop web).
- The solution MUST maintain a single, responsive codebase; native wrappers or separate platform
  codebases are PROHIBITED without explicit constitutional amendment.
- The PWA MUST meet standard installability criteria (valid Web App Manifest, Service Worker
  caching, and HTTPS enforcement).
- The application MUST support offline-resilient access and local data synchronization for
  critical cell group workflows (e.g., viewing member lists, recording attendance offline).
*Rationale*: A PWA enables frictionless adoption by church leaders and members without App Store
/ Play Store fees, submission delays, or multiple platform maintenance overhead.

### III. Lean Infrastructure & Cost Minimization
All architectural and operational choices MUST prioritize minimal financial and maintenance cost.
- Hosting and compute MUST prioritize free-tier, serverless, or static-first services (e.g.,
  Cloudflare Pages/Workers, Supabase/Firebase free tier, GitHub Pages, or lightweight managed BaaS)
  targeting $0/month in ongoing infrastructure expenses under standard community usage.
- High-cost, continuously running dedicated compute (e.g., enterprise Kubernetes, oversized cloud
  VMs, paid proprietary enterprise databases) is strictly PROHIBITED.
- Operational maintenance MUST require minimal human intervention: self-healing architectures,
  automated CI/CD deployments, and zero server maintenance for church volunteers.
*Rationale*: The GD Manager serves the Onda Mooca church community where financial resources and
technical volunteer time are limited; long-term sustainability demands zero-to-low overhead.

### IV. Architectural Simplicity & Maintainability
Simplicity, clarity, and readability MUST take precedence over speculative abstractions and
premature optimization (adhering strictly to YAGNI and KISS principles).
- Business logic and domain entities MUST remain decoupled from UI frameworks, persistence
  providers, and external libraries to enable painless refactoring or framework migration.
- External dependencies MUST be vetted, kept to a minimum, modern, and actively maintained.
  Avoid heavy monolithic frameworks when lightweight solutions suffice.
*Rationale*: Church volunteer developers of varying skill levels may contribute to this codebase
over time; low cognitive load and clear code organization ensure anyone can quickly understand
and maintain the project.

### V. Design System & Brand Identity Compliance (NON-NEGOTIABLE)
Every user interface (UI), frontend screen, component, and visual interaction in GD Manager MUST
strictly adhere to the design tokens, typography, visual hierarchy, and aesthetics specified in
`igreja_onda_ui_brand_guidelines.md` (Brandbook Oficial 2027).
- **Brand Identity & Logo**: Digital interfaces MUST use exclusively the horizontal wordmark
  `"igreja onda"` in lowercase SVG format with required clearance margin (x-height padding).
  Stacked logo variants are strictly PROHIBITED in digital interfaces. Recreating the logo with
  system fonts or distorting it is PROHIBITED.
- **Design Tokens & Palette**: All interface styling MUST use the official color tokens configured
  under `onda.*` (such as Onda Blue 900 through 500, offwhite, dark, mint, cream, and cyan).
  Primary actions MUST use Onda Blue 600 (`#1f2bc8`) and dynamic highlights MUST use Onda Blue
  500 (`#2537de`) or Mint (`#79caab`). Arbitrary unmapped colors outside the design system are
  PROHIBITED.
- **Typography Hierarchy**: Font choices MUST follow brand rules: Space Grotesk for body and
  general headings, Right Grotesk Compact Black / Right Grotesk Tight Dark (ALWAYS UPPERCASE)
  for impactful headers/titles, and SF Pro Display (or system fallback) for microcopy/metadata.
- **Glassmorphism & Visual Aesthetics**: Cards, modals, floating action bars, and notification
  pills MUST incorporate the official Glassmorphism visual signature (`backdrop-blur-md` to
  `backdrop-blur-xl`, translucent backgrounds between 10% and 30%, subtle translucent borders
  `border-white/15` to `20`, and rounded radii `rounded-2xl` to `rounded-3xl` or `rounded-full`).
  Dark wave gradients (`#181e5f` -> `#11187e` -> `#1f2bc8`) and concentric wave support graphics
  MUST be utilized without compromising readability or accessibility.
- **Tone & Accessibility**: Microcopy MUST remain direct, inspiring, and welcoming ("sem rodeios").
  All UI components MUST guarantee WCAG AA contrast compliance across all color combinations.
*Rationale*: A consistent, modern, and high-fidelity visual identity aligns the digital product
with the church's cultural DNA, builds community trust, and ensures an engaging experience
across all PWA client platforms.

## Platform Constraints & Infrastructure Architecture

- **Client Platforms**: Modern browsers across mobile (Android Chrome/Firefox, iOS Safari/WebKit
  PWA) and desktop (Windows, macOS, Linux browsers).
- **Offline & Connectivity**: Service Worker implementation MUST cache application assets and
  implement an offline-first or optimistic update strategy for core GD interactions (attendance,
  meeting dates).
- **Backend & Storage**: Serverless, lightweight BaaS, or client-side storage (e.g., IndexedDB /
  local persistence with lightweight cloud sync) providing simple data persistence within free-tier
  limits without unnecessary RBAC or complex authorization layers.
- **UI & Styling Framework**: Tailwind CSS configured with the official `onda` palette, typography
  families, and glassmorphic shadow/glow tokens as defined in `igreja_onda_ui_brand_guidelines.md`.
- **Resource Constraints**: Client bundle sizes MUST remain lean and performance-budgeted to ensure
  swift initial load times even over constrained mobile 3G/4G connections.

## Quality Gates & Verification Workflow

- **TDD Workflow**: Every code contribution begins with failing automated tests specifying the
  intended behavior.
- **Test Hierarchy**:
  - Unit Tests: Enforce domain rules, entity state transitions, date manipulations, and business
    calculations.
  - Integration Tests: Validate database interactions, repository contracts, API routes, and
    Service Worker caching behavior.
  - End-to-End Tests: Validate critical user journeys (attendance taking, group reporting, PWA
    installation) across mobile and desktop viewport profiles.
- **UI & Brand Compliance Check**: Every frontend PR and UI component MUST be validated against
  the checklist in `igreja_onda_ui_brand_guidelines.md` (horizontal lowercase logo, Right Grotesk
  uppercase rules, Space Grotesk body, glassmorphism visual styling, tokenized colors, and WCAG AA
  contrast).
- **Automated CI**: Every pull request MUST pass automated linting, type-checking, test suites,
  and asset verification prior to merge approval.
- **Constitutional Compliance Review**: All pull requests MUST explicitly verify adherence to
  TDD, PWA compatibility, cost constraints, and UI brand guidelines before deployment.

## Governance

- **Supremacy**: This constitution defines the non-negotiable architectural boundaries and
  engineering principles of GD Manager. It supersedes informal conventions and code-level
  preferences.
- **Amendment Procedure**: Any principle or constraint amendment MUST be submitted as a pull
  request updating `.specify/memory/constitution.md` with documented rationale, maintenance
  impact, and migration plan.
- **Versioning Policy**: Semantic versioning (SemVer) applies to this constitution:
  - MAJOR: Removal, weakening, or breaking redefinition of core principles (e.g., removing
    principles or weakening TDD/PWA mandates).
  - MINOR: Addition of new principles, architecture sections, or expanded governance rules.
  - PATCH: Clarifications, phrasing improvements, typo corrections, non-semantic refinements.
- **Compliance Enforcement**: Features or pull requests that violate these constitutional mandates
  (e.g., code committed without tests, introducing paid infrastructure, breaking PWA capabilities,
  or violating brand/UI design guidelines) MUST NOT be merged.

**Version**: 2.1.0 | **Ratified**: 2026-11-05 | **Last Amended**: 2026-11-05
