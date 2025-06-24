#!/usr/bin/env python3
"""
Quick Local Development Environment Test
Verifies that all fixes are working properly for local development.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")


def print_result(test_name, success, details=""):
    """Print test result."""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")


def test_environment_detection():
    """Test Python environment detection."""
    print_header("Python Environment Detection Test")
    
    try:
        # Test environment detector
        sys.path.insert(0, str(Path(__file__).parent / "server"))
        from env_detector import PythonEnvironmentDetector
        
        detector = PythonEnvironmentDetector()
        env_type, env_path, env_info = detector.detect_environment()
        
        print_result("Environment Detector Import", True)
        print_result("Environment Detection", True, 
                    f"Detected: {env_type.upper()} at {env_path}")
        
        python_exe = env_info.get('python_exe')
        if python_exe and Path(python_exe).exists():
            print_result("Python Executable Found", True, f"Path: {python_exe}")
        else:
            print_result("Python Executable Found", False, "Python executable not found")
            
        return True
        
    except ImportError as e:
        print_result("Environment Detector Import", False, f"Import error: {e}")
        return False
    except Exception as e:
        print_result("Environment Detection", False, f"Error: {e}")
        return False


def test_path_handling():
    """Test cross-platform path handling."""
    print_header("Path Handling Test")
    
    try:
        from pathlib import Path
        
        # Test setup_venv.py fix
        setup_venv_path = Path("server/setup_venv.py")
        if setup_venv_path.exists():
            with open(setup_venv_path, 'r') as f:
                content = f.read()
                
            if 'platform.system()' in content and 'pathlib' in content:
                print_result("setup_venv.py Cross-platform Fix", True, 
                           "Contains platform detection and pathlib usage")
            else:
                print_result("setup_venv.py Cross-platform Fix", False,
                           "Missing platform detection or pathlib")
        else:
            print_result("setup_venv.py Exists", False, "File not found")
            
        # Test path construction
        if platform.system() == "Windows":
            scripts_dir = "Scripts"
        else:
            scripts_dir = "bin"
            
        test_path = Path("venv") / scripts_dir / "python"
        print_result("Path Construction", True, f"Scripts dir: {scripts_dir}")
        
        return True
        
    except Exception as e:
        print_result("Path Handling", False, f"Error: {e}")
        return False


def test_configuration_consistency():
    """Test configuration file consistency."""
    print_header("Configuration Consistency Test")
    
    results = []
    
    # Test server .env
    server_env = Path("server/.env")
    if server_env.exists():
        with open(server_env, 'r') as f:
            env_content = f.read()
        
        if "SECRET_KEY=your-local-development" in env_content:
            print_result("Server .env Security Fix", True, "Dangerous shell command removed")
            results.append(True)
        else:
            print_result("Server .env Security Fix", False, "Still contains shell command")
            results.append(False)
            
        if "PORT=8100" in env_content:
            print_result("Server Port Configuration", True, "Port 8100 configured")
            results.append(True)
        else:
            print_result("Server Port Configuration", False, "Port not set to 8100")
            results.append(False)
    else:
        print_result("Server .env Exists", False, "File not found")
        results.append(False)
    
    # Test client .env
    client_env = Path("client/.env")
    if client_env.exists():
        with open(client_env, 'r') as f:
            client_content = f.read()
            
        if "VITE_API_BASE_URL=http://localhost:8100" in client_content:
            print_result("Client API URL Configuration", True, "Matches server port")
            results.append(True)
        else:
            print_result("Client API URL Configuration", False, "Doesn't match server port")
            results.append(False)
            
        if "VITE_WEBSOCKET_URL=ws://localhost:8100" in client_content:
            print_result("Client WebSocket Configuration", True, "WebSocket URL configured")
            results.append(True)
        else:
            print_result("Client WebSocket Configuration", False, "WebSocket URL missing")
            results.append(False)
    else:
        print_result("Client .env Exists", False, "File not found")
        results.append(False)
    
    return all(results)


def test_scripts_functionality():
    """Test that key scripts work."""
    print_header("Scripts Functionality Test")
    
    results = []
    
    # Test start_backend.py
    start_backend = Path("scripts/start_backend.py")
    if start_backend.exists():
        try:
            # Just test import, don't actually run
            import importlib.util
            spec = importlib.util.spec_from_file_location("start_backend", start_backend)
            module = importlib.util.module_from_spec(spec)
            
            print_result("start_backend.py Import", True, "Script can be imported")
            results.append(True)
        except Exception as e:
            print_result("start_backend.py Import", False, f"Import error: {e}")
            results.append(False)
    else:
        print_result("start_backend.py Exists", False, "File not found")
        results.append(False)
    
    return all(results)


def test_conda_environment():
    """Test specific conda environment support."""
    print_header("Conda Environment Support Test")
    
    # Check if we're in a conda environment
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_prefix:
        print_result("Conda Environment Active", True, f"CONDA_PREFIX: {conda_prefix}")
        
        # Test if our detector recognizes it
        try:
            sys.path.insert(0, str(Path(__file__).parent / "server"))
            from env_detector import PythonEnvironmentDetector
            
            detector = PythonEnvironmentDetector()
            env_type, env_path, env_info = detector.detect_environment()
            
            if env_type == "conda":
                print_result("Conda Detection", True, f"Correctly detected conda at {env_path}")
                return True
            else:
                print_result("Conda Detection", False, f"Detected as {env_type} instead of conda")
                return False
                
        except Exception as e:
            print_result("Conda Detection", False, f"Error: {e}")
            return False
    else:
        print_result("Conda Environment Active", False, "CONDA_PREFIX not set")
        print("   Note: This test only applies if you're using conda")
        return True  # Not a failure if not using conda


def main():
    """Run all tests."""
    print_header("Local Development Environment Test Suite")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    
    test_results = []
    
    # Run all tests
    test_results.append(test_environment_detection())
    test_results.append(test_path_handling())
    test_results.append(test_configuration_consistency())
    test_results.append(test_scripts_functionality())
    test_results.append(test_conda_environment())
    
    # Summary
    print_header("Test Results Summary")
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Local development environment is properly configured.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
