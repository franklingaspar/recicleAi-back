from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.auth_service import AuthService
from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.user import User
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.interfaces.api.schemas.user import Token

router = APIRouter()
settings = get_settings()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Any:
    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository, auth_service)

    user = await user_use_cases.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        user_id=user.id, role=user.role, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
