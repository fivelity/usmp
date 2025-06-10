#!/usr/bin/env python3
"""
Ultimate Sensor Monitor - Backend Server Launcher
Cross-platform Python launcher script
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("=" * 64)
    print("           Ultimate Sensor Monitor - Backend Server")
    print("=" * 64)
    print()

def check_environment():
    """Check if we're in the correct directory and environment"""
    # Check if server directory exists
    if not Path("server").exists():
        print("❌ Error: server directory not found!")
        print("Please run this script from the UltimateSensorMonitor root directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Change to server directory
    os.chdir("server")
    print("✅ [1/4] Changed to server directory")

    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ Error: requirements.txt not found!")
        print("Please ensure requirements.txt is present in the server directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    print("✅ [2/4] Found requirements.txt")

def activate_virtual_environment() -> str:
    """Activate virtual environment if available, create if it doesn't exist"""
    venv_path = Path("venv")
    
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if not python_exe.exists():
        print("⚙️ [3/4] Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            print("✅ Virtual environment created successfully")
            
            # Install requirements
            print("⚙️ [4/4] Installing dependencies...")
            if platform.system() == "Windows":
                pip_cmd = str(venv_path / "Scripts" / "pip.exe")
            else:
                pip_cmd = str(venv_path / "bin" / "pip")
            
            subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error setting up virtual environment: {e}")
            input("Press Enter to exit...")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error during setup: {e}")
            input("Press Enter to exit...")
            sys.exit(1)
    else:
        print("✅ [3/4] Found existing virtual environment")
        print("✅ [4/4] Using installed dependencies")
    
    return str(python_exe)

def start_server(python_cmd: str) -> None:
    """Start the backend server"""
    print("🚀 Starting backend server...")
    print()
    print("📡 Server starting on: http://localhost:8101")
    print("📚 API Documentation: http://localhost:8101/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8101/ws")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 64)
    print()
    
    try:
        # Run the server
        cmd: list[str] = [
            python_cmd, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8101", 
            "--reload",
            "--reload-dir", "app"
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        print("Make sure all dependencies are installed:")
        print(f"  {python_cmd} -m pip install -r requirements.txt")
    except FileNotFoundError:
        print(f"\n❌ Python not found: {python_cmd}")
        print("Please ensure Python is installed and available in PATH")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Try creating a new virtual environment:")
        print("  1. Delete the 'venv' directory")
        print("  2. Run this script again")
    finally:
        print("\n👋 Goodbye!")
        input("Press Enter to exit...")

def main():
    """Main launcher function"""
    print_banner()
    check_environment()
    python_cmd = activate_virtual_environment()
    start_server(python_cmd)

if __name__ == "__main__":
    main()
