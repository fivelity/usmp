"""
Custom exception classes for the application.
Provides structured error handling and HTTP status mapping.
"""

from typing import Any, Dict, Optional
from fastapi import status, Request
from fastapi.responses import JSONResponse
import structlog

log = structlog.get_logger(__name__)


class AppError(Exception):
    """Base exception for Ultimate Sensor Monitor."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "application_error"

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        status_code: Optional[int] = None,
    ):
        self.message = message
        self.details = details or {}
        if error_code:
            self.error_code = error_code
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.error_code}]: {self.message}"


class NotFoundException(AppError):
    """Resource not found."""

    status_code = status.HTTP_404_NOT_FOUND
    error_code = "resource_not_found"


class SensorException(AppError):
    """Exception related to sensor operations."""

    error_code = "sensor_error"


class ConfigurationException(AppError):
    """Exception related to configuration issues."""

    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "configuration_error"


class ValidationException(AppError):
    """Exception related to data validation."""

    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "validation_error"


class WebSocketException(AppError):
    """Exception related to WebSocket operations."""

    error_code = "websocket_error"


# HTTP Exception mappings
def sensor_not_found(sensor_id: str) -> HTTPException:
    """Sensor not found HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "sensor_not_found",
            "message": f"Sensor with ID '{sensor_id}' not found",
            "sensor_id": sensor_id,
        },
    )


def invalid_configuration(message: str) -> HTTPException:
    """Invalid configuration HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "invalid_configuration", "message": message},
    )


def service_unavailable(service: str) -> HTTPException:
    """Service unavailable HTTP exception."""
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "error": "service_unavailable",
            "message": f"Service '{service}' is currently unavailable",
        },
    )


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    """Global handler for AppError exceptions to log and return a standard response."""
    log.error(
        exc.message,
        details=exc.details,
        error_code=exc.error_code,
        status_code=exc.status_code,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )
