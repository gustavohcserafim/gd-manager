from datetime import date, timedelta
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
        birth_date=date(1990, 1, 1),
    )

    assert member.id is not None
    assert member.name == "Carlos Eduardo"
    assert member.phone == "11999990001"
    assert member.email == "carlos@exemplo.com"
    assert member.role == MemberRole.LEADER
    assert member.status == MemberStatus.ACTIVE
    assert member.initials == "CE"
    assert member.birth_date == date(1990, 1, 1)
    assert member.created_at is not None
    assert member.updated_at is not None


def test_member_initials_single_and_multiple_names():
    m1 = Member.create(name="Maria", phone="11988880001", birth_date=date(1992, 3, 4))
    assert m1.initials == "M"

    m2 = Member.create(name="João Victor dos Santos", phone="11988880002", birth_date=date(1993, 7, 8))
    assert m2.initials == "JS"


def test_name_too_short_raises_validation_exception():
    with pytest.raises(ValidationException, match="mínimo 3 caracteres"):
        Member.create(name="Ab", phone="11999990001", birth_date=date(1990, 1, 1))


def test_name_empty_or_whitespace_raises_validation_exception():
    with pytest.raises(ValidationException, match="mínimo 3 caracteres"):
        Member.create(name="   ", phone="11999990001", birth_date=date(1990, 1, 1))


def test_name_too_long_raises_validation_exception():
    with pytest.raises(ValidationException, match="máximo 150 caracteres"):
        Member.create(name="A" * 151, phone="11999990001", birth_date=date(1990, 1, 1))


def test_phone_empty_raises_validation_exception():
    with pytest.raises(ValidationException, match="Telefone é obrigatório"):
        Member.create(name="Carlos Eduardo", phone="   ", birth_date=date(1990, 1, 1))


def test_invalid_email_format_raises_validation_exception():
    with pytest.raises(ValidationException, match="E-mail inválido"):
        Member.create(name="Carlos Eduardo", phone="11999990001", email="email_invalido", birth_date=date(1990, 1, 1))


def test_valid_optional_email_none():
    member = Member.create(name="Carlos Eduardo", phone="11999990001", email=None, birth_date=date(1995, 5, 15))
    assert member.email is None


def test_create_member_without_birth_date_raises_validation_exception():
    with pytest.raises(ValidationException, match="Data de nascimento é obrigatória"):
        Member.create(name="Carlos Eduardo", phone="11999990001", birth_date=None)  # type: ignore


def test_create_member_future_birth_date_raises_validation_exception():
    future_date = date.today() + timedelta(days=1)
    with pytest.raises(ValidationException, match="não pode ser no futuro"):
        Member.create(name="Carlos Eduardo", phone="11999990001", birth_date=future_date)


def test_create_member_birth_date_before_1900_raises_validation_exception():
    with pytest.raises(ValidationException, match="a partir de 1900"):
        Member.create(name="Carlos Eduardo", phone="11999990001", birth_date=date(1899, 12, 31))


def test_update_member_without_birth_date_raises_validation_exception():
    member = Member.create(name="Carlos Eduardo", phone="11999990001", birth_date=date(1995, 5, 15))
    with pytest.raises(ValidationException, match="Data de nascimento é obrigatória"):
        member.update_info(name="Carlos Atualizado", phone="11999990002", email=None, role=MemberRole.LEADER, birth_date=None)  # type: ignore


def test_reconstitute_legacy_member_with_none_birth_date():
    member = Member.reconstitute(
        id="m-legacy",
        name="Membro Legado",
        phone="11988887777",
        email=None,
        role="normal",
        status="active",
        created_at="2026-01-01T00:00:00",
        updated_at="2026-01-01T00:00:00",
        birth_date=None,
    )
    assert member.birth_date is None
    assert member.birth_date_formatted is None
    assert member.age is None
    assert member.birthday_display is None
    assert member.is_birthday_today is False
    assert member.days_until_birthday is None


def test_member_birthday_display_and_age_calculation():
    # Supondo nascimento em 15 de Maio de 1995
    member = Member.create(
        name="Mariana Alves",
        phone="11988889999",
        role=MemberRole.CORE,
        birth_date=date(1995, 5, 15),
    )
    assert member.birthday_display == "15 de Maio"
    assert member.birth_date_formatted == "15/05/1995"
    today = date.today()
    expected_age = today.year - 1995 - ((today.month, today.day) < (5, 15))
    assert member.age == expected_age


def test_member_is_birthday_today():
    today = date.today()
    member = Member.create(
        name="Aniversariante do Dia",
        phone="11988889998",
        role=MemberRole.NORMAL,
        birth_date=date(1990, today.month, today.day),
    )
    assert member.is_birthday_today is True
    assert member.days_until_birthday == 0


def test_member_leap_year_february_29_in_non_leap_year():
    # Nascido em 29/02/2000 (ano bissexto)
    member = Member.create(
        name="Leap Born",
        phone="11988889997",
        role=MemberRole.NORMAL,
        birth_date=date(2000, 2, 29),
    )
    assert member.birthday_display == "29 de Fevereiro"
    assert member.birth_date == date(2000, 2, 29)


