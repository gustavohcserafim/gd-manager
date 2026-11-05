from fastapi import APIRouter, Request, HTTPException, Depends, Header
from src.domain.models import PinLoginRequest, PinLoginResponse
from src.services.database import get_db_connection
from src.services.auth_service import authenticate_pin, verify_session_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

def get_current_user(authorization: str = Header(None)) -> dict:
    """Dependency that verifies Bearer session token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={"error": "Não autenticado", "detail": "Token de sessão ausente ou inválido."}
        )

    token = authorization.split(" ", 1)[1]
    user = verify_session_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": "Sessão expirada", "detail": "Faça login com seu PIN novamente."}
        )
    return user

@router.post("/pin", response_model=PinLoginResponse)
def login_with_pin(payload: PinLoginRequest, request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    conn = get_db_connection()
    try:
        try:
            result = authenticate_pin(conn, payload.pin, client_ip=client_ip)
        except PermissionError as e:
            raise HTTPException(
                status_code=429,
                detail={"error": "Muitas tentativas", "detail": str(e)}
            )

        if not result:
            raise HTTPException(
                status_code=401,
                detail={"error": "PIN inválido", "detail": "PIN não encontrado ou incorreto."}
            )

        return result
    finally:
        conn.close()
