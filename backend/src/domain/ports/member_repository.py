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
    ) -> List[Member]:
        """Retorna a lista de membros filtrada por status, papel e termo de busca."""
        pass

    @abstractmethod
    def update(self, member: Member) -> Member:
        """Atualiza os dados de um membro existente."""
        pass
