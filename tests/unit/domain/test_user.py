import pytest
from uuid import uuid4
from datetime import datetime

from app.domain.entities.user import User, UserRole


def test_user_creation():
    # Arrange
    user_id = uuid4()
    username = "testuser"
    email = "test@example.com"
    hashed_password = "hashedpassword"
    role = UserRole.ADMIN
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()
    company_id = uuid4()

    # Act
    user = User(
        id=user_id,
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
        created_at=created_at,
        updated_at=updated_at,
        company_id=company_id,
    )

    # Assert
    assert user.id == user_id
    assert user.username == username
    assert user.email == email
    assert user.hashed_password == hashed_password
    assert user.role == role
    assert user.created_at == created_at
    assert user.updated_at == updated_at
    assert user.company_id == company_id


def test_user_creation_with_defaults():
    # Arrange
    username = "testuser"
    email = "test@example.com"
    hashed_password = "hashedpassword"
    role = UserRole.REGULAR

    # Act
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )

    # Assert
    assert user.id is not None
    assert user.username == username
    assert user.email == email
    assert user.hashed_password == hashed_password
    assert user.role == role
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.company_id is None
