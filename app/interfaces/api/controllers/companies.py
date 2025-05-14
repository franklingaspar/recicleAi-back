from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.company_use_cases import CompanyUseCases
from app.domain.entities.user import User
from app.infrastructure.auth.jwt import get_current_admin_user
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.company_repository_impl import CompanyRepositoryImpl
from app.interfaces.api.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter()


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_create: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> CompanyResponse:
    company_repository = CompanyRepositoryImpl(db)
    company_use_cases = CompanyUseCases(company_repository)

    try:
        company = await company_use_cases.create_company(
            name=company_create.name,
            description=company_create.description,
            zip_codes=company_create.zip_codes,
        )
        return CompanyResponse(
            id=company.id,
            name=company.name,
            description=company.description,
            zip_codes=company.zip_codes,
            created_at=company.created_at,
            updated_at=company.updated_at,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> List[CompanyResponse]:
    company_repository = CompanyRepositoryImpl(db)
    company_use_cases = CompanyUseCases(company_repository)

    companies = await company_use_cases.get_all_companies()
    return [
        CompanyResponse(
            id=company.id,
            name=company.name,
            description=company.description,
            zip_codes=company.zip_codes,
            created_at=company.created_at,
            updated_at=company.updated_at,
        )
        for company in companies
    ]


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> CompanyResponse:
    company_repository = CompanyRepositoryImpl(db)
    company_use_cases = CompanyUseCases(company_repository)

    company = await company_use_cases.get_company_by_id(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return CompanyResponse(
        id=company.id,
        name=company.name,
        description=company.description,
        zip_codes=company.zip_codes,
        created_at=company.created_at,
        updated_at=company.updated_at,
    )


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: UUID,
    company_update: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> CompanyResponse:
    company_repository = CompanyRepositoryImpl(db)
    company_use_cases = CompanyUseCases(company_repository)

    company = await company_use_cases.get_company_by_id(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    if company_update.name is not None:
        company.name = company_update.name
    if company_update.description is not None:
        company.description = company_update.description
    if company_update.zip_codes is not None:
        company.zip_codes = company_update.zip_codes

    try:
        updated_company = await company_use_cases.update_company(company)
        return CompanyResponse(
            id=updated_company.id,
            name=updated_company.name,
            description=updated_company.description,
            zip_codes=updated_company.zip_codes,
            created_at=updated_company.created_at,
            updated_at=updated_company.updated_at,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> None:
    company_repository = CompanyRepositoryImpl(db)
    company_use_cases = CompanyUseCases(company_repository)

    deleted = await company_use_cases.delete_company(company_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
