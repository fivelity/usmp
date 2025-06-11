#!/usr/bin/env python3
"""
WebSocket test client for Ultimate Sensor Monitor.
Tests real-time sensor data broadcasting.
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


class SensorWebSocketClient:
    def __init__(self, server_url="ws://localhost:8101", client_id="test-client"):
        self.server_url = f"{server_url}/ws/{client_id}"
        self.client_id = client_id
        self.websocket = None
        self.running = False
        self.message_count = 0
        self.sensor_data_count = 0

    async def connect(self):
        """Connect to the WebSocket server."""
        try:
            logger.info(f"🔌 Connecting to {self.server_url}")
            self.websocket = await websockets.connect(self.server_url)
            self.running = True
            logger.info(f"✅ Connected successfully as {self.client_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False

    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        self.running = False
        if self.websocket:
            await self.websocket.close()
            logger.info("🔌 Disconnected from server")

    async def send_command(self, command):
        """Send a command to the server."""
        if not self.websocket:
            logger.error("❌ Not connected to server")
            return

        try:
            message = json.dumps({"command": command})
            await self.websocket.send(message)
            logger.info(f"📤 Sent command: {command}")
        except Exception as e:
            logger.error(f"❌ Failed to send command {command}: {e}")

    async def listen(self):
        """Listen for messages from the server."""
        if not self.websocket:
            logger.error("❌ Not connected to server")
            return

        logger.info("👂 Starting to listen for messages...")

        try:
            async for message in self.websocket:
                self.message_count += 1

                try:
                    # Try to parse as JSON
                    data = json.loads(message)
                    await self.handle_json_message(data)
                except json.JSONDecodeError:
                    # Handle plain text messages
                    await self.handle_text_message(message)

        except websockets.exceptions.ConnectionClosed:
            logger.info("🔌 Connection closed by server")
        except Exception as e:
            logger.error(f"❌ Error in listen loop: {e}")

    async def handle_json_message(self, data):
        """Handle JSON messages from the server."""
        message_type = data.get("type", "unknown")
        timestamp = data.get("timestamp", "")

        if message_type == "connection_established":
            logger.info(f"🎉 {data.get('message', 'Connection established')}")

        elif message_type == "sensor_data":
            self.sensor_data_count += 1
            sensor_data = data.get("data", {})
            sources = sensor_data.get("sources", {})
            total_sensors = sensor_data.get("total_sensors", 0)
            active_sources = sensor_data.get("active_sources", 0)

            logger.info(
                f"📊 Sensor Data #{self.sensor_data_count}: {total_sensors} sensors from {active_sources} sources"
            )

            # Log details about each source
            for source_name, readings in sources.items():
                if readings:
                    logger.info(f"   🔧 {source_name}: {len(readings)} sensors")

                    # Show first few sensors as examples
                    for i, reading in enumerate(readings[:3]):
                        sensor_id = reading.get("sensor_id", "unknown")
                        value = reading.get("value", 0)
                        status = reading.get("status", "unknown")
                        logger.info(f"      • {sensor_id}: {value} ({status})")

                    if len(readings) > 3:
                        logger.info(f"      ... and {len(readings) - 3} more sensors")

        elif message_type == "stats_response":
            stats = data.get("data", {})
            logger.info(f"📈 Stats Response:")
            logger.info(f"   Running: {stats.get('is_running', False)}")
            logger.info(f"   Broadcasts sent: {stats.get('broadcasts_sent', 0)}")
            logger.info(f"   Connected clients: {stats.get('connected_clients', 0)}")

        elif message_type == "broadcast_response":
            success = data.get("success", False)
            logger.info(f"📡 Force broadcast: {'✅ Success' if success else '❌ Failed'}")

        elif message_type == "error":
            error_message = data.get("message", "Unknown error")
            logger.error(f"🚨 Server error: {error_message}")

        else:
            logger.info(f"📩 Message ({message_type}): {json.dumps(data, indent=2)}")

    async def handle_text_message(self, message):
        """Handle plain text messages from the server."""
        logger.info(f"📝 Text message: {message}")

    async def test_commands(self):
        """Test sending commands to the server."""
        if not self.websocket:
            return

        logger.info("🧪 Testing server commands...")

        # Wait a bit for initial connection
        await asyncio.sleep(2)

        # Test getting stats
        await self.send_command("get_stats")
        await asyncio.sleep(1)

        # Test force broadcast
        await self.send_command("force_broadcast")
        await asyncio.sleep(1)

        # Test unknown command
        await self.send_command("unknown_command")
        await asyncio.sleep(1)

        # Send a plain text message
        if self.websocket:
            await self.websocket.send("Hello from test client!")
            logger.info("📤 Sent plain text message")


async def main():
    """Main test function."""
    logger.info("🚀 Starting WebSocket Test Client")
    logger.info("=" * 60)

    client = SensorWebSocketClient()

    try:
        # Connect to server
        if not await client.connect():
            return

        # Start listening in background
        listen_task = asyncio.create_task(client.listen())

        # Test commands
        command_task = asyncio.create_task(client.test_commands())

        # Run for 30 seconds to collect some data
        logger.info("⏱️  Running test for 30 seconds...")
        await asyncio.sleep(30)

        # Stop tasks
        listen_task.cancel()
        command_task.cancel()

        # Summary
        logger.info("=" * 60)
        logger.info(f"📊 TEST SUMMARY:")
        logger.info(f"   Total messages received: {client.message_count}")
        logger.info(f"   Sensor data messages: {client.sensor_data_count}")
        logger.info(f"   Client ID: {client.client_id}")

        if client.sensor_data_count > 0:
            logger.info("✅ Real-time sensor data is working!")
        else:
            logger.warning("⚠️  No sensor data received - check server status")

    except KeyboardInterrupt:
        logger.info("🛑 Test interrupted by user")
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
    finally:
        await client.disconnect()
        logger.info("🏁 Test completed")


if __name__ == "__main__":
    asyncio.run(main())
