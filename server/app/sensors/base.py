"""
Abstract base class for sensor data sources.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional, Dict
from ..models.sensor import SensorReading, SensorDefinition
from ..core.config import AppSettings


class BaseSensor(ABC):
    """Abstract base class for all sensor data sources."""
    
    source_id: str # Class attribute to be defined by subclasses (e.g., "lhm", "mock")

    def __init__(self, display_name: str = "Unknown Sensor Provider"):
        self.display_name = display_name # User-friendly name for the provider
        self.is_active = False
        self.last_error: Optional[str] = None
        self.app_settings: Optional[AppSettings] = None # To store settings after initialization

    @abstractmethod
    async def initialize(self, app_settings: AppSettings) -> bool:
        """
        Initialize the sensor provider with application settings.
        Perform any setup, connect to hardware, etc.
        Set self.is_active = True on success.
        Returns True if initialization was successful, False otherwise.
        """
        self.app_settings = app_settings
        return False

    @abstractmethod
    async def close(self) -> None:
        """
        Gracefully shut down the sensor provider.
        Release resources, disconnect from hardware, etc.
        Set self.is_active = False.
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """
        Check if the sensor source is available.
        Returns True if available, False otherwise.
        """
        pass
    
    @abstractmethod
    async def get_available_sensors(self) -> List[SensorDefinition]:
        """
        Get list of available sensor definitions from this source.
        Returns list of SensorDefinition objects.
        """
        pass
    
    @abstractmethod
    async def get_current_data(self) -> List[SensorReading]:
        """
        Get current sensor readings for all sensors provided by this source.
        Returns list of SensorReading objects.
        """
        pass
    
    async def get_sensor_definition_by_id(self, sensor_id: str) -> Optional[SensorDefinition]:
        """Get a specific sensor definition by its ID."""
        sensors = await self.get_available_sensors()
        for sensor_def in sensors:
            if sensor_def.sensor_id == sensor_id:
                return sensor_def
        return None
    
    async def get_sensor_definitions_by_category(self, category: str) -> List[SensorDefinition]:
        """Get sensor definitions filtered by category."""
        sensors = await self.get_available_sensors()
        # Assuming SensorCategory is an Enum and category is a string value of that enum
        return [sensor_def for sensor_def in sensors if sensor_def.category.value == category]
    
    def get_source_info(self) -> Dict[str, Any]:
        """Get information about this sensor source provider."""
        return {
            "source_id": self.source_id,
            "display_name": self.display_name,
            "active": self.is_active,
            "last_error": self.last_error
        }
