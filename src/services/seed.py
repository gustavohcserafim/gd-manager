import sqlite3
import hashlib
import secrets
from datetime import datetime, timezone

def hash_pin(pin: str, salt: str | None = None) -> str:
    """Hashes a numeric PIN using SHA-256 with a cryptographic salt."""
    if salt is None:
        salt = secrets.token_hex(8)
    hashed = hashlib.sha256(f"{salt}:{pin}".encode("utf-8")).hexdigest()
    return f"{salt}${hashed}"

def verify_pin(pin: str, stored_hash: str) -> bool:
    """Verifies a plain PIN against a stored salted hash."""
    try:
        salt, _ = stored_hash.split("$", 1)
        expected = hash_pin(pin, salt=salt)
        return secrets.compare_digest(expected, stored_hash)
    except Exception:
        return False

INITIAL_LEADERS = [
    {"name": "Pr. Pedro", "role": "Líder", "pin": "1234"},
    {"name": "Mariana", "role": "Núcleo", "pin": "5678"},
    {"name": "Lucas", "role": "Núcleo", "pin": "4321"},
]

def seed_initial_leaders(conn: sqlite3.Connection) -> int:
    """
    Inserts initial Onda Mooca leadership accounts if users table is empty.
    Returns the number of users seeded.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count > 0:
        return 0

    now = datetime.now(timezone.utc).isoformat()
    inserted = 0

    for leader in INITIAL_LEADERS:
        pin_hash = hash_pin(leader["pin"])
        cursor.execute(
            """
            INSERT INTO users (name, pin_hash, role, active, created_at)
            VALUES (?, ?, ?, 1, ?)
            """,
            (leader["name"], pin_hash, leader["role"], now)
        )
        inserted += 1

    conn.commit()
    return inserted
