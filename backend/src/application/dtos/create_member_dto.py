from datetime import date, datetime
import re
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator
from src.domain.enums.member_enums import MemberRole, MemberStatus

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class CreateMemberRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=150, description="Nome completo do membro")
    phone: str = Field(..., min_length=8, max_length=20, description="Telefone de contato sanitizado")
    email: Optional[str] = Field(default=None, description="E-mail opcional")
    role: MemberRole = Field(default=MemberRole.NORMAL, description="Papel: leader, core, normal")
    birth_date: date = Field(..., description="Data de nascimento obrigatória. Aceita 'DD/MM/AAAA' ou 'YYYY-MM-DD'.")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            clean = v.strip()
            if not clean:
                return None
            if not EMAIL_REGEX.match(clean):
                raise ValueError("Formato de e-mail inválido.")
            return clean
        return None

    @field_validator("birth_date", mode="before")
    @classmethod
    def parse_birth_date(cls, v: Any) -> Any:
        if isinstance(v, str):
            clean = v.strip()
            if not clean:
                raise ValueError("Data de nascimento é obrigatória.")
            if "/" in clean:
                try:
                    return datetime.strptime(clean, "%d/%m/%Y").date()
                except ValueError:
                    raise ValueError("Data de nascimento inválida. Use o formato DD/MM/AAAA.")
            try:
                return datetime.strptime(clean, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Data de nascimento inválida. Use o formato DD/MM/AAAA.")
        return v


class MemberResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: Optional[str] = None
    role: MemberRole
    status: MemberStatus
    birth_date: Optional[date] = None
    birth_date_formatted: Optional[str] = None
    age: Optional[int] = None
    birthday_display: Optional[str] = None
    is_birthday_today: bool = False
    days_until_birthday: Optional[int] = None
    initials: str
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, member) -> "MemberResponse":
        return cls(
            id=member.id,
            name=member.name,
            phone=member.phone,
            email=member.email,
            role=member.role,
            status=member.status,
            birth_date=getattr(member, "birth_date", None),
            birth_date_formatted=getattr(member, "birth_date_formatted", None),
            age=getattr(member, "age", None),
            birthday_display=getattr(member, "birthday_display", None),
            is_birthday_today=getattr(member, "is_birthday_today", False),
            days_until_birthday=getattr(member, "days_until_birthday", None),
            initials=member.initials,
            created_at=member.created_at.isoformat() if hasattr(member.created_at, "isoformat") else str(member.created_at),
            updated_at=member.updated_at.isoformat() if hasattr(member.updated_at, "isoformat") else str(member.updated_at),
        )
