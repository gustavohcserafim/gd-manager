# Research & Technical Decisions: Gestão de Aniversários de Membros

**Feature**: `002-member-birthdays` | **Date**: 2026-11-04

## Overview

Este documento consolida as pesquisas técnicas, decisões de arquitetura e justificativas de engenharia para a implementação da gestão de aniversários no GD Manager, respeitando os princípios da [Constituição do GD Manager](../../.specify/memory/constitution.md) (Clean Architecture, TDD, Mobile-First, Custo Zero e Parcimônia de Dependências).

---

## Technical Decisions

### 1. Formato de Armazenamento e Manipulação de Datas

- **Decision**: Armazenamento em SQLite como `TEXT` no padrão ISO 8601 estrito (`YYYY-MM-DD`). Manipulação via `datetime.date` no backend (Python) e `DateTime` no frontend (Dart).
- **Rationale**:
  - Datas de nascimento são datas de calendário puras (não possuem fuso horário nem hora/minuto). O uso de `YYYY-MM-DD` evita anomalias de fuso horário (ex: membro nascido à meia-noite virar o dia anterior por conversão UTC).
  - O SQLite possui funções nativas de data (`strftime('%m', birth_date)`, `strftime('%d', birth_date)`) extremamente eficientes para queries de filtragem por mês e dia.
- **Alternatives Considered**:
  - *Unix Timestamp (inteiro em milissegundos)*: Rejeitado porque introduz distorções com fusos horários e horário de verão para datas de nascimento, além de dificultar consultas SQL por mês.
  - *Três colunas separadas (`birth_day`, `birth_month`, `birth_year`)*: Rejeitado por duplicar espaço e dificultar validações completas de calendário (ex: validar 29 de fevereiro apenas em anos bissextos).

### 2. Algoritmo de Cálculo de Idade e Próximos Aniversariantes

- **Decision**:
  - **Idade**: Calculada de forma determinística comparando `(hoje.month, hoje.day) < (nascimento.month, nascimento.day)`:
    $$\text{idade} = \text{hoje.year} - \text{nascimento.year} - (1 \text{ se aniversário ainda não ocorreu este ano senão } 0)$$
  - **Próximos Aniversariantes (próximos 30 dias)**:
    - Para cada membro ativo com data de nascimento, projeta-se o aniversário no ano atual.
    - Se a data já passou neste ano, projeta-se para o próximo ano (cobrindo perfeitamente a virada de Dezembro para Janeiro).
    - Membros cuja diferença de dias entre a data projetada e hoje for $\ge 0$ e $\le 30$ são selecionados e ordenados em ordem cronológica crescente.
  - **Anos Bissextos (29 de Fevereiro)**:
    - Em anos não bissextos, a data projetada é ajustada para 28 de Fevereiro.
- **Rationale**: Abordagem pura, testável em isolamento sem bibliotecas externas, garantindo precisão matemática e respeito às regras de negócio.
- **Alternatives Considered**:
  - *Filtro simples apenas por mês civil*: Não resolve o requisito de destacar os aniversariantes dos próximos 30 dias quando estamos no fim do mês (ex: dia 25 de novembro quer ver quem faz aniversário até 25 de dezembro).

### 3. Migração Não-Destrutiva do Banco de Dados SQLite

- **Decision**: Evolução de esquema idempotente em `backend/src/infrastructure/database/connection.py`:
  - Execução de verificação via `PRAGMA table_info(members)`.
  - Caso a coluna `birth_date` não exista, executar:
    ```sql
    ALTER TABLE members ADD COLUMN birth_date TEXT;
    CREATE INDEX IF NOT EXISTS idx_members_birth_date ON members(birth_date);
    ```
- **Rationale**: Garante compatibilidade total e preservação de dados existentes no banco `gd_manager.db` já em uso, sem interromper operações de desenvolvimento ou produção.
- **Alternatives Considered**:
  - *Deletar o banco e recriar*: Inviável para ambientes com dados reais ou persistentes.
  - *Ferramenta externa de migração (ex: Alembic)*: Viola o Princípio V da Constituição (Parcimônia de Dependências) para um banco embarcado monousuário/leve SQLite.

### 4. Componente de Seleção de Data no Mobile (Flutter)

- **Decision**: Utilização do `showDatePicker` nativo do Flutter Material 3 com máscara/validação local.
  - `firstDate`: `DateTime(1900, 1, 1)`
  - `lastDate`: `DateTime.now()`
  - Formatação visual no padrão brasileiro `DD/MM/AAAA`.
- **Rationale**:
  - 100% nativo do SDK Flutter (zero dependências extras no `pubspec.yaml`, atendendo ao Princípio V).
  - Experiência otimizada por toque para telas móveis (iOS e Android), responsivo e com suporte a acessibilidade.
- **Alternatives Considered**:
  - *Pacotes de terceiros (ex: `flutter_datetime_picker` ou `mask_text_input_formatter`)*: Rejeitados por violarem o Princípio V da Constituição, uma vez que o SDK padrão resolve com perfeição.

### 5. Destaque Visual e Experiência do Usuário

- **Decision**:
  - Na tela principal de listagem ([`MemberListScreen`](../../frontend/lib/presentation/screens/member_list_screen.dart)):
    - Um carrossel/linha horizontal expansível no topo com cards compactos dos aniversariantes dos próximos 30 dias.
    - Seção comemorativa quando o membro faz aniversário no dia atual (`🎂 Hoje!`).
    - Filtro de mês integrado na barra de filtros.
  - Nos cards da lista: selo discreto com dia e mês (ex: `🎂 15 de Maio`).
  - Na tela de detalhes ([`MemberDetailScreen`](../../frontend/lib/presentation/screens/member_detail_screen.dart)): linha dedicada com ícone de bolo/calendário, data completa `DD/MM/AAAA` e a idade calculada `(XX anos)`.
- **Rationale**: Atende rigorosamente às decisões validadas com o usuário (Q1: C, Q2: B) mantendo a interface leve e elegante.

### 6. Precedência de Rotas no FastAPI Router

- **Decision**: Registrar a rota estática `/birthdays/upcoming` estritamente antes das rotas dinâmicas parametrizadas (`/{id}`) no router do backend.
- **Rationale**: No FastAPI/Starlette, o roteamento avalia as regras sequencialmente. Declarar `/{id}` antes de `/birthdays/upcoming` causaria captura indevida de `"birthdays"` como parâmetro `id`, disparando erro 404 (MemberNotFoundException).
- **Alternatives Considered**: Criar um router separado para `birthdays` (desnecessário e violaria a simplicidade da estrutura).
