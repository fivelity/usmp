#!/usr/bin/env python3
"""
Ultimate Sensor Monitor Server Startup Script
"""
import os
import sys
import uvicorn
from pathlib import Path

def main():
    # Set up the environment
    server_dir = Path(__file__).parent
    os.chdir(server_dir)
    
    # Add the server directory to Python path
    if str(server_dir) not in sys.path:
        sys.path.insert(0, str(server_dir))
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8100))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    print(f"Starting Ultimate Sensor Monitor Server...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"WebSocket URL: ws://{host if host != '0.0.0.0' else 'localhost'}:{port}/ws")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info",
        access_log=True,
        ws_ping_interval=30,
        ws_ping_timeout=10,
    )

if __name__ == "__main__":
    main()
