from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole
from src.domain.exceptions.member_exceptions import DuplicatePhoneException, UnauthorizedRoleException
from src.domain.ports.member_repository import MemberRepository
from src.application.dtos.create_member_dto import CreateMemberRequest, MemberResponse


class CreateMemberUseCase:
    """Caso de uso para cadastrar novo membro com validação de permissões e telefone único ativo."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, dto: CreateMemberRequest, caller_role: MemberRole) -> MemberResponse:
        # Validação de autorização RBAC
        if not caller_role.can_manage_members():
            raise UnauthorizedRoleException(
                role=caller_role.value,
                action="cadastrar novos membros"
            )

        # Validação de unicidade de telefone entre membros ativos
        existing = self.member_repository.find_active_by_phone(dto.phone)
        if existing:
            raise DuplicatePhoneException(phone=dto.phone)

        # Criação da entidade de domínio pura
        member = Member.create(
            name=dto.name,
            phone=dto.phone,
            email=str(dto.email) if dto.email else None,
            role=dto.role,
            birth_date=dto.birth_date,
        )

        # Persistência
        saved = self.member_repository.create(member)
        return MemberResponse.from_entity(saved)
