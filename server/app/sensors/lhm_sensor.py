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
    source_name = "lhm"
    
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
        """Initialize the LHM sensor system with robust error handling"""
        if self.is_initialized:
            return True
            
        logger.info("[LHM] Initializing LHM sensor...")
        
        try:
            # Try HardwareMonitor package first
            if await self._initialize_hardware_monitor():
                self.active_backend = "hardware_monitor"
                logger.info("[LHM] Using HardwareMonitor package backend")
            # Fallback to DLL approach
            elif await self._initialize_dll_monitor():
                self.active_backend = "dll_monitor"
                logger.info("[LHM] Using DLL backend")
            else:
                logger.error("[LHM] Failed to initialize any backend")
                return False
            
            self.is_initialized = True
            logger.info("[LHM] LHM sensor system initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"[LHM] Initialization failed: {e}")
            return False

    async def _initialize_hardware_monitor(self) -> bool:
        """Initialize using HardwareMonitor package with improved error handling"""
        try:
            # Try to initialize Python.NET runtime first
            try:
                import pythonnet  # type: ignore
                pythonnet.load("coreclr")  # type: ignore
            except Exception as e:
                logger.debug(f"[LHM] Python.NET runtime already initialized or failed: {e}")
            
            # Try to load System.Management for HardwareMonitor package
            try:
                import clr  # type: ignore
                # Try different ways to load System.Management
                try:
                    clr.AddReference("System.Management")  # type: ignore
                    logger.info("[LHM] System.Management loaded for HardwareMonitor package")
                except:
                    # Try with full assembly name for .NET Framework compatibility
                    clr.AddReference("System.Management, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")  # type: ignore
                    logger.info("[LHM] System.Management loaded with full name for HardwareMonitor package")
            except Exception as e:
                logger.warning(f"[LHM] Could not preload System.Management for HardwareMonitor: {e}")
                # Continue anyway - the HardwareMonitor package might still work without explicit loading
            
            from HardwareMonitor.Hardware import Computer  # type: ignore
            from HardwareMonitor.Util import OpenComputer  # type: ignore
            
            # Try with motherboard disabled first to avoid System.Management issues
            try:
                self.hw_monitor = OpenComputer(
                    motherboard=False,  # Disable motherboard sensors to avoid System.Management
                    cpu=True,
                    gpu=True,
                    memory=True,
                    storage=True,
                    network=True,
                    controller=False,  # Disable controllers to avoid System.Management
                    battery=True
                )
                self.hw_monitor.Update()
                logger.info("[LHM] HardwareMonitor package initialized (motherboard/controllers disabled)")
            except Exception as e:
                logger.warning(f"[LHM] Failed with limited sensors, trying minimal configuration: {e}")
                # Try with only CPU and GPU
                self.hw_monitor = OpenComputer(
                    motherboard=False,
                    cpu=True,
                    gpu=True,
                    memory=False,
                    storage=False,
                    network=False,
                    controller=False,
                    battery=False
                )
                self.hw_monitor.Update()
                logger.info("[LHM] HardwareMonitor package initialized (minimal mode - CPU/GPU only)")
            return True
            
        except ImportError as e:
            logger.warning(f"[LHM] HardwareMonitor package not available: {e}")
            return False
        except Exception as e:
            logger.error(f"[LHM] HardwareMonitor initialization failed: {e}")
            return False

    async def _initialize_dll_monitor(self) -> bool:
        """Initialize using direct DLL access with improved Python.NET handling"""
        try:
            # Initialize Python.NET runtime before importing clr
            import pythonnet  # type: ignore
            pythonnet.load("coreclr")  # type: ignore
            
            import clr  # type: ignore
            import os
            import sys
            
            # Import System namespace for Python.NET 3.x compatibility
            import System  # type: ignore
            from System import AppDomain  # type: ignore
            from System.Reflection import Assembly  # type: ignore
            
            # AGGRESSIVE System.Management loading - try every possible method
            system_management_loaded = False
            
            # Method 1: Try direct GAC loading
            try:
                clr.AddReference("System.Management")  # type: ignore
                logger.info("[LHM] System.Management loaded via GAC")
                system_management_loaded = True
            except Exception as e:
                logger.warning(f"[LHM] GAC loading failed: {e}")
                
                # Method 2: Try with full assembly name
                try:
                    clr.AddReference("System.Management, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a")  # type: ignore
                    logger.info("[LHM] System.Management loaded with full assembly name")
                    system_management_loaded = True
                except Exception as e2:
                    logger.warning(f"[LHM] Full name loading failed: {e2}")
                    
                    # Method 3: Load from specific .NET Framework path
                    try:
                        framework_paths = [
                            r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Management.dll",
                            r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\System.Management.dll",
                            r"C:\Windows\Microsoft.NET\Framework64\v2.0.50727\System.Management.dll",
                            r"C:\Windows\Microsoft.NET\Framework\v2.0.50727\System.Management.dll"
                        ]
                        
                        for dll_path in framework_paths:
                            if os.path.exists(dll_path):
                                try:
                                    clr.AddReference(dll_path)  # type: ignore
                                    logger.info(f"[LHM] System.Management loaded from {dll_path}")
                                    system_management_loaded = True
                                    break
                                except Exception as e3:
                                    logger.debug(f"[LHM] Failed to load from {dll_path}: {e3}")
                                    continue
                    except Exception as e4:
                        logger.warning(f"[LHM] Direct path loading failed: {e4}")
                        
                        # Method 4: Force load via Assembly.LoadFrom
                        try:
                            for dll_path in framework_paths:
                                if os.path.exists(dll_path):
                                    try:
                                        Assembly.LoadFrom(dll_path)
                                        logger.info(f"[LHM] System.Management force-loaded via Assembly.LoadFrom: {dll_path}")
                                        system_management_loaded = True
                                        break
                                    except Exception as e5:
                                        logger.debug(f"[LHM] Assembly.LoadFrom failed for {dll_path}: {e5}")
                                        continue
                        except Exception as e6:
                            logger.warning(f"[LHM] Assembly.LoadFrom method failed: {e6}")
            
            if not system_management_loaded:
                logger.error("[LHM] CRITICAL: Could not load System.Management - trying PowerShell workaround")
                try:
                    import subprocess
                    result = subprocess.run([
                        'powershell', '-Command',
                        'Add-Type -AssemblyName "System.Management"; [System.Management.ManagementScope]::new().Path'
                    ], check=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        logger.info("[LHM] System.Management verified via PowerShell")
                        system_management_loaded = True
                except Exception as ps_error:
                    logger.error(f"[LHM] PowerShell workaround failed: {ps_error}")
            
            # Get the correct DLL path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.join(current_dir, "..", "..") # server directory
            dll_path = os.path.join(project_root, "LibreHardwareMonitorLib.dll")
            dll_path = os.path.abspath(dll_path)
            logger.info(f"[LHM] Looking for DLL at: {dll_path}")
            
            if not os.path.exists(dll_path):
                logger.error(f"[LHM] DLL not found at: {dll_path}")
                return False
                
            # Add the DLL directory to both sys.path and PATH
            dll_dir = os.path.dirname(dll_path)
            if dll_dir not in sys.path:
                sys.path.append(dll_dir)
                
            # Add to PATH for native DLL loading
            os.environ["PATH"] = f"{dll_dir};{os.environ['PATH']}"
            
            # Check for existing assembly and handle conflicts (Python.NET 3.x compatible)
            assembly_already_loaded = False
            try:
                existing_assemblies = AppDomain.CurrentDomain.GetAssemblies()
                for assembly in existing_assemblies:
                    if 'LibreHardwareMonitorLib' in str(assembly.GetName()):
                        logger.info("[LHM] Found existing LHM assembly, will reuse it")
                        assembly_already_loaded = True
                        break
            except Exception as e:
                logger.debug(f"[LHM] Could not check existing assemblies: {e}")
                    
            # Add reference to the DLL only if not already loaded
            if not assembly_already_loaded:
                try:
                    clr.AddReference(dll_path)  # type: ignore
                    logger.info("[LHM] LibreHardwareMonitorLib.dll loaded successfully")
                except Exception as e:
                    logger.error(f"[LHM] Failed to load DLL: {e}")
                    return False
            else:
                logger.info("[LHM] Reusing already loaded LibreHardwareMonitorLib assembly")
            
            # Import and initialize LibreHardwareMonitor
            from LibreHardwareMonitor.Hardware import Computer  # type: ignore
            
            self.dll_monitor = Computer()
            
            # FORCE FULL MONITORING - enable everything regardless of System.Management status
            self.dll_monitor.IsCpuEnabled = True
            self.dll_monitor.IsGpuEnabled = True
            self.dll_monitor.IsMemoryEnabled = True
            self.dll_monitor.IsNetworkEnabled = True
            
            # Try to enable storage and motherboard - if System.Management is loaded, this should work
            if system_management_loaded:
                logger.info("[LHM] Enabling FULL hardware monitoring (System.Management available)")
                self.dll_monitor.IsMotherboardEnabled = True
                self.dll_monitor.IsStorageEnabled = True
                self.dll_monitor.IsBatteryEnabled = True
                
                # Test if System.IO.Ports is available for controllers
                controllers_enabled = False
                try:
                    import System  # type: ignore
                    from System.Reflection import Assembly  # type: ignore
                    
                    # Try to load System.IO.Ports
                    try:
                        clr.AddReference("System.IO.Ports")  # type: ignore
                        logger.info("[LHM] System.IO.Ports loaded - enabling controllers")
                        self.dll_monitor.IsControllerEnabled = True
                        controllers_enabled = True
                    except Exception as ports_error:
                        logger.warning(f"[LHM] System.IO.Ports not available: {ports_error}")
                        self.dll_monitor.IsControllerEnabled = False
                        
                except Exception as ports_test_error:
                    logger.warning(f"[LHM] Cannot test System.IO.Ports: {ports_test_error}")
                    self.dll_monitor.IsControllerEnabled = False
                
                monitoring_type = "FULL" if controllers_enabled else "EXTENDED (no controllers)"
                logger.info(f"[LHM] Monitoring mode: {monitoring_type}")
                
            else:
                logger.warning("[LHM] Attempting LIMITED monitoring (System.Management issues)")
                self.dll_monitor.IsMotherboardEnabled = False
                self.dll_monitor.IsStorageEnabled = False
                self.dll_monitor.IsControllerEnabled = False
                self.dll_monitor.IsBatteryEnabled = False
            
            try:
                self.dll_monitor.Open()
                if system_management_loaded:
                    logger.info("[LHM] ✅ DLL backend initialized successfully - FULL MONITORING ACTIVE!")
                else:
                    logger.warning("[LHM] ⚠️ DLL backend initialized with limited sensors")
                return True
            except Exception as open_error:
                logger.error(f"[LHM] Failed to open DLL monitor: {open_error}")
                
                # If controllers are causing issues, try without them
                if system_management_loaded and self.dll_monitor.IsControllerEnabled:
                    logger.info("[LHM] Retrying without controller sensors (System.IO.Ports issues)...")
                    self.dll_monitor.IsControllerEnabled = False
                    try:
                        self.dll_monitor.Open()
                        logger.info("[LHM] ✅ DLL backend initialized successfully - EXTENDED monitoring active!")
                        return True
                    except Exception as retry_error:
                        logger.error(f"[LHM] Retry without controllers failed: {retry_error}")
                
                # If still failing, try step-by-step sensor enabling
                logger.info("[LHM] Attempting step-by-step sensor configuration...")
                
                # Reset computer instance
                self.dll_monitor = Computer()
                
                # Enable sensors one by one and test
                sensors_enabled = []
                
                # Core sensors (should always work)
                self.dll_monitor.IsCpuEnabled = True
                sensors_enabled.append("CPU")
                
                self.dll_monitor.IsGpuEnabled = True
                sensors_enabled.append("GPU")
                
                try:
                    self.dll_monitor.IsMemoryEnabled = True
                    sensors_enabled.append("Memory")
                except:
                    logger.warning("[LHM] Memory sensors failed")
                
                try:
                    self.dll_monitor.IsNetworkEnabled = True
                    sensors_enabled.append("Network")
                except:
                    logger.warning("[LHM] Network sensors failed")
                
                # Try storage (might fail without System.Management)
                try:
                    if system_management_loaded:
                        self.dll_monitor.IsStorageEnabled = True
                        sensors_enabled.append("Storage")
                except:
                    logger.warning("[LHM] Storage sensors failed")
                
                # Try motherboard (might fail without System.Management)
                try:
                    if system_management_loaded:
                        self.dll_monitor.IsMotherboardEnabled = True
                        sensors_enabled.append("Motherboard")
                except:
                    logger.warning("[LHM] Motherboard sensors failed")
                
                # Skip controllers completely if they're causing issues
                self.dll_monitor.IsControllerEnabled = False
                
                # Try final open
                try:
                    self.dll_monitor.Open()
                    logger.info(f"[LHM] ✅ DLL backend initialized with sensors: {', '.join(sensors_enabled)}")
                    return True
                except Exception as final_error:
                    logger.error(f"[LHM] Final initialization attempt failed: {final_error}")
                    
                    # Last resort - minimal config
                    logger.info("[LHM] Last resort: minimal configuration...")
                    self.dll_monitor = Computer()
                    self.dll_monitor.IsCpuEnabled = True
                    self.dll_monitor.IsGpuEnabled = True
                    # Disable everything else
                    self.dll_monitor.IsMemoryEnabled = False
                    self.dll_monitor.IsMotherboardEnabled = False
                    self.dll_monitor.IsControllerEnabled = False
                    self.dll_monitor.IsNetworkEnabled = False
                    self.dll_monitor.IsStorageEnabled = False
                    self.dll_monitor.IsBatteryEnabled = False
                    
                    try:
                        self.dll_monitor.Open()
                        logger.warning("[LHM] ⚠️ Minimal configuration active (CPU/GPU only)")
                        return True
                    except Exception as minimal_error:
                        logger.error(f"[LHM] Even minimal configuration failed: {minimal_error}")
                        return False
            
        except ImportError as e:
            logger.warning(f"[LHM] pythonnet not available for DLL backend: {e}")
            return False
        except Exception as e:
            logger.error(f"[LHM] DLL initialization failed: {e}")
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
                from HardwareMonitor.Hardware import SensorType  # type: ignore
            else:
                from LibreHardwareMonitor.Hardware import SensorType  # type: ignore
            
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
