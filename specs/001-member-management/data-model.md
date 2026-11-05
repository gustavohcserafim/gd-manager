# Data Model: Member Management (GD Manager)

**Feature**: `001-member-management`
**Date**: 2026-11-05
**Status**: Final

## 1. Entities & Schema

### 1.1 `users` (`UsuarioAdministrativo`)

Represents an authorized leader or core member who can log in with a PIN and perform management operations.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique identifier for the administrative user |
| `name` | `TEXT` | NOT NULL, Min 2 chars | Full display name (e.g., "Pr. Pedro", "Mariana") |
| `pin_hash` | `TEXT` | NOT NULL | Salted SHA-256 hash of the personal numeric PIN |
| `role` | `TEXT` | NOT NULL, IN ('Líder', 'Núcleo') | Administrative classification within the GD |
| `active` | `INTEGER` | NOT NULL, DEFAULT 1 | Boolean flag (1=Active, 0=Inactive) |
| `created_at` | `TEXT` | NOT NULL, ISO-8601 UTC | Record creation timestamp |

**Indexes**:
- `idx_users_active`: On `(active)` for fast lookups.

---

### 1.2 `members` (`Membro`)

Represents a member or participant in the Onda Mooca discipleship group (GD).

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique identifier for the member |
| `name` | `TEXT` | NOT NULL, Min 2 chars | Full name of the member |
| `phone` | `TEXT` | NOT NULL, UNIQUE | Clean digits (10 or 11 digits, e.g. "11987654321") |
| `phone_formatted` | `TEXT` | NOT NULL | Display mask, e.g. "(11) 98765-4321" |
| `birth_date` | `TEXT` | NOT NULL | Birthday string in PT-BR format ("DD/MM/AAAA" or "DD/MM") |
| `birth_day` | `INTEGER` | NOT NULL, 1..31 | Extracted day for sorting and upcoming birthday filters |
| `birth_month` | `INTEGER` | NOT NULL, 1..12 | Extracted month for sorting and upcoming birthday filters |
| `birth_year` | `INTEGER` | NULL | Extracted year if provided (optional) |
| `position` | `TEXT` | NOT NULL, IN ('Líder', 'Núcleo', 'Membro') | Member's spiritual/service role in the GD |
| `created_by_user_id`| `INTEGER` | NOT NULL, References `users(id)` | ID of the user who registered this member |
| `updated_by_user_id`| `INTEGER` | NOT NULL, References `users(id)` | ID of the user who last edited this member |
| `created_at` | `TEXT` | NOT NULL, ISO-8601 UTC | Timestamp of member creation |
| `updated_at` | `TEXT` | NOT NULL, ISO-8601 UTC | Timestamp of last modification |

**Indexes**:
- `idx_members_phone_unique`: Unique index on `phone`.
- `idx_members_name`: On `name COLLATE NOCASE` for fast search.
- `idx_members_position`: On `position` for filtering.
- `idx_members_birthday`: On `(birth_month, birth_day)` for birthday sorting.

---

### 1.3 `activity_logs` (`RegistroAtividade`)

Immutable chronological audit log capturing all member administrative actions.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique identifier for the log event |
| `user_id` | `INTEGER` | NOT NULL, References `users(id)` | User who executed the action |
| `user_name` | `TEXT` | NOT NULL | Snapshot of user name at time of action |
| `action_type` | `TEXT` | NOT NULL, IN ('CREATE_MEMBER', 'UPDATE_MEMBER', 'DELETE_MEMBER') | Type of operation performed |
| `member_id` | `INTEGER` | NULL | ID of the affected member (NULL if deleted) |
| `member_name` | `TEXT` | NOT NULL | Snapshot of member name |
| `details` | `TEXT` | NULL | JSON string describing changes (e.g. `{"position": {"from": "Membro", "to": "Núcleo"}}`) |
| `created_at` | `TEXT` | NOT NULL, ISO-8601 UTC | Timestamp of the action |

**Indexes**:
- `idx_logs_created_at_desc`: On `created_at DESC` for fast reverse-chronological retrieval.
- `idx_logs_user_id`: On `user_id`.

---

## 2. Validation Rules & Domain Constraints

### 2.1 Brazilian Phone Number Validation
- Raw input stripped of non-digits: `digits = re.sub(r'\D', '', raw_input)`
- Length must be either:
  - 10 digits: `(AA) NNNN-NNNN` (Landline format, area code `AA` between 11 and 99, 1st digit 2..5)
  - 11 digits: `(AA) 9NNNN-NNNN` (Mobile format, area code `AA` between 11 and 99, 1st digit must be 9)
- Formatting mask applied on output: `(XX) XXXXX-XXXX` or `(XX) XXXX-XXXX`
- WhatsApp link: `https://wa.me/55{digits}`
- Uniqueness: Must not exist in `members` table for another member.

### 2.2 PT-BR Birthday Validation
- Pattern: `^([0-3]?[0-9])/([0-1]?[0-9])(/([1-2][0-9]{3}))?$`
- Day and month extraction:
  - Month must be `01 <= month <= 12`.
  - Day must be valid for the given month (e.g., maximum 31 for Jan, 30 for Apr, 28/29 for Feb).
  - If year is provided: `1900 <= year <= current_year`. Leap year validation applies for Feb 29.
- Normalized storage: stored as standard PT-BR string `DD/MM/AAAA` or `DD/MM`.

### 2.3 Position Validation
- Must be strictly one of: `['Líder', 'Núcleo', 'Membro']`.

---

## 3. Pre-configured Seed Dataset

On first startup, if `users` table contains zero records, the following administrative users are inserted:

```json
[
  {
    "name": "Pr. Pedro",
    "role": "Líder",
    "pin": "1234",
    "active": 1
  },
  {
    "name": "Mariana",
    "role": "Núcleo",
    "pin": "5678",
    "active": 1
  },
  {
    "name": "Lucas",
    "role": "Núcleo",
    "pin": "4321",
    "active": 1
  }
]
```
*(PINs are hashed via SHA-256 with salt prior to database storage)*.
