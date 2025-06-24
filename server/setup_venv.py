import os
import subprocess
import sys
import platform
from pathlib import Path


def get_scripts_dir():
    """Get the correct scripts directory for the current platform."""
    return "Scripts" if platform.system() == "Windows" else "bin"


def create_venv():
    """Create virtual environment with cross-platform compatibility."""
    venv_dir = Path("venv")
    scripts_dir = get_scripts_dir()
    
    print(f"Creating virtual environment at: {venv_dir}")
    subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    
    # Use cross-platform path for pip
    pip_path = venv_dir / scripts_dir / ("pip.exe" if platform.system() == "Windows" else "pip")
    print(f"Installing requirements using: {pip_path}")
    
    subprocess.check_call(
        [str(pip_path), "install", "-r", "requirements-dev.txt"]
    )


if __name__ == "__main__":
    create_venv()
