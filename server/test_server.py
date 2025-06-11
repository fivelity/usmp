#!/usr/bin/env python3
"""
Simple test script to verify the server is working correctly.
"""

import requests
import time


def test_server():
    """Test if the server is responding correctly."""

    print("🧪 Testing Ultimate Sensor Monitor Server...")

    try:
        # Test main page
        print("📄 Testing main page...")
        r = requests.get("http://localhost:8101", timeout=5)
        print(f"✅ Main page: Status {r.status_code}")

        # Test API endpoints
        print("🔌 Testing API endpoints...")
        r2 = requests.get("http://localhost:8101/api/v1/sensors", timeout=5)
        print(f"✅ Sensors API: Status {r2.status_code}")

        r3 = requests.get("http://localhost:8101/api/v1/sensors/definitions", timeout=5)
        print(f"✅ Sensor Definitions API: Status {r3.status_code}")

        # Test docs
        print("📚 Testing documentation...")
        r4 = requests.get("http://localhost:8101/docs", timeout=5)
        print(f"✅ API Docs: Status {r4.status_code}")

        print("\n🎉 All tests passed! Server is working correctly.")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_server()
