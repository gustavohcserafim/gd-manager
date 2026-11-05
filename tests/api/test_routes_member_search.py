import pytest
from src.domain.models import MemberCreateRequest
from src.api.routes_members import create_member_route, list_members_route

@pytest.fixture
def leader_user():
    return {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

def test_routes_member_search_and_filter(leader_user):
    create_member_route(
        MemberCreateRequest(name="Cláudio Ramos", phone="(11) 97777-1111", birthDate="10/10/1985", position="Líder"),
        current_user=leader_user
    )
    create_member_route(
        MemberCreateRequest(name="Beatriz Lima", phone="(11) 97777-2222", birthDate="12/12/1990", position="Membro"),
        current_user=leader_user
    )

    # Search 'claudio' matches 'Cláudio Ramos'
    res_search = list_members_route(search="claudio")
    assert len(res_search) == 1
    assert res_search[0]["name"] == "Cláudio Ramos"

    # Filter 'Membro' matches 'Beatriz Lima'
    res_filter = list_members_route(position="Membro")
    assert any(m["name"] == "Beatriz Lima" for m in res_filter)
    assert not any(m["name"] == "Cláudio Ramos" for m in res_filter)
