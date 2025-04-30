from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = Field(
        min_length=32, description="Секретный ключ для подписи токенов"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = Field(
        default=10, description="Время жизни access токена в минутах"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: PositiveInt = Field(
        default=7, description="Время жизни refresh токена в днях"
    )
    ALGORITHM: str = Field(default="HS256", description="Алгоритм подписи токенов")

    # Cookies
    IS_PROD: bool

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        """Асинхронная URL для приложения."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self):
        """Синхронная URL для миграций."""
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
