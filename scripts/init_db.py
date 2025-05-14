import asyncio
import os
import sys
import uuid

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.application.services.auth_service import AuthService
from app.domain.entities.user import UserRole
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import Base, get_db
from app.infrastructure.database.models import UserModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select


async def init_db():
    settings = get_settings()

    # Create engine
    engine = create_async_engine(settings.database_url)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create admin user
    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )

    # Get a database session
    async for db in get_db():
        # Check if admin user already exists
        admin_email = "admin"
        result = await db.execute(
            select(UserModel).where(UserModel.email == admin_email)
        )
        admin_exists = result.scalars().first()

        if not admin_exists:
            # Create admin user
            hashed_password = auth_service.get_password_hash("admin123")
            admin_user = UserModel(
                id=str(uuid.uuid4()),
                username="admin",
                email=admin_email,
                hashed_password=hashed_password,
                role=UserRole.ADMIN,
            )
            db.add(admin_user)
            await db.commit()
            print(f"Admin user created with email: {admin_email} and password: admin123")
        else:
            print("Admin user already exists")

        break  # We only need one session

    print("Database initialized successfully")


if __name__ == "__main__":
    asyncio.run(init_db())
