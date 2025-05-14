from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        pass
        
    @abstractmethod
    async def get_collectors_by_company_id(self, company_id: UUID) -> List[User]:
        pass
