# Research & Technical Decisions: Gestão de Aniversários de Membros

**Feature**: `002-member-birthdays` | **Date**: 2026-11-04 (Atualizado com formato `DD/MM/AAAA`)

## Overview

Este documento consolida as pesquisas técnicas, decisões de arquitetura e justificativas de engenharia para a implementação da gestão de aniversários no GD Manager, com ênfase na padronização de preenchimento e exibição no formato `DD/MM/AAAA` (`dd/mm/YYYY`), respeitando os princípios da [Constituição do GD Manager](../../.specify/memory/constitution.md) (Clean Architecture, TDD, Mobile-First, Custo Zero e Parcimônia de Dependências).

---

## Technical Decisions

### 1. Formato de Preenchimento, Exibição e Armazenamento

- **Decision**: 
  - **Interface do Usuário (Preenchimento e Exibição)**: Estritamente no padrão brasileiro `DD/MM/AAAA` (`dd/mm/YYYY`).
  - **Trânsito na API (DTOs Pydantic)**: Suporte dual resiliente — aceita tanto `DD/MM/AAAA` quanto ISO `YYYY-MM-DD`, convertendo para `datetime.date`.
  - **Persistência no SQLite**: `TEXT` no padrão ISO 8601 estrito (`YYYY-MM-DD`).
- **Rationale**:
  - Para o usuário brasileiro, `DD/MM/AAAA` é intuitivo e elimina ambiguidades entre mês e dia.
  - Para o banco de dados relacional (SQLite), `YYYY-MM-DD` preserva a ordenabilidade cronológica natural e compatibilidade com funções embutidas de data (`strftime('%m', birth_date)`).
  - O desacoplamento através de adaptadores e validadores Pydantic segue rigorosamente o Princípio I da Clean Architecture (camadas externas adaptam dados para o domínio).
- **Alternatives Considered**:
  - *Armazenar `DD/MM/AAAA` diretamente no SQLite*: Rejeitado porque quebraria a capacidade do SQLite de ordenar cronologicamente por `birth_date` (ex: `01/12/2000` viria antes de `15/01/1990` em ordenação alfabética).
  - *Forçar o usuário a digitar `AAAA-MM-DD`*: Rejeitado por atrito na experiência móvel brasileira e violação do Princípio III (Mobile-First).

### 2. Máscara de Entrada de Data no Flutter sem Dependências Externas

- **Decision**: Criação de um `DateInputFormatter` estendendo a classe nativa do Flutter `TextInputFormatter`:
  - Intercepta a digitação e insere automaticamente os caracteres de barra `/` após o dia (2 dígitos) e após o mês (2 dígitos).
  - Limita o comprimento máximo a 10 caracteres (`DD/MM/AAAA`).
  - Permite tanto a digitação direta assistida quanto o preenchimento automático pelo calendário `showDatePicker`.
- **Rationale**:
  - Respeita o Princípio V da Constituição (Parcimônia Extrema de Dependências): não adiciona bibliotecas pesadas de formatação como `mask_text_input_formatter`.
  - Proporciona usabilidade ágil e intuitiva no celular (Mobile-First).
- **Alternatives Considered**:
  - *Instalar pacote `mask_text_input_formatter`*: Rejeitado para honrar o Princípio V e evitar dependências desnecessárias.
  - *Apenas seleção por DatePicker sem digitação manual*: Rejeitado porque usuários experientes muitas vezes preferem digitar rapidamente 8 dígitos numéricos em vez de navegar anos em um calendário.

### 3. Validação Resiliente nos DTOs do Backend (Pydantic v2)

- **Decision**: Inclusão de `@field_validator('birth_date', mode='before')` nos DTOs `CreateMemberDTO` e `UpdateMemberDTO`:
  ```python
  @field_validator("birth_date", mode="before")
  @classmethod
  def parse_birth_date(cls, v: Any) -> Any:
      if isinstance(v, str):
          v = v.strip()
          # Tenta primeiro formato brasileiro DD/MM/AAAA
          if "/" in v:
              try:
                  return datetime.strptime(v, "%d/%m/%Y").date()
              except ValueError:
                  raise ValueError("Data de nascimento inválida. Use o formato DD/MM/AAAA.")
          # Suporta formato ISO YYYY-MM-DD
          try:
              return datetime.strptime(v, "%Y-%m-%d").date()
          except ValueError:
              raise ValueError("Data de nascimento inválida. Use o formato DD/MM/AAAA.")
      return v
  ```
- **Rationale**:
  - Permite que requisições HTTP enviem payloads naturais com `"15/05/1990"` ou `"1990-05-15"`.
  - Respostas com HTTP 400 claras e educativas quando o formato estiver inconsistente.
- **Alternatives Considered**:
  - *Aceitar apenas ISO e exigir que o frontend converta*: Aceitável, mas oferecer suporte flexível no backend protege a API contra quebras se clientes externos enviarem `DD/MM/AAAA`.

### 4. Algoritmo de Cálculo de Idade e Próximos Aniversariantes

- **Decision**:
  - **Idade**: Calculada comparando tuplas `(hoje.month, hoje.day) < (nascimento.month, nascimento.day)`:
    $$\text{idade} = \text{hoje.year} - \text{nascimento.year} - (1 \text{ se aniversário ainda não ocorreu este ano senão } 0)$$
  - **Próximos Aniversariantes (próximos 30 dias)**:
    - Projeta o aniversário no ano atual; se já passou, projeta no próximo ano.
    - Se a diferença de dias $\ge 0$ e $\le 30$, inclui na lista em ordem cronológica crescente.
  - **Anos Bissextos (29 de Fevereiro)**:
    - Em anos não bissextos, ajusta a data projetada para 28 de Fevereiro.
- **Rationale**: Solução pura e determinística em Python e Dart.

### 5. Destaque Visual e Telas no Mobile (Flutter)

- **Decision**:
  - **Formulário** ([`MemberFormScreen`](../../frontend/lib/presentation/screens/member_form_screen.dart)): Campo de texto com máscara `DD/MM/AAAA`, ícone de calendário com toque abrindo o `showDatePicker`, populando o campo formatado em `DD/MM/AAAA`.
  - **Detalhes** ([`MemberDetailScreen`](../../frontend/lib/presentation/screens/member_detail_screen.dart)): Exibe a data de nascimento estritamente como `DD/MM/AAAA (XX anos)`.
  - **Listagem** ([`MemberListScreen`](../../frontend/lib/presentation/screens/member_list_screen.dart)): Carrossel superior de aniversariantes dos próximos 30 dias e filtro mensal.
- **Rationale**: Alinhamento estrito aos requisitos funcionais e de usabilidade móvel.
