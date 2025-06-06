from .mock_sensor import MockSensor
from .hwinfo_sensor import HWiNFOSensor
from .lhm_sensor import LHMSensor # Updated import

# List of available sensor classes
AVAILABLE_SENSOR_CLASSES = [
    MockSensor,
    HWiNFOSensor,
    LHMSensor, # Updated class name
]

# Dictionary to map source names to sensor classes for easy lookup
SENSOR_CLASS_MAP = {cls.source_name: cls for cls in AVAILABLE_SENSOR_CLASSES}

def get_sensor_class(source_name: str):
    """
    Retrieves a sensor class by its source name.
    """
    return SENSOR_CLASS_MAP.get(source_name)

def get_all_sensor_sources() -> list[str]:
    """
    Returns a list of all available sensor source names.
    """
    return list(SENSOR_CLASS_MAP.keys())

__all__ = [
    "MockSensor",
    "HWiNFOSensor",
    "LHMSensor", # Updated class name
    "AVAILABLE_SENSOR_CLASSES",
    "SENSOR_CLASS_MAP",
    "get_sensor_class",
    "get_all_sensor_sources",
]
