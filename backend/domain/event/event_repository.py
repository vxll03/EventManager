from datetime import datetime
from typing import Sequence
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from backend.domain.event.event_model import Event


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_events(
        self,
        location: str | None = None,
        date: datetime | None = None,
    ) -> Sequence[Event]:
        params = []
        if location:
            params.append(Event.location == location)
        if date:
            params.append(Event.start_time <= date)

        response = await self.session.scalars(
            select(Event).where(and_(*params)) if params else select(Event)
        )
        return response.all()

    async def create_event(
        self,
        title: str,
        description: str,
        location: str,
        capacity: int,
        start_time: datetime,
        end_time: datetime,
    ) -> Event:
        db_event = Event(
            title=title,
            description=description,
            location=location,
            capacity=capacity,
            start_time=start_time,
            end_time=end_time,
        )
        self.session.add(db_event)
        await self.session.commit()
        await self.session.refresh(db_event)
        return db_event
