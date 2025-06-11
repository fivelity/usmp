import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import (
    Depends,
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.websockets import WebSocketState

from app.api.api import api_router
from app.core.config import get_settings
from app.core.exceptions import AppError, app_error_handler
from app.core.logging import setup_logging, get_logger
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.models.websocket import WebSocketMessage
from app.services.realtime_service import RealtimeService
from app.services.sensor_manager import SensorManager
from app.websocket_manager import WebSocketManager

# Initialize logging
setup_logging()

settings = get_settings()


def get_sensor_manager(request: Request) -> SensorManager:
    return request.app.state.sensor_manager


def get_realtime_service(request: Request) -> RealtimeService:
    return request.app.state.realtime_service


def get_websocket_manager(request: Request) -> WebSocketManager:
    return request.app.state.websocket_manager


def _create_services() -> tuple[SensorManager, WebSocketManager, RealtimeService]:
    """Factory to create core services."""
    _sensor_manager = SensorManager(settings=settings)
    _websocket_manager = WebSocketManager()
    _realtime_service = RealtimeService(
        sensor_manager=_sensor_manager, websocket_manager=_websocket_manager
    )
    return _sensor_manager, _websocket_manager, _realtime_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context managing startup and shutdown."""
    sensor_manager, websocket_manager, realtime_service = _create_services()

    # Attach to app state for DI
    app.state.sensor_manager = sensor_manager
    app.state.websocket_manager = websocket_manager
    app.state.realtime_service = realtime_service
    app.state.start_time = time.time()

    # Startup logic
    await sensor_manager.start_all_sensors()
    asyncio.create_task(realtime_service.broadcast_updates())

    try:
        yield
    finally:
        # Shutdown logic
        await sensor_manager.shutdown_all_sensors()
        if realtime_service.is_running:
            await realtime_service.stop()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
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

    # Security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)

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
            get_logger(__name__).info(
                "Client %s disconnected", websocket.client.host
            )
        except Exception as e:
            get_logger(__name__).error(
                "Error in WebSocket connection for %s: %s",
                websocket.client.host,
                e,
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
            get_logger(__name__).info(
                "Client %s disconnected", websocket.client.host
            )

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
async def health_check(request: Request):
    """Performs a health check of the application."""
    sensor_manager: SensorManager = request.app.state.sensor_manager

    active_sources = [
        source_id
        for source_id, source in sensor_manager.get_all_sources().items()
        if source.is_active
    ]

    websocket_manager: WebSocketManager = request.app.state.websocket_manager

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "active_sources": active_sources,
            "connected_clients": websocket_manager.get_active_connections(),
            "uptime_seconds": time.time() - request.app.state.start_time,
        },
    )
