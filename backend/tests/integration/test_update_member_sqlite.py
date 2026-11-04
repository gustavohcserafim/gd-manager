from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository


def test_sqlite_update_member(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(name="Original Name", phone="11955556666", role=MemberRole.NORMAL)
    repo.create(m)

    m.update_info(
        name="Updated Name",
        phone="11955557777",
        email="updated@teste.com",
        role=MemberRole.LEADER,
    )
    repo.update(m)

    found = repo.find_by_id(m.id)
    assert found is not None
    assert found.name == "Updated Name"
    assert found.phone == "11955557777"
    assert found.email == "updated@teste.com"
    assert found.role == MemberRole.LEADER
