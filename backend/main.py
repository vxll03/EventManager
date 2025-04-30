from fastapi import FastAPI
from backend.exceptions.api_exceptions import register_exceptions_handler
from backend.api import user, event

prefix = "/api"

app = FastAPI(
    title="Transport App",
)
register_exceptions_handler(app)

# Endpoints
app.include_router(user, prefix=f"{prefix}/auth", tags=["Auth"])
app.include_router(event, prefix=f"{prefix}/events", tags=["Events"])