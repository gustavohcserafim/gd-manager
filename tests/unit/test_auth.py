import sqlite3
import pytest
from src.services.database import init_db
from src.services.seed import seed_initial_leaders
from src.services.auth_service import authenticate_pin, verify_session_token, reset_rate_limits

@pytest.fixture(autouse=True)
def clean_rate_limits():
    reset_rate_limits()

def test_authenticate_valid_pin():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_initial_leaders(conn)

    # Valid PIN for Pr. Pedro is 1234
    result = authenticate_pin(conn, "1234", client_ip="127.0.0.1")
    assert result is not None
    assert "token" in result
    assert result["user"]["name"] == "Pr. Pedro"
    assert result["user"]["role"] == "Líder"

    # Verify session token
    user = verify_session_token(result["token"])
    assert user is not None
    assert user["id"] == result["user"]["id"]
    assert user["name"] == "Pr. Pedro"
    assert user["role"] == "Líder"
    conn.close()

def test_authenticate_invalid_pin():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_initial_leaders(conn)

    result = authenticate_pin(conn, "9999", client_ip="127.0.0.1")
    assert result is None
    conn.close()

def test_rate_limit_lockout_after_five_failed_attempts():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_initial_leaders(conn)

    ip = "192.168.1.100"
    for _ in range(5):
        result = authenticate_pin(conn, "0000", client_ip=ip)
        assert result is None

    # 6th attempt should trigger lockout
    with pytest.raises(PermissionError) as exc_info:
        authenticate_pin(conn, "1234", client_ip=ip)
    assert "Muitas tentativas" in str(exc_info.value) or "cooldown" in str(exc_info.value).lower()
    conn.close()
