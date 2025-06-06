"""
LHM Sensor - LibreHardwareMonitor integration with real-time capabilities
Combines both DLL and HardwareMonitor package approaches for maximum compatibility
"""

import asyncio
import time
import json
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
from threading import Thread, Event
import queue
from .base import BaseSensor
from ..models import SensorData # Assuming SensorData is still relevant from models

logger = logging.getLogger(__name__)

@dataclass
class SensorReading:
    id: str
    name: str
    value: float
    unit: str
    category: str
    hardware_type: str
    hardware_name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    timestamp: str = None
    quality: str = "good"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}

@dataclass
class PerformanceMetrics:
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    update_latency: float = 0.0
    sensor_count: int = 0
    update_rate: float = 0.0
    error_rate: float = 0.0

class LHMSensor(BaseSensor): # Renamed from EnhancedLibreHardwareSensor
    """LHM Sensor - LibreHardwareMonitor sensor with real-time capabilities"""
    
    def __init__(self):
        super().__init__("LibreHardwareMonitor Enhanced") # Display name remains the same
        
        # Configuration
        self.config = {
            'update_interval': 2000,  # milliseconds
            'adaptive_polling': True,
            'enable_hardware_acceleration': True,
            'buffer_size': 1000,
            'compression_enabled': True,
            'filter_inactive_sensors': True,
            'timeout_duration': 5000,
            'retry_attempts': 3,
            'enable_detailed_logging': False
        }
        
        # State management
        self.is_running = False
        self.is_initialized = False
        self.last_update = None
        self.update_thread = None
        self.stop_event = Event()
        
        # Data storage
        self.current_readings: Dict[str, SensorReading] = {}
        self.reading_history: List[Dict[str, SensorReading]] = []
        self.performance_metrics = PerformanceMetrics()
        
        # Callbacks
        self.data_callbacks: List[Callable] = []
        self.error_callbacks: List[Callable] = []
        
        # Hardware monitor instances
        self.hw_monitor = None
        self.dll_monitor = None
        self.active_backend = None
        
        # Performance tracking
        self.update_times = []
        self.error_count = 0
        self.total_updates = 0

    async def initialize(self) -> bool:
        """Initialize the LHM sensor system"""
        if self.is_initialized:
            return True
            
        logger.info("[LHM] Initializing LHM sensor...") # Updated log prefix
        
        try:
            # Try HardwareMonitor package first (preferred)
            if await self._initialize_hardware_monitor():
                self.active_backend = "hardware_monitor"
                logger.info("[LHM] Using HardwareMonitor package backend") # Updated log prefix
            # Fallback to DLL approach
            elif await self._initialize_dll_monitor():
                self.active_backend = "dll_monitor"
                logger.info("[LHM] Using DLL backend") # Updated log prefix
            else:
                logger.error("[LHM] Failed to initialize any backend") # Updated log prefix
                return False
            
            self.is_initialized = True
            logger.info("[LHM] LHM sensor system initialized successfully") # Updated log prefix
            return True
            
        except Exception as e:
            logger.error(f"[LHM] Initialization failed: {e}") # Updated log prefix
            return False

    async def _initialize_hardware_monitor(self) -> bool:
        """Initialize using HardwareMonitor package"""
        try:
            from HardwareMonitor.Hardware import Computer
            from HardwareMonitor.Util import OpenComputer
            
            self.hw_monitor = OpenComputer(
                motherboard=True,
                cpu=True,
                gpu=True,
                memory=True,
                storage=True,
                network=True,
                controller=True,
                battery=True
            )
            
            self.hw_monitor.Update()
            logger.info("[LHM] HardwareMonitor package initialized successfully") # Updated log prefix
            return True
            
        except ImportError:
            logger.warning("[LHM] HardwareMonitor package not available") # Updated log prefix
            return False
        except Exception as e:
            logger.error(f"[LHM] HardwareMonitor initialization failed: {e}") # Updated log prefix
            return False

    async def _initialize_dll_monitor(self) -> bool:
        """Initialize using direct DLL access"""
        try:
            import clr
            import os
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.join(current_dir, "..", "..", "..") # Assuming structure server/app/sensors
            dll_path = os.path.join(project_root, "LibreHardwareMonitorLib.dll")
            dll_path = os.path.abspath(dll_path)
            
            if not os.path.exists(dll_path):
                logger.error(f"[LHM] DLL not found at: {dll_path}") # Updated log prefix
                return False
            
            clr.AddReference(dll_path)
            from LibreHardwareMonitor.Hardware import Computer
            
            self.dll_monitor = Computer()
            self.dll_monitor.IsCpuEnabled = True
            self.dll_monitor.IsGpuEnabled = True
            self.dll_monitor.IsMemoryEnabled = True
            self.dll_monitor.IsMotherboardEnabled = True
            self.dll_monitor.IsControllerEnabled = True
            self.dll_monitor.IsNetworkEnabled = True
            self.dll_monitor.IsStorageEnabled = True
            
            self.dll_monitor.Open()
            logger.info("[LHM] DLL backend initialized successfully") # Updated log prefix
            return True
            
        except ImportError:
            logger.warning("[LHM] pythonnet not available for DLL backend") # Updated log prefix
            return False
        except Exception as e:
            logger.error(f"[LHM] DLL initialization failed: {e}") # Updated log prefix
            return False

    def start_real_time_monitoring(self) -> bool:
        """Start real-time sensor monitoring"""
        if not self.is_initialized:
            logger.error("[LHM] Cannot start monitoring - not initialized") # Updated log prefix
            return False
            
        if self.is_running:
            logger.warning("[LHM] Monitoring already running") # Updated log prefix
            return True
            
        self.is_running = True
        self.stop_event.clear()
        
        self.update_thread = Thread(target=self._monitoring_loop, daemon=True)
        self.update_thread.start()
        
        logger.info(f"[LHM] Started real-time monitoring (interval: {self.config['update_interval']}ms)") # Updated log prefix
        return True

    def stop_real_time_monitoring(self):
        """Stop real-time sensor monitoring"""
        if not self.is_running:
            return
            
        self.is_running = False
        self.stop_event.set()
        
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=5.0)
            
        logger.info("[LHM] Stopped real-time monitoring") # Updated log prefix

    def _monitoring_loop(self):
        """Main monitoring loop running in separate thread"""
        logger.info("[LHM] Monitoring loop started") # Updated log prefix
        
        while not self.stop_event.is_set():
            try:
                start_time = time.time()
                
                self._update_sensor_data()
                
                update_time = (time.time() - start_time) * 1000
                self._update_performance_metrics(update_time)
                
                self._notify_data_callbacks()
                
                if self.config['adaptive_polling']:
                    self._adjust_polling_rate(update_time)
                
                sleep_time = self.config['update_interval'] / 1000.0
                if not self.stop_event.wait(sleep_time):
                    continue
                else:
                    break
                    
            except Exception as e:
                logger.error(f"[LHM] Error in monitoring loop: {e}") # Updated log prefix
                self.error_count += 1
                self._notify_error_callbacks(e)
                
                if not self.stop_event.wait(1.0):
                    continue
                else:
                    break
        
        logger.info("[LHM] Monitoring loop stopped") # Updated log prefix

    def _update_sensor_data(self):
        """Update sensor data from active backend"""
        if self.active_backend == "hardware_monitor":
            self._update_from_hardware_monitor()
        elif self.active_backend == "dll_monitor":
            self._update_from_dll_monitor()

    def _update_from_hardware_monitor(self):
        """Update sensor data using HardwareMonitor package"""
        if not self.hw_monitor:
            return
            
        try:
            self.hw_monitor.Update()
            new_readings = {}
            for hardware in self.hw_monitor.Hardware:
                self._process_hardware_component(hardware, new_readings, "")
                for subhardware in hardware.SubHardware:
                    parent_path = str(hardware.Name)
                    self._process_hardware_component(subhardware, new_readings, parent_path)
            self.current_readings = new_readings
            self.last_update = datetime.now()
            self.total_updates += 1
        except Exception as e:
            logger.error(f"[LHM] Error updating from HardwareMonitor: {e}") # Updated log prefix
            raise

    def _update_from_dll_monitor(self):
        """Update sensor data using DLL backend"""
        if not self.dll_monitor:
            return
            
        try:
            new_readings = {}
            for hardware in self.dll_monitor.Hardware:
                hardware.Update()
                self._process_hardware_component(hardware, new_readings, "")
                for subhardware in hardware.SubHardware:
                    subhardware.Update()
                    parent_path = str(hardware.Name)
                    self._process_hardware_component(subhardware, new_readings, parent_path)
            self.current_readings = new_readings
            self.last_update = datetime.now()
            self.total_updates += 1
        except Exception as e:
            logger.error(f"[LHM] Error updating from DLL: {e}") # Updated log prefix
            raise

    def _process_hardware_component(self, hardware, readings: Dict[str, SensorReading], parent_path: str):
        """Process sensors from a hardware component"""
        try:
            hardware_name = str(hardware.Name)
            hardware_type = self._get_hardware_type(hardware)
            current_path = f"{parent_path}/{hardware_name}" if parent_path else hardware_name
            
            for sensor in hardware.Sensors:
                try:
                    if sensor.Value is None:
                        continue
                        
                    sensor_id = self._generate_sensor_id(hardware, sensor)
                    sensor_name = str(sensor.Name)
                    sensor_value = float(sensor.Value)
                    category, unit = self._map_sensor_type(sensor.SensorType)
                    
                    reading = SensorReading(
                        id=sensor_id,
                        name=sensor_name,
                        value=sensor_value,
                        unit=unit,
                        category=category,
                        hardware_type=hardware_type,
                        hardware_name=current_path,
                        min_value=float(sensor.Min) if sensor.Min is not None else None,
                        max_value=float(sensor.Max) if sensor.Max is not None else None,
                        quality=self._assess_data_quality(sensor),
                        metadata={
                            'sensor_type': str(sensor.SensorType),
                            'identifier': str(sensor.Identifier),
                            'hardware_identifier': str(hardware.Identifier)
                        }
                    )
                    readings[sensor_id] = reading
                except Exception as e:
                    logger.debug(f"[LHM] Failed to process sensor {sensor.Name}: {e}") # Updated log prefix
        except Exception as e:
            logger.error(f"[LHM] Error processing hardware component: {e}") # Updated log prefix

    def _get_hardware_type(self, hardware) -> str:
        """Determine hardware type from hardware object"""
        try:
            hw_type = str(hardware.HardwareType).lower()
            type_mapping = {
                'cpu': 'cpu', 'gpu': 'gpu', 'memory': 'memory', 'motherboard': 'motherboard',
                'storage': 'storage', 'network': 'network', 'controller': 'controller', 'battery': 'battery'
            }
            for key, value in type_mapping.items():
                if key in hw_type:
                    return value
            return 'unknown'
        except Exception:
            return 'unknown'

    def _map_sensor_type(self, sensor_type) -> tuple[str, str]:
        """Map sensor type to category and unit"""
        try:
            if self.active_backend == "hardware_monitor":
                from HardwareMonitor.Hardware import SensorType
            else:
                from LibreHardwareMonitor.Hardware import SensorType
            
            type_mapping = {
                SensorType.Voltage: ("voltage", "V"), SensorType.Clock: ("clock", "MHz"),
                SensorType.Temperature: ("temperature", "°C"), SensorType.Load: ("load", "%"),
                SensorType.Fan: ("fan", "RPM"), SensorType.Flow: ("flow", "L/h"),
                SensorType.Control: ("control", "%"), SensorType.Level: ("level", "%"),
                SensorType.Factor: ("factor", ""), SensorType.Power: ("power", "W"),
                SensorType.Data: ("data", "GB"), SensorType.SmallData: ("data", "MB"),
                SensorType.Throughput: ("throughput", "B/s"), SensorType.TimeSpan: ("time", "s"),
                SensorType.Energy: ("energy", "mWh"), SensorType.Noise: ("noise", "dBA"),
            }
            return type_mapping.get(sensor_type, ("unknown", ""))
        except Exception:
            return ("unknown", "")

    def _generate_sensor_id(self, hardware, sensor) -> str:
        """Generate unique sensor ID"""
        try:
            import re
            hardware_id_str = str(hardware.Identifier).replace("/", "_").replace(" ", "_")
            sensor_id_str = str(sensor.Identifier).replace("/", "_").replace(" ", "_")
            hardware_id = re.sub(r'[^\w_]', '', hardware_id_str.lower())
            sensor_id = re.sub(r'[^\w_]', '', sensor_id_str.lower())
            return f"{hardware_id}_{sensor_id}"
        except Exception:
            return f"{hardware.Name}_{sensor.Name}".replace(" ", "_").lower()

    def _assess_data_quality(self, sensor) -> str:
        """Assess the quality of sensor data"""
        try:
            if sensor.Value is None: return "poor"
            value = float(sensor.Value)
            if hasattr(sensor, 'SensorType'):
                sensor_type_str = str(sensor.SensorType).lower()
                if 'temperature' in sensor_type_str:
                    if -50 <= value <= 150: return "excellent"
                    elif -100 <= value <= 200: return "good"
                    else: return "poor"
                elif 'load' in sensor_type_str or 'level' in sensor_type_str:
                    if 0 <= value <= 100: return "excellent"
                    else: return "fair"
                elif 'voltage' in sensor_type_str:
                    if 0 <= value <= 50: return "excellent"
                    else: return "fair"
            return "good"
        except Exception:
            return "unknown"

    def _update_performance_metrics(self, update_time: float):
        """Update performance metrics"""
        self.update_times.append(update_time)
        if len(self.update_times) > 100: self.update_times.pop(0)
        
        self.performance_metrics.update_latency = update_time
        self.performance_metrics.sensor_count = len(self.current_readings)
        
        if self.total_updates > 0 and self.update_times:
            avg_update_time = sum(self.update_times) / len(self.update_times)
            if avg_update_time > 0:
                 self.performance_metrics.update_rate = 1000.0 / avg_update_time
            else:
                 self.performance_metrics.update_rate = 0.0 # Avoid division by zero
            self.performance_metrics.error_rate = (self.error_count / self.total_updates) * 100
        
        self.performance_metrics.cpu_usage = min(update_time / 10.0, 100.0)
        self.performance_metrics.memory_usage = len(self.current_readings) * 0.1

    def _adjust_polling_rate(self, update_time: float):
        """Adjust polling rate based on system performance"""
        if not self.config['adaptive_polling']: return
            
        if update_time > self.config['update_interval'] * 0.8:
            new_interval = min(self.config['update_interval'] * 1.2, 10000)
            self.config['update_interval'] = int(new_interval)
            logger.debug(f"[LHM] Increased polling interval to {self.config['update_interval']}ms") # Updated log prefix
        elif update_time < self.config['update_interval'] * 0.2:
            new_interval = max(self.config['update_interval'] * 0.9, 500)
            self.config['update_interval'] = int(new_interval)
            logger.debug(f"[LHM] Decreased polling interval to {self.config['update_interval']}ms") # Updated log prefix

    def _notify_data_callbacks(self):
        """Notify all registered data callbacks"""
        for callback in self.data_callbacks:
            try:
                callback(self.current_readings, self.performance_metrics)
            except Exception as e:
                logger.error(f"[LHM] Error in data callback: {e}") # Updated log prefix

    def _notify_error_callbacks(self, error: Exception):
        """Notify all registered error callbacks"""
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception as e:
                logger.error(f"[LHM] Error in error callback: {e}") # Updated log prefix

    def add_data_callback(self, callback: Callable):
        self.data_callbacks.append(callback)

    def remove_data_callback(self, callback: Callable):
        if callback in self.data_callbacks: self.data_callbacks.remove(callback)

    def add_error_callback(self, callback: Callable):
        self.error_callbacks.append(callback)

    def remove_error_callback(self, callback: Callable):
        if callback in self.error_callbacks: self.error_callbacks.remove(callback)

    def update_configuration(self, new_config: Dict[str, Any]):
        old_interval = self.config['update_interval']
        self.config.update(new_config)
        if (self.is_running and old_interval != self.config['update_interval']):
            logger.info(f"[LHM] Restarting monitoring with new interval: {self.config['update_interval']}ms") # Updated log prefix
            self.stop_real_time_monitoring()
            time.sleep(0.1)
            self.start_real_time_monitoring()

    def get_current_readings(self) -> Dict[str, SensorReading]:
        return self.current_readings.copy()

    def get_performance_metrics(self) -> PerformanceMetrics:
        return self.performance_metrics

    def get_hardware_tree(self) -> List[Dict[str, Any]]:
        if not self.is_initialized: return []
        hardware_tree = []
        try:
            monitor = self.hw_monitor if self.active_backend == "hardware_monitor" else self.dll_monitor
            if not monitor: return []
            for hardware in monitor.Hardware:
                hardware_info = {
                    "name": str(hardware.Name), "type": self._get_hardware_type(hardware),
                    "identifier": str(hardware.Identifier), "sensors": [], "sub_hardware": []
                }
                for sensor in hardware.Sensors:
                    if sensor.Value is not None:
                        category, unit = self._map_sensor_type(sensor.SensorType)
                        hardware_info["sensors"].append({
                            "id": self._generate_sensor_id(hardware, sensor), "name": str(sensor.Name),
                            "value": float(sensor.Value), "unit": unit, "category": category,
                            "min": float(sensor.Min) if sensor.Min is not None else None,
                            "max": float(sensor.Max) if sensor.Max is not None else None
                        })
                for subhardware in hardware.SubHardware:
                    subhw_info = {
                        "name": str(subhardware.Name), "type": self._get_hardware_type(subhardware),
                        "identifier": str(subhardware.Identifier), "sensors": []
                    }
                    for sensor in subhardware.Sensors:
                        if sensor.Value is not None:
                            category, unit = self._map_sensor_type(sensor.SensorType)
                            subhw_info["sensors"].append({
                                "id": self._generate_sensor_id(subhardware, sensor), "name": str(sensor.Name),
                                "value": float(sensor.Value), "unit": unit, "category": category,
                                "min": float(sensor.Min) if sensor.Min is not None else None,
                                "max": float(sensor.Max) if sensor.Max is not None else None
                            })
                    hardware_info["sub_hardware"].append(subhw_info)
                hardware_tree.append(hardware_info)
        except Exception as e:
            logger.error(f"[LHM] Error getting hardware tree: {e}") # Updated log prefix
        return hardware_tree

    def is_available(self) -> bool:
        return self.is_initialized

    async def get_available_sensors(self) -> List[Dict[str, Any]]:
        if not self.is_initialized: await self.initialize()
        if not self.is_initialized: return []
        self._update_sensor_data()
        return [
            {"id": r.id, "name": r.name, "category": r.category, "unit": r.unit,
             "hardware_type": r.hardware_type, "hardware_name": r.hardware_name}
            for r in self.current_readings.values()
        ]

    async def get_current_data(self) -> Dict[str, Any]:
        if not self.is_initialized: await self.initialize()
        if not self.is_initialized: return {}
        self._update_sensor_data()
        return {
            r.id: {
                "id": r.id, "name": r.name, "value": r.value, "unit": r.unit,
                "category": r.category, "hardware_type": r.hardware_type,
                "min_value": r.min_value, "max_value": r.max_value,
                "parent": r.hardware_name, "timestamp": r.timestamp,
                "quality": r.quality, "metadata": r.metadata
            }
            for r in self.current_readings.values()
        }

    async def get_sensor_by_id(self, sensor_id: str) -> Optional[Dict[str, Any]]:
        current_data = await self.get_current_data()
        return current_data.get(sensor_id)

    async def get_sensors_by_category(self, category: str) -> List[Dict[str, Any]]:
        current_data = await self.get_current_data()
        return [sd for sd in current_data.values() if sd.get("category") == category]

    async def refresh(self) -> bool:
        try:
            if not self.is_initialized: await self.initialize()
            if self.is_initialized:
                self._update_sensor_data()
                return True
            return False
        except Exception as e:
            logger.error(f"[LHM] Error refreshing sensor data: {e}") # Updated log prefix
            return False

    def close(self):
        logger.info("[LHM] Closing LHM sensor system...") # Updated log prefix
        self.stop_real_time_monitoring()
        try:
            if self.hw_monitor: self.hw_monitor.Close(); self.hw_monitor = None
        except Exception as e: logger.error(f"[LHM] Error closing HardwareMonitor: {e}") # Updated log prefix
        try:
            if self.dll_monitor: self.dll_monitor.Close(); self.dll_monitor = None
        except Exception as e: logger.error(f"[LHM] Error closing DLL monitor: {e}") # Updated log prefix
        self.data_callbacks.clear()
        self.error_callbacks.clear()
        self.is_initialized = False
        logger.info("[LHM] LHM sensor system closed") # Updated log prefix

    def __del__(self):
        self.close()
