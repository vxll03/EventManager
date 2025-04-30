from fastapi import Depends, Request
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from backend.core.db import get_db
from backend.domain.user.user_model import User
from backend.domain.user.user_schema import TokenData

from .config import settings

# Exceptions
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

refresh_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token",
    headers={"WWW-Authenticate": "Bearer"},
)


# Authenticate functions
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(db: AsyncSession, username: str) -> User | None:
    user = await db.scalar(select(User).where(User.username == username))
    return user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user or not verify_password(password, user.password):
        return
    return user


# Token create functions
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    to_encode.update({"type": "access"})

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type": "refresh"})

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# Token validation functions
# Валидация пользователя через Access Token (авторизация)
async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise credentials_exception
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")

        if username is None or payload.get("type") != "access":
            raise credentials_exception

        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


# Валидация Refresh Token для обновления Access Token
async def validate_refresh_token(db: AsyncSession, refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if not username:
            raise refresh_token_exception

        if payload.get("type") != "refresh":
            raise refresh_token_exception

        user = await get_user(db, username=username)
        if not user:
            raise refresh_token_exception

        return user
    except JWTError:
        raise refresh_token_exception
