"""
Sensor data models with comprehensive validation.
Production-ready Pydantic models for type safety and validation.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


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
    FAN = "fan"
    FLOW = "flow"
    CONTROL = "control"
    LEVEL = "level"
    FACTOR = "factor"
    DATA = "data"
    THROUGHPUT = "throughput"
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
    UNKNOWN = "unknown"


class DataQuality(str, Enum):
    """Data quality enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNKNOWN = "unknown"


class SensorReading(BaseModel):
    """Individual sensor reading model."""
    
    id: str = Field(..., description="Unique sensor identifier")
    name: str = Field(..., description="Human-readable sensor name")
    value: Union[float, int] = Field(..., description="Current sensor value")
    unit: str = Field("", description="Unit of measurement")
    
    # Optional range information
    min_value: Optional[float] = Field(None, description="Minimum expected value")
    max_value: Optional[float] = Field(None, description="Maximum expected value")
    
    # Classification
    category: SensorCategory = Field(SensorCategory.UNKNOWN, description="Sensor category")
    hardware_type: HardwareType = Field(HardwareType.UNKNOWN, description="Hardware type")
    
    # Hierarchy and source
    source: str = Field(..., description="Data source identifier")
    parent_hardware: Optional[str] = Field(None, description="Parent hardware path")
    
    # Status and quality
    status: SensorStatus = Field(SensorStatus.ACTIVE, description="Sensor status")
    quality: DataQuality = Field(DataQuality.GOOD, description="Data quality assessment")
    
    # Timestamps
    timestamp: datetime = Field(default_factory=datetime.now, description="Reading timestamp")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    
    # Additional metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional sensor metadata")
    
    @validator("value")
    def validate_value(cls, v):
        """Validate sensor value is numeric."""
        if not isinstance(v, (int, float)):
            raise ValueError("Sensor value must be numeric")
        return v
    
    @validator("name")
    def validate_name(cls, v):
        """Validate sensor name is not empty."""
        if not v or not v.strip():
            raise ValueError("Sensor name cannot be empty")
        return v.strip()
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


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
    capabilities: Dict[str, Any] = Field(default_factory=dict, description="Source capabilities")
    
    # Configuration
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Source configuration")
    
    # Statistics
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Source statistics")
    
    # Hardware information
    hardware_components: List[Dict[str, Any]] = Field(default_factory=list, description="Hardware components")
    
    # Timestamps
    last_update: Optional[datetime] = Field(None, description="Last successful update")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    
    # Error handling
    error_message: Optional[str] = Field(None, description="Last error message")
    error_count: int = Field(0, description="Total error count")
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
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
    triggered_at: datetime = Field(default_factory=datetime.now, description="Alert trigger time")
    acknowledged_at: Optional[datetime] = Field(None, description="Acknowledgment time")
    resolved_at: Optional[datetime] = Field(None, description="Resolution time")
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PerformanceMetrics(BaseModel):
    """Performance metrics model."""
    
    # System metrics
    cpu_usage: float = Field(0.0, ge=0, le=100, description="CPU usage percentage")
    memory_usage: float = Field(0.0, ge=0, description="Memory usage in MB")
    network_usage: float = Field(0.0, ge=0, description="Network usage in bytes/sec")
    
    # Application metrics
    update_latency: float = Field(0.0, ge=0, description="Update latency in milliseconds")
    sensor_count: int = Field(0, ge=0, description="Total sensor count")
    active_sensors: int = Field(0, ge=0, description="Active sensor count")
    
    # Quality metrics
    update_rate: float = Field(0.0, ge=0, description="Updates per second")
    error_rate: float = Field(0.0, ge=0, le=100, description="Error rate percentage")
    data_quality_score: float = Field(100.0, ge=0, le=100, description="Overall data quality score")
    
    # Queue metrics
    queue_size: int = Field(0, ge=0, description="Processing queue size")
    dropped_updates: int = Field(0, ge=0, description="Number of dropped updates")
    
    # Timestamps
    timestamp: datetime = Field(default_factory=datetime.now, description="Metrics timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SensorDataBatch(BaseModel):
    """Batch of sensor readings for efficient processing."""
    
    batch_id: str = Field(..., description="Unique batch identifier")
    source_id: str = Field(..., description="Source identifier")
    
    # Batch data
    sensors: Dict[str, SensorReading] = Field(..., description="Sensor readings in batch")
    
    # Batch metadata
    sequence_number: int = Field(0, description="Batch sequence number")
    total_sensors: int = Field(0, description="Total sensors in batch")
    
    # Timestamps
    timestamp: datetime = Field(default_factory=datetime.now, description="Batch timestamp")
    processing_time: Optional[float] = Field(None, description="Processing time in milliseconds")
    
    @validator("sensors")
    def validate_sensors_not_empty(cls, v):
        """Validate that sensors dictionary is not empty."""
        if not v:
            raise ValueError("Sensor batch cannot be empty")
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
