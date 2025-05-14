import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.application.services.auth_service import AuthService
from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.user import User, UserRole


@pytest.fixture
def auth_service():
    service = MagicMock(spec=AuthService)
    service.get_password_hash.return_value = "hashed_password"
    service.verify_password.return_value = True
    return service


@pytest.fixture
def user_repository():
    repository = AsyncMock()
    repository.get_by_email.return_value = None
    repository.get_by_username.return_value = None
    repository.create.return_value = User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        role=UserRole.ADMIN,
    )
    return repository


@pytest.fixture
def user_use_cases(user_repository, auth_service):
    return UserUseCases(user_repository, auth_service)


@pytest.mark.asyncio
async def test_create_user(user_use_cases, user_repository, auth_service):
    # Arrange
    username = "testuser"
    email = "test@example.com"
    password = "password"
    role = UserRole.ADMIN

    # Act
    user = await user_use_cases.create_user(username, email, password, role)

    # Assert
    assert user is not None
    assert user.username == username
    assert user.email == email
    assert user.role == role
    auth_service.get_password_hash.assert_called_once_with(password)
    user_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_existing_email(user_use_cases, user_repository):
    # Arrange
    user_repository.get_by_email.return_value = User(
        username="existinguser",
        email="existing@example.com",
        hashed_password="hashed_password",
        role=UserRole.ADMIN,
    )

    # Act & Assert
    with pytest.raises(ValueError, match="User with this email already exists"):
        await user_use_cases.create_user(
            "testuser", "existing@example.com", "password", UserRole.ADMIN
        )


@pytest.mark.asyncio
async def test_authenticate_user_success(user_use_cases, user_repository, auth_service):
    # Arrange
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        role=UserRole.ADMIN,
    )
    user_repository.get_by_email.return_value = user
    auth_service.verify_password.return_value = True

    # Act
    authenticated_user = await user_use_cases.authenticate_user("test@example.com", "password")

    # Assert
    assert authenticated_user is not None
    assert authenticated_user == user
    auth_service.verify_password.assert_called_once_with("password", "hashed_password")


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(user_use_cases, user_repository, auth_service):
    # Arrange
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        role=UserRole.ADMIN,
    )
    user_repository.get_by_email.return_value = user
    auth_service.verify_password.return_value = False

    # Act
    authenticated_user = await user_use_cases.authenticate_user("test@example.com", "wrong_password")

    # Assert
    assert authenticated_user is None
    auth_service.verify_password.assert_called_once_with("wrong_password", "hashed_password")
