import sqlite3
from src.services.database import init_db
from src.services.seed import seed_initial_leaders, hash_pin, verify_pin

def test_seed_initial_leaders_populates_three_users():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)

    count = seed_initial_leaders(conn)
    assert count == 3

    cursor = conn.cursor()
    cursor.execute("SELECT name, role, pin_hash FROM users ORDER BY id")
    rows = cursor.fetchall()

    assert len(rows) == 3
    assert rows[0]["name"] == "Pr. Pedro"
    assert rows[0]["role"] == "Líder"
    assert verify_pin("1234", rows[0]["pin_hash"])

    assert rows[1]["name"] == "Mariana"
    assert rows[1]["role"] == "Núcleo"
    assert verify_pin("5678", rows[1]["pin_hash"])

    assert rows[2]["name"] == "Lucas"
    assert rows[2]["role"] == "Núcleo"
    assert verify_pin("4321", rows[2]["pin_hash"])
    conn.close()

def test_seed_initial_leaders_is_idempotent():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)

    first_run = seed_initial_leaders(conn)
    second_run = seed_initial_leaders(conn)

    assert first_run == 3
    assert second_run == 0

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    assert total == 3
    conn.close()
