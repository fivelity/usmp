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
    # Get the project root directory (one level up from 'scripts')
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Check if server directory exists
    server_dir = Path("server")
    if not server_dir.exists():
        print("❌ Error: server directory not found!")
        print(f"Expected at: {project_root / server_dir}")
        input("Press Enter to exit...")
        sys.exit(1)

    # Change to server directory
    os.chdir(server_dir)
    print("✅ [1/4] Changed to server directory")

    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ Error: requirements.txt not found!")
        print(
            "Please ensure requirements.txt is present in the server directory."
        )
        input("Press Enter to exit...")
        sys.exit(1)
    print("✅ [2/4] Found requirements.txt")


def detect_and_setup_python_environment() -> str:
    """Detect Python environment and setup if needed"""
    # Import the environment detector
    sys.path.insert(0, str(Path(__file__).parent.parent / "server"))
    try:
        from env_detector import PythonEnvironmentDetector
    except ImportError:
        print("⚠️ Environment detector not found, using fallback method")
        return fallback_environment_setup()
    
    detector = PythonEnvironmentDetector()
    env_type, env_path, env_info = detector.detect_environment()
    
    print(f"✅ [3/4] Detected {env_type.upper()} environment")
    print(f"    Path: {env_path}")
    
    python_exe = env_info.get('python_exe')
    if not python_exe or not Path(python_exe).exists():
        print("❌ Python executable not found, creating virtual environment...")
        return create_fallback_venv()
    
    # Check if we need to install requirements
    if env_type == "venv" and not env_info.get('active', False):
        # Local venv exists but might need dependency installation
        requirements_file = Path("requirements.txt")
        if requirements_file.exists():
            print("⚙️ [4/4] Checking dependencies...")
            pip_exe = detector.get_pip_executable(env_path)
            if pip_exe:
                try:
                    subprocess.run([pip_exe, "install", "-r", "requirements.txt"], 
                                 check=True, capture_output=True)
                    print("✅ Dependencies updated")
                except subprocess.CalledProcessError:
                    print("⚠️ Could not update dependencies (continuing anyway)")
    else:
        print("✅ [4/4] Using existing environment with dependencies")
    
    return python_exe


def fallback_environment_setup() -> str:
    """Fallback environment setup for when detector fails"""
    venv_path = Path("venv")
    
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    if not python_exe.exists():
        return create_fallback_venv()
    
    return str(python_exe)


def create_fallback_venv() -> str:
    """Create virtual environment as fallback"""
    venv_path = Path("venv")
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
        
        if platform.system() == "Windows":
            return str(venv_path / "Scripts" / "python.exe")
        else:
            return str(venv_path / "bin" / "python")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up virtual environment: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during setup: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


def start_server(python_cmd: str) -> None:
    """Start the backend server"""
    print("🚀 Starting backend server...")
    print()
    print("📡 Server starting on: http://localhost:8100")
    print("📚 API Documentation: http://localhost:8100/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8100/ws")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 64)
    print()

    try:
        # Run the server
        cmd: list[str] = [
            python_cmd,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8100",
            "--reload",
            "--reload-dir",
            "app",
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
    python_cmd = detect_and_setup_python_environment()
    start_server(python_cmd)


if __name__ == "__main__":
    main()
