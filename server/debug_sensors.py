#!/usr/bin/env python3

"""
Debug script to test sensor initialization directly
"""

import asyncio
import sys
import os
from app.core.config import get_settings
from app.sensors.mock_sensor import MockSensor


# Add the server directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def test_mock_sensor():
    """Test MockSensor initialization"""
    print("=== Testing MockSensor ===")

    mock = MockSensor()
    settings = get_settings()

    try:
        print(f"MockSensor source_id: {mock.source_id}")
        print(f"MockSensor display_name: {mock.display_name}")
        print(f"Initial is_active: {mock.is_active}")

        # Initialize
        result = await mock.initialize(settings)
        print(f"Initialize result: {result}")
        print(f"After init is_active: {mock.is_active}")

        # Check availability
        available = await mock.is_available()
        print(f"Is available: {available}")

        # Get sensor definitions
        definitions = await mock.get_available_sensors()
        print(f"Number of sensor definitions: {len(definitions)}")

        for i, sensor_def in enumerate(definitions):
            print(
                f"  Sensor {i+1}: {sensor_def.sensor_id} - "
                f"{sensor_def.name} ({sensor_def.category.value})"
            )

        # Get current data
        readings = await mock.get_current_data()
        print(f"Number of current readings: {len(readings)}")

        for i, reading in enumerate(readings):
            print(
                f"  Reading {i+1}: {reading.sensor_id} = "
                f"{reading.value} {reading.unit}"
            )

        # Clean up
        await mock.close()
        print("MockSensor closed successfully")

    except Exception as e:
        print(f"Error testing MockSensor: {e}")
        import traceback

        traceback.print_exc()


async def main():
    """Main test function"""
    print("Starting sensor debug tests...\n")

    await test_mock_sensor()

    print("\nDebug tests completed.")


if __name__ == "__main__":
    asyncio.run(main())
