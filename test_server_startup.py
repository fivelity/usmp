#!/usr/bin/env python3
"""
Test script to verify sensor manager initialization without DLL conflicts.
"""

import sys
import os
import asyncio

# Add server directory to path
server_dir = os.path.join(os.path.dirname(__file__), 'server')
sys.path.insert(0, server_dir)

async def test_sensor_manager_initialization():
    """Test sensor manager initialization directly."""
    print("🚀 Testing Sensor Manager Initialization")
    print("=" * 50)
    
    try:
        print("⚙️  Importing sensor manager...")
        from app.services.sensor_manager import SensorManager
        from app.core.config import AppSettings
        
        settings = AppSettings()
        manager = SensorManager(settings)
        
        print("🔧 Initializing sensor manager...")
        await manager.initialize()
        
        print("📊 Checking sensor data...")
        await asyncio.sleep(3)  # Give it time to collect data
        
        data = await manager.get_all_sensor_data()
        definitions = await manager.get_sensor_definitions()
        
        print(f"\n🎯 RESULTS:")
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
        hardware_sources = [source for source in data.keys() if source not in ['MockSensor', 'mock']]
        if hardware_sources:
            print(f"\n🎉 SUCCESS: Real hardware sensors detected!")
            print(f"   Hardware sources: {hardware_sources}")
        else:
            print(f"\n⚠️  Only mock sensors detected")
        
        await manager.shutdown()
        print("\n✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Error during sensor manager test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_sensor_manager_initialization()) 