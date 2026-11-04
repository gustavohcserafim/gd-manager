import pytest
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import ValidationException


def test_create_valid_member_defaults():
    member = Member.create(
        name="Carlos Eduardo",
        phone="11999990001",
        email="carlos@exemplo.com",
        role=MemberRole.LEADER,
    )

    assert member.id is not None
    assert member.name == "Carlos Eduardo"
    assert member.phone == "11999990001"
    assert member.email == "carlos@exemplo.com"
    assert member.role == MemberRole.LEADER
    assert member.status == MemberStatus.ACTIVE
    assert member.initials == "CE"
    assert member.created_at is not None
    assert member.updated_at is not None


def test_member_initials_single_and_multiple_names():
    m1 = Member.create(name="Maria", phone="11988880001")
    assert m1.initials == "M"

    m2 = Member.create(name="João Victor dos Santos", phone="11988880002")
    assert m2.initials == "JS"


def test_name_too_short_raises_validation_exception():
    with pytest.raises(ValidationException, match="mínimo 3 caracteres"):
        Member.create(name="Ab", phone="11999990001")


def test_name_empty_or_whitespace_raises_validation_exception():
    with pytest.raises(ValidationException, match="mínimo 3 caracteres"):
        Member.create(name="   ", phone="11999990001")


def test_name_too_long_raises_validation_exception():
    with pytest.raises(ValidationException, match="máximo 150 caracteres"):
        Member.create(name="A" * 151, phone="11999990001")


def test_phone_empty_raises_validation_exception():
    with pytest.raises(ValidationException, match="Telefone é obrigatório"):
        Member.create(name="Carlos Eduardo", phone="   ")


def test_invalid_email_format_raises_validation_exception():
    with pytest.raises(ValidationException, match="E-mail inválido"):
        Member.create(name="Carlos Eduardo", phone="11999990001", email="email_invalido")


def test_valid_optional_email_none():
    member = Member.create(name="Carlos Eduardo", phone="11999990001", email=None)
    assert member.email is None
