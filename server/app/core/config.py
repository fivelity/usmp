from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "Ultimate Sensor Monitor"
    api_v1_str: str = "/api/v1"
    server_host: str = "0.0.0.0"
    server_port: int = 8100
    debug_mode: bool = True
    # Default Svelte dev port, and common alternatives. Adjust as needed.
    backend_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"

    # LibreHardwareMonitor (LHM) sensor configuration
    lhm_enable_cpu: bool = True
    lhm_enable_gpu: bool = True
    lhm_enable_memory: bool = True
    lhm_enable_motherboard: bool = True
    lhm_enable_storage: bool = True
    lhm_enable_network: bool = True
    lhm_enable_controller: bool = True
    lhm_update_interval: int = 2000  # milliseconds
    lhm_include_null_sensors: bool = False
    lhm_float_precision: int = 2

    # General sensor configuration
    sensor_poll_interval_seconds: int = 5  # How often to poll sensors
    sensor_update_interval: int = 2  # Sensor update interval in seconds

    # Pydantic settings configuration
    # Reads from .env file, uses ULTIMON_ prefix for environment variables
    model_config = SettingsConfigDict(
        env_prefix="ULTIMON_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra fields from .env rather than raising an error
    )


@lru_cache()
def get_settings() -> AppSettings:
    """
    Returns the application settings.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return AppSettings()
