import asyncio
import logging
import subprocess
import sys
import os
from typing import List, Dict, Any, Optional, Type

from app.core.config import AppSettings
from app.core.logging import get_logger
from app.models.sensor import SensorDefinition, SensorReading
from app.sensors.base import BaseSensor

# Import only the mock sensor and base sensor - use dynamic imports for hardware sensors
from app.sensors.mock_sensor import MockSensor

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

    def _test_hardware_monitor_availability(self) -> bool:
        """Test if HardwareMonitor package is fully functional using subprocess isolation."""
        try:
            test_script = """
import sys
try:
    import HardwareMonitor
    from HardwareMonitor.Util import OpenComputer
    
    computer = OpenComputer(cpu=True, gpu=True, memory=True, storage=True, motherboard=True)
    if computer:
        computer.Update()
        hardware_list = list(computer.Hardware)
        print(f"SUCCESS:{len(hardware_list)}")
        for hw in hardware_list[:3]:
            print(f"HARDWARE:{hw.Name}")
    else:
        print("FAILED:Computer creation returned None")
except Exception as e:
    print(f"FAILED:{e}")
"""

            result = subprocess.run(
                [sys.executable, "-c", test_script],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if line.startswith("SUCCESS:"):
                        count = int(line.split(":")[1])
                        logger.info(
                            f"✅ HardwareMonitor package is fully functional (found {count} hardware components)"
                        )
                        return count > 0
                    elif line.startswith("HARDWARE:"):
                        hw_name = line.split(":", 1)[1]
                        logger.debug(f"   • {hw_name}")
                    elif line.startswith("FAILED:"):
                        error = line.split(":", 1)[1]
                        logger.warning(f"❌ HardwareMonitor failed: {error}")
                        return False
            else:
                logger.warning(
                    f"❌ HardwareMonitor process failed with return code {result.returncode}"
                )
                if result.stderr:
                    logger.debug(f"   Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.warning("❌ HardwareMonitor test timed out")
            return False
        except Exception as e:
            logger.info(f"❌ HardwareMonitor package not available: {e}")
            return False

    def _import_sensor_class(self, sensor_type: str):
        """Dynamically import sensor classes to avoid DLL conflicts."""
        if sensor_type == "HWSensor":
            from app.sensors.hw_sensor import HWSensor

            return HWSensor
        elif sensor_type == "MockSensor":
            return MockSensor
        else:
            raise ValueError(f"Unknown sensor type: {sensor_type}")

    async def initialize(self) -> None:
        """Discover, instantiate, and initialize all configured sensor providers."""
        if self._initialized:
            logger.warning("SensorManager already initialized.")
            return

        logger.info("Initializing SensorManager...")
        logger.info("🔍 Testing hardware sensor availability in an isolated process...")

        hw_sensor_available = self._test_hardware_monitor_availability()

        sensor_types: List[str] = []

        if hw_sensor_available:
            logger.info("✅ HardwareMonitor is available. Prioritizing it.")
            sensor_types = ["HWSensor", "MockSensor"]
        else:
            logger.warning("❌ HardwareMonitor is not available.")
            logger.warning("   Using MockSensor only - no real hardware monitoring.")
            sensor_types = ["MockSensor"]

        logger.info(f"📋 Selected sensor initialization order:")
        for i, sensor_type in enumerate(sensor_types, 1):
            logger.info(f"  {i}. {sensor_type}")

        successful_providers = 0
        failed_providers = []

        for sensor_type in sensor_types:
            logger.info(f"🔄 Attempting to initialize: {sensor_type}")

            try:
                # Dynamically import the sensor class to avoid conflicts
                # This import only happens AFTER we've decided which sensor to use
                sensor_cls = self._import_sensor_class(sensor_type)
                provider_instance = sensor_cls()
                provider_name = getattr(
                    provider_instance, "display_name", sensor_cls.__name__
                )

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
                    logger.info(
                        f"   📊 Found {sensor_count} sensors from {provider_name}"
                    )

                    for definition in definitions:
                        self._active_sensors[definition.sensor_id] = definition
                        logger.debug(
                            f"      • {definition.name} ({definition.category})"
                        )

                    # If we successfully loaded a hardware sensor, skip MockSensor
                    if sensor_type == "HWSensor":
                        logger.info(
                            f"   🎯 Successfully initialized hardware sensor, skipping remaining sensors"
                        )
                        break
                else:
                    logger.warning(
                        f"❌ UNAVAILABLE: {provider_name} initialized but is not available"
                    )
                    failed_providers.append(f"{provider_name} (unavailable)")
                    await provider_instance.close()  # Clean up if not available

            except Exception as e:
                logger.error(f"💥 FAILED: {sensor_type} initialization failed: {e}")
                failed_providers.append(f"{sensor_type} (error: {str(e)[:50]}...)")
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
            logger.error(
                "🚨 CRITICAL: No sensor providers were successfully initialized!"
            )
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
                await self._collect_data_once()

                # Use configured poll interval or default to 5 seconds
                poll_interval = getattr(
                    self.settings, "sensor_poll_interval_seconds", 5
                )
                await asyncio.sleep(poll_interval)
            except asyncio.CancelledError:
                logger.info("Sensor data collector task cancelled.")
                break
            except Exception as e:
                logger.error(f"Error in sensor data collector task: {e}", exc_info=True)
                await asyncio.sleep(10)  # Wait longer after an error

    async def _collect_data_once(self) -> None:
        """Performs a single round of data collection from all active providers."""
        for provider in self.sensor_providers:
            try:
                if await provider.is_available():
                    readings = await provider.get_current_data()
                    self._sensor_readings[provider.source_id] = readings
                    logger.debug(
                        f"Collected {len(readings)} readings from {provider.display_name}"
                    )
            except Exception as e:
                logger.error(
                    f"Failed to collect data from {provider.display_name}: {e}",
                    exc_info=True,
                )

    async def get_all_sensor_data(self) -> Dict[str, List[SensorReading]]:
        """Return all current sensor readings, aggregated from providers."""
        # If readings are empty on first call, perform an immediate collection
        if not self._sensor_readings:
            logger.info("Initial sensor data request; performing immediate collection.")
            await self._collect_data_once()
        return self._sensor_readings

    async def get_sensor_definitions(self) -> List[SensorDefinition]:
        """Return definitions of all active sensors."""
        return list(self._active_sensors.values())

    def get_available_sources(self) -> List[Dict[str, Any]]:
        """Return status information for all discovered sensor providers."""
        sources = []
        for provider in self.sensor_providers:
            # This is a synchronous method now, so we can't await is_available.
            # We will rely on the initialized state.
            # A better implementation would have availability checked periodically.
            sources.append(
                {
                    "name": provider.display_name,
                    "source_id": provider.source_id,
                    "available": True,  # Assumed available if it's in the list
                    "sensor_count": len(self._active_sensors)
                    # This is not ideal as it returns total sensors, not per provider
                    # A proper implementation would map sensors to providers.
                }
            )
        return sources

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
                logger.error(
                    f"Error during collector task shutdown: {e}", exc_info=True
                )

        for provider in self.sensor_providers:
            try:
                await provider.close()
                logger.info(f"Sensor provider {provider.display_name} closed.")
            except Exception as e:
                logger.error(
                    f"Error closing sensor provider {provider.display_name}: {e}",
                    exc_info=True,
                )

        self.sensor_providers.clear()
        self._active_sensors.clear()
        self._sensor_readings.clear()
        self._initialized = False
        logger.info("SensorManager shut down complete.")
