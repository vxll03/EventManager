from pydantic import BaseModel

from backend.domain.event.event_schema import EventResponse


class TicketResponse(BaseModel):
    username: str
    event: EventResponse