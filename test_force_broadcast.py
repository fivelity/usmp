#!/usr/bin/env python3
"""
Test force broadcast while connected.
"""

import asyncio
import websockets
import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

async def test_force_broadcast():
    """Test force broadcast while connected."""
    try:
        # Connect to WebSocket
        logger.info("🔌 Connecting to WebSocket...")
        websocket = await websockets.connect("ws://localhost:8101/ws/force-test")
        logger.info("✅ Connected successfully")
        
        messages = []
        
        async def listen():
            async for message in websocket:
                try:
                    data = json.loads(message)
                    messages.append(data)
                    msg_type = data.get("type", "unknown")
                    logger.info(f"📩 Received: {msg_type}")
                    
                    if msg_type == "sensor_data":
                        sensor_data = data.get("data", {})
                        total_sensors = sensor_data.get("total_sensors", 0)
                        logger.info(f"📊 Sensor Data: {total_sensors} sensors")
                        
                except json.JSONDecodeError:
                    logger.info(f"📝 Text: {message}")
        
        # Start listening
        listen_task = asyncio.create_task(listen())
        
        # Wait for connection to be established
        await asyncio.sleep(2)
        
        # Force a broadcast
        logger.info("🚀 Forcing broadcast...")
        response = requests.post("http://localhost:8101/realtime/broadcast")
        result = response.json()
        logger.info(f"   Result: {result}")
        
        # Wait for the broadcast
        await asyncio.sleep(3)
        
        # Clean up
        listen_task.cancel()
        await websocket.close()
        
        logger.info(f"🏁 Test completed. Received {len(messages)} messages.")
        
        # Check results
        sensor_data_count = sum(1 for msg in messages if msg.get("type") == "sensor_data")
        if sensor_data_count > 0:
            logger.info("✅ Force broadcast is working!")
        else:
            logger.warning("⚠️  No sensor data received from force broadcast")
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_force_broadcast()) 