from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core import get_db, get_current_user
from backend.domain.user import User
from backend.domain.user.user_schema import UserCreate, UserLogin, UserUpdatePassword
from backend.domain.user.user_service import UserService

user = APIRouter()


# Register user into DB
@user.post("/register", status_code=201)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    user = await service.register(user_data)
    return JSONResponse(
        content={
            "status": "success",
            "message": "user created",
            "data": {"username": user.username},
        }
    )


# Log user in
@user.post("/login", status_code=200)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    service = UserService(db)
    cookies = await service.login(user_data)

    response = JSONResponse(content={"status": "success", "message": "logged in"})
    response.set_cookie(**cookies[0])
    response.set_cookie(**cookies[1])
    return response


# Refresh user's token
@user.post(
    "/refresh",
    status_code=200,
    dependencies=[Depends(get_current_user)],
)
async def refresh(request: Request, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    service = UserService(db)
    cookies = await service.refresh(request)

    response = JSONResponse(
        content={"status": "success", "message": "tokens are refreshed"}
    )
    response.set_cookie(**cookies[0])
    return response


# Log user out
@user.post("/logout", status_code=200, dependencies=[Depends(get_current_user)])
async def logout() -> JSONResponse:
    response: JSONResponse = JSONResponse(
        content={"status": "success", "message": "logged out"}
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


# Change user's password
@user.post("/password/change", status_code=200)
async def change_password(
    passwords: UserUpdatePassword,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> JSONResponse:
    service = UserService(db)
    await service.change_password(
        user.username, passwords.old_password, passwords.new_password
    )
    return JSONResponse(
        content={
            "status": "success",
            "message": "password changed",
            "data": {"username": user.username},
        }
    )


# Deactivate user in db
@user.post("/deactivate", status_code=200)
async def deactivate(
    password: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> JSONResponse:
    service = UserService(db)
    await service.deactivate(user.username, password)
    return JSONResponse(
        {
            "status": "success",
            "message": "user deactivated",
            "data": {"username": user.username},
        }
    )
