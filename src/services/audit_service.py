import sqlite3
import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

def record_activity(
    conn: sqlite3.Connection,
    user_id: int,
    user_name: str,
    action_type: str,
    member_id: Optional[int],
    member_name: str,
    details: Optional[str | Dict[str, Any]] = None
) -> int:
    """Inserts an immutable activity log entry."""
    now = datetime.now(timezone.utc).isoformat()
    if isinstance(details, dict):
        details_str = json.dumps(details, ensure_ascii=False)
    else:
        details_str = details

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO activity_logs (user_id, user_name, action_type, member_id, member_name, details, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, user_name, action_type, member_id, member_name, details_str, now)
    )
    conn.commit()
    return cursor.lastrowid

def get_activity_logs(conn: sqlite3.Connection, limit: int = 50) -> List[Dict[str, Any]]:
    """Returns activity log records in reverse-chronological order."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, user_name, action_type, member_name, details, created_at
        FROM activity_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )
    rows = cursor.fetchall()
    return [
        {
            "id": row["id"],
            "userName": row["user_name"],
            "actionType": row["action_type"],
            "memberName": row["member_name"],
            "details": row["details"],
            "timestamp": row["created_at"]
        }
        for row in rows
    ]
