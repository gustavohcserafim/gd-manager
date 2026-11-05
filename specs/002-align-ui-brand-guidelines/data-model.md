# Data & UI Component Models: Align UI & Frontend with Brand Guidelines

**Feature**: `002-align-ui-brand-guidelines`
**Date**: 2026-11-05

## UI Presentation Entities & Schemas

### 1. DesignSystemTokens
Represents the core token values mapped into Tailwind CSS and CSS Custom Properties.

| Token Property | Token Name | Value | Purpose / Usage |
| :--- | :--- | :--- | :--- |
| `color.onda.blue.900` | `--color-onda-blue-900` | `#181e5f` | Deep dark wave background, gradient origin |
| `color.onda.blue.800` | `--color-onda-blue-800` | `#11187e` | Card backdrop layer, navigation surface base |
| `color.onda.blue.700` | `--color-onda-blue-700` | `#2027a7` | Focus states, intermediate gradients |
| `color.onda.blue.600` | `--color-onda-blue-600` | `#1f2bc8` | **Official Primary**: Buttons, CTAs, active tab |
| `color.onda.blue.500` | `--color-onda-blue-500` | `#2537de` | Electric blue hover states, dynamic glows |
| `color.onda.blue.light` | `--color-onda-blue-light` | `#9cc7e4` | Secondary text, subtle icons on blue cards |
| `color.onda.offwhite` | `--color-onda-offwhite` | `#eeeee7` | Primary high-contrast text on dark backgrounds |
| `color.onda.dark` | `--color-onda-dark` | `#161616` | Charcoal base for deep contrast accents |
| `color.onda.mint` | `--color-onda-accent-mint` | `#79caab` | Positive status badges, confirmation pills |
| `color.onda.cream` | `--color-onda-accent-cream` | `#ffffe6` | Subtle highlights, accent glows |
| `color.onda.cyan.100` | `--color-onda-cyan-100` | `#e5f4fe` | Subtle badge backgrounds, container tints |
| `color.onda.cyan.200` | `--color-onda-cyan-200` | `#e3f3f7` | Glassmorphic clear surfaces |
| `font.sans` | `--font-sans` | Space Grotesk, sans-serif | Body text, labels, input fields, descriptions |
| `font.display` | `--font-display` | Right Grotesk Compact Black | UPPERCASE impact headings, hero stats, hours |
| `font.condensed` | `--font-condensed` | Right Grotesk Tight Dark | UPPERCASE condensed headlines, compact banners |
| `font.system` | `--font-system` | SF Pro Display, sans-serif | Microcopy, timestamps, small tags, footnotes |
| `shadow.glass` | `--shadow-glass` | `0 8px 32px 0 rgba(0, 0, 0, 0.25)` | Glassmorphic elevation |
| `shadow.glass-glow`| `--shadow-glass-glow` | `0 0 24px rgba(37, 55, 222, 0.35)` | Interactive glow on focus/hover |

---

### 2. WordmarkLogoSpec
Defines the technical attributes of the official vector wordmark in digital interfaces.

```typescript
interface WordmarkLogoSpec {
  format: "svg";                  // Strictly SVG vector format
  variant: "horizontal";          // Horizontal wordmark only (stacked strictly prohibited)
  case: "lowercase";              // Always "igreja onda"
  aspectRatio: {
    heightProportion: 1.78;       // 1.78X
    widthProportion: 8.53;        // 8.53X
  };
  protectionPadding: "1X";        // Minimum clear space equal to logo x-height on all 4 sides
  color: "#eeeee7" | "#ffffff";   // High-contrast offwhite/white against dark wave background
  viewBox: "0 0 256 54";          // Scalable vector canvas
}
```

---

### 3. GlassmorphicSurfaceSpec
Defines the parameters for all glassmorphic containers in the interface.

```typescript
interface GlassmorphicSurfaceSpec {
  type: "card" | "modal" | "pill" | "navbar" | "keypad";
  translucency: number;           // 0.08 to 0.30 background opacity
  backdropBlur: "12px" | "16px" | "24px";
  borderWidth: "1px";
  borderColor: "rgba(255, 255, 255, 0.15)" | "rgba(156, 199, 228, 0.20)";
  borderRadius: "1rem" | "1.5rem" | "9999px"; // rounded-2xl, rounded-3xl, or rounded-full
  boxShadow: string;              // shadow-glass or shadow-glass-glow
  fallbackBackground: "#11187e";  // Solid opaque fallback when backdrop-filter unsupported
}
```

---

### 4. RoleBadgeSpec
Defines the presentation of member and user roles adhering to brand colors.

| Role Identifier | Label | Background Color | Text Color | Border Color |
| :--- | :--- | :--- | :--- | :--- |
| `lider` | LÍDER | `rgba(31, 43, 200, 0.35)` | `#9cc7e4` | `rgba(37, 55, 222, 0.60)` |
| `nucleo` | NÚCLEO | `rgba(121, 202, 171, 0.25)` | `#79caab` | `rgba(121, 202, 171, 0.50)` |
| `membro` | MEMBRO | `rgba(227, 243, 247, 0.15)` | `#e5f4fe` | `rgba(255, 255, 255, 0.25)` |

---

### 5. PWAShellConfig
Defines the brand assets for the PWA shell.

- `theme_color`: `#181e5f`
- `background_color`: `#181e5f`
- `display`: `standalone`
- `icon_path`: `/static/icons/icon.svg`
- `icon_spec`: 512x512 SVG with deep wave gradient background (`#181e5f` to `#11187e`), outer concentric wave circle in `#1f2bc8`, and disciple community core emblem.
