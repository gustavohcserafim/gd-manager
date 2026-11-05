import sqlite3
import pytest
from src.services.database import init_db
from src.services.seed import seed_initial_leaders
from src.services.member_service import create_member, list_members
from src.domain.models import MemberCreateRequest

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_initial_leaders(conn)
    yield conn
    conn.close()

def test_create_and_list_member_with_audit_log(db_conn):
    user = {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

    req = MemberCreateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Membro"
    )

    created = create_member(db_conn, req, user)
    assert created["id"] is not None
    assert created["name"] == "Lucas Silva"
    assert created["phone"] == "11987654321"
    assert created["phoneFormatted"] == "(11) 98765-4321"
    assert created["whatsappUrl"] == "https://wa.me/5511987654321"
    assert created["position"] == "Membro"
    assert created["createdByName"] == "Pr. Pedro"

    # Verify audit log was recorded
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM activity_logs WHERE member_id = ?", (created["id"],))
    log = cursor.fetchone()
    assert log is not None
    assert log["action_type"] == "CREATE_MEMBER"
    assert log["user_name"] == "Pr. Pedro"
    assert log["member_name"] == "Lucas Silva"

    # Verify list members
    members = list_members(db_conn)
    assert len(members) == 1
    assert members[0]["name"] == "Lucas Silva"

def test_create_member_duplicate_phone_rejected(db_conn):
    user = {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

    req1 = MemberCreateRequest(
        name="Lucas Silva",
        phone="(11) 98765-4321",
        birthDate="15/03/1998",
        position="Membro"
    )
    create_member(db_conn, req1, user)

    req2 = MemberCreateRequest(
        name="Outro Membro",
        phone="11987654321",  # Same digits, different formatting
        birthDate="10/10/2000",
        position="Membro"
    )
    with pytest.raises(ValueError) as exc:
        create_member(db_conn, req2, user)
    assert "Telefone já cadastrado" in str(exc.value)
