#!/usr/bin/env python3
import requests
import json


def verify_sensor_data():
    try:
        # Get current sensor data
        response = requests.get("http://127.0.0.1:8100/api/sensors/current", timeout=5)

        if response.status_code != 200:
            print(f"❌ API Error: HTTP {response.status_code}")
            return

        data = response.json()

        print(f"🔍 SENSOR DATA VERIFICATION")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Total sensors: {len(data)}")

        # Group by category
        categories = {}
        hardware_types = set()

        for sensor_data in data.values():
            category = sensor_data.get("category", "Unknown")
            hardware_type = sensor_data.get("hardware_type", "Unknown")

            if category not in categories:
                categories[category] = []
            categories[category].append(sensor_data)
            hardware_types.add(hardware_type)

        print(f"\n📊 SENSOR CATEGORIES:")
        for category, sensors in sorted(categories.items()):
            print(f"  {category}: {len(sensors)} sensors")

            # Show 2 examples from each category
            for i, sensor in enumerate(sensors[:2]):
                name = sensor.get("name", "Unknown")
                value = sensor.get("value", 0)
                unit = sensor.get("unit", "")
                hw_type = sensor.get("hardware_type", "Unknown")
                print(f"    - {name}: {value}{unit} ({hw_type})")

            if len(sensors) > 2:
                print(f"    ... and {len(sensors) - 2} more")

        print(f"\n🖥️ HARDWARE TYPES ({len(hardware_types)}):")
        for hw_type in sorted(hardware_types):
            count = sum(1 for s in data.values() if s.get("hardware_type") == hw_type)
            print(f"  - {hw_type}: {count} sensors")

        # Verify this is actually extended monitoring
        print(f"\n✅ EXTENDED MONITORING VERIFICATION:")
        extended_indicators = {
            "Voltage sensors": len(
                [s for s in data.values() if s.get("category") == "Voltage"]
            ),
            "Fan sensors": len(
                [s for s in data.values() if s.get("category") == "Fan"]
            ),
            "Clock sensors": len(
                [s for s in data.values() if s.get("category") == "Clock"]
            ),
            "Data sensors": len(
                [s for s in data.values() if s.get("category") == "Data"]
            ),
            "Temperature sensors": len(
                [s for s in data.values() if s.get("category") == "Temperature"]
            ),
            "Total sensors": len(data),
        }

        for indicator, count in extended_indicators.items():
            status = "✅" if count > 0 else "❌"
            print(f"  {status} {indicator}: {count}")

        if len(data) > 20:
            print(f"\n🎉 CONFIRMED: Extended hardware monitoring is active!")
            print(f"   This is significantly more than minimal CPU/GPU monitoring")
        else:
            print(f"\n⚠️ LIMITED: Only {len(data)} sensors detected")
            print(f"   This may be minimal monitoring mode")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - is it running on port 8100?")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    verify_sensor_data()
