from src.domain.enums.member_enums import MemberRole
from src.domain.exceptions.member_exceptions import (
    DuplicatePhoneException,
    UnauthorizedRoleException,
    MemberNotFoundException,
)
from src.domain.ports.member_repository import MemberRepository
from src.application.dtos.create_member_dto import MemberResponse


class DeactivateMemberUseCase:
    """Caso de uso para inativação lógica de membro (soft delete)."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, member_id: str, caller_role: MemberRole) -> MemberResponse:
        if not caller_role.can_manage_members():
            raise UnauthorizedRoleException(
                role=caller_role.value,
                action="inativar membros"
            )

        member = self.member_repository.find_by_id(member_id)
        if not member:
            raise MemberNotFoundException(member_id=member_id)

        member.deactivate()
        saved = self.member_repository.update(member)
        return MemberResponse.from_entity(saved)


class ReactivateMemberUseCase:
    """Caso de uso para reativação de membro inativo com revalidação de unicidade de telefone."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, member_id: str, caller_role: MemberRole) -> MemberResponse:
        if not caller_role.can_manage_members():
            raise UnauthorizedRoleException(
                role=caller_role.value,
                action="reativar membros"
            )

        member = self.member_repository.find_by_id(member_id)
        if not member:
            raise MemberNotFoundException(member_id=member_id)

        # Revalidação de colisão de telefone entre membros ativos
        existing_active = self.member_repository.find_active_by_phone(member.phone)
        if existing_active and existing_active.id != member.id:
            raise DuplicatePhoneException(
                phone=member.phone,
                message=f"Não é possível reativar o membro: o telefone '{member.phone}' já está sendo utilizado por outro membro ativo."
            )

        member.reactivate()
        saved = self.member_repository.update(member)
        return MemberResponse.from_entity(saved)
