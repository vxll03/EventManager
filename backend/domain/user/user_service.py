from datetime import timedelta
from typing import Any, Dict, List

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_user,
    validate_refresh_token,
    verify_password,
)
from backend.domain.user import Role, User
from backend.domain.user.user_repository import UserRepository
from backend.domain.user.user_schema import Token, UserCreate, UserLogin
from backend.exceptions.exceptions import (
    BadCredentialsError,
    NotFoundError,
    TokenNotFoundError,
    UserAlreadyExistsError,
)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = UserRepository(session)

    async def register(self, user_data: UserCreate) -> User:
        if await get_user(self.session, user_data.username):
            raise UserAlreadyExistsError(
                username=user_data.username,
                message="User already exists",
            )

        hashed_password = get_password_hash(user_data.password)
        user = await self.repo.create_user(
            user_data.username, hashed_password, user_data.role
        )
        return user

    async def login(self, user_data: UserLogin) -> List[Dict]:
        user = await get_user(self.session, user_data.username)
        if not user:
            raise NotFoundError(f"User not found with name {user_data.username}")

        if not user.is_active:
            raise BadCredentialsError("User is not active")

        if not verify_password(user_data.password, user.password):
            raise BadCredentialsError("Incorrect password")

        token = await generate_token(user.username, user.role, refresh=True)
        return await generate_cookie(token, refresh=True)

    async def refresh(self, request: Request) -> List[Dict]:
        token = request.cookies.get("refresh_token")
        if not token:
            raise TokenNotFoundError("User not logged in")

        user = await validate_refresh_token(self.session, token)

        if not user.is_active:
            raise BadCredentialsError("User is not active")

        new_access_token = await generate_token(user.username, user.role)
        return await generate_cookie(new_access_token)

    async def change_password(
        self, username: str, old_password: str, new_password: str
    ):
        user: User | None = await authenticate_user(
            self.session, username, old_password
        )
        if not user:
            raise BadCredentialsError("Incorrect password")

        user.password = get_password_hash(new_password)
        await self.session.commit()
        await self.session.refresh(user)

    async def deactivate(self, username: str, password: str):
        user: User | None = await authenticate_user(self.session, username, password)
        if not user:
            raise BadCredentialsError("Incorrect password")

        user.is_active = False
        await self.session.commit()
        await self.session.refresh(user)


# Functions for creating tokens and cookies
async def generate_token(username: str, role: Role, refresh: bool = False) -> Token:
    access_token = create_access_token(
        data={"sub": username, "role": role.value},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    if refresh:
        refresh_token = create_refresh_token(data={"sub": username, "role": role.value})
    else:
        refresh_token = None

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


async def generate_cookie(token: Token, refresh: bool = False) -> List[Dict[str, Any]]:
    access_token = {
        "key": "access_token",
        "value": token.access_token,
        "httponly": True,
        "secure": settings.IS_PROD,
        "samesite": "lax",
        "max_age": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

    if refresh:
        refresh_token = {
            "key": "refresh_token",
            "value": token.refresh_token,
            "httponly": True,
            "secure": settings.IS_PROD,
            "samesite": "lax",
            "max_age": settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        }
        return [access_token, refresh_token]

    return [access_token]
