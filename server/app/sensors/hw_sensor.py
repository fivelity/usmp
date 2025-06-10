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
from ..models.sensor import SensorDefinition, SensorReading, SensorStatus, SensorCategory, HardwareType
from .base import BaseSensor

try:
    import HardwareMonitor
    from HardwareMonitor.Util import OpenComputer, ToBuiltinTypes, SensorValueToString
    # from HardwareMonitor.Hardware import SensorType, HardwareType # Not used directly
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
    display_name = "Hardware Monitor"

    def __init__(self):
        super().__init__(display_name=self.display_name)
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
            return

        try:
            # Check admin privileges first
            is_admin = False
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            except (ImportError, AttributeError):
                 self.logger.warning("Could not check admin privileges (not on Windows).")

            self.logger.info(f"👑 Admin privileges: {'✅ YES' if is_admin else '❌ NO'}")

            if not is_admin:
                self.logger.warning("⚠️  Admin privileges recommended for full hardware access")

            self.logger.info("🖥️  Initializing HardwareMonitor computer...")
            self.computer = OpenComputer(
                cpu=True, gpu=True, motherboard=True, memory=True,
                storage=True, network=True, controller=True
            )

            if self.computer:
                self.logger.info("✅ HardwareMonitor computer initialized successfully!")
                self.computer.Update()
                hardware_list = ToBuiltinTypes(self.computer.Hardware)
                self.logger.info(f"🔍 Found {len(hardware_list) if hardware_list else 0} hardware components")
                self._initialized = True
                self._available = True
            else:
                self.logger.error("❌ Failed to initialize HardwareMonitor computer (returned None)")

        except Exception as e:
            self.logger.error(f"💥 Error initializing HardwareMonitor: {e}", exc_info=True)
            self._initialized = False
            self._available = False

    async def is_available(self) -> bool:
        """Check if HardwareMonitor is available and working."""
        return self._initialized and self._available

    async def get_available_sensors(self) -> List[SensorDefinition]:
        """Get all available sensor definitions from HardwareMonitor."""
        if not await self.is_available():
            return []

        sensors = []
        try:
            self.computer.Update()
            data = ToBuiltinTypes(self.computer.Hardware)

            if not data:
                self.logger.warning("No hardware data available from HardwareMonitor")
                return []

            for hardware in data:
                if not hardware or 'Sensors' not in hardware:
                    continue

                hardware_name = hardware.get('Name', 'Unknown Hardware')
                hardware_type = self._map_hardware_type(hardware.get('HardwareType'))

                for sensor in hardware['Sensors']:
                    if not sensor:
                        continue
                    
                    sensor_name = sensor.get('Name', 'Unknown Sensor')
                    sensor_type = sensor.get('SensorType')

                    sensor_id = f"{self.source_id}_{hardware_name}_{sensor_name}".replace(' ', '_').replace('/', '_').replace('\\', '_')

                    sensor_def = SensorDefinition(
                        sensor_id=sensor_id,
                        name=sensor_name,
                        category=self._map_sensor_type_to_category(sensor_type),
                        hardware_type=hardware_type,
                        unit=self._get_sensor_unit(sensor_type),
                        source_id=self.source_id,
                        description=f"{hardware_name} - {sensor_name}",
                        min_value=sensor.get('Min'),
                        max_value=sensor.get('Max'),
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
            self.computer.Update()
            data = ToBuiltinTypes(self.computer.Hardware)
            timestamp = datetime.now()

            if not data:
                return []

            for hardware in data:
                if not hardware or 'Sensors' not in hardware:
                    continue
                
                hardware_name = hardware.get('Name', 'Unknown Hardware')
                hardware_type = self._map_hardware_type(hardware.get('HardwareType'))

                for sensor in hardware['Sensors']:
                    if not sensor or sensor.get('Value') is None:
                        continue

                    sensor_name = sensor.get('Name', 'Unknown Sensor')
                    sensor_type = sensor.get('SensorType')
                    sensor_id = f"{self.source_id}_{hardware_name}_{sensor_name}".replace(' ', '_').replace('/', '_').replace('\\', '_')

                    reading = SensorReading(
                        sensor_id=sensor_id,
                        name=sensor_name,
                        value=float(sensor['Value']),
                        unit=self._get_sensor_unit(sensor_type),
                        category=self._map_sensor_type_to_category(sensor_type),
                        hardware_type=hardware_type,
                        source=self.source_id,
                        timestamp=timestamp,
                        status=SensorStatus.ACTIVE,
                        min_value=sensor.get('Min'),
                        max_value=sensor.get('Max'),
                        parent_hardware=hardware_name
                    )
                    readings.append(reading)

        except Exception as e:
            self.logger.error(f"Error getting current data from HardwareMonitor: {e}", exc_info=True)

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

    def _map_hardware_type(self, hw_type_str: Optional[str]) -> HardwareType:
        """Maps hardware type string from library to HardwareType enum."""
        if not hw_type_str:
            return HardwareType.UNKNOWN
        mapping = {
            'CPU': HardwareType.CPU,
            'GpuNvidia': HardwareType.GPU,
            'GpuAmd': HardwareType.GPU,
            'GpuIntel': HardwareType.GPU,
            'Memory': HardwareType.MEMORY,
            'Motherboard': HardwareType.MOTHERBOARD,
            'Storage': HardwareType.STORAGE,
            'Network': HardwareType.NETWORK,
            'Cooler': HardwareType.COOLER,
            'Psu': HardwareType.PSU,
        }
        return mapping.get(hw_type_str, HardwareType.UNKNOWN)

    def _map_sensor_type_to_category(self, sensor_type_str: Optional[str]) -> SensorCategory:
        """Map HardwareMonitor SensorType to our SensorCategory enum."""
        if not sensor_type_str:
            return SensorCategory.UNKNOWN
        mapping = {
            'Voltage': SensorCategory.VOLTAGE, 'Current': SensorCategory.CURRENT,
            'Clock': SensorCategory.CLOCK, 'Load': SensorCategory.LOAD,
            'Temperature': SensorCategory.TEMPERATURE, 'Fan': SensorCategory.FAN,
            'Flow': SensorCategory.FLOW, 'Control': SensorCategory.CONTROL,
            'Level': SensorCategory.LEVEL, 'Power': SensorCategory.POWER,
            'Data': SensorCategory.DATA, 'SmallData': SensorCategory.DATA_SIZE,
            'Factor': SensorCategory.FACTOR, 'Frequency': SensorCategory.FREQUENCY,
            'Throughput': SensorCategory.THROUGHPUT, 'Energy': SensorCategory.ENERGY,
            'Noise': SensorCategory.NOISE
        }
        return mapping.get(sensor_type_str, SensorCategory.UNKNOWN)

    def _get_sensor_unit(self, sensor_type_str: Optional[str]) -> str:
        """Get the unit for a sensor type."""
        if not sensor_type_str:
            return ""
        unit_mapping = {
            'Voltage': 'V', 'Current': 'A', 'Clock': 'MHz', 'Load': '%',
            'Temperature': '°C', 'Fan': 'RPM', 'Flow': 'L/h', 'Control': '%',
            'Level': '%', 'Power': 'W', 'Data': 'GB', 'SmallData': 'MB',
            'Factor': '', 'Frequency': 'Hz', 'Throughput': 'B/s',
            'TimeSpan': 's', 'Energy': 'mWh', 'Noise': 'dBA'
        }
        return unit_mapping.get(sensor_type_str, '')
