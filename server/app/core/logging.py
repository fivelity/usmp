"""
Production logging configuration.
Structured logging with proper levels and formatting.
"""

import logging
import sys
import os
import json
from logging.handlers import RotatingFileHandler
from typing import Dict, Any
from .config import get_settings


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for development."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        settings = get_settings()
        if not settings.debug_mode:
            return super().format(record)

        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Add color to levelname
        record.levelname = f"{color}{record.levelname}{reset}"

        return super().format(record)


class JsonFormatter(logging.Formatter):
    """Simple JSON log formatter for file output."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        log_record: Dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)  # type: ignore[arg-type]
        return json.dumps(log_record, ensure_ascii=False)


def setup_logging() -> None:
    """Configure application logging."""
    settings = get_settings()

    # Set log level
    log_level = logging.INFO  # Default log level

    # Create formatter
    if settings.debug_mode:
        formatter = ColoredFormatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (rotating JSON logs)
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    file_path = os.path.join(logs_dir, "app.jsonl")
    file_handler = RotatingFileHandler(file_path, maxBytes=2 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(file_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)

    # Application logger
    app_logger = logging.getLogger("ultimon")
    app_logger.setLevel(log_level)

    return app_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module."""
    return logging.getLogger(f"ultimon.{name}")
