from enum import Enum
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class UserRole(str, Enum):
    ADMIN = "admin"
    COLLECTOR = "collector"
    REGULAR = "regular"


class ProfileType(int, Enum):
    ADMIN = 1
    COMPANY_OWNER = 2
    COLLECTOR = 3
    REGULAR_USER = 4


class User:
    def __init__(
        self,
        username: str,
        email: str,
        hashed_password: str,
        role: UserRole,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        company_id: Optional[UUID] = None,
        profile_type: Optional[ProfileType] = None,
    ):
        self.id = id or uuid4()
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.company_id = company_id
        self.profile_type = profile_type or self._determine_profile_type(role, company_id)

    def _determine_profile_type(self, role: UserRole, company_id: Optional[UUID]) -> ProfileType:
        """Determina o tipo de perfil com base no papel e na associação com empresa."""
        if role == UserRole.ADMIN:
            return ProfileType.ADMIN
        elif role == UserRole.COLLECTOR:
            return ProfileType.COLLECTOR
        elif role == UserRole.REGULAR and company_id:
            return ProfileType.COMPANY_OWNER
        else:
            return ProfileType.REGULAR_USER
