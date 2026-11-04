"""Validação ponta a ponta dos 5 cenários descritos em specs/002-member-birthdays/quickstart.md."""
from datetime import date, timedelta
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.application.dtos.create_member_dto import CreateMemberRequest
from src.application.dtos.update_member_dto import UpdateMemberRequest
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import (
    create_member,
    list_members,
    get_member,
    update_member,
    get_upcoming_birthdays,
)


def test_quickstart_birthdays_all_5_scenarios(memory_db):
    repo = SqliteMemberRepository(memory_db)

    # =========================================================================
    # Cenário 1: Cadastro de Membro com Data de Nascimento Válida (P1)
    # =========================================================================
    lucas_payload = CreateMemberRequest(
        name="Lucas Nogueira",
        phone="11988881234",
        role=MemberRole.NORMAL,
        birth_date=date(1995, 5, 15),
    )
    lucas = create_member(lucas_payload, caller_role=MemberRole.LEADER, repo=repo)
    assert lucas.name == "Lucas Nogueira"
    assert lucas.birth_date == date(1995, 5, 15)
    assert lucas.birthday_display == "15 de Maio"
    assert lucas.age is not None
    assert lucas.age >= 30

    # =========================================================================
    # Cenário 2: Bloqueio de Cadastro sem Data ou com Data Futura (P1)
    # =========================================================================
    # 2a. Sem data de nascimento -> Falha de validação obrigatória
    with pytest.raises(ValidationError):
        CreateMemberRequest(
            name="Sem Data",
            phone="11988889999",
            role=MemberRole.NORMAL,  # type: ignore
        )

    # 2b. Com data futura -> Erro 400 Bad Request
    future_date = date.today() + timedelta(days=365)
    future_payload = CreateMemberRequest(
        name="Membro do Futuro",
        phone="11988889998",
        role=MemberRole.NORMAL,
        birth_date=future_date,
    )
    with pytest.raises(HTTPException) as exc_future:
        create_member(future_payload, caller_role=MemberRole.LEADER, repo=repo)
    assert exc_future.value.status_code == 400
    assert "no futuro" in exc_future.value.detail.lower()

    # =========================================================================
    # Cenário 3: Destaque de Próximos Aniversariantes no Topo (P3)
    # =========================================================================
    today = date.today()
    # 3a. Membro com aniversário em 5 dias
    target_5 = today + timedelta(days=5)
    m_5 = create_member(
        CreateMemberRequest(
            name="Membro Cinco Dias",
            phone="11988880005",
            role=MemberRole.NORMAL,
            birth_date=date(1993, target_5.month, target_5.day),
        ),
        caller_role=MemberRole.LEADER,
        repo=repo,
    )

    # 3b. Membro com aniversário em 45 dias
    target_45 = today + timedelta(days=45)
    m_45 = create_member(
        CreateMemberRequest(
            name="Membro Quarenta e Cinco Dias",
            phone="11988880045",
            role=MemberRole.NORMAL,
            birth_date=date(1991, target_45.month, target_45.day),
        ),
        caller_role=MemberRole.LEADER,
        repo=repo,
    )

    # Consulta próximos aniversariantes (janela 30 dias)
    upcoming = get_upcoming_birthdays(days=30, caller_role=MemberRole.NORMAL, repo=repo)
    upcoming_ids = [m.id for m in upcoming]
    assert m_5.id in upcoming_ids
    assert m_45.id not in upcoming_ids

    # Ambos aparecem na listagem geral
    general_list = list_members(caller_role=MemberRole.NORMAL, repo=repo)
    general_ids = [m.id for m in general_list]
    assert m_5.id in general_ids
    assert m_45.id in general_ids

    # =========================================================================
    # Cenário 4: Filtro por Mês de Aniversário (P3)
    # =========================================================================
    # Lucas foi cadastrado no mês 5 (Maio)
    may_members = list_members(birthday_month=5, caller_role=MemberRole.NORMAL, repo=repo)
    assert any(m.id == lucas.id for m in may_members)
    assert all(m.birth_date is not None and m.birth_date.month == 5 for m in may_members)

    # Filtro para mês sem aniversariantes (ex: mês 2 onde ninguém foi cadastrado)
    empty_month = list_members(birthday_month=2, caller_role=MemberRole.NORMAL, repo=repo)
    assert len(empty_month) == 0

    # =========================================================================
    # Cenário 5: Edição de Membro Legado Exigindo Data de Nascimento (P1)
    # =========================================================================
    # Simula membro legado cadastrado diretamente sem birth_date
    with repo.conn:
        repo.conn.execute("""
            INSERT INTO members (id, name, phone, email, role, status, created_at, updated_at, birth_date)
            VALUES ('legacy-id-01', 'Membro Legado Histórico', '11977770000', NULL, 'normal', 'active', '2025-01-01T00:00:00', '2025-01-01T00:00:00', NULL);
        """)

    legacy = get_member(id="legacy-id-01", caller_role=MemberRole.NORMAL, repo=repo)
    assert legacy.id == "legacy-id-01"
    assert legacy.birth_date is None
    assert legacy.age is None
    assert legacy.birthday_display is None

    # Tentar editar sem informar birth_date é bloqueado no DTO
    with pytest.raises(ValidationError):
        UpdateMemberRequest(
            name="Membro Legado Atualizado",
            phone="11977770000",
            role=MemberRole.NORMAL,  # type: ignore (sem birth_date)
        )

    # Atualiza com data de nascimento válida
    update_dto = UpdateMemberRequest(
        name="Membro Legado Atualizado",
        phone="11977770000",
        role=MemberRole.CORE,
        birth_date=date(1989, 7, 22),
    )
    updated = update_member(id="legacy-id-01", payload=update_dto, caller_role=MemberRole.LEADER, repo=repo)
    assert updated.name == "Membro Legado Atualizado"
    assert updated.birth_date == date(1989, 7, 22)
    assert updated.birthday_display == "22 de Julho"
    assert updated.age is not None
    assert updated.age >= 35
