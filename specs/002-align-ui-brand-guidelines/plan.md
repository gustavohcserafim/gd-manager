# Implementation Plan: Align UI & Frontend with Brand Guidelines and Constitution

**Branch**: `002-align-ui-brand-guidelines` | **Date**: 2026-11-05 | **Spec**: [specs/002-align-ui-brand-guidelines/spec.md](spec.md)

**Input**: Feature specification from `/specs/002-align-ui-brand-guidelines/spec.md`

## Summary

This plan outlines the complete alignment of GD Manager's frontend and UI with Constitutional Principle V and `igreja_onda_ui_brand_guidelines.md` (Brandbook Oficial 2027). The technical approach establishes an immersive single-theme Dark Wave atmosphere (`#181e5f` → `#11187e` → `#1f2bc8`), injects official design tokens via Tailwind CSS configuration, renders the authentic horizontal vector SVG wordmark `"igreja onda"`, restyles all container elements with glassmorphism (`backdrop-blur`, translucent surfaces, fine white borders, rounded-2xl/3xl), applies Space Grotesk / Right Grotesk typography hierarchy, aligns role badges (Líder, Núcleo, Membro), and rebrands the PWA manifest and app icon.

## Technical Context

**Language/Version**: HTML5, CSS3, Vanilla JavaScript (ES2022), Python 3.12+ (FastAPI static host)

**Primary Dependencies**: Tailwind CSS (via CDN script tag with inline `tailwind.config`), Google Fonts (Space Grotesk), native CSS backdrop-filter

**Storage**: LocalStorage / CacheStorage for PWA client; SQLite for server backend (schema untouched)

**Testing**: Pytest (static and contract routes), cross-device responsive inspection per `quickstart.md`

**Target Platform**: Responsive Progressive Web App (PWA) across mobile (Android Chrome/Firefox, iOS Safari/WebKit) and desktop browsers

**Project Type**: Web Application / PWA Frontend

**Performance Goals**: < 1.0s initial paint, 60fps GPU-composited scrolling across glassmorphic layers, 0 horizontal overflow down to 320px viewport

**Constraints**: Zero npm/Node build dependencies, strict Dark Wave theme only (no light theme toggle), WCAG AA contrast ratio compliance (≥ 4.5:1), offline resilience preserved

**Scale/Scope**: 1 single-page application shell, PIN lock screen, 2 main views (Members, History), 2 modal dialogs (Add/Edit Member), PWA manifest and SVG app icon

## Constitution Check

*GATE: Evaluated before Phase 0 research and re-checked post-Phase 1 design.*

| Principle / Gate | Requirement | Status | Notes |
| :--- | :--- | :---: | :--- |
| **I. Test-Driven Development** | Automated tests must cover static assets and regressions | **PASS** | Tests in `test_routes_static.py` will validate manifest, icons, and static routes. |
| **II. PWA & Multiplatform First** | Single responsive codebase, installable manifest, service worker offline caching | **PASS** | Responsive PWA preserved; manifest and icon upgraded to brand identity. |
| **III. Lean Infrastructure & Cost** | Zero continuous hosting expense, serverless/static assets | **PASS** | No added runtime infrastructure, zero npm dependencies, static CDN execution. |
| **IV. Architectural Simplicity** | YAGNI/KISS, decoupled presentation, clean maintainability | **PASS** | Centralized Tailwind config and CSS utility classes in `app.css`. |
| **V. Design System Compliance** | Full adherence to `igreja_onda_ui_brand_guidelines.md` | **PASS** | Horizontal lowercase logo, Onda Blue palette, glassmorphism, Space/Right Grotesk. |

All gates pass without constitutional violations.

## Project Structure

### Documentation (this feature)

```text
specs/002-align-ui-brand-guidelines/
├── plan.md              # This implementation plan
├── research.md          # Technical decisions and token architecture
├── data-model.md        # UI presentation entities and token specifications
├── quickstart.md        # Step-by-step verification and test guide
├── contracts/           # Component and token contracts
│   ├── design-tokens-contract.json
│   └── component-contracts.md
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
src/static/
├── index.html           # Main SPA layout, Tailwind config injection, SVG wordmark, header
├── css/
│   └── app.css          # Design token variables, glassmorphic utilities (.glass-card, etc.), badge styles
├── icons/
│   └── icon.svg         # Official PWA app icon with Onda Blue gradient and wave emblem
├── js/
│   ├── app.js           # Main app bootstrap, offline banner, install prompt & toasts
│   ├── auth.js          # PIN screen glassmorphic styling
│   ├── members.js       # Members roster, cards, and modal dialogs with brand tokens
│   └── history.js       # Activity log items and pill badges
└── manifest.json        # Updated PWA metadata (theme_color: #181e5f)

tests/api/
└── test_routes_static.py # Static file serving and manifest/icon regression tests
```

**Structure Decision**: The project maintains its lightweight single-project structure serving client assets from `src/static/`. All brand tokens and glassmorphism styling are implemented cleanly inside the existing static bundle without introducing external build step overhead.

## Complexity Tracking

*No constitutional violations or unjustified architectural complexity.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
| :--- | :--- | :--- |
| None | N/A | N/A |
