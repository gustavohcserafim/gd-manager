# Implementation Plan: Cadastro e Gestão de Membros (CRUD)

**Branch**: `001-member-management` | **Date**: 2026-11-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-member-management/spec.md`

## Summary

Implementação do ciclo completo de cadastro e gerenciamento de membros (CRUD) com três tipos de membros (`Líder`, `Membro do núcleo` e `Normal`), integrando aplicativo móvel em Flutter (iOS e Android) com backend em Python 3. A arquitetura segue rigorosamente a Clean Architecture em ambas as camadas com separação em Domain, Application, Infrastructure e Presentation, TDD inegociável em todos os componentes, custo zero de infraestrutura com SQLite e FastAPI, e controle de acesso hierárquico com alternância de perfil de teste no app.

## Technical Context

**Language/Version**: Python 3.11+ (Backend) e Dart 3.3+ / Flutter 3.19+ (Mobile Frontend)  
**Primary Dependencies**: 
- *Backend*: FastAPI (web e OpenAPI), Pydantic v2 (validação de tipos), Uvicorn (servidor ASGI leve) e Pytest (testes).
- *Frontend*: Flutter SDK nativo e pacote oficial `http` (comunicação REST).  
**Storage**: SQLite local estruturado via repositório abstrato (`MemberRepository`), com suporte a SQLite `:memory:` para suíte de testes. Custo zero de banco de dados.  
**Testing**: TDD estrito com `pytest` (unitários, integração e contrato no backend) e `flutter_test` (unitários e widgets no frontend).  
**Target Platform**: Multiplataforma mobile (iOS e Android) e servidor Linux/Container leve.  
**Project Type**: Mobile App (Flutter) + Web Service REST API (Python).  
**Performance Goals**: Tempo de resposta de listagem no app < 1s; resposta da API local < 50ms p95; renderização mobile constante a 60 fps.  
**Constraints**: 
- Custo zero de infraestrutura e hospedagem (Princípio IV da Constituição).
- Mínimo de pacotes externos; toda biblioteca com justificativa técnica formal (Princípio V da Constituição).
- Isolamento estrito de regras de negócio de frameworks e UI (Princípio I da Constituição).  
**Scale/Scope**: Gestão de grupos de 10 a 500 membros por unidade, com payloads JSON enxutos (<20KB por listagem padrão).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio Constitucional | Requisito Avaliado | Status | Evidência de Conformidade |
|---|---|---|---|
| **I. Clean Architecture** | Regras de domínio isoladas e fluxo de dependência para o centro | **PASS** | `domain/` sem imports de frameworks no Flutter e Python. Interfaces abstratas para repositórios. |
| **II. TDD Mandatório** | Testes criados antes da implementação de produção | **PASS** | Especificações de testes unitários, integração e contrato documentadas antes de tarefas de código. |
| **III. Mobile-First** | Paridade e fluidez em iOS e Android via Flutter | **PASS** | Interfaces desenhadas para toque, avatares dinâmicos por iniciais, feedback visual instantâneo e layout responsivo. |
| **IV. Mínimo Custo de Infra** | Zero custos proprietários fixos de infraestrutura | **PASS** | FastAPI com baixo consumo de memória (<50MB) e persistência em SQLite embutido sem custos de servidor gerenciado. |
| **V. Minimização de Dependências** | Apenas pacotes essenciais e justificados | **PASS** | Apenas FastAPI, Pydantic, Uvicorn e Pytest no backend; apenas `http` e SDK nativo no Flutter. |

## Project Structure

### Documentation (this feature)

```text
specs/001-member-management/
├── spec.md              # Especificação de requisitos e clarificações aprovadas
├── plan.md              # Este plano de implementação
├── research.md          # Decisões técnicas e justificativas de arquitetura (Fase 0)
├── data-model.md        # Entidades, enums, máquina de estados e SQLite DDL (Fase 1)
├── quickstart.md        # Roteiro de inicialização e cenários de validação E2E (Fase 1)
├── contracts/           # Contratos de interface e especificação OpenAPI (Fase 1)
│   └── members-api.yaml
└── checklists/
    └── requirements.md  # Checklist de qualidade da especificação
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml
├── src/
│   ├── main.py                          # Ponto de entrada FastAPI e injeção de dependências
│   ├── domain/                          # Camada pura de domínio (regras de negócio)
│   │   ├── entities/
│   │   │   └── member.py
│   │   ├── enums/
│   │   │   ├── member_role.py
│   │   │   └── member_status.py
│   │   ├── ports/
│   │   │   └── member_repository.py
│   │   └── exceptions/
│   │       ├── member_exceptions.py
│   │       └── authorization_exceptions.py
│   ├── application/                     # Casos de uso e DTOs
│   │   ├── dtos/
│   │   │   ├── create_member_dto.py
│   │   │   ├── update_member_dto.py
│   │   │   └── member_response_dto.py
│   │   └── use_cases/
│   │       ├── create_member_use_case.py
│   │       ├── get_members_use_case.py
│   │       ├── get_member_by_id_use_case.py
│   │       ├── update_member_use_case.py
│   │       ├── deactivate_member_use_case.py
│   │       └── reactivate_member_use_case.py
│   └── infrastructure/                  # Adaptadores de banco e web
│       ├── database/
│       │   ├── connection.py
│       │   └── sqlite_member_repository.py
│       └── web/
│           ├── dependencies.py          # Extração de X-User-Role e autorização
│           └── routers/
│               └── members_router.py
└── tests/
    ├── conftest.py                      # Fixtures de banco em memória e cliente de teste
    ├── unit/
    │   ├── test_member_entity.py
    │   └── test_member_use_cases.py
    ├── integration/
    │   └── test_sqlite_member_repository.py
    └── contract/
        └── test_members_api_contract.py

frontend/
├── pubspec.yaml
├── lib/
│   ├── main.dart                        # Inicialização do app Flutter
│   ├── core/
│   │   ├── constants/
│   │   └── errors/
│   ├── domain/                          # Camada pura de domínio em Dart
│   │   ├── entities/
│   │   │   └── member.dart
│   │   ├── repositories/
│   │   │   └── member_repository.dart
│   │   └── use_cases/
│   │       ├── get_members.dart
│   │       ├── create_member.dart
│   │       ├── update_member.dart
│   │       ├── deactivate_member.dart
│   │       └── reactivate_member.dart
│   ├── data/                            # Modelos e chamadas de rede
│   │   ├── models/
│   │   │   └── member_model.dart
│   │   ├── datasources/
│   │   │   └── member_remote_data_source.dart
│   │   └── repositories/
│   │       └── member_repository_impl.dart
│   └── presentation/                    # UI e Gerenciamento de Estado
│       ├── controllers/
│       │   ├── member_list_controller.dart
│       │   ├── member_form_controller.dart
│       │   └── session_context_controller.dart
│       ├── screens/
│       │   ├── member_list_screen.dart
│       │   ├── member_form_screen.dart
│       │   └── member_detail_screen.dart
│       └── widgets/
│           ├── member_card.dart
│           ├── member_avatar.dart
│           ├── role_badge.dart
│           └── user_role_selector_bar.dart
└── test/
    ├── unit/
    │   ├── domain/
    │   └── data/
    └── widget/
        ├── member_card_test.dart
        └── member_list_screen_test.dart
```

**Structure Decision**: Adotada a estrutura desacoplada `backend/` e `frontend/` com Clean Architecture explícita em ambos os projetos. Cada projeto mantém sua própria suíte de testes isolada com TDD, garantindo que o backend possa ser testado e executado de forma independente do Flutter e vice-versa.

## Complexity Tracking

> **Nenhuma violação constitucional identificada.** A arquitetura adota a separação mínima viável em camadas limpas, sem introduzir ferramentas desnecessárias, microserviços superdimensionados ou custos extras de hospedagem.
