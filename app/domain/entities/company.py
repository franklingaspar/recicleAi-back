from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class Company:
    def __init__(
        self,
        name: str,
        description: str,
        zip_codes: List[str],
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.description = description
        self.zip_codes = zip_codes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
