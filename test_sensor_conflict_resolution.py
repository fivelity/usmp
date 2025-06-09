#!/usr/bin/env python3
"""
Test script to verify DLL conflict resolution between HWSensor and LHMSensor.
"""

import sys
import os
import asyncio

# Add server directory to path
server_dir = os.path.join(os.path.dirname(__file__), 'server')
sys.path.insert(0, server_dir)

from app.services.sensor_manager import SensorManager
from app.core.config import AppSettings

async def test_sensor_conflict_resolution():
    """Test the improved sensor manager conflict resolution."""
    print("🔍 Testing DLL Conflict Resolution")
    print("=" * 50)
    
    settings = AppSettings()
    manager = SensorManager(settings)
    
    # Initialize the sensor manager
    await manager.initialize()
    
    # Get sensor data
    print("\n📊 SENSOR DATA SUMMARY")
    print("-" * 30)
    
    data = await manager.get_all_sensor_data()
    total_sensors = 0
    
    for source, readings in data.items():
        print(f"Source: {source}")
        print(f"  Readings: {len(readings)}")
        total_sensors += len(readings)
        
        if readings:
            print("  Sample readings:")
            for reading in readings[:5]:  # Show first 5
                print(f"    • {reading.name}: {reading.value} {reading.unit}")
        print()
    
    print(f"🎯 Total sensors detected: {total_sensors}")
    
    if total_sensors > 0:
        # Check if we have real hardware sensors (not just mock)
        real_sensors = sum(1 for source in data.keys() if source not in ['MockSensor', 'mock'])
        if real_sensors > 0:
            print("✅ SUCCESS: Real hardware sensors detected!")
        else:
            print("⚠️  Only mock sensors detected")
    else:
        print("❌ No sensors detected")
    
    # Cleanup
    await manager.shutdown()

if __name__ == "__main__":
    asyncio.run(test_sensor_conflict_resolution()) 