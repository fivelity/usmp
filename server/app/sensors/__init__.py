from .mock_sensor import MockSensor
from .hwinfo_sensor import HWiNFOSensor
from .lhm_sensor import LHMSensor
from .hw_sensor import HWSensor

# List of available sensor classes in priority order
# Primary: HardwareMonitor Python package
# Fallback 1: LibreHardwareMonitor.dll direct
# Fallback 2: Mock data (always available)
AVAILABLE_SENSOR_CLASSES = [
    HWSensor,        # Primary: HardwareMonitor Python package
    LHMSensor,       # Fallback: LibreHardwareMonitor.dll
    MockSensor,      # Final fallback: Mock data
    # HWiNFOSensor,  # Disabled for now
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
    "LHMSensor",
    "HWSensor",
    "AVAILABLE_SENSOR_CLASSES",
    "SENSOR_CLASS_MAP",
    "get_sensor_class",
    "get_all_sensor_sources",
]
