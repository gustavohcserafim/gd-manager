import json
from pathlib import Path
from src.main import serve_index, serve_sw, serve_manifest, health_check


def test_health_check_endpoint():
    res = health_check()
    assert res == {"status": "ok", "app": "GD Manager"}


def test_serve_index():
    res = serve_index()
    # Should return FileResponse
    assert hasattr(res, "path")
    assert "index.html" in str(res.path)


def test_serve_sw():
    res = serve_sw()
    assert hasattr(res, "path")
    assert "sw.js" in str(res.path)
    assert res.headers.get("Service-Worker-Allowed") == "/"


def test_serve_manifest():
    res = serve_manifest()
    assert hasattr(res, "path")
    assert "manifest.json" in str(res.path)


# --- TDD Tests for US1, US2, US3 (Brand Guidelines & Constitution Alignment) ---

def test_pwa_manifest_and_icon_branding():
    """T007: Assert PWA manifest defines Onda Blue #181e5f and icon.svg has Onda palette."""
    manifest_path = Path("src/static/manifest.json")
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data.get("theme_color") == "#181e5f"
    assert data.get("background_color") == "#181e5f"

    icon_path = Path("src/static/icons/icon.svg")
    assert icon_path.exists()
    icon_content = icon_path.read_text(encoding="utf-8")
    assert "#181e5f" in icon_content
    assert "#1f2bc8" in icon_content


def test_index_serves_horizontal_lowercase_wordmark_and_dark_wave():
    """T008: Assert index.html serves horizontal lowercase 'igreja onda' SVG logo and dark wave gradient."""
    html_path = Path("src/static/index.html")
    assert html_path.exists()
    content = html_path.read_text(encoding="utf-8")
    # Must have authentic horizontal lowercase wordmark text or aria-label
    assert "igreja onda" in content
    # Must use dark wave / onda-blue palette classes, not legacy slate-900 / amber
    assert "onda-blue-900" in content
    assert "bg-slate-900" not in content


def test_role_badges_and_glassmorphism_css():
    """T011: Assert role badge CSS classes and glassmorphic utilities exist in app.css."""
    css_path = Path("src/static/css/app.css")
    assert css_path.exists()
    content = css_path.read_text(encoding="utf-8")
    assert ".glass-card" in content
    assert ".glass-modal" in content
    assert ".glass-pill" in content
    assert "--color-onda-blue-600" in content
    # Mint token used for nucleo
    assert "#79caab" in content
    # Blue token used for lider
    assert "#9cc7e4" in content or "rgba(31, 43, 200" in content


def test_offline_banner_and_toast_pill_styling():
    """T015: Assert offline banner and notifications use glassmorphism pill styling without amber."""
    html_path = Path("src/static/index.html")
    assert html_path.exists()
    content = html_path.read_text(encoding="utf-8")
    # Offline banner must not use legacy amber-600
    assert "bg-amber-600" not in content
    # Must use glassmorphism pill / rounded-full or rounded-2xl
    assert "rounded-full" in content or "rounded-2xl" in content or "glass-pill" in content
