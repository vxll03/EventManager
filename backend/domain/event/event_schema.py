from datetime import datetime, timezone
from pydantic import BaseModel, field_validator, model_validator


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    capacity: int

    start_time: datetime
    end_time: datetime

    @field_validator("title")
    def title_validate(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Title too long")
        if len(value) < 5:
            raise ValueError("Title too short")
        return value

    @field_validator("location")
    def location_validate(cls, value: str) -> str:
        if len(value) > 100:
            raise ValueError("Title too long")
        if len(value) < 5:
            raise ValueError("Title too short")
        return value

    @field_validator("capacity")
    def capacity_validator(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Capacity too small")
        return value

    @field_validator("start_time", "end_time")
    def start_end_validator(cls, value: datetime) -> datetime:
        if value.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
            raise ValueError("Date cannot be in the past")
        return value

    @model_validator(mode="after")
    def end_validate(self) -> "EventCreate":
        if self.start_time >= self.end_time:
            raise ValueError("End cannot be earlier than start")
        return self


class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    capacity: int

    start_time: datetime
    end_time: datetime

    @field_validator("start_time", "end_time")
    def serialize_departure_date(cls, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M")

    class Config:
        from_attributes = True


class EventFilter(BaseModel):
    location: str | None = None
    date: datetime | None = None
