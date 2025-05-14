import pytest
from datetime import timedelta
from uuid import uuid4

from jose import jwt

from app.application.services.auth_service import AuthService
from app.domain.entities.user import UserRole


def test_password_hashing():
    # Arrange
    auth_service = AuthService(secret_key="test-secret-key")
    password = "testpassword"

    # Act
    hashed_password = auth_service.get_password_hash(password)

    # Assert
    assert hashed_password != password
    assert auth_service.verify_password(password, hashed_password)
    assert not auth_service.verify_password("wrongpassword", hashed_password)


def test_create_access_token():
    # Arrange
    auth_service = AuthService(
        secret_key="test-secret-key",
        algorithm="HS256",
        access_token_expire_minutes=30,
    )
    user_id = uuid4()
    role = UserRole.ADMIN
    expires_delta = timedelta(minutes=15)

    # Act
    token = auth_service.create_access_token(
        user_id=user_id, role=role, expires_delta=expires_delta
    )

    # Assert
    payload = jwt.decode(
        token, auth_service.secret_key, algorithms=[auth_service.algorithm]
    )
    assert payload["sub"] == str(user_id)
    assert payload["role"] == role
    assert "exp" in payload
