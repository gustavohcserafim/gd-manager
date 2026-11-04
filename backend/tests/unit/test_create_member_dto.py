from datetime import date
import pytest
from pydantic import ValidationError

from src.application.dtos.create_member_dto import CreateMemberRequest, MemberResponse
from src.application.dtos.update_member_dto import UpdateMemberRequest
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus


def test_create_member_request_parses_brazilian_date_format():
    req = CreateMemberRequest(
        name="Carlos Silva",
        phone="11999998888",
        role=MemberRole.NORMAL,
        birth_date="15/05/1990",  # type: ignore[arg-type]
    )
    assert req.birth_date == date(1990, 5, 15)


def test_create_member_request_parses_iso_date_format():
    req = CreateMemberRequest(
        name="Carlos Silva",
        phone="11999998888",
        role=MemberRole.NORMAL,
        birth_date="1990-05-15",  # type: ignore[arg-type]
    )
    assert req.birth_date == date(1990, 5, 15)


def test_create_member_request_rejects_invalid_date_format():
    with pytest.raises(ValidationError) as exc_info:
        CreateMemberRequest(
            name="Carlos Silva",
            phone="11999998888",
            role=MemberRole.NORMAL,
            birth_date="32/01/1990",  # type: ignore[arg-type]
        )
    assert "Data de nascimento inválida" in str(exc_info.value)


def test_update_member_request_parses_brazilian_date_format():
    req = UpdateMemberRequest(
        name="Carlos Silva",
        phone="11999998888",
        role=MemberRole.CORE,
        birth_date="20/10/1988",  # type: ignore[arg-type]
    )
    assert req.birth_date == date(1988, 10, 20)


def test_update_member_request_rejects_invalid_date_format():
    with pytest.raises(ValidationError) as exc_info:
        UpdateMemberRequest(
            name="Carlos Silva",
            phone="11999998888",
            role=MemberRole.CORE,
            birth_date="invalid-date",  # type: ignore[arg-type]
        )
    assert "Data de nascimento inválida" in str(exc_info.value)


def test_member_response_includes_birth_date_formatted():
    member = Member.create(
        name="Lucas Nogueira",
        phone="11988881234",
        birth_date=date(1995, 5, 15),
    )
    response = MemberResponse.from_entity(member)
    assert response.birth_date == date(1995, 5, 15)
    assert response.birth_date_formatted == "15/05/1995"
