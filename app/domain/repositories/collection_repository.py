from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.collection import Collection, CollectionStatus


class CollectionRepository(ABC):
    @abstractmethod
    async def create(self, collection: Collection) -> Collection:
        pass

    @abstractmethod
    async def get_by_id(self, collection_id: UUID) -> Optional[Collection]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Collection]:
        pass

    @abstractmethod
    async def get_by_collector_id(self, collector_id: UUID) -> List[Collection]:
        pass

    @abstractmethod
    async def get_by_company_id(self, company_id: UUID) -> List[Collection]:
        pass

    @abstractmethod
    async def get_by_status(self, status: CollectionStatus) -> List[Collection]:
        pass

    @abstractmethod
    async def get_by_zip_code(self, zip_code: str) -> List[Collection]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Collection]:
        pass

    @abstractmethod
    async def update(self, collection: Collection) -> Collection:
        pass

    @abstractmethod
    async def delete(self, collection_id: UUID) -> bool:
        pass
