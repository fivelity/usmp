#!/usr/bin/env python3

"""
Simple WebSocket test script for Ultimate Sensor Monitor
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_websocket():
    """Test WebSocket connection and basic functionality"""
    
    uri = "ws://127.0.0.1:8101/ws/test_client"
    
    try:
        print("🔌 Connecting to WebSocket...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket!")
            
            # Wait for welcome message
            welcome_msg = await websocket.recv()
            print(f"📨 Welcome message: {welcome_msg}")
            
            # Send a test message
            test_message = {
                "type": "test",
                "timestamp": datetime.now().isoformat(),
                "message": "Hello from test client!"
            }
            
            await websocket.send(json.dumps(test_message))
            print(f"📤 Sent test message: {test_message}")
            
            # Wait for echo response
            response = await websocket.recv()
            print(f"📥 Received response: {response}")
            
            # Send heartbeat
            heartbeat = {
                "type": "heartbeat",
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(heartbeat))
            print(f"💓 Sent heartbeat: {heartbeat}")
            
            # Wait for heartbeat response
            heartbeat_response = await websocket.recv()
            print(f"💓 Heartbeat response: {heartbeat_response}")
            
            print("✅ WebSocket test completed successfully!")
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(test_websocket()) 