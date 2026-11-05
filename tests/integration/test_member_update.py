import sqlite3
import pytest
from src.services.database import init_db
from src.services.seed import seed_initial_leaders
from src.services.member_service import create_member, update_member
from src.domain.models import MemberCreateRequest, MemberUpdateRequest

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_initial_leaders(conn)
    yield conn
    conn.close()

def test_update_member_and_audit_diff(db_conn):
    user_creator = {"id": 1, "name": "Pr. Pedro", "role": "Líder"}
    user_editor = {"id": 2, "name": "Mariana", "role": "Núcleo"}

    created = create_member(db_conn, MemberCreateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Membro"
    ), user_creator)

    # Mariana promotes Lucas to Núcleo
    updated = update_member(db_conn, created["id"], MemberUpdateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Núcleo"
    ), user_editor)

    assert updated["position"] == "Núcleo"
    assert updated["updatedByName"] == "Mariana"

    # Verify audit log diff
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM activity_logs WHERE member_id = ? AND action_type = 'UPDATE_MEMBER'", (created["id"],))
    log = cursor.fetchone()
    assert log is not None
    assert log["user_name"] == "Mariana"
    assert "Núcleo" in log["details"]

def test_update_member_phone_collision(db_conn):
    user = {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

    m1 = create_member(db_conn, MemberCreateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Membro"
    ), user)

    m2 = create_member(db_conn, MemberCreateRequest(
        name="Ana Paula",
        phone="(11) 91234-5678",
        birthDate="20/07/1995",
        position="Membro"
    ), user)

    # Trying to update Ana's phone to Lucas's phone should fail
    with pytest.raises(ValueError) as exc:
        update_member(db_conn, m2["id"], MemberUpdateRequest(
            name="Ana Paula",
            phone="(11) 98765-4321",
            birthDate="20/07/1995",
            position="Membro"
        ), user)
    assert "Telefone já cadastrado" in str(exc.value)
