from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from backend.domain.ticket.ticket_model import Ticket
from backend.exceptions.exceptions import BadCredentialsError

class TicketRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_ticket(self, ticket: Ticket) -> Ticket:
        try:
            self.session.add(ticket)
            await self.session.commit()
            await self.session.refresh(ticket)
            return ticket
        except IntegrityError:
            raise BadCredentialsError

    async def get_ticket_by_user(self, user_id: int) -> Sequence[Ticket]:
        response = await self.session.scalars(
            select(Ticket)
            .where(Ticket.user_id == user_id)
            .options(selectinload(Ticket.event),
                     selectinload(Ticket.user)))
        tickets = response.all()
        return tickets