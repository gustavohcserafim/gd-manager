from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from src.domain.models import MemberCreateRequest, MemberUpdateRequest, MemberResponse
from src.services.database import get_db_connection
from src.services.member_service import create_member, list_members, update_member, delete_member
from src.api.routes_auth import get_current_user

router = APIRouter(prefix="/api/members", tags=["members"])

@router.delete("/{member_id}")
def delete_member_route(
    member_id: int,
    current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    try:
        success = delete_member(conn, member_id, current_user)
        if not success:
            raise HTTPException(
                status_code=404,
                detail={"error": "Não encontrado", "detail": f"Membro ID {member_id} não encontrado."}
            )
        return {"message": "Membro removido com sucesso", "deletedId": member_id}
    finally:
        conn.close()

@router.put("/{member_id}", response_model=MemberResponse)

def update_member_route(
    member_id: int,
    payload: MemberUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    try:
        try:
            result = update_member(conn, member_id, payload, current_user)
        except ValueError as err:
            err_msg = str(err)
            error_label = "Telefone já cadastrado" if "Telefone já cadastrado" in err_msg else "Erro de validação"
            raise HTTPException(
                status_code=400,
                detail={"error": error_label, "detail": err_msg}
            )

        if not result:
            raise HTTPException(
                status_code=404,
                detail={"error": "Não encontrado", "detail": f"Membro ID {member_id} não encontrado."}
            )

        return result
    finally:
        conn.close()

@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)

def create_member_route(
    payload: MemberCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    try:
        try:
            return create_member(conn, payload, current_user)
        except ValueError as err:
            err_msg = str(err)
            error_label = "Telefone já cadastrado" if "Telefone já cadastrado" in err_msg else "Erro de validação"
            raise HTTPException(
                status_code=400,
                detail={"error": error_label, "detail": err_msg}
            )
    finally:
        conn.close()

@router.get("", response_model=List[MemberResponse])
def list_members_route(
    search: Optional[str] = None,
    position: Optional[str] = None
):
    conn = get_db_connection()
    try:
        # Protect against Query objects when called directly in tests
        search_str = str(search) if search and not hasattr(search, "default") else None
        pos_str = str(position) if position and not hasattr(position, "default") else None
        return list_members(conn, search=search_str, position=pos_str)
    finally:
        conn.close()
