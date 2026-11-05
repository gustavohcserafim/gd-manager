from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

RoleType = Literal["Líder", "Núcleo"]
PositionType = Literal["Líder", "Núcleo", "Membro"]
ActionType = Literal["CREATE_MEMBER", "UPDATE_MEMBER", "DELETE_MEMBER"]

class UserBase(BaseModel):
    name: str = Field(..., min_length=2)
    role: RoleType
    active: bool = True

class UserResponse(BaseModel):
    id: int
    name: str
    role: RoleType

    model_config = ConfigDict(from_attributes=True)

class PinLoginRequest(BaseModel):
    pin: str = Field(..., min_length=1, max_length=12)

class PinLoginResponse(BaseModel):
    token: str
    user: UserResponse

class MemberCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    birthDate: str = Field(..., min_length=4, max_length=10)
    position: PositionType

class MemberUpdateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    birthDate: str = Field(..., min_length=4, max_length=10)
    position: PositionType

class MemberResponse(BaseModel):
    id: int
    name: str
    phone: str
    phoneFormatted: str
    whatsappUrl: str
    birthDate: str
    position: PositionType
    createdByName: Optional[str] = None
    updatedByName: Optional[str] = None
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class ActivityLogResponse(BaseModel):
    id: int
    userName: str
    actionType: ActionType
    memberName: str
    details: Optional[str] = None
    timestamp: str

    model_config = ConfigDict(from_attributes=True)
