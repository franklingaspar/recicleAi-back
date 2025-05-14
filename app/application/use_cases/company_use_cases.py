from typing import List, Optional
from uuid import UUID

from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository


class CompanyUseCases:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    async def create_company(
        self, name: str, description: str, zip_codes: List[str]
    ) -> Company:
        # Check for zip code conflicts
        for zip_code in zip_codes:
            existing_company = await self.company_repository.get_by_zip_code(zip_code)
            if existing_company:
                raise ValueError(f"Zip code {zip_code} is already assigned to another company")

        # Create company
        company = Company(
            name=name,
            description=description,
            zip_codes=zip_codes,
        )

        # Save company
        return await self.company_repository.create(company)

    async def get_company_by_id(self, company_id: UUID) -> Optional[Company]:
        return await self.company_repository.get_by_id(company_id)

    async def get_company_by_zip_code(self, zip_code: str) -> Optional[Company]:
        return await self.company_repository.get_by_zip_code(zip_code)

    async def get_all_companies(self) -> List[Company]:
        return await self.company_repository.get_all()

    async def update_company(self, company: Company) -> Company:
        # Check for zip code conflicts
        for zip_code in company.zip_codes:
            existing_company = await self.company_repository.get_by_zip_code(zip_code)
            if existing_company and existing_company.id != company.id:
                raise ValueError(f"Zip code {zip_code} is already assigned to another company")

        return await self.company_repository.update(company)

    async def delete_company(self, company_id: UUID) -> bool:
        return await self.company_repository.delete(company_id)
