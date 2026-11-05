# API Contracts: Member Management (GD Manager)

**Feature**: `001-member-management`
**Date**: 2026-11-05
**Base URL**: `/api`

All mutating endpoints require an authenticated user session token passed in the `Authorization: Bearer <token>` header.

---

## 1. Authentication Endpoints

### 1.1 Authenticate via PIN

- **Method**: `POST`
- **Path**: `/api/auth/pin`
- **Description**: Authenticates an administrative user by their numeric PIN and returns an active session token.

#### Request Body
```json
{
  "pin": "1234"
}
```

#### Response 200 (Success)
```json
{
  "token": "sess_eyJhbGciOi...",
  "user": {
    "id": 1,
    "name": "Pr. Pedro",
    "role": "Líder"
  }
}
```

#### Response 401 (Invalid PIN)
```json
{
  "error": "PIN inválido",
  "detail": "PIN não encontrado ou incorreto."
}
```

#### Response 429 (Rate Limit / Cooldown)
```json
{
  "error": "Muitas tentativas",
  "detail": "Limite de 5 tentativas atingido. Aguarde 30 segundos."
}
```

---

## 2. Member Management Endpoints

### 2.1 List / Search Members

- **Method**: `GET`
- **Path**: `/api/members`
- **Query Parameters**:
  - `search` (optional, string): Search term matched against member name (case and accent insensitive).
  - `position` (optional, string): Filter by role (`Líder`, `Núcleo`, `Membro`).

#### Response 200 (Success)
```json
[
  {
    "id": 1,
    "name": "Lucas Silva",
    "phone": "11987654321",
    "phoneFormatted": "(11) 98765-4321",
    "whatsappUrl": "https://wa.me/5511987654321",
    "birthDate": "15/03/1998",
    "position": "Membro",
    "createdByName": "Pr. Pedro",
    "updatedByName": "Pr. Pedro",
    "createdAt": "2026-11-05T10:00:00Z",
    "updatedAt": "2026-11-05T10:00:00Z"
  }
]
```

---

### 2.2 Create Member

- **Method**: `POST`
- **Path**: `/api/members`
- **Headers**: `Authorization: Bearer <token>`

#### Request Body
```json
{
  "name": "Lucas Silva",
  "phone": "(11) 98765-4321",
  "birthDate": "15/03/1998",
  "position": "Membro"
}
```

#### Response 201 (Created)
```json
{
  "id": 1,
  "name": "Lucas Silva",
  "phone": "11987654321",
  "phoneFormatted": "(11) 98765-4321",
  "whatsappUrl": "https://wa.me/5511987654321",
  "birthDate": "15/03/1998",
  "position": "Membro",
  "createdByName": "Pr. Pedro",
  "updatedByName": "Pr. Pedro",
  "createdAt": "2026-11-05T10:00:00Z",
  "updatedAt": "2026-11-05T10:00:00Z"
}
```

#### Response 400 (Validation Error / Duplicate Phone)
```json
{
  "error": "Telefone já cadastrado",
  "detail": "O número (11) 98765-4321 já está em uso por outro membro."
}
```

---

### 2.3 Update Member

- **Method**: `PUT`
- **Path**: `/api/members/{id}`
- **Headers**: `Authorization: Bearer <token>`

#### Request Body
```json
{
  "name": "Lucas Silva",
  "phone": "(11) 98765-4321",
  "birthDate": "15/03/1998",
  "position": "Núcleo"
}
```

#### Response 200 (Success)
```json
{
  "id": 1,
  "name": "Lucas Silva",
  "phone": "11987654321",
  "phoneFormatted": "(11) 98765-4321",
  "whatsappUrl": "https://wa.me/5511987654321",
  "birthDate": "15/03/1998",
  "position": "Núcleo",
  "createdByName": "Pr. Pedro",
  "updatedByName": "Mariana",
  "createdAt": "2026-11-05T10:00:00Z",
  "updatedAt": "2026-11-05T10:20:00Z"
}
```

---

### 2.4 Delete Member

- **Method**: `DELETE`
- **Path**: `/api/members/{id}`
- **Headers**: `Authorization: Bearer <token>`

#### Response 200 (Success)
```json
{
  "message": "Membro removido com sucesso",
  "deletedId": 1
}
```

---

## 3. Activity History Endpoint

### 3.1 Get Activity Log

- **Method**: `GET`
- **Path**: `/api/history`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `limit` (optional, default 50)

#### Response 200 (Success)
```json
[
  {
    "id": 10,
    "userName": "Mariana",
    "actionType": "UPDATE_MEMBER",
    "memberName": "Lucas Silva",
    "details": "Posição alterada de 'Membro' para 'Núcleo'",
    "timestamp": "2026-11-05T10:20:00Z"
  },
  {
    "id": 9,
    "userName": "Pr. Pedro",
    "actionType": "CREATE_MEMBER",
    "memberName": "Lucas Silva",
    "details": "Cadastrado como Membro",
    "timestamp": "2026-11-05T10:00:00Z"
  }
]
```
