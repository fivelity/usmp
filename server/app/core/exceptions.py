"""
Custom exception classes for the application.
Provides structured error handling and HTTP status mapping.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class UltimonException(Exception):
    """Base exception for Ultimate Sensor Monitor."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.details = details or {}
        self.error_code = error_code
        super().__init__(self.message)


class SensorException(UltimonException):
    """Exception related to sensor operations."""
    pass


class ConfigurationException(UltimonException):
    """Exception related to configuration issues."""
    pass


class ValidationException(UltimonException):
    """Exception related to data validation."""
    pass


class WebSocketException(UltimonException):
    """Exception related to WebSocket operations."""
    pass


# HTTP Exception mappings
def sensor_not_found(sensor_id: str) -> HTTPException:
    """Sensor not found HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "sensor_not_found",
            "message": f"Sensor with ID '{sensor_id}' not found",
            "sensor_id": sensor_id
        }
    )


def invalid_configuration(message: str) -> HTTPException:
    """Invalid configuration HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "invalid_configuration",
            "message": message
        }
    )


def service_unavailable(service: str) -> HTTPException:
    """Service unavailable HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "error": "service_unavailable",
            "message": f"Service '{service}' is currently unavailable"
        }
    )
