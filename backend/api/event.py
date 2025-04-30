from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_db
from backend.core.security import get_current_role, get_current_user
from backend.domain.event.event_schema import EventCreate, EventFilter
from backend.domain.event.event_service import EventService

event = APIRouter()


@event.get("/", status_code=200, dependencies=[Depends(get_current_user)])
async def get_events(
    param: EventFilter = Depends(),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    service = EventService(db)
    events = await service.get_events(location=param.location, date=param.date)

    return JSONResponse(content={
        "status": "success",
        "message": "events found",
        "data": list(map(dict, events))
    })


@event.post(
    "/", 
    status_code=201, 
    dependencies=[Depends(get_current_role)])
async def create_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    service = EventService(db)
    new_event = await service.create_event(event)
    
    return JSONResponse(content={
        "status": "success",
        "message": "event created",
        "data": dict(new_event)
    })