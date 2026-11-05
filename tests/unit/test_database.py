import sqlite3
import pytest
from src.services.database import init_db

def test_init_db_creates_required_tables():
    conn = sqlite3.connect(":memory:")
    init_db(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]

    assert "users" in tables
    assert "members" in tables
    assert "activity_logs" in tables
    conn.close()

def test_members_table_has_unique_phone_constraint():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    cursor = conn.cursor()

    # Insert a user first for foreign key reference
    cursor.execute(
        "INSERT INTO users (name, pin_hash, role, active, created_at) VALUES (?, ?, ?, ?, ?)",
        ("Pr. Pedro", "hash123", "Líder", 1, "2026-11-05T10:00:00Z")
    )
    user_id = cursor.lastrowid

    # Insert member 1
    cursor.execute(
        """
        INSERT INTO members (name, phone, phone_formatted, birth_date, birth_day, birth_month, birth_year, position, created_by_user_id, updated_by_user_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        ("Lucas Silva", "11987654321", "(11) 98765-4321", "15/03/1998", 15, 3, 1998, "Membro", user_id, user_id, "2026-11-05T10:00:00Z", "2026-11-05T10:00:00Z")
    )
    conn.commit()

    # Attempt to insert member 2 with the same phone number
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            """
            INSERT INTO members (name, phone, phone_formatted, birth_date, birth_day, birth_month, birth_year, position, created_by_user_id, updated_by_user_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("Outro Lucas", "11987654321", "(11) 98765-4321", "20/04/1995", 20, 4, 1995, "Membro", user_id, user_id, "2026-11-05T10:05:00Z", "2026-11-05T10:05:00Z")
        )
        conn.commit()

    conn.close()

def test_activity_logs_table_structure():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, pin_hash, role, active, created_at) VALUES (?, ?, ?, ?, ?)",
        ("Pr. Pedro", "hash123", "Líder", 1, "2026-11-05T10:00:00Z")
    )
    user_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO activity_logs (user_id, user_name, action_type, member_id, member_name, details, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, "Pr. Pedro", "CREATE_MEMBER", 1, "Lucas Silva", '{"position": "Membro"}', "2026-11-05T10:00:00Z")
    )
    conn.commit()

    cursor.execute("SELECT user_name, action_type, member_name FROM activity_logs WHERE id = 1")
    row = cursor.fetchone()
    assert row == ("Pr. Pedro", "CREATE_MEMBER", "Lucas Silva")
    conn.close()
