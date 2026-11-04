import re
import uuid
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass

from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import ValidationException


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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

    @classmethod
    def create(
        cls,
        name: str,
        phone: str,
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
    ) -> "Member":
        return cls(
            id=id,
            name=name,
            phone=phone,
            email=email,
            role=MemberRole.from_str(role),
            status=MemberStatus.from_str(status),
            created_at=datetime.fromisoformat(created_at),
            updated_at=datetime.fromisoformat(updated_at),
        )

    @property
    def initials(self) -> str:
        parts = [p for p in self.name.strip().split() if p]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    def update_info(
        self,
        name: str,
        phone: str,
        email: Optional[str],
        role: MemberRole,
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

        self.name = clean_name
        self.phone = clean_phone
        self.email = clean_email
        self.role = role
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        self.status = MemberStatus.INACTIVE
        self.updated_at = datetime.now(timezone.utc)

    def reactivate(self) -> None:
        self.status = MemberStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)
