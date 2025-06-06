"""
Production-grade configuration management.
Centralized settings with environment variable support and validation.
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application metadata
    app_name: str = "Ultimate Sensor Monitor"
    app_version: str = "2.0.0"
    app_description: str = "Professional hardware sensor monitoring system"
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8100
    debug: bool = False
    reload: bool = False
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # CORS configuration
    cors_origins: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:4173",  # Vite preview
        "http://localhost:5501",  # Custom dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
        "http://127.0.0.1:5501",
    ]
    
    # Database settings (for future expansion)
    database_url: Optional[str] = None
    
    # Sensor configuration
    sensor_update_interval: float = 2.0
    max_sensor_history: int = 1000
    enable_mock_sensors: bool = True
    enable_hardware_sensors: bool = True
    
    # WebSocket settings
    websocket_heartbeat_interval: int = 30
    max_websocket_connections: int = 100
    
    # File storage
    data_directory: str = "data"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance settings
    worker_processes: int = 1
    max_request_size: int = 16 * 1024 * 1024  # 16MB
    
    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from environment variable."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("data_directory")
    def create_data_directory(cls, v):
        """Ensure data directory exists."""
        os.makedirs(v, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        env_prefix = "ULTIMON_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Global settings instance
settings = get_settings()
