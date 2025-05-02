from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_db
from backend.core.security import get_current_user
from backend.domain.ticket.ticket_service import TicketService
from backend.domain.user.user_model import User

ticket = APIRouter()


@ticket.post("/buy", status_code=201)
async def create_ticket(
    event_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    print(event_id)
    service = TicketService(db)
    ticket = await service.create_ticket(user.id, event_id)
    return JSONResponse(
        content={
            "status": "success",
            "message": "ticket created",
            "data": {"username": ticket.username, "event": dict(ticket.event)},
        }
    )


@ticket.get("", status_code=200)
async def get_tickets_by_user(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    service = TicketService(db)
    tickets = await service.get_tickets_by_user(user.id)
    return JSONResponse(
        content={
            "status": "success",
            "message": f"ticket list for user {user.username}",
            "data": [{"username": ticket.username, "event": dict(ticket.event)} for ticket in tickets],
        }
    )
