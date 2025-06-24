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
from typing import Dict, Any
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
            "recommendations": [],
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
            "architecture": platform.architecture(),
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
            "prefix": sys.prefix,
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
            "HardwareMonitor": {
                "required": False,
                "description": (
                    "Hardware monitoring package "
                    "(PyHardwareMonitor or HardwareMonitor)"
                ),
            },
            "psutil": {
                "required": False,
                "description": "System and process utilities",
            },
            "asyncio": {"required": True, "description": "Async support (built-in)"},
            "fastapi": {"required": True, "description": "Web framework"},
            "uvicorn": {"required": True, "description": "ASGI server"},
        }

        package_results = {}

        for package, info in packages.items():
            try:
                if package == "asyncio":
                    # Built-in module
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
                    "description": info["description"],
                }

                status = "✅" if installed else ("❌" if info["required"] else "⚠️ ")
                ver_str = f" (v{version})" if version and version != "unknown" else ""
                print(f"   {status} {package}{ver_str} - {info['description']}")

            except Exception as e:
                package_results[package] = {
                    "installed": False,
                    "version": None,
                    "required": info["required"],
                    "error": str(e),
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
                timeout=10,
            )
            if result.returncode == 0:
                runtimes = result.stdout.strip().split("\n")
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
            # import clr is not used directly, but its import is a test
            import clr  # noqa

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
                # Try to import the package
                import HardwareMonitor
                from HardwareMonitor.Util import OpenComputer, ToBuiltinTypes

                package_info["package_imported"] = True
                package_info["version"] = getattr(
                    HardwareMonitor, "__version__", "unknown"
                )
                print(f"      ✅ {package_name} package imported successfully")

                # Test OpenComputer function
                try:
                    package_info["open_computer_available"] = True
                    print("      ✅ OpenComputer function available")

                    # Try to actually open the computer
                    try:
                        computer = OpenComputer()
                        if computer:
                            package_info["computer_opened"] = True
                            print("      ✅ Computer opened successfully")

                            try:
                                computer.Update()
                                package_info["computer_updated"] = True
                                print("      ✅ Computer updated successfully")

                                data = ToBuiltinTypes(computer.Hardware)
                                package_info["data_retrieved"] = True
                                print(
                                    "      ✅ Retrieved data for "
                                    f"{len(data)} components"
                                )

                            except Exception as update_e:
                                package_info["computer_updated"] = False
                                package_info["error_updating"] = str(update_e)
                                print(
                                    "      ❌ Failed to update or get data: "
                                    f"{update_e}"
                                )

                            finally:
                                if computer:
                                    computer.Close()
                        else:
                            package_info["computer_opened"] = False
                            print("      ❌ Failed to open computer " "(returned None)")

                    except Exception as open_e:
                        package_info["computer_opened"] = False
                        package_info["error_opening"] = str(open_e)
                        print(f"      ❌ Exception opening computer: {open_e}")

                except ImportError:
                    package_info["open_computer_available"] = False
                    print("      ❌ OpenComputer function not available")

            except ImportError:
                package_info["package_imported"] = False
                print("      ❌ Package not installed or not in Python path")

            except Exception as e:
                package_info["error"] = str(e)
                print(f"      ❌ An unexpected error occurred: {e}")

            hw_monitor_info["packages_tested"][package_name] = package_info

        self.results["hardware_monitoring"] = hw_monitor_info

    def _check_lhm_dependencies(self):
        """Check for LibreHardwareMonitor dependencies."""
        print("\n🔗 LibreHardwareMonitor Dependencies")
        print("-" * 30)
        lhm_deps = {"found_dll": False, "dll_path": None}
        dll_name = "LibreHardwareMonitorLib.dll"
        search_paths = [
            Path.cwd(),
            Path.cwd() / "server",
            Path.cwd() / "server" / "lib",
            Path(sys.prefix) / "Lib" / "site-packages" / "HardwareMonitor",
        ]
        for path in search_paths:
            if (path / dll_name).exists():
                lhm_deps["found_dll"] = True
                lhm_deps["dll_path"] = str(path / dll_name)
                print(f"   ✅ Found {dll_name} at: {lhm_deps['dll_path']}")
                break
        if not lhm_deps["found_dll"]:
            print(f"   ❌ {dll_name} not found in common search paths.")
        self.results["dependencies"]["lhm_dll"] = lhm_deps

    def _check_dll_availability(self):
        """Check if DLLs are available and accessible."""
        print("\n💾 DLL Availability and Access")
        print("-" * 30)
        # Placeholder for future checks like file permissions
        print("   -> Placeholder for DLL access checks.")

    def _generate_recommendations(self):
        """Generate recommendations based on diagnostics."""
        print("\n💡 Recommendations")
        print("-" * 30)
        recommendations = []
        if not self.results["permissions"].get("is_admin"):
            recommendations.append(
                "Run the script with administrator privileges for full "
                "hardware access."
            )
        if not self.results["dependencies"]["lhm_dll"].get("found_dll"):
            recommendations.append(
                "Ensure LibreHardwareMonitorLib.dll is in the server "
                "directory or a standard path."
            )
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   ✅ No immediate recommendations.")
        self.results["recommendations"] = recommendations

    def _print_summary(self):
        """Print a summary of the diagnostics."""
        print("\n" + "=" * 60)
        print("📋 Diagnostics Summary")
        print("=" * 60)
        # Basic summary printout
        if self.results["permissions"].get("is_admin"):
            print("   - Privileges: Admin")
        else:
            print("   - Privileges: User (Limited)")
        if self.results["dependencies"]["lhm_dll"].get("found_dll"):
            print("   - LHM DLL: Found")
        else:
            print("   - LHM DLL: Not Found")
        print("\nFor full details, check the returned results dictionary.")


def main():
    """Main execution function."""
    diagnostics = SystemDiagnostics()
    results = diagnostics.run_full_diagnostics()

    # Example of how to use results
    if not results["permissions"]["is_admin"]:
        print("\nWarning: Running without admin rights.")


if __name__ == "__main__":
    main()
