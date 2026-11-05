# Feature Specification: Align UI & Frontend with Brand Guidelines and Constitution

**Feature Branch**: `002-align-ui-brand-guidelines`

**Created**: 2026-11-05

**Status**: Draft

**Input**: User description: "Ajuste todo o frontend e UI do projeto para as novas diretrizes da constituição"

## Clarifications

### Session 2026-11-05

- Q: Should the GD Manager interface operate exclusively in the immersive Dark Wave theme, or should it also support an alternate Light theme mode? → A: Strict Dark Wave theme only (Option A). All screens, dialogs, and components will exclusively render the signature deep wave gradient (`#181e5f` → `#11187e` → `#1f2bc8`), translucent glass cards, and high-contrast accents without an alternate light theme mode.
- Q: Should the PWA shell metadata (manifest theme-color and home screen app icon) also be updated to the Onda Blue palette and brand motif? → A: Yes (Option A). Both `manifest.json` (`theme_color: #181e5f`, `background_color: #181e5f`) and `icon.svg` will be updated to reflect the official Onda Blue palette and concentric wave brand motif for end-to-end PWA brand consistency.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Brand Identity & Atmosphere Across Core Surfaces (Priority: P1)

When a leader or member opens the GD Manager application or installs it on their device home screen, they immediately encounter the authentic Igreja Onda digital visual identity: the dark wave atmosphere, authentic horizontal wordmark logo, distinctive Onda blue color palette, updated PWA app icon/theme color, and modern glassmorphic surfaces on the entry and navigation screens.

**Why this priority**: Establishes brand credibility, recognition, and psychological alignment with the church's cultural identity before accessing management operations.

**Independent Test**: Can be fully tested by launching the application on mobile or desktop, viewing the PIN access screen and top navigation header, inspecting the PWA manifest/icon colors, and verifying the presence of the dark wave gradient, horizontal lowercase logo, and glassmorphic container aesthetics.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user opens the application, **When** the PIN lock screen is displayed, **Then** the screen renders the dark wave gradient background, a glassmorphic keypad/card with backdrop blur and subtle translucent borders, and Onda color tokens.
2. **Given** an authenticated user views the main application, **When** inspecting the top navigation header, **Then** the official horizontal `"igreja onda"` wordmark logo is displayed in lowercase SVG format with required clear space, and the app header uses brand typography.
3. **Given** a user navigates between application views (e.g., Members and History), **When** switching tabs, **Then** active tabs clearly indicate their selected state with Onda Blue and subtle glass indicators while inactive tabs maintain readable, accessible contrast.
4. **Given** a user views the PWA manifest and mobile browser shell, **When** inspecting theme color and app icon, **Then** the PWA manifest specifies `#181e5f` as the theme/background color and `icon.svg` depicts the Onda Blue palette and wave emblem.

---

### User Story 2 - Responsive Glassmorphic Member Roster & Interaction Modals (Priority: P2)

As a GD leader managing group members, I want the members roster, search inputs, status badges, action buttons, and modal dialogs to feature the official glassmorphism styling, clean typography hierarchy, and recognizable status colors so that managing disciples is visually clear, pleasant, and intuitive.

**Why this priority**: The members list and member detail modals constitute the primary operational workflow for cell group leaders; aligning these surfaces ensures consistency and day-to-day usability.

**Independent Test**: Can be fully tested by searching for members, viewing member cards, opening the member creation/editing modal, and observing glassmorphic styling, rounded-2xl/3xl card containers, and WCAG AA contrast.

**Acceptance Scenarios**:

1. **Given** a leader views the member list, **When** member cards render, **Then** each card presents a glassmorphic surface (translucent background, backdrop-blur, subtle border, rounded-2xl to 3xl) with clear typography hierarchy (Space Grotesk body, Right Grotesk uppercase headings/numbers where applicable).
2. **Given** a leader inspects member role tags (Líder, Núcleo, Membro), **When** the badges render, **Then** they use official brand color tokens (Onda Blue, Mint, Cyan) with readable contrast.
3. **Given** a leader clicks to add or edit a member, **When** the modal dialog opens, **Then** it appears over a blurred translucent backdrop with a glassmorphic card container, and the primary action button is styled in Onda Blue 600 with hover feedback.

---

### User Story 3 - Activity History, Status Banners & Welcoming Tone (Priority: P3)

As a leader reviewing past actions or receiving system feedback, I want activity logs, offline banners, and notification pills to follow the brand's notification and pill styling with direct, inspiring, and welcoming microcopy.

**Why this priority**: Completes all auxiliary touchpoints and reinforces the church's welcoming tone of voice ("sem rodeios", biblical, and inspiring) across alerts and historical logs.

**Independent Test**: Can be fully tested by performing a data update or viewing the history log, verifying that toast notifications and banners render in glassmorphic pill formats with official microcopy.

**Acceptance Scenarios**:

1. **Given** a leader performs an action (e.g., saving a member or toggling status), **When** confirmation or feedback displays, **Then** it renders as an official glassmorphic notification pill with rounded-full or rounded-2xl shape and Mint/Onda Blue status accents.
2. **Given** the application enters offline mode, **When** the offline notice appears, **Then** it is presented as a sleek glassmorphic banner with clear, friendly, and non-alarmist microcopy.
3. **Given** a user reads system empty states or action prompts, **When** reading the text, **Then** the phrasing aligns with the direct, warm, and inspiring tone of voice specified in the brand guidelines.

---

### Edge Cases

- **Lack of Backdrop-Filter Support**: On older browsers or devices lacking CSS backdrop-filter capabilities, surfaces must fall back to semi-opaque solid surfaces (`#181e5f` / `#11187e`) maintaining legible contrast and clear border definitions without layout breakage.
- **Extreme Screen Widths**: On small mobile screens (down to 320px width), glassmorphic cards, buttons, search bars, and logo padding must wrap and resize cleanly without horizontal overflow or touch target clipping.
- **Accessibility & Contrast**: On varying background gradient sections, all text, badges, and actionable controls must maintain WCAG AA contrast ratios (at least 4.5:1 for body text, 3:1 for large text/icons).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST operate exclusively in the official Dark Wave visual theme across all application surfaces, utilizing the deep gradient (`#181e5f` → `#11187e` → `#1f2bc8`), translucent glassmorphic surfaces, and tokenized accents (Onda Blue, Mint, Cyan, Offwhite) without an alternate light theme mode.
- **FR-002**: System MUST render the official `"igreja onda"` wordmark logo horizontally in lowercase SVG format with required clear space; stacked logo variants and system-font approximations are strictly prohibited.
- **FR-003**: System MUST style cards, headers, navigation bars, modals, and notification containers using the official Glassmorphism visual language (translucent backgrounds between 10% and 30%, backdrop blur, subtle translucent white borders, and organic rounded corners: rounded-2xl, rounded-3xl, or rounded-full).
- **FR-004**: System MUST apply the brand typography hierarchy: Space Grotesk for body text, form controls, and general headings; Right Grotesk (Compact Black / Tight Dark) in UPPERCASE for prominent hero titles, counts, and time displays; and SF Pro Display (or system fallback) for microcopy, badges, and metadata.
- **FR-005**: System MUST style primary interactive call-to-action buttons in Onda Blue 600 (`#1f2bc8`) with Onda Blue 500 (`#2537de`) hover states and responsive touch feedback.
- **FR-006**: System MUST format status tags, role badges (Líder, Núcleo, Membro), and alert pills using brand secondary tokens (Mint for positive states, Cyan/Blue for informational states) with high-contrast text.
- **FR-007**: System MUST use microcopy that is direct, inspiring, and welcoming ("sem rodeios"), consistent with the brand tone of voice across all empty states, tooltips, dialogs, and notifications.
- **FR-008**: System MUST update PWA shell assets (`manifest.json` theme/background color to `#181e5f` and `icon.svg` to Onda Blue/wave styling) while preserving full responsive usability and PWA installability across mobile (Android, iOS) and desktop devices without breaking offline functionality.

### Key Entities

- **UI Theme Configuration**: Represents the design system tokens (colors, font families, box shadows, blur filters) mapped to the frontend presentation layer.
- **Brand Component Catalog**: Represents reusable visual presentation patterns (Glass Cards, Action Buttons, Role Badges, Notification Pills, Header with SVG Wordmark, PWA Icon).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of user-facing views (PIN access, main navigation, members roster, member edit/create modals, history view, and feedback toasts) and PWA shell metadata adhere to the brand guidelines and constitutional requirements.
- **SC-002**: 100% of text and background pairings across all glassmorphic and colored surfaces meet or exceed WCAG AA contrast ratios (minimum 4.5:1 for body copy, 3:1 for large titles and icons).
- **SC-003**: The interface displays zero horizontal scrollbars and zero clipped containers across viewport widths from 320px to 2560px.
- **SC-004**: All touch targets on mobile viewports measure at least 44x44 pixels to ensure ergonomic interaction.
- **SC-005**: Zero instances of unmapped arbitrary color codes or prohibited logo variations remain in client stylesheets or templates.

## Assumptions

- Modern browser support includes WebKit, Blink, and Gecko engines that support standard CSS backdrop-filter and flex/grid layout properties.
- Existing business logic, authentication PIN flow, offline caching, and member management APIs remain intact; this specification governs visual presentation, typography, styling tokens, and brand compliance.
- Brand web fonts (Space Grotesk, Right Grotesk, SF Pro Display / fallbacks) will be loaded with sensible system font fallbacks to preserve fast initial page loads under PWA constraints.
- Alternate light theme mode is explicitly out of scope; the application is single-theme Dark Wave by design to maximize brand immersion and maintain architectural simplicity.
