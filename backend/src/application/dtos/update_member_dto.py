from datetime import date, datetime
import re
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator
from src.domain.enums.member_enums import MemberRole

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UpdateMemberRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=150, description="Nome completo do membro")
    phone: str = Field(..., min_length=8, max_length=20, description="Telefone de contato")
    email: Optional[str] = Field(default=None, description="E-mail opcional")
    role: MemberRole = Field(..., description="Papel: leader, core, normal")
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
