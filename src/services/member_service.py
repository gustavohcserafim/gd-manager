import sqlite3
import unicodedata
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from src.domain.validators import (
    validate_and_format_phone,
    validate_and_parse_birth_date,
    validate_position,
)
from src.domain.models import MemberCreateRequest, MemberUpdateRequest
from src.services.audit_service import record_activity

def strip_accents(text: str) -> str:
    """Removes accents for case- and accent-insensitive matching."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    ).lower()

def create_member(conn: sqlite3.Connection, data: MemberCreateRequest, current_user: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a new member and records an audit log entry."""
    clean_phone, phone_formatted, wa_url = validate_and_format_phone(data.phone)
    day, month, year, birth_formatted = validate_and_parse_birth_date(data.birthDate)
    pos = validate_position(data.position)

    cursor = conn.cursor()
    # Check phone uniqueness
    cursor.execute("SELECT id FROM members WHERE phone = ?", (clean_phone,))
    if cursor.fetchone():
        raise ValueError(f"Telefone já cadastrado: o número {phone_formatted} já está em uso por outro membro.")

    now = datetime.now(timezone.utc).isoformat()
    user_id = current_user["id"]
    user_name = current_user["name"]

    cursor.execute(
        """
        INSERT INTO members (
            name, phone, phone_formatted, birth_date, birth_day, birth_month, birth_year,
            position, created_by_user_id, updated_by_user_id, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.name.strip(), clean_phone, phone_formatted, birth_formatted,
            day, month, year, pos, user_id, user_id, now, now
        )
    )
    member_id = cursor.lastrowid
    conn.commit()

    # Record audit log
    record_activity(
        conn,
        user_id=user_id,
        user_name=user_name,
        action_type="CREATE_MEMBER",
        member_id=member_id,
        member_name=data.name.strip(),
        details=f"Cadastrado como {pos}"
    )

    return {
        "id": member_id,
        "name": data.name.strip(),
        "phone": clean_phone,
        "phoneFormatted": phone_formatted,
        "whatsappUrl": wa_url,
        "birthDate": birth_formatted,
        "position": pos,
        "createdByName": user_name,
        "updatedByName": user_name,
        "createdAt": now,
        "updatedAt": now
    }

def update_member(
    conn: sqlite3.Connection,
    member_id: int,
    data: MemberUpdateRequest,
    current_user: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Updates an existing member, tracking field changes in audit logs."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    existing = cursor.fetchone()
    if not existing:
        return None

    clean_phone, phone_formatted, wa_url = validate_and_format_phone(data.phone)
    day, month, year, birth_formatted = validate_and_parse_birth_date(data.birthDate)
    pos = validate_position(data.position)
    new_name = data.name.strip()

    # Check phone collision with other members
    cursor.execute("SELECT id FROM members WHERE phone = ? AND id != ?", (clean_phone, member_id))
    if cursor.fetchone():
        raise ValueError(f"Telefone já cadastrado: o número {phone_formatted} já está em uso por outro membro.")

    # Diff tracking
    diffs = []
    if existing["name"] != new_name:
        diffs.append(f"Nome alterado para '{new_name}'")
    if existing["position"] != pos:
        diffs.append(f"Posição alterada de '{existing['position']}' para '{pos}'")
    if existing["phone"] != clean_phone:
        diffs.append(f"Telefone alterado para '{phone_formatted}'")
    if existing["birth_date"] != birth_formatted:
        diffs.append(f"Aniversário alterado para '{birth_formatted}'")

    details = "; ".join(diffs) if diffs else "Dados cadastrais atualizados"

    now = datetime.now(timezone.utc).isoformat()
    user_id = current_user["id"]
    user_name = current_user["name"]

    cursor.execute(
        """
        UPDATE members SET
            name = ?, phone = ?, phone_formatted = ?, birth_date = ?,
            birth_day = ?, birth_month = ?, birth_year = ?, position = ?,
            updated_by_user_id = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            new_name, clean_phone, phone_formatted, birth_formatted,
            day, month, year, pos, user_id, now, member_id
        )
    )
    conn.commit()

    # Record audit log
    record_activity(
        conn,
        user_id=user_id,
        user_name=user_name,
        action_type="UPDATE_MEMBER",
        member_id=member_id,
        member_name=new_name,
        details=details
    )

    # Fetch creator name
    cursor.execute("SELECT name FROM users WHERE id = ?", (existing["created_by_user_id"],))
    creator_row = cursor.fetchone()
    creator_name = creator_row["name"] if creator_row else "Sistema"

    return {
        "id": member_id,
        "name": new_name,
        "phone": clean_phone,
        "phoneFormatted": phone_formatted,
        "whatsappUrl": wa_url,
        "birthDate": birth_formatted,
        "position": pos,
        "createdByName": creator_name,
        "updatedByName": user_name,
        "createdAt": existing["created_at"],
        "updatedAt": now
    }

def delete_member(conn: sqlite3.Connection, member_id: int, current_user: Dict[str, Any]) -> bool:
    """Deletes a member from the roster and records an audit log entry."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM members WHERE id = ?", (member_id,))
    member = cursor.fetchone()
    if not member:
        return False

    member_name = member["name"]
    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()

    record_activity(
        conn,
        user_id=current_user["id"],
        user_name=current_user["name"],
        action_type="DELETE_MEMBER",
        member_id=member_id,
        member_name=member_name,
        details="Membro removido do GD"
    )
    return True

def list_members(

    conn: sqlite3.Connection,

    search: Optional[str] = None,
    position: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Lists members in alphabetical order, supporting search and role filter."""
    cursor = conn.cursor()
    query = """
        SELECT
            m.id, m.name, m.phone, m.phone_formatted, m.birth_date, m.position,
            m.created_at, m.updated_at,
            u1.name as created_by_name,
            u2.name as updated_by_name
        FROM members m
        LEFT JOIN users u1 ON m.created_by_user_id = u1.id
        LEFT JOIN users u2 ON m.updated_by_user_id = u2.id
        WHERE 1=1
    """
    params = []

    if position and position in ("Líder", "Núcleo", "Membro"):
        query += " AND m.position = ?"
        params.append(position)

    query += " ORDER BY m.name COLLATE NOCASE ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    normalized_search = strip_accents(search) if search else None
    results = []

    for r in rows:
        name = r["name"]
        if normalized_search:
            if normalized_search not in strip_accents(name):
                continue

        results.append({
            "id": r["id"],
            "name": name,
            "phone": r["phone"],
            "phoneFormatted": r["phone_formatted"],
            "whatsappUrl": f"https://wa.me/55{r['phone']}",
            "birthDate": r["birth_date"],
            "position": r["position"],
            "createdByName": r["created_by_name"] or "Sistema",
            "updatedByName": r["updated_by_name"] or "Sistema",
            "createdAt": r["created_at"],
            "updatedAt": r["updated_at"]
        })

    return results
