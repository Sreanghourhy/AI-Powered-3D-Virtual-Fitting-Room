from fastapi import FastAPI

from app.api import data, garments, health, jobs, scans
from app.core.config import get_settings
from app.core.local_only import protect


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
    protect(app)  # localhost-only access, no CORS (CR-02, D10)
    app.include_router(health.router)
    app.include_router(garments.router)
    app.include_router(jobs.router)
    app.include_router(data.router)
    app.include_router(scans.router)
    return app


app = create_app()
