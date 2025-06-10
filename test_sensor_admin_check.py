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
    
    # Test sensor availability
    hw_available = test_hardware_monitor()
    
    print("\n📊 SUMMARY")
    print("-" * 20)
    print(f"Admin privileges: {'✅ YES' if is_admin else '❌ NO'}")
    print(f"HardwareMonitor:  {'✅ Working' if hw_available else '❌ Failed'}")
    
    if not is_admin:
        print("\n💡 RECOMMENDATION:")
        print("   Run this script as Administrator to enable hardware monitoring")
        print("   Right-click → 'Run as administrator'")
    
    if not hw_available:
        print("\n⚠️  No hardware sensors available!")
        print("   The application will use MockSensor only")

if __name__ == "__main__":
    main() 