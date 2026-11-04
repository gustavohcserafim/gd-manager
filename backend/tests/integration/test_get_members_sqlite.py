from datetime import date
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository


def test_sqlite_find_all_with_filters(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m1 = Member.create(name="Beatriz Santos", phone="11911110001", role=MemberRole.LEADER, birth_date=date(1993, 3, 3))
    m2 = Member.create(name="Bruno Alves", phone="11911110002", role=MemberRole.NORMAL, birth_date=date(1994, 4, 4))
    m3 = Member.create(name="Camila Costa", phone="11911110003", role=MemberRole.CORE, birth_date=date(1995, 5, 5))
    m3.deactivate()

    repo.create(m1)
    repo.create(m2)
    repo.create(m3)

    # Apenas ativos (default)
    actives = repo.find_all(status=MemberStatus.ACTIVE)
    assert len(actives) == 2
    assert actives[0].name == "Beatriz Santos"
    assert actives[1].name == "Bruno Alves"

    # Apenas inativos
    inactives = repo.find_all(status=MemberStatus.INACTIVE)
    assert len(inactives) == 1
    assert inactives[0].name == "Camila Costa"

    # Busca textual case-insensitive
    searched = repo.find_all(search="beatriz")
    assert len(searched) == 1
    assert searched[0].name == "Beatriz Santos"
