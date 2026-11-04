import pytest
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import (
    DuplicatePhoneException,
    UnauthorizedRoleException,
    MemberNotFoundException,
)
from src.application.dtos.update_member_dto import UpdateMemberRequest
from src.application.use_cases.update_member_use_case import UpdateMemberUseCase, GetMemberByIdUseCase
from backend.tests.unit.test_create_member_use_case import InMemoryMemberRepository


def test_get_member_by_id_success():
    repo = InMemoryMemberRepository()
    m = Member.create(name="Gustavo Silva", phone="11911112222")
    repo.create(m)

    use_case = GetMemberByIdUseCase(repo)
    found = use_case.execute(m.id)
    assert found.id == m.id
    assert found.name == "Gustavo Silva"


def test_get_member_by_id_not_found():
    repo = InMemoryMemberRepository()
    use_case = GetMemberByIdUseCase(repo)
    with pytest.raises(MemberNotFoundException):
        use_case.execute("id-inexistente")


def test_update_member_success():
    repo = InMemoryMemberRepository()
    m = Member.create(name="Gustavo Silva", phone="11911112222", role=MemberRole.NORMAL)
    repo.create(m)

    use_case = UpdateMemberUseCase(repo)
    dto = UpdateMemberRequest(
        name="Gustavo Dias Silva",
        phone="11911113333",
        email="gustavo@teste.com",
        role=MemberRole.CORE,
    )
    updated = use_case.execute(m.id, dto, caller_role=MemberRole.LEADER)

    assert updated.name == "Gustavo Dias Silva"
    assert updated.phone == "11911113333"
    assert updated.role == MemberRole.CORE


def test_update_member_as_normal_fails_unauthorized():
    repo = InMemoryMemberRepository()
    m = Member.create(name="Gustavo Silva", phone="11911112222")
    repo.create(m)

    use_case = UpdateMemberUseCase(repo)
    dto = UpdateMemberRequest(name="Novo Nome", phone="11911112222", role=MemberRole.NORMAL)
    with pytest.raises(UnauthorizedRoleException):
        use_case.execute(m.id, dto, caller_role=MemberRole.NORMAL)


def test_update_member_duplicate_phone_fails():
    repo = InMemoryMemberRepository()
    m1 = Member.create(name="Membro Um", phone="11911111111")
    m2 = Member.create(name="Membro Dois", phone="11922222222")
    repo.create(m1)
    repo.create(m2)

    use_case = UpdateMemberUseCase(repo)
    # Tenta atualizar m2 com o telefone de m1
    dto = UpdateMemberRequest(name="Membro Dois", phone="11911111111", role=MemberRole.NORMAL)
    with pytest.raises(DuplicatePhoneException):
        use_case.execute(m2.id, dto, caller_role=MemberRole.LEADER)
