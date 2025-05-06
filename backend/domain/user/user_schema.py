from pydantic import BaseModel, Field, model_validator

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
    username: str = Field(min_length=4, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    role: Role = Role.USER

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
    new_password: str = Field(min_length=8, max_length=100)

    @model_validator(mode="after")
    def credentials_validate(self) -> "UserUpdatePassword":
        if self.old_password == self.new_password:
            raise ValueError("New password same as old password")
        return self


class UserActivation(BaseModel):
    is_active: bool
