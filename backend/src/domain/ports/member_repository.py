from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus


class MemberRepository(ABC):
    """Porta de abstração de repositório da Clean Architecture para gerenciamento de membros."""

    @abstractmethod
    def create(self, member: Member) -> Member:
        """Persiste um novo membro no banco de dados."""
        pass

    @abstractmethod
    def find_active_by_phone(self, phone: str) -> Optional[Member]:
        """Localiza um membro ativo com o telefone especificado."""
        pass

    @abstractmethod
    def find_by_id(self, member_id: str) -> Optional[Member]:
        """Localiza um membro por seu ID."""
        pass

    @abstractmethod
    def find_all(
        self,
        status: Optional[MemberStatus] = None,
        role: Optional[MemberRole] = None,
        search: Optional[str] = None,
        birthday_month: Optional[int] = None,
    ) -> List[Member]:
        """Retorna a lista de membros filtrada por status, papel, termo de busca e mês de aniversário."""
        pass

    @abstractmethod
    def update(self, member: Member) -> Member:
        """Atualiza os dados de um membro existente."""
        pass

    @abstractmethod
    def find_upcoming_birthdays(self, days: int = 30) -> List[Member]:
        """Retorna membros ativos com aniversários nos próximos `days` dias em ordem cronológica."""
        pass

    @abstractmethod
    def find_by_birthday_month(self, month: int) -> List[Member]:
        """Retorna membros ativos com aniversário no mês especificado (1 a 12)."""
        pass
