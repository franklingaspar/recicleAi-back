from typing import List, Optional
from uuid import UUID

from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService


class UserUseCases:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def create_user(
        self, username: str, email: str, password: str, role: UserRole, company_id: Optional[UUID] = None
    ) -> User:
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        existing_username = await self.user_repository.get_by_username(username)
        if existing_username:
            raise ValueError("User with this username already exists")

        # Hash password
        hashed_password = self.auth_service.get_password_hash(password)

        # Create user
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role,
            company_id=company_id,
        )

        # Save user
        return await self.user_repository.create(user)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        if not self.auth_service.verify_password(password, user.hashed_password):
            return None
        return user

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.get_all()

    async def update_user(self, user: User) -> User:
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: UUID) -> bool:
        return await self.user_repository.delete(user_id)
        
    async def get_collectors_by_company(self, company_id: UUID) -> List[User]:
        return await self.user_repository.get_collectors_by_company_id(company_id)
