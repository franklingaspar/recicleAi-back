from datetime import datetime
import uuid
from typing import List

from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Table, JSON
from sqlalchemy.orm import relationship

from app.infrastructure.database.database import Base


# Association table for company zip codes
company_zip_codes = Table(
    "company_zip_codes",
    Base.metadata,
    Column("company_id", String, ForeignKey("companies.id"), primary_key=True),
    Column("zip_code", String, primary_key=True),
)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)

    # Relationships
    company = relationship("CompanyModel", back_populates="collectors")
    collections_requested = relationship("CollectionModel", back_populates="user", foreign_keys="CollectionModel.user_id")
    collections_assigned = relationship("CollectionModel", back_populates="collector", foreign_keys="CollectionModel.collector_id")


class CompanyModel(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    collectors = relationship("UserModel", back_populates="company")
    collections = relationship("CollectionModel", back_populates="company")
    zip_codes = relationship("ZipCodeModel", back_populates="company")


class ZipCodeModel(Base):
    __tablename__ = "zip_codes"

    zip_code = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id"), primary_key=True)

    # Relationships
    company = relationship("CompanyModel", back_populates="zip_codes")


class CollectionModel(Base):
    __tablename__ = "collections"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    description = Column(String)
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    zip_code = Column(String)
    images = Column(JSON)  # Store as JSON array in SQLite
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    collector_id = Column(String, ForeignKey("users.id"), nullable=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)

    # Relationships
    user = relationship("UserModel", back_populates="collections_requested", foreign_keys=[user_id])
    collector = relationship("UserModel", back_populates="collections_assigned", foreign_keys=[collector_id])
    company = relationship("CompanyModel", back_populates="collections")
