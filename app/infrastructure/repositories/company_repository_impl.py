from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository
from app.infrastructure.database.models import CompanyModel, ZipCodeModel


class CompanyRepositoryImpl(CompanyRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, company: Company) -> Company:
        db_company = CompanyModel(
            id=company.id,
            name=company.name,
            description=company.description,
            created_at=company.created_at,
            updated_at=company.updated_at,
        )
        self.db.add(db_company)
        
        # Add zip codes
        for zip_code in company.zip_codes:
            db_zip_code = ZipCodeModel(
                zip_code=zip_code,
                company_id=company.id,
            )
            self.db.add(db_zip_code)
            
        await self.db.commit()
        await self.db.refresh(db_company)
        
        # Get zip codes for the company
        result = await self.db.execute(
            select(ZipCodeModel.zip_code).where(ZipCodeModel.company_id == company.id)
        )
        zip_codes = result.scalars().all()
        
        return Company(
            id=db_company.id,
            name=db_company.name,
            description=db_company.description,
            zip_codes=zip_codes,
            created_at=db_company.created_at,
            updated_at=db_company.updated_at,
        )

    async def get_by_id(self, company_id: UUID) -> Optional[Company]:
        result = await self.db.execute(select(CompanyModel).where(CompanyModel.id == company_id))
        db_company = result.scalars().first()
        if db_company is None:
            return None
            
        # Get zip codes for the company
        result = await self.db.execute(
            select(ZipCodeModel.zip_code).where(ZipCodeModel.company_id == company_id)
        )
        zip_codes = result.scalars().all()
        
        return Company(
            id=db_company.id,
            name=db_company.name,
            description=db_company.description,
            zip_codes=zip_codes,
            created_at=db_company.created_at,
            updated_at=db_company.updated_at,
        )

    async def get_by_zip_code(self, zip_code: str) -> Optional[Company]:
        result = await self.db.execute(
            select(ZipCodeModel).where(ZipCodeModel.zip_code == zip_code)
        )
        db_zip_code = result.scalars().first()
        if db_zip_code is None:
            return None
            
        return await self.get_by_id(db_zip_code.company_id)

    async def get_all(self) -> List[Company]:
        result = await self.db.execute(select(CompanyModel))
        db_companies = result.scalars().all()
        
        companies = []
        for db_company in db_companies:
            # Get zip codes for the company
            result = await self.db.execute(
                select(ZipCodeModel.zip_code).where(ZipCodeModel.company_id == db_company.id)
            )
            zip_codes = result.scalars().all()
            
            companies.append(
                Company(
                    id=db_company.id,
                    name=db_company.name,
                    description=db_company.description,
                    zip_codes=zip_codes,
                    created_at=db_company.created_at,
                    updated_at=db_company.updated_at,
                )
            )
            
        return companies

    async def update(self, company: Company) -> Company:
        result = await self.db.execute(select(CompanyModel).where(CompanyModel.id == company.id))
        db_company = result.scalars().first()
        if db_company is None:
            raise ValueError(f"Company with id {company.id} not found")
        
        db_company.name = company.name
        db_company.description = company.description
        db_company.updated_at = company.updated_at
        
        # Delete existing zip codes
        await self.db.execute(
            delete(ZipCodeModel).where(ZipCodeModel.company_id == company.id)
        )
        
        # Add new zip codes
        for zip_code in company.zip_codes:
            db_zip_code = ZipCodeModel(
                zip_code=zip_code,
                company_id=company.id,
            )
            self.db.add(db_zip_code)
            
        await self.db.commit()
        await self.db.refresh(db_company)
        
        # Get zip codes for the company
        result = await self.db.execute(
            select(ZipCodeModel.zip_code).where(ZipCodeModel.company_id == company.id)
        )
        zip_codes = result.scalars().all()
        
        return Company(
            id=db_company.id,
            name=db_company.name,
            description=db_company.description,
            zip_codes=zip_codes,
            created_at=db_company.created_at,
            updated_at=db_company.updated_at,
        )

    async def delete(self, company_id: UUID) -> bool:
        result = await self.db.execute(select(CompanyModel).where(CompanyModel.id == company_id))
        db_company = result.scalars().first()
        if db_company is None:
            return False
        
        # Delete zip codes
        await self.db.execute(
            delete(ZipCodeModel).where(ZipCodeModel.company_id == company_id)
        )
        
        # Delete company
        await self.db.delete(db_company)
        await self.db.commit()
        return True
