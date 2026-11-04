import pytest
from fastapi import HTTPException
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import deactivate_member, reactivate_member


def test_deactivate_contract_200_and_403(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(name="Nelson Piquet", phone="11933332222")
    repo.create(m)

    # 403 para Normal
    with pytest.raises(HTTPException) as exc_info:
        deactivate_member(id=m.id, caller_role=MemberRole.NORMAL, repo=repo)
    assert exc_info.value.status_code == 403

    # 200 para Líder
    res = deactivate_member(id=m.id, caller_role=MemberRole.LEADER, repo=repo)
    assert res.status == MemberStatus.INACTIVE


def test_reactivate_contract_200_and_409(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m1 = Member.create(name="Nelson Piquet", phone="11933332222")
    m1.deactivate()
    repo.create(m1)

    # 200 reativação simples
    res = reactivate_member(id=m1.id, caller_role=MemberRole.LEADER, repo=repo)
    assert res.status == MemberStatus.ACTIVE

    # Inativa novamente
    m1.deactivate()
    repo.update(m1)

    # Cadastra outro com mesmo telefone
    m2 = Member.create(name="Outro Nelson", phone="11933332222")
    repo.create(m2)

    # 409 ao tentar reativar m1 com colisão de telefone
    with pytest.raises(HTTPException) as exc_info:
        reactivate_member(id=m1.id, caller_role=MemberRole.CORE, repo=repo)
    assert exc_info.value.status_code == 409
