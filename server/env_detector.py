#!/usr/bin/env python3
"""
Unified Python Environment Detection Utility
Detects conda, pyenv, venv, and system Python environments for local development.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Tuple, Optional, Dict, Any


class PythonEnvironmentDetector:
    """Detects and manages different Python environments for local development."""
    
    def __init__(self):
        self.system = platform.system()
        self.is_windows = self.system == "Windows"
        
    def detect_environment(self) -> Tuple[str, str, Dict[str, Any]]:
        """
        Detect the current Python environment.
        
        Returns:
            Tuple of (env_type, env_path, env_info)
        """
        # Check for conda first (priority for this project)
        conda_info = self._detect_conda()
        if conda_info:
            return "conda", conda_info["path"], conda_info
            
        # Check for pyenv
        pyenv_info = self._detect_pyenv()
        if pyenv_info:
            return "pyenv", pyenv_info["path"], pyenv_info
            
        # Check for virtual environment
        venv_info = self._detect_venv()
        if venv_info:
            return "venv", venv_info["path"], venv_info
            
        # Fall back to system Python
        system_info = self._detect_system_python()
        return "system", system_info["path"], system_info
    
    def _detect_conda(self) -> Optional[Dict[str, Any]]:
        """Detect conda environment."""
        conda_prefix = os.environ.get('CONDA_PREFIX')
        if conda_prefix:
            python_exe = self._get_python_executable(conda_prefix)
            if python_exe and python_exe.exists():
                return {
                    "path": str(conda_prefix),
                    "python_exe": str(python_exe),
                    "type": "conda",
                    "active": True,
                    "conda_env": os.environ.get('CONDA_DEFAULT_ENV', 'base')
                }
        
        # Check for conda installation even if not activated
        conda_exe = self._find_conda_executable()
        if conda_exe:
            return {
                "path": str(Path(conda_exe).parent.parent),
                "python_exe": str(self._get_python_executable(Path(conda_exe).parent.parent)),
                "type": "conda",
                "active": False,
                "conda_exe": str(conda_exe)
            }
        
        return None
    
    def _detect_pyenv(self) -> Optional[Dict[str, Any]]:
        """Detect pyenv environment."""
        pyenv_root = os.environ.get('PYENV_ROOT')
        if not pyenv_root:
            # Try common pyenv locations
            if self.is_windows:
                pyenv_root = os.path.expanduser('~/.pyenv/pyenv-win')
            else:
                pyenv_root = os.path.expanduser('~/.pyenv')
        
        if pyenv_root and Path(pyenv_root).exists():
            # Get current pyenv version
            try:
                result = subprocess.run(['pyenv', 'version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip().split()[0]
                    python_path = Path(pyenv_root) / 'versions' / version
                    python_exe = self._get_python_executable(python_path)
                    if python_exe and python_exe.exists():
                        return {
                            "path": str(python_path),
                            "python_exe": str(python_exe),
                            "type": "pyenv",
                            "version": version,
                            "pyenv_root": pyenv_root
                        }
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        return None
    
    def _detect_venv(self) -> Optional[Dict[str, Any]]:
        """Detect virtual environment."""
        virtual_env = os.environ.get('VIRTUAL_ENV')
        if virtual_env:
            python_exe = self._get_python_executable(virtual_env)
            if python_exe and python_exe.exists():
                return {
                    "path": virtual_env,
                    "python_exe": str(python_exe),
                    "type": "venv",
                    "active": True
                }
        
        # Check for local venv directory
        local_venv = Path("venv")
        if local_venv.exists():
            python_exe = self._get_python_executable(local_venv)
            if python_exe and python_exe.exists():
                return {
                    "path": str(local_venv.absolute()),
                    "python_exe": str(python_exe),
                    "type": "venv",
                    "active": False
                }
        
        return None
    
    def _detect_system_python(self) -> Dict[str, Any]:
        """Detect system Python."""
        return {
            "path": str(Path(sys.executable).parent),
            "python_exe": sys.executable,
            "type": "system",
            "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
    
    def _get_python_executable(self, env_path: Path) -> Optional[Path]:
        """Get Python executable for given environment path."""
        env_path = Path(env_path)
        
        if self.is_windows:
            # Try Scripts directory first (venv, conda)
            python_exe = env_path / "Scripts" / "python.exe"
            if python_exe.exists():
                return python_exe
            # Try direct python.exe (pyenv, system)
            python_exe = env_path / "python.exe"
            if python_exe.exists():
                return python_exe
        else:
            # Try bin directory (Unix-like systems)
            python_exe = env_path / "bin" / "python"
            if python_exe.exists():
                return python_exe
            # Try direct python
            python_exe = env_path / "python"
            if python_exe.exists():
                return python_exe
        
        return None
    
    def _find_conda_executable(self) -> Optional[str]:
        """Find conda executable."""
        conda_commands = ['conda', 'conda.exe'] if self.is_windows else ['conda']
        
        for cmd in conda_commands:
            try:
                result = subprocess.run(['where' if self.is_windows else 'which', cmd],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        return None
    
    def get_pip_executable(self, env_path: str) -> Optional[str]:
        """Get pip executable for given environment."""
        env_path = Path(env_path)
        
        if self.is_windows:
            pip_exe = env_path / "Scripts" / "pip.exe"
            if pip_exe.exists():
                return str(pip_exe)
        else:
            pip_exe = env_path / "bin" / "pip"
            if pip_exe.exists():
                return str(pip_exe)
        
        return None
    
    def print_environment_info(self):
        """Print detailed environment information."""
        env_type, env_path, env_info = self.detect_environment()
        
        print(f"🐍 Python Environment Detection Results")
        print(f"═══════════════════════════════════════")
        print(f"Environment Type: {env_type.upper()}")
        print(f"Environment Path: {env_path}")
        print(f"Python Executable: {env_info.get('python_exe', 'Unknown')}")
        
        if env_type == "conda":
            print(f"Conda Environment: {env_info.get('conda_env', 'Unknown')}")
            print(f"Active: {'Yes' if env_info.get('active') else 'No'}")
        elif env_type == "pyenv":
            print(f"Pyenv Version: {env_info.get('version', 'Unknown')}")
            print(f"Pyenv Root: {env_info.get('pyenv_root', 'Unknown')}")
        elif env_type == "venv":
            print(f"Active: {'Yes' if env_info.get('active') else 'No'}")
        elif env_type == "system":
            print(f"Python Version: {env_info.get('version', 'Unknown')}")
        
        print(f"Platform: {self.system}")
        print(f"═══════════════════════════════════════")


def main():
    """Command line interface for environment detection."""
    detector = PythonEnvironmentDetector()
    detector.print_environment_info()


if __name__ == "__main__":
    main()
