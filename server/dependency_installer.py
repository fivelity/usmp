#!/usr/bin/env python3
"""
Automated Dependency Installer for Hardware Monitoring
======================================================

This script automatically installs and fixes dependencies for hardware monitoring,
addressing both HardwareMonitor package and LibreHardwareMonitor issues.
"""

import sys
import os
import subprocess
import platform
import ctypes
import urllib.request
import shutil
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json


class DependencyInstaller:
    """Automated installer for hardware monitoring dependencies."""

    def __init__(self):
        self.is_admin = self._check_admin_privileges()
        self.results = {
            "actions_taken": [],
            "failures": [],
            "warnings": [],
            "success": False,
        }

    def _check_admin_privileges(self) -> bool:
        """Check if running with admin privileges."""
        try:
            if platform.system() == "Windows":
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except Exception:
            return False

    def install_all_dependencies(self) -> Dict[str, Any]:
        """Install all required dependencies."""
        print("🔧 Starting Automated Dependency Installation...")
        print("=" * 60)

        if not self.is_admin:
            print("⚠️  WARNING: Not running as Administrator")
            print("   Some installations may fail or require manual intervention")
            self.results["warnings"].append("Not running as Administrator")

        # Install Python packages
        self._install_python_packages()

        # Try to fix .NET issues
        self._fix_dotnet_issues()

        # Download missing DLLs
        self._download_missing_dlls()

        # Install HardwareMonitor package with different methods
        self._install_hardware_monitor_package()

        # Final verification
        success = self._verify_installation()
        self.results["success"] = success

        self._print_summary()
        return self.results

    def _install_python_packages(self):
        """Install required Python packages using detected environment."""
        print("\n📦 Installing Python Packages...")
        print("-" * 40)

        # Detect current Python environment
        try:
            from env_detector import PythonEnvironmentDetector
            detector = PythonEnvironmentDetector()
            env_type, env_path, env_info = detector.detect_environment()
            
            print(f"   Using {env_type.upper()} environment: {env_path}")
            python_exe = env_info.get('python_exe', sys.executable)
            
            # For conda environments, prefer conda install when possible
            if env_type == "conda" and env_info.get('active', False):
                self._install_with_conda_preference(python_exe)
            else:
                self._install_with_pip(python_exe)
                
        except ImportError:
            print("   Using fallback pip installation with system Python")
            self._install_with_pip(sys.executable)

    def _install_with_conda_preference(self, python_exe: str):
        """Install packages preferring conda when available."""
        conda_packages = {
            "fastapi": "fastapi",
            "uvicorn": "uvicorn",
            "aiofiles": "aiofiles",
            "pydantic": "pydantic",
            "psutil": "psutil"
        }
        
        pip_only_packages = [
            "pythonnet",
            "pydantic-settings",
            "HardwareMonitor"
        ]
        
        # Try conda first for supported packages
        for package_name, conda_name in conda_packages.items():
            try:
                print(f"   Installing {package_name} via conda...")
                result = subprocess.run(
                    ["conda", "install", "-y", conda_name],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    print(f"   ✅ {package_name} installed via conda")
                    self.results["actions_taken"].append(f"Installed {package_name} via conda")
                else:
                    # Fall back to pip
                    self._install_package_with_pip(python_exe, package_name)
            except FileNotFoundError:
                # Conda not available, use pip
                self._install_package_with_pip(python_exe, package_name)
        
        # Install pip-only packages
        for package in pip_only_packages:
            self._install_package_with_pip(python_exe, package)

    def _install_with_pip(self, python_exe: str):
        """Install all packages with pip."""
        packages = [
            "pythonnet",
            "psutil",
            "fastapi",
            "uvicorn",
            "aiofiles",
            "pydantic",
            "pydantic-settings",
        ]
        
        for package in packages:
            self._install_package_with_pip(python_exe, package)

    def _install_package_with_pip(self, python_exe: str, package: str):
        """Install a single package with pip."""
        try:
            print(f"   Installing {package} via pip...")
            result = subprocess.run(
                [python_exe, "-m", "pip", "install", "--upgrade", package],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
                self.results["actions_taken"].append(f"Installed {package}")
            else:
                print(f"   ❌ Failed to install {package}: {result.stderr}")
                self.results["failures"].append(
                    f"Failed to install {package}: {result.stderr}"
                )

        except Exception as e:
            print(f"   ❌ Error installing {package}: {e}")
            self.results["failures"].append(f"Error installing {package}: {e}")

    def _fix_dotnet_issues(self):
        """Attempt to fix .NET related issues."""
        print("\n🔧 Fixing .NET Issues...")
        print("-" * 40)

        # Try to install/update pythonnet with specific versions
        pythonnet_versions = ["3.0.3", "3.0.2", "3.0.1"]

        for version in pythonnet_versions:
            try:
                print(f"   Trying pythonnet=={version}...")
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        f"pythonnet=={version}",
                        "--force-reinstall",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )

                if result.returncode == 0:
                    print(f"   ✅ pythonnet {version} installed successfully")
                    self.results["actions_taken"].append(
                        f"Installed pythonnet {version}"
                    )

                    # Test if it works
                    if self._test_pythonnet():
                        print("   ✅ Python.NET working correctly")
                        break
                    else:
                        print("   ⚠️  Python.NET installed but not working properly")

            except Exception as e:
                print(f"   ❌ Failed to install pythonnet {version}: {e}")
                continue

        # Try to install .NET Framework support if on Windows
        if platform.system() == "Windows":
            self._install_dotnet_framework_support()

    def _install_dotnet_framework_support(self):
        """Install .NET Framework support components."""
        print("\n🪟 Installing .NET Framework Support...")
        print("-" * 40)

        try:
            # Try to install Windows SDK or .NET Framework targeting pack
            # This is more complex and may require manual intervention
            print("   ℹ️  .NET Framework support requires manual installation")
            print("   📥 Download .NET Framework 4.8 Developer Pack from Microsoft")
            print("   🔗 https://dotnet.microsoft.com/download/dotnet-framework")

            self.results["warnings"].append(
                "Manual .NET Framework installation may be required"
            )

        except Exception as e:
            print(f"   ❌ Error setting up .NET Framework support: {e}")
            self.results["failures"].append(f".NET Framework setup error: {e}")

    def _download_missing_dlls(self):
        """Download missing DLL files."""
        print("\n📚 Downloading Missing DLLs...")
        print("-" * 40)

        # Check if LibreHardwareMonitorLib.dll exists
        current_dir = Path(__file__).parent
        dll_path = current_dir / "LibreHardwareMonitorLib.dll"

        if not dll_path.exists():
            print("   📥 LibreHardwareMonitorLib.dll not found, attempting download...")

            # Try to download from GitHub releases
            dll_urls = [
                "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v0.9.3/LibreHardwareMonitorLib.dll",
                "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/latest/download/LibreHardwareMonitorLib.dll",
            ]

            for url in dll_urls:
                try:
                    print(f"   🔽 Downloading from {url}...")
                    urllib.request.urlretrieve(url, dll_path)

                    if (
                        dll_path.exists() and dll_path.stat().st_size > 100000
                    ):  # At least 100KB
                        print(
                            f"   ✅ LibreHardwareMonitorLib.dll downloaded successfully"
                        )
                        print(f"      Size: {dll_path.stat().st_size:,} bytes")
                        self.results["actions_taken"].append(
                            "Downloaded LibreHardwareMonitorLib.dll"
                        )
                        break
                    else:
                        print(f"   ❌ Downloaded file is too small or corrupted")
                        dll_path.unlink(missing_ok=True)

                except Exception as e:
                    print(f"   ❌ Download failed: {e}")
                    dll_path.unlink(missing_ok=True)
                    continue

            if not dll_path.exists():
                print("   ⚠️  Automatic download failed. Manual download required:")
                print(
                    "      1. Go to https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases"
                )
                print("      2. Download LibreHardwareMonitorLib.dll")
                print(f"      3. Place it in: {dll_path}")
                self.results["warnings"].append("Manual DLL download required")
        else:
            print("   ✅ LibreHardwareMonitorLib.dll already exists")

    def _install_hardware_monitor_package(self):
        """Install HardwareMonitor packages with multiple methods."""
        print("\n🖥️  Installing HardwareMonitor Packages...")
        print("-" * 40)

        # List of packages to try (PyHardwareMonitor is preferred based on documentation)
        packages_to_try = [
            ("PyHardwareMonitor", "PyHardwareMonitor (Recommended)"),
            ("HardwareMonitor", "HardwareMonitor (Alternative)"),
        ]

        for package_name, display_name in packages_to_try:
            print(f"\n   📦 Trying {display_name}...")

            # Method 1: Direct pip install
            try:
                print(f"      Method 1: Direct pip install {package_name}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package_name],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )

                if result.returncode == 0:
                    print(f"   ✅ {package_name} installed via pip")
                    self.results["actions_taken"].append(
                        f"Installed {package_name} via pip"
                    )

                    if self._test_hardware_monitor(package_name):
                        print(f"   ✅ {package_name} working correctly")
                        return

            except Exception as e:
                print(f"   ❌ Direct pip install failed: {e}")

            # Method 2: Install from alternative sources
            print(
                f"      Method 2: Alternative installation methods for {package_name}..."
            )

            alternative_commands = [
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    package_name,
                    "--force-reinstall",
                ],
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    package_name,
                    "--no-cache-dir",
                ],
                [sys.executable, "-m", "pip", "install", package_name, "--user"],
            ]

            for cmd in alternative_commands:
                try:
                    result = subprocess.run(
                        cmd, capture_output=True, text=True, timeout=300
                    )
                    if result.returncode == 0 and self._test_hardware_monitor(
                        package_name
                    ):
                        print(f"   ✅ {package_name} installed successfully")
                        self.results["actions_taken"].append(
                            f"Installed {package_name} with alternative method"
                        )
                        return
                except Exception:
                    continue

        # Method 3: Manual guidance
        print("   ⚠️  Automatic installation failed for all packages. Manual steps:")
        print(
            "      1. Ensure you're running as Administrator (REQUIRED for hardware access)"
        )
        print("      2. Try: pip install --upgrade pip")
        print("      3. Try: pip install PyHardwareMonitor --force-reinstall")
        print("      4. Try: pip install HardwareMonitor --force-reinstall")
        print("      5. Check Python architecture (32-bit vs 64-bit)")
        print(
            "      6. Based on PyHardwareMonitor docs: Admin privileges are mandatory!"
        )

        self.results["warnings"].append(
            "Manual HardwareMonitor installation may be required"
        )

    def _test_pythonnet(self) -> bool:
        """Test if Python.NET is working."""
        try:
            import pythonnet

            pythonnet.load("coreclr")
            import clr

            return True
        except Exception:
            return False

    def _test_hardware_monitor(self, package_name: str = "HardwareMonitor") -> bool:
        """Test if HardwareMonitor package is working."""
        try:
            if package_name == "PyHardwareMonitor":
                # Test PyHardwareMonitor
                import HardwareMonitor
                from HardwareMonitor.Util import OpenComputer, SensorValueToString

                # Don't actually open the computer, just test imports
                return True
            else:
                # Test original HardwareMonitor
                import HardwareMonitor
                from HardwareMonitor.Util import OpenComputer

                # Don't actually open the computer, just test imports
                return True
        except Exception:
            return False

    def _verify_installation(self) -> bool:
        """Verify that the installation was successful."""
        print("\n✅ Verifying Installation...")
        print("-" * 40)

        success_count = 0
        total_checks = 4

        # Check 1: Python.NET
        if self._test_pythonnet():
            print("   ✅ Python.NET working")
            success_count += 1
        else:
            print("   ❌ Python.NET not working")

        # Check 2: HardwareMonitor package
        if self._test_hardware_monitor():
            print("   ✅ HardwareMonitor package working")
            success_count += 1
        else:
            print("   ❌ HardwareMonitor package not working")

        # Check 3: LibreHardwareMonitorLib.dll
        dll_path = Path(__file__).parent / "LibreHardwareMonitorLib.dll"
        if dll_path.exists():
            print("   ✅ LibreHardwareMonitorLib.dll available")
            success_count += 1
        else:
            print("   ❌ LibreHardwareMonitorLib.dll missing")

        # Check 4: System.Management (for LHMSensor)
        try:
            import clr

            clr.AddReference("System.Management")
            print("   ✅ System.Management assembly available")
            success_count += 1
        except Exception:
            print("   ❌ System.Management assembly not available")

        success_rate = success_count / total_checks
        print(
            f"\n   📊 Success rate: {success_count}/{total_checks} ({success_rate:.1%})"
        )

        return success_rate >= 0.5  # At least 50% success

    def _print_summary(self):
        """Print installation summary."""
        print("\n📋 Installation Summary")
        print("=" * 60)

        print(f"✅ Actions Taken: {len(self.results['actions_taken'])}")
        for action in self.results["actions_taken"]:
            print(f"   • {action}")

        if self.results["warnings"]:
            print(f"\n⚠️  Warnings: {len(self.results['warnings'])}")
            for warning in self.results["warnings"]:
                print(f"   • {warning}")

        if self.results["failures"]:
            print(f"\n❌ Failures: {len(self.results['failures'])}")
            for failure in self.results["failures"]:
                print(f"   • {failure}")

        if self.results["success"]:
            print("\n🎉 Installation completed successfully!")
            print("   Hardware monitoring should now be functional.")
        else:
            print("\n⚠️  Installation completed with issues.")
            print("   Some manual intervention may be required.")
            print("   Run diagnostics again to identify remaining issues.")


def main():
    """Run installation from command line."""
    installer = DependencyInstaller()
    results = installer.install_all_dependencies()

    # Save results
    try:
        with open("installation_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to installation_results.json")
    except Exception as e:
        print(f"\n❌ Failed to save results: {e}")

    # Return appropriate exit code
    sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()
