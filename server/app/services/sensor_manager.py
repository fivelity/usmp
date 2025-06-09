import asyncio
import logging
from typing import List, Dict, Any, Optional, Type

from app.core.config import AppSettings
from app.core.logging import get_logger
from app.models.sensor import SensorDefinition, SensorReading
from app.sensors.base import BaseSensor
# Import available sensor providers in priority order
from app.sensors.hw_sensor import HWSensor
from app.sensors.lhm_sensor import LHMSensor
from app.sensors.mock_sensor import MockSensor
# from app.sensors.hwinfo_sensor import HWiNFOSensor  # TODO: Implement properly

logger = get_logger("sensor_manager")

class SensorManager:
    """Manages all sensor providers, collects and caches data."""

    def __init__(self, settings: AppSettings):
        self.settings: AppSettings = settings
        self.sensor_providers: List[BaseSensor] = []
        self._active_sensors: Dict[str, SensorDefinition] = {}
        self._sensor_readings: Dict[str, List[SensorReading]] = {}
        self._collector_task: Optional[asyncio.Task] = None
        self._initialized: bool = False

    async def initialize(self) -> None:
        """Discover, instantiate, and initialize all configured sensor providers."""
        if self._initialized:
            logger.warning("SensorManager already initialized.")
            return

        logger.info("Initializing SensorManager...")
        
        # Sensor classes in priority order: HW -> LHM -> Mock
        sensor_classes: List[Type[BaseSensor]] = [
            HWSensor,        # Primary: HardwareMonitor Python package
            LHMSensor,       # Fallback: LibreHardwareMonitor.dll
            MockSensor,      # Final fallback: Mock data
            # HWiNFOSensor   # TODO: Implement HWiNFOSensor properly
        ]

        logger.info(f"Attempting to initialize {len(sensor_classes)} sensor providers in priority order:")
        for i, sensor_cls in enumerate(sensor_classes, 1):
            logger.info(f"  {i}. {sensor_cls.__name__} - {getattr(sensor_cls, 'display_name', 'Unknown')}")

        successful_providers = 0
        failed_providers = []

        for sensor_cls in sensor_classes:
            provider_name = getattr(sensor_cls, 'display_name', sensor_cls.__name__)
            logger.info(f"🔄 Attempting to initialize: {provider_name}")
            
            try:
                provider_instance = sensor_cls()
                
                # Initialize the sensor provider with settings
                logger.debug(f"   📋 Calling initialize() for {provider_name}")
                await provider_instance.initialize(self.settings)
                
                # Check if the sensor is available
                logger.debug(f"   🔍 Checking availability for {provider_name}")
                if await provider_instance.is_available():
                    logger.info(f"✅ SUCCESS: {provider_name} is available and working!")
                    self.sensor_providers.append(provider_instance)
                    successful_providers += 1
                    
                    # Store available sensors from this provider
                    definitions = await provider_instance.get_available_sensors()
                    sensor_count = len(definitions)
                    logger.info(f"   📊 Found {sensor_count} sensors from {provider_name}")
                    
                    for definition in definitions:
                        self._active_sensors[definition.sensor_id] = definition
                        logger.debug(f"      • {definition.name} ({definition.category})")
                else:
                    logger.warning(f"❌ UNAVAILABLE: {provider_name} initialized but is not available")
                    failed_providers.append(f"{provider_name} (unavailable)")
                    await provider_instance.close()  # Clean up if not available
                    
            except Exception as e:
                logger.error(f"💥 FAILED: {provider_name} initialization failed: {e}")
                failed_providers.append(f"{provider_name} (error: {str(e)[:50]}...)")
                logger.debug(f"   Full error details:", exc_info=True)

        # Summary of initialization results
        logger.info("=" * 60)
        logger.info(f"📈 SENSOR INITIALIZATION SUMMARY:")
        logger.info(f"   ✅ Successful providers: {successful_providers}")
        logger.info(f"   ❌ Failed providers: {len(failed_providers)}")
        logger.info(f"   📊 Total active sensors: {len(self._active_sensors)}")
        
        if failed_providers:
            logger.info(f"   💔 Failed providers:")
            for failed in failed_providers:
                logger.info(f"      • {failed}")
        
        if successful_providers > 0:
            logger.info(f"   🎯 Active providers:")
            for provider in self.sensor_providers:
                logger.info(f"      • {provider.display_name} ({provider.source_id})")
        
        if not self.sensor_providers:
            logger.error("🚨 CRITICAL: No sensor providers were successfully initialized!")
            logger.error("   The system will not provide any sensor data.")
        else:
            # Start the data collection task
            self._collector_task = asyncio.create_task(self._run_collector_task())
            logger.info(f"🚀 SensorManager initialized successfully!")
            
        logger.info("=" * 60)
        self._initialized = True

    async def _run_collector_task(self) -> None:
        """Periodically collects data from all active sensor providers."""
        logger.info("Sensor data collector task started.")
        while self._initialized:
            try:
                for provider in self.sensor_providers:
                    if await provider.is_available():
                        readings = await provider.get_current_data()
                        self._sensor_readings[provider.source_id] = readings
                        logger.debug(f"Collected {len(readings)} readings from {provider.display_name}")
                
                # Use configured poll interval or default to 5 seconds
                poll_interval = getattr(self.settings, 'sensor_poll_interval_seconds', 5)
                await asyncio.sleep(poll_interval)
            except asyncio.CancelledError:
                logger.info("Sensor data collector task cancelled.")
                break
            except Exception as e:
                logger.error(f"Error in sensor data collector task: {e}", exc_info=True)
                await asyncio.sleep(10) # Wait longer after an error

    async def get_all_sensor_data(self) -> Dict[str, List[SensorReading]]:
        """Return all current sensor readings, aggregated from providers."""
        # TODO: Implement proper data aggregation and caching
        return self._sensor_readings

    async def get_sensor_definitions(self) -> List[SensorDefinition]:
        """Return definitions of all active sensors."""
        return list(self._active_sensors.values())

    async def shutdown(self) -> None:
        """Gracefully shut down all sensor providers and stop tasks."""
        if not self._initialized:
            return
            
        logger.info("Shutting down SensorManager...")
        if self._collector_task:
            self._collector_task.cancel()
            try:
                await self._collector_task
            except asyncio.CancelledError:
                logger.info("Collector task successfully cancelled.")
            except Exception as e:
                logger.error(f"Error during collector task shutdown: {e}", exc_info=True)
        
        for provider in self.sensor_providers:
            try:
                await provider.close()
                logger.info(f"Sensor provider {provider.display_name} closed.")
            except Exception as e:
                logger.error(f"Error closing sensor provider {provider.display_name}: {e}", exc_info=True)
        
        self.sensor_providers.clear()
        self._active_sensors.clear()
        self._sensor_readings.clear()
        self._initialized = False
        logger.info("SensorManager shut down complete.")
