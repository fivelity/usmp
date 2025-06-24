#!/usr/bin/env python3
"""Quick HardwareMonitor test"""

print("Testing HardwareMonitor import...")
try:
    from HardwareMonitor.Util import OpenComputer, ToBuiltinTypes

    print("✅ Import successful")

    computer = OpenComputer(cpu=True, gpu=True)
    if computer:
        print("✅ Computer created")
        computer.Update()
        data = ToBuiltinTypes(computer.Hardware)
        print(f"✅ Found {len(data)} hardware components")
        computer.Close()
        print("✅ Test completed successfully")
    else:
        print("❌ Computer creation failed")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
