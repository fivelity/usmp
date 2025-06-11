#!/usr/bin/env python3
"""
Test the RealTimeService and sensor data broadcasting.
"""

import asyncio
import websockets
import json
import logging
import requests
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


async def test_with_client_connected():
    """Test force broadcast while a client is connected."""
    logger.info("🧪 Testing RealTimeService with client connected")

    try:
        # Connect to WebSocket
        logger.info("🔌 Connecting to WebSocket...")
        websocket = await websockets.connect("ws://localhost:8101/ws/realtime-test")
        logger.info("✅ Connected to WebSocket")

        # Start listening for messages
        async def listen():
            message_count = 0
            async for message in websocket:
                message_count += 1
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "unknown")
                    logger.info(f"📩 Message #{message_count}: {msg_type}")

                    if msg_type == "sensor_data":
                        sensor_data = data.get("data", {})
                        total_sensors = sensor_data.get("total_sensors", 0)
                        active_sources = sensor_data.get("active_sources", 0)
                        is_forced = sensor_data.get("forced", False)
                        forced_text = " (FORCED)" if is_forced else ""
                        logger.info(
                            f"   📊 {total_sensors} sensors from {active_sources} sources{forced_text}"
                        )

                        # Show sensor details
                        sources = sensor_data.get("sources", {})
                        for source_name, readings in sources.items():
                            if readings:
                                logger.info(
                                    f"      🔧 {source_name}: {len(readings)} sensors"
                                )
                                # Show first sensor as example
                                first_sensor = readings[0]
                                logger.info(
                                    f"         • {first_sensor.get('sensor_id', 'unknown')}: {first_sensor.get('value', 0)}"
                                )

                except json.JSONDecodeError:
                    logger.info(f"📝 Text: {message}")

        # Start listening task
        listen_task = asyncio.create_task(listen())

        # Wait for connection to be established
        await asyncio.sleep(2)

        # Get initial stats
        logger.info("📈 Getting initial stats...")
        response = requests.get("http://localhost:8101/realtime/stats")
        stats = response.json()
        logger.info(f"   Connected clients: {stats['connected_clients']}")
        logger.info(f"   Broadcasts sent: {stats['broadcasts_sent']}")
        logger.info(f"   Errors: {stats['errors_count']}")

        # Force a broadcast
        logger.info("🚀 Forcing broadcast...")
        response = requests.post("http://localhost:8101/realtime/broadcast")
        result = response.json()
        logger.info(f"   Force broadcast result: {result}")

        # Wait for the broadcast
        await asyncio.sleep(3)

        # Get updated stats
        logger.info("📈 Getting updated stats...")
        response = requests.get("http://localhost:8101/realtime/stats")
        stats = response.json()
        logger.info(f"   Connected clients: {stats['connected_clients']}")
        logger.info(f"   Broadcasts sent: {stats['broadcasts_sent']}")
        logger.info(f"   Errors: {stats['errors_count']}")

        # Let it run for a bit to see automatic broadcasts
        logger.info("⏱️  Waiting for automatic broadcasts (10 seconds)...")
        await asyncio.sleep(10)

        # Clean up
        listen_task.cancel()
        await websocket.close()
        logger.info("🔌 Disconnected")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")


async def test_sensor_data_directly():
    """Test sensor data directly from the server."""
    logger.info("🔍 Testing sensor data endpoints...")

    # Test various endpoints
    endpoints = [
        "/health",
        "/realtime/stats",
        "/test-websocket",  # This should show available endpoints
    ]

    for endpoint in endpoints:
        try:
            logger.info(f"🌐 Testing {endpoint}")
            response = requests.get(f"http://localhost:8101{endpoint}")
            if response.status_code == 200:
                if endpoint == "/test-websocket":
                    logger.info(f"   ✅ {response.status_code} - HTML page available")
                else:
                    data = response.json()
                    logger.info(f"   ✅ {response.status_code} - {data}")
            else:
                logger.warning(f"   ⚠️  {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")


async def main():
    """Main test function."""
    logger.info("🚀 Starting RealTimeService Tests")
    logger.info("=" * 60)

    # Test endpoints first
    await test_sensor_data_directly()

    logger.info("=" * 60)

    # Test with WebSocket client
    await test_with_client_connected()

    logger.info("=" * 60)
    logger.info("🏁 Tests completed")


if __name__ == "__main__":
    asyncio.run(main())
