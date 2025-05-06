from enum import Enum as PyEnum

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core import Base


# Role enumerate
class Role(PyEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    ORGANIZER = "ORGANIZER"


# User SQLAlchemy table
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(Text)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)

    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tickets: Mapped["Ticket"] = relationship("Ticket", back_populates="user")
