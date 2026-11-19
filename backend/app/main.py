from fastapi import FastAPI

from app.api import health

app = FastAPI(title="AI-Powered 3D Virtual Fitting Room API", version="0.1.0")

app.include_router(health.router)
