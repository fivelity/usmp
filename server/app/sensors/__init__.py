from .mock_sensor import MockSensor
from .hwinfo_sensor import HWiNFOSensor

# The hardware-specific sensors are now dynamically imported by the SensorManager
# to avoid startup DLL conflicts.
# from .lhm_sensor import LHMSensor
# from .hw_sensor import HWSensor

# The AVAILABLE_SENSOR_CLASSES list is now effectively managed within the
# SensorManager's initialization logic. It is left empty here to prevent
# causing premature imports of hardware-related modules.
AVAILABLE_SENSOR_CLASSES = [
    MockSensor,  # Mock data is always safe to import
    # HWSensor,      # Removed to prevent eager loading
    # LHMSensor,     # Removed to prevent eager loading
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
    # "LHMSensor",  # No longer exported from here
    # "HWSensor",   # No longer exported from here
    "AVAILABLE_SENSOR_CLASSES",
    "SENSOR_CLASS_MAP",
    "get_sensor_class",
    "get_all_sensor_sources",
]
