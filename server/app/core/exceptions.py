"""
Custom exception classes for the application.
Provides structured error handling and HTTP status mapping.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base exception for Ultimate Sensor Monitor."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ):
        self.message = message
        self.details = details or {}
        self.error_code = error_code
        super().__init__(self.message)


class SensorException(AppError):
    """Exception related to sensor operations."""

    pass


class ConfigurationException(AppError):
    """Exception related to configuration issues."""

    pass


class ValidationException(AppError):
    """Exception related to data validation."""

    pass


class WebSocketException(AppError):
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


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Global handler for AppError exceptions."""
    # Try to get a specific status code from the exception, default to 500
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.error_code or "application_error",
            "message": exc.message,
            "details": exc.details,
        },
    )
