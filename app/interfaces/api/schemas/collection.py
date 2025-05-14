from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.entities.collection import CollectionStatus


class CollectionBase(BaseModel):
    description: str
    location_latitude: float
    location_longitude: float
    zip_code: str
    images: List[str]


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    description: Optional[str] = None
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    zip_code: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[CollectionStatus] = None


class CollectionResponse(CollectionBase):
    id: UUID
    user_id: UUID
    status: CollectionStatus
    created_at: datetime
    updated_at: datetime
    collector_id: Optional[UUID] = None
    company_id: Optional[UUID] = None

    class Config:
        from_attributes = True


class CollectionAssign(BaseModel):
    collector_id: UUID


class CollectionStatusUpdate(BaseModel):
    status: CollectionStatus
