from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: str
    zip_codes: List[str]


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str = None
    description: str = None
    zip_codes: List[str] = None


class CompanyResponse(CompanyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
