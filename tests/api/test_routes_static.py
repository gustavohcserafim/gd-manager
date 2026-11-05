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
