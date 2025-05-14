from typing import List, Optional
from uuid import UUID

from app.domain.entities.collection import Collection, CollectionStatus
from app.domain.repositories.collection_repository import CollectionRepository
from app.domain.repositories.company_repository import CompanyRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import UserRole


class CollectionUseCases:
    def __init__(
        self, 
        collection_repository: CollectionRepository,
        company_repository: CompanyRepository,
        user_repository: UserRepository
    ):
        self.collection_repository = collection_repository
        self.company_repository = company_repository
        self.user_repository = user_repository

    async def request_collection(
        self,
        user_id: UUID,
        description: str,
        location_latitude: float,
        location_longitude: float,
        zip_code: str,
        images: List[str],
    ) -> Collection:
        # Find the company responsible for this zip code
        company = await self.company_repository.get_by_zip_code(zip_code)
        if not company:
            raise ValueError(f"No collection company available for zip code {zip_code}")

        # Create collection request
        collection = Collection(
            user_id=user_id,
            description=description,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            zip_code=zip_code,
            images=images,
            status=CollectionStatus.REQUESTED,
            company_id=company.id,
        )

        # Save collection
        return await self.collection_repository.create(collection)

    async def assign_collection(
        self, collection_id: UUID, collector_id: UUID
    ) -> Collection:
        # Get collection
        collection = await self.collection_repository.get_by_id(collection_id)
        if not collection:
            raise ValueError("Collection not found")

        # Verify collector exists and belongs to the right company
        collector = await self.user_repository.get_by_id(collector_id)
        if not collector:
            raise ValueError("Collector not found")
        
        if collector.role != UserRole.COLLECTOR:
            raise ValueError("User is not a collector")
            
        if collector.company_id != collection.company_id:
            raise ValueError("Collector does not belong to the company responsible for this collection")

        # Update collection
        collection.collector_id = collector_id
        collection.status = CollectionStatus.ASSIGNED
        
        return await self.collection_repository.update(collection)

    async def update_collection_status(
        self, collection_id: UUID, status: CollectionStatus, collector_id: UUID
    ) -> Collection:
        # Get collection
        collection = await self.collection_repository.get_by_id(collection_id)
        if not collection:
            raise ValueError("Collection not found")

        # Verify collector is assigned to this collection
        if collection.collector_id != collector_id:
            raise ValueError("Collector is not assigned to this collection")

        # Update status
        collection.status = status
        
        return await self.collection_repository.update(collection)

    async def get_collection_by_id(self, collection_id: UUID) -> Optional[Collection]:
        return await self.collection_repository.get_by_id(collection_id)

    async def get_collections_by_user(self, user_id: UUID) -> List[Collection]:
        return await self.collection_repository.get_by_user_id(user_id)

    async def get_collections_by_collector(self, collector_id: UUID) -> List[Collection]:
        return await self.collection_repository.get_by_collector_id(collector_id)

    async def get_collections_by_company(self, company_id: UUID) -> List[Collection]:
        return await self.collection_repository.get_by_company_id(company_id)

    async def get_collections_by_status(self, status: CollectionStatus) -> List[Collection]:
        return await self.collection_repository.get_by_status(status)

    async def get_collections_by_zip_code(self, zip_code: str) -> List[Collection]:
        return await self.collection_repository.get_by_zip_code(zip_code)
