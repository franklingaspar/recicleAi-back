from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.company import Company


class CompanyRepository(ABC):
    @abstractmethod
    async def create(self, company: Company) -> Company:
        pass

    @abstractmethod
    async def get_by_id(self, company_id: UUID) -> Optional[Company]:
        pass

    @abstractmethod
    async def get_by_zip_code(self, zip_code: str) -> Optional[Company]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Company]:
        pass

    @abstractmethod
    async def update(self, company: Company) -> Company:
        pass

    @abstractmethod
    async def delete(self, company_id: UUID) -> bool:
        pass
