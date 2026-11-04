from typing import List
from src.domain.ports.member_repository import MemberRepository
from src.application.dtos.create_member_dto import MemberResponse


class GetUpcomingBirthdaysUseCase:
    """Caso de uso para consultar membros aniversariantes nos próximos dias (janela configurável, padrão 30 dias)."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, days: int = 30) -> List[MemberResponse]:
        members = self.member_repository.find_upcoming_birthdays(days=days)
        return [MemberResponse.from_entity(m) for m in members]
