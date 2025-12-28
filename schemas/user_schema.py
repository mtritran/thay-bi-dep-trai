from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    username: str = "admin"
    password: str = "admin"

class UserCreate(UserBase):
    # id: Optional[str] = None
    pass

class UserUpdate(UserBase):
    id: str
    roles: list[str] | None = None

class UserResponse(UserBase):
    roles: list[str]
    id: UUID

class LoginRequest(BaseModel):
    username: str = "admin"
    password: str = "admin"

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class PaginatedUserResponse(BaseModel):
    total_pages: int
    total_elements: int
    has_next: bool
    data: list[UserResponse]
