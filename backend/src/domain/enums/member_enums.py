from enum import Enum


class MemberRole(str, Enum):
    """Categorias de pertencimento e papéis de acesso do GD Manager."""
    LEADER = "leader"
    CORE = "core"
    NORMAL = "normal"

    @classmethod
    def from_str(cls, value: str) -> "MemberRole":
        val = value.lower().strip()
        for role in cls:
            if role.value == val:
                return role
        raise ValueError(f"Papel inválido: {value}. Valores permitidos: leader, core, normal")

    def can_manage_members(self) -> bool:
        """Indica se este papel possui permissão para criar, editar, inativar e reativar membros."""
        return self in (MemberRole.LEADER, MemberRole.CORE)


class MemberStatus(str, Enum):
    """Status cadastral do membro no grupo."""
    ACTIVE = "active"
    INACTIVE = "inactive"

    @classmethod
    def from_str(cls, value: str) -> "MemberStatus":
        val = value.lower().strip()
        for status in cls:
            if status.value == val:
                return status
        raise ValueError(f"Status inválido: {value}. Valores permitidos: active, inactive")
