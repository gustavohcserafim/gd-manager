import re
import uuid
from datetime import date, datetime, timezone
from typing import Optional
from dataclasses import dataclass

from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import ValidationException


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MONTHS_PT = [
    "",
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


@dataclass
class Member:
    """Entidade central pura de domínio representando um integrante do GD Manager."""
    id: str
    name: str
    phone: str
    email: Optional[str]
    role: MemberRole
    status: MemberStatus
    created_at: datetime
    updated_at: datetime
    birth_date: Optional[date] = None

    @classmethod
    def create(
        cls,
        name: str,
        phone: str,
        birth_date: date,
        email: Optional[str] = None,
        role: MemberRole = MemberRole.NORMAL,
    ) -> "Member":
        clean_name = (name or "").strip()
        clean_phone = (phone or "").strip()
        clean_email = email.strip() if email else None

        # Validações invariantes
        if len(clean_name) < 3 or len(clean_name) > 150:
            raise ValidationException("O nome do membro deve conter no mínimo 3 caracteres e no máximo 150 caracteres.")

        if not clean_phone:
            raise ValidationException("Telefone é obrigatório.")

        if clean_email and not EMAIL_REGEX.match(clean_email):
            raise ValidationException(f"E-mail inválido: '{clean_email}'.")

        if birth_date is None:
            raise ValidationException("Data de nascimento é obrigatória.")

        today = date.today()
        if birth_date > today:
            raise ValidationException("Data de nascimento não pode ser no futuro.")

        if birth_date.year < 1900:
            raise ValidationException("Ano de nascimento deve ser a partir de 1900.")

        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid.uuid4()),
            name=clean_name,
            phone=clean_phone,
            email=clean_email,
            role=role,
            status=MemberStatus.ACTIVE,
            created_at=now,
            updated_at=now,
            birth_date=birth_date,
        )

    @classmethod
    def reconstitute(
        cls,
        id: str,
        name: str,
        phone: str,
        email: Optional[str],
        role: str,
        status: str,
        created_at: str,
        updated_at: str,
        birth_date: Optional[str] = None,
    ) -> "Member":
        parsed_birth_date: Optional[date] = None
        if birth_date:
            try:
                parsed_birth_date = date.fromisoformat(birth_date[:10])
            except ValueError:
                parsed_birth_date = None

        return cls(
            id=id,
            name=name,
            phone=phone,
            email=email,
            role=MemberRole.from_str(role),
            status=MemberStatus.from_str(status),
            created_at=datetime.fromisoformat(created_at),
            updated_at=datetime.fromisoformat(updated_at),
            birth_date=parsed_birth_date,
        )

    @property
    def initials(self) -> str:
        parts = [p for p in self.name.strip().split() if p]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def age(self) -> Optional[int]:
        if self.birth_date is None:
            return None
        today = date.today()
        calculated = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        return max(0, calculated)

    @property
    def birthday_display(self) -> Optional[str]:
        if self.birth_date is None:
            return None
        return f"{self.birth_date.day} de {MONTHS_PT[self.birth_date.month]}"

    @property
    def is_birthday_today(self) -> bool:
        if self.birth_date is None:
            return False
        today = date.today()
        # Tratamento especial de 29 de Fevereiro em anos não bissextos
        if self.birth_date.month == 2 and self.birth_date.day == 29:
            is_leap = (today.year % 4 == 0 and today.year % 100 != 0) or (today.year % 400 == 0)
            if not is_leap:
                return today.month == 2 and today.day == 28
        return today.month == self.birth_date.month and today.day == self.birth_date.day

    @property
    def days_until_birthday(self) -> Optional[int]:
        if self.birth_date is None:
            return None
        today = date.today()
        target_year = today.year
        b_month = self.birth_date.month
        b_day = self.birth_date.day

        def _resolve_date(y: int, m: int, d: int) -> date:
            try:
                return date(y, m, d)
            except ValueError:
                return date(y, m, d - 1)

        next_bday = _resolve_date(target_year, b_month, b_day)
        if next_bday < today:
            next_bday = _resolve_date(target_year + 1, b_month, b_day)

        return (next_bday - today).days

    def update_info(
        self,
        name: str,
        phone: str,
        email: Optional[str],
        role: MemberRole,
        birth_date: date,
    ) -> None:
        clean_name = (name or "").strip()
        clean_phone = (phone or "").strip()
        clean_email = email.strip() if email else None

        if len(clean_name) < 3 or len(clean_name) > 150:
            raise ValidationException("O nome do membro deve conter no mínimo 3 caracteres e no máximo 150 caracteres.")
        if not clean_phone:
            raise ValidationException("Telefone é obrigatório.")
        if clean_email and not EMAIL_REGEX.match(clean_email):
            raise ValidationException(f"E-mail inválido: '{clean_email}'.")

        if birth_date is None:
            raise ValidationException("Data de nascimento é obrigatória.")

        today = date.today()
        if birth_date > today:
            raise ValidationException("Data de nascimento não pode ser no futuro.")

        if birth_date.year < 1900:
            raise ValidationException("Ano de nascimento deve ser a partir de 1900.")

        self.name = clean_name
        self.phone = clean_phone
        self.email = clean_email
        self.role = role
        self.birth_date = birth_date
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        self.status = MemberStatus.INACTIVE
        self.updated_at = datetime.now(timezone.utc)

    def reactivate(self) -> None:
        self.status = MemberStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)
