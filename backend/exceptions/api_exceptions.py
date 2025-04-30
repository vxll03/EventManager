from fastapi import Request
from fastapi.responses import JSONResponse

from backend.exceptions.exceptions import (
    BadCredentialsError,
    NotFoundError,
    TokenNotFoundError,
    UserAlreadyExistsError,
)


def register_exceptions_handler(app):
    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(
        request: Request, exc: UserAlreadyExistsError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "error": str(exc),
                "data": {"username": exc.username},
            },
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "error": str(exc),
            },
        )

    @app.exception_handler(BadCredentialsError)
    async def bad_credentials_handler(request: Request, exc: BadCredentialsError):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "error": str(exc),
            },
        )

    @app.exception_handler(TokenNotFoundError)
    async def token_not_found_handler(request: Request, exc: TokenNotFoundError):
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "error": str(exc),
            },
        )
