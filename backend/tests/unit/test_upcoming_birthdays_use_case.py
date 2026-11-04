from datetime import date, timedelta
import pytest
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.application.use_cases.get_upcoming_birthdays_use_case import GetUpcomingBirthdaysUseCase
from backend.tests.unit.test_create_member_use_case import InMemoryMemberRepository


def test_upcoming_birthdays_within_30_days_window():
    today = date.today()
    repo = InMemoryMemberRepository()

    # Membro com aniversário em 5 dias (deve vir)
    bday_5_days = today + timedelta(days=5)
    m1 = Member.create(
        name="Aniversariante Próximo",
        phone="11911110001",
        birth_date=date(1990, bday_5_days.month, bday_5_days.day),
    )

    # Membro com aniversário hoje (deve vir)
    m_today = Member.create(
        name="Aniversariante Hoje",
        phone="11911110002",
        birth_date=date(1992, today.month, today.day),
    )

    # Membro com aniversário em 45 dias (fora da janela)
    bday_45_days = today + timedelta(days=45)
    m_far = Member.create(
        name="Aniversariante Distante",
        phone="11911110003",
        birth_date=date(1985, bday_45_days.month, bday_45_days.day),
    )

    # Membro inativo com aniversário amanhã (não deve vir)
    bday_tomorrow = today + timedelta(days=1)
    m_inactive = Member.create(
        name="Inativo Amanhã",
        phone="11911110004",
        birth_date=date(1988, bday_tomorrow.month, bday_tomorrow.day),
    )
    m_inactive.deactivate()

    repo.create(m1)
    repo.create(m_today)
    repo.create(m_far)
    repo.create(m_inactive)

    use_case = GetUpcomingBirthdaysUseCase(repo)
    results = use_case.execute(days=30)

    # Deve conter m_today (0 dias) e m1 (5 dias) ordenados
    assert len(results) == 2
    assert results[0].id == m_today.id
    assert results[1].id == m1.id
