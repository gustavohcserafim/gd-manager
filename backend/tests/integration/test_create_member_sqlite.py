import pytest
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import DuplicatePhoneException
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository


def test_sqlite_create_and_find_member(memory_db):
    repo = SqliteMemberRepository(memory_db)
    member = Member.create(
        name="Carlos Silva",
        phone="11988887777",
        email="carlos@teste.com",
        role=MemberRole.CORE,
    )

    saved = repo.create(member)
    assert saved.id == member.id

    found = repo.find_active_by_phone("11988887777")
    assert found is not None
    assert found.id == member.id
    assert found.name == "Carlos Silva"
    assert found.role == MemberRole.CORE
    assert found.status == MemberStatus.ACTIVE


def test_sqlite_duplicate_active_phone_raises_duplicate_phone_exception(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m1 = Member.create(name="Membro Um", phone="11911112222")
    repo.create(m1)

    m2 = Member.create(name="Membro Dois", phone="11911112222")
    with pytest.raises(DuplicatePhoneException):
        repo.create(m2)
