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
from app.services.realtime_service import RealTimeService
from app.services.sensor_manager import SensorManager
from app.websocket_manager import WebSocketManager

# Initialize logging
setup_logging()

settings = get_settings()


def get_sensor_manager(request: Request) -> SensorManager:
    return request.app.state.sensor_manager


def get_realtime_service(request: Request) -> RealTimeService:
    return request.app.state.realtime_service


def get_websocket_manager(request: Request) -> WebSocketManager:
    return request.app.state.websocket_manager


def _create_services() -> tuple[SensorManager, WebSocketManager, RealTimeService]:
    """Factory to create core services."""
    _sensor_manager = SensorManager(settings=settings)
    _websocket_manager = WebSocketManager()
    _realtime_service = RealTimeService(
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
    await sensor_manager.initialize()
    await realtime_service.start(settings)

    try:
        yield
    finally:
        # Shutdown logic
        await sensor_manager.shutdown()
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
        rt_service: RealTimeService = Depends(get_realtime_service),
    ):
        """Main WebSocket endpoint for real-time communication."""
        client_id = f"client_{int(time.time() * 1000)}"
        logger = get_logger(__name__)
        
        try:
            await manager.connect(websocket, client_id)
            logger.info(f"WebSocket client {client_id} connected successfully")
            
            # Simply wait for disconnect - no forced message receiving
            # The client will receive sensor data via broadcasts from the realtime service
            try:
                while True:
                    # Optional: Handle incoming messages if any (like ping/pong)
                    try:
                        # Wait for messages with a long timeout, but don't require them
                        message = await asyncio.wait_for(
                            websocket.receive_text(), 
                            timeout=300.0  # 5 minutes - very long timeout
                        )
                        
                        # Process any client messages (like ping, configuration changes, etc.)
                        if message:
                            await rt_service.handle_incoming_ws_message(websocket, message)
                            
                    except asyncio.TimeoutError:
                        # Timeout is normal - just continue the loop
                        # Send a heartbeat to check connection health
                        try:
                            await websocket.ping()
                        except Exception:
                            # Connection is dead, break the loop
                            break
                            
            except WebSocketDisconnect:
                logger.info(f"WebSocket client {client_id} disconnected normally")
                
        except Exception as e:
            logger.error(f"WebSocket error for client {client_id}: {e}")
        finally:
            # Always clean up
            manager.disconnect(websocket, client_id)

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
        source["source_id"]
        for source in sensor_manager.get_available_sources()
        if source.get("available")
    ]

    websocket_manager: WebSocketManager = request.app.state.websocket_manager

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "active_sources": active_sources,
            "connected_clients": len(websocket_manager.active_connections),
            "uptime_seconds": time.time() - request.app.state.start_time,
        },
    )
