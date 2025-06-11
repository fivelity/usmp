"""
Ultimate Sensor Monitor - Models Package
Centralized model exports for the sensor monitoring system.
"""

# Core sensor models
from .sensor import (
    SensorReading,
    SensorSource,
    SensorAlert,
    PerformanceMetrics,
    SensorDataBatch,
    # Enumerations
    SensorStatus,
    SensorCategory,
    HardwareType,
    DataQuality,
)

# Widget and Dashboard models
from .widget import (
    WidgetConfig,
    WidgetGroup,
    DashboardLayout,
    DashboardPreset,
    VisualSettings,
    GaugeType,
)

# Backward compatibility alias
SensorData = SensorReading


# Export all models for easy importing
__all__ = [
    # Core sensor models
    "SensorReading",
    "SensorSource",
    "SensorAlert",
    "PerformanceMetrics",
    "SensorDataBatch",
    # Enumerations from sensor models
    "SensorStatus",
    "SensorCategory",
    "HardwareType",
    "DataQuality",
    # Widget and Dashboard models
    "WidgetConfig",
    "WidgetGroup",
    "DashboardLayout",
    "DashboardPreset",
    "VisualSettings",
    "GaugeType",
    # Backward compatibility
    "SensorData",
]

# Version info
__version__ = "2.0.0"
