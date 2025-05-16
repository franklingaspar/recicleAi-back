from enum import Enum
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class CollectionStatus(str, Enum):
    REQUESTED = "REQUESTED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Collection:
    def __init__(
        self,
        user_id: UUID,
        description: str,
        location_latitude: float,
        location_longitude: float,
        zip_code: str,
        images: List[str],
        status: CollectionStatus = CollectionStatus.REQUESTED,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        collector_id: Optional[UUID] = None,
        company_id: Optional[UUID] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.description = description
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self.zip_code = zip_code
        self.images = images
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.collector_id = collector_id
        self.company_id = company_id
