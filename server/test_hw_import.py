#!/usr/bin/env python3
"""
Direct test for the HardwareMonitor package import
"""

import traceback
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_hw_monitor():
    """Test importing HardwareMonitor package directly"""
    try:
        logger.info("1. Testing Python.NET import...")
        import pythonnet
        logger.info("✅ Python.NET imported successfully")
        
        try:
            # Try loading CoreCLR runtime first
            logger.info("2. Loading CoreCLR runtime...")
            pythonnet.load("coreclr")
            logger.info("✅ CoreCLR loaded successfully")
        except Exception as e:
            logger.warning(f"⚠️ CoreCLR loading failed: {e}")
            logger.warning("Attempting with default runtime...")
            
        try:
            logger.info("3. Importing CLR...")
            import clr
            logger.info("✅ CLR imported successfully")
            
            # Try to find and add the dll reference
            logger.info("4. Looking for LibreHardwareMonitorLib.dll...")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dll_path = os.path.join(current_dir, "LibreHardwareMonitorLib.dll")
            
            if os.path.exists(dll_path):
                logger.info(f"✅ Found DLL at: {dll_path}")
                clr.AddReference(dll_path)
                logger.info("✅ DLL reference added")
            else:
                logger.error(f"❌ DLL not found at: {dll_path}")
                return False
            
        except Exception as e:
            logger.error(f"❌ CLR error: {e}")
            logger.error(traceback.format_exc())
            return False
            
        logger.info("5. Now trying to import HardwareMonitor...")
        try:
            import HardwareMonitor
            logger.info("✅ HardwareMonitor imported successfully")
            
            # Test utility functions
            try:
                logger.info("6. Testing HardwareMonitor.Util...")
                from HardwareMonitor.Util import OpenComputer, ToBuiltinTypes
                logger.info("✅ HardwareMonitor.Util imports successful")
            except Exception as e:
                logger.error(f"❌ Error importing HardwareMonitor.Util: {e}")
                logger.error(traceback.format_exc())
            
            return True
        except ImportError as e:
            logger.error(f"❌ Failed to import HardwareMonitor: {e}")
            logger.error(traceback.format_exc())
            return False
        
    except Exception as e:
        logger.error(f"❌ Main error in test: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 HardwareMonitor Import Test")
    print("=" * 60)
    success = test_hw_monitor()
    print("\n" + "=" * 60)
    print(f"Test Result: {'✅ PASSED' if success else '❌ FAILED'}")
    print("=" * 60)
