import pytest
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import (
    DuplicatePhoneException,
    UnauthorizedRoleException,
    MemberNotFoundException,
)
from src.application.use_cases.lifecycle_use_cases import DeactivateMemberUseCase, ReactivateMemberUseCase
from backend.tests.unit.test_create_member_use_case import InMemoryMemberRepository


def test_deactivate_member_success():
    repo = InMemoryMemberRepository()
    m = Member.create(name="Lucas Ferreira", phone="11912345678")
    repo.create(m)

    use_case = DeactivateMemberUseCase(repo)
    result = use_case.execute(m.id, caller_role=MemberRole.LEADER)

    assert result.status == MemberStatus.INACTIVE


def test_deactivate_member_as_normal_fails_unauthorized():
    repo = InMemoryMemberRepository()
    m = Member.create(name="Lucas Ferreira", phone="11912345678")
    repo.create(m)

    use_case = DeactivateMemberUseCase(repo)
    with pytest.raises(UnauthorizedRoleException):
        use_case.execute(m.id, caller_role=MemberRole.NORMAL)


def test_reactivate_member_success():
    repo = InMemoryMemberRepository()
    m = Member.create(name="Lucas Ferreira", phone="11912345678")
    m.deactivate()
    repo.create(m)

    use_case = ReactivateMemberUseCase(repo)
    result = use_case.execute(m.id, caller_role=MemberRole.CORE)

    assert result.status == MemberStatus.ACTIVE


def test_reactivate_member_phone_conflict_fails():
    repo = InMemoryMemberRepository()
    # Membro 1 foi inativado
    m1 = Member.create(name="Lucas Ferreira", phone="11912345678")
    m1.deactivate()
    repo.create(m1)

    # Membro 2 foi cadastrado ativo com o mesmo telefone
    m2 = Member.create(name="Novo Titular Telefone", phone="11912345678")
    repo.create(m2)

    use_case = ReactivateMemberUseCase(repo)
    with pytest.raises(DuplicatePhoneException):
        use_case.execute(m1.id, caller_role=MemberRole.LEADER)
