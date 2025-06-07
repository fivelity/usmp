#!/usr/bin/env python3
"""
Ultimate Sensor Monitor - Connection Test Script
Tests both backend server and frontend proxy connectivity
"""

import requests
import json
import time
import websocket
import threading
from urllib.parse import urlparse

def test_backend_direct():
    """Test direct connection to backend server"""
    print("🔧 Testing Backend Server (Direct Connection)...")
    print("=" * 50)
    
    backend_url = "http://localhost:8100"
    
    try:
        # Test main API endpoint
        print(f"📡 Testing: {backend_url}/api/sensors")
        response = requests.get(f"{backend_url}/api/sensors", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            sensor_count = sum(len(source.get('sensors', [])) for source in data.get('sources', {}).values())
            print(f"✅ API Response: {response.status_code} OK")
            print(f"📊 Sensor Sources: {len(data.get('sources', {}))}")
            print(f"🎯 Total Sensors: {sensor_count}")
        else:
            print(f"❌ API Response: {response.status_code} {response.reason}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Backend Connection Failed: {e}")
        return False
    
    try:
        # Test API documentation
        print(f"📚 Testing: {backend_url}/docs")
        response = requests.get(f"{backend_url}/docs", timeout=5)
        
        if response.status_code == 200:
            print(f"✅ API Docs: {response.status_code} OK")
        else:
            print(f"⚠️  API Docs: {response.status_code} {response.reason}")
            
    except requests.RequestException as e:
        print(f"⚠️  API Docs Failed: {e}")
    
    print("✅ Backend server is working correctly!")
    return True

def test_websocket():
    """Test WebSocket connection"""
    print("\n🔌 Testing WebSocket Connection...")
    print("=" * 50)
    
    ws_url = "ws://localhost:8100/ws"
    ws_connected = threading.Event()
    ws_error = threading.Event()
    message_received = threading.Event()
    
    def on_message(ws, message):
        print("📨 WebSocket message received")
        data = json.loads(message)
        if data.get('type') == 'sensor_data':
            print(f"🎯 Sensor data timestamp: {data.get('timestamp')}")
            print(f"📊 Data sources: {len(data.get('sources', {}))}")
        message_received.set()
    
    def on_error(ws, error):
        print(f"❌ WebSocket error: {error}")
        ws_error.set()
    
    def on_open(ws):
        print("✅ WebSocket connection opened")
        ws_connected.set()
    
    def on_close(ws, close_status_code, close_msg):
        print(f"🔌 WebSocket connection closed: {close_status_code}")
    
    try:
        print(f"🔗 Connecting to: {ws_url}")
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_open=on_open,
                                    on_close=on_close)
        
        # Start WebSocket in a thread
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        
        # Wait for connection or error
        if ws_connected.wait(timeout=5):
            print("✅ WebSocket connected successfully")
            
            # Wait for a message
            if message_received.wait(timeout=10):
                print("✅ WebSocket data flow is working")
            else:
                print("⚠️  No WebSocket data received within 10 seconds")
            
            ws.close()
            return True
        else:
            print("❌ WebSocket connection timeout")
            return False
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def test_frontend_proxy():
    """Test frontend server proxy"""
    print("\n🌐 Testing Frontend Proxy...")
    print("=" * 50)
    
    frontend_url = "http://localhost:5501"
    
    try:
        # Test if frontend server is running
        print(f"🏠 Testing: {frontend_url}/")
        response = requests.get(frontend_url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Frontend Server: {response.status_code} OK")
        else:
            print(f"❌ Frontend Server: {response.status_code} {response.reason}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Frontend Server Failed: {e}")
        print("💡 Make sure to run: npm run dev")
        return False
    
    try:
        # Test proxy to backend API
        print(f"🔀 Testing Proxy: {frontend_url}/api/sensors")
        response = requests.get(f"{frontend_url}/api/sensors", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            sensor_count = sum(len(source.get('sensors', [])) for source in data.get('sources', {}).values())
            print(f"✅ Proxy Response: {response.status_code} OK")
            print(f"📊 Sensor Sources: {len(data.get('sources', {}))}")
            print(f"🎯 Total Sensors: {sensor_count}")
            print("✅ Frontend proxy is working correctly!")
            return True
        else:
            print(f"❌ Proxy Response: {response.status_code} {response.reason}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Frontend Proxy Failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Ultimate Sensor Monitor - Connection Test")
    print("=" * 60)
    print("This script tests connectivity to both backend and frontend servers")
    print()
    
    # Test backend
    backend_ok = test_backend_direct()
    
    # Test WebSocket
    websocket_ok = test_websocket()
    
    # Test frontend proxy
    frontend_ok = test_frontend_proxy()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Backend Server:   {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"WebSocket:        {'✅ PASS' if websocket_ok else '❌ FAIL'}")
    print(f"Frontend Proxy:   {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if all([backend_ok, websocket_ok, frontend_ok]):
        print("\n🎉 All tests passed! Your application should be working correctly.")
        print("\n🌐 Access your application at: http://localhost:5501")
        print("📚 Backend API docs at: http://localhost:8100/docs")
    else:
        print("\n❌ Some tests failed. Please check the failed components.")
        
        if not backend_ok:
            print("💡 Start backend: python start_backend.py")
        if not frontend_ok:
            print("💡 Start frontend: cd client && npm run dev")
    
    print("\n👋 Test complete!")

if __name__ == "__main__":
    main()
