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
        client_host = getattr(websocket.client, 'host', 'unknown') if websocket.client else 'unknown'
        logger = get_logger(__name__)
        
        # Validate connection before accepting
        try:
            await manager.connect(websocket)
            logger.info("Client %s connected successfully", client_host)
        except Exception as e:
            logger.error("Failed to establish connection with %s: %s", client_host, e)
            try:
                await websocket.close(code=1011, reason="Connection setup failed")
            except Exception:
                pass  # Connection may already be closed
            return

        connection_active = True
        heartbeat_failures = 0
        max_heartbeat_failures = 3
        
        try:
            while connection_active:
                # Check connection state before attempting to receive
                if websocket.application_state != WebSocketState.CONNECTED:
                    logger.warning("WebSocket state changed to %s for client %s", 
                                 websocket.application_state, client_host)
                    break
                
                try:
                    # Set a reasonable timeout for receiving messages
                    message_text = await asyncio.wait_for(
                        websocket.receive_text(), 
                        timeout=30.0  # 30 second timeout
                    )
                    
                    # Reset heartbeat failure counter on successful message
                    heartbeat_failures = 0
                    
                    # Validate message before processing
                    if not message_text or not message_text.strip():
                        logger.warning("Received empty message from client %s", client_host)
                        continue
                    
                    # Process the message
                    await rt_service.handle_incoming_ws_message(
                        websocket, message_text
                    )
                    
                except asyncio.TimeoutError:
                    # Handle timeout - this could be normal if no messages are sent
                    heartbeat_failures += 1
                    logger.debug("Timeout waiting for message from client %s (failure %d/%d)", 
                               client_host, heartbeat_failures, max_heartbeat_failures)
                    
                    if heartbeat_failures >= max_heartbeat_failures:
                        logger.warning("Too many heartbeat failures for client %s, closing connection", 
                                     client_host)
                        break
                    
                    # Send a ping to check if connection is still alive
                    try:
                        await websocket.ping()
                    except Exception as ping_error:
                        logger.error("Failed to ping client %s: %s", client_host, ping_error)
                        break
                        
                except WebSocketDisconnect:
                    logger.info("Client %s disconnected normally", client_host)
                    connection_active = False
                    break
                    
                except Exception as msg_error:
                    logger.error("Error processing message from client %s: %s", 
                               client_host, msg_error)
                    
                    # Send error response to client if possible
                    try:
                        if isinstance(msg_error, AppError):
                            await manager.send_to_client(
                                websocket,
                                WebSocketMessage(
                                    event="error",
                                    data={
                                        "message": msg_error.message,
                                        "code": msg_error.error_code,
                                        "timestamp": time.time(),
                                    },
                                ),
                            )
                        else:
                            await manager.send_to_client(
                                websocket,
                                WebSocketMessage(
                                    event="error",
                                    data={
                                        "message": "An error occurred processing your request",
                                        "timestamp": time.time(),
                                    },
                                ),
                            )
                    except Exception as send_error:
                        logger.error("Failed to send error message to client %s: %s", 
                                   client_host, send_error)
                        # If we can't send error messages, the connection is likely broken
                        break

        except Exception as outer_error:
            logger.error("Unexpected error in WebSocket connection for %s: %s", 
                        client_host, outer_error)
        finally:
            # Ensure cleanup always happens
            try:
                manager.disconnect(websocket)
                logger.info("Cleaned up connection for client %s", client_host)
            except Exception as cleanup_error:
                logger.error("Error during connection cleanup for %s: %s", 
                           client_host, cleanup_error)
            
            # Attempt graceful close if connection is still open
            try:
                if websocket.application_state == WebSocketState.CONNECTED:
                    await websocket.close(code=1000, reason="Server shutdown")
            except Exception:
                pass  # Connection may already be closed

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
