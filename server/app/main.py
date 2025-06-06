"""
Ultimate Sensor Monitor Reimagined - Enhanced FastAPI Backend
Main application with enhanced LibreHardwareMonitor integration
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import os
from typing import Dict, List, Any
import logging
from datetime import datetime

from .config import settings
from .websockets import WebSocketManager
from .sensors.mock_sensor import MockSensor
from .sensors.lhm_sensor import LHMSensor # Updated import
from .sensors.hwinfo_sensor import HWiNFOSensor
from .models import DashboardPreset, WidgetGroup, SensorData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Ultimate Sensor Monitor Reimagined",
    description="Real-time hardware monitoring with enhanced LibreHardwareMonitor integration",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5501", "http://localhost:4173"], # Adjust as needed for your Svelte dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers and sensors
websocket_manager = WebSocketManager()
mock_sensor = MockSensor()
lhm_sensor = LHMSensor() # Updated instantiation
hwinfo_sensor = HWiNFOSensor()

# Collect all available sensor sources
sensor_sources = [
    ("mock", "Mock Sensor Data", mock_sensor),
    ("lhm", "LibreHardwareMonitor Enhanced", lhm_sensor), # Updated source_id and instance variable
    ("hwinfo", "HWiNFO64", hwinfo_sensor)
]

# In-memory storage for presets and widget groups
presets_storage: Dict[str, Dict] = {}
widget_groups_storage: Dict[str, Dict] = {}

# Real-time configuration
realtime_config = {
    "polling_rate": 2000,
    "adaptive_polling": True,
    "burst_mode": False,
    "compression": True,
    "batch_size": 50,
    "max_sensors_per_update": 200
}

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Ultimate Sensor Monitor Reimagined API", 
        "version": "2.0.0",
        "features": [
            "Enhanced LibreHardwareMonitor integration", # This description can remain
            "Real-time sensor monitoring",
            "Adaptive polling rates",
            "Performance optimization",
            "WebSocket real-time updates"
        ]
    }

@app.get("/api/sensors/sources")
async def get_sensor_sources_endpoint(): # Renamed function to avoid conflict with list name
    """Get all available sensor sources with enhanced information."""
    sources_info = {} # Renamed variable
    
    for source_id, source_name, sensor_instance in sensor_sources:
        try:
            is_available = sensor_instance.is_available()
            
            if is_available:
                performance_metrics_data = {}
                if hasattr(sensor_instance, 'get_performance_metrics'):
                    # Ensure get_performance_metrics is not a coroutine or handle appropriately
                    perf_metrics_obj = sensor_instance.get_performance_metrics()
                    performance_metrics_data = {
                        "total_sensors": perf_metrics_obj.sensor_count,
                        "active_sensors": perf_metrics_obj.sensor_count, # Assuming same for now
                        "update_rate": perf_metrics_obj.update_rate,
                        "error_rate": perf_metrics_obj.error_rate,
                        "cpu_usage": perf_metrics_obj.cpu_usage,
                        "memory_usage": perf_metrics_obj.memory_usage,
                        "update_latency": perf_metrics_obj.update_latency
                    }
                
                capabilities = {
                    "supports_real_time": True, # Default, adjust if sensor_instance has specific flags
                    "supports_history": False,
                    "supports_alerts": isinstance(sensor_instance, LHMSensor), # Example: only LHM supports alerts
                    "supports_calibration": False,
                    "min_update_interval": 500 if isinstance(sensor_instance, LHMSensor) else 1000,
                    "max_update_interval": 10000,
                    "adaptive_polling": isinstance(sensor_instance, LHMSensor) and sensor_instance.config.get('adaptive_polling', False),
                    "hardware_acceleration": isinstance(sensor_instance, LHMSensor) and sensor_instance.config.get('enable_hardware_acceleration', False)
                }
                
                sensors_list = []
                if hasattr(sensor_instance, 'get_available_sensors'):
                    if asyncio.iscoroutinefunction(sensor_instance.get_available_sensors):
                        sensors_list = await sensor_instance.get_available_sensors()
                    else:
                        sensors_list = sensor_instance.get_available_sensors()
                
                sources_info[source_id] = {
                    "id": source_id,
                    "name": source_name, # This is the display name from the sensor_sources tuple
                    "active": True,
                    "sensors": sensors_list,
                    "capabilities": capabilities,
                    "statistics": performance_metrics_data,
                    "configuration": {
                        "update_interval": sensor_instance.config.get('update_interval', realtime_config["polling_rate"]) if hasattr(sensor_instance, 'config') else realtime_config["polling_rate"],
                        "adaptive_polling": sensor_instance.config.get('adaptive_polling', realtime_config["adaptive_polling"]) if hasattr(sensor_instance, 'config') else realtime_config["adaptive_polling"],
                        "compression": realtime_config["compression"] # Assuming global for now
                    },
                    "last_update": datetime.now().isoformat()
                }
            else:
                sources_info[source_id] = {
                    "id": source_id,
                    "name": source_name,
                    "active": False,
                    "sensors": [],
                    "error_message": "Sensor source not available",
                    "capabilities": {},
                    "statistics": {}
                }
                
        except Exception as e:
            logger.error(f"Failed to get information from {source_name}: {e}")
            sources_info[source_id] = {
                "id": source_id,
                "name": source_name,
                "active": False,
                "sensors": [],
                "error_message": f"Error: {str(e)}",
                "capabilities": {},
                "statistics": {}
            }
    
    return {"sources": sources_info}


@app.post("/api/sensors/sources/{source_id}/configure")
async def configure_sensor_source(source_id: str, config: Dict[str, Any]):
    """Configure a specific sensor source."""
    sensor_instance = next((inst for sid, _, inst in sensor_sources if sid == source_id), None)
    
    if not sensor_instance:
        raise HTTPException(status_code=404, detail="Sensor source not found")
    
    try:
        if hasattr(sensor_instance, 'update_configuration'):
            sensor_instance.update_configuration(config)
            
        # Update global realtime config if applicable to the specific sensor (e.g., our LHM sensor)
        if isinstance(sensor_instance, LHMSensor): # Check if it's our LHM sensor
            # Only update global config keys that are present in the sensor's config
            for key in config:
                if key in realtime_config:
                    realtime_config[key] = config[key]
            
        return {"message": f"Configuration updated for {source_id}", "config": sensor_instance.config if hasattr(sensor_instance, 'config') else config}
        
    except Exception as e:
        logger.error(f"Failed to configure {source_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sensors/sources/{source_id}/toggle")
async def toggle_sensor_source(source_id: str, toggle_data: Dict[str, bool]):
    """Enable or disable a sensor source."""
    enabled = toggle_data.get("enabled", False)
    sensor_instance = next((inst for sid, _, inst in sensor_sources if sid == source_id), None)
    
    if not sensor_instance:
        raise HTTPException(status_code=404, detail="Sensor source not found")
    
    try:
        message = f"Toggle not supported for {source_id}"
        current_status = False

        if hasattr(sensor_instance, 'start_real_time_monitoring') and hasattr(sensor_instance, 'stop_real_time_monitoring'):
            if enabled:
                if not sensor_instance.is_available():
                    # Ensure initialize is awaited if it's a coroutine
                    if asyncio.iscoroutinefunction(sensor_instance.initialize):
                        await sensor_instance.initialize()
                    else:
                        sensor_instance.initialize()
                
                # Ensure start_real_time_monitoring is not a coroutine or handle appropriately
                sensor_instance.start_real_time_monitoring()
                message = f"Enabled real-time monitoring for {source_id}"
                current_status = True
            else:
                # Ensure stop_real_time_monitoring is not a coroutine or handle appropriately
                sensor_instance.stop_real_time_monitoring()
                message = f"Disabled real-time monitoring for {source_id}"
                current_status = False
        
        return {"message": message, "enabled": current_status} # Return actual status
        
    except Exception as e:
        logger.error(f"Failed to toggle {source_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensors/current")
async def get_current_sensor_data():
    """Get current sensor data from all sources with enhanced information."""
    all_data = {}
    
    for source_id, source_name, sensor_instance in sensor_sources:
        try:
            is_available = sensor_instance.is_available()
            
            if is_available:
                data = {}
                if hasattr(sensor_instance, 'get_current_data'):
                    if asyncio.iscoroutinefunction(sensor_instance.get_current_data):
                        data = await sensor_instance.get_current_data()
                    else:
                        data = sensor_instance.get_current_data()
                
                performance_info = {}
                if hasattr(sensor_instance, 'get_performance_metrics'):
                    metrics = sensor_instance.get_performance_metrics()
                    performance_info = {
                        "update_latency": metrics.update_latency,
                        "sensor_count": metrics.sensor_count,
                        "update_rate": metrics.update_rate,
                        "error_rate": metrics.error_rate,
                        "cpu_usage": metrics.cpu_usage,
                        "memory_usage": metrics.memory_usage
                    }
                
                all_data[source_id] = {
                    "source_id": source_id, # Add source_id here
                    "name": source_name, # Display name
                    "active": True,
                    "sensors": data,
                    "performance": performance_info,
                    "last_update": datetime.now().isoformat()
                }
            else:
                all_data[source_id] = {
                    "source_id": source_id,
                    "name": source_name,
                    "active": False,
                    "sensors": {},
                    "error": "Source not available"
                }
                
        except Exception as e:
            logger.error(f"Failed to get data from {source_name}: {e}")
            all_data[source_id] = {
                "source_id": source_id,
                "name": source_name,
                "active": False,
                "error": str(e),
                "sensors": {}
            }
    
    return {
        "timestamp": datetime.now().isoformat(),
        "sources": all_data, # This is now a dict of sources
        "configuration": realtime_config # Global config
    }


@app.get("/api/sensors/hardware-tree")
async def get_hardware_tree():
    """Get hierarchical view of hardware components and sensors."""
    try:
        if lhm_sensor.is_available(): # Use the renamed instance
            hardware_tree_data = lhm_sensor.get_hardware_tree() # Use the renamed instance
            return {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "hardware": hardware_tree_data
            }
        else:
            return {
                "success": False,
                "error": "LHM Sensor is not available", # Updated message
                "hardware": []
            }
    except Exception as e:
        logger.error(f"Failed to get hardware tree: {e}")
        return {
            "success": False,
            "error": str(e),
            "hardware": []
        }

@app.post("/api/realtime/configure")
async def configure_realtime_settings(config: Dict[str, Any]):
    """Configure real-time monitoring settings."""
    try:
        realtime_config.update(config)
        
        if lhm_sensor.is_available(): # Use the renamed instance
            lhm_sensor.update_configuration(config) # Update specific sensor if needed
        
        logger.info(f"Updated real-time configuration: {config}")
        return {
            "message": "Real-time configuration updated",
            "configuration": realtime_config
        }
        
    except Exception as e:
        logger.error(f"Failed to update real-time configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/realtime/status")
async def get_realtime_status():
    """Get real-time monitoring status and performance metrics."""
    try:
        status = {
            "configuration": realtime_config,
            "sources": {}
        }
        
        for source_id, source_name, sensor_instance in sensor_sources:
            source_status = {
                "name": source_name,
                "available": sensor_instance.is_available(),
                "monitoring": False,
                "performance": {}
            }
            
            if hasattr(sensor_instance, 'is_running'):
                source_status["monitoring"] = getattr(sensor_instance, 'is_running', False)
            
            if hasattr(sensor_instance, 'get_performance_metrics'):
                metrics = sensor_instance.get_performance_metrics()
                source_status["performance"] = {
                    "update_latency": metrics.update_latency,
                    "sensor_count": metrics.sensor_count,
                    "update_rate": metrics.update_rate,
                    "error_rate": metrics.error_rate,
                    "cpu_usage": metrics.cpu_usage,
                    "memory_usage": metrics.memory_usage
                }
            
            status["sources"][source_id] = source_status
        
        return status
        
    except Exception as e:
        logger.error(f"Failed to get real-time status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time sensor data."""
    await websocket_manager.connect(websocket)
    
    active_sensor_callbacks = {}

    def create_data_callback(source_id_cb: str):
        def data_callback(readings, performance_metrics):
            try:
                sensor_data_payload = {}
                for reading_id, reading in readings.items():
                    sensor_data_payload[reading_id] = {
                        "id": reading.id, "name": reading.name, "value": reading.value,
                        "unit": reading.unit, "category": reading.category,
                        "hardware_type": reading.hardware_type, "parent": reading.hardware_name,
                        "timestamp": reading.timestamp, "quality": reading.quality
                    }
                
                message = {
                    "type": "sensor_data", "timestamp": datetime.now().isoformat(),
                    "source_id": source_id_cb, # Use the captured source_id
                    "data": { # Keep consistent with HTTP GET /api/sensors/current structure
                         "sources": { 
                            source_id_cb: {
                                "active": True,
                                "sensors": sensor_data_payload
                            }
                         }
                    },
                    "performance": {
                        "update_latency": performance_metrics.update_latency,
                        "sensor_count": performance_metrics.sensor_count,
                        "update_rate": performance_metrics.update_rate,
                        "cpu_usage": performance_metrics.cpu_usage,
                        "memory_usage": performance_metrics.memory_usage
                    }
                }
                asyncio.create_task(websocket_manager.broadcast(json.dumps(message)))
            except Exception as e_cb:
                logger.error(f"Error in data callback for {source_id_cb}: {e_cb}")
        return data_callback

    # Register callbacks for sensors that support them (like LHMSensor)
    for sid, _, sensor_inst in sensor_sources:
        if hasattr(sensor_inst, 'add_data_callback') and sensor_inst.is_available():
            cb = create_data_callback(sid)
            sensor_inst.add_data_callback(cb)
            active_sensor_callbacks[sid] = (sensor_inst, cb) # Store instance and callback
    
    try:
        while True:
            try:
                message_text = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                try:
                    parsed_message = json.loads(message_text)
                    await handle_websocket_message(parsed_message, websocket)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received: {message_text}")
            except asyncio.TimeoutError:
                continue # No message received, continue loop
            except WebSocketDisconnect:
                break # Client disconnected
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {websocket.client}")
    finally:
        # Clean up callbacks
        for sid, (sensor_inst, cb) in active_sensor_callbacks.items():
            if hasattr(sensor_inst, 'remove_data_callback'):
                sensor_inst.remove_data_callback(cb)
        websocket_manager.disconnect(websocket)
        logger.info(f"Cleaned up WebSocket connection: {websocket.client}")


async def handle_websocket_message(message: Dict[str, Any], websocket: WebSocket):
    """Handle incoming WebSocket messages from clients."""
    message_type = message.get("type")
    
    if message_type == "configure_realtime":
        try:
            config = message.get("config", {})
            # Apply to global config
            realtime_config.update(config) 
            
            # Apply to specific sensors if they support it and are targeted
            target_source_id = message.get("source_id")
            if target_source_id:
                sensor_instance = next((inst for sid, _, inst in sensor_sources if sid == target_source_id), None)
                if sensor_instance and hasattr(sensor_instance, 'update_configuration'):
                    sensor_instance.update_configuration(config)
            elif isinstance(lhm_sensor, LHMSensor) and lhm_sensor.is_available(): # Default to LHM if no source_id
                 lhm_sensor.update_configuration(config)

            response = {
                "type": "configuration_updated", "timestamp": datetime.now().isoformat(),
                "configuration": realtime_config # Send back the global config
            }
            await websocket.send_text(json.dumps(response))
        except Exception as e:
            error_response = {"type": "error", "timestamp": datetime.now().isoformat(), "error": str(e)}
            await websocket.send_text(json.dumps(error_response))
    
    elif message_type == "heartbeat":
        response = {"type": "heartbeat_response", "timestamp": datetime.now().isoformat()}
        await websocket.send_text(json.dumps(response))

async def broadcast_sensor_data_task(): # Renamed function
    """Background task to broadcast sensor data for non-callback sources."""
    while True:
        try:
            if not websocket_manager.active_connections:
                await asyncio.sleep(realtime_config.get("polling_rate", 2000) / 1000.0) # Use configured rate
                continue
            
            data_to_broadcast = {}
            for source_id, source_name, sensor_instance in sensor_sources:
                # Skip sensors that use their own callback mechanism (like LHMSensor)
                if hasattr(sensor_instance, 'add_data_callback'): 
                    continue
                    
                if sensor_instance.is_available():
                    try:
                        current_data = {}
                        if hasattr(sensor_instance, 'get_current_data'):
                            if asyncio.iscoroutinefunction(sensor_instance.get_current_data):
                                current_data = await sensor_instance.get_current_data()
                            else:
                                current_data = sensor_instance.get_current_data()
                        
                        data_to_broadcast[source_id] = {
                            "source_id": source_id, "name": source_name, "active": True,
                            "sensors": current_data, "last_update": datetime.now().isoformat()
                        }
                    except Exception as e_loop:
                        logger.error(f"Failed to get data from {source_name} in broadcast loop: {e_loop}")
                        data_to_broadcast[source_id] = {
                            "source_id": source_id, "name": source_name, "active": False,
                            "error": str(e_loop), "sensors": {}
                        }
            
            if data_to_broadcast:
                message = {
                    "type": "sensor_data", "timestamp": datetime.now().isoformat(),
                    "sources": data_to_broadcast # This is a dict of sources
                }
                await websocket_manager.broadcast(json.dumps(message))
            
            await asyncio.sleep(realtime_config.get("polling_rate", 2000) / 1000.0)
            
        except Exception as e_main_loop:
            logger.error(f"Error in sensor data broadcast task: {e_main_loop}")
            await asyncio.sleep(5) # Longer sleep on major error

@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    logger.info("Starting Ultimate Sensor Monitor Reimagined v2.0...")
    
    # Initialize LHM sensor
    try:
        logger.info("Initializing LHM Sensor...")
        if asyncio.iscoroutinefunction(lhm_sensor.initialize): # Check if initialize is async
            if await lhm_sensor.initialize():
                logger.info("✓ LHM Sensor initialized successfully")
                if lhm_sensor.start_real_time_monitoring(): # This is not async
                    logger.info("✓ LHM real-time monitoring started")
                else:
                    logger.warning("⚠ Failed to start LHM real-time monitoring")
            else:
                logger.warning("⚠ LHM Sensor initialization failed")
        else: # If initialize is not async (should be consistent)
            if lhm_sensor.initialize():
                logger.info("✓ LHM Sensor initialized successfully")
                if lhm_sensor.start_real_time_monitoring():
                    logger.info("✓ LHM real-time monitoring started")
                else:
                    logger.warning("⚠ Failed to start LHM real-time monitoring")
            else:
                logger.warning("⚠ LHM Sensor initialization failed")


    except Exception as e:
        logger.error(f"✗ LHM Sensor initialization error: {e}")
    
    # Initialize other sensors if they have an async initialize method
    for sid, sname, sensor_inst in sensor_sources:
        if sensor_inst is lhm_sensor: # Already handled
            continue
        if hasattr(sensor_inst, 'initialize') and asyncio.iscoroutinefunction(sensor_inst.initialize):
            try:
                logger.info(f"Initializing {sname}...")
                if await sensor_inst.initialize():
                    logger.info(f"✓ {sname} initialized successfully.")
                    if hasattr(sensor_inst, 'start_real_time_monitoring') and sensor_inst.start_real_time_monitoring():
                         logger.info(f"✓ {sname} real-time monitoring started.")
                else:
                    logger.warning(f"⚠ {sname} initialization failed.")
            except Exception as e_other_sensor:
                 logger.error(f"✗ {sname} initialization error: {e_other_sensor}")


    # Load existing presets from files
    try:
        for filename in os.listdir("data"):
            if filename.startswith("preset_") and filename.endswith(".json"):
                preset_id = filename.replace("preset_", "").replace(".json", "")
                with open(f"data/{filename}", "r") as f:
                    presets_storage[preset_id] = json.load(f)
            elif filename.startswith("widget_group_") and filename.endswith(".json"):
                group_id = filename.replace("widget_group_", "").replace(".json", "")
                with open(f"data/{filename}", "r") as f:
                    widget_groups_storage[group_id] = json.load(f)
    except FileNotFoundError:
        logger.info("Data directory not found or empty, no presets/widget groups loaded.")
    except Exception as e_load:
        logger.error(f"Error loading presets/widget groups: {e_load}")

    asyncio.create_task(broadcast_sensor_data_task()) # Use renamed task
    
    logger.info("✓ Application startup complete!")
    logger.info("=" * 60)
    logger.info("🚀 Ultimate Sensor Monitor Reimagined v2.0 is running!")
    logger.info(f"📡 Server: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"🔌 WebSocket: ws://{settings.HOST}:{settings.PORT}/ws")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    logger.info("Shutting down Ultimate Sensor Monitor Reimagined...")
    
    for _, _, sensor_instance in sensor_sources:
        if hasattr(sensor_instance, 'close'):
            try:
                sensor_instance.close() # Assuming close is not async
                logger.info(f"✓ Closed sensor: {sensor_instance.source_name if hasattr(sensor_instance, 'source_name') else type(sensor_instance).__name__}")
            except Exception as e_close:
                logger.error(f"Error closing sensor {type(sensor_instance).__name__}: {e_close}")
    
    logger.info("✓ Shutdown complete")

# --- Presets and Widget Groups API Endpoints ---
@app.get("/api/presets", response_model=List[DashboardPreset])
async def get_presets_list(): # Renamed for clarity
    """Get all saved dashboard presets."""
    # This should return a list of DashboardPreset objects, not just keys
    return list(presets_storage.values())

@app.post("/api/presets", response_model=DashboardPreset)
async def save_preset(preset: DashboardPreset):
    """Save a dashboard preset."""
    # If ID is not provided, generate one (though frontend should ideally provide it)
    if not preset.id:
        preset.id = f"preset_{int(datetime.now().timestamp())}"
    
    preset.updated_at = datetime.now().isoformat()
    if not preset.created_at: # Set created_at only if not already set
        preset.created_at = datetime.now().isoformat()

    presets_storage[preset.id] = preset.dict() # Store as dict
    
    try:
        with open(f"data/preset_{preset.id}.json", "w") as f:
            json.dump(preset.dict(), f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save preset to file: {e}")
        # Optionally, re-raise or handle this error if saving to disk is critical
    
    return preset # Return the Pydantic model instance

@app.get("/api/presets/{preset_id}", response_model=DashboardPreset)
async def get_preset_by_id(preset_id: str): # Renamed for clarity
    """Get a specific preset by ID."""
    if preset_id not in presets_storage:
        try:
            with open(f"data/preset_{preset_id}.json", "r") as f:
                preset_data_dict = json.load(f)
                # Validate and parse into Pydantic model
                presets_storage[preset_id] = DashboardPreset(**preset_data_dict).dict()
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Preset not found")
        except Exception as e_load_preset: # Catch Pydantic validation errors too
            logger.error(f"Error loading or parsing preset {preset_id}: {e_load_preset}")
            raise HTTPException(status_code=500, detail=f"Error loading preset: {preset_id}")

    # Ensure we return a Pydantic model instance
    return DashboardPreset(**presets_storage[preset_id])


@app.delete("/api/presets/{preset_id}", status_code=204)
async def delete_preset_by_id(preset_id: str): # Renamed for clarity
    """Delete a preset."""
    if preset_id in presets_storage:
        del presets_storage[preset_id]
    
    try:
        os.remove(f"data/preset_{preset_id}.json")
    except FileNotFoundError:
        # If it's not in memory and not on disk, it's effectively gone.
        # If it was in memory but not on disk, that's fine too.
        # If it was not in memory but on disk, we still try to remove.
        # Only raise 404 if it was never found anywhere.
        if preset_id not in presets_storage: # Check again if it was loaded
             pass # No error if file not found and not in memory
    except Exception as e_delete:
        logger.error(f"Error deleting preset file for {preset_id}: {e_delete}")
        # Decide if this should be a 500 error or just a warning
    
    return {"message": "Preset deleted successfully"} # Or just return 204 No Content

# Placeholder for WidgetGroup endpoints - assuming similar structure if needed
# @app.get("/api/widget-groups", response_model=List[WidgetGroup])
# async def get_widget_groups(): ...
# @app.post("/api/widget-groups", response_model=WidgetGroup)
# async def save_widget_group(group: WidgetGroup): ...
# etc.


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Ultimate Sensor Monitor Enhanced Backend...")
    print(f"📡 Server will be available at: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔌 WebSocket endpoint: ws://{settings.HOST}:{settings.PORT}/ws")
    print("⚡ LHM Sensor integration enabled") # Updated message
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app", # Ensure this matches your module structure
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD, # Use setting
        log_level=settings.LOG_LEVEL.lower() # Use setting
    )
