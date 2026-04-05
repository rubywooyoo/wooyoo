from datetime import datetime, timezone

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.schemas.common import HealthResponse
from app import models  # noqa: F401

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix=settings.api_prefix)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        timestamp=datetime.now(timezone.utc),
    )
