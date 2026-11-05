# Research & Technical Decisions: Member Management (GD Manager)

**Feature**: `001-member-management`
**Date**: 2026-11-05
**Status**: Completed

## 1. Architecture & Technology Stack

### Decision
A modern, zero-dependency stack combining **FastAPI (Python 3.14)** with **SQLite** on the backend and a **Vanilla/Modern ES Modules PWA** (HTML5, CSS3, JavaScript) on the frontend.

### Rationale
- **Zero Cost & Lean Infrastructure**: Python 3.14, FastAPI, and SQLite are already available in the runtime environment. SQLite requires zero configuration, zero cloud database subscriptions, and zero ongoing server maintenance ($0/month).
- **Universal Multiplatform PWA**: The frontend consists of standards-compliant web technologies (Web App Manifest, Service Worker, Responsive CSS) that run identically across Android (Chrome/Firefox), iOS (Safari PWA), and PC (Desktop browsers) without third-party framework churn.
- **TDD Compatibility**: `pytest 9.2.0` and `httpx` allow writing lightning-fast, deterministic automated tests for all business logic, phone/date validations, authentication, and audit trails before writing any implementation code.
- **Maintainability (KISS/YAGNI)**: Avoids complex microservice setups, heavyweight node builds, and expensive database hosting. The entire system can be tested, run, or containerized effortlessly.

### Alternatives Considered
- *Full-stack Node.js / Next.js*: Rejected due to absence of Node/npm in the current sandbox environment, heavy dependency bloat, and frequent breaking changes across versions.
- *Pure Client-Side LocalStorage without Backend*: Rejected because multiple GD leaders (Pastor, Líder, Núcleo) need to share the same member roster and see who performed which edits. A local-only app would isolate data on a single phone.
- *Third-party BaaS (Supabase/Firebase)*: Evaluated, but introduces external service dependencies, vendor lock-in, and configuration complexity. An embedded SQLite database provides total autonomy and zero cost.

---

## 2. PWA Strategy & Offline Support

### Decision
Implement a standard Progressive Web App using:
1. `manifest.json`: Defines app metadata (`name: "GD Manager"`, `short_name: "GD Manager"`, `display: "standalone"`, `theme_color: "#1e293b"`, icons for mobile home screens).
2. `sw.js` (Service Worker): Implements a Cache-First strategy for static assets (HTML, CSS, JS, icons) and a Network-First strategy with local client fallback for member roster viewing.
3. Offline Experience: The application caches the latest retrieved member roster and activity history locally (`localStorage`/`IndexedDB`). When connectivity is lost, leaders can still browse members, view birthdays, and initiate direct WhatsApp calls.

### Rationale
- Complies strictly with Principle II (Progressive Web App & Multiplatform First) of the Constitution.
- Solves poor network scenarios during church cell meetings (e.g., in homes or basements with weak cellular reception).

### Alternatives Considered
- *Native Android/iOS apps*: Prohibited by the Constitution (Principle II) due to app store fees and multi-codebase maintenance.
- *Online-only Web App*: Fails usability requirements during cell gatherings when internet connectivity drops.

---

## 3. User Authentication via PIN & Session Management

### Decision
- Each authorized leader/core member has a unique record containing their `id`, `name`, `role` (`Líder` or `Núcleo`), and numeric `pin` (stored as a secure salted hash).
- Authentication endpoint (`POST /api/auth/pin`) validates the submitted PIN.
- On success, the API returns a lightweight signed session token and user profile (`id`, `name`, `role`).
- The frontend stores the active session in `sessionStorage`/`localStorage` and transmits it via the `Authorization: Bearer <token>` header on all subsequent requests.
- **Security & Lockout**: 5 consecutive incorrect PIN attempts enforce a 30-second client-side and server-side cooldown to mitigate brute-force guessing.

### Rationale
- Fulfills the explicit user clarification: "PIN por usuário, para podermos efetuar logging das ações de cada usuário."
- Significantly simpler than email/password or OAuth workflows, eliminating registration confirmation emails, password reset flows, and complex user management while still providing complete action accountability.

### Alternatives Considered
- *Shared group password*: Rejected by user clarification; cannot identify which individual leader made changes.
- *OAuth2 / Social Login*: Overkill for a single cell group of 3-5 leaders, adding third-party API dependencies and setup friction.

---

## 4. Audit Logging (Histórico de Atividades)

### Decision
- Dedicated `activity_logs` table in SQLite recording every mutation (`CREATE_MEMBER`, `UPDATE_MEMBER`, `DELETE_MEMBER`).
- Captures: `id`, `user_id`, `user_name`, `action_type`, `member_id`, `member_name`, `details` (JSON diff of modified fields for updates), and `timestamp` (ISO-8601 UTC).
- Dedicated endpoint `GET /api/history` returning records in reverse-chronological order.
- The UI features a dedicated "Histórico de Atividades" view displaying a timeline feed of all operations.

### Rationale
- Direct response to User Clarifications 2 and 3.
- Guarantees transparency and accountability across cell leadership.

### Alternatives Considered
- *In-place updated_at columns only*: Insufficient because it does not record deletions or provide a historical audit log of past changes.

---

## 5. PT-BR Formatting & Validation Rules

### Decision
- **Phone / WhatsApp**:
  - Validates Brazilian mobile and landline patterns: `(XX) 9XXXX-XXXX` (11 digits) or `(XX) XXXX-XXXX` (10 digits).
  - Normalizes phone numbers to pure digits (`DDD + 8 or 9 digits`) for database storage and uniqueness checking.
  - Generates WhatsApp click-to-chat links using `https://wa.me/55<digits>`.
  - Enforces strict uniqueness across all active members.
- **Birthday**:
  - Accepts standard PT-BR format: `DD/MM/AAAA` or `DD/MM` (year optional).
  - Validates calendar rules: rejects nonexistent dates (e.g., `31/02`, `31/04`, `29/02` on non-leap years) and future birth years.
- **Position**:
  - Strictly limited to `Líder`, `Núcleo`, or `Membro`.

### Rationale
- Matches standard Brazilian church conventions and user expectations without external third-party validation libraries.

---

## 6. Seed Data & Initialization

### Decision
The system initializes with a default seed dataset populated upon first run:
- Initial Onda Mooca leaders:
  1. `Pr. Pedro (Líder)` - Default PIN: `1234`
  2. `Mariana (Núcleo)` - Default PIN: `5678`
  3. `Lucas (Núcleo)` - Default PIN: `4321`
- Seed data automatically checks if the `users` table is empty; if so, populates initial accounts and logs a `SYSTEM_INIT` event.

### Rationale
- Satisfies User Clarification 4 ("Pre-configured seed data").
- Enables instantaneous out-of-the-box operation upon deployment.

---

## 7. Testing & TDD Strategy

### Decision
- Test Runner: `pytest` with `pytest-asyncio` and `httpx.AsyncClient`.
- Execution:
  1. Domain / Unit Tests: Validate phone formatting, PT-BR birthday calendar sanity, and PIN hash verification in isolation.
  2. Service / Integration Tests: Validate SQLite repository contracts, duplicate phone rejection, audit log recording, and seed initialization.
  3. API Tests: Validate HTTP status codes, payload structures, authentication barriers, and error messages.
- Test suites run in-memory (`:memory:` SQLite database) ensuring sub-second execution for rapid Red-Green-Refactor cycles.
