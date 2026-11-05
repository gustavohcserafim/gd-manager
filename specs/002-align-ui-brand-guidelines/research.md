# Research & Technical Decisions: Align UI & Frontend with Brand Guidelines and Constitution

**Feature**: `002-align-ui-brand-guidelines`
**Date**: 2026-11-05

## Research Topics & Consolidations

### 1. Tailwind CSS Configuration & Token Injection
- **Decision**: Configure Tailwind via the `tailwind.config` JavaScript object preceding the CDN script in `src/static/index.html` (and align CSS variables in `app.css`) using the exact schema specified in Section 6 of `igreja_onda_ui_brand_guidelines.md`.
  - Colors: `onda.blue.900` (`#181e5f`), `onda.blue.800` (`#11187e`), `onda.blue.700` (`#2027a7`), `onda.blue.600` (`#1f2bc8`), `onda.blue.500` (`#2537de`), `onda.blue.light` (`#9cc7e4`), `onda.offwhite` (`#eeeee7`), `onda.dark` (`#161616`), `onda.mint` (`#79caab`), `onda.cream` (`#ffffe6`), `onda.cyan.100` (`#e5f4fe`), `onda.cyan.200` (`#e3f3f7`).
  - Fonts: `sans` (Space Grotesk, sans-serif), `display` (Right Grotesk Compact Black, Space Grotesk, sans-serif), `condensed` (Right Grotesk Tight Dark, Space Grotesk, sans-serif), `system` (SF Pro Display, -apple-system, BlinkMacSystemFont, sans-serif).
  - Shadows: `glass` (`0 8px 32px 0 rgba(0, 0, 0, 0.25)`), `glass-glow` (`0 0 24px rgba(37, 55, 222, 0.35)`).
- **Rationale**: Keeps the architecture simple, zero-build, and immediately maintainable by volunteers without requiring Node.js/npm dependencies, honoring Constitutional Principles III (Lean Infrastructure / Zero Overhead) and IV (Architectural Simplicity).
- **Alternatives Considered**: Full Vite/PostCSS build pipeline (rejected: adds unnecessary compilation steps, dependency vulnerabilities, and build configuration overhead for a lightweight PWA).

### 2. Typography Strategy & Offline Performance
- **Decision**: Load *Space Grotesk* via Google Fonts with `display=swap` and declare robust system fallbacks (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `sans-serif`). For display/impact titles (hours, counts, hero badges), apply uppercase styling with `font-display` falling back to `Arial Black` / `Impact` as defined in the brand guidelines.
- **Rationale**: Assures immediate rendering without layout shift (FOUT/FOIT) and provides reliable, readable offline presentation when the Service Worker operates disconnected from external networks.
- **Alternatives Considered**: Embedding multiple large proprietary WOFF2 font files directly in repository (rejected: increases Git repository footprint and mobile payload size unnecessarily).

### 3. Vector Wordmark Logo & Concentric Waves
- **Decision**: Implement the official horizontal `"igreja onda"` wordmark as an authentic inline vector SVG with exact aspect ratio (1.78X height by 8.53X width), lowercase typography, and the prescribed protective exclusion zone ($1X$). Support section backgrounds with a subtle concentric wave graphic (`opacity: 0.1` to `0.15`).
- **Rationale**: Section 2 of `igreja_onda_ui_brand_guidelines.md` strictly mandates horizontal lowercase SVG format and expressly forbids system font text approximation or stacked layouts in digital interfaces.
- **Alternatives Considered**: Raster PNG or WebP assets (rejected: blurriness on high-DPI retina screens and extra HTTP request overhead).

### 4. Glassmorphism Architecture & Accessibility (WCAG AA)
- **Decision**: Centralize glassmorphism patterns in `src/static/css/app.css` using utility classes (`.glass-card`, `.glass-modal`, `.glass-pill`, `.glass-nav`) with `backdrop-filter: blur(16px)`, `background: rgba(255, 255, 255, 0.08)`, and `border: 1px solid rgba(255, 255, 255, 0.15)`. Add `@supports not (backdrop-filter: blur(1px))` fallbacks with semi-opaque `#11187e` solid styling.
- **Rationale**: Ensures smooth 60fps GPU-composited rendering on mobile devices, graceful degradation for older browsers, and consistent WCAG AA contrast (≥ 4.5:1 for body text, ≥ 3.0:1 for large headers) against deep wave gradients.
- **Alternatives Considered**: Arbitrary inline classes duplicated across JavaScript template literals (rejected: high risk of visual inconsistency and harder maintenance).

### 5. PWA Shell & Metadata Branding
- **Decision**: Update `src/static/manifest.json` (`theme_color: #181e5f`, `background_color: #181e5f`) and redesign `src/static/icons/icon.svg` using the official Onda Blue gradient (`#181e5f` → `#11187e` → `#1f2bc8`) with concentric wave rings.
- **Rationale**: Fulfills user clarification and Constitutional Principle II (PWA First) by providing a cohesive brand experience from the operating system launcher to in-app execution.
- **Alternatives Considered**: Retaining legacy amber app icon (rejected: jarring disconnect between OS icon and in-app blue aesthetic).
