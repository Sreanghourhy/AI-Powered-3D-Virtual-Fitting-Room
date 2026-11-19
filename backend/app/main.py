from fastapi import FastAPI

from app.api import auth, consents, health
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="AI-Powered 3D Virtual Fitting Room API",
        version="0.1.0",
        # Hide interactive docs in production.
        docs_url=None if settings.environment == "production" else "/docs",
        redoc_url=None,
        openapi_url=None if settings.environment == "production" else "/openapi.json",
    )
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(consents.router)
    return app


app = create_app()
