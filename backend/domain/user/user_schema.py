from pydantic import BaseModel, field_validator, model_validator

from backend.domain.user import Role


# Token
class Token(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


# User
class UserCreate(BaseModel):
    username: str
    password: str
    role: Role = Role.USER

    @field_validator("username")
    def username_validate(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Username too long")
        if len(value) < 4:
            raise ValueError("Username too short")
        return value

    @field_validator("password")
    def pass_validate(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Password too long")
        if len(value) < 8:
            raise ValueError("Password too short")
        return value

    @model_validator(mode="after")
    def credentials_validate(self) -> "UserCreate":
        if self.username == self.password:
            raise ValueError("Password cannot match username")
        return self


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str

    @model_validator(mode="after")
    def credentials_validate(self) -> "UserUpdatePassword":
        if self.old_password == self.new_password:
            raise ValueError("New password same as old password")
        return self

    @field_validator("new_password")
    def pass_validate(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Password too long")
        if len(value) < 8:
            raise ValueError("Password too short")
        return value


class UserActivation(BaseModel):
    is_active: bool
