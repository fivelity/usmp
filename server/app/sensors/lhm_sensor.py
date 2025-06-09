"""
LHM Sensor - LibreHardwareMonitor integration.
Uses LibreHardwareMonitor library for hardware monitoring with robust error handling.
"""

import asyncio
import os
import sys
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone

from app.core.config import AppSettings
from app.core.logging import get_logger
from app.models.sensor import (
    SensorDefinition, SensorReading, SensorCategory, HardwareType, SensorValueType
)
from app.sensors.base import BaseSensor

# LibreHardwareMonitor availability check
LHM_AVAILABLE = False
LHMComputerClass = None
LHMHardwareTypeEnum = None
LHMSensorTypeEnum = None

try:
    # Initialize Python.NET runtime
    import pythonnet  # type: ignore
    pythonnet.load("coreclr")  # type: ignore
    
    import clr  # type: ignore
    
    # Locate and load LibreHardwareMonitorLib.dll
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, "..", "..")
    dll_path = os.path.join(project_root, "LibreHardwareMonitorLib.dll")
    dll_path = os.path.abspath(dll_path)
    
    if os.path.exists(dll_path):
        # Add DLL directory to path
        dll_dir = os.path.dirname(dll_path)
        if dll_dir not in sys.path:
            sys.path.append(dll_dir)
        os.environ["PATH"] = f"{dll_dir};{os.environ.get('PATH', '')}"
        
        # Load the DLL
        clr.AddReference(dll_path)  # type: ignore
        
        # Import LibreHardwareMonitor classes
        from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType  # type: ignore
        
        LHMComputerClass = Computer
        LHMHardwareTypeEnum = HardwareType
        LHMSensorTypeEnum = SensorType
        LHM_AVAILABLE = True
        
        _temp_logger = get_logger("lhm_sensor_setup")
        _temp_logger.info("LibreHardwareMonitorLib loaded successfully")
    else:
        _temp_logger = get_logger("lhm_sensor_setup")
        _temp_logger.error(f"LibreHardwareMonitorLib.dll not found at: {dll_path}")

except Exception as e:
    _temp_logger = get_logger("lhm_sensor_setup")
    error_msg = str(e)
    if "System.Management" in error_msg:
        _temp_logger.warning(
            f"LHMSensor initialization failed: Missing .NET System.Management assembly. "
            f"This is common on systems without full .NET Framework support. "
            f"LHMSensor will be disabled, but MockSensor and other providers remain available."
        )
    elif "dotnet --list-runtimes" in error_msg:
        _temp_logger.warning(
            f"LHMSensor initialization failed: .NET runtime detection issue. "
            f"This may occur on some Windows configurations. "
            f"LHMSensor will be disabled, but other sensor providers remain available."
        )
    else:
        _temp_logger.error(
            f"Failed to load LibreHardwareMonitorLib: {e}. "
            f"Ensure Python.NET is installed and LibreHardwareMonitorLib.dll is accessible. "
            f"LHMSensor will not be available."
        )


class LHMSensor(BaseSensor):
    """LibreHardwareMonitor sensor provider with async support and robust error handling."""
    
    source_id = "lhm"  # Unique identifier for this sensor source
    source_name = "LibreHardwareMonitor"
    
    def __init__(self):
        super().__init__(display_name=self.source_name)
        self.logger = get_logger(f"sensor.{self.source_id}")
        self.app_settings: Optional[AppSettings] = None
        self.lhm_computer: Optional[Any] = None
        self._sensor_definitions_map: Dict[str, SensorDefinition] = {}
        self._lhm_sensor_map: Dict[str, Any] = {}
        self._update_task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        self._current_readings: Dict[str, SensorReading] = {}
        
        if not LHM_AVAILABLE:
            self.logger.error("LHM libraries not loaded during initialization. LHMSensor will be inactive.")
            self._mark_inactive()

    async def initialize(self, app_settings: AppSettings) -> bool:
        """Initialize the LHM sensor with proper async handling."""
        await super().initialize(app_settings)
        self.app_settings = app_settings

        if not LHM_AVAILABLE:
            self._mark_inactive()
            self.logger.warning("Initialization skipped: LHM libraries not available.")
            return False

        self.logger.info("Initializing LHMSensor...")
        try:
            # Initialize LHM core in thread to avoid blocking
            init_success = await asyncio.to_thread(self._initialize_lhm_core)
            if init_success:
                self.logger.info(f"LHMSensor initialized successfully with {len(self._sensor_definitions_map)} sensors.")
                # Start background update task
                self._update_task = asyncio.create_task(self._background_update_loop())
                return True
            else:
                self.logger.error("LHMSensor core initialization failed.")
                self._mark_inactive()
                return False
        except Exception as e:
            self.logger.error(f"Exception during LHMSensor initialization: {e}", exc_info=True)
            self._mark_inactive()
            return False

    def _initialize_lhm_core(self) -> bool:
        """Synchronous core LHM initialization logic."""
        if not LHMComputerClass:
            self.logger.error("LHM Computer class not available.")
            return False
            
        try:
            self.lhm_computer = LHMComputerClass()
            
            # Configure hardware monitoring based on settings
            self.lhm_computer.IsCpuEnabled = self.app_settings.lhm_enable_cpu
            self.lhm_computer.IsGpuEnabled = self.app_settings.lhm_enable_gpu
            self.lhm_computer.IsMemoryEnabled = self.app_settings.lhm_enable_memory
            self.lhm_computer.IsMotherboardEnabled = self.app_settings.lhm_enable_motherboard
            self.lhm_computer.IsStorageEnabled = self.app_settings.lhm_enable_storage
            self.lhm_computer.IsNetworkEnabled = self.app_settings.lhm_enable_network
            self.lhm_computer.IsControllerEnabled = self.app_settings.lhm_enable_controller
            
            # Open the computer for monitoring
            self.lhm_computer.Open()
            
            # Verify hardware was detected
            hardware_list = list(self.lhm_computer.Hardware)
            if not hardware_list:
                self.logger.warning("No LHM hardware components found. Check permissions and hardware support.")
                self.lhm_computer.Close()
                self.lhm_computer = None
                return False
            
            # Process all hardware and sensors
            self._sensor_definitions_map.clear()
            self._lhm_sensor_map.clear()
            
            for hardware_item in hardware_list:
                self._process_lhm_hardware(hardware_item)
            
            self.logger.info(f"LHM core initialized with {len(hardware_list)} hardware components.")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in _initialize_lhm_core: {e}", exc_info=True)
            if self.lhm_computer:
                try:
                    self.lhm_computer.Close()
                except Exception:
                    pass
                self.lhm_computer = None
            return False

    async def close(self) -> None:
        """Clean shutdown of LHM sensor."""
        self.logger.info("Closing LHMSensor...")
        
        # Stop background update task
        if self._update_task and not self._update_task.done():
            self._stop_event.set()
            try:
                await asyncio.wait_for(self._update_task, timeout=5.0)
            except asyncio.TimeoutError:
                self.logger.warning("Background update task did not stop gracefully, cancelling...")
                self._update_task.cancel()
                try:
                    await self._update_task
                except asyncio.CancelledError:
                    pass
        
        # Close LHM computer
        if self.lhm_computer:
            try:
                await asyncio.to_thread(self.lhm_computer.Close)
                self.logger.info("LHM Computer closed successfully.")
            except Exception as e:
                self.logger.error(f"Exception closing LHM Computer: {e}", exc_info=True)
            self.lhm_computer = None
        
        # Clear data structures
        self._sensor_definitions_map.clear()
        self._lhm_sensor_map.clear()
        self._current_readings.clear()
        self._mark_inactive()
        
        await super().close()

    async def is_available(self) -> bool:
        """Check if LHM sensor is available and functional."""
        return (
            LHM_AVAILABLE and 
            self.is_active and 
            self.lhm_computer is not None and
            bool(self._sensor_definitions_map)
        )

    async def get_available_sensors(self) -> List[SensorDefinition]:
        """Get list of available sensor definitions."""
        if not await self.is_available():
            return []
        return list(self._sensor_definitions_map.values())

    async def get_current_data(self) -> List[SensorReading]:
        """Get current sensor readings."""
        if not await self.is_available():
            return []
        
        # Return cached readings from background task
        return list(self._current_readings.values())

    async def _background_update_loop(self) -> None:
        """Background task to continuously update sensor readings."""
        self.logger.info("Starting background sensor update loop...")
        
        while not self._stop_event.is_set():
            try:
                # Update sensor data
                readings = await asyncio.to_thread(self._get_lhm_readings_core)
                
                # Update cached readings
                self._current_readings.clear()
                for reading in readings:
                    self._current_readings[reading.id] = reading
                
                self.logger.debug(f"Updated {len(readings)} sensor readings.")
                
                # Wait for next update interval
                try:
                    await asyncio.wait_for(
                        self._stop_event.wait(), 
                        timeout=self.app_settings.lhm_update_interval / 1000.0
                    )
                    break  # Stop event was set
                except asyncio.TimeoutError:
                    continue  # Normal timeout, continue loop
                    
            except Exception as e:
                self.logger.error(f"Error in background update loop: {e}", exc_info=True)
                await asyncio.sleep(1.0)  # Brief pause before retry

    def _get_lhm_readings_core(self) -> List[SensorReading]:
        """Synchronous core logic for fetching LHM readings."""
        readings: List[SensorReading] = []
        
        if not self.lhm_computer:
            return readings
        
        try:
            # Update all hardware components
            for hardware_item in self.lhm_computer.Hardware:
                hardware_item.Update()
                for sub_hardware in hardware_item.SubHardware:
                    sub_hardware.Update()
            
            timestamp = datetime.now(timezone.utc)
            
            # Process all sensors
            for sensor_id, lhm_sensor_obj in self._lhm_sensor_map.items():
                definition = self._sensor_definitions_map.get(sensor_id)
                if not definition:
                    continue
                
                current_value = lhm_sensor_obj.Value
                
                # Skip null values if configured to do so
                if current_value is None and not self.app_settings.lhm_include_null_sensors:
                    continue
                
                # Process and convert value
                processed_value, actual_value_type = self._process_sensor_value(
                    current_value, definition.value_type
                )
                
                reading = SensorReading(
                    sensor_id=definition.sensor_id,
                    name=definition.name,
                    value=processed_value,
                    unit=definition.unit,
                    category=definition.category,
                    hardware_type=definition.hardware_type,
                    source=self.source_id,
                    min_value=definition.min_value,
                    max_value=definition.max_value,
                    timestamp=timestamp,
                    metadata=definition.metadata.copy() if definition.metadata else {}
                )
                readings.append(reading)
                
        except Exception as e:
            self.logger.error(f"Error in _get_lhm_readings_core: {e}", exc_info=True)
        
        return readings

    def _process_sensor_value(self, raw_value: Any, expected_type: SensorValueType) -> tuple[Any, SensorValueType]:
        """Process and convert sensor value to appropriate type."""
        if raw_value is None:
            return None, expected_type
        
        try:
            # Convert to float first for numeric processing
            float_val = float(raw_value)
            
            if expected_type == SensorValueType.INTEGER:
                return int(round(float_val)), SensorValueType.INTEGER
            elif expected_type == SensorValueType.FLOAT:
                return round(float_val, self.app_settings.lhm_float_precision), SensorValueType.FLOAT
            else:
                return str(raw_value), SensorValueType.STRING
                
        except (ValueError, TypeError):
            # If conversion fails, store as string
            self.logger.debug(f"Could not convert value '{raw_value}' to numeric, storing as string.")
            return str(raw_value), SensorValueType.STRING

    def _process_lhm_hardware(self, hardware_item: Any, parent_hw_name: Optional[str] = None) -> None:
        """Recursively process LHM hardware items and their sensors."""
        hardware_item.Update()
        
        hw_name = str(hardware_item.Name)
        hw_id_str = str(hardware_item.Identifier)
        mapped_hw_type = self._map_lhm_hardware_type(hardware_item.HardwareType)
        
        # Create hierarchical name for sub-hardware
        current_hw_path = f"{parent_hw_name} / {hw_name}" if parent_hw_name else hw_name
        
        # Process sensors for this hardware item
        for sensor_item in hardware_item.Sensors:
            if sensor_item.Value is None and not self.app_settings.lhm_include_null_sensors:
                continue
            
            sensor_id = self._generate_sensor_id(hw_id_str, str(sensor_item.Identifier), str(sensor_item.Name))
            category, unit, value_type = self._map_lhm_sensor_type(sensor_item.SensorType)
            
            definition = SensorDefinition(
                sensor_id=sensor_id,
                name=str(sensor_item.Name).strip(),
                source_id=self.source_id,
                unit=unit,
                category=category,
                hardware_type=mapped_hw_type,
                min_value=float(sensor_item.Min) if sensor_item.Min is not None else None,
                max_value=float(sensor_item.Max) if sensor_item.Max is not None else None,
                metadata={
                    "lhm_sensor_type": str(sensor_item.SensorType),
                    "lhm_sensor_identifier": str(sensor_item.Identifier),
                    "hardware_id": hw_id_str.strip(),
                    "hardware_name": current_hw_path.strip(),
                    "value_type": value_type.value
                }
            )
            
            self._sensor_definitions_map[definition.sensor_id] = definition
            self._lhm_sensor_map[definition.sensor_id] = sensor_item
        
        # Recursively process sub-hardware
        for sub_hardware in hardware_item.SubHardware:
            self._process_lhm_hardware(sub_hardware, parent_hw_name=current_hw_path)

    def _generate_sensor_id(self, hw_identifier: str, sensor_identifier: str, sensor_name: str) -> str:
        """Generate a unique sensor ID from LHM identifiers."""
        # Clean and process identifier components
        hw_part = hw_identifier.split('/')[-1].lower().replace(' ', '_').replace('#', '').replace('.', '_')
        sensor_part = sensor_identifier.split('/')[-1].lower().replace(' ', '_').replace('#', '').replace('.', '_')
        name_part = sensor_name.lower().replace(' ', '_').replace('#', '').replace('.', '_')
        
        # Combine parts with reasonable length limit
        full_id = f"lhm_{hw_part}_{sensor_part}_{name_part}"[:128]
        return full_id.strip('_')

    def _map_lhm_hardware_type(self, lhm_hw_type: Any) -> HardwareType:
        """Map LHM HardwareType to our HardwareType enum."""
        if not LHMHardwareTypeEnum:
            return HardwareType.UNKNOWN
        
        mapping = {
            LHMHardwareTypeEnum.Cpu: HardwareType.CPU,
            LHMHardwareTypeEnum.GpuNvidia: HardwareType.GPU,
            LHMHardwareTypeEnum.GpuAmd: HardwareType.GPU,
            LHMHardwareTypeEnum.GpuIntel: HardwareType.GPU,
            LHMHardwareTypeEnum.Memory: HardwareType.MEMORY,
            LHMHardwareTypeEnum.Motherboard: HardwareType.MOTHERBOARD,
            LHMHardwareTypeEnum.Storage: HardwareType.STORAGE,
            LHMHardwareTypeEnum.Network: HardwareType.NETWORK,
            LHMHardwareTypeEnum.Cooler: HardwareType.COOLER,
            LHMHardwareTypeEnum.Psu: HardwareType.PSU,
            LHMHardwareTypeEnum.EmbeddedController: HardwareType.CONTROLLER,
        }
        
        # Handle additional hardware types that might exist
        hw_type_str = str(lhm_hw_type).lower()
        if 'fan' in hw_type_str:
            return HardwareType.FAN
        elif 'battery' in hw_type_str:
            return HardwareType.BATTERY
        
        return mapping.get(lhm_hw_type, HardwareType.UNKNOWN)

    def _map_lhm_sensor_type(self, lhm_sensor_type: Any) -> tuple[SensorCategory, str, SensorValueType]:
        """Map LHM SensorType to our sensor category, unit, and value type."""
        if not LHMSensorTypeEnum:
            return SensorCategory.UNKNOWN, "N/A", SensorValueType.FLOAT
        
        # Mapping dictionary for LHM sensor types
        mapping = {
            LHMSensorTypeEnum.Voltage: (SensorCategory.VOLTAGE, "V", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Current: (SensorCategory.CURRENT, "A", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Power: (SensorCategory.POWER, "W", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Clock: (SensorCategory.FREQUENCY, "MHz", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Temperature: (SensorCategory.TEMPERATURE, "°C", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Load: (SensorCategory.USAGE, "%", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Frequency: (SensorCategory.FREQUENCY, "MHz", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Fan: (SensorCategory.FAN_SPEED, "RPM", SensorValueType.INTEGER),
            LHMSensorTypeEnum.Flow: (SensorCategory.FLOW_RATE, "L/h", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Control: (SensorCategory.CONTROL, "%", SensorValueType.INTEGER),
            LHMSensorTypeEnum.Level: (SensorCategory.LEVEL, "%", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Factor: (SensorCategory.FACTOR, "", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Data: (SensorCategory.DATA_SIZE, "GB", SensorValueType.FLOAT),
            LHMSensorTypeEnum.SmallData: (SensorCategory.DATA_SIZE, "MB", SensorValueType.FLOAT),
            LHMSensorTypeEnum.Throughput: (SensorCategory.THROUGHPUT, "MB/s", SensorValueType.FLOAT),
        }
        
        # Handle additional sensor types that might exist
        if hasattr(LHMSensorTypeEnum, 'Energy'):
            mapping[LHMSensorTypeEnum.Energy] = (SensorCategory.ENERGY, "Wh", SensorValueType.FLOAT)
        if hasattr(LHMSensorTypeEnum, 'Noise'):
            mapping[LHMSensorTypeEnum.Noise] = (SensorCategory.NOISE, "dBA", SensorValueType.FLOAT)
        
        return mapping.get(lhm_sensor_type, (SensorCategory.UNKNOWN, "N/A", SensorValueType.FLOAT))

    def _mark_inactive(self) -> None:
        """Mark this sensor as inactive."""
        self.is_active = False
