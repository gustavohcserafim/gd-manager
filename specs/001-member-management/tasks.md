# Tasks: Member Management (GD Manager)

**Input**: Design documents from `specs/001-member-management/` (`spec.md`, `plan.md`, `data-model.md`, `contracts/api-contracts.md`, `research.md`, `quickstart.md`)
**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/`
**Development Approach**: **Strict TDD (Test-Driven Development)** per Constitution Principle I. All automated tests MUST be written and verified failing before writing production code.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, configuration, and testing fixtures.

- [X] T001 Create project directory structure (`src/domain`, `src/services`, `src/api`, `src/static`, `tests/unit`, `tests/integration`, `tests/api`) per plan.md
- [X] T002 [P] Create application package configuration and dependency specification in `pyproject.toml`
- [X] T003 [P] Configure Pytest test fixtures and in-memory SQLite database setup in `tests/conftest.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data layer, database schema migrations, and pre-configured seed data required by all user stories.

⚠️ **CRITICAL**: No user story implementation can begin until this foundational phase is complete.

- [X] T004 Write TDD tests for SQLite database connection and table creation in `tests/unit/test_database.py`
- [X] T005 Implement SQLite schema manager with tables `users`, `members`, and `activity_logs` in `src/services/database.py`
- [X] T006 Write TDD tests for pre-configured Onda Mooca seed data loader in `tests/integration/test_seed.py`
- [X] T007 Implement seed loader for initial leaders ("Pr. Pedro", "Mariana", "Lucas" with default PINs) in `src/services/seed.py`
- [X] T008 [P] Implement core Pydantic domain models (`UsuarioAdministrativo`, `Membro`, `RegistroAtividade`) with exact field constraints in `src/domain/models.py`
- [X] T009 [P] Initialize FastAPI application instance with CORS and static file mounting in `src/main.py`

**Checkpoint**: Core database, seed data, and base application runner verified and ready.

---

## Phase 3: User Story 1 - Authenticate via PIN & Access Roster (Priority: P1) 🎯 MVP Part 1

**Goal**: Enable administrative leaders and core members to enter their individual PIN, validate credentials against seed data, establish an active session, and unlock the application with user identification.

**Independent Test**: Enter valid seed PIN `1234` on lock screen → verifies immediate unlock, greeting "Olá, Pr. Pedro", and active session establishment. Enter invalid PIN → verifies error alert and 5-attempt rate-limiting lockout.

### Tests for User Story 1 (TDD - Write First) ⚠️

- [X] T010 [P] [US1] Write unit tests for PIN hashing, salted SHA-256 verification, and session tokens in `tests/unit/test_auth.py`
- [X] T011 [P] [US1] Write contract test for `POST /api/auth/pin` (success, invalid PIN, 5-attempt lockout) in `tests/api/test_routes_auth.py`

### Implementation for User Story 1

- [X] T012 [US1] Implement PIN verification, session token generation, and rate limiting in `src/services/auth_service.py`
- [X] T013 [US1] Implement `POST /api/auth/pin` route and session validation dependency in `src/api/routes_auth.py`
- [X] T014 [P] [US1] Build responsive PIN lock screen UI with numeric keypad in `src/static/index.html`
- [X] T015 [US1] Implement shared HTTP client in `src/static/js/api.js` (token header injection & error handling) and PIN authentication client logic with session storage in `src/static/js/auth.js`

**Checkpoint**: User Story 1 complete — leaders can securely log in via PIN with individual accountability.

---

## Phase 4: User Story 2 - Register and List Members with Audit Logging (Priority: P1) 🎯 MVP Part 2

**Goal**: Authenticated leaders register new discipleship group members with Name, unique Phone/WhatsApp, PT-BR Birthday (`DD/MM` or `DD/MM/AAAA`), and Position (`Líder`, `Núcleo`, `Membro`). View full alphabetical roster and record creation audit log.

**Independent Test**: Log in with PIN `1234`, open "+ Novo Membro", register "Lucas Silva" with valid phone and birthday → verifies member appears in roster with role badge, and creation audit log is recorded under "Pr. Pedro". Attempt duplicate phone → verifies rejection.

### Tests for User Story 2 (TDD - Write First) ⚠️

- [X] T016 [P] [US2] Write unit tests for Brazilian phone validation (10/11 digits, mask, clean digits) and PT-BR calendar validation (reject 31/02, accept DD/MM and DD/MM/AAAA) in `tests/unit/test_validators.py`
- [X] T017 [P] [US2] Write integration test for member creation, duplicate phone rejection, and audit log generation in `tests/integration/test_member_crud.py`
- [X] T018 [P] [US2] Write API contract tests for `GET /api/members` and `POST /api/members` in `tests/api/test_routes_members.py`

### Implementation for User Story 2

- [X] T019 [P] [US2] Implement phone, birthday, and position validation functions with exact regex and calendar sanity rules in `src/domain/validators.py`
- [X] T020 [US2] Implement audit log recorder service in `src/services/audit_service.py`
- [X] T021 [US2] Implement member creation and listing with strict phone uniqueness check in `src/services/member_service.py`
- [X] T022 [US2] Implement `GET /api/members` and `POST /api/members` endpoints with auth protection in `src/api/routes_members.py`
- [X] T023 [P] [US2] Build member roster view and "+ Novo Membro" modal form in `src/static/index.html`
- [X] T024 [US2] Implement member listing, registration form submission, and input masking in `src/static/js/members.js`

**Checkpoint**: User Story 2 complete — Core MVP is functional! Members can be added, validated, listed, and audited.

---

## Phase 5: User Story 3 - Edit and Update Member Information with Audit Logging (Priority: P2)

**Goal**: Authenticated leaders update existing member details (e.g. phone correction, birthday adjustment, role promotion to Núcleo/Líder). System re-validates phone uniqueness and logs field diff in audit trail.

**Independent Test**: Edit existing member "Lucas Silva", change position to "Núcleo", save → verifies roster badge updates to "Núcleo" and audit log records `Posição alterada de 'Membro' para 'Núcleo'` with user attribution.

### Tests for User Story 3 (TDD - Write First) ⚠️

- [X] T025 [P] [US3] Write integration tests for member updates, phone change uniqueness validation, and audit diff generation in `tests/integration/test_member_update.py`
- [X] T026 [P] [US3] Write API contract test for `PUT /api/members/{id}` in `tests/api/test_routes_member_update.py`

### Implementation for User Story 3

- [X] T027 [US3] Implement member update method with field diff tracking and phone collision checks in `src/services/member_service.py`
- [X] T028 [US3] Implement `PUT /api/members/{id}` endpoint with auth verification in `src/api/routes_members.py`
- [X] T029 [US3] Add edit modal dialog with pre-populated member data in `src/static/index.html`
- [X] T030 [US3] Implement edit form submission, inline error handling, and roster refresh in `src/static/js/members.js`

**Checkpoint**: User Story 3 complete — full update capabilities with automated change auditing.

---

## Phase 6: User Story 4 - Remove Member with Confirmation & Audit Logging (Priority: P3)

**Goal**: Authenticated leaders remove a member from the cell group with an explicit confirmation dialog preventing accidental deletion, logging the deletion in the audit trail.

**Independent Test**: Click delete on "Lucas Silva", dismiss confirmation dialog → verifies member remains untouched. Click delete, confirm dialog → verifies member is removed from roster and deletion audit event is recorded.

### Tests for User Story 4 (TDD - Write First) ⚠️

- [X] T031 [P] [US4] Write integration test for member deletion and audit log recording in `tests/integration/test_member_delete.py`
- [X] T032 [P] [US4] Write API contract test for `DELETE /api/members/{id}` in `tests/api/test_routes_member_delete.py`

### Implementation for User Story 4

- [X] T033 [US4] Implement member deletion and deletion audit logging in `src/services/member_service.py`
- [X] T034 [US4] Implement `DELETE /api/members/{id}` endpoint in `src/api/routes_members.py`
- [X] T035 [US4] Add deletion confirmation modal dialog in `src/static/index.html`
- [X] T036 [US4] Implement delete confirmation flow and immediate roster update in `src/static/js/members.js`

**Checkpoint**: User Story 4 complete — secure, confirmed member removal with audit trail.

---

## Phase 7: User Story 5 - Dedicated Activity History Screen (Priority: P3)

**Goal**: Provide a dedicated "Histórico de Atividades" view displaying a reverse-chronological feed of all creations, updates, and deletions with leader attribution and timestamps.

**Independent Test**: Navigate to the "Histórico" view → verifies all past member additions, edits, and deletions appear in chronological order showing acting leader's name, action type, member name, and formatted date/time.

### Tests for User Story 5 (TDD - Write First) ⚠️

- [X] T037 [P] [US5] Write integration tests for reverse-chronological activity log retrieval in `tests/integration/test_audit_service.py`
- [X] T038 [P] [US5] Write API contract test for `GET /api/history` in `tests/api/test_routes_history.py`

### Implementation for User Story 5

- [X] T039 [US5] Implement reverse-chronological log retrieval with limit support in `src/services/audit_service.py`
- [X] T040 [US5] Implement `GET /api/history` endpoint with auth verification in `src/api/routes_history.py`
- [X] T041 [P] [US5] Build "Histórico de Atividades" timeline view container in `src/static/index.html`
- [X] T042 [US5] Implement activity history rendering, event badge formatting, and tab switching in `src/static/js/history.js`

**Checkpoint**: User Story 5 complete — full transparency and accountability across cell leadership.

---

## Phase 8: User Story 6 - Search, Filter, and Quick WhatsApp Action (Priority: P4)

**Goal**: Real-time member search by name (case and accent insensitive), role filtering chips (`Líder`, `Núcleo`, `Membro`), and one-click WhatsApp action opening `https://wa.me/55...`.

**Independent Test**: Type "ana" in search bar → filters roster in <300ms. Click "Líder" filter chip → displays only leaders. Click WhatsApp icon on member with phone `(11) 98765-4321` → triggers universal WhatsApp URL `https://wa.me/5511987654321`.

### Tests for User Story 6 (TDD - Write First) ⚠️

- [X] T043 [P] [US6] Write unit tests for accent-insensitive and case-insensitive search matching in `tests/unit/test_search_filter.py`
- [X] T044 [P] [US6] Write API contract tests for `GET /api/members?search=...&position=...` in `tests/api/test_routes_member_search.py`

### Implementation for User Story 6

- [X] T045 [US6] Add accent-insensitive search and position filtering query logic in `src/services/member_service.py`
- [X] T046 [US6] Wire search and position query parameters into `GET /api/members` in `src/api/routes_members.py`
- [X] T047 [P] [US6] Add search bar input, role filter chips, and WhatsApp click-to-chat links in `src/static/index.html`
- [X] T048 [US6] Implement real-time search input listener (debounced <300ms) and role filter toggles in `src/static/js/members.js`

**Checkpoint**: User Story 6 complete — high-velocity search, filtering, and direct WhatsApp communication.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: PWA installability, Service Worker offline caching, responsive styling, and end-to-end validation.

- [X] T049 [P] Create Web App Manifest with app metadata, theme color, and icons in `src/static/manifest.json`
- [X] T050 [P] Implement Service Worker with Cache-First asset strategy (caching self-contained local SVG icons, CSS, and JS) and Network-First offline fallback in `src/static/sw.js`
- [X] T051 Register Service Worker and PWA install prompt handlers in `src/static/js/app.js`
- [X] T052 Refine responsive mobile-first CSS styling for Android, iOS, and PC viewports in `src/static/css/app.css`
- [X] T053 Execute full automated test suite (`python -m pytest tests/ -v`) and verify 100% pass rate
- [X] T054 Execute manual end-to-end scenarios per `quickstart.md` (PIN login, CRUD, offline mode)

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (BLOCKS all user stories)
    │
    ├──────────────────────────┐
    ▼                          ▼
Phase 3: US1 (PIN Auth)    Phase 4: US2 (Member CRUD P1)
    │                          │
    └──────────┬───────────────┘
               ▼
Phase 5: US3 (Member Edit P2)
               │
               ▼
Phase 6: US4 (Member Delete P3)
               │
               ▼
Phase 7: US5 (History Screen P3)
               │
               ▼
Phase 8: US6 (Search, Filter, WhatsApp P4)
               │
               ▼
Phase 9: Polish & PWA Offline
```

### User Story Dependencies

- **US1 (PIN Auth)**: Depends on Phase 2 (Foundational). Can proceed immediately after foundation.
- **US2 (Member CRUD P1)**: Depends on Phase 2 (Foundational) and US1 session token for authenticated operations.
- **US3 (Member Edit P2)**: Depends on US2 member entity and persistence structure.
- **US4 (Member Delete P3)**: Depends on US2 member entity.
- **US5 (History Screen P3)**: Depends on US1, US2, US3, US4 audit log event records.
- **US6 (Search, Filter, WhatsApp P4)**: Depends on US2 member listing view.
- **Polish Phase**: Depends on all user story implementations being complete.

---

## Parallel Execution Opportunities

- **Phase 1**: T002 (`pyproject.toml`) and T003 (`conftest.py`) can run in parallel.
- **Phase 2**: T008 (`models.py`) and T009 (`main.py`) can run in parallel.
- **Phase 3 (US1)**: Tests T010 and T011 can be written in parallel. UI layout T014 can be built in parallel with backend T012/T013.
- **Phase 4 (US2)**: Tests T016, T017, and T018 can be written in parallel. Validators T019 and UI layout T023 can be built in parallel.
- **Phase 5 (US3)**: Tests T025 and T026 can run in parallel.
- **Phase 6 (US4)**: Tests T031 and T032 can run in parallel.
- **Phase 7 (US5)**: Tests T037 and T038 can run in parallel. UI container T041 can run in parallel with backend T039/T040.
- **Phase 8 (US6)**: Tests T043 and T044 can run in parallel. UI controls T047 can run in parallel.
- **Phase 9 (Polish)**: Manifest T049 and Service Worker T050 can be created in parallel.

---

## Implementation Strategy & MVP Delivery

### MVP Phase (Phases 1, 2, 3, and 4)
Delivers a fully functional, test-driven application where:
1. Leaders authenticate via PIN.
2. Members are registered with strict PT-BR phone uniqueness, validated PT-BR birthdays, and roles.
3. Members are listed in alphabetical order with position badges.
4. All actions are logged under the acting leader's identity.

### Incremental Feature Additions
1. **Increment 2**: US3 (Edit member details and role promotions).
2. **Increment 3**: US4 (Safe member deletion with confirmation barrier).
3. **Increment 4**: US5 (Dedicated "Histórico de Atividades" screen).
4. **Increment 5**: US6 (Instant search, role filtering chips, and click-to-WhatsApp).
5. **Increment 6**: Polish (PWA installability on home screens and offline caching).
