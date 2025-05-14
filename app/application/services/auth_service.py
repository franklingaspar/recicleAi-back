import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Dict, Any
from uuid import UUID

from jose import jwt
from passlib.context import CryptContext

from app.domain.entities.user import User, UserRole


class AuthService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(
        self, user_id: UUID, role: UserRole, expires_delta: Optional[timedelta] = None
    ) -> Tuple[str, datetime]:
        to_encode = {"sub": str(user_id), "role": role, "type": "access"}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, expire

    def create_refresh_token(self, user_id: UUID) -> Tuple[str, datetime]:
        # Gera um token aleatório seguro
        token = secrets.token_hex(32)
        expires = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        return token, expires

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decodifica um token JWT e retorna seu payload."""
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
