# Research & Technical Decisions: Cadastro e Gestão de Membros (CRUD)

**Feature**: `001-member-management`  
**Date**: 2026-11-03  
**Status**: Concluded  

---

## 1. Backend Architecture (Python 3 & Clean Architecture)

- **Decision**: Adotar **FastAPI** (Python 3.11+) com tipagem estrita via **Pydantic v2** e organização estrita em **Clean Architecture** (Ports and Adapters).
- **Rationale**:
  - FastAPI é extremamente leve, assíncrono e gera automaticamente especificações OpenAPI/Swagger.
  - Não impõe acoplamento com banco de dados ou ORM, permitindo que a camada de domínio (`domain/`) seja 100% pura (sem dependência do FastAPI ou bibliotecas externas).
  - Possui footprint de memória ínfimo (<50MB RAM em execução), viabilizando hospedagem em containers serverless ou instâncias gratuitas (Render, Fly.io, Railway, AWS Lambda).
- **Alternatives Considered**:
  - *Django*: Rejeitado por ser um framework "batteries-included" monolítico, trazendo ORM proprietário que viola a pureza do domínio da Clean Architecture e consumo de memória substancialmente maior.
  - *Flask*: Rejeitado por exigir montagem manual de validações de schemas e serialização que o FastAPI já resolve nativamente com Pydantic de forma padronizada.

---

## 2. Storage & Persistência com Custo Zero

- **Decision**: Utilizar **SQLite** local/arquivo estruturado via repositório abstrato (`MemberRepository`), com suporte a SQLite em memória (`:memory:`) para a suíte de testes unitários e de integração.
- **Rationale**:
  - Custo de infraestrutura é exatamente **R$ 0,00** (Princípio IV da Constituição).
  - Dispensa o provisionamento de servidores de banco de dados gerenciados caros.
  - O repositório segue a interface abstrata do domínio; quando o sistema precisar escalar para PostgreSQL/MySQL no futuro, basta implementar um novo adaptador de infraestrutura sem alterar nenhuma linha de regra de negócio no domínio ou nos casos de uso.
- **Alternatives Considered**:
  - *PostgreSQL / Supabase / RDS*: Rejeitado nesta fase inicial por introduzir custos fixos ou complexidade operacional desnecessária para validar o CRUD de membros.

---

## 3. Frontend Architecture (Flutter Multiplataforma iOS & Android)

- **Decision**: Estruturar o Flutter seguindo rigorosamente a **Clean Architecture**:
  - `domain/`: Entidades (`Member`), interfaces de repositório (`MemberRepository`), casos de uso (`GetMembersUseCase`, `CreateMemberUseCase`, `UpdateMemberUseCase`, `DeactivateMemberUseCase`, `ReactivateMemberUseCase`).
  - `data/`: Modelos DTO (`MemberModel`), fontes de dados (`MemberRemoteDataSource` via HTTP), implementação de repositório.
  - `presentation/`: Gerenciamento de estado previsível e desacoplado via `ChangeNotifier` / `ValueNotifier` nativo do Flutter, telas de listagem/detalhes/cadastro e componentes de avatar gerados por iniciais.
- **Rationale**:
  - Permite testar todos os casos de uso e lógicas de apresentação sem necessidade de emuladores ou dispositivos físicos (TDD rápido com testes unitários em Dart puro).
  - Garante total independência de bibliotecas de terceiros (Princípio V da Constituição).
  - Desempenho nativo de 60/120 fps no iOS e Android.
- **Alternatives Considered**:
  - *GetX*: Rejeitado por misturar rotas, estado e dependências em um padrão acoplado que viola Clean Architecture.
  - *Bloc/Cubit com pacotes pesados*: Adotaremos a separação limpa com `ChangeNotifier`/`StateNotifier` nativo para evitar dependência externa desnecessária.

---

## 4. Estratégia de Testes (TDD Rigoroso)

- **Decision**: Test-Driven Development (TDD) com ciclo Red-Green-Refactor estrito:
  - **Backend (Python)**:
    - Testes Unitários de Domínio & Use Cases (`pytest`): 100% isolados, sem I/O real.
    - Testes de Integração de Repositório (`pytest`): validando queries SQLite e integridade referencial com `:memory:`.
    - Testes de Contrato de API (`TestClient`/FastAPI): validando status HTTP, cabeçalhos de permissão e schemas de resposta.
  - **Frontend (Flutter)**:
    - Testes Unitários de Casos de Uso e Modelos (`flutter_test`): sem dependência de widgets.
    - Testes de Estado/Controller (`flutter_test`): validando fluxo de carregamento, sucesso e tratamento de erro.
    - Testes de Widgets (`flutter_test`): validando exibição de campos, mensagens de erro e bloqueio de botões para membros Normais.
- **Rationale**: Cumprimento mandatório do Princípio II da Constituição (TDD inegociável).

---

## 5. Controle de Acesso e Perfil Ativo (RBAC)

- **Decision**: Passagem do papel ativo através do cabeçalho de requisição `X-User-Role: leader | core | normal` com middleware / dependency injection no FastAPI (`get_current_role`).
- **Rationale**:
  - Permite simular e alternar instantaneamente entre Líder, Núcleo e Normal no Flutter (via drawer ou seletor de perfil no topo da tela em modo de depuração/demonstração).
  - Valida todas as regras de autorização no backend e frontend sem inflar o escopo com telas de login, geração de senhas ou tokens JWT neste primeiro slice.

---

## 6. Unicidade de Telefone e Inativação Lógica (Soft Delete)

- **Decision**:
  - O campo `status` suportará `'active'` e `'inactive'`.
  - A regra de domínio e persistência valida que não pode haver dois membros com `status == 'active'` e o mesmo `phone`.
  - Membros inativos preservam seu histórico e telefone anterior, mas caso tentem ser reativados com um telefone que agora pertence a outro membro ativo, a reativação é bloqueada até que o conflito seja resolvido.
- **Rationale**: Atende diretamente às clarificações Q1 e Q4 do usuário.
