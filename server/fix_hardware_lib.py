#!/usr/bin/env python3
"""
LibreHardwareMonitorLib.dll fix script for HardwareMonitor package
"""

import os
import sys
import subprocess
import platform
import logging
import shutil
import urllib.request
from pathlib import Path
import ctypes

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Constants
DLL_VERSION = "0.9.3"
DLL_NAME = "LibreHardwareMonitorLib.dll"
DLL_URL = "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v0.9.3/LibreHardwareMonitor-net472.zip"

def is_admin():
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

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

def download_dll():
    """Download the correct version of LibreHardwareMonitorLib.dll"""
    import zipfile
    import tempfile
    
    logger.info(f"📥 Downloading LibreHardwareMonitorLib v{DLL_VERSION}...")
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "lhm.zip")
        
        # Download the zip file
        try:
            logger.info(f"   Downloading from {DLL_URL}")
            urllib.request.urlretrieve(DLL_URL, zip_path)
        except Exception as e:
            logger.error(f"❌ Failed to download DLL: {e}")
            return False
        
        # Extract the zip file
        try:
            logger.info("   Extracting zip file...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the DLL file
            dll_path = None
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file == DLL_NAME:
                        dll_path = os.path.join(root, file)
                        break
                if dll_path:
                    break
            
            if not dll_path:
                logger.error(f"❌ Could not find {DLL_NAME} in the downloaded package")
                return False
            
            # Copy the DLL to the script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            target_path = os.path.join(script_dir, DLL_NAME)
            
            logger.info(f"   Copying DLL to {target_path}")
            shutil.copy(dll_path, target_path)
            
            logger.info("✅ DLL downloaded and installed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to extract or copy DLL: {e}")
            return False

def register_dll():
    """Register the DLL using regasm (requires admin privileges on Windows)"""
    if not platform.system() == "Windows":
        logger.warning("⚠️ DLL registration is only supported on Windows")
        return False
    
    if not is_admin():
        logger.warning("⚠️ Admin privileges required for DLL registration")
        logger.warning("   Please run this script as Administrator")
        return False
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(script_dir, DLL_NAME)
    
    if not os.path.exists(dll_path):
        logger.error(f"❌ DLL file not found at {dll_path}")
        return False
    
    # Look for .NET Framework regasm tools
    regasm_paths = [
        r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regasm.exe",
        r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe",
    ]
    
    regasm_path = None
    for path in regasm_paths:
        if os.path.exists(path):
            regasm_path = path
            break
    
    if not regasm_path:
        logger.error("❌ Could not find regasm.exe")
        return False
    
    logger.info(f"📝 Registering DLL using {regasm_path}...")
    success, output = run_command([regasm_path, "/codebase", dll_path], "Running regasm")
    
    if success:
        logger.info("✅ DLL registered successfully")
        return True
    else:
        logger.error("❌ Failed to register DLL")
        return False

def verify_hw_monitor():
    """Verify that HardwareMonitor can import the DLL correctly"""
    logger.info("🔍 Verifying HardwareMonitor package...")
    
    try:
        logger.info("1. Testing Python.NET import...")
        import pythonnet
        
        try:
            # Try loading CoreCLR runtime
            logger.info("2. Loading runtime...")
            pythonnet.load("coreclr")
        except:
            # If that fails, try the default approach
            logger.info("   CoreCLR loading failed, using default runtime")
            pass
        
        logger.info("3. Importing CLR...")
        import clr
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dll_path = os.path.join(script_dir, DLL_NAME)
        
        logger.info(f"4. Adding reference to {dll_path}...")
        clr.AddReference(dll_path)
        
        logger.info("5. Importing LibreHardwareMonitor...")
        from LibreHardwareMonitor.Hardware import Computer
        
        logger.info("6. Creating Computer instance...")
        computer = Computer()
        
        logger.info("✅ Verification successful!")
        return True
    
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def fix_hardware_lib():
    """Main function to fix LibreHardwareMonitorLib issues"""
    logger.info("🔧 Starting LibreHardwareMonitorLib fix...")
    logger.info("-" * 60)
    
    # 1. Check admin privileges
    admin_status = "✅ YES" if is_admin() else "⚠️ NO"
    logger.info(f"👤 Admin privileges: {admin_status}")
    
    if not is_admin():
        logger.warning("⚠️ WARNING: Running without admin privileges.")
        logger.warning("   Some operations may fail.")
        logger.warning("   Consider running this script as Administrator.")
    
    # 2. Download the correct DLL version
    dll_success = download_dll()
    if not dll_success:
        logger.error("❌ Failed to obtain the correct DLL")
        return False
    
    # 3. Install pythonnet if needed
    logger.info("📦 Ensuring Python.NET is installed correctly...")
    run_command([sys.executable, "-m", "pip", "install", "pythonnet==3.0.3", "--force-reinstall"], "Installing pythonnet")
    
    # 4. Register DLL if running as admin
    if is_admin():
        register_dll()
    
    # 5. Verify the fix
    verification = verify_hw_monitor()
    
    if verification:
        logger.info("✅ LibreHardwareMonitorLib successfully fixed!")
        if not is_admin():
            logger.info("ℹ️ Note: For full functionality, run your application as Administrator")
        return True
    else:
        logger.error("❌ LibreHardwareMonitorLib fix incomplete")
        logger.info("ℹ️ Try running this script as Administrator")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🛠️  LibreHardwareMonitorLib Fix Tool")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("-" * 60)
    
    if platform.system() != "Windows":
        print("⛔ This script is intended for Windows only")
        print("   LibreHardwareMonitor is a Windows-only library")
        sys.exit(1)
    
    success = fix_hardware_lib()
    
    if success:
        print("\n✅ SUCCESS: LibreHardwareMonitorLib fixed successfully!")
        print("   HardwareMonitor should now work properly.")
        print("   For full functionality, run your application as Administrator.")
    else:
        print("\n⚠️ PARTIAL FIX: Some issues could not be resolved.")
        print("   To resolve remaining issues:")
        print("   1. Run this script as Administrator")
        print("   2. Ensure .NET Framework 4.7.2+ is installed")
        print("   3. Run your application as Administrator")
        
    print("=" * 60)
