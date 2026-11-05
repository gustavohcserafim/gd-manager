<!--
SYNC IMPACT REPORT
- Version change: 1.0.0 -> 2.0.0
- Modified principles: None
- Added sections: None
- Removed sections / principles:
  - Removed Principle: V. Data Privacy & Community Trust (eliminated RBAC and sensitive data constraints per revised project scope)
  - Updated Platform Constraints: Simplified backend & storage expectations to eliminate RBAC / row-level security requirements
- Follow-up TODOs: None
-->

# GD Manager Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)
Test-Driven Development (TDD) is mandatory across all domain logic, services, data operations, and critical UI interactions. Developers MUST strictly follow the Red-Green-Refactor cycle:
- **Red**: Tests MUST be written before writing implementation code and MUST fail initially.
- **Green**: Write only the minimal production code necessary to make the tests pass.
- **Refactor**: Clean up and optimize the implementation while keeping all tests passing.
No feature, bug fix, or refactor may be merged without automated tests validating its behavior. Test suites MUST execute quickly, deterministically, and without dependency on unmocked external networks.
*Rationale*: TDD guarantees software correctness, prevents regressions, guides clean decoupled design, and provides living documentation of domain requirements.

### II. Progressive Web App (PWA) & Multiplatform First
The GD Manager application MUST be built as a responsive Progressive Web App (PWA) delivering a first-class user experience across Android, iOS, and PC (Desktop web).
- The solution MUST maintain a single, responsive codebase; native wrappers or separate platform codebases are PROHIBITED without explicit constitutional amendment.
- The PWA MUST meet standard installability criteria (valid Web App Manifest, Service Worker caching, and HTTPS enforcement).
- The application MUST support offline-resilient access and local data synchronization for critical cell group workflows (e.g., viewing member lists, recording attendance offline).
*Rationale*: A PWA enables frictionless adoption by church leaders and members without App Store / Play Store fees, submission delays, or multiple platform maintenance overhead.

### III. Lean Infrastructure & Cost Minimization
All architectural and operational choices MUST prioritize minimal financial and maintenance cost.
- Hosting and compute MUST prioritize free-tier, serverless, or static-first services (e.g., Cloudflare Pages/Workers, Supabase/Firebase free tier, GitHub Pages, or lightweight managed BaaS) targeting $0/month in ongoing infrastructure expenses under standard community usage.
- High-cost, continuously running dedicated compute (e.g., enterprise Kubernetes, oversized cloud VMs, paid proprietary enterprise databases) is strictly PROHIBITED.
- Operational maintenance MUST require minimal human intervention: self-healing architectures, automated CI/CD deployments, and zero server maintenance for church volunteers.
*Rationale*: The GD Manager serves the Onda Mooca church community where financial resources and technical volunteer time are limited; long-term sustainability demands zero-to-low overhead.

### IV. Architectural Simplicity & Maintainability
Simplicity, clarity, and readability MUST take precedence over speculative abstractions and premature optimization (adhering strictly to YAGNI and KISS principles).
- Business logic and domain entities MUST remain decoupled from UI frameworks, persistence providers, and external libraries to enable painless refactoring or framework migration.
- External dependencies MUST be vetted, kept to a minimum, modern, and actively maintained. Avoid heavy monolithic frameworks when lightweight solutions suffice.
*Rationale*: Church volunteer developers of varying skill levels may contribute to this codebase over time; low cognitive load and clear code organization ensure anyone can quickly understand and maintain the project.

## Platform Constraints & Infrastructure Architecture

- **Client Platforms**: Modern browsers across mobile (Android Chrome/Firefox, iOS Safari/WebKit PWA) and desktop (Windows, macOS, Linux browsers).
- **Offline & Connectivity**: Service Worker implementation MUST cache application assets and implement an offline-first or optimistic update strategy for core GD interactions (attendance, meeting dates).
- **Backend & Storage**: Serverless, lightweight BaaS, or client-side storage (e.g., IndexedDB / local persistence with lightweight cloud sync) providing simple data persistence within free-tier limits without unnecessary RBAC or complex authorization layers.
- **Resource Constraints**: Client bundle sizes MUST remain lean and performance-budgeted to ensure swift initial load times even over constrained mobile 3G/4G connections.

## Quality Gates & Verification Workflow

- **TDD Workflow**: Every code contribution begins with failing automated tests specifying the intended behavior.
- **Test Hierarchy**:
  - Unit Tests: Enforce domain rules, entity state transitions, date manipulations, and business calculations.
  - Integration Tests: Validate database interactions, repository contracts, API routes, and Service Worker caching behavior.
  - End-to-End Tests: Validate critical user journeys (attendance taking, group reporting, PWA installation) across mobile and desktop viewport profiles.
- **Automated CI**: Every pull request MUST pass automated linting, type-checking, and test suites prior to merge approval.
- **Constitutional Compliance Review**: All pull requests MUST explicitly verify adherence to TDD, PWA compatibility, and cost constraints before deployment.

## Governance

- **Supremacy**: This constitution defines the non-negotiable architectural boundaries and engineering principles of GD Manager. It supersedes informal conventions and code-level preferences.
- **Amendment Procedure**: Any principle or constraint amendment MUST be submitted as a pull request updating `.specify/memory/constitution.md` with documented rationale, maintenance impact, and migration plan.
- **Versioning Policy**: Semantic versioning (SemVer) applies to this constitution:
  - MAJOR: Removal, weakening, or breaking redefinition of core principles (e.g., removing principles or weakening TDD/PWA mandates).
  - MINOR: Addition of new principles, architecture sections, or expanded governance rules.
  - PATCH: Clarifications, phrasing improvements, typo corrections, non-semantic refinements.
- **Compliance Enforcement**: Features or pull requests that violate these constitutional mandates (e.g., code committed without tests, introducing paid infrastructure, breaking PWA capabilities) MUST NOT be merged.

**Version**: 2.0.0 | **Ratified**: 2026-11-05 | **Last Amended**: 2026-11-05
