#!/usr/bin/env python3
"""
Quick test for real-time sensor data broadcasting.
"""

import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

async def test_realtime_broadcast():
    """Test real-time broadcasting with a connected client."""
    try:
        # Connect to WebSocket
        logger.info("🔌 Connecting to WebSocket...")
        websocket = await websockets.connect("ws://localhost:8101/ws/quick-test")
        logger.info("✅ Connected successfully")
        
        # Listen for messages for 15 seconds
        message_count = 0
        start_time = asyncio.get_event_loop().time()
        
        async def listen():
            nonlocal message_count
            async for message in websocket:
                message_count += 1
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "unknown")
                    
                    if msg_type == "sensor_data":
                        sensor_data = data.get("data", {})
                        total_sensors = sensor_data.get("total_sensors", 0)
                        active_sources = sensor_data.get("active_sources", 0)
                        logger.info(f"📊 Sensor Data: {total_sensors} sensors from {active_sources} sources")
                        
                        # Show sample data
                        sources = sensor_data.get("sources", {})
                        for source_name, readings in sources.items():
                            if readings and len(readings) > 0:
                                first_sensor = readings[0]
                                logger.info(f"   🔧 {source_name}: {first_sensor.get('name', 'unknown')} = {first_sensor.get('value', 0)} {first_sensor.get('unit', '')}")
                    else:
                        logger.info(f"📩 Message: {msg_type}")
                        
                except json.JSONDecodeError:
                    logger.info(f"📝 Text: {message}")
        
        # Start listening
        listen_task = asyncio.create_task(listen())
        
        # Wait for 15 seconds
        logger.info("⏱️  Listening for 15 seconds...")
        await asyncio.sleep(15)
        
        # Clean up
        listen_task.cancel()
        await websocket.close()
        
        logger.info(f"🏁 Test completed. Received {message_count} messages.")
        
        if message_count > 1:  # 1 for connection message + sensor data
            logger.info("✅ Real-time broadcasting is working!")
        else:
            logger.warning("⚠️  No sensor data received - check broadcasting")
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_realtime_broadcast()) 