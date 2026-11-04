from datetime import date, timedelta
import pytest
from typing import Optional, List
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import DuplicatePhoneException, UnauthorizedRoleException, ValidationException
from src.domain.ports.member_repository import MemberRepository
from src.application.dtos.create_member_dto import CreateMemberRequest
from src.application.use_cases.create_member_use_case import CreateMemberUseCase


class InMemoryMemberRepository(MemberRepository):
    def __init__(self):
        self.members: List[Member] = []

    def create(self, member: Member) -> Member:
        self.members.append(member)
        return member

    def find_active_by_phone(self, phone: str) -> Optional[Member]:
        for m in self.members:
            if m.status == MemberStatus.ACTIVE and m.phone == phone:
                return m
        return None

    def find_by_id(self, member_id: str) -> Optional[Member]:
        for m in self.members:
            if m.id == member_id:
                return m
        return None

    def find_all(
        self,
        status: Optional[MemberStatus] = None,
        role: Optional[MemberRole] = None,
        search: Optional[str] = None,
        birthday_month: Optional[int] = None,
    ) -> List[Member]:
        result = self.members
        if status:
            result = [m for m in result if m.status == status]
        if role:
            result = [m for m in result if m.role == role]
        if search:
            result = [m for m in result if search.lower() in m.name.lower()]
        if birthday_month is not None:
            result = [m for m in result if m.birth_date is not None and m.birth_date.month == birthday_month]
        return result

    def find_upcoming_birthdays(self, days: int = 30) -> List[Member]:
        active_with_bday = [m for m in self.members if m.status == MemberStatus.ACTIVE and m.birth_date is not None]
        candidates = []
        for m in active_with_bday:
            rem = m.days_until_birthday
            if rem is not None and 0 <= rem <= days:
                candidates.append((rem, m))
        candidates.sort(key=lambda x: x[0])
        return [m for _, m in candidates]

    def find_by_birthday_month(self, month: int) -> List[Member]:
        return [m for m in self.members if m.status == MemberStatus.ACTIVE and m.birth_date is not None and m.birth_date.month == month]

    def update(self, member: Member) -> Member:
        for idx, m in enumerate(self.members):
            if m.id == member.id:
                self.members[idx] = member
                return member
        return member


def test_create_member_as_leader_success():
    repo = InMemoryMemberRepository()
    use_case = CreateMemberUseCase(repo)
    dto = CreateMemberRequest(
        name="Ana Paula",
        phone="11987654321",
        email="ana@exemplo.com",
        role=MemberRole.LEADER,
        birth_date=date(1990, 5, 20),
    )

    response = use_case.execute(dto, caller_role=MemberRole.LEADER)

    assert response.id is not None
    assert response.name == "Ana Paula"
    assert response.phone == "11987654321"
    assert response.role == MemberRole.LEADER
    assert response.status == MemberStatus.ACTIVE
    assert response.initials == "AP"
    assert response.birth_date == date(1990, 5, 20)


def test_create_member_as_normal_fails_unauthorized():
    repo = InMemoryMemberRepository()
    use_case = CreateMemberUseCase(repo)
    dto = CreateMemberRequest(name="Ana Paula", phone="11987654321", birth_date=date(1990, 5, 20))

    with pytest.raises(UnauthorizedRoleException):
        use_case.execute(dto, caller_role=MemberRole.NORMAL)


def test_create_member_duplicate_phone_fails():
    repo = InMemoryMemberRepository()
    use_case = CreateMemberUseCase(repo)
    dto1 = CreateMemberRequest(name="Ana Paula", phone="11987654321", birth_date=date(1990, 5, 20))
    use_case.execute(dto1, caller_role=MemberRole.LEADER)

    dto2 = CreateMemberRequest(name="Marcos Silva", phone="11987654321", birth_date=date(1985, 3, 10))
    with pytest.raises(DuplicatePhoneException):
        use_case.execute(dto2, caller_role=MemberRole.CORE)


def test_create_member_rejects_future_birth_date():
    repo = InMemoryMemberRepository()
    use_case = CreateMemberUseCase(repo)
    future_date = date.today() + timedelta(days=2)
    dto = CreateMemberRequest(name="Futuro Membro", phone="11988887777", birth_date=future_date)
    with pytest.raises(ValidationException, match="não pode ser no futuro"):
        use_case.execute(dto, caller_role=MemberRole.LEADER)


def test_create_member_rejects_birth_date_before_1900():
    repo = InMemoryMemberRepository()
    use_case = CreateMemberUseCase(repo)
    dto = CreateMemberRequest(name="Membro Centenário", phone="11988887777", birth_date=date(1899, 1, 1))
    with pytest.raises(ValidationException, match="a partir de 1900"):
        use_case.execute(dto, caller_role=MemberRole.LEADER)
