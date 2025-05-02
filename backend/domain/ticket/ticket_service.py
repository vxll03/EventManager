from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.event.event_repository import EventRepository
from backend.domain.event.event_schema import EventResponse
from backend.domain.ticket.ticket_model import Ticket
from backend.domain.ticket.ticket_repository import TicketRepository
from backend.domain.ticket.ticket_schema import TicketResponse
from backend.exceptions.exceptions import NotFoundError


class TicketService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TicketRepository(session)

    async def create_ticket(self, user_id: int, event_id: int) -> TicketResponse:
        event = await EventRepository(self.session).get_event_by_id(event_id)
        if event is None:
            raise NotFoundError("Event not found")

        ticket = Ticket(user_id=user_id, event_id=event_id)
        
        db_ticket = await self.repo.create_ticket(ticket)
        ticket_response = TicketResponse(
            username=ticket.user.username,
            event= EventResponse.model_validate(db_ticket.event),
        )
        return ticket_response

    async def get_tickets_by_user(self, user_id: int) -> List[TicketResponse]:
        tickets = await self.repo.get_ticket_by_user(user_id)
        if not tickets:
            raise NotFoundError("No tickets found")

        tickets_response = [
            TicketResponse(
                username=ticket.user.username,
                event=EventResponse.model_validate(ticket.event),
            )
            for ticket in tickets
        ]

        return tickets_response
