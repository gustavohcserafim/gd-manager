from src.services.database import get_db_connection
from src.services.auth_service import authenticate_pin, reset_rate_limits
from src.domain.models import MemberCreateRequest, MemberUpdateRequest
from src.services.member_service import (
    create_member,
    list_members,
    update_member,
    delete_member,
)
from src.services.audit_service import get_activity_logs
import pytest


def test_quickstart_scenarios_e2e():
    conn = get_db_connection()
    reset_rate_limits()

    try:
        # Scenario A: PIN Unlock & Seed Data Authentication
        auth_result = authenticate_pin(conn, "1234")
        assert auth_result is not None
        user = auth_result["user"]
        assert user["name"] == "Pr. Pedro"
        assert user["role"] == "Líder"

        # Scenario B: Register New Member (Lucas Silva)
        create_req = MemberCreateRequest(
            name="Lucas Silva",
            phone="(11) 98765-4321",
            birthDate="15/03/1998",
            position="Membro",
        )
        member_b = create_member(conn, create_req, user)
        assert member_b["id"] is not None
        assert member_b["name"] == "Lucas Silva"
        assert member_b["phoneFormatted"] == "(11) 98765-4321"
        assert member_b["position"] == "Membro"

        # Check member is listed
        members = list_members(conn)
        assert len(members) == 1
        assert members[0]["id"] == member_b["id"]

        # Scenario C: Duplicate Phone Validation (Edge Case)
        with pytest.raises(ValueError, match="já cadastrado"):
            dup_req = MemberCreateRequest(
                name="Outro Membro",
                phone="(11) 98765-4321",
                birthDate="01/01/2000",
                position="Membro",
            )
            create_member(conn, dup_req, user)

        # Scenario D: Member Edit & Position Change
        update_req = MemberUpdateRequest(
            name="Lucas Silva",
            phone="(11) 98765-4321",
            birthDate="15/03/1998",
            position="Núcleo",
        )
        updated_b = update_member(conn, member_b["id"], update_req, user)
        assert updated_b["position"] == "Núcleo"

        # Scenario E: Audit History Verification
        logs = get_activity_logs(conn)
        assert len(logs) == 2
        # Reverse-chronological: latest is UPDATE_MEMBER
        assert logs[0]["actionType"] == "UPDATE_MEMBER"
        assert logs[0]["userName"] == "Pr. Pedro"
        assert "Posição alterada" in logs[0]["details"]

        # Second is CREATE_MEMBER
        assert logs[1]["actionType"] == "CREATE_MEMBER"
        assert logs[1]["userName"] == "Pr. Pedro"

        # Scenario F: Delete Member with Confirmation
        deleted = delete_member(conn, member_b["id"], user)
        assert deleted is True

        # Check roster is empty
        assert len(list_members(conn)) == 0

        # Check audit logs now has 3 entries
        final_logs = get_activity_logs(conn)
        assert len(final_logs) == 3
        assert final_logs[0]["actionType"] == "DELETE_MEMBER"
        assert final_logs[0]["memberName"] == "Lucas Silva"
    finally:
        conn.close()
