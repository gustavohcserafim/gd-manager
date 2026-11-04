from src.domain.enums.member_enums import MemberRole
from src.domain.exceptions.member_exceptions import (
    DuplicatePhoneException,
    UnauthorizedRoleException,
    MemberNotFoundException,
)
from src.domain.ports.member_repository import MemberRepository
from src.application.dtos.create_member_dto import MemberResponse
from src.application.dtos.update_member_dto import UpdateMemberRequest


class GetMemberByIdUseCase:
    """Caso de uso para consultar um membro por seu ID."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, member_id: str) -> MemberResponse:
        member = self.member_repository.find_by_id(member_id)
        if not member:
            raise MemberNotFoundException(member_id=member_id)
        return MemberResponse.from_entity(member)


class UpdateMemberUseCase:
    """Caso de uso para atualizar dados de um membro com validação de unicidade de telefone."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, member_id: str, dto: UpdateMemberRequest, caller_role: MemberRole) -> MemberResponse:
        if not caller_role.can_manage_members():
            raise UnauthorizedRoleException(
                role=caller_role.value,
                action="editar dados de membros"
            )

        member = self.member_repository.find_by_id(member_id)
        if not member:
            raise MemberNotFoundException(member_id=member_id)

        # Se o telefone foi alterado, checar unicidade entre membros ativos
        if dto.phone.strip() != member.phone:
            existing = self.member_repository.find_active_by_phone(dto.phone.strip())
            if existing and existing.id != member.id:
                raise DuplicatePhoneException(phone=dto.phone.strip())

        member.update_info(
            name=dto.name,
            phone=dto.phone,
            email=str(dto.email) if dto.email else None,
            role=dto.role,
            birth_date=dto.birth_date,
        )

        saved = self.member_repository.update(member)
        return MemberResponse.from_entity(saved)
