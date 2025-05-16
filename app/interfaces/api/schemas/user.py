from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.domain.entities.user import UserRole, ProfileType


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole
    company_id: Optional[UUID] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    company_id: Optional[UUID] = None


class UserResponse(UserBase):
    id: UUID
    role: UserRole
    created_at: datetime
    updated_at: datetime
    company_id: Optional[UUID] = None
    profile_type: Optional[ProfileType] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int  # Tempo de expiração em segundos
    user: Optional[UserResponse] = None  # Dados do usuário


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: UUID
    role: UserRole
