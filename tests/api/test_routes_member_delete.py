import pytest
from fastapi import HTTPException
from src.domain.models import MemberCreateRequest
from src.api.routes_members import create_member_route, delete_member_route

@pytest.fixture
def current_user():
    return {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

def test_delete_member_route_success(current_user):
    created = create_member_route(
        MemberCreateRequest(
            name="Lucas Silva",
            phone="(11) 98765-4321",
            birthDate="15/03/1998",
            position="Membro"
        ),
        current_user=current_user
    )

    response = delete_member_route(member_id=created["id"], current_user=current_user)
    assert response["deletedId"] == created["id"]
    assert "sucesso" in response["message"].lower()

def test_delete_member_route_not_found(current_user):
    with pytest.raises(HTTPException) as exc_info:
        delete_member_route(member_id=99999, current_user=current_user)

    assert exc_info.value.status_code == 404
