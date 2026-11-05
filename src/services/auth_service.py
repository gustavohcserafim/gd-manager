import time
import secrets
import sqlite3
from typing import Optional, Dict, Any
from src.services.seed import verify_pin

# In-memory session store: token -> {user_id, name, role, expires_at}
_active_sessions: Dict[str, Dict[str, Any]] = {}

# Rate limiting: client_ip -> list of failure timestamps
_failed_attempts: Dict[str, list[float]] = {}
MAX_FAILED_ATTEMPTS = 5
COOLDOWN_SECONDS = 30
SESSION_EXPIRATION_SECONDS = 86400  # 24 hours

def reset_rate_limits() -> None:
    """Clears rate limits and active sessions (useful for tests)."""
    _failed_attempts.clear()
    _active_sessions.clear()

def check_rate_limit(client_ip: str) -> None:
    now = time.time()
    attempts = _failed_attempts.get(client_ip, [])
    # Keep only attempts within cooldown window
    recent = [t for t in attempts if now - t < COOLDOWN_SECONDS]
    _failed_attempts[client_ip] = recent

    if len(recent) >= MAX_FAILED_ATTEMPTS:
        raise PermissionError("Muitas tentativas. Limite de 5 tentativas atingido. Aguarde 30 segundos.")

def record_failed_attempt(client_ip: str) -> None:
    now = time.time()
    attempts = _failed_attempts.get(client_ip, [])
    attempts.append(now)
    _failed_attempts[client_ip] = attempts

def clear_failed_attempts(client_ip: str) -> None:
    if client_ip in _failed_attempts:
        del _failed_attempts[client_ip]

def authenticate_pin(conn: sqlite3.Connection, pin: str, client_ip: str = "127.0.0.1") -> Optional[Dict[str, Any]]:
    """Authenticates a user by numeric PIN, returning session token and user info or None."""
    check_rate_limit(client_ip)

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, role, pin_hash, active FROM users WHERE active = 1")
    users = cursor.fetchall()

    for user in users:
        if verify_pin(pin, user["pin_hash"]):
            clear_failed_attempts(client_ip)
            token = f"sess_{secrets.token_urlsafe(32)}"
            session_data = {
                "id": user["id"],
                "name": user["name"],
                "role": user["role"],
                "expires_at": time.time() + SESSION_EXPIRATION_SECONDS
            }
            _active_sessions[token] = session_data
            return {
                "token": token,
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "role": user["role"]
                }
            }

    record_failed_attempt(client_ip)
    return None

def verify_session_token(token: str) -> Optional[Dict[str, Any]]:
    """Validates session token and returns authenticated user info if active."""
    if not token or not token.startswith("sess_"):
        return None

    session = _active_sessions.get(token)
    if not session:
        return None

    if time.time() > session["expires_at"]:
        del _active_sessions[token]
        return None

    return {
        "id": session["id"],
        "name": session["name"],
        "role": session["role"]
    }
