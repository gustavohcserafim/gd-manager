from typing import Optional, List
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import UnauthorizedRoleException
from src.domain.ports.member_repository import MemberRepository
from src.application.dtos.create_member_dto import MemberResponse


class GetMembersUseCase:
    """Caso de uso para consulta e listagem de membros com filtros e busca."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(
        self,
        caller_role: MemberRole,
        status: Optional[MemberStatus] = MemberStatus.ACTIVE,
        role: Optional[MemberRole] = None,
        search: Optional[str] = None,
        birthday_month: Optional[int] = None,
    ) -> List[MemberResponse]:
        # Visualizar membros inativos exige papel leader ou core
        if status == MemberStatus.INACTIVE and not caller_role.can_manage_members():
            raise UnauthorizedRoleException(
                role=caller_role.value,
                action="visualizar membros com status inativo"
            )

        members = self.member_repository.find_all(
            status=status,
            role=role,
            search=search,
            birthday_month=birthday_month,
        )
        return [MemberResponse.from_entity(m) for m in members]
