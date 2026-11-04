from datetime import date
import pytest
from fastapi import HTTPException
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import list_members


def test_list_members_contract_returns_200(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(name="Daniel Rocha", phone="11922223333", role=MemberRole.LEADER, birth_date=date(1990, 7, 10))
    repo.create(m)

    response = list_members(caller_role=MemberRole.NORMAL, repo=repo)
    assert len(response) == 1
    item = response[0]
    assert item.name == "Daniel Rocha"
    assert item.phone == "11922223333"
    assert item.role == MemberRole.LEADER
    assert item.status == MemberStatus.ACTIVE
    assert item.initials == "DR"


def test_list_members_inactive_as_normal_returns_403(memory_db):
    repo = SqliteMemberRepository(memory_db)
    with pytest.raises(HTTPException) as exc_info:
        list_members(status=MemberStatus.INACTIVE, caller_role=MemberRole.NORMAL, repo=repo)
    assert exc_info.value.status_code == 403
