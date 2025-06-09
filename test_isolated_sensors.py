#!/usr/bin/env python3
"""
Test script to verify sensors in isolation to avoid DLL conflicts.
"""

import subprocess
import sys
import os

def test_hardware_monitor_isolated():
    """Test HardwareMonitor in a separate process to avoid DLL conflicts."""
    print("🔍 Testing HardwareMonitor in isolation...")
    
    test_script = '''
import sys
try:
    import HardwareMonitor
    from HardwareMonitor.Util import OpenComputer
    
    computer = OpenComputer(cpu=True, gpu=True, memory=True)
    if computer:
        computer.Update()
        hardware_list = list(computer.Hardware)
        print(f"SUCCESS:{len(hardware_list)}")
        for hw in hardware_list[:3]:
            print(f"HARDWARE:{hw.Name}")
    else:
        print("FAILED:Computer creation returned None")
except Exception as e:
    print(f"FAILED:{e}")
'''
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith("SUCCESS:"):
                    count = int(line.split(":")[1])
                    print(f"   ✅ Found {count} hardware components")
                    return True
                elif line.startswith("HARDWARE:"):
                    hw_name = line.split(":", 1)[1]
                    print(f"      • {hw_name}")
                elif line.startswith("FAILED:"):
                    error = line.split(":", 1)[1]
                    print(f"   ❌ Failed: {error}")
                    return False
        else:
            print(f"   ❌ Process failed with return code {result.returncode}")
            if result.stderr:
                print(f"      Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("   ❌ Test timed out")
        return False
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False

def test_lhm_sensor_isolated():
    """Test LHMSensor in a separate process to avoid DLL conflicts."""
    print("🔍 Testing LHMSensor in isolation...")
    
    dll_path = os.path.abspath("LibreHardwareMonitorLib.dll")
    
    test_script = f'''
import sys
import os
try:
    import pythonnet
    pythonnet.load("coreclr")
    import clr
    
    # Test System.Management availability
    system_mgmt_available = False
    try:
        clr.AddReference("System.Management")
        system_mgmt_available = True
    except Exception:
        pass
    
    # Load LibreHardwareMonitor DLL
    dll_path = r"{dll_path}"
    if os.path.exists(dll_path):
        clr.AddReference(dll_path)
        from LibreHardwareMonitor.Hardware import Computer
        
        computer = Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.IsMemoryEnabled = True
        computer.IsStorageEnabled = True
        
        if system_mgmt_available:
            computer.IsMotherboardEnabled = True
        else:
            computer.IsMotherboardEnabled = False
        
        computer.Open()
        hardware_list = list(computer.Hardware)
        computer.Close()
        
        print(f"SUCCESS:{{len(hardware_list)}}")
        for hw in hardware_list[:3]:
            print(f"HARDWARE:{{hw.Name}}")
    else:
        print("FAILED:DLL not found")
except Exception as e:
    print(f"FAILED:{{e}}")
'''
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith("SUCCESS:"):
                    count = int(line.split(":")[1])
                    print(f"   ✅ Found {count} hardware components")
                    return True
                elif line.startswith("HARDWARE:"):
                    hw_name = line.split(":", 1)[1]
                    print(f"      • {hw_name}")
                elif line.startswith("FAILED:"):
                    error = line.split(":", 1)[1]
                    print(f"   ❌ Failed: {error}")
                    return False
        else:
            print(f"   ❌ Process failed with return code {result.returncode}")
            if result.stderr:
                print(f"      Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("   ❌ Test timed out")
        return False
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False

def main():
    print("🔍 Isolated Sensor Testing (No DLL Conflicts)")
    print("=" * 50)
    
    hw_available = test_hardware_monitor_isolated()
    lhm_available = test_lhm_sensor_isolated()
    
    print("\n📊 RESULTS")
    print("-" * 20)
    print(f"HardwareMonitor: {'✅ Available' if hw_available else '❌ Not Available'}")
    print(f"LHMSensor:       {'✅ Available' if lhm_available else '❌ Not Available'}")
    
    if hw_available and lhm_available:
        print("\n🎯 RECOMMENDATION: Use HardwareMonitor (primary) to avoid conflicts")
    elif hw_available:
        print("\n🎯 RECOMMENDATION: Use HardwareMonitor")
    elif lhm_available:
        print("\n🎯 RECOMMENDATION: Use LHMSensor")
    else:
        print("\n⚠️  No hardware sensors available - use MockSensor only")

if __name__ == "__main__":
    main() 