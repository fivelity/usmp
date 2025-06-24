# /server/app/api/debug_routes.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.sensor_manager import SensorManager
from app.core.config import get_settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/debug/sensors")
async def debug_sensors():
    """
    An endpoint to get a detailed list of all discovered sensors,
    including their current values. Useful for debugging sensor issues.
    """
    sensor_manager = SensorManager(settings=get_settings())
    await sensor_manager.initialize()
    all_sensors = sensor_manager.get_all_sensors_with_readings()
    await sensor_manager.shutdown()
    return all_sensors


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify that the server is running.
    """
    return {"status": "ok"}


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the main index.html page for the frontend.
    This is a fallback for when the application is not being served by a dedicated web server.
    """

    # In a real-world scenario, you'd want to serve the SvelteKit build output.
    # This is a simple placeholder.
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/test-websocket", response_class=HTMLResponse)
async def websocket_test_page(request: Request):
    """
    A simple HTML page for testing the WebSocket connection.
    """
    return templates.TemplateResponse("websocket_test.html", {"request": request})
