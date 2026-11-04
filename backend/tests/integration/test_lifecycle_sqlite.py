from datetime import date
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberStatus
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository


def test_sqlite_deactivate_and_reactivate(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(name="Mariana Lopes", phone="11977770001", birth_date=date(1996, 6, 6))
    repo.create(m)

    # Inativa
    m.deactivate()
    repo.update(m)

    found = repo.find_by_id(m.id)
    assert found.status == MemberStatus.INACTIVE

    # Não deve constar na busca de ativos por telefone
    assert repo.find_active_by_phone("11977770001") is None

    # Reativa
    m.reactivate()
    repo.update(m)

    found_active = repo.find_active_by_phone("11977770001")
    assert found_active is not None
    assert found_active.id == m.id
    assert found_active.status == MemberStatus.ACTIVE
