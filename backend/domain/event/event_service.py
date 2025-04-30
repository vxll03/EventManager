from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.event.event_repository import EventRepository
from backend.domain.event.event_schema import EventCreate, EventResponse
from backend.exceptions.exceptions import NotFoundError


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = EventRepository(session)

    async def get_events(
        self,
        location: str | None = None,
        date: datetime | None = None,
    ) -> List[EventResponse]:
        events = await self.repo.get_events(location=location, date=date)
        if len(events) <= 0:
            raise NotFoundError("No events found")
        return [EventResponse.model_validate(event) for event in events]

    async def create_event(self, event: EventCreate) -> EventResponse:
        new_event = await self.repo.create_event(
            event.title,
            event.description,
            event.location,
            event.capacity,
            event.start_time,
            event.end_time,
        )
        return EventResponse.model_validate(new_event)
