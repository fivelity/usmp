#!/usr/bin/env python3
"""
Test script to verify Python.NET and LibreHardwareMonitor integration
"""

import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_pythonnet_basic():
    """Test basic Python.NET functionality"""
    try:
        logger.info("Testing basic Python.NET import...")
        import pythonnet

        logger.info(f"✓ Python.NET version: {pythonnet.__version__}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to import pythonnet: {e}")
        return False


def test_clr_import():
    """Test CLR import with different approaches"""
    approaches = [
        ("Direct import", lambda: __import__("clr")),
        ("With netfx runtime", lambda: test_netfx_runtime()),
        ("With coreclr runtime", lambda: test_coreclr_runtime()),
    ]

    for name, test_func in approaches:
        try:
            logger.info(f"Testing {name}...")
            test_func()
            logger.info(f"✓ {name} successful")
            return True
        except Exception as e:
            logger.warning(f"⚠ {name} failed: {e}")

    return False


def test_netfx_runtime():
    """Test with .NET Framework runtime"""
    import pythonnet

    pythonnet.load("netfx")
    import clr

    return clr


def test_coreclr_runtime():
    """Test with CoreCLR runtime"""
    import pythonnet

    pythonnet.load("coreclr")
    import clr

    return clr


def test_dll_loading():
    """Test LibreHardwareMonitor DLL loading"""
    try:
        # First ensure we have a working CLR
        if not test_clr_import():
            logger.error("✗ Cannot test DLL loading without working CLR")
            return False

        import clr

        # Find the DLL
        dll_path = os.path.abspath("LibreHardwareMonitorLib.dll")
        logger.info(f"Looking for DLL at: {dll_path}")

        if not os.path.exists(dll_path):
            logger.error(f"✗ DLL not found at: {dll_path}")
            return False

        logger.info(f"✓ DLL found at: {dll_path}")

        # Try to add reference
        logger.info("Adding DLL reference...")
        clr.AddReference(dll_path)
        logger.info("✓ DLL reference added successfully")

        # Try to import LibreHardwareMonitor classes
        logger.info("Importing LibreHardwareMonitor classes...")
        from LibreHardwareMonitor.Hardware import Computer

        logger.info("✓ LibreHardwareMonitor classes imported successfully")

        # Try to create Computer instance
        logger.info("Creating Computer instance...")
        computer = Computer()
        logger.info("✓ Computer instance created successfully")

        # Try basic configuration
        logger.info("Configuring Computer instance...")
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.IsMemoryEnabled = True
        logger.info("✓ Computer instance configured successfully")

        # Try to open
        logger.info("Opening hardware monitoring...")
        computer.Open()
        logger.info("✓ Hardware monitoring opened successfully")

        # Check if we can see any hardware
        hardware_count = len(list(computer.Hardware))
        logger.info(f"✓ Found {hardware_count} hardware components")

        # Clean up
        computer.Close()
        logger.info("✓ Hardware monitoring closed successfully")

        return True

    except Exception as e:
        logger.error(f"✗ DLL loading failed: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return False


def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Python.NET and LibreHardwareMonitor Test Suite")
    logger.info("=" * 60)

    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info(f"Current directory: {os.getcwd()}")

    tests = [
        ("Python.NET Basic Import", test_pythonnet_basic),
        ("CLR Import", test_clr_import),
        ("LibreHardwareMonitor DLL Loading", test_dll_loading),
    ]

    results = []
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        success = test_func()
        results.append((test_name, success))
        logger.info(f"Result: {'PASS' if success else 'FAIL'}")

    logger.info("\n" + "=" * 60)
    logger.info("Test Results Summary:")
    logger.info("=" * 60)

    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        logger.info(f"{test_name}: {status}")

    all_passed = all(success for _, success in results)
    logger.info(
        f"\nOverall Result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}"
    )

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
