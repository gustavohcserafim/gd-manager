# Quickstart & Validation Guide: Member Management (GD Manager)

**Feature**: `001-member-management`
**Date**: 2026-11-05
**Status**: Ready for Implementation

This guide provides step-by-step instructions to validate the GD Manager member management feature end-to-end, from automated test execution to manual verification of the PWA in browser profiles.

---

## 1. Prerequisites & Environment Setup

- **Python**: Version 3.14+ (includes `pytest`, `fastapi`, `uvicorn`, `httpx`).
- **Dependencies**: Verified installed in current Python environment.
- **Port**: Default local port `8000`.

---

## 2. Automated Test Execution (TDD Verification)

Run the full automated test suite using `pytest`:

```bash
# Execute all unit, integration, and API tests
python -m pytest tests/ -v
```

### Expected Test Suite Outcomes:
1. `tests/unit/test_validators.py`:
   - Validates PT-BR phone numbers (10 and 11 digits, masking, non-digit stripping).
   - Validates PT-BR birthdays (rejects `31/02`, accepts `DD/MM` and `DD/MM/AAAA`).
   - Validates position enumeration (`Líder`, `Núcleo`, `Membro`).
2. `tests/unit/test_auth.py`:
   - Validates PIN hashing, verification, session token generation, and 5-attempt rate-limiting lockout.
3. `tests/integration/test_member_crud.py`:
   - Verifies Member creation, listing, updating, deletion, and duplicate phone rejection.
   - Verifies audit log creation on each mutation.
4. `tests/api/test_api_endpoints.py`:
   - Tests HTTP contracts for `/api/auth/pin`, `/api/members`, and `/api/history`.

---

## 3. Launching the GD Manager PWA Locally

Start the local server:

```bash
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

The application will be accessible at: `http://127.0.0.1:8000`

---

## 4. End-to-End User Scenario Validation

### Scenario A: PIN Unlock & Seed Data Authentication
1. Open `http://127.0.0.1:8000` in your browser.
2. The PIN lock screen appears.
3. Enter seed PIN `1234` (Pr. Pedro).
4. **Expected Outcome**: Screen unlocks in <1 second, greeting "Olá, Pr. Pedro" appears, and member roster view is displayed.

### Scenario B: Register New Member (P1 Flow)
1. Click the **"+ Novo Membro"** button.
2. Fill in the form:
   - **Nome**: `Lucas Silva`
   - **Telefone / WhatsApp**: `(11) 98765-4321`
   - **Data de Aniversário**: `15/03/1998`
   - **Posição**: `Membro`
3. Click **"Salvar"**.
4. **Expected Outcome**:
   - Modal closes and `Lucas Silva` appears in the roster with role badge "Membro".
   - Tapping the WhatsApp icon initiates link `https://wa.me/5511987654321`.

### Scenario C: Duplicate Phone Validation (Edge Case)
1. Attempt to register another member with the exact same phone number `(11) 98765-4321`.
2. Click **"Salvar"**.
3. **Expected Outcome**: Submission is rejected; an inline alert indicates "O número (11) 98765-4321 já está em uso por outro membro."

### Scenario D: Member Edit & Position Change (P2 Flow)
1. Click the edit icon on `Lucas Silva`.
2. Change position to `Núcleo`.
3. Click **"Salvar"**.
4. **Expected Outcome**: The badge for Lucas Silva updates to "Núcleo".

### Scenario E: Audit History Verification
1. Navigate to the **"Histórico"** tab / screen.
2. **Expected Outcome**:
   - Entry 1 shows: `Pr. Pedro cadastrou Lucas Silva como Membro`.
   - Entry 2 shows: `Pr. Pedro alterou posição de Lucas Silva para Núcleo`.

### Scenario F: Delete Member with Confirmation (P3 Flow)
1. Return to the roster and click the delete trash icon for `Lucas Silva`.
2. A confirmation dialog appears asking: *"Tem certeza que deseja remover Lucas Silva do GD?"*.
3. Click **"Confirmar"**.
4. **Expected Outcome**: `Lucas Silva` is removed from the active roster. A new audit entry records the deletion.

### Scenario G: PWA Offline Resilience
1. In browser DevTools > Network, toggle to **"Offline"**.
2. Refresh the page.
3. **Expected Outcome**:
   - The PWA loads completely from Service Worker cache.
   - Roster data is readable from local cache.
