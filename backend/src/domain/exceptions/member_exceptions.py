class DomainException(Exception):
    """Exceção base para regras de negócio do domínio GD Manager."""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        super().__init__(message)
        self.message = message
        self.code = code


class DuplicatePhoneException(DomainException):
    """Lançada quando há tentativa de associar um telefone já em uso por outro membro ativo."""
    def __init__(self, phone: str, message: str = None):
        msg = message or f"O telefone '{phone}' já está cadastrado para outro membro ativo."
        super().__init__(msg, code="DUPLICATE_PHONE")
        self.phone = phone


class UnauthorizedRoleException(DomainException):
    """Lançada quando o papel do usuário não possui permissão para executar a operação."""
    def __init__(self, role: str, action: str = "esta operação", message: str = None):
        msg = message or f"Usuários com perfil '{role}' não têm permissão para {action}."
        super().__init__(msg, code="UNAUTHORIZED_ROLE")
        self.role = role


class MemberNotFoundException(DomainException):
    """Lançada quando um membro solicitado por identificador não é localizado."""
    def __init__(self, member_id: str, message: str = None):
        msg = message or f"Membro com ID '{member_id}' não foi encontrado."
        super().__init__(msg, code="MEMBER_NOT_FOUND")
        self.member_id = member_id


class ValidationException(DomainException):
    """Lançada quando dados fornecidos não satisfazem as restrições invariantes da entidade."""
    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")
