abstract class Failure {
  final String message;
  const Failure(this.message);

  @override
  String toString() => message;
}

class ServerFailure extends Failure {
  const ServerFailure([super.message = 'Erro no servidor de dados. Tente novamente mais tarde.']);
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'Falha de conexão. Verifique sua rede e tente novamente.']);
}

class ValidationFailure extends Failure {
  const ValidationFailure(super.message);
}

class DuplicatePhoneFailure extends Failure {
  const DuplicatePhoneFailure([super.message = 'Este número de telefone já está cadastrado para outro membro ativo.']);
}

class UnauthorizedFailure extends Failure {
  const UnauthorizedFailure([super.message = 'Você não possui permissão para executar esta ação.']);
}

class NotFoundFailure extends Failure {
  const NotFoundFailure([super.message = 'Membro não encontrado no sistema.']);
}
