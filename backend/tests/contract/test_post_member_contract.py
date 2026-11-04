import pytest
from fastapi import HTTPException
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.application.dtos.create_member_dto import CreateMemberRequest
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import create_member


def test_post_member_success_returns_201_and_schema(memory_db):
    repo = SqliteMemberRepository(memory_db)
    payload = CreateMemberRequest(
        name="Ana Paula Silva",
        phone="11987654321",
        email="ana.silva@exemplo.com",
        role=MemberRole.LEADER,
    )
    response = create_member(payload, caller_role=MemberRole.LEADER, repo=repo)

    assert response.name == "Ana Paula Silva"
    assert response.phone == "11987654321"
    assert response.role == MemberRole.LEADER
    assert response.status == MemberStatus.ACTIVE
    assert response.initials == "AS"
    assert response.id is not None
    assert response.created_at is not None
    assert response.updated_at is not None


def test_post_member_as_normal_returns_403_forbidden(memory_db):
    repo = SqliteMemberRepository(memory_db)
    payload = CreateMemberRequest(
        name="Ana Paula Silva",
        phone="11987654321",
        role=MemberRole.NORMAL,
    )
    with pytest.raises(HTTPException) as exc_info:
        create_member(payload, caller_role=MemberRole.NORMAL, repo=repo)
    assert exc_info.value.status_code == 403


def test_post_member_duplicate_phone_returns_409_conflict(memory_db):
    repo = SqliteMemberRepository(memory_db)
    payload1 = CreateMemberRequest(
        name="Carlos Eduardo",
        phone="11999990001",
        role=MemberRole.LEADER,
    )
    create_member(payload1, caller_role=MemberRole.LEADER, repo=repo)

    payload2 = CreateMemberRequest(
        name="Outro Carlos",
        phone="11999990001",
        role=MemberRole.NORMAL,
    )
    with pytest.raises(HTTPException) as exc_info:
        create_member(payload2, caller_role=MemberRole.CORE, repo=repo)
    assert exc_info.value.status_code == 409
    assert "já está cadastrado" in exc_info.value.detail
