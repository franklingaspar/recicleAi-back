import os
import secrets
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field


# Gera uma chave secreta forte por padrão (apenas para desenvolvimento)
DEFAULT_SECRET_KEY = secrets.token_hex(32)


class Settings(BaseModel):
    app_name: str = "Waste Collection API"
    admin_email: str = "admin"
    database_url: str = Field(
        default="sqlite+aiosqlite:///./waste_collection.db"
    )
    secret_key: str = Field(default=DEFAULT_SECRET_KEY)
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)


@lru_cache()
def get_settings() -> Settings:
    # Verifica se a SECRET_KEY está definida no ambiente
    if not os.getenv("SECRET_KEY") and os.getenv("APP_ENV") == "production":
        print("WARNING: No SECRET_KEY set in production environment. Using a randomly generated key.")
        print("This will invalidate all existing tokens when the application restarts.")
        print("Please set a permanent SECRET_KEY environment variable.")

    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./waste_collection.db"),
        secret_key=os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY),
        algorithm=os.getenv("ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
        refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
    )
