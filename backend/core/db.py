from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = create_async_engine(url=settings.DATABASE_URL)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Parent class for all other
class Base(DeclarativeBase):
    pass


# Session generator
async def get_db():
    async with async_session() as session:
        yield session
