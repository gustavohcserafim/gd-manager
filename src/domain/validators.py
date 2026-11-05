import re
from datetime import datetime
from typing import Tuple, Optional

VALID_POSITIONS = {"Líder", "Núcleo", "Membro"}

# Valid Brazilian area codes (DDDs)
VALID_DDDS = {
    11, 12, 13, 14, 15, 16, 17, 18, 19, # SP
    21, 22, 24, # RJ
    27, 28, # ES
    31, 32, 33, 34, 35, 37, 38, # MG
    41, 42, 43, 44, 45, 46, # PR
    47, 48, 49, # SC
    51, 53, 54, 55, # RS
    61, # DF
    62, 64, # GO
    63, # TO
    65, 66, # MT
    67, # MS
    68, # AC
    69, # RO
    71, 73, 74, 75, 77, # BA
    79, # SE
    81, 87, # PE
    82, # AL
    83, # PB
    84, # RN
    85, 88, # CE
    86, 89, # PI
    91, 93, 94, # PA
    92, 97, # AM
    95, # RR
    96, # AP
    98, 99  # MA
}

def validate_and_format_phone(raw_phone: str) -> Tuple[str, str, str]:
    """
    Validates a Brazilian phone number, returns:
    (clean_digits, formatted_display, whatsapp_url)
    Raises ValueError on invalid numbers.
    """
    digits = re.sub(r"\D", "", raw_phone)

    if len(digits) not in (10, 11):
        raise ValueError("Número de telefone deve conter DDD + 8 ou 9 dígitos.")

    ddd = int(digits[:2])
    if ddd not in VALID_DDDS:
        raise ValueError(f"DDD '{ddd}' inválido para telefonia brasileira.")

    if len(digits) == 11:
        # Mobile: must start with 9 after DDD
        if digits[2] != "9":
            raise ValueError("Celulares brasileiros devem iniciar com o dígito 9 após o DDD.")
        formatted = f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    else:
        # Landline: first digit after DDD usually 2..5
        formatted = f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"

    wa_url = f"https://wa.me/55{digits}"
    return digits, formatted, wa_url

def validate_and_parse_birth_date(raw_date: str) -> Tuple[int, int, Optional[int], str]:
    """
    Validates a PT-BR birthday string ('DD/MM/AAAA' or 'DD/MM').
    Returns (day, month, year, formatted_str).
    Raises ValueError on invalid dates.
    """
    match = re.match(r"^(\d{1,2})/(\d{1,2})(?:/(\d{4}))?$", raw_date.strip())
    if not match:
        raise ValueError("Data de aniversário deve estar no formato DD/MM/AAAA ou DD/MM.")

    day_s, month_s, year_s = match.groups()
    day = int(day_s)
    month = int(month_s)
    year = int(year_s) if year_s else None

    if month < 1 or month > 12:
        raise ValueError("Mês de aniversário deve estar entre 1 e 12.")

    # Calendar sanity checking
    check_year = year if year is not None else 2024  # 2024 is leap year to allow 29/02 if year omitted
    try:
        datetime(year=check_year, month=month, day=day)
    except ValueError:
        raise ValueError(f"Dia {day:02d}/{month:02d} não existe no calendário.")

    current_year = 2026
    if year is not None:
        if year < 1900 or year > current_year:
            raise ValueError(f"Ano de nascimento deve estar entre 1900 e {current_year}.")
        formatted = f"{day:02d}/{month:02d}/{year:04d}"
    else:
        formatted = f"{day:02d}/{month:02d}"

    return day, month, year, formatted

def validate_position(position: str) -> str:
    """Validates position is one of Líder, Núcleo, Membro."""
    pos = position.strip()
    if pos not in VALID_POSITIONS:
        raise ValueError(f"Posição '{position}' inválida. Deve ser Líder, Núcleo ou Membro.")
    return pos
