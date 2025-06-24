#!/usr/bin/env python3
"""
Specialized Python.NET and clr_loader fix script for sensor monitoring
"""

import os
import sys
import subprocess
import platform
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, description=None):
    """Run a command and log the output"""
    if description:
        logger.info(f"⚙️ {description}")
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Command failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False, e.stderr
    except Exception as e:
        logger.error(f"❌ Error executing command: {e}")
        return False, str(e)

def fix_pythonnet():
    """Comprehensive fix for Python.NET and clr_loader issues"""
    logger.info("🔧 Starting Python.NET and clr_loader fix...")
    logger.info("-" * 60)
    
    # 1. First, check if we're running as administrator (recommended)
    is_admin = False
    if platform.system() == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            pass
        
    logger.info(f"👤 Admin privileges: {'✅ YES' if is_admin else '⚠️ NO'}")
    if not is_admin:
        logger.warning("⚠️ WARNING: Running without admin privileges.")
        logger.warning("   Some hardware sensors may not be accessible.")
        logger.warning("   Consider running this script as Administrator.")
    
    # 2. Uninstall existing pythonnet and clr_loader packages
    logger.info("🗑️ Removing existing Python.NET and clr_loader packages...")
    run_command([sys.executable, "-m", "pip", "uninstall", "-y", "pythonnet", "clr-loader"], "Uninstalling packages")
    
    # 3. Clear pip cache
    logger.info("🧹 Cleaning pip cache...")
    run_command([sys.executable, "-m", "pip", "cache", "purge"], "Purging pip cache")
    
    # 4. Install specific, compatible versions
    versions_to_try = [
        # Version tuple: (pythonnet_version, clr_loader_version)
        ("3.0.3", "0.2.7.post0"),  # Most stable combination
        ("3.0.2", "0.2.6"),        # Alternative stable combination
        ("3.0.1", "0.2.6"),        # Older but reliable combination
    ]
    
    for python_net_ver, clr_loader_ver in versions_to_try:
        logger.info(f"📦 Installing pythonnet {python_net_ver} with clr_loader {clr_loader_ver}...")
        
        # First install clr_loader with specific version
        success, _ = run_command(
            [sys.executable, "-m", "pip", "install", f"clr_loader=={clr_loader_ver}", "--no-cache-dir", "--force-reinstall"],
            f"Installing clr_loader {clr_loader_ver}"
        )
        
        if not success:
            logger.warning(f"⚠️ Failed to install clr_loader {clr_loader_ver}, trying next version combo...")
            continue
            
        # Then install pythonnet with specific version
        success, _ = run_command(
            [sys.executable, "-m", "pip", "install", f"pythonnet=={python_net_ver}", "--no-cache-dir", "--force-reinstall"],
            f"Installing pythonnet {python_net_ver}"
        )
        
        if not success:
            logger.warning(f"⚠️ Failed to install pythonnet {python_net_ver}, trying next version combo...")
            continue
            
        # Test if installation works
        logger.info("🧪 Testing Python.NET functionality...")
        try:
            # Test basic import
            logger.info("   - Testing basic import...")
            import pythonnet
            
            # Test loading CoreCLR
            logger.info("   - Testing CoreCLR runtime...")
            pythonnet.load("coreclr")
            
            # Test CLR import
            logger.info("   - Testing CLR import...")
            import clr
            
            logger.info("✅ SUCCESS! Python.NET installed and working correctly!")
            return True
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            logger.info("   Trying next version combination...")
    
    # If we got here, all combinations failed
    logger.error("❌ All Python.NET installation attempts failed")
    logger.error("   Please run the script with administrator privileges or")
    logger.error("   check your system configuration.")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("🛠️  Python.NET and clr_loader Fix Tool")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("-" * 60)
    
    success = fix_pythonnet()
    
    if success:
        print("\n✅ SUCCESS: Python.NET environment fixed successfully!")
        print("   You should now be able to use the HardwareMonitor package.")
    else:
        print("\n❌ FAILED: Could not fix Python.NET environment.")
        print("   Try running this script with Administrator privileges.")
        
    print("=" * 60)
