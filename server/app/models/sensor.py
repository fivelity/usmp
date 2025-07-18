"""
Sensor data models with comprehensive validation.
Production-ready Pydantic models for type safety and validation.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, conlist, field_validator
from enum import Enum


class SensorProviderStatus(BaseModel):
    """Model for reporting the status of a single sensor provider."""

    name: str
    source_id: str
    available: bool
    sensor_count: int


class SensorStatus(str, Enum):
    """Sensor status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    UNKNOWN = "unknown"


class SensorCategory(str, Enum):
    """Sensor category enumeration."""

    TEMPERATURE = "temperature"
    VOLTAGE = "voltage"
    CURRENT = "current"
    POWER = "power"
    CLOCK = "clock"
    LOAD = "load"
    USAGE = "usage"  # Added for CPU/GPU usage
    FREQUENCY = "frequency"  # Added for clock frequencies
    FAN = "fan"
    FAN_SPEED = "fan_speed"  # Added for fan RPM
    FLOW = "flow"
    FLOW_RATE = "flow_rate"  # Added for flow rates
    CONTROL = "control"
    LEVEL = "level"
    FACTOR = "factor"
    DATA = "data"
    DATA_SIZE = "data_size"  # Added for data sizes
    THROUGHPUT = "throughput"
    ENERGY = "energy"  # Added for energy measurements
    NOISE = "noise"
    UNKNOWN = "unknown"


class HardwareType(str, Enum):
    """Hardware type enumeration."""

    CPU = "cpu"
    GPU = "gpu"
    MEMORY = "memory"
    MOTHERBOARD = "motherboard"
    STORAGE = "storage"
    NETWORK = "network"
    CONTROLLER = "controller"
    BATTERY = "battery"
    COOLER = "cooler"  # Added for cooling systems
    PSU = "psu"  # Added for power supplies
    FAN = "fan"  # Added for individual fans
    UNKNOWN = "unknown"


class SensorValueType(str, Enum):
    """Sensor value type enumeration."""

    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    UNKNOWN = "unknown"


class DataQuality(str, Enum):
    """Data quality enumeration."""

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNKNOWN = "unknown"


class SensorMetadata(BaseModel):
    """Detailed metadata for a sensor."""

    hardware_name: Optional[str] = Field(None, description="Parent hardware name")
    sensor_type: Optional[str] = Field(None, description="Type of the sensor")
    identifier: Optional[str] = Field(None, description="Raw sensor identifier from source")
    description: Optional[str] = Field(None, description="Sensor description")
    location: Optional[str] = Field(None, description="Physical location of the sensor")
    vendor: Optional[str] = Field(None, description="Sensor manufacturer")
    driver_version: Optional[str] = Field(None, description="Driver version for the sensor")
    last_calibration: Optional[datetime] = Field(None, description="Last calibration date")
    accuracy: Optional[float] = Field(None, description="Sensor accuracy percentage")
    resolution: Optional[float] = Field(None, description="Smallest change the sensor can detect")
    update_rate: Optional[float] = Field(None, description="Sensor's own update rate in Hz")


class SensorReading(BaseModel):
    """Individual sensor reading model."""

    sensor_id: str = Field(..., description="Unique sensor identifier")
    name: str = Field(..., description="Human-readable sensor name")
    value: Union[float, int] = Field(..., description="Current sensor value")
    unit: str = Field("", description="Unit of measurement")

    # Optional range information
    min_value: Optional[float] = Field(None, description="Minimum expected value")
    max_value: Optional[float] = Field(None, description="Maximum expected value")

    # Classification
    category: SensorCategory = Field(
        SensorCategory.UNKNOWN, description="Sensor category"
    )
    hardware_type: HardwareType = Field(
        HardwareType.UNKNOWN, description="Hardware type"
    )

    # Hierarchy and source
    source: str = Field(..., description="Data source identifier")
    parent_hardware: Optional[str] = Field(None, description="Parent hardware path")

    # Status and quality
    status: SensorStatus = Field(SensorStatus.ACTIVE, description="Sensor status")
    quality: DataQuality = Field(
        DataQuality.GOOD, description="Data quality assessment"
    )

    # Timestamps
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Reading timestamp"
    )
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")

    # Additional metadata
    metadata: SensorMetadata = Field(
        default_factory=SensorMetadata, description="Additional sensor metadata"
    )

    @field_validator("value")
    def validate_value(cls, v):
        """Validate sensor value is numeric."""
        if not isinstance(v, (int, float)):
            raise ValueError("Sensor value must be numeric")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        """Validate sensor name is not empty."""
        if not v or not v.strip():
            raise ValueError("Sensor name cannot be empty")
        return v.strip()

    model_config = {
        "use_enum_values": True,
        "json_encoders": {datetime: lambda v: v.isoformat()},
    }


class SourceCapabilities(BaseModel):
    """Model for sensor source capabilities."""
    supports_real_time: bool = False
    supports_history: bool = False
    min_update_interval: float = 1.0
    supported_hardware_types: List[HardwareType] = []
    supported_sensor_categories: List[SensorCategory] = []


class SourceConfiguration(BaseModel):
    """Model for sensor source configuration."""
    update_interval: float = 2.0
    filter_inactive_sensors: bool = True
    hardware_filters: List[HardwareType] = []


class SourceStatistics(BaseModel):
    """Model for sensor source statistics."""
    total_sensors: int = 0
    active_sensors: int = 0
    update_count: int = 0
    error_count: int = 0
    average_update_time: float = 0.0
    data_throughput: float = 0.0
    last_error: Optional[str] = None


class SensorSource(BaseModel):
    """Sensor data source model."""

    id: str = Field(..., description="Source identifier")
    name: str = Field(..., description="Human-readable source name")
    description: Optional[str] = Field(None, description="Source description")
    version: str = Field("1.0.0", description="Source version")

    # Status
    active: bool = Field(False, description="Whether source is active")
    connection_status: str = Field("disconnected", description="Connection status")

    # Capabilities
    capabilities: SourceCapabilities = Field(default_factory=SourceCapabilities)

    # Configuration
    configuration: SourceConfiguration = Field(default_factory=SourceConfiguration)

    # Statistics
    statistics: SourceStatistics = Field(default_factory=SourceStatistics)

    # Hardware information
    hardware_components: List[Dict[str, Any]] = Field(
        default_factory=list, description="Hardware components"
    )

    # Timestamps
    last_update: Optional[datetime] = Field(None, description="Last successful update")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )

    # Error handling
    error_message: Optional[str] = Field(None, description="Last error message")
    error_count: int = Field(0, description="Total error count")

    model_config = {
        "use_enum_values": True,
        "json_encoders": {datetime: lambda v: v.isoformat()},
    }


class SensorAlert(BaseModel):
    """Sensor alert model."""

    id: str = Field(..., description="Alert identifier")
    sensor_id: str = Field(..., description="Associated sensor ID")

    # Alert configuration
    alert_type: str = Field(..., description="Type of alert")
    threshold: float = Field(..., description="Alert threshold value")
    current_value: float = Field(..., description="Current sensor value")

    # Alert details
    message: str = Field(..., description="Alert message")
    severity: str = Field("warning", description="Alert severity level")

    # Status
    active: bool = Field(True, description="Whether alert is active")
    acknowledged: bool = Field(False, description="Whether alert is acknowledged")
    auto_resolve: bool = Field(True, description="Whether alert auto-resolves")

    # Timestamps
    triggered_at: datetime = Field(
        default_factory=datetime.now, description="Alert trigger time"
    )
    acknowledged_at: Optional[datetime] = Field(None, description="Acknowledgment time")
    resolved_at: Optional[datetime] = Field(None, description="Resolution time")

    model_config = {
        "use_enum_values": True,
        "json_encoders": {datetime: lambda v: v.isoformat()},
    }


class SensorDefinition(BaseModel):
    """Static definition of a sensor."""

    sensor_id: str = Field(
        ..., description="Unique sensor identifier provided by the source"
    )
    name: str = Field(..., description="Human-readable sensor name")
    unit: str = Field("", description="Unit of measurement")
    category: SensorCategory = Field(
        SensorCategory.UNKNOWN, description="Sensor category"
    )
    hardware_type: HardwareType = Field(
        HardwareType.UNKNOWN, description="Associated hardware type"
    )
    source_id: str = Field(
        ..., description="Identifier of the sensor provider (e.g., 'lhm', 'mock')"
    )

    # Optional descriptive fields
    description: Optional[str] = Field(
        None, description="Optional detailed description of the sensor"
    )
    min_value: Optional[float] = Field(
        None, description="Typical minimum value for this sensor type"
    )
    max_value: Optional[float] = Field(
        None, description="Typical maximum value for this sensor type"
    )

    # Additional static metadata specific to the sensor
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional static sensor metadata"
    )

    # Pydantic V2 model_config (if needed, though enums and datetime are handled by default or in other models)
    # model_config = {
    #     "use_enum_values": True # Already default in Pydantic V2 for Enums
    # }

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class PerformanceMetrics(BaseModel):
    """Performance metrics model."""

    # System metrics
    cpu_usage: float = Field(0.0, ge=0, le=100, description="CPU usage percentage")
    memory_usage: float = Field(0.0, ge=0, description="Memory usage in MB")
    network_usage: float = Field(0.0, ge=0, description="Network usage in bytes/sec")

    # Application metrics
    update_latency: float = Field(
        0.0, ge=0, description="Update latency in milliseconds"
    )
    sensor_count: int = Field(0, ge=0, description="Total sensor count")
    active_sensors: int = Field(0, ge=0, description="Active sensor count")

    # Quality metrics
    update_rate: float = Field(0.0, ge=0, description="Updates per second")
    error_rate: float = Field(0.0, ge=0, le=100, description="Error rate percentage")
    data_quality_score: float = Field(
        100.0, ge=0, le=100, description="Overall data quality score"
    )

    # Queue metrics
    queue_size: int = Field(0, ge=0, description="Processing queue size")
    dropped_updates: int = Field(0, ge=0, description="Number of dropped updates")

    # Timestamps
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Metrics timestamp"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class SensorDataBatch(BaseModel):
    """Batch of sensor readings for efficient processing."""

    batch_id: str = Field(..., description="Unique batch identifier")
    source_id: str = Field(..., description="Source identifier")

    # Batch data
    sensors: Dict[str, SensorReading] = Field(
        ..., description="Sensor readings in batch"
    )

    # Batch metadata
    sequence_number: int = Field(0, description="Batch sequence number")
    total_sensors: int = Field(0, description="Total sensors in batch")

    # Timestamps
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Batch timestamp"
    )
    processing_time: Optional[float] = Field(
        None, description="Processing time in milliseconds"
    )

    @field_validator("sensors")
    def validate_sensors_not_empty(cls, v):
        """Validate that sensors dictionary is not empty."""
        if not v:
            raise ValueError("Sensor batch cannot be empty")
        return v

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
