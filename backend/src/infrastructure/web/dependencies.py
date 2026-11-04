from typing import Optional
from fastapi import Header, HTTPException, status
from src.domain.enums.member_enums import MemberRole


def get_current_role(
    x_user_role: Optional[str] = Header(default="normal", alias="X-User-Role")
) -> MemberRole:
    """Extrai e valida o papel ativo do usuário a partir do cabeçalho HTTP X-User-Role."""
    try:
        return MemberRole.from_str(x_user_role or "normal")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Valor de cabeçalho 'X-User-Role' inválido: '{x_user_role}'. Válidos: leader, core, normal"
        )


def require_manager_role(
    role: MemberRole = Header(default="normal", alias="X-User-Role")
) -> MemberRole:
    """Valida se o usuário solicitante possui perfil de liderança (Líder ou Membro do núcleo)."""
    current_role = get_current_role(role)
    if not current_role.can_manage_members():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Operação não permitida para o perfil '{current_role.value}'. Exige perfil 'leader' ou 'core'."
        )
    return current_role
