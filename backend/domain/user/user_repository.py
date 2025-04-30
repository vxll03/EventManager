from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from backend.domain.user import User
from backend.domain.user.user_model import Role
from backend.exceptions.exceptions import UserAlreadyExistsError


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, username: str, password: str, role: Role) -> User:
        try:
            db_user = User(username=username, password=password, role=role)
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError(username=username)