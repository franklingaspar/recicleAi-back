import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Waste Collection API"
    admin_email: str = "admin"
    database_url: str = Field(
        default="sqlite+aiosqlite:///./waste_collection.db"
    )
    secret_key: str = Field(default="your-secret-key-for-jwt")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./waste_collection.db"),
        secret_key=os.getenv("SECRET_KEY", "your-secret-key-for-jwt"),
        algorithm=os.getenv("ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
    )
