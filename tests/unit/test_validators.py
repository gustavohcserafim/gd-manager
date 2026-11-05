import pytest
from src.domain.validators import (
    validate_and_format_phone,
    validate_and_parse_birth_date,
    validate_position,
)

def test_validate_and_format_phone_mobile():
    clean, formatted, wa_url = validate_and_format_phone("(11) 98765-4321")
    assert clean == "11987654321"
    assert formatted == "(11) 98765-4321"
    assert wa_url == "https://wa.me/5511987654321"

def test_validate_and_format_phone_landline():
    clean, formatted, wa_url = validate_and_format_phone("1134567890")
    assert clean == "1134567890"
    assert formatted == "(11) 3456-7890"
    assert wa_url == "https://wa.me/551134567890"

def test_validate_and_format_phone_invalid():
    with pytest.raises(ValueError):
        validate_and_format_phone("12345")

    with pytest.raises(ValueError):
        validate_and_format_phone("05987654321")  # Invalid DDD (05)

    with pytest.raises(ValueError):
        validate_and_format_phone("11987654321000")  # Too long

def test_validate_and_parse_birth_date_full():
    day, month, year, formatted = validate_and_parse_birth_date("15/03/1998")
    assert day == 15
    assert month == 3
    assert year == 1998
    assert formatted == "15/03/1998"

def test_validate_and_parse_birth_date_day_month_only():
    day, month, year, formatted = validate_and_parse_birth_date("05/11")
    assert day == 5
    assert month == 11
    assert year is None
    assert formatted == "05/11"

def test_validate_and_parse_birth_date_invalid():
    with pytest.raises(ValueError):
        validate_and_parse_birth_date("31/02/2000")  # Feb 31 does not exist

    with pytest.raises(ValueError):
        validate_and_parse_birth_date("29/02/2023")  # 2023 is not leap year

    with pytest.raises(ValueError):
        validate_and_parse_birth_date("15/13/2000")  # Month 13

    with pytest.raises(ValueError):
        validate_and_parse_birth_date("32/01/2000")  # Day 32

    with pytest.raises(ValueError):
        validate_and_parse_birth_date("invalid-date")

def test_validate_position():
    assert validate_position("Líder") == "Líder"
    assert validate_position("Núcleo") == "Núcleo"
    assert validate_position("Membro") == "Membro"

    with pytest.raises(ValueError):
        validate_position("Outro")
