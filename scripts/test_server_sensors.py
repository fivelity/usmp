#!/usr/bin/env python3
"""
Test script to check if the server is running and providing real sensor data.
"""

import requests
import json


def test_server_sensors():
    """Test if the server is running and providing sensor data."""
    try:
        print("🔍 Testing server sensor endpoints...")

        # Test basic health
        response = requests.get(
            "http://localhost:8100/api/realtime/sensors", timeout=10
        )
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data)} sensors")

            # Check sensor sources
            sources = set()
            for sensor in data:
                source = sensor.get("source", "unknown")
                sources.add(source)

            print(f"📡 Sensor sources: {list(sources)}")

            # Show sample sensors
            print(f"\n📊 Sample sensors:")
            for sensor in data[:10]:
                name = sensor.get("name", "Unknown")
                value = sensor.get("value", "N/A")
                unit = sensor.get("unit", "")
                source = sensor.get("source", "unknown")
                print(f"   [{source}] {name}: {value} {unit}")

            # Check if we have real hardware sensors
            hardware_sources = [s for s in sources if s not in ["MockSensor", "mock"]]
            if hardware_sources:
                print(f"\n🎉 SUCCESS: Real hardware sensors detected!")
                print(f"   Hardware sources: {hardware_sources}")
            else:
                print(f"\n⚠️  Only mock sensors detected")

        else:
            print(f"❌ Server returned status {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server - is it running?")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_server_sensors()
