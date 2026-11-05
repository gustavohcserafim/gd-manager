import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.services.auth_service import reset_rate_limits
from src.api.routes_auth import login_with_pin, get_current_user
from src.domain.models import PinLoginRequest

@pytest.fixture(autouse=True)
def clean_rate_limits_fixture():
    reset_rate_limits()

def test_api_auth_pin_success():
    req = MagicMock()
    req.client.host = "127.0.0.1"
    response = login_with_pin(PinLoginRequest(pin="1234"), req)

    assert "token" in response
    assert response["user"]["name"] == "Pr. Pedro"
    assert response["user"]["role"] == "Líder"

    # Test dependency get_current_user with generated token
    auth_header = f"Bearer {response['token']}"
    current_user = get_current_user(authorization=auth_header)
    assert current_user["name"] == "Pr. Pedro"
    assert current_user["role"] == "Líder"

def test_api_auth_pin_invalid():
    req = MagicMock()
    req.client.host = "127.0.0.1"
    with pytest.raises(HTTPException) as exc_info:
        login_with_pin(PinLoginRequest(pin="9999"), req)

    assert exc_info.value.status_code == 401
    assert "PIN inválido" in exc_info.value.detail["error"]

def test_api_auth_pin_rate_limiting():
    req = MagicMock()
    req.client.host = "192.168.1.50"
    for _ in range(5):
        with pytest.raises(HTTPException):
            login_with_pin(PinLoginRequest(pin="0000"), req)

    with pytest.raises(HTTPException) as exc_info:
        login_with_pin(PinLoginRequest(pin="1234"), req)

    assert exc_info.value.status_code == 429
    assert "Muitas tentativas" in exc_info.value.detail["error"]
