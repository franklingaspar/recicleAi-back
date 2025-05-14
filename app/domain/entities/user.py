from enum import Enum
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class UserRole(str, Enum):
    ADMIN = "admin"
    COLLECTOR = "collector"
    REGULAR = "regular"


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
    ):
        self.id = id or uuid4()
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.company_id = company_id
