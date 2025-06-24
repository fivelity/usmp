"""
Production logging configuration.
Structured logging with proper levels and formatting.
"""

import logging
import logging.config
import sys
from typing import Dict, Any

import structlog
from structlog.types import Processor

from .config import get_settings

# --- Structlog Processors ---
# Processors are functions that process log records. They are chained together.


def add_log_level_as_str(
    logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add the log level to the event dict.
    """
    event_dict["level"] = method_name.upper()
    return event_dict


def add_logger_name(
    logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add the logger name to the event dict.
    """
    event_dict["name"] = logger.name
    return event_dict


# --- Logging Configuration ---


def setup_logging():
    """
    Configure structured logging for the entire application.

    This setup uses `structlog` to provide context-rich, structured logging
    that can be rendered as colored text in development or as JSON in production.
    """
    settings = get_settings()
    log_level = settings.log_level.upper()

    # Shared processors for all loggers
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    # Processors for development (human-readable) vs production (machine-readable)
    if settings.debug_mode:
        processors: list[Processor] = shared_processors + [
            structlog.dev.set_exc_info,
            structlog.dev.ConsoleRenderer(
                colors=True, exception_formatter=structlog.dev.plain_traceback
            ),
        ]
    else:
        processors: list[Processor] = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    # Configure the standard logging library to be a sink for structlog
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "structlog.stdlib.ProcessorFormatter",
                    "processor": structlog.processors.JSONRenderer()
                    if not settings.debug_mode
                    else structlog.dev.ConsoleRenderer(colors=False),
                    "foreign_pre_chain": shared_processors,
                },
            },
            "handlers": {
                "default": {
                    "level": log_level,
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": log_level,
                    "propagate": True,
                },
                # Silence noisy third-party loggers
                "uvicorn.error": {
                    "level": "INFO",
                },
                "uvicorn.access": {
                    "level": "WARNING",
                },
                "websockets": {
                    "level": "WARNING",
                },
            },
        }
    )

    # Configure structlog itself
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    log = get_logger("core.logging")
    log.info(
        "Logging configured",
        log_level=log_level,
        debug_mode=settings.debug_mode,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Get a pre-configured structlog logger.

    Args:
        name: The name for the logger, typically __name__.

    Returns:
        A structlog logger instance.
    """
    return structlog.get_logger(name)


def get_logger_for_module(name: str) -> logging.Logger:
    """Get a logger instance for a module."""
    return logging.getLogger(f"ultimon.{name}")
