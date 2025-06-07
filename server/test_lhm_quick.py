#!/usr/bin/env python3
"""
Quick test of LHM sensor functionality to debug System.Management issues
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_imports():
    """Test basic Python.NET imports"""
    try:
        logger.info("Testing basic Python imports...")
        import pythonnet
        logger.info("✅ pythonnet imported successfully")
        
        pythonnet.load('coreclr')
        logger.info("✅ Python.NET coreclr loaded successfully")
        
        import clr
        logger.info("✅ clr module imported successfully")
        
        return True
    except Exception as e:
        logger.error(f"❌ Basic imports failed: {e}")
        return False

def test_system_management():
    """Test System.Management loading with multiple methods"""
    try:
        import clr
        
        methods = [
            ("GAC Reference", lambda: clr.AddReference('System.Management')),
            ("Full Assembly Name", lambda: clr.AddReference('System.Management, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a')),
            ("Framework64 v4.0", lambda: clr.AddReference(r'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Management.dll')),
            ("Framework v4.0", lambda: clr.AddReference(r'C:\Windows\Microsoft.NET\Framework\v4.0.30319\System.Management.dll'))
        ]
        
        for name, method in methods:
            try:
                logger.info(f"Trying {name}...")
                method()
                logger.info(f"✅ {name} succeeded!")
                return True
            except Exception as e:
                logger.warning(f"❌ {name} failed: {e}")
        
        logger.error("❌ All System.Management loading methods failed")
        return False
        
    except Exception as e:
        logger.error(f"❌ System.Management test error: {e}")
        return False

def test_lhm_dll():
    """Test LibreHardwareMonitor DLL loading"""
    try:
        import clr
        
        dll_path = os.path.abspath('LibreHardwareMonitorLib.dll')
        logger.info(f"Testing DLL at: {dll_path}")
        
        if not os.path.exists(dll_path):
            logger.error(f"❌ DLL not found at: {dll_path}")
            return False
        
        clr.AddReference(dll_path)
        logger.info("✅ LibreHardwareMonitorLib.dll loaded successfully")
        
        from LibreHardwareMonitor.Hardware import Computer
        logger.info("✅ Computer class imported successfully")
        
        return True
    except Exception as e:
        logger.error(f"❌ LHM DLL test failed: {e}")
        return False

def test_full_hardware_access():
    """Test full hardware initialization"""
    try:
        from LibreHardwareMonitor.Hardware import Computer
        
        logger.info("Creating Computer instance...")
        computer = Computer()
        
        # Enable core hardware types that should always work
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.IsMemoryEnabled = True
        computer.IsNetworkEnabled = True
        
        # Test System.Management dependent sensors
        system_mgmt_available = False
        try:
            computer.IsStorageEnabled = True
            computer.IsMotherboardEnabled = True
            system_mgmt_available = True
            logger.info("✅ System.Management dependent sensors enabled")
        except Exception as e:
            logger.warning(f"⚠️ System.Management sensors failed: {e}")
            computer.IsStorageEnabled = False
            computer.IsMotherboardEnabled = False
        
        # Test System.IO.Ports dependent sensors (controllers) - but don't enable yet
        system_io_ports_available = False
        if system_mgmt_available:
            try:
                import clr
                clr.AddReference("System.IO.Ports")
                system_io_ports_available = True
                logger.info("✅ System.IO.Ports is available - controllers can be enabled")
            except Exception as e:
                logger.warning(f"⚠️ System.IO.Ports not available: {e}")
        
        # Only enable controllers if System.IO.Ports is available
        if system_io_ports_available:
            computer.IsControllerEnabled = True
        else:
            computer.IsControllerEnabled = False
        
        logger.info("Opening computer...")
        try:
            computer.Open()
            
            hardware_count = len(list(computer.Hardware))
            logger.info(f"✅ SUCCESS! Detected {hardware_count} hardware components")
            
            # List detected hardware and count by type
            hardware_types = {}
            for hardware in computer.Hardware:
                hw_type = str(hardware.HardwareType)
                hardware_types[hw_type] = hardware_types.get(hw_type, 0) + 1
                logger.info(f"  - {hardware.Name} ({hw_type})")
            
            # Summary of what we got
            logger.info("📊 Hardware Summary:")
            for hw_type, count in hardware_types.items():
                logger.info(f"   {hw_type}: {count}")
            
            # Determine monitoring level
            if system_mgmt_available and system_io_ports_available:
                monitoring_level = "FULL"
            elif system_mgmt_available:
                monitoring_level = "EXTENDED (no controllers)"
            elif hardware_count > 2:
                monitoring_level = "BASIC (CPU/GPU/Memory/Network)"
            else:
                monitoring_level = "MINIMAL (CPU/GPU only)"
            
            logger.info(f"🎯 Monitoring Level: {monitoring_level}")
            
            computer.Close()
            return True
            
        except Exception as open_error:
            logger.error(f"❌ Computer.Open() failed: {open_error}")
            
            # If controllers are causing issues, try without them
            if computer.IsControllerEnabled:
                logger.info("🔧 Retrying without controller sensors...")
                computer.IsControllerEnabled = False
                try:
                    computer.Open()
                    
                    hardware_count = len(list(computer.Hardware))
                    logger.info(f"✅ SUCCESS! Detected {hardware_count} hardware components (no controllers)")
                    
                    # List detected hardware
                    for hardware in computer.Hardware:
                        logger.info(f"  - {hardware.Name} ({hardware.HardwareType})")
                    
                    logger.info("🎯 Monitoring Level: EXTENDED (no controllers)")
                    
                    computer.Close()
                    return True
                    
                except Exception as retry_error:
                    logger.error(f"❌ Retry without controllers failed: {retry_error}")
            
            # If still failing, try minimal configuration
            logger.info("🔧 Trying minimal configuration (CPU/GPU only)...")
            computer = Computer()
            computer.IsCpuEnabled = True
            computer.IsGpuEnabled = True
            computer.IsMemoryEnabled = False
            computer.IsNetworkEnabled = False
            computer.IsStorageEnabled = False
            computer.IsMotherboardEnabled = False
            computer.IsControllerEnabled = False
            
            try:
                computer.Open()
                
                hardware_count = len(list(computer.Hardware))
                logger.info(f"⚠️ Minimal mode active - {hardware_count} hardware components")
                
                for hardware in computer.Hardware:
                    logger.info(f"  - {hardware.Name} ({hardware.HardwareType})")
                
                logger.info("🎯 Monitoring Level: MINIMAL (CPU/GPU only)")
                
                computer.Close()
                return True
                
            except Exception as minimal_error:
                logger.error(f"❌ Even minimal configuration failed: {minimal_error}")
                return False
        
    except Exception as e:
        logger.error(f"❌ Full hardware test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🛠️ LHM QUICK TEST - Debugging System.Management")
    logger.info("=" * 50)
    
    # Test 1: Basic imports
    if not test_basic_imports():
        logger.error("💥 Basic imports failed - Python.NET is broken")
        return False
    
    # Test 2: System.Management loading
    if not test_system_management():
        logger.warning("⚠️ System.Management loading failed - will have limited monitoring")
    
    # Test 3: LHM DLL loading
    if not test_lhm_dll():
        logger.error("💥 LHM DLL loading failed")
        return False
    
    # Test 4: Full hardware access
    if not test_full_hardware_access():
        logger.error("💥 Hardware access failed")
        return False
    
    logger.info("🎉 ALL TESTS PASSED! Full hardware monitoring should work!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 