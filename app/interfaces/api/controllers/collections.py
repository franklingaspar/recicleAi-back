from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.collection_use_cases import CollectionUseCases
from app.domain.entities.collection import CollectionStatus
from app.domain.entities.user import User, UserRole
from app.infrastructure.auth.jwt import get_current_collector_user, get_current_user
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.collection_repository_impl import CollectionRepositoryImpl
from app.infrastructure.repositories.company_repository_impl import CompanyRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.interfaces.api.schemas.collection import (
    CollectionAssign,
    CollectionCreate,
    CollectionResponse,
    CollectionStatusUpdate,
    CollectionUpdate,
)

router = APIRouter()


@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection_create: CollectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CollectionResponse:
    collection_repository = CollectionRepositoryImpl(db)
    company_repository = CompanyRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    collection_use_cases = CollectionUseCases(
        collection_repository, company_repository, user_repository
    )

    try:
        collection = await collection_use_cases.request_collection(
            user_id=current_user.id,
            description=collection_create.description,
            location_latitude=collection_create.location_latitude,
            location_longitude=collection_create.location_longitude,
            zip_code=collection_create.zip_code,
            images=collection_create.images,
        )
        return CollectionResponse(
            id=collection.id,
            user_id=collection.user_id,
            description=collection.description,
            location_latitude=collection.location_latitude,
            location_longitude=collection.location_longitude,
            zip_code=collection.zip_code,
            images=collection.images,
            status=collection.status,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            collector_id=collection.collector_id,
            company_id=collection.company_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[CollectionResponse])
async def get_collections(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[CollectionResponse]:
    collection_repository = CollectionRepositoryImpl(db)
    company_repository = CompanyRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    collection_use_cases = CollectionUseCases(
        collection_repository, company_repository, user_repository
    )

    if current_user.role == UserRole.ADMIN:
        collections = await collection_repository.get_all()
    elif current_user.role == UserRole.COLLECTOR:
        collections = await collection_use_cases.get_collections_by_collector(current_user.id)
    else:  # Regular user
        collections = await collection_use_cases.get_collections_by_user(current_user.id)

    return [
        CollectionResponse(
            id=collection.id,
            user_id=collection.user_id,
            description=collection.description,
            location_latitude=collection.location_latitude,
            location_longitude=collection.location_longitude,
            zip_code=collection.zip_code,
            images=collection.images,
            status=collection.status,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            collector_id=collection.collector_id,
            company_id=collection.company_id,
        )
        for collection in collections
    ]


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(
    collection_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CollectionResponse:
    collection_repository = CollectionRepositoryImpl(db)
    company_repository = CompanyRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    collection_use_cases = CollectionUseCases(
        collection_repository, company_repository, user_repository
    )

    collection = await collection_use_cases.get_collection_by_id(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found",
        )

    # Check permissions
    if (
        current_user.role == UserRole.REGULAR
        and collection.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    if (
        current_user.role == UserRole.COLLECTOR
        and collection.collector_id != current_user.id
        and collection.company_id != current_user.company_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return CollectionResponse(
        id=collection.id,
        user_id=collection.user_id,
        description=collection.description,
        location_latitude=collection.location_latitude,
        location_longitude=collection.location_longitude,
        zip_code=collection.zip_code,
        images=collection.images,
        status=collection.status,
        created_at=collection.created_at,
        updated_at=collection.updated_at,
        collector_id=collection.collector_id,
        company_id=collection.company_id,
    )


@router.post("/{collection_id}/assign", response_model=CollectionResponse)
async def assign_collection(
    collection_id: UUID,
    collection_assign: CollectionAssign,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CollectionResponse:
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.COLLECTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    collection_repository = CollectionRepositoryImpl(db)
    company_repository = CompanyRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    collection_use_cases = CollectionUseCases(
        collection_repository, company_repository, user_repository
    )

    try:
        collection = await collection_use_cases.assign_collection(
            collection_id=collection_id,
            collector_id=collection_assign.collector_id,
        )
        return CollectionResponse(
            id=collection.id,
            user_id=collection.user_id,
            description=collection.description,
            location_latitude=collection.location_latitude,
            location_longitude=collection.location_longitude,
            zip_code=collection.zip_code,
            images=collection.images,
            status=collection.status,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            collector_id=collection.collector_id,
            company_id=collection.company_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{collection_id}/status", response_model=CollectionResponse)
async def update_collection_status(
    collection_id: UUID,
    status_update: CollectionStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_collector_user),
) -> CollectionResponse:
    collection_repository = CollectionRepositoryImpl(db)
    company_repository = CompanyRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    collection_use_cases = CollectionUseCases(
        collection_repository, company_repository, user_repository
    )

    try:
        collection = await collection_use_cases.update_collection_status(
            collection_id=collection_id,
            status=status_update.status,
            collector_id=current_user.id,
        )
        return CollectionResponse(
            id=collection.id,
            user_id=collection.user_id,
            description=collection.description,
            location_latitude=collection.location_latitude,
            location_longitude=collection.location_longitude,
            zip_code=collection.zip_code,
            images=collection.images,
            status=collection.status,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            collector_id=collection.collector_id,
            company_id=collection.company_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
