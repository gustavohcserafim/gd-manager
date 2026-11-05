# Feature Specification: Member Management

**Feature Branch**: `001-member-management`

**Created**: 2026-11-05

**Status**: Draft

**Input**: User description: "Todo acessos feito ao aplicativo será por usuários que tem privilégio administrativos (lider ou membro do nucleo). Desenvolva a plataforma de gestão de membros, um CRUD classico. Devemos armazenar incialmente: Nome, Número de telefone/Whatsapp, data de aniversario(em formato pt-br), e posição (Lider, Nucleo ou membro)."

## Clarifications

### Session 2026-11-05
- Q: Should the system allow multiple members to share the same phone/WhatsApp number? → A: Option B: Enforce strict uniqueness (reject any duplicate phone number).
- Q: How should the application gate access for administrative users (leaders and core members)? → A: Individual PIN per user, enabling activity logging for each user's actions.
- Q: How should the activity log of user actions be displayed to administrative users in the application? → A: Option B: Dedicated "Histórico de Atividades" screen (chronological list of all creations, edits, and deletions).
- Q: How should initial administrative users (leaders and core members) be registered and provisioned in the application? → A: Option B: Pre-configured seed data (system deploys with pre-loaded initial leaders and default PINs).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticate via PIN & Access Roster (Priority: P1)

An administrative user (leader or core member) opens the application and enters their personal PIN (from pre-configured seed data) to identify themselves, unlocking access to the member roster and enabling tracked administrative actions.

**Why this priority**: Required entry point to identify the acting user and satisfy the audit logging requirement for all subsequent member mutations.

**Independent Test**: Can be tested independently by entering a valid user PIN, verifying immediate unlock and display of the user's name/greeting, and confirming that invalid PINs are rejected with appropriate feedback.

**Acceptance Scenarios**:

1. **Given** an administrative user with a pre-configured seed PIN, **When** they enter their valid PIN on the lock screen, **Then** the application unlocks immediately, sets the active session with the user's identity, and displays the member roster.
2. **Given** the PIN lock screen, **When** an invalid or unknown PIN is entered, **Then** the system denies access, displays an invalid PIN alert, and prompts the user to re-enter.
3. **Given** an active authenticated session, **When** the user closes and re-opens the PWA within an active session timeout window, **Then** the application restores the authenticated session without requiring re-entry.

---

### User Story 2 - Register and List Members with Audit Logging (Priority: P1)

An authenticated administrative user needs to register new discipleship group members and view the full roster, with the system automatically recording who registered each member.

**Why this priority**: Core value of the application; allows recording and viewing all cell participants while maintaining accountable action history.

**Independent Test**: Can be tested independently by filling in valid member details (Name, unique Phone/WhatsApp, PT-BR Birthday, and Position), submitting the form, verifying the member appears in the list, and verifying the action log records the registration by the active user.

**Acceptance Scenarios**:

1. **Given** an authenticated user ("Pr. Pedro"), **When** they fill in valid details (Name: "Lucas Silva", WhatsApp: "(11) 98765-4321", Birthday: "15/03/1998", Position: "Membro") and submit, **Then** the system saves the member, displays them in the roster, and records a creation log event attributable to "Pr. Pedro".
2. **Given** an authenticated user viewing the roster, **When** members exist, **Then** each member displays their name, formatted phone number, birthday, and position badge (Líder, Núcleo, or Membro).
3. **Given** an authenticated user attempting to register a member, **When** mandatory fields are missing or blank, **Then** the system blocks submission and highlights the missing fields.
4. **Given** a phone number already registered for an existing member, **When** an authenticated user attempts to register another member with the identical phone number, **Then** the system rejects registration and alerts that the phone number is already registered.

---

### User Story 3 - Edit and Update Member Information with Audit Logging (Priority: P2)

An authenticated administrative user needs to update existing member details (e.g., corrected phone, birthday, or position promotion), with all updates attributed in the audit trail.

**Why this priority**: Cell data changes dynamically; updates must be tracked so leaders know who last modified member records.

**Independent Test**: Can be tested independently by selecting an existing member, modifying attributes, saving, and verifying updated values on screen along with an update audit log entry.

**Acceptance Scenarios**:

1. **Given** an existing member "Lucas Silva" with position "Membro", **When** authenticated user "Mariana (Núcleo)" edits his position to "Núcleo" and saves, **Then** the system updates the record, displays the new position badge, and logs the change under Mariana's user ID.
2. **Given** an authenticated user in the edit form, **When** they enter an invalid date format (e.g., "32/13/2000") or a duplicate phone number assigned to another member, **Then** the system shows validation errors and retains the existing valid data.
3. **Given** an authenticated user editing a member, **When** they cancel the edit dialog, **Then** member data remains unmodified and no audit event is logged.

---

### User Story 4 - Remove Member with Confirmation & Audit Logging (Priority: P3)

An authenticated administrative user removes a member who has left the cell, guarded by an explicit confirmation prompt and logged for accountability.

**Why this priority**: Prevents accidental deletions while keeping an audit record of who removed the member.

**Independent Test**: Can be tested independently by initiating member deletion, confirming the prompt, and checking that the member is removed from the active roster and a deletion event is logged.

**Acceptance Scenarios**:

1. **Given** an existing member in the list, **When** the user clicks delete, **Then** the system presents an explicit confirmation dialog.
2. **Given** the confirmation dialog, **When** the user confirms deletion, **Then** the member is removed from the roster and a deletion event is recorded with the user's ID and timestamp.
3. **Given** the confirmation dialog, **When** the user cancels, **Then** the member remains in the roster untouched.

---

### User Story 5 - Dedicated Activity History Screen (Priority: P3)

An authenticated administrative user opens the dedicated "Histórico de Atividades" screen to audit all past group operations chronologically.

**Why this priority**: Fulfills the governance and tracking requirement, allowing cell leaders to review who added, modified, or removed members.

**Independent Test**: Can be tested independently by navigating to the history screen and verifying that all previously performed operations appear in reverse chronological order with the user's name, timestamp, and details.

**Acceptance Scenarios**:

1. **Given** authenticated users have created, edited, and deleted members, **When** an administrative user navigates to the "Histórico de Atividades" screen, **Then** the system displays a chronological log feed showing user name, action type, affected member name, and timestamp.
2. **Given** an edit operation was performed, **When** viewing the history entry, **Then** the log specifies which fields were modified.
3. **Given** no activity has occurred yet, **When** opening the history screen, **Then** an informative empty state indicates no recorded actions yet.

---

### User Story 6 - Search, Filter, and Quick WhatsApp Action (Priority: P4)

An authenticated user quickly searches members by name, filters by position, and initiates one-click WhatsApp chats.

**Why this priority**: Speeds up weekly cell communication and member lookups on mobile devices.

**Independent Test**: Can be tested independently by filtering via search input, clicking role filter chips, and clicking the WhatsApp icon to open the formatted `wa.me` URL.

**Acceptance Scenarios**:

1. **Given** a list of members, **When** typing "Ana" in the search bar, **Then** the roster filters in real-time to only show matching members.
2. **Given** a list of members with mixed roles, **When** clicking the "Líder" filter, **Then** only leaders are displayed.
3. **Given** a member with phone "(11) 98765-4321", **When** tapping the WhatsApp action, **Then** the application triggers the universal link (`https://wa.me/5511987654321`).

---

### Edge Cases

- **Strict Phone Number Uniqueness**: Phone/WhatsApp numbers MUST be strictly unique across all members. Duplicate phone numbers are rejected during both creation and edits.
- **PIN Lockout & Security**: If an invalid PIN is entered 5 consecutive times, the system enforces a temporary 30-second cooldown before allowing subsequent attempts.
- **PT-BR Birthday Formatting**:
  - Accepts standard Brazilian date formats (`DD/MM/AAAA` or `DD/MM` when year is omitted).
  - Validates calendar sanity: rejects invalid days (e.g., `31/02`), invalid months (`> 12` or `< 1`), and future birth years.
- **Brazilian Phone Number Formatting**:
  - Accepts 10-digit (landline) and 11-digit (mobile with 9th digit) numbers, applying standard mask `(XX) XXXXX-XXXX` or `(XX) XXXX-XXXX`.
- **Offline Roster Access & Local Audit Sync**:
  - In line with PWA principles, when offline, cached members and the history screen can be browsed. Actions taken while offline are staged locally with the authenticated user's ID and synced when connectivity resumes.
- **Empty States**:
  - When no members exist yet, the system shows an encouraging empty state prompting the user to register their first member.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST require administrative users to authenticate using an individual PIN before granting access to member management.
- **FR-002**: System MUST allow authenticated administrative users to register a new member with the following required attributes: Full Name (`Nome`), Phone/WhatsApp (`Telefone/WhatsApp`), Birthday (`Data de aniversário`), and Position (`Posição`).
- **FR-003**: System MUST validate that the member's `Posição` is strictly one of three designated values: `Líder`, `Núcleo`, or `Membro`.
- **FR-004**: System MUST enforce PT-BR date format for birthdays (`DD/MM/AAAA` or `DD/MM`), rejecting impossible calendar dates.
- **FR-005**: System MUST validate Brazilian phone numbers, accepting DDD plus 8 or 9 digits, formatting display cleanly as `(XX) XXXXX-XXXX` or `(XX) XXXX-XXXX`, and strictly enforcing uniqueness across all members.
- **FR-006**: System MUST display the full list of members in alphabetical order by name by default, showing name, phone, birthday, and role badge.
- **FR-007**: System MUST allow authenticated users to edit all attributes (`Nome`, `Telefone`, `Data de aniversário`, `Posição`) of any existing member, re-validating phone uniqueness if modified.
- **FR-008**: System MUST provide a deletion capability for any member record, requiring an explicit confirmation dialog before removal.
- **FR-009**: System MUST record an activity log (audit trail) for every member creation, update, and deletion, capturing the user's identity, timestamp, operation type, and modified attributes.
- **FR-010**: System MUST associate each member record with the user who created it (`createdByUserId`) and the user who last updated it (`updatedByUserId`).
- **FR-011**: System MUST provide a dedicated "Histórico de Atividades" screen accessible to authenticated users, displaying a reverse-chronological list of all logged events (creation, update, deletion) showing user name, action type, affected member, changed fields (for updates), and formatted date/time.
- **FR-012**: System MUST provide real-time search filtering by member name (case-insensitive and accent-insensitive).
- **FR-013**: System MUST provide position-based filtering allowing users to view all members, or filter specifically by `Líder`, `Núcleo`, or `Membro`.
- **FR-014**: System MUST provide a one-click WhatsApp action for members with valid phone numbers, opening WhatsApp directly (`https://wa.me/55...`).
- **FR-015**: System MUST persist member records and audit logs across browser sessions and support offline read access as required by PWA standards.
- **FR-016**: System MUST initialize on deployment with pre-configured seed data containing initial Onda Mooca leadership accounts and default PINs, allowing immediate administrative access and action logging without manual onboarding.

### Key Entities *(include if feature involves data)*

- **Administrative User (`UsuarioAdministrativo`)**:
  - Represents an authorized leader or core member who can access the app.
  - Attributes:
    - `id`: Unique identifier.
    - `name` (`nome`): Full or display name of the leader/core member.
    - `pin`: Personal numeric PIN used to unlock the application.
    - `role` (`cargo`): `Líder` or `Núcleo`.
    - `active`: Boolean flag indicating whether the user is active.

- **Member (`Membro`)**:
  - Represents an individual participant in the discipleship cell group (GD).
  - Attributes:
    - `id`: Unique identifier.
    - `name` (`nome`): Full or preferred name (text, required, min 2 characters).
    - `phone` (`telefone`): Contact phone and WhatsApp number (digits, strictly unique, required).
    - `birthDate` (`dataNascimento`): Birthday in PT-BR format (`DD/MM/AAAA` or `DD/MM`, required).
    - `position` (`posicao`): Role in the group, strictly `Líder`, `Núcleo`, or `Membro` (required).
    - `createdByUserId`: ID of the administrative user who created the member.
    - `updatedByUserId`: ID of the administrative user who last updated the member.
    - `createdAt`: Timestamp when the member was added to the group.
    - `updatedAt`: Timestamp when member details were last updated.

- **Audit Log (`RegistroAtividade`)**:
  - Represents an immutable log entry of administrative actions.
  - Attributes:
    - `id`: Unique identifier.
    - `userId`: ID of the administrative user who performed the action.
    - `userName`: Cached name of the user at the time of the action.
    - `actionType`: `CREATE_MEMBER`, `UPDATE_MEMBER`, or `DELETE_MEMBER`.
    - `memberId`: ID of the affected member.
    - `memberName`: Name of the affected member.
    - `details`: Summary of modified fields (for updates).
    - `timestamp`: Date and time when the action occurred.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Administrative users can unlock the application with their personal PIN in under 3 seconds.
- **SC-002**: Administrative users can register a new member with all valid fields in under 30 seconds.
- **SC-003**: The member list and all member details render within 1 second on mobile and desktop devices.
- **SC-004**: Real-time search by name or filtering by role produces filtered results on screen in under 300 milliseconds.
- **SC-005**: 100% of member create, update, and delete actions are permanently recorded in the audit log with the acting user's ID and exact timestamp.
- **SC-006**: Authenticated users can navigate to and view the "Histórico de Atividades" screen in under 1 second.
- **SC-007**: 100% of duplicate phone numbers, malformed phone numbers, or invalid calendar dates are intercepted and highlighted with clear guidance, preventing conflicting or invalid submissions.
- **SC-008**: 100% of cached member records are accessible and readable when the application is launched without an active internet connection (PWA offline capability).
- **SC-009**: 0% unintentional deletions: no member record can be deleted without triggering and confirming an explicit confirmation prompt.

## Assumptions

- **Target Audience & Authorization**: All users accessing the application are authorized administrators (leaders or core group members of the GD). Individual PINs identify each leader for action logging purposes without requiring complex multi-tier RBAC.
- **Administrative User Provisioning**: The application initializes with pre-configured seed data for Onda Mooca leaders and core members with default PINs, allowing immediate use upon deployment.
- **Single GD Scope**: In this initial release, all registered members belong to the Onda Mooca GD managed in the application instance. Multi-tenant or cross-church cell grouping is out of scope.
- **Birthday Format**: PT-BR convention `DD/MM/AAAA` is standard, with birth year optional (`DD/MM`) to respect members who prefer not to disclose their birth year while still supporting annual cell celebrations.
- **WhatsApp Integration**: Uses standard universal web links (`wa.me`) to open WhatsApp on Android, iOS, and PC without requiring external paid WhatsApp Business APIs.
- **Offline-First PWA**: Member data and pending audit events are stored locally (client storage / IndexedDB) with cloud synchronization when online, ensuring resilience and low infrastructure cost consistent with the project constitution.
