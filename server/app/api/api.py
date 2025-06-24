from fastapi import APIRouter
from app.api.endpoints import (
    system,
    settings,
    sensors,
    presets,
    widgets,
)  # Import other endpoint routers here as they are created

api_router = APIRouter()

# Include routers from endpoint modules
api_router.include_router(system.router, prefix="/system", tags=["System"])
# api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
api_router.include_router(presets.router, prefix="/presets", tags=["Presets"])
api_router.include_router(widgets.router, prefix="/widgets", tags=["Widgets"])

# This main api_router will be included by the FastAPI app instance in main.py
