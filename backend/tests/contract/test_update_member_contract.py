from datetime import date
import pytest
from fastapi import HTTPException
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole
from src.application.dtos.update_member_dto import UpdateMemberRequest
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import get_member, update_member


def test_get_member_contract_200_and_404(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(name="Helena Castro", phone="11977778888", birth_date=date(1991, 5, 10))
    repo.create(m)

    res = get_member(id=m.id, repo=repo)
    assert res.id == m.id
    assert res.name == "Helena Castro"

    with pytest.raises(HTTPException) as exc_info:
        get_member(id="non-existent", repo=repo)
    assert exc_info.value.status_code == 404


def test_update_member_contract_200_and_403(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(name="Igor Mendes", phone="11988889999", role=MemberRole.NORMAL, birth_date=date(1992, 6, 12))
    repo.create(m)

    # 403 quando Normal tenta editar
    update_dto = UpdateMemberRequest(name="Igor Mendes Editado", phone="11988889999", role=MemberRole.NORMAL, birth_date=date(1992, 6, 12))
    with pytest.raises(HTTPException) as exc_info:
        update_member(id=m.id, payload=update_dto, caller_role=MemberRole.NORMAL, repo=repo)
    assert exc_info.value.status_code == 403

    # 200 quando Líder edita
    res = update_member(id=m.id, payload=update_dto, caller_role=MemberRole.LEADER, repo=repo)
    assert res.name == "Igor Mendes Editado"
