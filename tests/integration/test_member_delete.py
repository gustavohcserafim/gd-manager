import sqlite3
import pytest
from src.services.database import init_db
from src.services.seed import seed_initial_leaders
from src.services.member_service import create_member, delete_member, list_members
from src.domain.models import MemberCreateRequest

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_initial_leaders(conn)
    yield conn
    conn.close()

def test_delete_member_and_record_audit(db_conn):
    user = {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

    created = create_member(db_conn, MemberCreateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Membro"
    ), user)

    # Delete member
    success = delete_member(db_conn, created["id"], user)
    assert success is True

    # Check member is gone from roster
    members = list_members(db_conn)
    assert len(members) == 0

    # Check audit log recorded deletion
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM activity_logs WHERE action_type = 'DELETE_MEMBER'")
    log = cursor.fetchone()
    assert log is not None
    assert log["member_name"] == "Lucas Silva"
    assert log["user_name"] == "Pr. Pedro"

def test_delete_nonexistent_member(db_conn):
    user = {"id": 1, "name": "Pr. Pedro", "role": "Líder"}
    success = delete_member(db_conn, 99999, user)
    assert success is False
