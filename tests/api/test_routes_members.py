import pytest
from fastapi import HTTPException
from src.domain.models import MemberCreateRequest
from src.api.routes_members import create_member_route, list_members_route

@pytest.fixture
def current_user():
    return {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

def test_create_member_route_success(current_user):
    payload = MemberCreateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Membro"
    )

    response = create_member_route(payload, current_user=current_user)
    assert response["id"] is not None
    assert response["name"] == "Lucas Silva"
    assert response["phoneFormatted"] == "(11) 98765-4321"
    assert response["position"] == "Membro"

    # Verify list route
    roster = list_members_route()
    assert len(roster) >= 1
    assert any(m["name"] == "Lucas Silva" for m in roster)

def test_create_member_route_duplicate_phone(current_user):
    payload1 = MemberCreateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Membro"
    )
    create_member_route(payload1, current_user=current_user)

    payload2 = MemberCreateRequest(
        name="Outro Membro",
        phone="11987654321",
        birthDate="20/05/1999",
        position="Membro"
    )
    with pytest.raises(HTTPException) as exc_info:
        create_member_route(payload2, current_user=current_user)

    assert exc_info.value.status_code == 400
    assert "Telefone já cadastrado" in exc_info.value.detail["error"]
