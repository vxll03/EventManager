from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.exceptions.api_exceptions import register_exceptions_handler
from backend.api import user, event, ticket

prefix = "/api"

app = FastAPI(
    title="Transport App",
)
register_exceptions_handler(app)

# Middleware
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Endpoints
app.include_router(user, prefix=f"{prefix}/auth", tags=["Auth"])
app.include_router(event, prefix=f"{prefix}/events", tags=["Events"])
app.include_router(ticket, prefix=f"{prefix}/tickets", tags=["Tickets"])