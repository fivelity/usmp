#!/usr/bin/env python3
"""
Final test script for the resolved DLL conflict in sensor manager.
"""

import sys
import os
import asyncio

# Add project root to path to allow importing 'app'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


async def test_final_sensor_manager():
    """Test the final sensor manager with DLL conflict resolution."""
    print("🚀 Final Sensor Manager Test")
    print("=" * 50)

    # Import here to avoid any early DLL loading
    from app.services.sensor_manager import SensorManager
    from app.core.config import AppSettings

    settings = AppSettings()
    manager = SensorManager(settings)

    print("🔧 Initializing sensor manager...")
    await manager.initialize()

    print("\n📊 Getting sensor data...")
    await asyncio.sleep(2)  # Give it time to collect some data

    data = await manager.get_all_sensor_data()
    definitions = await manager.get_sensor_definitions()

    print("\n🎯 RESULTS:")
    print(f"   Active providers: {len(manager.sensor_providers)}")
    print(f"   Total sensors: {len(definitions)}")
    print(f"   Data sources: {list(data.keys())}")

    if manager.sensor_providers:
        for provider in manager.sensor_providers:
            print(f"   • {provider.display_name} ({provider.source_id})")

    # Show sample sensor data
    for source, readings in data.items():
        print(f"\n📡 {source} ({len(readings)} readings):")
        for reading in readings[:5]:  # Show first 5
            print(f"      {reading.name}: {reading.value} {reading.unit}")

    # Check if we have real hardware sensors
    hardware_sources = [
        source for source in data.keys() if source not in ["MockSensor", "mock"]
    ]
    if hardware_sources:
        print("\n✅ SUCCESS: Real hardware sensors are working!")
        print(f"   Hardware sources: {hardware_sources}")
    else:
        print("\n⚠️  Only mock sensors detected")

    await manager.shutdown()
    print("\n✅ Test completed successfully")


if __name__ == "__main__":
    asyncio.run(test_final_sensor_manager())
