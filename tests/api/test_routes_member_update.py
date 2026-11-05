import pytest
from fastapi import HTTPException
from src.domain.models import MemberCreateRequest, MemberUpdateRequest
from src.api.routes_members import create_member_route, update_member_route

@pytest.fixture
def leader_user():
    return {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

@pytest.fixture
def nucleo_user():
    return {"id": 2, "name": "Mariana", "role": "Núcleo"}

def test_update_member_route_success(leader_user, nucleo_user):
    created = create_member_route(
        MemberCreateRequest(
            name="Lucas Silva",
            phone="(11) 98765-4321",
            birthDate="15/03/1998",
            position="Membro"
        ),
        current_user=leader_user
    )

    update_payload = MemberUpdateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Núcleo"
    )

    updated = update_member_route(
        member_id=created["id"],
        payload=update_payload,
        current_user=nucleo_user
    )

    assert updated["id"] == created["id"]
    assert updated["position"] == "Núcleo"
    assert updated["updatedByName"] == "Mariana"

def test_update_member_route_not_found(leader_user):
    with pytest.raises(HTTPException) as exc_info:
        update_member_route(
            member_id=99999,
            payload=MemberUpdateRequest(
                name="Inexistente",
                phone="(11) 98765-4321",
                birthDate="15/03/1998",
                position="Membro"
            ),
            current_user=leader_user
        )
    assert exc_info.value.status_code == 404
