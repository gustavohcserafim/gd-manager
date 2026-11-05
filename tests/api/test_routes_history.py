import pytest
from src.services.database import get_db_connection
from src.services.audit_service import record_activity
from src.api.routes_history import get_history_route

@pytest.fixture
def auth_user():
    return {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

def test_get_history_route_success(auth_user):
    conn = get_db_connection()
    record_activity(conn, user_id=1, user_name="Pr. Pedro", action_type="CREATE_MEMBER", member_id=1, member_name="Lucas", details="Cadastrado como Membro")
    conn.close()

    history = get_history_route(limit=10, current_user=auth_user)
    assert len(history) >= 1
    assert history[0]["userName"] == "Pr. Pedro"
    assert history[0]["actionType"] == "CREATE_MEMBER"
    assert history[0]["memberName"] == "Lucas"
