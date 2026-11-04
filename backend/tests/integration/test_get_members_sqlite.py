from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository


def test_sqlite_find_all_with_filters(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m1 = Member.create(name="Beatriz Santos", phone="11911110001", role=MemberRole.LEADER)
    m2 = Member.create(name="Bruno Alves", phone="11911110002", role=MemberRole.NORMAL)
    m3 = Member.create(name="Camila Costa", phone="11911110003", role=MemberRole.CORE)
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
