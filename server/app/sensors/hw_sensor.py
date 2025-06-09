"""
Hardware Monitor Sensor implementation using the HardwareMonitor Python package.
This is the primary sensor source with fallback to other implementations.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..core.config import AppSettings
from ..core.logging import get_logger
from ..models.sensor import SensorDefinition, SensorReading
from .base import BaseSensor

try:
    import HardwareMonitor
    from HardwareMonitor.Util import OpenComputer, ToBuiltinTypes, SensorValueToString
    from HardwareMonitor.Hardware import SensorType, HardwareType
    HARDWARE_MONITOR_AVAILABLE = True
    _hw_import_error = None
except ImportError as e:
    HARDWARE_MONITOR_AVAILABLE = False
    HardwareMonitor = None
    _hw_import_error = str(e)
except Exception as e:
    HARDWARE_MONITOR_AVAILABLE = False
    HardwareMonitor = None
    _hw_import_error = str(e)
    

class HWSensor(BaseSensor):
    """Primary sensor implementation using HardwareMonitor Python package."""
    
    source_id = "HardwareMonitor"
    source_name = "HardwareMonitor"
    display_name = "Hardware Monitor (Python Package)"
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("hw_sensor")
        self.computer = None
        self._initialized = False
        self._available = False
        
    async def initialize(self, settings: AppSettings) -> None:
        """Initialize the HardwareMonitor sensor."""
        self.logger.info("🔧 Starting HardwareMonitor initialization...")
        
        if not HARDWARE_MONITOR_AVAILABLE:
            self.logger.error("💥 HardwareMonitor package is not available!")
            self.logger.error(f"   Import error: {_hw_import_error}")
            self.logger.info("   💡 Possible solutions:")
            self.logger.info("      • Install package: pip install HardwareMonitor")
            self.logger.info("      • Fix Python.NET: pip install --upgrade pythonnet")
            self.logger.info("      • Run as Administrator")
            self.logger.info("      • Run automated fix: python dependency_installer.py")
            self.logger.info("      • Run diagnostics: python system_diagnostics.py")
            return
            
        try:
            # Check admin privileges first
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            self.logger.info(f"👑 Admin privileges: {'✅ YES' if is_admin else '❌ NO'}")
            
            if not is_admin:
                self.logger.warning("⚠️  Admin privileges recommended for full hardware access")
            
            self.logger.info("🖥️  Initializing HardwareMonitor computer...")
            self.logger.debug("   Enabling all sensor types: CPU, GPU, Memory, Storage, Network, etc.")
            
            # Initialize computer with all sensor types enabled
            self.computer = OpenComputer(
                cpu=True,
                gpu=True,
                motherboard=True,
                memory=True,
                storage=True,
                network=True,
                controller=True,
                all=True  # Enable all available sensors
            )
            
            if self.computer:
                self.logger.info("✅ HardwareMonitor computer initialized successfully!")
                
                # Try to get some initial data to verify it's working
                try:
                    self.computer.Update()
                    data = ToBuiltinTypes(self.computer.Hardware)
                    hardware_count = len(data) if data else 0
                    self.logger.info(f"🔍 Found {hardware_count} hardware components")
                    
                    self._initialized = True
                    self._available = True
                except Exception as test_e:
                    self.logger.error(f"❌ HardwareMonitor computer created but data access failed: {test_e}")
                    self._initialized = False
                    self._available = False
            else:
                self.logger.error("❌ Failed to initialize HardwareMonitor computer (returned None)")
                
        except Exception as e:
            self.logger.error(f"💥 Error initializing HardwareMonitor: {e}")
            self.logger.debug("   Full error details:", exc_info=True)
            
            # Provide specific guidance based on error type
            error_str = str(e).lower()
            if "access" in error_str or "permission" in error_str:
                self.logger.info("   💡 Try running as Administrator")
            elif "assembly" in error_str or "dll" in error_str:
                self.logger.info("   💡 Check .NET Framework installation")
            elif "clr" in error_str:
                self.logger.info("   💡 Try: pip install --upgrade pythonnet")
                
            self._initialized = False
            self._available = False
    
    async def is_available(self) -> bool:
        """Check if HardwareMonitor is available and working."""
        if not HARDWARE_MONITOR_AVAILABLE:
            return False
            
        if not self._initialized:
            return False
            
        try:
            # Try to update the computer to verify it's working
            if self.computer:
                self.computer.Update()
                return True
        except Exception as e:
            self.logger.warning(f"HardwareMonitor availability check failed: {e}")
            self._available = False
            
        return False
    
    async def get_available_sensors(self) -> List[SensorDefinition]:
        """Get all available sensor definitions from HardwareMonitor."""
        if not await self.is_available():
            return []
            
        sensors = []
        
        try:
            # Update computer to get latest data
            self.computer.Update()
            
            # Convert to builtin types for easier processing
            data = ToBuiltinTypes(self.computer.Hardware)
            
            if not data:
                self.logger.warning("No hardware data available from HardwareMonitor")
                return sensors
            
            # Process each hardware component
            for hardware in data:
                if not hardware or 'Sensors' not in hardware:
                    continue
                    
                hardware_name = hardware.get('Name', 'Unknown Hardware')
                hardware_type = hardware.get('HardwareType', 'Unknown')
                
                # Process each sensor
                for sensor in hardware['Sensors']:
                    if not sensor:
                        continue
                        
                    sensor_id = f"{self.source_id}_{hardware_name}_{sensor.get('Name', 'Unknown')}"
                    sensor_id = sensor_id.replace(' ', '_').replace('/', '_').replace('\\', '_')
                    
                    sensor_def = SensorDefinition(
                        sensor_id=sensor_id,
                        name=sensor.get('Name', 'Unknown Sensor'),
                        category=self._map_hardware_type(hardware_type),
                        subcategory=hardware_name,
                        data_type=self._map_sensor_type(sensor.get('SensorType', '')),
                        unit=self._get_sensor_unit(sensor.get('SensorType', '')),
                        source=self.source_id,
                        description=f"{hardware_name} - {sensor.get('Name', 'Unknown Sensor')}"
                    )
                    
                    sensors.append(sensor_def)
                    
        except Exception as e:
            self.logger.error(f"Error getting available sensors from HardwareMonitor: {e}", exc_info=True)
            
        self.logger.info(f"Found {len(sensors)} sensors in HardwareMonitor")
        return sensors
    
    async def get_current_data(self) -> List[SensorReading]:
        """Get current sensor readings from HardwareMonitor."""
        if not await self.is_available():
            return []
            
        readings = []
        
        try:
            # Update computer to get latest data
            self.computer.Update()
            
            # Convert to builtin types for easier processing
            data = ToBuiltinTypes(self.computer.Hardware)
            
            if not data:
                return readings
            
            timestamp = datetime.now()
            
            # Process each hardware component
            for hardware in data:
                if not hardware or 'Sensors' not in hardware:
                    continue
                    
                hardware_name = hardware.get('Name', 'Unknown Hardware')
                
                # Process each sensor
                for sensor in hardware['Sensors']:
                    if not sensor:
                        continue
                        
                    sensor_id = f"{self.source_id}_{hardware_name}_{sensor.get('Name', 'Unknown')}"
                    sensor_id = sensor_id.replace(' ', '_').replace('/', '_').replace('\\', '_')
                    
                    value = sensor.get('Value')
                    if value is not None:
                        reading = SensorReading(
                            sensor_id=sensor_id,
                            value=float(value),
                            timestamp=timestamp,
                            status="OK"
                        )
                        readings.append(reading)
                        
        except Exception as e:
            self.logger.error(f"Error getting current data from HardwareMonitor: {e}", exc_info=True)
            
        self.logger.debug(f"Collected {len(readings)} readings from HardwareMonitor")
        return readings
    
    async def close(self) -> None:
        """Close the HardwareMonitor sensor."""
        try:
            if self.computer:
                self.computer.Close()
                self.logger.info("HardwareMonitor computer closed")
        except Exception as e:
            self.logger.error(f"Error closing HardwareMonitor: {e}", exc_info=True)
        finally:
            self.computer = None
            self._initialized = False
            self._available = False
    
    def _map_hardware_type(self, hardware_type: str) -> str:
        """Map HardwareMonitor hardware types to our categories."""
        type_mapping = {
            'Cpu': 'CPU',
            'GpuNvidia': 'GPU',
            'GpuAmd': 'GPU',
            'GpuIntel': 'GPU',
            'Memory': 'Memory',
            'Motherboard': 'Motherboard',
            'SuperIO': 'Motherboard',
            'Storage': 'Storage',
            'Network': 'Network',
            'Cooler': 'Cooling',
            'EmbeddedController': 'System',
            'Psu': 'Power'
        }
        return type_mapping.get(hardware_type, 'System')
    
    def _map_sensor_type(self, sensor_type: str) -> str:
        """Map HardwareMonitor sensor types to our data types."""
        type_mapping = {
            'Voltage': 'voltage',
            'Current': 'current',
            'Clock': 'frequency',
            'Load': 'percentage',
            'Temperature': 'temperature',
            'Fan': 'rpm',
            'Flow': 'flow',
            'Control': 'percentage',
            'Level': 'percentage',
            'Power': 'power',
            'Data': 'data',
            'SmallData': 'data',
            'Factor': 'factor',
            'Frequency': 'frequency',
            'Throughput': 'throughput',
            'TimeSpan': 'time',
            'Energy': 'energy'
        }
        return type_mapping.get(sensor_type, 'unknown')
    
    def _get_sensor_unit(self, sensor_type: str) -> str:
        """Get the unit for a sensor type."""
        unit_mapping = {
            'Voltage': 'V',
            'Current': 'A',
            'Clock': 'MHz',
            'Load': '%',
            'Temperature': '°C',
            'Fan': 'RPM',
            'Flow': 'L/h',
            'Control': '%',
            'Level': '%',
            'Power': 'W',
            'Data': 'GB',
            'SmallData': 'MB',
            'Factor': '',
            'Frequency': 'Hz',
            'Throughput': 'B/s',
            'TimeSpan': 's',
            'Energy': 'mWh'
        }
        return unit_mapping.get(sensor_type, '') 