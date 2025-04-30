from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, Text, VARCHAR

from backend.core.db import Base


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(VARCHAR(100))
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(VARCHAR(100))
    capacity: Mapped[int] = mapped_column(Integer)

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
