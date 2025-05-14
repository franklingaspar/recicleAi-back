from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.auth_service import AuthService
from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.user import User, UserRole
from app.infrastructure.auth.jwt import get_current_admin_user, get_current_user
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.interfaces.api.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()
settings = get_settings()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> UserResponse:
    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository, auth_service)

    try:
        user = await user_use_cases.create_user(
            username=user_create.username,
            email=user_create.email,
            password=user_create.password,
            role=user_create.role,
            company_id=user_create.company_id,
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            company_id=user.company_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> List[UserResponse]:
    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository, auth_service)

    users = await user_use_cases.get_all_users()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            company_id=user.company_id,
        )
        for user in users
    ]


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        company_id=current_user.company_id,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> UserResponse:
    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository, auth_service)

    user = await user_use_cases.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
        company_id=user.company_id,
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> UserResponse:
    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository, auth_service)

    user = await user_use_cases.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.hashed_password = auth_service.get_password_hash(user_update.password)
    if user_update.role is not None:
        user.role = user_update.role
    if user_update.company_id is not None:
        user.company_id = user_update.company_id

    updated_user = await user_use_cases.update_user(user)
    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        role=updated_user.role,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
        company_id=updated_user.company_id,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> None:
    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository, auth_service)

    deleted = await user_use_cases.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
