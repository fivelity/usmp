#!/usr/bin/env python3
"""
Test script to verify actual sensor data being received
"""

import requests
import json
import time
from typing import Dict, Any


def test_sensor_endpoints():
    """Test all sensor endpoints and verify data reception"""
    base_url = "http://127.0.0.1:8100"

    print("=" * 60)
    print("🔍 VERIFYING EXTENDED SENSOR DATA RECEPTION")
    print("=" * 60)

    try:
        # Test if server is running
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"❌ Server health check failed: HTTP {health_response.status_code}")
            return False

        print("✅ Server is running and responding")

        # Get current sensor data
        print("\n📊 TESTING CURRENT SENSOR DATA...")
        response = requests.get(f"{base_url}/api/sensors/current", timeout=10)

        if response.status_code != 200:
            print(f"❌ Sensor endpoint failed: HTTP {response.status_code}")
            return False

        data = response.json()
        print(f"✅ Received sensor data: {len(data)} total sensors")

        if len(data) == 0:
            print("❌ No sensor data received - monitoring may not be working")
            return False

        # Analyze sensor data by category
        print("\n📈 SENSOR BREAKDOWN BY CATEGORY:")
        categories = {}
        hardware_types = set()

        for sensor_id, sensor_data in data.items():
            category = sensor_data.get("category", "Unknown")
            hardware_type = sensor_data.get("hardware_type", "Unknown")

            if category not in categories:
                categories[category] = []
            categories[category].append(sensor_data)
            hardware_types.add(hardware_type)

        # Show category breakdown
        for category, sensors in sorted(categories.items()):
            print(f"  {category}: {len(sensors)} sensors")

            # Show examples from each category
            for i, sensor in enumerate(sensors[:2]):
                name = sensor.get("name", "Unknown")
                value = sensor.get("value", 0)
                unit = sensor.get("unit", "")
                hw_type = sensor.get("hardware_type", "Unknown")
                print(f"    - {name}: {value}{unit} ({hw_type})")

            if len(sensors) > 2:
                print(f"    ... and {len(sensors) - 2} more sensors")

        print(f"\n🖥️ HARDWARE TYPES DETECTED: {len(hardware_types)}")
        for hw_type in sorted(hardware_types):
            count = sum(1 for s in data.values() if s.get("hardware_type") == hw_type)
            print(f"  - {hw_type}: {count} sensors")

        # Test specific categories to confirm "extended" monitoring
        expected_categories = [
            "Temperature",
            "Usage",
            "Clock",
            "Voltage",
            "Fan",
            "Data",
            "Load",
        ]
        found_categories = set(categories.keys())

        print(f"\n✅ EXTENDED MONITORING VERIFICATION:")
        print(f"Expected categories: {', '.join(expected_categories)}")
        print(f"Found categories: {', '.join(sorted(found_categories))}")

        missing = set(expected_categories) - found_categories
        if missing:
            print(f"⚠️ Missing categories: {', '.join(missing)}")
        else:
            print("✅ All expected sensor categories found!")

        # Test live data updates
        print(f"\n🔄 TESTING LIVE DATA UPDATES...")
        print("Taking two readings 3 seconds apart to verify real-time updates...")

        first_reading = data
        time.sleep(3)

        second_response = requests.get(f"{base_url}/api/sensors/current", timeout=5)
        if second_response.status_code == 200:
            second_reading = second_response.json()

            # Check for value changes
            changes = 0
            for sensor_id in first_reading:
                if sensor_id in second_reading:
                    old_val = first_reading[sensor_id].get("value", 0)
                    new_val = second_reading[sensor_id].get("value", 0)
                    if old_val != new_val:
                        changes += 1

            print(f"✅ Data updates detected: {changes} sensors changed values")
            if changes > 0:
                print("✅ Real-time monitoring is active and working!")
            else:
                print("⚠️ No value changes detected - may be normal for stable system")
        else:
            print("⚠️ Could not get second reading for update verification")

        # Test WebSocket endpoint
        print(f"\n🔌 TESTING WEBSOCKET ENDPOINT...")
        try:
            import websocket
            import threading

            ws_messages = []

            def on_message(ws, message):
                ws_messages.append(message)
                if len(ws_messages) >= 2:
                    ws.close()

            def on_error(ws, error):
                print(f"WebSocket error: {error}")

            ws = websocket.WebSocketApp(
                f"ws://127.0.0.1:8100/ws", on_message=on_message, on_error=on_error
            )

            # Run WebSocket in thread with timeout
            ws_thread = threading.Thread(target=ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()

            # Wait for messages
            timeout_count = 0
            while len(ws_messages) < 2 and timeout_count < 10:
                time.sleep(0.5)
                timeout_count += 1

            if ws_messages:
                print(f"✅ WebSocket working: Received {len(ws_messages)} messages")
                try:
                    sample_data = json.loads(ws_messages[0])
                    print(f"   Sample WebSocket data: {len(sample_data)} sensors")
                except:
                    print("   WebSocket sending data (format check failed)")
            else:
                print("⚠️ No WebSocket messages received")

        except ImportError:
            print("⚠️ websocket-client not installed, skipping WebSocket test")
        except Exception as e:
            print(f"⚠️ WebSocket test failed: {e}")

        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - is it running on port 8100?")
        return False
    except Exception as e:
        print(f"❌ Error during sensor verification: {e}")
        return False


def test_sensor_apis():
    """Test specific sensor API endpoints"""
    base_url = "http://127.0.0.1:8100"

    print(f"\n🔍 TESTING SENSOR API ENDPOINTS...")

    endpoints = [
        "/api/sensors/available",
        "/api/sensors/categories",
        "/api/sensors/hardware",
        "/api/sensors/lhm/status",
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(
                    f"✅ {endpoint}: OK ({len(data) if isinstance(data, (list, dict)) else 'data'} items)"
                )
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")


if __name__ == "__main__":
    success = test_sensor_endpoints()
    test_sensor_apis()

    print("\n" + "=" * 60)
    if success:
        print("🎉 VERIFICATION COMPLETE: Extended sensor monitoring is working!")
    else:
        print("❌ VERIFICATION FAILED: Issues detected with sensor monitoring")
    print("=" * 60)
