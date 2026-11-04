from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import (
    DuplicatePhoneException,
    UnauthorizedRoleException,
    MemberNotFoundException,
    ValidationException,
)
from src.domain.ports.member_repository import MemberRepository
from src.application.dtos.create_member_dto import CreateMemberRequest, MemberResponse
from src.application.dtos.update_member_dto import UpdateMemberRequest
from src.application.use_cases.create_member_use_case import CreateMemberUseCase
from src.application.use_cases.get_members_use_case import GetMembersUseCase
from src.application.use_cases.get_upcoming_birthdays_use_case import GetUpcomingBirthdaysUseCase
from src.application.use_cases.update_member_use_case import GetMemberByIdUseCase, UpdateMemberUseCase
from src.application.use_cases.lifecycle_use_cases import DeactivateMemberUseCase, ReactivateMemberUseCase
from src.infrastructure.web.dependencies import get_current_role, require_manager_role

router = APIRouter(prefix="/api/v1/members", tags=["members"])


def get_repository() -> MemberRepository:
    raise NotImplementedError("Repositório deve ser injetado pela aplicação principal.")


@router.post("", response_model=MemberResponse, status_code=http_status.HTTP_201_CREATED)
def create_member(
    payload: CreateMemberRequest,
    caller_role: MemberRole = Depends(require_manager_role),
    repo: MemberRepository = Depends(get_repository),
):
    try:
        use_case = CreateMemberUseCase(repo)
        return use_case.execute(payload, caller_role=caller_role)
    except DuplicatePhoneException as e:
        raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=e.message)
    except UnauthorizedRoleException as e:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.get("", response_model=List[MemberResponse], status_code=http_status.HTTP_200_OK)
def list_members(
    status: Optional[MemberStatus] = Query(default=MemberStatus.ACTIVE),
    role: Optional[MemberRole] = Query(default=None),
    search: Optional[str] = Query(default=None),
    birthday_month: Optional[int] = Query(default=None, ge=1, le=12, description="Mês do aniversário (1 a 12)"),
    caller_role: MemberRole = Depends(get_current_role),
    repo: MemberRepository = Depends(get_repository),
):
    try:
        resolved_status = MemberStatus.ACTIVE if not isinstance(status, MemberStatus) and status is not None and not isinstance(status, str) else status
        resolved_role = None if not isinstance(role, MemberRole) and role is not None and not isinstance(role, str) else role
        resolved_search = None if not isinstance(search, str) and search is not None else search
        resolved_month = birthday_month if isinstance(birthday_month, int) else None

        use_case = GetMembersUseCase(repo)
        return use_case.execute(
            caller_role=caller_role,
            status=resolved_status,
            role=resolved_role,
            search=resolved_search,
            birthday_month=resolved_month,
        )
    except UnauthorizedRoleException as e:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail=e.message)


@router.get("/birthdays/upcoming", response_model=List[MemberResponse], status_code=http_status.HTTP_200_OK)
def get_upcoming_birthdays(
    days: int = Query(default=30, ge=1, le=365, description="Janela de dias para próximos aniversários"),
    caller_role: MemberRole = Depends(get_current_role),
    repo: MemberRepository = Depends(get_repository),
):
    resolved_days = days if isinstance(days, int) else 30
    use_case = GetUpcomingBirthdaysUseCase(repo)
    return use_case.execute(days=resolved_days)


@router.get("/{id}", response_model=MemberResponse, status_code=http_status.HTTP_200_OK)
def get_member(
    id: str,
    caller_role: MemberRole = Depends(get_current_role),
    repo: MemberRepository = Depends(get_repository),
):
    try:
        use_case = GetMemberByIdUseCase(repo)
        return use_case.execute(id)
    except MemberNotFoundException as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=e.message)


@router.put("/{id}", response_model=MemberResponse, status_code=http_status.HTTP_200_OK)
def update_member(
    id: str,
    payload: UpdateMemberRequest,
    caller_role: MemberRole = Depends(require_manager_role),
    repo: MemberRepository = Depends(get_repository),
):
    try:
        use_case = UpdateMemberUseCase(repo)
        return use_case.execute(id, payload, caller_role=caller_role)
    except MemberNotFoundException as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=e.message)
    except DuplicatePhoneException as e:
        raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=e.message)
    except UnauthorizedRoleException as e:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.delete("/{id}", response_model=MemberResponse, status_code=http_status.HTTP_200_OK)
def deactivate_member(
    id: str,
    caller_role: MemberRole = Depends(require_manager_role),
    repo: MemberRepository = Depends(get_repository),
):
    try:
        use_case = DeactivateMemberUseCase(repo)
        return use_case.execute(id, caller_role=caller_role)
    except MemberNotFoundException as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=e.message)
    except UnauthorizedRoleException as e:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail=e.message)


@router.patch("/{id}/reactivate", response_model=MemberResponse, status_code=http_status.HTTP_200_OK)
def reactivate_member(
    id: str,
    caller_role: MemberRole = Depends(require_manager_role),
    repo: MemberRepository = Depends(get_repository),
):
    try:
        use_case = ReactivateMemberUseCase(repo)
        return use_case.execute(id, caller_role=caller_role)
    except MemberNotFoundException as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=e.message)
    except DuplicatePhoneException as e:
        raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=e.message)
    except UnauthorizedRoleException as e:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail=e.message)
