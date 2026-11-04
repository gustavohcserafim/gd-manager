---
description: "Task list for Cadastro e Gestão de Membros (CRUD) implementation"
---

# Tasks: Cadastro e Gestão de Membros (CRUD)

**Input**: Design documents from `specs/001-member-management/` (`spec.md`, `plan.md`, `data-model.md`, `research.md`, `contracts/members-api.yaml`, `quickstart.md`)  
**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/members-api.yaml`, `research.md`  
**Tests**: TDD Mandatório (Princípio II da Constituição). Todos os testes unitários, de repositório, de contrato e de interface DEVEM ser escritos antes da implementação do código de produção correspondente.  
**Organization**: As tarefas são agrupadas por fases e por histórias de usuário para viabilizar entregas e testes independentes de cada fatia.

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Tarefa paralelizável (arquivos diferentes, sem dependências de tarefas não concluídas).
- **[Story]**: Rótulo da história de usuário (`[US1]`, `[US2]`, `[US3]`, `[US4]`) obrigatório exclusivamente nas fases de histórias.
- Caminhos de arquivo exatos incluídos em cada descrição.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicialização dos projetos de backend e frontend com dependências mínimas justificadas e estrutura Clean Architecture.

- [X] T001 Inicializar estrutura de diretórios do backend e arquivo de dependências enxutas (FastAPI, Uvicorn, Pydantic, Pytest) em `backend/pyproject.toml`
- [X] T002 [P] Inicializar estrutura de diretórios do frontend Flutter e manifesto de dependências com pacote `http` em `frontend/pubspec.yaml`
- [X] T003 [P] Configurar analisador estático e regras de linting para Python em `backend/pyproject.toml`
- [X] T004 [P] Configurar regras de análise e linting para Dart/Flutter em `frontend/analysis_options.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infraestrutura central de domínio, banco de dados e controle de acesso (RBAC) que DEVE estar concluída antes da implementação das histórias de usuário.

⚠️ **CRITICAL**: Nenhuma tarefa de história de usuário pode ser iniciada antes da conclusão desta fase.

- [X] T005 Implementar enums de domínio `MemberRole` ("leader, core, normal") e `MemberStatus` ("active, inactive") em `backend/src/domain/enums/member_enums.py`
- [X] T006 [P] Implementar exceções de domínio (`DuplicatePhoneException`, `UnauthorizedRoleException`, `MemberNotFoundException`) em `backend/src/domain/exceptions/member_exceptions.py`
- [X] T007 [P] Implementar conexão SQLite e criação de tabelas/índices (`CREATE TABLE members ... CHECK (role IN ('leader', 'core', 'normal'))`, `idx_members_active_phone ON members(phone) WHERE status = 'active'`) em `backend/src/infrastructure/database/connection.py`
- [X] T008 [P] Implementar middleware/dependência FastAPI de extração e validação do cabeçalho `X-User-Role` (`leader`, `core`, `normal`) em `backend/src/infrastructure/web/dependencies.py`
- [X] T009 [P] Implementar enums de domínio `MemberRole` e `MemberStatus` em Dart em `frontend/lib/domain/enums/member_enums.dart`
- [X] T010 [P] Implementar classes base de exceções e falhas de domínio no Flutter em `frontend/lib/core/errors/failures.dart`
- [X] T011 [P] Implementar cliente base de rede e constantes de API em `frontend/lib/data/datasources/api_client.dart`
- [X] T012 Implementar controlador de contexto de sessão/perfil ativo para alternância de testes no app (`SessionContextController`) em `frontend/lib/presentation/controllers/session_context_controller.dart`
- [X] T013 [P] Implementar barra superior de alternância rápida de perfil (`UserRoleSelectorBar`) para testes manuais em `frontend/lib/presentation/widgets/user_role_selector_bar.dart`

**Checkpoint**: Fundação pronta - a implementação das histórias de usuário orientada a TDD pode começar.

---

## Phase 3: User Story 1 - Cadastro de Novo Membro (Priority: P1) 🎯 MVP

**Goal**: Permitir que usuários com perfil Líder ou Membro do núcleo cadastrem novos membros informando nome, contato telefônico único e tipo de membro, com validação de campos obrigatórios, bloqueio para usuários com perfil Normal e exibição de avatar gerado por iniciais.

**Independent Test**: Com o perfil alternado para Líder, preencher formulário com nome válido, telefone e tipo "Líder". Verificar persistência e retorno HTTP 201 com avatar de iniciais gerado. Tentar cadastrar com mesmo telefone e verificar HTTP 409 com mensagem de duplicidade. Com perfil Normal, verificar que botão de cadastro não é exibido e tentativa de envio é rejeitada com HTTP 403.

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL) ⚠️

- [X] T014 [P] [US1] Escrever testes unitários para a entidade `Member` validando restrições: "name mínimo 3 caracteres e máximo 150 caracteres", "phone obrigatório sanitizado", "email opcional com formato válido", "role obrigatório default normal", "status obrigatório default active" em `backend/tests/unit/test_member_entity.py`
- [X] T015 [P] [US1] Escrever testes unitários para `CreateMemberUseCase` validando regras de unicidade de telefone ativo e permissões de perfil em `backend/tests/unit/test_create_member_use_case.py`
- [X] T016 [P] [US1] Escrever testes de integração de repositório SQLite para inserção de membro e disparo de constraint de telefone duplicado em `backend/tests/integration/test_create_member_sqlite.py`
- [X] T017 [P] [US1] Escrever testes de contrato OpenAPI para endpoint `POST /api/v1/members` validando status 201, 400 (dados inválidos), 403 (perfil normal) e 409 (telefone duplicado) em `backend/tests/contract/test_post_member_contract.py`
- [X] T018 [P] [US1] Escrever testes unitários em Dart para `Member` e `CreateMember` use case em `frontend/test/unit/domain/create_member_test.dart`
- [X] T019 [P] [US1] Escrever testes de estado para `MemberFormController` validando submissão e tratamento de erro em `frontend/test/unit/presentation/member_form_controller_test.dart`
- [X] T020 [P] [US1] Escrever testes de widgets para `MemberFormScreen` validando exibição de campos obrigatórios e mensagens de validação em `frontend/test/widget/member_form_screen_test.dart`

### Implementation for User Story 1

- [X] T021 [US1] Implementar entidade pura de domínio `Member` ("id UUID v4 imutável", "name string 3..150", "phone único ativo", "role enum", "status enum", "created_at", "updated_at") em `backend/src/domain/entities/member.py`
- [X] T022 [US1] Definir interface de porta de repositório `MemberRepository` com método `create(member: Member) -> Member` e `find_active_by_phone(phone: str) -> Optional[Member]` em `backend/src/domain/ports/member_repository.py`
- [X] T023 [P] [US1] Implementar DTOs `CreateMemberRequest` e `MemberResponse` (com cálculo de `initials` a partir do nome) em `backend/src/application/dtos/create_member_dto.py`
- [X] T024 [US1] Implementar caso de uso `CreateMemberUseCase` em `backend/src/application/use_cases/create_member_use_case.py`
- [X] T025 [US1] Implementar método de inserção e verificação de telefone único no adaptador SQLite em `backend/src/infrastructure/database/sqlite_member_repository.py`
- [X] T026 [US1] Implementar rota `POST /api/v1/members` com injeção de dependências e verificação de autorização RBAC em `backend/src/infrastructure/web/routers/members_router.py`
- [X] T027 [P] [US1] Implementar entidade Dart `Member` e interface de repositório em `frontend/lib/domain/entities/member.dart` e `frontend/lib/domain/repositories/member_repository.dart`
- [X] T028 [P] [US1] Implementar caso de uso `CreateMember` em `frontend/lib/domain/use_cases/create_member.dart`
- [X] T029 [P] [US1] Implementar modelo DTO `MemberModel` com serialização JSON e cálculo de iniciais em `frontend/lib/data/models/member_model.dart`
- [X] T030 [US1] Implementar chamada HTTP `createMember` no DataSource remoto em `frontend/lib/data/datasources/member_remote_data_source.dart`
- [X] T031 [US1] Implementar `MemberRepositoryImpl` no Flutter em `frontend/lib/data/repositories/member_repository_impl.dart`
- [X] T032 [US1] Implementar `MemberFormController` com controle de estados (loading, success, error) em `frontend/lib/presentation/controllers/member_form_controller.dart`
- [X] T033 [P] [US1] Implementar componente de avatar visual dinâmico com as iniciais do nome (`MemberAvatar`) em `frontend/lib/presentation/widgets/member_avatar.dart`
- [X] T034 [US1] Implementar tela de formulário de cadastro `MemberFormScreen` com validações de entrada em tempo real em `frontend/lib/presentation/screens/member_form_screen.dart`

**Checkpoint**: Neste ponto, a User Story 1 (MVP) está 100% funcional e testável de ponta a ponta.

---

## Phase 4: User Story 2 - Consulta e Listagem de Membros (Priority: P2)

**Goal**: Permitir que qualquer membro do grupo consulte a lista de integrantes com nome, avatar de iniciais e categoria, oferecendo pesquisa em tempo real por nome, filtro por tipo (Líder, Núcleo, Normal) e filtro de inativos (exclusivo para Líder e Núcleo), além de exibição de empty state amigável.

**Independent Test**: Popular base com membros de categorias variadas. Acessar listagem no app e verificar exibição correta dos cards. Filtrar por "Membro do núcleo" e verificar que apenas integrantes do núcleo aparecem. Digitar texto na barra de busca e confirmar filtragem dinâmica. Verificar que usuários com perfil Normal não veem o filtro de inativos.

### Tests for User Story 2 (TDD - Write FIRST, ensure FAIL) ⚠️

- [X] T035 [P] [US2] Escrever testes unitários para `GetMembersUseCase` cobrindo filtros de status, tipo, busca textual e bloqueio de inativos para perfil Normal em `backend/tests/unit/test_get_members_use_case.py`
- [X] T036 [P] [US2] Escrever testes de integração SQLite para queries de listagem com paginação/filtros em `backend/tests/integration/test_get_members_sqlite.py`
- [X] T037 [P] [US2] Escrever testes de contrato OpenAPI para endpoint `GET /api/v1/members` validando query params `status`, `role`, `search` e resposta 403 em `backend/tests/contract/test_get_members_contract.py`
- [X] T038 [P] [US2] Escrever testes unitários em Dart para use case `GetMembers` e `MemberListController` em `frontend/test/unit/presentation/member_list_controller_test.dart`
- [X] T039 [P] [US2] Escrever testes de widgets para `MemberListScreen` cobrindo cards, chips de filtro, badge de tipo e empty state em `frontend/test/widget/member_list_screen_test.dart`

### Implementation for User Story 2

- [X] T040 [US2] Adicionar método `find_all(status, role, search) -> List[Member]` na porta `MemberRepository` em `backend/src/domain/ports/member_repository.py`
- [X] T041 [US2] Implementar caso de uso `GetMembersUseCase` com regras de autorização de inativos em `backend/src/application/use_cases/get_members_use_case.py`
- [X] T042 [US2] Implementar método `find_all` com queries parametrizadas no repositório SQLite em `backend/src/infrastructure/database/sqlite_member_repository.py`
- [X] T043 [US2] Implementar rota `GET /api/v1/members` com suporte aos query parameters e headers em `backend/src/infrastructure/web/routers/members_router.py`
- [X] T044 [P] [US2] Implementar caso de uso `GetMembers` em `frontend/lib/domain/use_cases/get_members.dart`
- [X] T045 [US2] Implementar método `getMembers` com parâmetros de busca no DataSource remoto em `frontend/lib/data/datasources/member_remote_data_source.dart`
- [X] T046 [US2] Implementar `MemberListController` gerenciando listas filtradas e estados de carregamento em `frontend/lib/presentation/controllers/member_list_controller.dart`
- [X] T047 [P] [US2] Implementar widget visual de badge para papel (`RoleBadge`) em `frontend/lib/presentation/widgets/role_badge.dart`
- [X] T048 [P] [US2] Implementar widget de cartão de membro (`MemberCard`) exibindo avatar, nome e função em `frontend/lib/presentation/widgets/member_card.dart`
- [X] T049 [US2] Implementar tela principal de listagem `MemberListScreen` com campo de busca, chips de filtro por tipo/status e empty state em `frontend/lib/presentation/screens/member_list_screen.dart`

**Checkpoint**: As User Stories 1 e 2 funcionam juntas e são testáveis de forma independente.

---

## Phase 5: User Story 3 - Visualização e Edição de Dados do Membro (Priority: P3)

**Goal**: Permitir que usuários autorizados (Líder e Membro do núcleo) visualizem o detalhamento de um membro e editem seus dados cadastrais e categoria de função, garantindo validação de unicidade de telefone ativo e ocultando opções de edição para perfil Normal.

**Independent Test**: Abrir detalhes de um membro existente, alterar telefone para outro número válido e salvar, confirmando persistência. Tentar alterar para telefone de outro membro ativo e verificar erro 409. Com perfil Normal, confirmar que botões de edição não aparecem e chamadas diretas são negadas.

### Tests for User Story 3 (TDD - Write FIRST, ensure FAIL) ⚠️

- [X] T050 [P] [US3] Escrever testes unitários para `GetMemberByIdUseCase` e `UpdateMemberUseCase` validando regras de edição e unicidade de telefone em `backend/tests/unit/test_update_member_use_case.py`
- [X] T051 [P] [US3] Escrever testes de integração SQLite para busca por ID e atualização de registro em `backend/tests/integration/test_update_member_sqlite.py`
- [X] T052 [P] [US3] Escrever testes de contrato OpenAPI para `GET /api/v1/members/{id}` e `PUT /api/v1/members/{id}` em `backend/tests/contract/test_update_member_contract.py`
- [X] T053 [P] [US3] Escrever testes unitários em Dart para use cases `GetMemberById` e `UpdateMember` em `frontend/test/unit/domain/update_member_test.dart`
- [X] T054 [P] [US3] Escrever testes de widgets para `MemberDetailScreen` e fluxo de edição em `frontend/test/widget/member_detail_screen_test.dart`

### Implementation for User Story 3

- [X] T055 [P] [US3] Implementar DTO `UpdateMemberRequest` em `backend/src/application/dtos/update_member_dto.py`
- [X] T056 [US3] Adicionar métodos `find_by_id(id)` e `update(member)` na porta `MemberRepository` em `backend/src/domain/ports/member_repository.py`
- [X] T057 [US3] Implementar casos de uso `GetMemberByIdUseCase` e `UpdateMemberUseCase` em `backend/src/application/use_cases/update_member_use_case.py`
- [X] T058 [US3] Implementar métodos `find_by_id` e `update` com validação de unicidade de telefone no SQLite em `backend/src/infrastructure/database/sqlite_member_repository.py`
- [X] T059 [US3] Implementar rotas `GET /api/v1/members/{id}` e `PUT /api/v1/members/{id}` com controle RBAC em `backend/src/infrastructure/web/routers/members_router.py`
- [X] T060 [P] [US3] Implementar casos de uso `GetMemberById` e `UpdateMember` em `frontend/lib/domain/use_cases/update_member.dart`
- [X] T061 [US3] Implementar métodos correspondentes no DataSource remoto em `frontend/lib/data/datasources/member_remote_data_source.dart`
- [X] T062 [US3] Implementar tela de detalhes `MemberDetailScreen` com ações condicionadas ao perfil ativo em `frontend/lib/presentation/screens/member_detail_screen.dart`
- [X] T063 [US3] Integrar formulário `MemberFormScreen` para suportar modo de edição pré-populado em `frontend/lib/presentation/screens/member_form_screen.dart`

**Checkpoint**: User Stories 1, 2 e 3 estão concluídas e integradas com sucesso.

---

## Phase 6: User Story 4 - Inativação e Reativação de Membros (Priority: P4)

**Goal**: Permitir que Líderes e Membros do núcleo inativem integrantes que deixaram o grupo (soft delete com confirmação obrigatória) e reativem membros que retornarem, revalidando a unicidade de telefone ativo antes da reativação.

**Independent Test**: Autenticado como Líder, inativar um membro ativo e confirmar no diálogo. Verificar que ele desaparece da lista ativa e aparece no filtro de inativos. Reativar o membro e verificar seu retorno à lista ativa.

### Tests for User Story 4 (TDD - Write FIRST, ensure FAIL) ⚠️

- [X] T064 [P] [US4] Escrever testes unitários para `DeactivateMemberUseCase` e `ReactivateMemberUseCase` cobrindo colisão de telefone na reativação em `backend/tests/unit/test_lifecycle_use_cases.py`
- [X] T065 [P] [US4] Escrever testes de integração SQLite para transições de status `active` <-> `inactive` em `backend/tests/integration/test_lifecycle_sqlite.py`
- [X] T066 [P] [US4] Escrever testes de contrato OpenAPI para `DELETE /api/v1/members/{id}` e `PATCH /api/v1/members/{id}/reactivate` em `backend/tests/contract/test_lifecycle_contract.py`
- [X] T067 [P] [US4] Escrever testes unitários em Dart para use cases de inativação e reativação em `frontend/test/unit/domain/lifecycle_member_test.dart`
- [X] T068 [P] [US4] Escrever testes de widgets para o diálogo de confirmação de inativação em `frontend/test/widget/deactivate_dialog_test.dart`

### Implementation for User Story 4

- [X] T069 [US4] Adicionar métodos `deactivate(id)` e `reactivate(id)` na porta `MemberRepository` em `backend/src/domain/ports/member_repository.py`
- [X] T070 [US4] Implementar casos de uso `DeactivateMemberUseCase` e `ReactivateMemberUseCase` com revalidação de unicidade em `backend/src/application/use_cases/lifecycle_use_cases.py`
- [X] T071 [US4] Implementar queries de atualização de status com controle de transação no SQLite em `backend/src/infrastructure/database/sqlite_member_repository.py`
- [X] T072 [US4] Implementar rotas `DELETE /api/v1/members/{id}` e `PATCH /api/v1/members/{id}/reactivate` em `backend/src/infrastructure/web/routers/members_router.py`
- [X] T073 [P] [US4] Implementar casos de uso `DeactivateMember` e `ReactivateMember` em `frontend/lib/domain/use_cases/lifecycle_member.dart`
- [X] T074 [US4] Implementar métodos de inativação e reativação no DataSource remoto em `frontend/lib/data/datasources/member_remote_data_source.dart`
- [X] T075 [P] [US4] Implementar diálogo de confirmação de inativação (`DeactivateConfirmationDialog`) em `frontend/lib/presentation/widgets/deactivate_confirmation_dialog.dart`
- [X] T076 [US4] Conectar botões de inativação e reativação na tela `MemberDetailScreen` e atualizar a listagem dinamicamente em `frontend/lib/presentation/screens/member_detail_screen.dart`

**Checkpoint**: Todas as 4 histórias de usuário estão totalmente implementadas com TDD.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Verificação de integridade, testes de ponta a ponta e auditoria de qualidade sem acoplamento a histórias específicas.

- [X] T077 [P] Implementar tratamento global de erros de conexão e banner de aviso offline em `frontend/lib/presentation/widgets/network_error_banner.dart`
- [X] T078 Executar roteiro completo de validação ponta a ponta descrito em `specs/001-member-management/quickstart.md`
- [X] T079 [P] Executar suite completa de testes e cobertura no backend (`pytest`) em `backend/`
- [X] T080 [P] Executar testes de unidade e widgets no Flutter em `frontend/`
- [X] T081 [P] Executar compilação e verificação de sintaxe de todos os arquivos do projeto
- [X] T082 Atualizar documentação técnica e instruções de inicialização no `README.md` raiz do repositório

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1: Setup
     │
     ▼
Phase 2: Foundational (BLOCKING - Core Domain, Database, RBAC)
     │
     ├──────────────────────┬──────────────────────┬──────────────────────┐
     ▼                      ▼                      ▼                      ▼
Phase 3: US1 (P1)      Phase 4: US2 (P2)      Phase 5: US3 (P3)      Phase 6: US4 (P4)
     │                      │                      │                      │
     └──────────────────────┴──────────────────────┴──────────────────────┘
                                    │
                                    ▼
                         Phase 7: Polish & Quickstart
```

### User Story Dependencies

- **US1 (P1)**: Pode iniciar imediatamente após a Phase 2 (Foundational). Não depende de outras histórias.
- **US2 (P2)**: Pode iniciar após a Phase 2. Utiliza as entidades e tabelas criadas na fundação.
- **US3 (P3)**: Pode iniciar após a Phase 2. Depende da existência do modelo de dados básico da US1.
- **US4 (P4)**: Pode iniciar após a Phase 2. Opera sobre os membros criados na US1/US2.

### Within Each User Story (TDD Enforcement)

1. Testes de unidade e contrato DEVEM ser escritos primeiro e comprovadamente falhar (Red).
2. Entidades e interfaces de domínio antes de casos de uso.
3. Casos de uso e DTOs antes dos adaptadores de infraestrutura (banco e rotas).
4. No frontend: Use Cases e Models antes dos Controllers e Telas.
5. Validação de testes verdes (Green) e refatoração limpa (Refactor).

---

## Parallel Opportunities

- **Setup (Phase 1)**: Tarefas T002, T003 e T004 podem ser executadas em paralelo com T001.
- **Foundational (Phase 2)**: Tarefas T006, T007, T008 (backend) e T009, T010, T011, T013 (frontend) podem ser desenvolvidas em paralelo.
- **Histórias de Usuário**: Em equipe multideveloper, após a Phase 2 ser concluída:
  - Desenvolvedor Backend A: Implementação de Use Cases e rotas de US1 e US2.
  - Desenvolvedor Frontend B: Implementação de componentes de UI e telas de US1 e US2.
- **Testes TDD**: Todos os testes com marcador `[P]` dentro de cada fase de história podem ser redigidos em paralelo.

---

## Parallel Example: User Story 1 (MVP)

```bash
# Executar simultaneamente a escrita dos testes TDD:
Task: "T014 [P] [US1] Escrever testes unitários para a entidade Member em backend/tests/unit/test_member_entity.py"
Task: "T017 [P] [US1] Escrever testes de contrato OpenAPI para endpoint POST /api/v1/members em backend/tests/contract/test_post_member_contract.py"
Task: "T018 [P] [US1] Escrever testes unitários em Dart para CreateMember em frontend/test/unit/domain/create_member_test.dart"
Task: "T020 [P] [US1] Escrever testes de widgets para MemberFormScreen em frontend/test/widget/member_form_screen_test.dart"

# Desenvolver paralelamente modelos de dados e DTOs:
Task: "T023 [P] [US1] Implementar DTOs CreateMemberRequest e MemberResponse em backend/src/application/dtos/create_member_dto.py"
Task: "T027 [P] [US1] Implementar entidade Dart Member em frontend/lib/domain/entities/member.dart"
Task: "T029 [P] [US1] Implementar modelo DTO MemberModel em frontend/lib/data/models/member_model.dart"
Task: "T033 [P] [US1] Implementar componente de avatar visual dinâmico em frontend/lib/presentation/widgets/member_avatar.dart"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Concluir **Phase 1: Setup**.
2. Concluir **Phase 2: Foundational** (bloqueante para todo o sistema).
3. Concluir **Phase 3: User Story 1 (Cadastro de Novo Membro)** seguindo o ciclo TDD.
4. **STOP e VALIDAR**: Testar a criação de membros com validação de duplicidade e controle de acesso hierárquico isoladamente.
5. MVP pronto para validação de ponta a ponta!

### Entrega Incremental

1. MVP funcional (Setup + Foundational + US1) → Membros podem ser cadastrados e validados.
2. Adicionar US2 → Membros podem ser visualizados, pesquisados e filtrados por tipo.
3. Adicionar US3 → Membros existentes podem ser consultados em detalhes e editados.
4. Adicionar US4 → Membros podem ser inativados e reativados com segurança.
5. Polimento e validação cruzada (Phase 7).


---

## Phase 8: Convergence

- [X] T083 [CRITICAL] Corrigir resolução de importações dos testes unitários em backend/tests/conftest.py ou backend/pyproject.toml para viabilizar execução limpa do pytest a partir do diretório backend/ per Constitution II (contradicts)
- [X] T084 Adicionar mensagens de feedback visual (SnackBar) e tratamento de erros (try/catch) nas operações de inativação e reativação em frontend/lib/main.dart per FR-010 / US4/AC2 / US4/AC5 (partial)
- [X] T085 Condicionar o retorno da tela de detalhes de membro ao resultado da edição evitando fechamento indevido no cancelamento em frontend/lib/main.dart per US3/AC1 / US3/AC2 (partial)
- [X] T086 Ajustar asserção do botão de edição em frontend/test/widget/member_detail_screen_test.dart para coincidir com o rótulo 'Editar Dados' renderizado per Constitution II / T054 (partial)
