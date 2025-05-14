from datetime import timedelta, datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.auth_service import AuthService
from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.user import User
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db
from app.infrastructure.database.models import RefreshTokenModel
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.utils.security_logger import SecurityLogger
from app.interfaces.api.schemas.user import Token, RefreshToken

router = APIRouter()
settings = get_settings()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # Obter o endereço IP do cliente
    client_ip = request.client.host if request.client else "unknown"

    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
        refresh_token_expire_days=settings.refresh_token_expire_days,
    )
    user_repository = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repository, auth_service)

    try:
        user = await user_use_cases.authenticate_user(form_data.username, form_data.password)
        if not user:
            # Registrar falha de login
            SecurityLogger.log_login_attempt(
                success=False,
                username=form_data.username,
                ip_address=client_ip,
                error="Credenciais inválidas"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Criar access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token, expires = auth_service.create_access_token(
            user_id=user.id, role=user.role, expires_delta=access_token_expires
        )

        # Criar refresh token
        refresh_token, refresh_expires = auth_service.create_refresh_token(user_id=user.id)

        # Salvar refresh token no banco de dados
        db_refresh_token = RefreshTokenModel(
            token=refresh_token,
            expires_at=refresh_expires,
            user_id=str(user.id),
        )
        db.add(db_refresh_token)
        await db.commit()

        # Registrar login bem-sucedido
        SecurityLogger.log_login_attempt(
            success=True,
            username=form_data.username,
            ip_address=client_ip,
            user_id=user.id
        )

        # Calcular tempo de expiração em segundos
        expires_in = int(access_token_expires.total_seconds())

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": expires_in
        }
    except Exception as e:
        # Registrar erro inesperado
        if not isinstance(e, HTTPException):
            SecurityLogger.log_security_event(
                event_type="login_error",
                ip_address=client_ip,
                details={"username": form_data.username, "error": str(e)},
                level="error"
            )
        raise


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    request: Request,
    refresh_token_data: RefreshToken = Body(...),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # Obter o endereço IP do cliente
    client_ip = request.client.host if request.client else "unknown"

    auth_service = AuthService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
        refresh_token_expire_days=settings.refresh_token_expire_days,
    )

    try:
        # Verificar se o refresh token existe e é válido
        db_refresh_token = await db.query(RefreshTokenModel).filter(
            RefreshTokenModel.token == refresh_token_data.refresh_token,
            RefreshTokenModel.revoked == False,
            RefreshTokenModel.expires_at > datetime.now(timezone.utc)
        ).first()

        if not db_refresh_token:
            # Registrar falha de refresh token
            SecurityLogger.log_security_event(
                event_type="token_refresh_failure",
                ip_address=client_ip,
                details={"error": "Refresh token inválido ou expirado"},
                level="warning"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Obter o usuário
        user_repository = UserRepositoryImpl(db)
        user = await user_repository.get_by_id(UUID(db_refresh_token.user_id))

        if not user:
            # Registrar falha de refresh token
            SecurityLogger.log_security_event(
                event_type="token_refresh_failure",
                ip_address=client_ip,
                details={"error": "Usuário não encontrado", "user_id": db_refresh_token.user_id},
                level="warning"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Criar novo access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token, expires = auth_service.create_access_token(
            user_id=user.id, role=user.role, expires_delta=access_token_expires
        )

        # Criar novo refresh token
        new_refresh_token, refresh_expires = auth_service.create_refresh_token(user_id=user.id)

        # Revogar o refresh token antigo
        db_refresh_token.revoked = True

        # Salvar novo refresh token
        new_db_refresh_token = RefreshTokenModel(
            token=new_refresh_token,
            expires_at=refresh_expires,
            user_id=str(user.id),
        )
        db.add(new_db_refresh_token)
        await db.commit()

        # Registrar refresh token bem-sucedido
        SecurityLogger.log_token_refresh(
            user_id=user.id,
            ip_address=client_ip,
            success=True
        )

        # Calcular tempo de expiração em segundos
        expires_in = int(access_token_expires.total_seconds())

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": expires_in
        }
    except Exception as e:
        # Registrar erro inesperado
        if not isinstance(e, HTTPException):
            SecurityLogger.log_security_event(
                event_type="token_refresh_error",
                ip_address=client_ip,
                details={"error": str(e)},
                level="error"
            )
        raise
