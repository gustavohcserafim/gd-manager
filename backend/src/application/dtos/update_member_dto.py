import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from src.domain.enums.member_enums import MemberRole

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UpdateMemberRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=150, description="Nome completo do membro")
    phone: str = Field(..., min_length=8, max_length=20, description="Telefone de contato")
    email: Optional[str] = Field(default=None, description="E-mail opcional")
    role: MemberRole = Field(..., description="Papel: leader, core, normal")

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
