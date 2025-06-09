import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn # Required for uvicorn.run in __main__

from app.api.api import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.security import SecurityHeaders
from app.core.exceptions import (
    UltimonException,
    SensorException,
    ConfigurationException,
    ValidationException
)
from fastapi.responses import JSONResponse
from fastapi import status
from app.websocket_manager import WebSocketManager
from app.services.sensor_manager import SensorManager
from app.services.realtime_service import RealTimeService

# Configure logging
setup_logging()
logger = get_logger("main")

# Initialize services (will be initialized in lifespan)
websocket_manager = None
sensor_manager = None
realtime_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global websocket_manager, sensor_manager, realtime_service
    
    logger.info("Application startup: Initializing resources...")
    
    # Initialize services
    websocket_manager = WebSocketManager()
    sensor_manager = SensorManager(settings=get_settings())
    realtime_service = RealTimeService(sensor_manager, websocket_manager)
    
    # Start services in order
    await websocket_manager.initialize()
    logger.info("WebSocketManager initialized.")
    await sensor_manager.initialize()
    logger.info("SensorManager initialized.")
    await realtime_service.start(get_settings())
    logger.info("RealTimeService started.")
    
    # Get origins for logging
    origins = []
    if get_settings().backend_cors_origins:
        origins_raw = get_settings().backend_cors_origins.split(",")
        for origin in origins_raw:
            origins.append(origin.strip())
    logger.info(f"Allowed CORS origins: {origins if origins else '*'}")
    
    yield
    
    # Shutdown
    logger.info("Application shutdown: Cleaning up resources...")
    if realtime_service:
        await realtime_service.stop()
        logger.info("RealTimeService stopped.")
    if websocket_manager:
        await websocket_manager.cleanup()
        logger.info("WebSocketManager cleaned up.")
    if sensor_manager:
        await sensor_manager.shutdown()
        logger.info("SensorManager shut down.")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title=get_settings().app_name,
    openapi_url=f"{get_settings().api_v1_str}/openapi.json",
    lifespan=lifespan
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    headers = SecurityHeaders.get_headers()
    for key, value in headers.items():
        response.headers[key] = value
    return response

# CORS Middleware
# Origins should be more restrictive in a production environment
origins = []
if get_settings().backend_cors_origins:
    origins_raw = get_settings().backend_cors_origins.split(",")
    for origin in origins_raw:
        origins.append(origin.strip())

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else: # Default permissive CORS if not specified
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allows all origins
        allow_credentials=True,
        allow_methods=["*"], # Allows all methods
        allow_headers=["*"], # Allows all headers
    )


# Global Exception Handlers
@app.exception_handler(UltimonException)
async def ultimon_base_exception_handler(request: Request, exc: UltimonException):
    return JSONResponse(
        status_code=getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={
            "error": exc.error_code or "internal_server_error",
            "message": exc.message,
            "details": exc.details,
        },
    )

@app.exception_handler(SensorException)
async def sensor_exception_handler(request: Request, exc: SensorException):
    default_status = status.HTTP_503_SERVICE_UNAVAILABLE
    if exc.error_code == "sensor_not_found": # Example specific error code handling
        default_status = status.HTTP_404_NOT_FOUND
    return JSONResponse(
        status_code=getattr(exc, 'status_code', default_status),
        content={
            "error": exc.error_code or "sensor_error",
            "message": exc.message,
            "details": exc.details,
        },
    )

@app.exception_handler(ConfigurationException)
async def configuration_exception_handler(request: Request, exc: ConfigurationException):
    return JSONResponse(
        status_code=getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={
            "error": exc.error_code or "configuration_error",
            "message": exc.message,
            "details": exc.details,
        },
    )

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=getattr(exc, 'status_code', status.HTTP_422_UNPROCESSABLE_ENTITY),
        content={
            "error": exc.error_code or "validation_error",
            "message": exc.message,
            "details": exc.details,
        },
    )

# API Router
app.include_router(api_router, prefix=get_settings().api_v1_str)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                # Try to parse as JSON for structured commands
                import json
                message = json.loads(data)
                
                if isinstance(message, dict) and "command" in message:
                    # Handle structured commands
                    command = message.get("command")
                    
                    if command == "get_stats":
                        # Send real-time service stats to this client
                        stats = realtime_service.get_stats()
                        response = {
                            "type": "stats_response",
                            "data": stats,
                            "timestamp": datetime.now().isoformat()
                        }
                        await websocket_manager.send_personal_message(json.dumps(response), websocket)
                    
                    elif command == "force_broadcast":
                        # Force a broadcast and notify this client
                        success = await realtime_service.force_broadcast()
                        response = {
                            "type": "broadcast_response",
                            "success": success,
                            "timestamp": datetime.now().isoformat()
                        }
                        await websocket_manager.send_personal_message(json.dumps(response), websocket)
                    
                    else:
                        # Unknown command
                        response = {
                            "type": "error",
                            "message": f"Unknown command: {command}",
                            "timestamp": datetime.now().isoformat()
                        }
                        await websocket_manager.send_personal_message(json.dumps(response), websocket)
                else:
                    # Handle as plain text message (echo back)
                    logger.info(f"Message from {client_id}: {data}")
                    await websocket_manager.send_personal_message(f"Echo: {data}", websocket)
                    
            except json.JSONDecodeError:
                # Handle as plain text message (echo back)
                logger.info(f"Message from {client_id}: {data}")
                await websocket_manager.send_personal_message(f"Echo: {data}", websocket)
            except Exception as cmd_error:
                logger.error(f"Error processing command from {client_id}: {cmd_error}")
                error_response = {
                    "type": "error",
                    "message": f"Error processing command: {str(cmd_error)}",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket_manager.send_personal_message(json.dumps(error_response), websocket)
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, client_id)
    except Exception as e:
        logger.error(f"Error in WebSocket connection for {client_id}: {e}")
        websocket_manager.disconnect(websocket, client_id, reason=str(e))


# Real-time service status endpoints
@app.get("/realtime/stats")
async def get_realtime_stats():
    """Get real-time service statistics."""
    return realtime_service.get_stats()

@app.post("/realtime/broadcast")
async def force_broadcast():
    """Force an immediate sensor data broadcast."""
    success = await realtime_service.force_broadcast()
    return {"success": success, "message": "Broadcast initiated" if success else "Broadcast failed"}

@app.get("/sensors/status")
async def get_sensor_status():
    """Get current sensor provider status and fallback information."""
    if sensor_manager:
        providers = []
        for provider in sensor_manager.sensor_providers:
            providers.append({
                "name": provider.display_name,
                "source_id": provider.source_id,
                "available": await provider.is_available(),
                "sensor_count": len(await provider.get_available_sensors())
            })
        
        return {
            "active_providers": len(sensor_manager.sensor_providers),
            "total_sensors": len(sensor_manager._active_sensors),
            "providers": providers,
            "fallback_order": ["HWSensor (HardwareMonitor)", "LHMSensor (LibreHardwareMonitor.dll)", "MockSensor"]
        }
    return {"error": "SensorManager not available"}

@app.get("/debug/sensors")
async def debug_sensors():
    """Debug endpoint to check sensor data collection."""
    if not sensor_manager._initialized:
        return {"error": "SensorManager not initialized"}
    
    debug_info = {
        "initialized": sensor_manager._initialized,
        "provider_count": len(sensor_manager.sensor_providers),
        "active_sensors_count": len(sensor_manager._active_sensors),
        "sensor_readings_keys": list(sensor_manager._sensor_readings.keys()),
        "providers": [],
        "collector_task_running": sensor_manager._collector_task is not None and not sensor_manager._collector_task.done()
    }
    
    # Get provider details
    for provider in sensor_manager.sensor_providers:
        provider_info = {
            "name": provider.display_name,
            "source_id": provider.source_id,
            "available": await provider.is_available()
        }
        
        # Try to get current data
        try:
            readings = await provider.get_current_data()
            provider_info["current_readings_count"] = len(readings)
            provider_info["sample_readings"] = [
                {
                    "sensor_id": reading.sensor_id,
                    "name": reading.name,
                    "value": reading.value,
                    "unit": reading.unit,
                    "category": reading.category
                } for reading in readings[:3]  # First 3 as examples
            ]
        except Exception as e:
            provider_info["error_getting_data"] = str(e)
        
        debug_info["providers"].append(provider_info)
    
    # Check what's in the cache
    debug_info["cached_readings"] = {}
    for source_id, readings in sensor_manager._sensor_readings.items():
        debug_info["cached_readings"][source_id] = {
            "count": len(readings),
            "sample": [
                {
                    "sensor_id": reading.sensor_id,
                    "name": reading.name,
                    "value": reading.value,
                    "unit": reading.unit
                } for reading in readings[:2]  # First 2 as examples
            ] if readings else []
        }
    
    return debug_info

@app.get("/health")
async def health_check():
    """Health check endpoint including real-time service status."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "realtime_service": {
                "running": realtime_service.is_running,
                "broadcasts_sent": realtime_service.broadcasts_sent,
                "connected_clients": len(websocket_manager.active_connections)
            },
            "websocket_manager": {
                "active_connections": len(websocket_manager.active_connections)
            },
            "sensor_manager": {
                "initialized": True  # Assuming it's initialized if we get here
            }
        }
    }

# Basic root endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = f"""
    <html>
        <head>
            <title>{get_settings().app_name}</title>
        </head>
        <body>
            <h1>Welcome to {get_settings().app_name}!</h1>
            <p>API documentation available at <a href=\"/docs\">/docs</a> or <a href=\"/redoc\">/redoc</a>.</p>
            <p>API base URL: {get_settings().api_v1_str}</p>
            <h2>Monitoring & Real-time</h2>
            <ul>
                <li>Health check: <a href=\"/health\">/health</a></li>
                <li>Real-time service stats: <a href=\"/realtime/stats\">/realtime/stats</a></li>
                <li>Force broadcast: <code>POST /realtime/broadcast</code></li>
                <li>WebSocket test page: <a href=\"/test-websocket\">/test-websocket</a></li>
                <li>WebSocket endpoint: <code>ws://localhost:{get_settings().server_port}/ws/{{client_id}}</code></li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/test-websocket", response_class=HTMLResponse)
async def websocket_test_page():
    """Simple WebSocket test page for development and debugging."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Test - {get_settings().app_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 800px; }}
            .message-area {{ background: #f5f5f5; padding: 10px; height: 300px; overflow-y: auto; border: 1px solid #ddd; }}
            .controls {{ margin: 10px 0; }}
            input, button {{ padding: 5px; margin: 5px; }}
            .status {{ font-weight: bold; }}
            .connected {{ color: green; }}
            .disconnected {{ color: red; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>WebSocket Test - {get_settings().app_name}</h1>
            <div class="controls">
                <input type="text" id="clientId" placeholder="Client ID" value="test-client">
                <button onclick="connect()">Connect</button>
                <button onclick="disconnect()">Disconnect</button>
                <span id="status" class="status disconnected">Disconnected</span>
            </div>
            <div class="controls">
                <input type="text" id="message" placeholder="Message to send" style="width: 200px;">
                <button onclick="sendMessage()">Send Message</button>
                <button onclick="sendCommand('get_stats')">Get Stats</button>
                <button onclick="sendCommand('force_broadcast')">Force Broadcast</button>
            </div>
            <div class="message-area" id="messages"></div>
        </div>
        
        <script>
            let ws = null;
            const messages = document.getElementById('messages');
            const status = document.getElementById('status');
            
            function connect() {{
                const clientId = document.getElementById('clientId').value || 'test-client';
                const wsUrl = `ws://localhost:{get_settings().server_port}/ws/${{clientId}}`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function() {{
                    status.textContent = 'Connected';
                    status.className = 'status connected';
                    addMessage('Connected to server', 'system');
                }};
                
                ws.onmessage = function(event) {{
                    addMessage('Received: ' + event.data, 'received');
                }};
                
                ws.onclose = function() {{
                    status.textContent = 'Disconnected';
                    status.className = 'status disconnected';
                    addMessage('Connection closed', 'system');
                }};
                
                ws.onerror = function(error) {{
                    addMessage('Error: ' + error, 'error');
                }};
            }}
            
            function disconnect() {{
                if (ws) {{
                    ws.close();
                    ws = null;
                }}
            }}
            
            function sendMessage() {{
                const message = document.getElementById('message').value;
                if (ws && message) {{
                    ws.send(message);
                    addMessage('Sent: ' + message, 'sent');
                    document.getElementById('message').value = '';
                }}
            }}
            
            function sendCommand(command) {{
                if (ws) {{
                    const cmd = JSON.stringify({{ command: command }});
                    ws.send(cmd);
                    addMessage('Sent command: ' + command, 'sent');
                }}
            }}
            
            function addMessage(message, type) {{
                const div = document.createElement('div');
                div.style.margin = '2px 0';
                div.style.padding = '2px';
                if (type === 'system') div.style.color = 'blue';
                if (type === 'error') div.style.color = 'red';
                if (type === 'sent') div.style.color = 'green';
                if (type === 'received') div.style.color = 'purple';
                
                const time = new Date().toLocaleTimeString();
                div.textContent = `[${{time}}] ${{message}}`;
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
            }}
            
            // Allow Enter key to send message
            document.getElementById('message').addEventListener('keypress', function(e) {{
                if (e.key === 'Enter') {{
                    sendMessage();
                }}
            }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# This is for running with `python app/main.py` for development
# Uvicorn is typically run from the command line as `uvicorn app.main:app --reload`
if __name__ == "__main__":
    settings = get_settings()
    logger.info(f"Starting Uvicorn server for {settings.app_name} on host {settings.server_host} port {settings.server_port}")
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug_mode, # Enable reload in debug mode
        log_level="info" if settings.debug_mode else "warning"
    )
