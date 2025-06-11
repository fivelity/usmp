#!/usr/bin/env python3
"""
Quick Hardware Access Test
==========================

Test actual hardware sensor access with current permissions.
"""

import ctypes
import os
import platform
import subprocess
import sys
import time


def is_admin():
    """Check if running with admin privileges."""
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def setup_hardware_monitor_lib():
    """
    Sets up the HardwareMonitor library for the current operating system.
    """
    if platform.system() == "Windows":
        # from HardwareMonitor import Hardware, HardwareType, Identifier
        pass  # Library should be handled by pythonnet

    elif platform.system() == "Linux":
        # Linux-specific setup (placeholder)
        print("Linux support is not fully implemented for hardware monitoring.")


def get_hardware_info():
    """
    if platform.system() == "Windows":
        try:
            # Import and initialize LibreHardwareMonitor
            # Note: Ensure the .dll files are in the expected path
            from HardwareMonitor import Hardware, Identifier  # noqa: F401
        except ImportError as e:
            return {
                "error": "Failed to import LibreHardwareMonitor.",
                "details": str(e),
            }

        computer = Hardware.Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
    """
    if platform.system() == "Windows":
        try:
            # Import and initialize LibreHardwareMonitor
            # Note: Ensure the .dll files are in the expected path
            from HardwareMonitor import Hardware, Identifier  # noqa: F401
        except ImportError as e:
            return {
                "error": "Failed to import LibreHardwareMonitor.",
                "details": str(e),
            }

        computer = Hardware.Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.IsMemoryEnabled = True
        computer.IsMotherboardEnabled = True
        computer.IsStorageEnabled = True
        computer.Open()

        info = {
            "cpu": [],
            "gpu": [],
            "memory": [],
            "storage": [],
            "motherboard": [],
        }

        for hardware in computer.Hardware:
            hardware.Update()
            if hardware.HardwareType == Hardware.HardwareType.Cpu:
                info["cpu"].extend(process_hardware(hardware))
            elif (
                hardware.HardwareType == Hardware.HardwareType.GpuNvidia
                or hardware.HardwareType == Hardware.HardwareType.GpuAmd
            ):
                info["gpu"].extend(process_hardware(hardware))
            elif hardware.HardwareType == Hardware.HardwareType.Memory:
                info["memory"].extend(process_hardware(hardware))
            elif hardware.HardwareType == Hardware.HardwareType.Storage:
                info["storage"].extend(process_hardware(hardware))
            elif hardware.HardwareType == Hardware.HardwareType.Motherboard:
                info["motherboard"].extend(process_hardware(hardware))

        computer.Close()
        return info
    elif platform.system() == "Linux":
        return {"error": "Linux hardware monitoring not implemented."}
    else:
        return {"error": "Unsupported operating system."}


def process_hardware(hardware):
    """Processes a hardware component and its sensors."""
    results = []
    hardware.Update()
    for sensor in hardware.Sensors:
        if sensor.Value is not None:
            results.append(
                {
                    "name": sensor.Name,
                    "type": sensor.SensorType.ToString(),
                    "value": f"{sensor.Value:.2f}",
                    "identifier": str(sensor.Identifier),
                }
            )
    for sub_hardware in hardware.SubHardware:
        results.extend(process_hardware(sub_hardware))
    return results


def main():
    """Main function to run the hardware info script."""
    if not is_admin():
        print("Administrator privileges are recommended to run this script.")
        # Attempt to re-run with sudo/admin rights
        try:
            if platform.system() == "Windows":
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, __file__, None, 1
                )
                # Exit after launching new process
                return
            else:
                subprocess.check_call(["sudo", "python"] + sys.argv)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to elevate privileges: {e}")
            # return

    print("Setting up hardware monitoring library...")
    setup_hardware_monitor_lib()

    print("Fetching hardware information...")
    start_time = time.time()
    hardware_info = get_hardware_info()
    end_time = time.time()
    print(f"Finished in {end_time - start_time:.2f} seconds.")

    if "error" in hardware_info:
        print(f"Error: {hardware_info['error']}")
        if "details" in hardware_info:
            print(f"Details: {hardware_info['details']}")
        return

    # Print collected information
    for category, items in hardware_info.items():
        if items:
            print(f"\n----- {category.upper()} -----")
            for item in items:
                print(
                    f"  {item['name']} ({item['type']}): " f"{item.get('value', 'N/A')}"
                )


if __name__ == "__main__":
    main()
