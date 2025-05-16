from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User, UserRole, ProfileType
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        db_user = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            company_id=user.company_id,
            profile_type=user.profile_type.value if user.profile_type else None,
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return self._map_to_entity(db_user)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalars().first()
        if db_user is None:
            return None
        return self._map_to_entity(db_user)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        db_user = result.scalars().first()
        if db_user is None:
            return None
        return self._map_to_entity(db_user)

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(UserModel).where(UserModel.username == username))
        db_user = result.scalars().first()
        if db_user is None:
            return None
        return self._map_to_entity(db_user)

    async def get_all(self) -> List[User]:
        result = await self.db.execute(select(UserModel))
        db_users = result.scalars().all()
        return [self._map_to_entity(db_user) for db_user in db_users]

    async def update(self, user: User) -> User:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user.id))
        db_user = result.scalars().first()
        if db_user is None:
            raise ValueError(f"User with id {user.id} not found")

        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = user.hashed_password
        db_user.role = user.role
        db_user.updated_at = user.updated_at
        db_user.company_id = user.company_id
        db_user.profile_type = user.profile_type.value if user.profile_type else None

        await self.db.commit()
        await self.db.refresh(db_user)
        return self._map_to_entity(db_user)

    async def delete(self, user_id: UUID) -> bool:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalars().first()
        if db_user is None:
            return False

        await self.db.delete(db_user)
        await self.db.commit()
        return True

    async def get_collectors_by_company_id(self, company_id: UUID) -> List[User]:
        result = await self.db.execute(
            select(UserModel).where(
                UserModel.company_id == company_id,
                UserModel.role == UserRole.COLLECTOR
            )
        )
        db_users = result.scalars().all()
        return [self._map_to_entity(db_user) for db_user in db_users]

    def _map_to_entity(self, db_user: UserModel) -> User:
        profile_type = None
        if db_user.profile_type:
            try:
                profile_type = ProfileType(db_user.profile_type)
            except ValueError:
                # Se o valor não for válido, deixamos como None e o método _determine_profile_type
                # na entidade User vai determinar o tipo de perfil
                pass

        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            role=UserRole(db_user.role),
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            company_id=db_user.company_id,
            profile_type=profile_type,
        )
