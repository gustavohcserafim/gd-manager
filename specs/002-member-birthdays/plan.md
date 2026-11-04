# Implementation Plan: Gestão de Aniversários de Membros

**Branch**: `002-member-birthdays` | **Date**: 2026-11-04 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-member-birthdays/spec.md`

## Summary

Implementação da funcionalidade de gestão de aniversários de membros no GD Manager. Torna obrigatória a informação de data de nascimento no cadastro e na edição de membros, calcula idade e dias até o aniversário dinamicamente, oferece destaque de próximos aniversariantes (janela de 30 dias) no topo da tela principal, filtro mensal de aniversariantes e exibição do dia/mês nos cards e data completa com idade nos detalhes cadastrais. A arquitetura segue estritamente a Clean Architecture em Python 3 (FastAPI/SQLite) e Flutter (Dart), com TDD inegociável, custo zero de infraestrutura e zero bibliotecas externas adicionais.

## Technical Context

**Language/Version**: Python 3.11+ (Backend) e Dart 3.3+ / Flutter 3.19+ (Mobile Frontend)  
**Primary Dependencies**:
- *Backend*: FastAPI, Pydantic v2, Uvicorn, Pytest, padrão `datetime` nativo.
- *Frontend*: Flutter SDK nativo (`showDatePicker`, `DateTime`), pacote `http`. Zero novas dependências.  
**Storage**: SQLite local persistente (`gd_manager.db`) e em memória para testes (`:memory:`), com evolução de esquema idempotente (`ALTER TABLE members ADD COLUMN birth_date TEXT;`).  
**Testing**: TDD estrito com `pytest` (unitários, integração e contrato no backend) e `flutter_test` (unitários e widgets no frontend).  
**Target Platform**: Multiplataforma mobile (Android e iOS) e Web (Google Chrome/Edge).  
**Project Type**: Mobile App (Flutter) + Web Service REST API (Python).  
**Performance Goals**: Tempo de resposta de listagem com cálculo de aniversários < 50ms localmente; renderização da lista e carrossel de aniversariantes a 60 fps constantes.  
**Constraints**:
- Custo zero de infraestrutura e hospedagem (Princípio IV da Constituição).
- Parcimônia extrema de dependências externas sem introduzir pacotes novos (Princípio V da Constituição).
- Isolamento estrito de regras de negócio de frameworks e UI (Princípio I da Constituição).  
**Scale/Scope**: Gestão de grupos de 10 a 500 membros, com janelas de cálculo eficientes e sem sobrecarga de processamento no dispositivo móvel.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio Constitucional | Requisito Avaliado | Status | Evidência de Conformidade |
|---|---|---|---|
| **I. Clean Architecture** | Regras de cálculo de idade e validação de data no domínio | **PASS** | Cálculo de idade, dias até aniversário e validação de datas implementados puramente nas entidades de domínio (`Member`), sem acoplamento a frameworks. |
| **II. TDD Mandatório** | Testes criados antes da implementação de produção | **PASS** | Testes unitários para cálculo de idade e bissexto, testes de repositório SQLite e testes de contrato OpenAPI documentados antes da codificação. |
| **III. Mobile-First** | Experiência fluida e nativa em telas de toque | **PASS** | Seletor de data (`showDatePicker`) nativo do Flutter, seção horizontal de destaque no topo da tela e cartões compactos otimizados para toque. |
| **IV. Mínimo Custo de Infra** | Zero custos proprietários fixos de infraestrutura | **PASS** | Cálculos executados na CPU local e no SQLite embutido, sem serviços externos de calendário ou servidores adicionais. |
| **V. Minimização de Dependências** | Apenas pacotes essenciais sem novas adições | **PASS** | Zero novas dependências no `pubspec.yaml` e no `pyproject.toml`. Uso exclusivo de recursos nativos (`datetime`, `showDatePicker`). |

## Project Structure

### Documentation (this feature)

```text
specs/002-member-birthdays/
├── spec.md              # Especificação de requisitos e clarificações aprovadas
├── plan.md              # Este plano de implementação
├── research.md          # Pesquisa técnica e decisões de arquitetura (Fase 0)
├── data-model.md        # Entidade Member estendida, DTOs e SQLite DDL (Fase 1)
├── quickstart.md        # Roteiro de inicialização e cenários de validação E2E (Fase 1)
├── contracts/           # Especificação OpenAPI dos endpoints de aniversário (Fase 1)
│   └── members-birthdays-api.yaml
└── checklists/
    └── requirements.md  # Checklist de qualidade da especificação
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── domain/
│   │   └── entities/
│   │       └── member.py                # Atributo birth_date, age, birthday_display, is_birthday_today
│   ├── application/
│   │   ├── dtos/
│   │   │   ├── create_member_dto.py     # Campo birth_date obrigatório
│   │   │   └── update_member_dto.py     # Campo birth_date obrigatório
│   │   └── use_cases/
│   │       ├── get_members_use_case.py  # Suporte ao filtro birthday_month
│   │       └── get_upcoming_birthdays_use_case.py  # Caso de uso de próximos aniversariantes (30 dias)
│   └── infrastructure/
│       ├── database/
│       │   ├── connection.py            # Migração de esquema (coluna birth_date e índice)
│       │   └── sqlite_member_repository.py # Queries por mês e próximos aniversários
│       └── web/
│           └── routers/
│               └── members_router.py    # Query param birthday_month e rota /birthdays/upcoming
└── tests/
    ├── unit/
    │   ├── test_member_entity.py        # Testes de cálculo de idade, validação e bissexto
    │   └── test_upcoming_birthdays_use_case.py
    ├── integration/
    │   └── test_birthday_queries_sqlite.py
    └── contract/
        └── test_birthday_contract.py

frontend/
├── lib/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── member.dart              # birthDate, age, birthdayDisplay, isBirthdayToday
│   │   └── use_cases/
│   │       └── get_upcoming_birthdays.dart # Use case de próximos aniversariantes
│   ├── data/
│   │   ├── models/
│   │   │   └── member_model.dart        # Serialização/deserialização de birth_date
│   │   └── datasources/
│   │       └── member_remote_data_source.dart # Chamada getUpcomingBirthdays e filtro birthday_month
│   └── presentation/
│       ├── controllers/
│       │   ├── member_form_controller.dart # Controle e validação de birthDate no formulário
│       │   └── member_list_controller.dart # Lista de aniversariantes próximos e filtro por mês
│       ├── screens/
│       │   ├── member_form_screen.dart  # Campo de data de nascimento com DatePicker integrado
│       │   ├── member_list_screen.dart  # Seção de próximos aniversariantes e chips de meses
│       │   └── member_detail_screen.dart # Exibição de data completa e idade calculada
│       └── widgets/
│           ├── upcoming_birthdays_section.dart # Widget comemorativo no topo da tela
│           └── member_card.dart         # Tag comemorativa de aniversário no card
└── test/
    ├── unit/
    │   └── domain/birthdays_test.dart
    └── widget/
        ├── member_form_birthday_test.dart
        └── upcoming_birthdays_section_test.dart
```

**Structure Decision**: Mantida rigorosamente a divisão desacoplada `backend/` e `frontend/` com Clean Architecture. Nenhuma nova camada ou dependência externa foi criada, estendendo harmonicamente os módulos já consolidados na Feature 001.

## Complexity Tracking

> **Nenhuma violação constitucional identificada.** Toda a lógica foi concebida utilizando a biblioteca padrão do Python e o SDK nativo do Flutter.
