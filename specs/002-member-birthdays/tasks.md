---
description: "Task list for Gestão de Aniversários de Membros implementation"
---

# Tasks: Gestão de Aniversários de Membros

**Input**: Design documents from `specs/002-member-birthdays/` (`spec.md`, `plan.md`, `data-model.md`, `research.md`, `contracts/members-birthdays-api.yaml`, `quickstart.md`)  
**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/members-birthdays-api.yaml`, `research.md`  
**Tests**: TDD Mandatório (Princípio II da Constituição). Testes automatizados DEVEM ser escritos antes da implementação do código de produção correspondente.  
**Organization**: As tarefas são agrupadas por histórias de usuário para viabilizar implementação e testes independentes de cada história.

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Tarefa paralelizável (arquivos diferentes, sem dependências de tarefas não concluídas).
- **[Story]**: Rótulo da história de usuário (`[US1]`, `[US2]`, `[US3]`) obrigatório exclusivamente nas fases de histórias de usuário.
- Caminhos de arquivo exatos incluídos em cada descrição.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verificação de infraestrutura de persistência e preparação do ambiente para a Feature 002.

- [X] T001 Verificar e validar ambiente de execução de testes do backend com `pytest` em `backend/pyproject.toml`
- [X] T002 [P] Verificar e validar dependências do Flutter SDK nativo e regras de análise em `frontend/pubspec.yaml` e `frontend/analysis_options.yaml`
- [X] T003 [P] Documentar contratos OpenAPI atualizados com formato `DD/MM/AAAA` em `specs/002-member-birthdays/contracts/members-birthdays-api.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Migração de banco de dados, formatadores nativos de entrada e contratos de dados essenciais que bloqueiam as histórias de usuário.

⚠️ **CRITICAL**: Nenhuma tarefa de história de usuário pode ser iniciada antes da conclusão desta fase.

- [X] T004 Implementar migração idempotente de esquema SQLite adicionando a coluna `birth_date TEXT` e o índice `idx_members_birth_date ON members(birth_date)` em `backend/src/infrastructure/database/connection.py`
- [X] T005 [P] Escrever testes de migração e compatibilidade com registros legados em `backend/tests/integration/test_birthday_queries_sqlite.py`
- [X] T006 [P] Atualizar DTOs `CreateMemberRequest` e `UpdateMemberRequest` com validador aceitando `DD/MM/AAAA` e `YYYY-MM-DD` ("Data de nascimento obrigatória. Aceita 'DD/MM/AAAA' ou 'YYYY-MM-DD'") e `MemberResponse` com `birth_date: Optional[date]` e `birth_date_formatted: Optional[str]` em `backend/src/application/dtos/create_member_dto.py` e `backend/src/application/dtos/update_member_dto.py`
- [X] T007 [P] Implementar formatador nativo `DateInputFormatter` estendendo `TextInputFormatter` para máscara automática no padrão `DD/MM/AAAA` em `frontend/lib/presentation/formatters/date_input_formatter.dart`
- [X] T008 [P] Escrever testes unitários para `DateInputFormatter` validando inserção automática de barras e limite de 10 caracteres em `frontend/test/unit/presentation/date_input_formatter_test.dart`
- [X] T009 [P] Atualizar modelo DTO `MemberModel` com parsing flexível de `birth_date` (aceitando `DD/MM/AAAA` e ISO `YYYY-MM-DD`) e serialização JSON em `frontend/lib/data/models/member_model.dart`
- [X] T010 [P] Atualizar interface `MemberRemoteDataSource` e `MemberRepositoryImpl` com suporte a `birth_date` em `frontend/lib/data/datasources/member_remote_data_source.dart` e `frontend/lib/data/repositories/member_repository_impl.dart`

**Checkpoint**: Fundação pronta - a implementação das histórias de usuário orientada a TDD pode começar.

---

## Phase 3: User Story 1 - Obrigatoriedade e Formato no Cadastro e Edição (Priority: P1) 🎯 MVP

**Goal**: Exigir obrigatoriamente data de nascimento válida no padrão brasileiro `DD/MM/AAAA` (`dd/mm/YYYY`), aceitando preenchimento manual com máscara assistida ou seletor visual nativo no cadastro e na edição de membros, validando que não seja futura e ano >= 1900.

**Independent Test**: Cadastrar novo membro digitando data no formato `DD/MM/AAAA` (ex: `15/05/1995`) ou selecionando via calendário (deve persistir com sucesso). Tentar cadastrar sem preencher data ou com data futura (deve bloquear com mensagem clara). Editar membro legado sem data (deve exigir informar a data em `DD/MM/AAAA`).

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL) ⚠️

- [X] T011 [P] [US1] Escrever testes unitários na entidade `Member` validando invariantes: "birth_date obrigatório em create e update", "birth_date não pode ser no futuro (birth_date <= date.today())", "birth_date ano mínimo 1900 (birth_date.year >= 1900)" em `backend/tests/unit/test_member_entity.py`
- [X] T012 [P] [US1] Escrever testes unitários para os DTOs `CreateMemberDTO` e `UpdateMemberDTO` validando parsing de formato `DD/MM/AAAA` e rejeição de formatos inválidos (ex: `32/01/1990` ou `15/13/1990`) em `backend/tests/unit/test_create_member_dto.py`
- [X] T013 [P] [US1] Escrever testes unitários em `CreateMemberUseCase` e `UpdateMemberUseCase` validando repasse e exigência de `birth_date` em `backend/tests/unit/test_create_member_use_case.py` e `backend/tests/unit/test_update_member_use_case.py`
- [X] T014 [P] [US1] Escrever testes de integração SQLite para persistência e recuperação do campo `birth_date` em `backend/tests/integration/test_birthday_queries_sqlite.py`
- [X] T015 [P] [US1] Escrever testes de contrato OpenAPI para `POST /api/v1/members` e `PUT /api/v1/members/{id}` validando status 201, 200 e 400 com payload contendo `birth_date` em `DD/MM/AAAA` e `YYYY-MM-DD` em `backend/tests/contract/test_birthday_contract.py`
- [X] T016 [P] [US1] Escrever testes unitários em Dart para validações de `birthDate` na entidade `Member` e no use case `CreateMember` em `frontend/test/unit/domain/birthdays_test.dart`
- [X] T017 [P] [US1] Escrever testes de estado para `MemberFormController` validando submissão e validação com `birthDate` em `DD/MM/AAAA` em `frontend/test/unit/presentation/member_form_birthday_test.dart`
- [X] T018 [P] [US1] Escrever testes de widgets para `MemberFormScreen` validando campo formatado em `DD/MM/AAAA`, máscara assistida e acionamento do DatePicker em `frontend/test/widget/member_form_birthday_test.dart`

### Implementation for User Story 1

- [X] T019 [US1] Atualizar entidade `Member` adicionando o atributo `birth_date: Optional[date]` e validações invariantes (`birth_date <= date.today()`, `birth_date.year >= 1900`) em `backend/src/domain/entities/member.py`
- [X] T020 [US1] Implementar validador de formato flexível (`DD/MM/AAAA` e `YYYY-MM-DD`) em `CreateMemberDTO` e `UpdateMemberDTO` em `backend/src/application/dtos/create_member_dto.py` e `backend/src/application/dtos/update_member_dto.py`
- [X] T021 [US1] Atualizar `CreateMemberUseCase` para exigir e repassar `birth_date` em `backend/src/application/use_cases/create_member_use_case.py`
- [X] T022 [US1] Atualizar `UpdateMemberUseCase` para exigir `birth_date` na edição em `backend/src/application/use_cases/update_member_use_case.py`
- [X] T023 [US1] Atualizar `SqliteMemberRepository` nos métodos `create`, `update`, `find_by_id` e `find_all` para persistir e ler a coluna `birth_date` em formato ISO em `backend/src/infrastructure/database/sqlite_member_repository.py`
- [X] T024 [US1] Atualizar rotas `POST /api/v1/members` e `PUT /api/v1/members/{id}` para recepção e retorno de dados de aniversário em `backend/src/infrastructure/web/routers/members_router.py`
- [X] T025 [P] [US1] Atualizar entidade Dart `Member` adicionando `DateTime? birthDate` e getter `birthDateFormatted` no padrão `DD/MM/AAAA` em `frontend/lib/domain/entities/member.dart`
- [X] T026 [P] [US1] Atualizar caso de uso `CreateMember` e `UpdateMember` no Flutter com suporte a `DateTime birthDate` em `frontend/lib/domain/use_cases/create_member.dart` e `frontend/lib/domain/use_cases/update_member.dart`
- [X] T027 [US1] Implementar chamadas com `birthDate` no DataSource e Repositório em `frontend/lib/data/datasources/member_remote_data_source.dart` e `frontend/lib/data/repositories/member_repository_impl.dart`
- [X] T028 [US1] Atualizar `MemberFormController` gerenciando o campo `birthDate`, validação estrita no padrão `DD/MM/AAAA` e integração com o DatePicker em `frontend/lib/presentation/controllers/member_form_controller.dart`
- [X] T029 [US1] Atualizar tela `MemberFormScreen` com campo de texto utilizando `DateInputFormatter`, placeholder `DD/MM/AAAA` e seletor `showDatePicker` populando o formato `DD/MM/AAAA` em `frontend/lib/presentation/screens/member_form_screen.dart`
- [X] T030 [US1] Conectar a inicialização de `birthDate` formatado em `DD/MM/AAAA` no formulário de edição em `frontend/lib/main.dart`

**Checkpoint**: User Story 1 (MVP) está 100% funcional. Novos membros e edições exigem data de nascimento em `DD/MM/AAAA`.

---

## Phase 4: User Story 2 - Exibição da Data de Nascimento no Formato DD/MM/AAAA e Idade (Priority: P2)

**Goal**: Exibir a data completa estritamente no padrão `DD/MM/AAAA` acompanhada da idade calculada na tela de detalhes, e exibir o dia e mês com indicador amigável nos cards da lista, destacando visualmente se o membro for aniversariante do dia.

**Independent Test**: Acessar o detalhe de um membro cadastrado e verificar exibição estrita no formato `DD/MM/AAAA` com a idade (ex: `15/05/1995 (31 anos)`). Visualizar card na listagem e verificar tag `🎂 15 de Maio` ou badge de aniversariante de hoje.

### Tests for User Story 2 (TDD - Write FIRST, ensure FAIL) ⚠️

- [X] T031 [P] [US2] Escrever testes unitários na entidade `Member` para cálculo de `age`, `birthday_display`, `birth_date_formatted` e `is_birthday_today` com suporte a 29 de fevereiro em `backend/tests/unit/test_member_entity.py`
- [X] T032 [P] [US2] Escrever testes de contrato OpenAPI validando os campos `age`, `birthday_display`, `birth_date_formatted`, `is_birthday_today` em `backend/tests/contract/test_birthday_contract.py`
- [X] T033 [P] [US2] Escrever testes unitários em Dart para getters `age`, `birthdayDisplay`, `birthDateFormatted` e `isBirthdayToday` em `frontend/test/unit/domain/birthdays_test.dart`
- [X] T034 [P] [US2] Escrever testes de widgets para `MemberCard` cobrindo exibição de indicador de aniversário e badge de aniversariante do dia em `frontend/test/widget/member_detail_birthday_test.dart`
- [X] T035 [P] [US2] Escrever testes de widgets para `MemberDetailScreen` validando exibição de data completa no formato `DD/MM/AAAA` e idade calculada em `frontend/test/widget/member_detail_birthday_test.dart`

### Implementation for User Story 2

- [X] T036 [US2] Implementar propriedades computadas `age`, `birthday_display`, `is_birthday_today` e `days_until_birthday` na entidade `Member` em `backend/src/domain/entities/member.py`
- [X] T037 [P] [US2] Atualizar DTO `MemberResponse` para incluir os campos computados e `birth_date_formatted` em `backend/src/application/dtos/create_member_dto.py`
- [X] T038 [P] [US2] Implementar getters computados `age`, `birthdayDisplay`, `birthDateFormatted` e `isBirthdayToday` na entidade `Member` em `frontend/lib/domain/entities/member.dart`
- [X] T039 [P] [US2] Atualizar `MemberModel` com mapeamento dos campos computados de aniversário e formatação em `frontend/lib/data/models/member_model.dart`
- [X] T040 [US2] Atualizar widget `MemberCard` exibindo o selo de aniversário com dia/mês (ex: `🎂 15 de Maio`) e indicador se for hoje em `frontend/lib/presentation/widgets/member_card.dart`
- [X] T041 [US2] Atualizar tela `MemberDetailScreen` exibindo a seção de aniversário com data completa no padrão `DD/MM/AAAA` e idade calculada em `frontend/lib/presentation/screens/member_detail_screen.dart`
- [X] T042 [US2] Tratar visualização de membros legados sem data de nascimento com rótulo "Data não informada" nos cards e detalhes em `frontend/lib/presentation/screens/member_detail_screen.dart` e `frontend/lib/presentation/widgets/member_card.dart`

**Checkpoint**: User Stories 1 e 2 funcionam juntas e são testáveis de forma independente.

---

## Phase 5: User Story 3 - Consulta e Filtro de Aniversariantes do Mês (Priority: P3)

**Goal**: Permitir que os integrantes visualizem uma seção de próximos aniversariantes (janela de 30 dias) no topo da tela principal e filtrem membros pelo mês de aniversário para planejamento.

**Independent Test**: Cadastrar membros com aniversários nos próximos 10 dias e outros em meses distintos. Acessar listagem no app e verificar o carrossel de próximos aniversariantes no topo. Selecionar filtro de mês (ex: Maio) e confirmar que apenas aniversariantes de maio são listados.

### Tests for User Story 3 (TDD - Write FIRST, ensure FAIL) ⚠️

- [X] T043 [P] [US3] Escrever testes unitários para `GetUpcomingBirthdaysUseCase` (janela de 30 dias e virada de ano) em `backend/tests/unit/test_upcoming_birthdays_use_case.py`
- [X] T044 [P] [US3] Escrever testes unitários para `GetMembersUseCase` com filtro de `birthday_month` em `backend/tests/unit/test_get_members_use_case.py`
- [X] T045 [P] [US3] Escrever testes de integração SQLite para queries de aniversariantes por mês e próximos aniversários em `backend/tests/integration/test_birthday_queries_sqlite.py`
- [X] T046 [P] [US3] Escrever testes de contrato OpenAPI para endpoint `GET /api/v1/members/birthdays/upcoming` e query param `birthday_month` em `backend/tests/contract/test_birthday_contract.py`
- [X] T047 [P] [US3] Escrever testes unitários em Dart para caso de uso `GetUpcomingBirthdays` e `MemberListController` com filtro de mês em `frontend/test/unit/presentation/member_list_birthday_test.dart`
- [X] T048 [P] [US3] Escrever testes de widgets para `UpcomingBirthdaysSection` em `frontend/test/widget/upcoming_birthdays_section_test.dart`

### Implementation for User Story 3

- [X] T049 [US3] Adicionar métodos `find_by_birthday_month(month: int)` e `find_upcoming_birthdays(days: int)` na porta `MemberRepository` em `backend/src/domain/ports/member_repository.py`
- [X] T050 [US3] Implementar caso de uso `GetUpcomingBirthdaysUseCase` em `backend/src/application/use_cases/get_upcoming_birthdays_use_case.py`
- [X] T051 [US3] Atualizar `GetMembersUseCase` para suportar o parâmetro opcional `birthday_month: Optional[int]` em `backend/src/application/use_cases/get_members_use_case.py`
- [X] T052 [US3] Implementar queries SQL otimizadas no SQLite para filtro por mês e próximos aniversariantes em `backend/src/infrastructure/database/sqlite_member_repository.py`
- [X] T053 [US3] Implementar endpoint `GET /api/v1/members/birthdays/upcoming` (registrado antes das rotas `/{id}` no APIRouter para evitar colisão de precedência) e adicionar query param `birthday_month` em `backend/src/infrastructure/web/routers/members_router.py`
- [X] T054 [P] [US3] Implementar caso de uso `GetUpcomingBirthdays` no Flutter em `frontend/lib/domain/use_cases/get_upcoming_birthdays.dart`
- [X] T055 [US3] Implementar chamadas remotas de próximos aniversariantes e query param de mês no DataSource em `frontend/lib/data/datasources/member_remote_data_source.dart` e `frontend/lib/data/repositories/member_repository_impl.dart`
- [X] T056 [US3] Atualizar `MemberListController` com lista de `upcomingBirthdays` e controle do filtro `selectedBirthdayMonth` em `frontend/lib/presentation/controllers/member_list_controller.dart`
- [X] T057 [P] [US3] Criar componente visual `UpcomingBirthdaysSection` exibindo avatares e dias restantes para o aniversário em `frontend/lib/presentation/widgets/upcoming_birthdays_section.dart`
- [X] T058 [US3] Integrar `UpcomingBirthdaysSection` no topo da `MemberListScreen` e adicionar seletor de meses na barra de filtros em `frontend/lib/presentation/screens/member_list_screen.dart`
- [X] T059 [US3] Conectar o caso de uso `GetUpcomingBirthdays` e atualizar inicialização do app em `frontend/lib/main.dart`

**Checkpoint**: Todas as 3 histórias de usuário estão totalmente implementadas com TDD.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verificação de integridade, testes de ponta a ponta e validação de qualidade sem regressões.

- [X] T060 [P] Executar cenários de validação ponta a ponta descritos em `specs/002-member-birthdays/quickstart.md`
- [X] T061 [P] Executar suite completa de testes e cobertura no backend com `python -m pytest tests/ -v -p no:cacheprovider` em `backend/`
- [X] T062 [P] Executar testes unitários e de widgets do Flutter em `frontend/`
- [X] T063 [P] Executar análise estática e linting sem erros em `backend/` (`ruff check`) e `frontend/`
- [X] T064 Atualizar documentação técnica e notas da funcionalidade no `README.md` raiz do repositório
- [X] T065 Executar validação de convergência da funcionalidade com `/speckit-converge`

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1: Setup
     │
     ▼
Phase 2: Foundational (BLOCKING - SQLite Migration, DTOs, DateInputFormatter)
     │
     ├──────────────────────┬──────────────────────┐
     ▼                      ▼                      ▼
Phase 3: US1 (P1 - MVP) Phase 4: US2 (P2)      Phase 5: US3 (P3)
     │                      │                      │
     └──────────────────────┴──────────────────────┘
                                    │
                                    ▼
                         Phase 6: Polish & Quickstart
```

### User Story Dependencies

- **US1 (P1 - MVP)**: Inicia após a Fase 2 (Foundational). Implementa a obrigatoriedade e preenchimento da data de nascimento em `DD/MM/AAAA`.
- **US2 (P2)**: Inicia após a Fase 2 (Foundational). Requer o atributo `birth_date` para renderizar a data estritamente como `DD/MM/AAAA` e a idade nos detalhes e cards.
- **US3 (P3)**: Inicia após a Fase 2 (Foundational). Opera sobre membros que possuem `birth_date` para prover a seção de próximos aniversariantes e filtros de meses.

### Within Each User Story (TDD Strict)

1. Testes automatizados DEVEM ser escritos primeiro e comprovadamente falhar (Red).
2. Entidades de domínio e portas antes dos casos de uso e DTOs.
3. Adaptadores de infraestrutura (SQLite e rotas web) após os casos de uso.
4. No frontend: Use Cases e Models antes dos Controllers, Componentes visuais e Telas.
5. Validação de testes verdes (Green) e refatoração limpa (Refactor).

---

## Parallel Opportunities

- **Setup (Phase 1)**: T002 e T003 podem ser executadas em paralelo com T001.
- **Foundational (Phase 2)**: T005, T006, T007, T008, T009 e T010 podem rodar em paralelo após a definição do DDL (T004).
- **Testes TDD**: Todos os testes com marcador `[P]` em cada fase de história podem ser redigidos simultaneamente.
- **Trabalho Fullstack**:
  - Desenvolvedor Backend: Endpoints, DTOs com suporte a `DD/MM/AAAA` e queries de US1, US2 e US3.
  - Desenvolvedor Frontend: `DateInputFormatter`, DatePicker em `DD/MM/AAAA`, Cards, Seção de Aniversários de US1, US2 e US3.

---

## Parallel Example: User Story 1 (MVP)

```bash
# Redigir simultaneamente os testes TDD:
Task: "T011 [P] [US1] Escrever testes unitários na entidade Member em backend/tests/unit/test_member_entity.py"
Task: "T012 [P] [US1] Escrever testes unitários para DTOs com DD/MM/AAAA em backend/tests/unit/test_create_member_dto.py"
Task: "T015 [P] [US1] Escrever testes de contrato OpenAPI em backend/tests/contract/test_birthday_contract.py"
Task: "T016 [P] [US1] Escrever testes unitários em Dart em frontend/test/unit/domain/birthdays_test.dart"
Task: "T018 [P] [US1] Escrever testes de widgets para MemberFormScreen com DD/MM/AAAA em frontend/test/widget/member_form_birthday_test.dart"

# Desenvolver paralelamente modelos de dados e DTOs:
Task: "T025 [P] [US1] Atualizar entidade Dart Member em frontend/lib/domain/entities/member.dart"
Task: "T026 [P] [US1] Atualizar caso de uso CreateMember e UpdateMember em frontend/lib/domain/use_cases/create_member.dart"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Concluir **Phase 1: Setup**.
2. Concluir **Phase 2: Foundational** (migração do banco, DTOs com parsing `DD/MM/AAAA`, `DateInputFormatter`).
3. Concluir **Phase 3: User Story 1 (Obrigatoriedade e Formato DD/MM/AAAA)** seguindo o ciclo TDD estrito.
4. **STOP e VALIDAR**: Cadastrar novo membro digitando `15/05/1995` ou selecionando via calendário e testar validação.
5. MVP pronto para validação!

### Entrega Incremental

1. MVP funcional (Setup + Foundational + US1) → Membros novos e editados agora têm data de nascimento obrigatória em `DD/MM/AAAA`.
2. Adicionar US2 → Idade e aniversário aparecem estritamente em `DD/MM/AAAA` nos detalhes e cards.
3. Adicionar US3 → Destaque de próximos aniversariantes no topo da tela e filtro de aniversariantes por mês.
4. Polimento, testes completos e validação cruzada (Phase 6).
