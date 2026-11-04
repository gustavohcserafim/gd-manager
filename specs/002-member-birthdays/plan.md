# Implementation Plan: Gestão de Aniversários de Membros

**Branch**: `002-member-birthdays` | **Date**: 2026-11-04 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-member-birthdays/spec.md` (atualizada para formato `DD/MM/AAAA` no preenchimento e exibição)

## Summary

Implementação da funcionalidade de gestão de aniversários de membros no GD Manager. Torna obrigatória a informação de data de nascimento no cadastro e na edição de membros, assegurando que o preenchimento no formulário (seja por digitação assistida ou seletor de calendário) e a exibição em todas as telas (detalhes, cards e listas) ocorra estritamente no padrão brasileiro `DD/MM/AAAA` (`dd/mm/YYYY`). Internamente, a persistência segue o formato ISO 8601 (`YYYY-MM-DD`) no SQLite para eficiência de índices e queries com `strftime`. A arquitetura segue estritamente a Clean Architecture em Python 3 (FastAPI/SQLite) e Flutter (Dart), com TDD inegociável, custo zero de infraestrutura e zero bibliotecas externas adicionais.

## Technical Context

**Language/Version**: Python 3.11+ (Backend) e Dart 3.3+ / Flutter 3.19+ (Mobile Frontend)  
**Primary Dependencies**:
- *Backend*: FastAPI, Pydantic v2, Uvicorn, Pytest, padrão `datetime` nativo (`strptime`/`strftime`).
- *Frontend*: Flutter SDK nativo (`showDatePicker`, `TextInputFormatter`, `DateTime`), pacote `http`. Zero novas dependências (Princípio V).  
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
| **I. Clean Architecture** | Regras de cálculo de idade, validação e desacoplamento de formato | **PASS** | Entidade de domínio armazena data pura (`date` / `DateTime`); conversão do formato `DD/MM/AAAA` ocorre nas camadas de apresentação/DTOs sem poluir o núcleo de domínio. |
| **II. TDD Mandatório** | Testes criados antes da implementação de produção | **PASS** | Testes cobrindo preenchimento `DD/MM/AAAA`, validação de máscara/caracteres, parsers nos DTOs e exibição formatada criados antes do código de produção. |
| **III. Mobile-First** | Experiência fluida e nativa em telas de toque no formato brasileiro | **PASS** | Campo com máscara/formatação assistida `DD/MM/AAAA` e `showDatePicker` integrado, evitando erros comuns de digitação em telas móveis. |
| **IV. Mínimo Custo de Infra** | Zero custos proprietários fixos de infraestrutura | **PASS** | Conversões e cálculos puramente locais no cliente Flutter e no backend Python, sem APIs ou serviços em nuvem pagos. |
| **V. Minimização de Dependências** | Apenas recursos nativos sem novos pacotes | **PASS** | Formatação de data e máscara implementadas usando recursos nativos do Flutter (`TextInputFormatter` nativo) e Python (`datetime.strptime`). Zero novos pacotes no `pubspec.yaml` e `pyproject.toml`. |

## Project Structure

### Documentation (this feature)

```text
specs/002-member-birthdays/
├── spec.md              # Especificação de requisitos (atualizada para DD/MM/AAAA)
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
│   │       └── member.py                # birth_date como date, cálculos de idade e propriedades
│   ├── application/
│   │   ├── dtos/
│   │   │   ├── create_member_dto.py     # Suporte a entrada em DD/MM/AAAA e ISO YYYY-MM-DD
│   │   │   └── update_member_dto.py     # Suporte a entrada em DD/MM/AAAA e ISO YYYY-MM-DD
│   │   └── use_cases/
│   │       ├── get_members_use_case.py  # Suporte ao filtro birthday_month
│   │       └── get_upcoming_birthdays_use_case.py  # Caso de uso de próximos aniversariantes (30 dias)
│   └── infrastructure/
│       ├── database/
│       │   ├── connection.py            # Migração de esquema (coluna birth_date e índice)
│       │   └── sqlite_member_repository.py # Queries por mês e próximos aniversários
│       └── web/
│           └── routers/
│               └── members_router.py    # Rotas de membros e aniversariantes
└── tests/
    ├── unit/
    │   ├── test_member_entity.py        # Testes de cálculo de idade, validação e bissexto
    │   ├── test_create_member_dto.py    # Testes de parsing de DD/MM/AAAA e ISO
    │   └── test_upcoming_birthdays_use_case.py
    ├── integration/
    │   └── test_birthday_queries_sqlite.py
    └── contract/
        └── test_birthday_contract.py

frontend/
├── lib/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── member.dart              # birthDate, age, birthdayDisplay, birthDateFormatted
│   │   └── use_cases/
│   │       └── get_upcoming_birthdays.dart # Use case de próximos aniversariantes
│   ├── data/
│   │   ├── models/
│   │   │   └── member_model.dart        # Parsing flexível de birth_date (DD/MM/AAAA e ISO)
│   │   └── datasources/
│   │       └── member_remote_data_source.dart # Chamada getUpcomingBirthdays e filtro birthday_month
│   └── presentation/
│       ├── controllers/
│       │   ├── member_form_controller.dart # Validação e formatação de birthDate em DD/MM/AAAA
│       │   └── member_list_controller.dart # Lista de aniversariantes próximos e filtro por mês
│       ├── formatters/
│       │   └── date_input_formatter.dart # TextInputFormatter nativo para máscara DD/MM/AAAA
│       ├── screens/
│       │   ├── member_form_screen.dart  # Campo de data DD/MM/AAAA com DatePicker integrado
│       │   ├── member_list_screen.dart  # Seção de próximos aniversariantes e chips de meses
│       │   └── member_detail_screen.dart # Exibição estrita em DD/MM/AAAA e idade calculada
│       └── widgets/
│           ├── upcoming_birthdays_section.dart # Widget comemorativo no topo da tela
│           └── member_card.dart         # Tag comemorativa de aniversário no card
└── test/
    ├── unit/
    │   ├── domain/birthdays_test.dart
    │   └── presentation/date_input_formatter_test.dart
    └── widget/
        ├── member_form_birthday_test.dart
        ├── member_detail_birthday_test.dart
        └── upcoming_birthdays_section_test.dart
```

**Structure Decision**: A conversão de formatos reside nas bordas do sistema (Presentation no Flutter e DTOs na Application do Python), garantindo que as entidades de domínio permaneçam puras e desacopladas de formatos regionais de texto.

## Complexity Tracking

> **Nenhuma violação constitucional identificada.** A máscara de entrada é implementada via subclasse leve de `TextInputFormatter` nativo do Flutter, sem adicionar pacotes como `mask_text_input_formatter`, honrando estritamente o Princípio V da Constituição.
