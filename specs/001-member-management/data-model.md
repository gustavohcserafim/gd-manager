# Data Model: Cadastro e Gestão de Membros (CRUD)

**Feature**: `001-member-management`  
**Date**: 2026-11-03  
**Status**: Completed  

---

## 1. Entidade de Domínio: `Member` (Membro)

A entidade central do domínio representa os integrantes do grupo e suas respectivas funções e status cadastrais.

### Atributos

| Campo | Tipo | Obrigatório | Padrão | Descrição e Regras de Validação |
|---|---|---|---|---|
| `id` | `UUID` (string v4) | Sim | Gerado | Identificador único universal imutável. |
| `name` | `string` | Sim | - | Nome completo do membro. Mínimo 3 caracteres, máximo 150 caracteres. Espaços no início e fim são removidos. |
| `phone` | `string` | Sim | - | Telefone ou WhatsApp de contato. Formato canônico numérico sanitizado (ex: `+5511999999999` ou `11999999999`). **Único entre membros ativos**. |
| `email` | `string` (opcional) | Não | `null` | Endereço de e-mail opcional. Se informado, deve ter formato de e-mail válido (`user@domain.com`). |
| `role` | `MemberRole` (Enum) | Sim | `normal` | Categoria de atuação: `leader`, `core`, `normal`. |
| `status` | `MemberStatus` (Enum) | Sim | `active` | Situação cadastral: `active` ou `inactive`. |
| `created_at` | `DateTime` (ISO 8601) | Sim | UTC Now | Momento do cadastro original no sistema. |
| `updated_at` | `DateTime` (ISO 8601) | Sim | UTC Now | Momento da última alteração de dados ou status. |

---

## 2. Tipos Enumerados (Enums de Domínio)

### `MemberRole` (Tipo de Membro)
- `leader` (*Líder*): Responsável pela liderança e condução do grupo. Possui privilégios totais de leitura e escrita.
- `core` (*Membro do núcleo*): Integrante ativo do núcleo gestor/apoio. Possui privilégios totais de leitura e escrita.
- `normal` (*Normal*): Membro regular do grupo. Possui acesso estritamente restrito à consulta e visualização de membros ativos.

### `MemberStatus` (Status Cadastral)
- `active` (*Ativo*): Membro em plena participação no grupo. Participa da listagem regular e exige unicidade do número de telefone.
- `inactive` (*Inativo*): Membro que deixou o grupo (inativação lógica / soft delete). Oculto da listagem comum, visível apenas na visualização filtrada de inativos por Líder e Núcleo.

---

## 3. Máquina de Estados e Transições de Ciclo de Vida

```text
       [ Formulário de Cadastro ]
                   │
                   ▼ (Criar Membro)
             ┌───────────┐
             │   ACTIVE  │◄────────────────┐
             └─────┬─────┘                 │
                   │                       │ (Reativar Membro:
                   │ (Inativar Membro:     │  revalida unicidade
                   │  soft delete)         │  de telefone ativo)
                   ▼                       │
             ┌───────────┐                 │
             │  INACTIVE ├─────────────────┘
             └───────────┘
```

### Regras de Transição de Estado:
1. **Criação**: Novo membro nasce sempre com status `active`. O telefone fornecido é verificado; se já existir outro membro com status `active` e o mesmo `phone`, a criação falha com exceção de domínio `DuplicatePhoneException`.
2. **Atualização**: Apenas membros `active` podem ter seus dados cadastrais alterados. Se o telefone for alterado para um número pertencente a outro membro ativo, a operação falha com `DuplicatePhoneException`.
3. **Inativação (Soft Delete)**: Membro com status `active` transiciona para `inactive`. Não há exclusão física de registros do banco de dados para preservar integridade e histórico.
4. **Reativação**: Membro com status `inactive` transiciona para `active`. **Validação obrigatória**: se durante o período de inatividade outro membro ativo foi cadastrado com o mesmo telefone, a reativação é rejeitada até que o telefone seja modificado.

---

## 4. Esquema de Persistência (SQLite DDL)

```sql
CREATE TABLE IF NOT EXISTS members (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    role TEXT NOT NULL CHECK (role IN ('leader', 'core', 'normal')),
    status TEXT NOT NULL CHECK (status IN ('active', 'inactive')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Índice para busca rápida e ordenação por nome
CREATE INDEX IF NOT EXISTS idx_members_name ON members(name COLLATE NOCASE);

-- Índice para filtragem eficiente por status e tipo
CREATE INDEX IF NOT EXISTS idx_members_status_role ON members(status, role);

-- Índice parcial de unicidade: garante que telefones não se repitam entre membros ativos
CREATE UNIQUE INDEX IF NOT EXISTS idx_members_active_phone 
ON members(phone) 
WHERE status = 'active';
```

---

## 5. DTOs (Data Transfer Objects) e Contratos de Dados

### `CreateMemberDTO`
- `name`: string (3..150 chars, obrigatório)
- `phone`: string (obrigatório, numérico formatado)
- `email`: string (opcional)
- `role`: string (`leader` | `core` | `normal`, obrigatório, default `normal`)

### `UpdateMemberDTO`
- `name`: string (3..150 chars, opcional/completo)
- `phone`: string (opcional/completo)
- `email`: string (opcional)
- `role`: string (`leader` | `core` | `normal`, opcional/completo)

### `MemberResponseDTO`
- `id`: string (UUID)
- `name`: string
- `phone`: string
- `email`: string ou null
- `role`: string (`leader` | `core` | `normal`)
- `status`: string (`active` | `inactive`)
- `initials`: string (ex: "Gustavo Dias" -> "GD")
- `created_at`: string (ISO 8601)
- `updated_at`: string (ISO 8601)
