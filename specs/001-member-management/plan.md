# Implementation Plan: Member Management

**Branch**: `001-member-management` | **Date**: 2026-11-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-member-management/spec.md`

## Summary

Deliver a lightweight, universal Progressive Web App (PWA) for managing cell group members (GD - Grupo de Discípulos) of Onda Mooca church. The solution includes a classic CRUD interface for members (Name, unique Phone/WhatsApp, PT-BR Birthday, and Position), individual PIN authentication for administrative leaders, automatic audit logging of all mutations, and a dedicated "Histórico de Atividades" view. The architecture pairs a zero-cost, serverless embedded FastAPI + SQLite backend with a modern responsive frontend with Service Worker caching for seamless offline operation on Android, iOS, and PC.

## Technical Context

**Language/Version**: Python 3.14 (Backend/Services) & Modern Web Standards (HTML5, CSS3, ES2022+ JavaScript PWA)

**Primary Dependencies**:
- Backend: `fastapi (0.162.0)`, `uvicorn (0.54.0)`, `pydantic (2.14.2)`, `sqlite3` (built-in standard library)
- Testing: `pytest (9.2.0)`, `httpx (0.28.1)`
- Frontend: Web App Manifest (`manifest.json`), Service Worker (`sw.js`), Modern CSS/Tailwind utilities

**Storage**: Embedded SQLite database (`data/gd_manager.db`) with client-side local caching (`localStorage` / Cache API) for offline read resilience.

**Testing**: `pytest` for all unit, domain validation, database integration, and API contract test suites. Strictly follows TDD (Red-Green-Refactor).

**Target Platform**: Universal PWA running seamlessly across mobile (Android Chrome, iOS Safari PWA) and desktop (Windows, macOS, Linux web).

**Project Type**: Single-repository Web Application / PWA with embedded zero-maintenance backend.

**Performance Goals**:
- Roster and detail views render in `<1` second.
- Real-time search and role filtering respond in `<300` milliseconds.
- PIN unlock process executes in `<3` seconds.

**Constraints**:
- Absolute zero infrastructure cost ($0/month).
- Zero routine server administration for church volunteers.
- Strict phone uniqueness enforcement across members.
- Valid PT-BR date calendar checking (rejecting invalid dates like 31/02).

**Scale/Scope**: Single GD unit (up to 200 members, 3-5 administrative leaders).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle / Gate | Assessment | Status |
|---|---|:---:|
| **I. Test-Driven Development (NON-NEGOTIABLE)** | Strict Red-Green-Refactor workflow enforced. All domain models, phone/birthday validators, PIN auth, member CRUD, and audit trail will have automated tests in `tests/` written and failing before production code is written. | **PASS** |
| **II. Progressive Web App & Multiplatform First** | Standards-compliant PWA with `manifest.json`, Service Worker caching, and responsive design running identically on Android, iOS, and PC. Single codebase; no native wrappers. | **PASS** |
| **III. Lean Infrastructure & Cost Minimization** | Uses embedded SQLite with zero external database subscriptions ($0/month), zero continuous cloud VM expenses, and self-contained static PWA assets. | **PASS** |
| **IV. Architectural Simplicity & Maintainability** | Clean, modular separation between domain models, persistence services, API routes, and UI components. Zero framework bloat (YAGNI/KISS). | **PASS** |

## Project Structure

### Documentation (this feature)

```text
specs/001-member-management/
├── spec.md              # Feature specification & user clarifications
├── plan.md              # This implementation plan (/speckit-plan command output)
├── research.md          # Phase 0 technical decisions & architecture rationale
├── data-model.md        # Phase 1 database schema, entities, & validation rules
├── quickstart.md        # Phase 1 validation guide & end-to-end testing scenarios
├── contracts/           # Phase 1 API specifications
│   └── api-contracts.md # Endpoints, request/response formats, and error codes
├── checklists/
│   └── requirements.md  # Spec quality validation checklist
└── tasks.md             # Phase 2 task decomposition (/speckit-tasks command)
```

### Source Code (repository root)

```text
src/
├── domain/
│   ├── __init__.py
│   ├── models.py        # Pydantic domain models: User, Member, AuditLog
│   └── validators.py    # PT-BR phone, PT-BR birthday, and position validators
├── services/
│   ├── __init__.py
│   ├── database.py      # SQLite connection & schema migration manager
│   ├── seed.py          # Initial Onda Mooca leaders & default PIN loader
│   ├── auth_service.py  # PIN hashing, verification, & session tokens
│   ├── member_service.py# Member CRUD, uniqueness checks, & business logic
│   └── audit_service.py # Immutable activity log recorder
├── api/
│   ├── __init__.py
│   ├── routes_auth.py   # POST /api/auth/pin
│   ├── routes_members.py# GET, POST, PUT, DELETE /api/members
│   └── routes_history.py# GET /api/history
├── static/
│   ├── index.html       # Single-page PWA shell
│   ├── manifest.json    # PWA installability manifest
│   ├── sw.js            # Service worker for asset caching & offline fallback
│   ├── css/
│   │   └── app.css      # Responsive layout, badges, modals, & utility styling
│   └── js/
│       ├── app.js       # App initialization, routing & state controller
│       ├── api.js       # HTTP client with auth token headers & offline caching
│       ├── auth.js      # PIN lock screen UI & session management
│       ├── members.js   # Member list, search, position filter, & modals
│       └── history.js   # Dedicated "Histórico de Atividades" view
└── main.py              # FastAPI application entry point serving API & static PWA

tests/
├── conftest.py          # Pytest fixtures: in-memory SQLite DB & AsyncClient
├── unit/
│   ├── test_validators.py  # TDD tests for PT-BR phone and birthday logic
│   └── test_auth.py        # TDD tests for PIN hashing and token verification
├── integration/
│   ├── test_seed.py        # TDD tests for initial leader provisioning
│   ├── test_member_crud.py # TDD tests for member CRUD & uniqueness
│   └── test_audit_logs.py  # TDD tests for activity history recording
└── api/
    └── test_api_routes.py  # TDD tests for HTTP API contracts
```

**Structure Decision**: Clean web application structure combining a domain/service-oriented backend with an embedded static PWA frontend. Every component is directly testable with `pytest` and runs with zero external hosting dependencies.

## Complexity Tracking

> *No constitutional violations. All architecture decisions strictly uphold TDD, PWA, Low-Cost, and Simplicity mandates.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| *None* | *N/A* | *N/A* |
