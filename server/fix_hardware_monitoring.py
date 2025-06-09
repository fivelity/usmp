#!/usr/bin/env python3
"""
Unified Hardware Monitoring Fix Script
======================================

This script orchestrates all fixes for both LHMSensor System.Management dependency 
issues and HardwareMonitor package installation/permissions problems.
"""

import sys
import os
import subprocess
import platform
import asyncio
from pathlib import Path

# Add the app directory to the Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print(f"{'='*60}")

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{title}")
    print("-" * len(title))

def run_command(command: list, description: str, timeout: int = 300) -> bool:
    """Run a command and return success status."""
    try:
        print(f"   🔄 {description}...")
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        
        if result.returncode == 0:
            print(f"   ✅ {description} - Success")
            return True
        else:
            print(f"   ❌ {description} - Failed")
            if result.stderr:
                print(f"      Error: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {description} - Timeout")
        return False
    except Exception as e:
        print(f"   ❌ {description} - Error: {e}")
        return False

def check_admin_privileges() -> bool:
    """Check if running with admin privileges."""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except Exception:
        return False

async def test_sensor_implementations():
    """Test sensor implementations."""
    print_section("🧪 Testing Sensor Implementations")
    
    try:
        # Import sensor classes
        from sensors import HWSensor, LHMSensor, MockSensor
        from core.config import AppSettings
        
        # Create test settings
        settings = AppSettings()
        
        # Test each sensor
        sensors_to_test = [
            ("HardwareMonitor Package", HWSensor),
            ("LibreHardwareMonitor", LHMSensor),
            ("Mock Sensor", MockSensor)
        ]
        
        working_sensors = []
        
        for name, sensor_class in sensors_to_test:
            try:
                print(f"\n   Testing {name}...")
                sensor = sensor_class()
                await sensor.initialize(settings)
                
                if await sensor.is_available():
                    print(f"   ✅ {name} - Working")
                    working_sensors.append(name)
                else:
                    print(f"   ❌ {name} - Not available")
                    
                await sensor.close()
                
            except Exception as e:
                print(f"   ❌ {name} - Error: {e}")
        
        print(f"\n📊 Summary: {len(working_sensors)}/{len(sensors_to_test)} sensors working")
        for sensor in working_sensors:
            print(f"   • {sensor}")
            
        return len(working_sensors) > 0
        
    except Exception as e:
        print(f"   ❌ Sensor testing failed: {e}")
        return False

def main():
    """Main fix orchestration."""
    print_header("Hardware Monitoring Comprehensive Fix")
    
    # Check admin privileges
    is_admin = check_admin_privileges()
    print(f"👑 Admin privileges: {'✅ YES' if is_admin else '❌ NO'}")
    
    if not is_admin:
        print("⚠️  Warning: Running without admin privileges may limit fix effectiveness")
    
    # Step 1: Run system diagnostics
    print_section("📊 Step 1: System Diagnostics")
    print("   Running comprehensive system diagnostics...")
    
    try:
        import system_diagnostics
        diagnostics = system_diagnostics.SystemDiagnostics()
        diag_results = diagnostics.run_full_diagnostics()
        
        critical_issues = len([r for r in diag_results["recommendations"] if r["priority"] == "critical"])
        high_issues = len([r for r in diag_results["recommendations"] if r["priority"] == "high"])
        
        print(f"   📊 Found {critical_issues} critical and {high_issues} high priority issues")
        
    except Exception as e:
        print(f"   ❌ Diagnostics failed: {e}")
        diag_results = {}
    
    # Step 2: Install dependencies
    print_section("📦 Step 2: Dependency Installation")
    print("   Running automated dependency installer...")
    
    try:
        import dependency_installer
        installer = dependency_installer.DependencyInstaller()
        install_results = installer.install_all_dependencies()
        
        if install_results["success"]:
            print("   ✅ Dependency installation completed successfully")
        else:
            print("   ⚠️  Dependency installation completed with issues")
            
    except Exception as e:
        print(f"   ❌ Dependency installation failed: {e}")
        install_results = {}
    
    # Step 3: .NET Framework fixes (Windows only)
    if platform.system() == "Windows":
        print_section("🪟 Step 3: .NET Framework Fixes")
        
        # Run PowerShell script for .NET Framework
        ps_script = current_dir / "install_dotnet_framework.ps1"
        if ps_script.exists():
            print("   Running .NET Framework installer...")
            success = run_command(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script), "-Force"],
                ".NET Framework setup",
                timeout=600
            )
            if not success:
                print("   ⚠️  .NET Framework setup may require manual intervention")
        else:
            print("   ❌ .NET Framework installer script not found")
    
    # Step 4: Test sensor implementations
    print_section("🧪 Step 4: Sensor Testing")
    
    try:
        # Run sensor tests
        has_working_sensors = asyncio.run(test_sensor_implementations())
        
        if has_working_sensors:
            print("   ✅ At least one sensor implementation is working")
        else:
            print("   ❌ No sensor implementations are working")
            
    except Exception as e:
        print(f"   ❌ Sensor testing failed: {e}")
        has_working_sensors = False
    
    # Step 5: Final recommendations
    print_section("📋 Final Recommendations")
    
    if has_working_sensors:
        print("🎉 SUCCESS: Hardware monitoring is functional!")
        print("   Your system can now monitor hardware sensors.")
        print("\n   Next steps:")
        print("   • Start the backend server: python start_backend.py")
        print("   • Check the web interface for sensor data")
        print("   • Monitor logs for any runtime issues")
    else:
        print("⚠️  PARTIAL SUCCESS: Issues remain")
        print("   Some manual intervention may be required.")
        print("\n   Troubleshooting steps:")
        print("   1. Ensure you're running as Administrator")
        print("   2. Install .NET Framework 4.8 manually if needed")
        print("   3. Check Python architecture (32-bit vs 64-bit)")
        print("   4. Verify antivirus isn't blocking hardware access")
        print("   5. Try different Python versions if issues persist")
    
    # Additional resources
    print("\n🔧 Additional Resources:")
    print("   • Diagnostics: python system_diagnostics.py")
    print("   • Manual install: python dependency_installer.py")
    print("   • .NET fixes: powershell install_dotnet_framework.ps1")
    print("   • Test sensors: python -c 'import asyncio; from fix_hardware_monitoring import test_sensor_implementations; asyncio.run(test_sensor_implementations())'")
    
    print("\n✨ Fix script completed!")
    
    # Return success status
    return has_working_sensors

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Fix script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Fix script failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 