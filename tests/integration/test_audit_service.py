import sqlite3
import pytest
from src.services.database import init_db
from src.services.audit_service import record_activity, get_activity_logs

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, pin_hash, role, active, created_at) VALUES (?, ?, ?, ?, ?)",
        ("Pr. Pedro", "hash", "Líder", 1, "2026-11-05T10:00:00Z")
    )
    conn.commit()
    yield conn
    conn.close()

def test_audit_logs_reverse_chronological_order(db_conn):
    record_activity(db_conn, user_id=1, user_name="Pr. Pedro", action_type="CREATE_MEMBER", member_id=1, member_name="Lucas", details="Cadastrado")
    record_activity(db_conn, user_id=1, user_name="Pr. Pedro", action_type="UPDATE_MEMBER", member_id=1, member_name="Lucas", details="Posição alterada")
    record_activity(db_conn, user_id=1, user_name="Pr. Pedro", action_type="DELETE_MEMBER", member_id=1, member_name="Lucas", details="Removido")

    logs = get_activity_logs(db_conn, limit=10)
    assert len(logs) == 3
    # First item is the most recent (DELETE)
    assert logs[0]["actionType"] == "DELETE_MEMBER"
    assert logs[1]["actionType"] == "UPDATE_MEMBER"
    assert logs[2]["actionType"] == "CREATE_MEMBER"
