# Data Model: Gestão de Aniversários de Membros

**Feature**: `002-member-birthdays` | **Date**: 2026-11-04

## Entity Definitions

### 1. Membro (`Member`)

A entidade central de domínio é estendida com o atributo de data de nascimento e métodos de cálculo de aniversário.

| Campo | Tipo (Python) | Tipo (Dart) | SQLite | Descrição & Regras de Validação |
|---|---|---|---|---|
| `id` | `str` (UUID v4) | `String` | `TEXT PRIMARY KEY` | Identificador único imutável do membro. |
| `name` | `str` | `String` | `TEXT NOT NULL` | Nome completo (3 a 150 caracteres). |
| `phone` | `str` | `String` | `TEXT NOT NULL` | Telefone único entre membros ativos. |
| `email` | `Optional[str]` | `String?` | `TEXT` | E-mail de contato opcional formatado. |
| `role` | `MemberRole` | `MemberRole` | `TEXT NOT NULL` | `leader`, `core`, `normal`. |
| `status` | `MemberStatus` | `MemberStatus` | `TEXT NOT NULL` | `active`, `inactive`. |
| `birth_date` | `Optional[date]` | `DateTime?` | `TEXT` | Data de nascimento no formato ISO `YYYY-MM-DD`. Obrigatória em cadastros e atualizações. Nullable no domínio para registros legados. |
| `created_at` | `datetime` | `DateTime` | `TEXT NOT NULL` | Data/hora UTC de criação. |
| `updated_at` | `datetime` | `DateTime` | `TEXT NOT NULL` | Data/hora UTC da última alteração. |

### 2. Atributos Computados de Domínio (`Member`)

Estes atributos não são persistidos em colunas separadas do banco, sendo calculados dinamicamente pelas entidades puras de domínio:

- **`age -> Optional[int]`**: Idade completada em anos calculada em relação à data atual do sistema. Retorna `None`/`null` se `birth_date` não estiver preenchido.
- **`birthday_display -> Optional[str]`**: Representação amigável do dia e mês em português (ex: `"15 de Maio"`).
- **`is_birthday_today -> bool`**: Retorna `True` caso o dia e mês da data de nascimento coincidam com a data de hoje (com suporte a 29 de fevereiro caindo em 28 de fevereiro em anos não bissextos).
- **`days_until_birthday -> Optional[int]`**: Número de dias restantes até o próximo aniversário (0 se for hoje, até 365).

---

## DTOs & Contratos de Dados

### 1. `CreateMemberRequest` (Atualizado)
```python
class CreateMemberRequest(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    phone: str = Field(min_length=8, max_length=20)
    email: Optional[EmailStr] = None
    role: MemberRole = MemberRole.NORMAL
    birth_date: date = Field(..., description="Data de nascimento obrigatória no formato YYYY-MM-DD")
```

### 2. `UpdateMemberRequest` (Atualizado)
```python
class UpdateMemberRequest(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    phone: str = Field(min_length=8, max_length=20)
    email: Optional[EmailStr] = None
    role: MemberRole
    birth_date: date = Field(..., description="Data de nascimento obrigatória no formato YYYY-MM-DD")
```

### 3. `MemberResponse` (Atualizado)
```python
class MemberResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: Optional[str] = None
    role: MemberRole
    status: MemberStatus
    birth_date: Optional[date] = None
    age: Optional[int] = None
    birthday_display: Optional[str] = None
    is_birthday_today: bool = False
    days_until_birthday: Optional[int] = None
    initials: str
    created_at: datetime
    updated_at: datetime
```

---

## Esquema SQLite & Migração DDL

```sql
-- Adição idempotente da coluna de data de nascimento na tabela members
ALTER TABLE members ADD COLUMN birth_date TEXT;

-- Índice para acelerar ordenações e filtros por data de nascimento
CREATE INDEX IF NOT EXISTS idx_members_birth_date ON members(birth_date);
```

---

## Invariantes e Regras de Validação

1. **Obrigatoriedade**: Em novas criações e edições, `birth_date` não pode ser nulo nem vazio.
2. **Proibição de Data Futura**: `birth_date <= date.today()`. Tentativas de envio de datas futuras devem disparar `ValidationException` (HTTP 400).
3. **Limite Inferior de Idade**: `birth_date.year >= 1900`. Idades superiores a 120 anos disparam `ValidationException` (HTTP 400).
4. **Ano Bissexto**: Nascidos em 29 de fevereiro são tratados com aniversário no dia 28 de fevereiro em anos não bissextos.
