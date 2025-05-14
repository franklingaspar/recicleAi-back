from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.collection import Collection, CollectionStatus
from app.domain.repositories.collection_repository import CollectionRepository
from app.infrastructure.database.models import CollectionModel


class CollectionRepositoryImpl(CollectionRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, collection: Collection) -> Collection:
        db_collection = CollectionModel(
            id=collection.id,
            user_id=collection.user_id,
            description=collection.description,
            location_latitude=collection.location_latitude,
            location_longitude=collection.location_longitude,
            zip_code=collection.zip_code,
            images=collection.images,
            status=collection.status,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            collector_id=collection.collector_id,
            company_id=collection.company_id,
        )
        self.db.add(db_collection)
        await self.db.commit()
        await self.db.refresh(db_collection)
        return self._map_to_entity(db_collection)

    async def get_by_id(self, collection_id: UUID) -> Optional[Collection]:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.id == collection_id))
        db_collection = result.scalars().first()
        if db_collection is None:
            return None
        return self._map_to_entity(db_collection)

    async def get_by_user_id(self, user_id: UUID) -> List[Collection]:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.user_id == user_id))
        db_collections = result.scalars().all()
        return [self._map_to_entity(db_collection) for db_collection in db_collections]

    async def get_by_collector_id(self, collector_id: UUID) -> List[Collection]:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.collector_id == collector_id))
        db_collections = result.scalars().all()
        return [self._map_to_entity(db_collection) for db_collection in db_collections]

    async def get_by_company_id(self, company_id: UUID) -> List[Collection]:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.company_id == company_id))
        db_collections = result.scalars().all()
        return [self._map_to_entity(db_collection) for db_collection in db_collections]

    async def get_by_status(self, status: CollectionStatus) -> List[Collection]:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.status == status))
        db_collections = result.scalars().all()
        return [self._map_to_entity(db_collection) for db_collection in db_collections]

    async def get_by_zip_code(self, zip_code: str) -> List[Collection]:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.zip_code == zip_code))
        db_collections = result.scalars().all()
        return [self._map_to_entity(db_collection) for db_collection in db_collections]

    async def get_all(self) -> List[Collection]:
        result = await self.db.execute(select(CollectionModel))
        db_collections = result.scalars().all()
        return [self._map_to_entity(db_collection) for db_collection in db_collections]

    async def update(self, collection: Collection) -> Collection:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.id == collection.id))
        db_collection = result.scalars().first()
        if db_collection is None:
            raise ValueError(f"Collection with id {collection.id} not found")
        
        db_collection.description = collection.description
        db_collection.location_latitude = collection.location_latitude
        db_collection.location_longitude = collection.location_longitude
        db_collection.zip_code = collection.zip_code
        db_collection.images = collection.images
        db_collection.status = collection.status
        db_collection.updated_at = collection.updated_at
        db_collection.collector_id = collection.collector_id
        db_collection.company_id = collection.company_id
        
        await self.db.commit()
        await self.db.refresh(db_collection)
        return self._map_to_entity(db_collection)

    async def delete(self, collection_id: UUID) -> bool:
        result = await self.db.execute(select(CollectionModel).where(CollectionModel.id == collection_id))
        db_collection = result.scalars().first()
        if db_collection is None:
            return False
        
        await self.db.delete(db_collection)
        await self.db.commit()
        return True

    def _map_to_entity(self, db_collection: CollectionModel) -> Collection:
        return Collection(
            id=db_collection.id,
            user_id=db_collection.user_id,
            description=db_collection.description,
            location_latitude=db_collection.location_latitude,
            location_longitude=db_collection.location_longitude,
            zip_code=db_collection.zip_code,
            images=db_collection.images,
            status=CollectionStatus(db_collection.status),
            created_at=db_collection.created_at,
            updated_at=db_collection.updated_at,
            collector_id=db_collection.collector_id,
            company_id=db_collection.company_id,
        )
