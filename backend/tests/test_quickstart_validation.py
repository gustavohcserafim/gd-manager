"""Validação ponta a ponta dos 6 cenários descritos em specs/001-member-management/quickstart.md."""
from datetime import date
import pytest
from fastapi import HTTPException
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.application.dtos.create_member_dto import CreateMemberRequest
from src.application.dtos.update_member_dto import UpdateMemberRequest
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import (
    create_member,
    list_members,
    get_member,
    update_member,
    deactivate_member,
    reactivate_member,
)


def test_quickstart_all_scenarios(memory_db):
    repo = SqliteMemberRepository(memory_db)

    # =========================================================================
    # Cenário 1: Cadastro de Líder com Sucesso (P1)
    # =========================================================================
    carlos_payload = CreateMemberRequest(
        name="Carlos Eduardo",
        phone="11999990001",
        email="carlos@exemplo.com",
        role=MemberRole.LEADER,
        birth_date=date(1990, 5, 15),
    )
    carlos = create_member(carlos_payload, caller_role=MemberRole.LEADER, repo=repo)
    assert carlos.name == "Carlos Eduardo"
    assert carlos.phone == "11999990001"
    assert carlos.role == MemberRole.LEADER
    assert carlos.status == MemberStatus.ACTIVE
    assert carlos.initials == "CE"

    # =========================================================================
    # Cenário 2: Bloqueio de Telefone Duplicado (Regra de Negócio)
    # =========================================================================
    marcos_payload = CreateMemberRequest(
        name="Marcos Souza",
        phone="11999990001",  # Mesmo número do Carlos
        role=MemberRole.NORMAL,
        birth_date=date(1992, 8, 20),
    )
    with pytest.raises(HTTPException) as exc_info:
        create_member(marcos_payload, caller_role=MemberRole.LEADER, repo=repo)
    assert exc_info.value.status_code == 409
    assert "já está cadastrado para outro membro ativo" in exc_info.value.detail

    # =========================================================================
    # Cenário 3: Consulta, Filtro e Busca (P2)
    # =========================================================================
    # Cadastra mais um membro do núcleo
    create_member(
        CreateMemberRequest(name="Ana Paula", phone="11999990002", role=MemberRole.CORE, birth_date=date(1994, 11, 2)),
        caller_role=MemberRole.LEADER,
        repo=repo,
    )

    # Busca por "Carlos"
    search_res = list_members(search="Carlos", caller_role=MemberRole.NORMAL, repo=repo)
    assert len(search_res) == 1
    assert search_res[0].name == "Carlos Eduardo"

    # Filtro por tipo "Membro do núcleo"
    core_res = list_members(role=MemberRole.CORE, caller_role=MemberRole.NORMAL, repo=repo)
    assert len(core_res) == 1
    assert core_res[0].name == "Ana Paula"

    # =========================================================================
    # Cenário 4: Edição de Membro (P3)
    # =========================================================================
    # Carlos é promovido / alterado para CORE
    carlos_detail = get_member(carlos.id, repo=repo)
    assert carlos_detail.id == carlos.id

    update_payload = UpdateMemberRequest(
        name="Carlos Eduardo da Silva",
        phone="11999990001",
        email="carlos.silva@exemplo.com",
        role=MemberRole.CORE,
        birth_date=date(1990, 5, 15),
    )
    carlos_updated = update_member(carlos.id, update_payload, caller_role=MemberRole.LEADER, repo=repo)
    assert carlos_updated.name == "Carlos Eduardo da Silva"
    assert carlos_updated.role == MemberRole.CORE

    # =========================================================================
    # Cenário 5: Inativação e Reativação (P4)
    # =========================================================================
    # Inativa Carlos
    carlos_inactive = deactivate_member(carlos.id, caller_role=MemberRole.LEADER, repo=repo)
    assert carlos_inactive.status == MemberStatus.INACTIVE

    # Carlos não aparece mais na lista de ativos padrão
    active_members = list_members(status=MemberStatus.ACTIVE, caller_role=MemberRole.LEADER, repo=repo)
    assert not any(m.id == carlos.id for m in active_members)

    # Carlos aparece na lista de inativos (acessível por líder)
    inactive_members = list_members(status=MemberStatus.INACTIVE, caller_role=MemberRole.LEADER, repo=repo)
    assert any(m.id == carlos.id for m in inactive_members)

    # Reativa Carlos
    carlos_reactivated = reactivate_member(carlos.id, caller_role=MemberRole.CORE, repo=repo)
    assert carlos_reactivated.status == MemberStatus.ACTIVE

    # Carlos volta à lista de ativos
    active_after_reactivate = list_members(status=MemberStatus.ACTIVE, caller_role=MemberRole.LEADER, repo=repo)
    assert any(m.id == carlos.id for m in active_after_reactivate)

    # =========================================================================
    # Cenário 6: Controle de Acesso para Perfil Normal (RBAC)
    # =========================================================================
    # Normal tentando cadastrar -> 403
    with pytest.raises(HTTPException) as exc_403_post:
        create_member(
            CreateMemberRequest(name="Tentativa", phone="11988880000", birth_date=date(1990, 1, 1)),
            caller_role=MemberRole.NORMAL,
            repo=repo,
        )
    assert exc_403_post.value.status_code == 403

    # Normal tentando editar -> 403
    with pytest.raises(HTTPException) as exc_403_put:
        update_member(carlos.id, update_payload, caller_role=MemberRole.NORMAL, repo=repo)
    assert exc_403_put.value.status_code == 403

    # Normal tentando inativar -> 403
    with pytest.raises(HTTPException) as exc_403_del:
        deactivate_member(carlos.id, caller_role=MemberRole.NORMAL, repo=repo)
    assert exc_403_del.value.status_code == 403

    # Normal tentando listar inativos -> 403
    with pytest.raises(HTTPException) as exc_403_get_inact:
        list_members(status=MemberStatus.INACTIVE, caller_role=MemberRole.NORMAL, repo=repo)
    assert exc_403_get_inact.value.status_code == 403
