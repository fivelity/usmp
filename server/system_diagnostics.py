#!/usr/bin/env python3
"""
Comprehensive System Diagnostics for Hardware Monitoring
========================================================

This script performs thorough diagnostics of the hardware monitoring system,
identifying issues with dependencies, permissions, and configurations.
"""

import sys
import os
import subprocess
import platform
import ctypes
from typing import Dict, List, Any, Tuple
import importlib.util
from pathlib import Path

class SystemDiagnostics:
    """Comprehensive diagnostics for hardware monitoring system."""
    
    def __init__(self):
        self.results = {
            "system_info": {},
            "python_environment": {},
            "dependencies": {},
            "permissions": {},
            "hardware_monitoring": {},
            "recommendations": []
        }
        
    def run_full_diagnostics(self) -> Dict[str, Any]:
        """Run all diagnostic checks."""
        print("🔍 Starting Hardware Monitoring System Diagnostics...")
        print("=" * 60)
        
        self._check_system_info()
        self._check_python_environment()
        self._check_admin_privileges()
        self._check_python_packages()
        self._check_dotnet_environment()
        self._check_hardware_monitor_package()
        self._check_lhm_dependencies()
        self._check_dll_availability()
        self._generate_recommendations()
        
        self._print_summary()
        return self.results
    
    def _check_system_info(self):
        """Check basic system information."""
        print("\n📊 System Information")
        print("-" * 30)
        
        info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture()
        }
        
        self.results["system_info"] = info
        
        for key, value in info.items():
            print(f"   {key.capitalize()}: {value}")
    
    def _check_python_environment(self):
        """Check Python environment details."""
        print("\n🐍 Python Environment")
        print("-" * 30)
        
        env = {
            "version": sys.version,
            "executable": sys.executable,
            "platform": sys.platform,
            "path": sys.path[:3],  # First 3 paths
            "prefix": sys.prefix
        }
        
        self.results["python_environment"] = env
        
        print(f"   Version: {sys.version.split()[0]}")
        print(f"   Executable: {sys.executable}")
        print(f"   Platform: {sys.platform}")
        print(f"   Prefix: {sys.prefix}")
    
    def _check_admin_privileges(self):
        """Check if running with admin privileges."""
        print("\n👑 Administrator Privileges")
        print("-" * 30)
        
        is_admin = False
        try:
            if platform.system() == "Windows":
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            else:
                is_admin = os.geteuid() == 0
        except Exception as e:
            print(f"   ❌ Error checking admin privileges: {e}")
        
        self.results["permissions"]["is_admin"] = is_admin
        
        if is_admin:
            print("   ✅ Running with Administrator privileges")
        else:
            print("   ⚠️  NOT running with Administrator privileges")
            print("      Hardware monitoring may have limited functionality")
    
    def _check_python_packages(self):
        """Check essential Python packages."""
        print("\n📦 Python Package Dependencies")
        print("-" * 30)
        
        packages = {
            "pythonnet": {"required": True, "description": "Python.NET integration"},
            "HardwareMonitor": {"required": False, "description": "Hardware monitoring package (PyHardwareMonitor or HardwareMonitor)"},
            "psutil": {"required": False, "description": "System and process utilities"},
            "asyncio": {"required": True, "description": "Async support (built-in)"},
            "fastapi": {"required": True, "description": "Web framework"},
            "uvicorn": {"required": True, "description": "ASGI server"}
        }
        
        package_results = {}
        
        for package, info in packages.items():
            try:
                if package == "asyncio":
                    # Built-in module
                    import asyncio
                    version = "built-in"
                    installed = True
                else:
                    spec = importlib.util.find_spec(package)
                    if spec is not None:
                        mod = importlib.import_module(package)
                        version = getattr(mod, "__version__", "unknown")
                        installed = True
                    else:
                        installed = False
                        version = None
                
                package_results[package] = {
                    "installed": installed,
                    "version": version,
                    "required": info["required"],
                    "description": info["description"]
                }
                
                status = "✅" if installed else ("❌" if info["required"] else "⚠️ ")
                ver_str = f" (v{version})" if version and version != "unknown" else ""
                print(f"   {status} {package}{ver_str} - {info['description']}")
                
            except Exception as e:
                package_results[package] = {
                    "installed": False,
                    "version": None,
                    "required": info["required"],
                    "error": str(e)
                }
                status = "❌" if info["required"] else "⚠️ "
                print(f"   {status} {package} - Error: {e}")
        
        self.results["dependencies"]["python_packages"] = package_results
    
    def _check_dotnet_environment(self):
        """Check .NET environment."""
        print("\n🔧 .NET Environment")
        print("-" * 30)
        
        dotnet_info = {}
        
        # Check for .NET runtime
        try:
            result = subprocess.run(
                ["dotnet", "--list-runtimes"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                runtimes = result.stdout.strip().split('\n')
                dotnet_info["runtimes"] = runtimes
                print(f"   ✅ .NET runtimes found ({len(runtimes)} installed)")
                for runtime in runtimes[:3]:  # Show first 3
                    print(f"      • {runtime}")
                if len(runtimes) > 3:
                    print(f"      ... and {len(runtimes) - 3} more")
            else:
                dotnet_info["runtimes"] = []
                print("   ⚠️  .NET runtime check failed")
        except Exception as e:
            dotnet_info["error"] = str(e)
            print(f"   ❌ .NET runtime check error: {e}")
        
        # Check for Python.NET specifically
        try:
            import clr
            dotnet_info["pythonnet_clr"] = True
            print("   ✅ Python.NET CLR integration working")
        except Exception as e:
            dotnet_info["pythonnet_clr"] = False
            print(f"   ❌ Python.NET CLR integration failed: {e}")
        
        self.results["dependencies"]["dotnet"] = dotnet_info
    
    def _check_hardware_monitor_package(self):
        """Check HardwareMonitor Python packages specifically."""
        print("\n🖥️  HardwareMonitor Packages")
        print("-" * 30)
        
        hw_monitor_info = {"packages_tested": {}}
        
        # Test both PyHardwareMonitor and HardwareMonitor packages
        packages_to_test = ["PyHardwareMonitor", "HardwareMonitor"]
        
        for package_name in packages_to_test:
            print(f"\n   📦 Testing {package_name}...")
            package_info = {}
            
            try:
                # Try to import the package (note: both use 'HardwareMonitor' module name)
                import HardwareMonitor
                package_info["package_imported"] = True
                package_info["version"] = getattr(HardwareMonitor, "__version__", "unknown")
                print(f"      ✅ {package_name} package imported successfully")
                
                # Test OpenComputer function
                try:
                    from HardwareMonitor.Util import OpenComputer
                    package_info["open_computer_available"] = True
                    print(f"      ✅ OpenComputer function available")
                    
                    # Test SensorValueToString (specific to PyHardwareMonitor)
                    if package_name == "PyHardwareMonitor":
                        try:
                            from HardwareMonitor.Util import SensorValueToString
                            package_info["sensor_value_to_string_available"] = True
                            print(f"      ✅ SensorValueToString function available (PyHardwareMonitor feature)")
                        except Exception:
                            package_info["sensor_value_to_string_available"] = False
                            print(f"      ⚠️  SensorValueToString not available (might not be PyHardwareMonitor)")
                    
                    # Try to actually open the computer (admin privileges test)
                    try:
                        computer = OpenComputer()
                        if computer:
                            package_info["computer_opened"] = True
                            print(f"      ✅ Computer opened successfully")
                            
                            # Try to update and get data
                            try:
                                computer.Update()
                                from HardwareMonitor.Util import ToBuiltinTypes
                                data = ToBuiltinTypes(computer.Hardware)
                                hw_count = len(data) if data else 0
                                package_info["hardware_count"] = hw_count
                                print(f"      ✅ Found {hw_count} hardware components")
                            except Exception as e:
                                package_info["data_access_error"] = str(e)
                                print(f"      ⚠️  Data access issue: {e}")
                        else:
                            package_info["computer_opened"] = False
                            print(f"      ❌ Computer.Open() returned None (likely admin privileges required)")
                    except Exception as e:
                        package_info["open_error"] = str(e)
                        print(f"      ❌ Failed to open computer: {e}")
                        
                except Exception as e:
                    package_info["open_computer_error"] = str(e)
                    print(f"      ❌ OpenComputer import failed: {e}")
                
                # If we successfully imported, we found a working package
                hw_monitor_info["working_package"] = package_name
                hw_monitor_info.update(package_info)  # Copy successful package info to main level
                break  # Stop testing other packages
                    
            except ImportError as e:
                package_info["package_imported"] = False
                package_info["import_error"] = str(e)
                print(f"      ❌ {package_name} package not available: {e}")
            except Exception as e:
                package_info["package_imported"] = False
                package_info["error"] = str(e)
                print(f"      ❌ {package_name} package error: {e}")
            
            hw_monitor_info["packages_tested"][package_name] = package_info
        
        # Overall status
        if not hw_monitor_info.get("working_package"):
            print(f"\n   ❌ No HardwareMonitor packages found")
            print(f"      💡 Try: pip install PyHardwareMonitor")
            print(f"      💡 Alternative: pip install HardwareMonitor") 
            print(f"      ⚠️  Admin privileges required for hardware access!")
        
        self.results["hardware_monitoring"]["hw_package"] = hw_monitor_info
    
    def _check_lhm_dependencies(self):
        """Check LibreHardwareMonitor dependencies."""
        print("\n🔩 LibreHardwareMonitor Dependencies")
        print("-" * 30)
        
        lhm_info = {}
        
        # Check Python.NET
        try:
            import pythonnet
            pythonnet.load("coreclr")
            lhm_info["pythonnet_loaded"] = True
            print("   ✅ Python.NET loaded successfully")
            
            import clr
            lhm_info["clr_available"] = True
            print("   ✅ CLR module available")
            
            # Test System.Management specifically
            try:
                clr.AddReference("System.Management")
                lhm_info["system_management"] = True
                print("   ✅ System.Management assembly loaded")
            except Exception as e:
                lhm_info["system_management"] = False
                lhm_info["system_management_error"] = str(e)
                print(f"   ❌ System.Management assembly failed: {e}")
                print("      This is the main LHMSensor issue!")
            
        except Exception as e:
            lhm_info["pythonnet_error"] = str(e)
            print(f"   ❌ Python.NET error: {e}")
        
        self.results["hardware_monitoring"]["lhm_dependencies"] = lhm_info
    
    def _check_dll_availability(self):
        """Check for LibreHardwareMonitorLib.dll."""
        print("\n📚 DLL Dependencies")
        print("-" * 30)
        
        dll_info = {}
        
        # Look for LibreHardwareMonitorLib.dll
        current_dir = Path(__file__).parent
        dll_paths = [
            current_dir / "LibreHardwareMonitorLib.dll",
            current_dir.parent / "LibreHardwareMonitorLib.dll",
            Path("LibreHardwareMonitorLib.dll")
        ]
        
        dll_found = False
        for dll_path in dll_paths:
            if dll_path.exists():
                dll_info["dll_path"] = str(dll_path.absolute())
                dll_info["dll_size"] = dll_path.stat().st_size
                dll_found = True
                print(f"   ✅ LibreHardwareMonitorLib.dll found: {dll_path}")
                print(f"      Size: {dll_path.stat().st_size:,} bytes")
                break
        
        if not dll_found:
            dll_info["dll_found"] = False
            print("   ❌ LibreHardwareMonitorLib.dll not found")
            print("      Searched in:")
            for path in dll_paths:
                print(f"      • {path}")
        
        self.results["dependencies"]["dll"] = dll_info
    
    def _generate_recommendations(self):
        """Generate specific recommendations based on findings."""
        print("\n💡 Recommendations")
        print("-" * 30)
        
        recommendations = []
        
        # Admin privileges
        if not self.results["permissions"].get("is_admin", False):
            recommendations.append({
                "priority": "high",
                "category": "permissions",
                "issue": "Not running as Administrator",
                "solution": "Run the application as Administrator for full hardware access",
                "command": "Right-click and 'Run as Administrator'"
            })
        
        # Python packages
        packages = self.results["dependencies"].get("python_packages", {})
        for pkg, info in packages.items():
            if info.get("required", False) and not info.get("installed", False):
                recommendations.append({
                    "priority": "critical",
                    "category": "dependencies",
                    "issue": f"Required package '{pkg}' not installed",
                    "solution": f"Install {pkg}",
                    "command": f"pip install {pkg}"
                })
        
        # HardwareMonitor package issues
        hw_pkg = self.results["hardware_monitoring"].get("hw_package", {})
        if not hw_pkg.get("package_imported", False):
            recommendations.append({
                "priority": "high",
                "category": "dependencies",
                "issue": "HardwareMonitor package not available",
                "solution": "Install HardwareMonitor package",
                "command": "pip install HardwareMonitor"
            })
        
        # System.Management issue
        lhm_deps = self.results["hardware_monitoring"].get("lhm_dependencies", {})
        if not lhm_deps.get("system_management", False):
            recommendations.append({
                "priority": "high",
                "category": "dotnet",
                "issue": "System.Management assembly not available",
                "solution": "Install .NET Framework or enable System.Management",
                "command": "Download .NET Framework 4.8 from Microsoft"
            })
        
        # DLL missing
        dll_info = self.results["dependencies"].get("dll", {})
        if not dll_info.get("dll_found", True):
            recommendations.append({
                "priority": "medium",
                "category": "files",
                "issue": "LibreHardwareMonitorLib.dll not found",
                "solution": "Download LibreHardwareMonitorLib.dll to project directory",
                "command": "Download from LibreHardwareMonitor releases"
            })
        
        self.results["recommendations"] = recommendations
        
        # Print recommendations
        for i, rec in enumerate(recommendations, 1):
            priority_icon = {"critical": "🚨", "high": "⚠️ ", "medium": "💡", "low": "ℹ️ "}
            icon = priority_icon.get(rec["priority"], "•")
            print(f"   {icon} {rec['issue']}")
            print(f"      Solution: {rec['solution']}")
            if "command" in rec:
                print(f"      Command: {rec['command']}")
            print()
    
    def _print_summary(self):
        """Print diagnostic summary."""
        print("\n📋 Diagnostic Summary")
        print("=" * 60)
        
        # Count issues
        critical_issues = len([r for r in self.results["recommendations"] if r["priority"] == "critical"])
        high_issues = len([r for r in self.results["recommendations"] if r["priority"] == "high"])
        medium_issues = len([r for r in self.results["recommendations"] if r["priority"] == "medium"])
        
        print(f"🚨 Critical Issues: {critical_issues}")
        print(f"⚠️  High Priority Issues: {high_issues}")
        print(f"💡 Medium Priority Issues: {medium_issues}")
        
        # Overall status
        if critical_issues > 0:
            print("\n❌ System has critical issues that prevent hardware monitoring")
        elif high_issues > 0:
            print("\n⚠️  System has issues that may limit hardware monitoring functionality")
        elif medium_issues > 0:
            print("\n💡 System is mostly functional but has some recommended improvements")
        else:
            print("\n✅ System appears to be configured correctly for hardware monitoring")
        
        print(f"\nFor detailed results, check the returned dictionary.")


def main():
    """Run diagnostics from command line."""
    diagnostics = SystemDiagnostics()
    results = diagnostics.run_full_diagnostics()
    
    # Optional: Save results to file
    import json
    try:
        with open("diagnostic_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to diagnostic_results.json")
    except Exception as e:
        print(f"\n❌ Failed to save results: {e}")


if __name__ == "__main__":
    main() 