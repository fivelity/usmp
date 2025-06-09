"""
Production logging configuration.
Structured logging with proper levels and formatting.
"""

import logging
import sys
from typing import Dict, Any
from .config import get_settings


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for development."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        settings = get_settings()
        if not settings.debug_mode:
            return super().format(record)
            
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Add color to levelname
        record.levelname = f"{color}{record.levelname}{reset}"
        
        return super().format(record)


def setup_logging() -> None:
    """Configure application logging."""
    settings = get_settings()
    
    # Set log level
    log_level = logging.INFO  # Default log level
    
    # Create formatter
    if settings.debug_mode:
        formatter = ColoredFormatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%H:%M:%S"
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
