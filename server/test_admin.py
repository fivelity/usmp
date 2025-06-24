"""Test admin privileges and LHM initialization."""
import os
import ctypes
import sys
import logging
import subprocess
from pathlib import Path


def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def install_system_management():
    """Install System.Management assembly using Windows PowerShell."""
    try:
        # Use Add-Type to load System.Management
        cmd = [
            "powershell",
            "-Command",
            '[System.Reflection.Assembly]::LoadWithPartialName("System.Management")',
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing System.Management: {e}")
        return False


def test_hardware_monitor():
    """Test HardwareMonitor package initialization"""
    try:
        import pythonnet

        pythonnet.load("coreclr")

        from HardwareMonitor.Hardware import Computer
        from HardwareMonitor.Util import OpenComputer

        print("✅ HardwareMonitor package available")
        computer = OpenComputer(
            motherboard=True,
            cpu=True,
            gpu=True,
            memory=True,
            storage=True,
            network=True,
            controller=True,
        )

        print("\nDetected Hardware:")
        for hardware in computer.Hardware:
            print(f"- {hardware.Name}")

        computer.Close()
        return True
    except ImportError:
        print("⚠️ HardwareMonitor package not available")
        return False
    except Exception as e:
        print(f"❌ Error testing HardwareMonitor: {e}")
        return False


def test_dll_approach():
    """Test direct DLL initialization"""
    try:
        import clr

        server_dir = Path(__file__).parent
        dll_path = server_dir / "LibreHardwareMonitorLib.dll"

        if not dll_path.exists():
            print(f"❌ DLL not found at: {dll_path}")
            return False

        print(f"✅ Found DLL at: {dll_path}")

        os.environ["PATH"] = f"{str(server_dir)};{os.environ['PATH']}"
        clr.AddReference(str(dll_path))

        from LibreHardwareMonitor.Hardware import Computer

        print("✅ LibreHardwareMonitor assembly loaded")

        computer = Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.IsMemoryEnabled = True
        computer.IsMotherboardEnabled = True
        computer.Open()

        print("\nDetected Hardware:")
        for hardware in computer.Hardware:
            print(f"- {hardware.Name}")

        computer.Close()
        return True
    except Exception as e:
        print(f"❌ Error testing DLL approach: {e}")
        return False


def main():
    print("=== LibreHardwareMonitor Setup Test ===")

    # Check admin privileges
    if not is_admin():
        print("❌ Not running with administrator privileges")
        print("Please run this script as administrator")
        if sys.version_info >= (3, 9):
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        return

    print("✅ Running with administrator privileges")

    # Install System.Management if needed
    print("\nChecking System.Management assembly...")
    if install_system_management():
        print("✅ System.Management assembly is available")
    else:
        print("❌ Failed to load System.Management assembly")
        return

    # Test initialization approaches
    print("\nTesting HardwareMonitor package...")
    if test_hardware_monitor():
        print("\n✅ HardwareMonitor package test passed!")
    else:
        print("\n⚠️ Trying DLL approach...")
        if test_dll_approach():
            print("\n✅ DLL approach test passed!")
        else:
            print("\n❌ Both approaches failed")


if __name__ == "__main__":
    main()
