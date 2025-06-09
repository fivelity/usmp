#!/usr/bin/env python3
"""
Test script to show admin privilege requirements and sensor detection behavior.
"""

import sys
import os
import ctypes

def check_admin_privileges():
    """Check if we're running with admin privileges."""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        return is_admin
    except Exception as e:
        print(f"Error checking admin privileges: {e}")
        return False

def test_hardware_monitor():
    """Test HardwareMonitor package availability."""
    print("\n🔍 Testing HardwareMonitor Package")
    print("-" * 40)
    
    try:
        import HardwareMonitor
        print("✅ HardwareMonitor package imported successfully")
        
        from HardwareMonitor.Util import OpenComputer
        print("✅ OpenComputer imported successfully")
        
        # Try to create computer (this may fail without admin)
        try:
            computer = OpenComputer(cpu=True, gpu=True, memory=True)
            if computer:
                print("✅ Computer instance created successfully")
                try:
                    computer.Update()
                    hardware_list = list(computer.Hardware)
                    print(f"✅ Found {len(hardware_list)} hardware components")
                    
                    if hardware_list:
                        for hw in hardware_list[:3]:  # Show first 3
                            print(f"   • {hw.Name}")
                    return True
                except Exception as e:
                    print(f"❌ Computer update failed: {e}")
                    return False
            else:
                print("❌ Computer creation returned None")
                return False
        except Exception as e:
            print(f"❌ Computer creation failed: {e}")
            return False
    except Exception as e:
        print(f"❌ HardwareMonitor import failed: {e}")
        return False

def test_lhm_sensor():
    """Test LHMSensor availability."""
    print("\n🔍 Testing LHMSensor (LibreHardwareMonitor)")
    print("-" * 40)
    
    try:
        import pythonnet
        pythonnet.load("coreclr")
        import clr
        print("✅ Python.NET loaded successfully")
        
        # Test System.Management
        try:
            clr.AddReference("System.Management")
            print("✅ System.Management available")
        except Exception as e:
            print(f"❌ System.Management not available: {e}")
        
        # Test DLL loading
        dll_path = os.path.abspath("LibreHardwareMonitorLib.dll")
        if os.path.exists(dll_path):
            print(f"✅ Found LibreHardwareMonitorLib.dll at: {dll_path}")
            
            try:
                clr.AddReference(dll_path)
                from LibreHardwareMonitor.Hardware import Computer
                print("✅ LibreHardwareMonitor classes imported")
                
                # Try to create computer
                computer = Computer()
                computer.IsCpuEnabled = True
                computer.IsGpuEnabled = True
                computer.IsMemoryEnabled = True
                
                # Careful with motherboard
                try:
                    clr.AddReference("System.Management")
                    computer.IsMotherboardEnabled = True
                    print("✅ Motherboard sensors enabled")
                except Exception:
                    computer.IsMotherboardEnabled = False
                    print("⚠️  Motherboard sensors disabled (System.Management missing)")
                
                computer.Open()
                hardware_list = list(computer.Hardware)
                computer.Close()
                
                print(f"✅ Found {len(hardware_list)} hardware components")
                
                if hardware_list:
                    for hw in hardware_list[:3]:  # Show first 3
                        print(f"   • {hw.Name}")
                return True
                
            except Exception as e:
                print(f"❌ LHM hardware access failed: {e}")
                return False
        else:
            print(f"❌ LibreHardwareMonitorLib.dll not found at: {dll_path}")
            return False
    except Exception as e:
        print(f"❌ LHMSensor test failed: {e}")
        return False

def main():
    print("🔍 Hardware Sensor Admin Privilege Test")
    print("=" * 50)
    
    # Check admin privileges
    is_admin = check_admin_privileges()
    if is_admin:
        print("👑 ✅ Running with Administrator privileges")
    else:
        print("👤 ❌ Running without Administrator privileges")
        print("   ⚠️  Hardware monitoring may be limited or unavailable")
    
    # Test both sensor types
    hw_available = test_hardware_monitor()
    lhm_available = test_lhm_sensor()
    
    print("\n📊 SUMMARY")
    print("-" * 20)
    print(f"Admin privileges: {'✅ YES' if is_admin else '❌ NO'}")
    print(f"HardwareMonitor:  {'✅ Working' if hw_available else '❌ Failed'}")
    print(f"LHMSensor:        {'✅ Working' if lhm_available else '❌ Failed'}")
    
    if not is_admin:
        print("\n💡 RECOMMENDATION:")
        print("   Run this script as Administrator to enable hardware monitoring")
        print("   Right-click → 'Run as administrator'")
    
    if not hw_available and not lhm_available:
        print("\n⚠️  No hardware sensors available!")
        print("   The application will use MockSensor only")

if __name__ == "__main__":
    main() 