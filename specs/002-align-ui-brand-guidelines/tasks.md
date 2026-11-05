# Tasks: Align UI & Frontend with Brand Guidelines and Constitution

**Input**: Design documents from `/specs/002-align-ui-brand-guidelines/` (`plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`)

**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Test tasks included in accordance with Constitutional Principle I (Test-Driven Development).

**Organization**: Tasks are organized by user story (P1, P2, P3) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable task (independent files, no blocking prerequisites)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`) mapping to `spec.md`
- Exact file paths are explicitly stated in every task description

---

## Phase 1: Setup (Shared Token & Styling Infrastructure)

**Purpose**: Initialize official Onda design tokens, typography, and base CSS variables across frontend assets.

- [X] T001 Configure Tailwind CSS tokens (`onda.blue.900` `#181e5f` through `onda.blue.500` `#2537de`, `onda.offwhite` `#eeeee7`, `onda.dark` `#161616`, `onda.mint` `#79caab`, `onda.cyan.100` `#e5f4fe`, fonts, shadows) in `src/static/index.html`
- [X] T002 [P] Import Space Grotesk Google Font and define fallback font families in `src/static/index.html` and `src/static/css/app.css`
- [X] T003 [P] Define CSS custom properties and core Glassmorphism utility classes (`.glass-card`, `.glass-modal`, `.glass-pill`, `.glass-nav`, `.shadow-glass`, `.shadow-glass-glow`) in `src/static/css/app.css`

---

## Phase 2: Foundational (Brand Assets & PWA Shell)

**Purpose**: Core brand assets and PWA metadata that MUST be in place before user story interfaces are wired up.

**⚠️ CRITICAL**: Foundational assets required for UI components.

- [X] T004 Create official horizontal lowercase `"igreja onda"` vector SVG wordmark component with 1.78X:8.53X aspect ratio and clear space in `src/static/index.html`
- [X] T005 [P] Update PWA manifest theme and background colors to `theme_color: "#181e5f"` and `background_color: "#181e5f"` in `src/static/manifest.json`
- [X] T006 [P] Redesign PWA application icon with Onda Blue wave gradient (`#181e5f` to `#11187e`) and concentric wave circles in `src/static/icons/icon.svg`

**Checkpoint**: Brand tokens and foundational PWA assets in place; User Story implementation can begin.

---

## Phase 3: User Story 1 - Brand Identity & Atmosphere Across Core Surfaces (Priority: P1) 🎯 MVP

**Goal**: Deliver the authentic Onda brand identity on core surfaces: dark wave gradient background, official horizontal lowercase vector SVG logo (`"igreja onda"`), glassmorphic PIN lock screen, top navigation header with brand typography, active tabs, and PWA shell metadata (`manifest.json` and `icon.svg`).

**Independent Test**: Launch the application at `http://localhost:8000`, verify the dark wave gradient background and glassmorphic keypad on the PIN access screen, enter PIN `1234`, and verify that the top navigation displays the horizontal lowercase `"igreja onda"` SVG wordmark, Right Grotesk uppercase title, user role badge, and active tab styling.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST and ensure they FAIL before implementation.**

- [X] T007 [P] [US1] Write automated test in `tests/api/test_routes_static.py` asserting `manifest.json` defines `theme_color: "#181e5f"` and `icon.svg` contains Onda Blue palette tokens (`#181e5f`, `#1f2bc8`)
- [X] T008 [P] [US1] Write automated test in `tests/api/test_routes_static.py` asserting `index.html` serves the horizontal lowercase `"igreja onda"` SVG logo and dark wave gradient background classes

### Implementation for User Story 1

- [X] T009 [US1] Refactor PIN lock screen layout, concentric rings background, glassmorphic card container (`backdrop-blur-xl`, `border-white/15`), and keypad buttons in `src/static/index.html` and `src/static/js/auth.js`
- [X] T010 [US1] Refactor top navigation header in `src/static/index.html` with horizontal lowercase SVG wordmark, Right Grotesk uppercase title, user greeting, role badge, and active tab contrast indicators

**Checkpoint**: User Story 1 (MVP) is fully functional and testable independently.

---

## Phase 4: User Story 2 - Responsive Glassmorphic Member Roster & Interaction Modals (Priority: P2)

**Goal**: Refactor the member roster list, search input, status badges (Líder, Núcleo, Membro), action buttons, and member create/edit modal dialogs to use official glassmorphism styling, clean typography, and brand color tokens.

**Independent Test**: Search for members, observe glassmorphic card containers (`rounded-2xl`, translucent white border, backdrop blur), role badges using brand tokens (`onda-blue`, `onda-mint`, `onda-cyan`), open create/edit member modal and verify glassmorphic backdrop and Onda Blue 600 CTA button.

### Tests for User Story 2 ⚠️

- [X] T011 [P] [US2] Write automated test in `tests/api/test_routes_static.py` asserting role badge CSS classes (`badge-lider`, `badge-nucleo`, `badge-membro`) and glassmorphic card styles exist in `src/static/css/app.css`

### Implementation for User Story 2

- [X] T012 [P] [US2] Update role badge styles in `src/static/css/app.css` with exact token mappings: `lider` (`rgba(31, 43, 200, 0.35)` text `#9cc7e4`), `nucleo` (`rgba(121, 202, 171, 0.25)` text `#79caab`), and `membro` (`rgba(227, 243, 247, 0.15)` text `#e5f4fe`)
- [X] T013 [US2] Refactor member card HTML template in `src/static/js/members.js` to render glassmorphic containers (`rounded-2xl`, `bg-white/10`, `backdrop-blur-md`, `border-white/15`), brand badges, and Space Grotesk typography
- [X] T014 [US2] Refactor member create/edit modal dialog, action bar, search input, and primary CTA button (`bg-onda-blue-600` hover `bg-onda-blue-500`) in `src/static/index.html` and `src/static/js/members.js`

**Checkpoint**: User Stories 1 AND 2 are both functional and independently testable.

---

## Phase 5: User Story 3 - Activity History, Status Banners & Welcoming Tone (Priority: P3)

**Goal**: Align activity history items, offline banner, and toast/notification pills with the brand's pill and reminder styling, applying the welcoming, direct tone of voice ("sem rodeios", biblical and inspiring).

**Independent Test**: Trigger offline mode or simulate an update action, verify that notification pills render in glassmorphic pill formats (`rounded-full` or `rounded-2xl`) with Mint/Onda Blue status accents and inspiring microcopy.

### Tests for User Story 3 ⚠️

- [X] T015 [P] [US3] Write automated test in `tests/api/test_routes_static.py` asserting offline banner and toast notification container use glassmorphic pill classes and brand typography

### Implementation for User Story 3

- [X] T016 [US3] Refactor activity history log item rendering in `src/static/js/history.js` using glassmorphic cards, SF Pro Display timestamps, and Onda Blue action icons
- [X] T017 [US3] Refactor offline banner and toast notification feedback in `src/static/index.html` and `src/static/js/app.js` with glassmorphic pill styling (`rounded-full`, `backdrop-blur-md`, `border-white/20`, Mint accents) and inspiring microcopy

**Checkpoint**: All three user stories are complete and independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Accessibility verification, fallback safety, and end-to-end quickstart validation across all screens.

- [X] T018 [P] Verify WCAG AA contrast ratios (≥ 4.5:1 for body copy, ≥ 3.0:1 for headings/icons) across all text and glassmorphic card surfaces in `src/static/css/app.css` and `src/static/index.html`
- [X] T019 [P] Add CSS `@supports not (backdrop-filter: blur(1px))` fallback rules with semi-opaque `#11187e` solid backgrounds in `src/static/css/app.css`
- [X] T020 Run complete test suite and execute all manual validation scenarios in `specs/002-align-ui-brand-guidelines/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion. Delivers the core brand MVP.
- **User Story 2 (Phase 4)**: Depends on Phase 1 & 2 completion; integrates with User Story 1 navbar.
- **User Story 3 (Phase 5)**: Depends on Phase 1 & 2 completion; extends history view and notifications.
- **Polish (Phase 6)**: Depends on completion of User Stories 1, 2, and 3.

### User Story Dependencies

- **US1 (P1)**: Independent of other stories; requires Foundational phase (T001-T006).
- **US2 (P2)**: Independent functionality; shares base CSS classes from T003/T012.
- **US3 (P3)**: Independent functionality; shares base CSS classes from T003.

### Parallel Opportunities

- **Phase 1**: T002 and T003 can execute in parallel after T001.
- **Phase 2**: T005 and T006 can execute in parallel while T004 is being designed.
- **Phase 3**: Tests T007 and T008 can be written in parallel.
- **Phase 4**: T011 and T012 can execute in parallel before T013/T014.
- **Phase 5**: T015 can be written in parallel with T016.
- **Phase 6**: T018 and T019 can execute in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003).
2. Complete Phase 2: Foundational (T004-T006).
3. Complete Phase 3: User Story 1 (T007-T010).
4. **STOP and VALIDATE**: Verify PIN screen, navbar, horizontal SVG wordmark, and PWA shell.
5. Deliver/Demonstrate MVP.

### Incremental Delivery

1. Setup + Foundational → Brand infrastructure ready.
2. User Story 1 → Test independently → Core brand atmosphere & entry (MVP!).
3. User Story 2 → Test independently → Glassmorphic member roster & modals.
4. User Story 3 → Test independently → Activity history & notification pills.
5. Polish & Verification → WCAG AA verification and quickstart sign-off.
