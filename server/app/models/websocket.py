"""
WebSocket message models for real-time communication.
Type-safe models for WebSocket message handling.
"""

from datetime import datetime
from typing import Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """WebSocket message type enumeration."""
    
    # Connection messages
    CONNECTION_ESTABLISHED = "connection_established"
    CONNECTION_CLOSED = "connection_closed"
    HEARTBEAT = "heartbeat"
    HEARTBEAT_RESPONSE = "heartbeat_response"
    
    # Sensor data messages
    SENSOR_DATA = "sensor_data"
    SENSOR_UPDATE = "sensor_update"
    SENSOR_SOURCES_UPDATED = "sensor_sources_updated"
    HARDWARE_CHANGE = "hardware_change"
    
    # Configuration messages
    CONFIGURE_REALTIME = "configure_realtime"
    CONFIGURATION_UPDATED = "configuration_updated"
    
    # System messages
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    STATUS_UPDATE = "status_update"
    
    # Widget messages
    WIDGET_UPDATE = "widget_update"
    WIDGET_CREATED = "widget_created"
    WIDGET_DELETED = "widget_deleted"


class WebSocketMessage(BaseModel):
    """Base WebSocket message model."""
    
    type: MessageType = Field(..., description="Message type")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    message_id: Optional[str] = Field(None, description="Unique message identifier")
    
    # Message content
    data: Optional[Dict[str, Any]] = Field(None, description="Message data payload")
    content: Optional[Dict[str, Any]] = Field(None, description="Message content")
    message: Optional[str] = Field(None, description="Text message")
    
    # Source information
    source_id: Optional[str] = Field(None, description="Source identifier")
    client_id: Optional[str] = Field(None, description="Client identifier")
    
    # Error information
    error: Optional[str] = Field(None, description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    
    # Sequence information
    sequence_number: Optional[int] = Field(None, description="Message sequence number")
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SensorDataMessage(WebSocketMessage):
    """Sensor data WebSocket message."""
    
    type: MessageType = Field(MessageType.SENSOR_DATA, description="Message type")
    data: Dict[str, Any] = Field(..., description="Sensor data payload")
    
    # Performance metrics
    performance: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")
    
    # Data quality information
    quality_score: Optional[float] = Field(None, ge=0, le=100, description="Data quality score")
    total_sensors: Optional[int] = Field(None, ge=0, description="Total sensor count")


class ConfigurationMessage(WebSocketMessage):
    """Configuration update WebSocket message."""
    
    type: MessageType = Field(MessageType.CONFIGURE_REALTIME, description="Message type")
    config: Dict[str, Any] = Field(..., description="Configuration data")
    
    # Configuration metadata
    config_version: Optional[str] = Field(None, description="Configuration version")
    applied_at: Optional[datetime] = Field(None, description="Configuration application time")


class ErrorMessage(WebSocketMessage):
    """Error WebSocket message."""
    
    type: MessageType = Field(MessageType.ERROR, description="Message type")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    
    # Error details
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    severity: str = Field("error", description="Error severity level")
    recoverable: bool = Field(True, description="Whether error is recoverable")


class HeartbeatMessage(WebSocketMessage):
    """Heartbeat WebSocket message."""
    
    type: MessageType = Field(MessageType.HEARTBEAT, description="Message type")
    
    # System status
    system_status: Optional[Dict[str, Any]] = Field(None, description="System status information")
    uptime: Optional[float] = Field(None, description="System uptime in seconds")
    
    # Connection metrics
    connection_count: Optional[int] = Field(None, ge=0, description="Active connection count")
    message_count: Optional[int] = Field(None, ge=0, description="Total message count")


class StatusUpdateMessage(WebSocketMessage):
    """Status update WebSocket message."""
    
    type: MessageType = Field(MessageType.STATUS_UPDATE, description="Message type")
    status: str = Field(..., description="Status value")
    
    # Status details
    component: Optional[str] = Field(None, description="Component name")
    previous_status: Optional[str] = Field(None, description="Previous status")
    status_details: Optional[Dict[str, Any]] = Field(None, description="Status details")


# Message type mapping for deserialization
MESSAGE_TYPE_MAP = {
    MessageType.SENSOR_DATA: SensorDataMessage,
    MessageType.CONFIGURE_REALTIME: ConfigurationMessage,
    MessageType.ERROR: ErrorMessage,
    MessageType.HEARTBEAT: HeartbeatMessage,
    MessageType.HEARTBEAT_RESPONSE: HeartbeatMessage,
    MessageType.STATUS_UPDATE: StatusUpdateMessage,
}


def parse_websocket_message(data: dict) -> WebSocketMessage:
    """Parse WebSocket message data into appropriate model."""
    message_type = data.get("type")
    
    if not message_type:
        raise ValueError("Message type is required")
    
    try:
        message_type_enum = MessageType(message_type)
    except ValueError:
        raise ValueError(f"Unknown message type: {message_type}")
    
    # Get appropriate model class
    model_class = MESSAGE_TYPE_MAP.get(message_type_enum, WebSocketMessage)
    
    return model_class(**data)
