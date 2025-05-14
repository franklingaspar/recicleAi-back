from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.infrastructure.config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
