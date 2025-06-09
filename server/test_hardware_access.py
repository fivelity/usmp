#!/usr/bin/env python3
"""
Quick Hardware Access Test
==========================

Test actual hardware sensor access with current permissions.
"""

import sys
import platform
import ctypes

def check_admin_privileges():
    """Check if running with admin privileges."""
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except Exception:
        return False

def test_pyhardwaremonitor():
    """Test PyHardwareMonitor access."""
    print("🖥️  Testing PyHardwareMonitor...")
    print("-" * 40)
    
    try:
        import HardwareMonitor
        from HardwareMonitor.Util import OpenComputer, ToBuiltinTypes, SensorValueToString
        
        print("   ✅ PyHardwareMonitor imports successful")
        
        # Try to open computer
        computer = OpenComputer(
            cpu=True,
            gpu=True, 
            motherboard=True,
            memory=True,
            storage=True,
            network=True,
            controller=True
        )
        
        if computer:
            print("   ✅ Computer opened successfully")
            
            # Update and get data
            computer.Update()
            data = ToBuiltinTypes(computer.Hardware)
            
            if data:
                hardware_list = data
                print(f"   📊 Found {len(hardware_list)} hardware components:")
                
                total_sensors = 0
                
                for hardware in hardware_list:
                    hw_name = hardware.get('Name', 'Unknown')
                    hw_type = hardware.get('HardwareType', 'Unknown')
                    sensors = hardware.get('Sensors', [])
                    
                    print(f"      🔧 {hw_name} ({hw_type}) - {len(sensors)} sensors")
                    
                    # Show first few sensors as examples
                    for i, sensor in enumerate(sensors[:3]):
                        sensor_name = sensor.get('Name', 'Unknown')
                        sensor_value = sensor.get('Value', 'N/A')
                        sensor_type = sensor.get('SensorType', 'Unknown')
                        
                        # Try to format with SensorValueToString
                        try:
                            formatted_value = SensorValueToString(sensor_value, sensor_type)
                            print(f"         • {sensor_name}: {formatted_value}")
                        except Exception:
                            print(f"         • {sensor_name}: {sensor_value} ({sensor_type})")
                    
                    if len(sensors) > 3:
                        print(f"         ... and {len(sensors) - 3} more sensors")
                    
                    total_sensors += len(sensors)
                
                print(f"   📈 Total sensors available: {total_sensors}")
                
                if total_sensors == 0:
                    print("   ⚠️  No sensors detected - this likely indicates admin privileges are needed")
                else:
                    print("   🎉 Hardware monitoring is fully functional!")
            
            else:
                print("   ❌ No hardware data returned")
                
            computer.Close()
            
        else:
            print("   ❌ Failed to open computer")
            
    except ImportError as e:
        print(f"   ❌ PyHardwareMonitor not available: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error testing PyHardwareMonitor: {e}")
        return False
    
    return True

def test_librehardwaremonitor():
    """Test LibreHardwareMonitor fallback."""
    print("\n🔩 Testing LibreHardwareMonitor Fallback...")
    print("-" * 40)
    
    try:
        import pythonnet
        pythonnet.load("coreclr")
        import clr
        
        # Try to load LibreHardwareMonitorLib.dll
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dll_path = os.path.join(current_dir, "LibreHardwareMonitorLib.dll")
        
        if os.path.exists(dll_path):
            clr.AddReference(dll_path)
            from LibreHardwareMonitor.Hardware import Computer
            
            print("   ✅ LibreHardwareMonitorLib loaded successfully")
            
            computer = Computer()
            computer.IsCpuEnabled = True
            computer.IsGpuEnabled = True
            computer.IsMemoryEnabled = True
            computer.IsMotherboardEnabled = True
            computer.IsStorageEnabled = True
            
            computer.Open()
            hardware_list = list(computer.Hardware)
            
            print(f"   📊 Found {len(hardware_list)} hardware components via LHM")
            
            if len(hardware_list) == 0:
                print("   ⚠️  No hardware detected - admin privileges likely needed")
            else:
                print("   🎉 LibreHardwareMonitor fallback is working!")
            
            computer.Close()
            return True
            
        else:
            print("   ❌ LibreHardwareMonitorLib.dll not found")
            return False
            
    except Exception as e:
        print(f"   ❌ LibreHardwareMonitor test failed: {e}")
        return False

def main():
    """Run hardware access tests."""
    print("🧪 Hardware Access Test")
    print("=" * 50)
    
    # Check admin privileges
    is_admin = check_admin_privileges()
    print(f"👑 Admin privileges: {'✅ YES' if is_admin else '❌ NO'}")
    
    if not is_admin:
        print("⚠️  Note: PyHardwareMonitor docs state admin privileges are required for full access")
    
    # Test PyHardwareMonitor
    pyhm_works = test_pyhardwaremonitor()
    
    # Test LibreHardwareMonitor fallback
    lhm_works = test_librehardwaremonitor()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    
    if pyhm_works:
        print("✅ PyHardwareMonitor: Working")
    else:
        print("❌ PyHardwareMonitor: Not working")
    
    if lhm_works:
        print("✅ LibreHardwareMonitor: Working")
    else:
        print("❌ LibreHardwareMonitor: Not working")
    
    if pyhm_works or lhm_works:
        print("\n🎉 SUCCESS: At least one hardware monitoring method is functional!")
        if not is_admin:
            print("💡 For full sensor access, run as Administrator")
    else:
        print("\n❌ FAILURE: No hardware monitoring methods are working")
        print("💡 Try running as Administrator and check installations")

if __name__ == "__main__":
    main() 