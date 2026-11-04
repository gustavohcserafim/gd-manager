from datetime import date, timedelta
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.application.dtos.create_member_dto import CreateMemberRequest
from src.application.dtos.update_member_dto import UpdateMemberRequest
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import create_member, update_member, list_members, get_upcoming_birthdays


def test_post_member_with_birth_date_contract_201(memory_db):
    repo = SqliteMemberRepository(memory_db)
    payload = CreateMemberRequest(
        name="Mariana Souza",
        phone="11988884444",
        email="mariana@exemplo.com",
        role=MemberRole.NORMAL,
        birth_date=date(1995, 5, 15),
    )
    response = create_member(payload, caller_role=MemberRole.LEADER, repo=repo)

    assert response.name == "Mariana Souza"
    assert response.birth_date == date(1995, 5, 15)
    assert response.birth_date_formatted == "15/05/1995"
    assert response.status == MemberStatus.ACTIVE
    assert response.id is not None

    # Teste de contrato com string DD/MM/AAAA
    payload_br = CreateMemberRequest(
        name="Mariana Souza Formato BR",
        phone="11988884445",
        email="mariana.br@exemplo.com",
        role=MemberRole.NORMAL,
        birth_date="15/05/1995",  # type: ignore[arg-type]
    )
    response_br = create_member(payload_br, caller_role=MemberRole.LEADER, repo=repo)
    assert response_br.birth_date == date(1995, 5, 15)
    assert response_br.birth_date_formatted == "15/05/1995"


def test_post_member_with_future_birth_date_contract_400(memory_db):
    repo = SqliteMemberRepository(memory_db)
    future_date = date.today() + timedelta(days=2)
    payload = CreateMemberRequest(
        name="Mariana Souza",
        phone="11988884444",
        role=MemberRole.NORMAL,
        birth_date=future_date,
    )
    with pytest.raises(HTTPException) as exc_info:
        create_member(payload, caller_role=MemberRole.LEADER, repo=repo)
    assert exc_info.value.status_code == 400
    assert "no futuro" in exc_info.value.detail.lower()


def test_post_member_missing_birth_date_raises_validation_error():
    with pytest.raises(ValidationError):
        CreateMemberRequest(
            name="Mariana Souza",
            phone="11988884444",
            role=MemberRole.NORMAL,  # type: ignore
        )


def test_put_member_with_birth_date_contract_200(memory_db):
    repo = SqliteMemberRepository(memory_db)
    create_payload = CreateMemberRequest(
        name="Mariana Souza",
        phone="11988884444",
        role=MemberRole.NORMAL,
        birth_date=date(1995, 5, 15),
    )
    created = create_member(create_payload, caller_role=MemberRole.LEADER, repo=repo)

    update_payload = UpdateMemberRequest(
        name="Mariana Souza Editada",
        phone="11988884444",
        role=MemberRole.CORE,
        birth_date=date(1995, 5, 20),
    )
    response = update_member(id=created.id, payload=update_payload, caller_role=MemberRole.LEADER, repo=repo)

    assert response.name == "Mariana Souza Editada"
    assert response.birth_date == date(1995, 5, 20)
    assert response.role == MemberRole.CORE


def test_put_member_with_future_birth_date_contract_400(memory_db):
    repo = SqliteMemberRepository(memory_db)
    create_payload = CreateMemberRequest(
        name="Mariana Souza",
        phone="11988884444",
        role=MemberRole.NORMAL,
        birth_date=date(1995, 5, 15),
    )
    created = create_member(create_payload, caller_role=MemberRole.LEADER, repo=repo)

    future_date = date.today() + timedelta(days=2)
    update_payload = UpdateMemberRequest(
        name="Mariana Souza Editada",
        phone="11988884444",
        role=MemberRole.CORE,
        birth_date=future_date,
    )
    with pytest.raises(HTTPException) as exc_info:
        update_member(id=created.id, payload=update_payload, caller_role=MemberRole.LEADER, repo=repo)
    assert exc_info.value.status_code == 400
    assert "no futuro" in exc_info.value.detail.lower()


def test_member_response_includes_birthday_computed_fields(memory_db):
    repo = SqliteMemberRepository(memory_db)
    today = date.today()
    payload = CreateMemberRequest(
        name="Aniversariante Hoje",
        phone="11955551111",
        role=MemberRole.NORMAL,
        birth_date=date(1992, today.month, today.day),
    )
    res = create_member(payload, caller_role=MemberRole.LEADER, repo=repo)

    assert res.is_birthday_today is True
    assert res.days_until_birthday == 0
    assert res.age is not None
    assert res.birthday_display is not None
    assert str(today.day) in res.birthday_display
    assert res.birth_date_formatted == f"{today.day:02d}/{today.month:02d}/1992"


def test_get_upcoming_birthdays_contract_200(memory_db):
    repo = SqliteMemberRepository(memory_db)
    today = date.today()
    tomorrow = today + timedelta(days=1)
    payload = CreateMemberRequest(
        name="Aniversariante Amanhã",
        phone="11955552222",
        role=MemberRole.NORMAL,
        birth_date=date(1990, tomorrow.month, tomorrow.day),
    )
    create_member(payload, caller_role=MemberRole.LEADER, repo=repo)

    results = get_upcoming_birthdays(days=30, caller_role=MemberRole.NORMAL, repo=repo)
    assert len(results) == 1
    assert results[0].name == "Aniversariante Amanhã"


def test_list_members_with_birthday_month_query_param_200(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m1 = CreateMemberRequest(name="Aniversário Maio", phone="11955553333", role=MemberRole.NORMAL, birth_date=date(1990, 5, 10))
    m2 = CreateMemberRequest(name="Aniversário Outubro", phone="11955554444", role=MemberRole.NORMAL, birth_date=date(1991, 10, 10))
    create_member(m1, caller_role=MemberRole.LEADER, repo=repo)
    create_member(m2, caller_role=MemberRole.LEADER, repo=repo)

    res = list_members(birthday_month=5, caller_role=MemberRole.NORMAL, repo=repo)
    assert len(res) == 1
    assert res[0].name == "Aniversário Maio"


