import asyncio
import time

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.websockets import WebSocketState

from app.api.api import api_router
from app.core.config import get_settings
from app.core.exceptions import AppError, app_error_handler
from app.core.logging_config import setup_logging
from app.models.websocket import WebSocketMessage
from app.services.realtime_service import RealtimeService
from app.services.sensor_manager import SensorManager
from app.websocket_manager import WebSocketManager

# Initialize logging
setup_logging()

# Global variables
settings = get_settings()
sensor_manager: SensorManager | None = None
realtime_service: RealtimeService | None = None
websocket_manager: WebSocketManager | None = None


def get_sensor_manager() -> SensorManager:
    if sensor_manager is None:
        raise RuntimeError("SensorManager not initialized")
    return sensor_manager


def get_realtime_service() -> RealtimeService:
    if realtime_service is None:
        raise RuntimeError("RealtimeService not initialized")
    return realtime_service


def get_websocket_manager() -> WebSocketManager:
    if websocket_manager is None:
        raise RuntimeError("WebSocketManager not initialized")
    return websocket_manager


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    global sensor_manager, realtime_service, websocket_manager
    app = FastAPI(
        title=settings.app_name,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )
    app.state.start_time = time.time()

    # Initialize services
    sensor_manager = SensorManager(settings=settings)
    websocket_manager = WebSocketManager()
    realtime_service = RealtimeService(
        sensor_manager=sensor_manager, websocket_manager=websocket_manager
    )

    # Exception Handlers
    app.add_exception_handler(AppError, app_error_handler)

    # Middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip()
                for origin in settings.BACKEND_CORS_ORIGINS.split(",")
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Startup and Shutdown events
    @app.on_event("startup")
    async def startup_event():
        """Handles application startup events."""
        print("🚀 Application starting up...")
        await get_sensor_manager().start_all_sensors()
        asyncio.create_task(get_realtime_service().broadcast_updates())
        print("✅ Sensor manager and realtime service started.")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Handles application shutdown events."""
        print("Application shutting down...")
        await get_sensor_manager().shutdown_all_sensors()
        if realtime_service and realtime_service.is_running:
            await realtime_service.stop()
        print("Services stopped.")

    # API Router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # WebSocket Endpoint
    @app.websocket("/ws")
    async def websocket_endpoint(
        websocket: WebSocket,
        manager: WebSocketManager = Depends(get_websocket_manager),
        rt_service: RealtimeService = Depends(get_realtime_service),
    ):
        """Main WebSocket endpoint for real-time communication."""
        await manager.connect(websocket)
        try:
            while websocket.application_state == WebSocketState.CONNECTED:
                message_text = await websocket.receive_text()
                await rt_service.handle_incoming_ws_message(
                    websocket, message_text
                )

        except WebSocketDisconnect:
            print(f"Client {websocket.client.host} disconnected")
        except Exception as e:
            print(
                "Error in WebSocket connection for "
                f"{websocket.client.host}: {e}"
            )
            if isinstance(e, AppError):
                await manager.send_to_client(
                    websocket,
                    WebSocketMessage(
                        event="error",
                        data={
                            "message": e.message,
                            "code": e.error_code,
                        },
                    ),
                )
            else:
                await manager.send_to_client(
                    websocket,
                    WebSocketMessage(
                        event="error",
                        data={"message": "An unknown error occurred"},
                    ),
                )
        finally:
            manager.disconnect(websocket)
            print(f"Client {websocket.client.host} disconnected")

    return app


app = create_app()


# Optional: Add a root endpoint for basic info
@app.get("/")
async def read_root():
    """Provides basic information about the application."""
    return {
        "project": "Ultimate Sensor Monitor",
        "version": "1.0.0",
        "description": "Real-time hardware sensor monitoring application",
        "docs": "/docs",
        "api_version": settings.API_V1_STR,
    }


@app.get("/health")
async def health_check():
    """Performs a health check of the application."""
    sensor_manager = get_sensor_manager()
    active_sources = [
        source_id
        for source_id, source in sensor_manager.get_all_sources().items()
        if source.is_active
    ]

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "active_sources": active_sources,
            "connected_clients": (
                get_websocket_manager().get_active_connections()
            ),
            "uptime_seconds": time.time() - app.state.start_time,
        },
    )
