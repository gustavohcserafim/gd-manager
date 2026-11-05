# Quickstart Validation Guide: Align UI & Frontend with Brand Guidelines

**Feature**: `002-align-ui-brand-guidelines`
**Date**: 2026-11-05

This guide provides step-by-step verification procedures to validate that GD Manager frontend and UI strictly comply with the brand guidelines and constitutional rules.

---

## 1. Prerequisites & Environment Setup

- Python 3.12+ installed.
- Modern web browser (Chrome, Safari, Edge, or Firefox).
- Workspace dependencies installed (`pip install -e .` or active virtualenv with FastAPI & Pytest).

```bash
# Verify Python test suite passes
pytest
```

---

## 2. Launch Local Server

```bash
# Start FastAPI application
python -m uvicorn src.main:app --port 8000 --reload
```

Access the application in your browser at: `http://localhost:8000`

---

## 3. End-to-End Validation Scenarios

### Scenario 1: PIN Access Screen & Dark Wave Atmosphere
1. Open `http://localhost:8000` in a private / incognito browser window.
2. **Verify Visual Atmosphere**:
   - The entire background renders the deep Dark Wave gradient (`#181e5f` → `#11187e` → `#1f2bc8`).
   - The central PIN keypad container displays a glassmorphic surface with visible backdrop blur and a fine translucent border (`border-white/15`).
   - The app title "GD MANAGER" is rendered in uppercase brand typography (`Right Grotesk / font-display`).
   - The keypad buttons have translucent backgrounds with smooth active touch feedback.
3. Enter PIN `1234` to unlock.

### Scenario 2: Brand Identity Header & Navigation
1. Upon unlocking, inspect the top navigation bar.
2. **Verify Brand Assets**:
   - The horizontal `"igreja onda"` wordmark is rendered in lowercase vector SVG (no raster pixels, no stacked text).
   - The wordmark respects clear space margins without clipping.
   - The active tab ("Membros") displays an Onda Blue underline and active state contrast.
   - The role badge for the logged-in leader ("Líder") displays the official Onda Blue styling (see [data-model.md](data-model.md)).

### Scenario 3: Members Roster & Glassmorphic Cards
1. Inspect member roster items.
2. **Verify Card Styling**:
   - Each member card displays a glassmorphic translucent container (`rounded-2xl`, subtle white border, backdrop blur).
   - Status badges for *Líder*, *Núcleo*, and *Membro* use their respective brand tokens (`onda-blue`, `onda-mint`, `onda-cyan`).
   - Click "Novo Membro".
   - The modal dialog opens with a blurred backdrop and translucent glass container.
   - The primary action button is styled in Onda Blue 600 (`#1f2bc8`) with Onda Blue 500 hover transition.

### Scenario 4: PWA Shell & Manifest Verification
1. Inspect `http://localhost:8000/static/manifest.json`.
2. Verify `"theme_color": "#181e5f"` and `"background_color": "#181e5f"`.
3. Open `http://localhost:8000/static/icons/icon.svg` in browser:
   - Icon features the deep wave gradient and concentric wave circles adhering to the Onda brand guidelines.

---

## 4. Automated UI & Static Asset Verification

Run automated tests to verify static route integrity and brand asset availability:

```bash
pytest tests/api/test_routes_static.py
```
Expected output: All static tests pass with code 0.
