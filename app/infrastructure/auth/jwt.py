from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        role: str = payload.get("role")
        if role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repository: UserRepository = UserRepositoryImpl(db)
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user


async def get_current_collector_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.COLLECTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
