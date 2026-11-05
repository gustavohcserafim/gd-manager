from typing import List
from fastapi import APIRouter, Depends, Query
from src.domain.models import ActivityLogResponse
from src.services.database import get_db_connection
from src.services.audit_service import get_activity_logs
from src.api.routes_auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("", response_model=List[ActivityLogResponse])
def get_history_route(
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    try:
        # Handle Query object if called directly in tests
        limit_val = int(limit) if isinstance(limit, (int, str)) and not hasattr(limit, "default") else 50
        return get_activity_logs(conn, limit=limit_val)
    finally:
        conn.close()
