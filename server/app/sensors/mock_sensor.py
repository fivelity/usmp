"""
Mock sensor implementation for development and testing.
Generates realistic-looking hardware monitoring data.
"""

import random
import math
import time
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from .base import BaseSensor
from ..models.sensor import SensorReading, SensorDefinition, SensorCategory, HardwareType, SensorValueType
from ..core.config import AppSettings
from ..core.logging import get_logger

class MockSensor(BaseSensor):
    """Mock sensor data generator for development and testing."""
    source_id = "mock"  # Unique identifier for this sensor source
    source_name = "MockSensor" # Display name for this sensor source

    def __init__(self):
        super().__init__(display_name=self.source_name)
        self.logger = get_logger("mock_sensor")
        self.app_settings: Optional[AppSettings] = None
        self.start_time = time.monotonic()
        self._pydantic_sensor_definitions: List[SensorDefinition] = []
        
        # Raw definitions, to be converted to Pydantic models in initialize()
        # Added 'hardware_name' for more descriptive SensorDefinition
        # Added 'value_type' to guide data generation/interpretation
        self._raw_sensor_definitions = [
            {
                "id": "cpu_temp", "name": "CPU Core #1 Temp", "hardware_name": "CPU Package", "unit": "°C", 
                "category_str": "temperature", "hardware_type_str": "cpu", "value_type": SensorValueType.FLOAT,
                "min_value": 30.0, "max_value": 95.0, "base_value": 45.0, "variation": 25.0
            },
            {
                "id": "cpu_usage", "name": "CPU Total Usage", "hardware_name": "CPU Package", "unit": "%", 
                "category_str": "usage", "hardware_type_str": "cpu", "value_type": SensorValueType.FLOAT,
                "min_value": 0.0, "max_value": 100.0, "base_value": 25.0, "variation": 40.0
            },
            {
                "id": "cpu_power", "name": "CPU Package Power", "hardware_name": "CPU Package", "unit": "W", 
                "category_str": "power", "hardware_type_str": "cpu", "value_type": SensorValueType.FLOAT,
                "min_value": 10.0, "max_value": 150.0, "base_value": 55.0, "variation": 35.0
            },
            {
                "id": "gpu_temp", "name": "GPU Core Temp", "hardware_name": "GPU NVIDIA XYZ", "unit": "°C", 
                "category_str": "temperature", "hardware_type_str": "gpu", "value_type": SensorValueType.FLOAT,
                "min_value": 30.0, "max_value": 85.0, "base_value": 50.0, "variation": 20.0
            },
            {
                "id": "gpu_fan_speed", "name": "GPU Fan 1 Speed", "hardware_name": "GPU NVIDIA XYZ", "unit": "RPM", 
                "category_str": "fan", "hardware_type_str": "gpu", "value_type": SensorValueType.INTEGER,
                "min_value": 0.0, "max_value": 3500.0, "base_value": 800.0, "variation": 1000.0
            },
            {
                "id": "ram_usage_percent", "name": "RAM Usage", "hardware_name": "System Memory", "unit": "%", 
                "category_str": "usage", "hardware_type_str": "memory", "value_type": SensorValueType.FLOAT,
                "min_value": 10.0, "max_value": 95.0, "base_value": 40.0, "variation": 15.0
            },
            {
                "id": "ram_used_gb", "name": "RAM Used", "hardware_name": "System Memory", "unit": "GB", 
                "category_str": "data_size", "hardware_type_str": "memory", "value_type": SensorValueType.FLOAT,
                "min_value": 2.0, "max_value": 30.0, "base_value": 8.0, "variation": 6.0 # Assuming 32GB total for variation range
            },
            {
                "id": "main_drive_temp", "name": "SSD Main Temp", "hardware_name": "NVMe SSD XYZ", "unit": "°C", 
                "category_str": "temperature", "hardware_type_str": "storage", "value_type": SensorValueType.FLOAT,
                "min_value": 25.0, "max_value": 70.0, "base_value": 35.0, "variation": 10.0
            }
        ]

    async def initialize(self, app_settings: AppSettings) -> bool:
        await super().initialize(app_settings)
        self.app_settings = app_settings
        self._pydantic_sensor_definitions = []

        for raw_def in self._raw_sensor_definitions:
            try:
                category = SensorCategory(raw_def["category_str"])
                hardware_type = HardwareType(raw_def["hardware_type_str"])
                
                sensor_def = SensorDefinition(
                    sensor_id=raw_def["id"],
                    name=raw_def["name"],
                    source_id=self.source_id,
                    unit=raw_def["unit"],
                    category=category,
                    hardware_type=hardware_type,
                    min_value=raw_def.get("min_value"),
                    max_value=raw_def.get("max_value"),
                    metadata={
                        "hardware_id": f"mock_hw_{raw_def['id']}",
                        "hardware_name": raw_def["hardware_name"],
                        "value_type": raw_def["value_type"].value
                    }
                )
                self._pydantic_sensor_definitions.append(sensor_def)
            except ValueError as e:
                self.logger.error(f"Invalid enum value for sensor {raw_def['id']}: {e}")
            except Exception as e:
                self.logger.error(f"Error processing raw sensor definition {raw_def['id']}: {e}", exc_info=True)
        
        if not self._pydantic_sensor_definitions:
            self.logger.warning("MockSensor: No sensor definitions were successfully loaded.")
            self.is_active = False # Explicitly set to inactive if no sensors
        else:
            self.is_active = True # Set to active when sensors are successfully loaded
            self.logger.info(f"MockSensor initialized with {len(self._pydantic_sensor_definitions)} sensor definitions.")
        return self.is_active

    async def close(self) -> None:
        await super().close()
        self.logger.info("MockSensor closed.")

    async def is_available(self) -> bool:
        await asyncio.sleep(0) # Yield control, simulate async check
        return self.is_active # Availability determined during initialization

    async def get_available_sensors(self) -> List[SensorDefinition]:
        await asyncio.sleep(0)
        if not self.is_active:
            return []
        return self._pydantic_sensor_definitions

    async def get_current_data(self) -> List[SensorReading]:
        await asyncio.sleep(0)
        if not self.is_active:
            return []

        readings: List[SensorReading] = []
        current_monotonic_time = time.monotonic()
        elapsed = current_monotonic_time - self.start_time

        for i, sensor_def in enumerate(self._pydantic_sensor_definitions):
            # Find corresponding raw definition for generation parameters
            # This assumes IDs in _raw_sensor_definitions match SensorDefinition IDs
            raw_def = next((rd for rd in self._raw_sensor_definitions if rd["id"] == sensor_def.sensor_id), None)
            if not raw_def:
                self.logger.warning(f"Could not find raw definition for sensor ID {sensor_def.sensor_id}. Skipping.")
                continue

            base_value = raw_def["base_value"]
            variation = raw_def["variation"]
            min_val = raw_def["min_value"]
            max_val = raw_def["max_value"]

            # Create realistic variations using sine waves and random noise
            # Different time factors for variety across sensors
            time_factor = elapsed / (60.0 + i * 5)  # Convert to minutes, vary period
            
            sine_variation = math.sin(time_factor * 0.1 * (1 + i * 0.05)) * 0.3 
            fast_variation = math.sin(time_factor * 2.0 * (1 + i * 0.05)) * 0.1
            noise = (random.random() - 0.5) * 0.2
            
            variation_factor = sine_variation + fast_variation + noise
            current_value_unclamped = base_value + (variation_factor * variation)
            current_value = max(min_val, min(max_val, current_value_unclamped))

            # Get value type from metadata
            value_type = raw_def["value_type"]
            if value_type == SensorValueType.INTEGER:
                current_value = round(current_value)
            elif value_type == SensorValueType.FLOAT:
                current_value = round(current_value, 2) # Default to 2 decimal places for floats
            # else string, boolean - not handled by this mock's generation logic for now

            reading = SensorReading(
                sensor_id=sensor_def.sensor_id,
                name=sensor_def.name,
                value=current_value,
                unit=sensor_def.unit,
                category=sensor_def.category,
                hardware_type=sensor_def.hardware_type,
                source=self.source_id,
                min_value=sensor_def.min_value,
                max_value=sensor_def.max_value,
                timestamp=datetime.now(timezone.utc),
                metadata=sensor_def.metadata.copy() if sensor_def.metadata else {}
            )
            readings.append(reading)
        
        return readings
