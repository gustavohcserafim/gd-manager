import pytest
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import UnauthorizedRoleException
from src.application.use_cases.get_members_use_case import GetMembersUseCase
from backend.tests.unit.test_create_member_use_case import InMemoryMemberRepository


def test_get_members_returns_all_active_by_default():
    repo = InMemoryMemberRepository()
    m1 = Member.create(name="Carlos Líder", phone="11999990001", role=MemberRole.LEADER)
    m2 = Member.create(name="Maria Núcleo", phone="11999990002", role=MemberRole.CORE)
    repo.create(m1)
    repo.create(m2)

    use_case = GetMembersUseCase(repo)
    members = use_case.execute(caller_role=MemberRole.NORMAL)

    assert len(members) == 2
    assert members[0].name == "Carlos Líder"
    assert members[1].name == "Maria Núcleo"


def test_get_members_filter_inactive_as_normal_raises_unauthorized():
    repo = InMemoryMemberRepository()
    use_case = GetMembersUseCase(repo)

    with pytest.raises(UnauthorizedRoleException):
        use_case.execute(caller_role=MemberRole.NORMAL, status=MemberStatus.INACTIVE)


def test_get_members_filter_by_role_and_search():
    repo = InMemoryMemberRepository()
    m1 = Member.create(name="Ana Maria", phone="11999990001", role=MemberRole.NORMAL)
    m2 = Member.create(name="Lucas Silva", phone="11999990002", role=MemberRole.NORMAL)
    m3 = Member.create(name="Ana Clara", phone="11999990003", role=MemberRole.LEADER)
    repo.create(m1)
    repo.create(m2)
    repo.create(m3)

    use_case = GetMembersUseCase(repo)

    # Filtrar por role normal
    only_normal = use_case.execute(caller_role=MemberRole.LEADER, role=MemberRole.NORMAL)
    assert len(only_normal) == 2

    # Filtrar por busca 'Ana'
    search_ana = use_case.execute(caller_role=MemberRole.LEADER, search="Ana")
    assert len(search_ana) == 2
    assert all("Ana" in m.name for m in search_ana)
