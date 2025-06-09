# Hardware Monitoring Fixes Documentation

This document provides comprehensive information about fixing both LHMSensor System.Management dependency issues and HardwareMonitor package installation/permissions problems.

## 🔍 Overview

The hardware monitoring system uses a cascading fallback approach:
1. **PyHardwareMonitor Package** (Primary) - Recommended Python wrapper for LibreHardwareMonitor
2. **HardwareMonitor Package** (Alternative) - Alternative Python package with direct hardware access
3. **LibreHardwareMonitor** (Fallback) - .NET library integration via Python.NET
4. **Mock Sensor** (Final Fallback) - Simulated data for testing

**📚 Based on PyHardwareMonitor Documentation:**
- **Admin privileges are mandatory** for proper hardware sensor access
- Includes `SensorValueToString` function for proper sensor value formatting
- Built on top of LibreHardwareMonitorLib with better Python integration

## ⚡ Quick Fix

**For immediate resolution, run:**

```bash
# Option 1: Automated fix with admin privileges (Recommended)
fix_hardware_monitoring.bat

# Option 2: Manual Python execution
python fix_hardware_monitoring.py
```

## 🧰 Individual Fix Tools

### 1. System Diagnostics
Comprehensive analysis of your system:

```bash
python system_diagnostics.py
```

**What it checks:**
- System information and Python environment
- Administrator privileges
- Python package dependencies
- .NET Framework installation
- HardwareMonitor package functionality
- LibreHardwareMonitor dependencies
- System.Management assembly availability

### 2. Dependency Installer
Automated installation of missing dependencies:

```bash
python dependency_installer.py
```

**What it fixes:**
- Installs/updates Python packages (pythonnet, psutil, etc.)
- Downloads LibreHardwareMonitorLib.dll
- Attempts HardwareMonitor package installation
- Tests various Python.NET configurations

### 3. .NET Framework Installer
Windows-specific .NET Framework fixes:

```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File install_dotnet_framework.ps1
```

**What it does:**
- Checks .NET Framework 4.8 installation
- Downloads .NET Framework installer
- Verifies System.Management assembly
- Tests Python.NET integration

## 🚨 Common Issues and Solutions

### Issue 1: System.Management Assembly Not Found

**Symptoms:**
- LHMSensor fails to initialize
- Error mentions "System.Management"
- .NET assembly loading failures

**Solutions:**
1. **Install .NET Framework 4.8:**
   ```bash
   # Run the PowerShell installer
   powershell install_dotnet_framework.ps1
   
   # Or download manually from Microsoft:
   # https://dotnet.microsoft.com/download/dotnet-framework/net48
   ```

2. **Install Developer Pack:**
   ```bash
   # Provides additional .NET libraries
   # Downloads automatically via PowerShell script
   ```

3. **Verify Installation:**
   ```bash
   python -c "import clr; clr.AddReference('System.Management'); print('SUCCESS')"
   ```

### Issue 2: HardwareMonitor Package Not Available

**Symptoms:**
- HWSensor fails to import
- "HardwareMonitor package not available" errors
- ImportError on HardwareMonitor module

**Solutions:**
1. **Install PyHardwareMonitor (Recommended):**
   ```bash
   # PyHardwareMonitor is the recommended package based on latest documentation
   pip install PyHardwareMonitor
   
   # Alternative methods if the above fails:
   pip install PyHardwareMonitor --force-reinstall
   pip install PyHardwareMonitor --no-cache-dir
   pip install PyHardwareMonitor --user
   ```

2. **Install Original HardwareMonitor (Alternative):**
   ```bash
   pip install HardwareMonitor
   
   # Alternative methods if the above fails:
   pip install HardwareMonitor --force-reinstall
   pip install HardwareMonitor --no-cache-dir
   pip install HardwareMonitor --user
   ```

3. **Fix Python.NET:**
   ```bash
   pip install --upgrade pythonnet
   
   # Try specific versions if needed:
   pip install pythonnet==3.0.3 --force-reinstall
   ```

4. **⚠️ CRITICAL - Admin Privileges Required:**
   - **PyHardwareMonitor documentation explicitly states: "Python must have admin privileges for HardwareMonitor to be able to access all available sensors properly!"**
   - Right-click Command Prompt/PowerShell
   - Select "Run as Administrator"
   - Re-run installation and execution commands

### Issue 3: Admin Privileges Required

**Symptoms:**
- Hardware access denied
- Limited sensor detection
- Permission errors

**Solutions:**
1. **Run as Administrator:**
   - Right-click your terminal/IDE
   - Select "Run as Administrator"
   - Re-run your Python scripts

2. **Use the Batch File:**
   ```bash
   # Automatically requests admin privileges
   fix_hardware_monitoring.bat
   ```

### Issue 4: Python Architecture Mismatch

**Symptoms:**
- DLL loading errors
- Architecture-specific import failures
- "32-bit vs 64-bit" errors

**Solutions:**
1. **Check Python Architecture:**
   ```bash
   python -c "import platform; print(platform.architecture())"
   ```

2. **Install Matching Packages:**
   - Ensure all packages match your Python architecture
   - Consider using a 64-bit Python installation

## 📁 File Structure

```
server/
├── fix_hardware_monitoring.py      # 🔧 Main orchestration script
├── fix_hardware_monitoring.bat     # 🪟 Windows batch with admin privileges
├── system_diagnostics.py           # 🔍 Comprehensive system analysis
├── dependency_installer.py         # 📦 Automated dependency fixes
├── install_dotnet_framework.ps1    # 🔧 .NET Framework installer
├── app/sensors/
│   ├── hw_sensor.py                # 🖥️  HardwareMonitor package integration
│   ├── lhm_sensor.py               # 🔩 LibreHardwareMonitor integration
│   └── mock_sensor.py              # 🎭 Fallback mock sensor
└── LibreHardwareMonitorLib.dll     # 📚 Required DLL (auto-downloaded)
```

## 🔄 Execution Flow

The fix system follows this process:

1. **Diagnostics** → Identify specific issues
2. **Dependencies** → Install missing packages
3. **.NET Framework** → Fix System.Management issues
4. **Testing** → Verify sensor functionality
5. **Recommendations** → Provide next steps

## 🎯 Verification Commands

After running fixes, verify functionality:

```bash
# Test individual components
python -c "import HardwareMonitor; print('PyHardwareMonitor/HardwareMonitor: OK')"
python -c "from HardwareMonitor.Util import SensorValueToString; print('PyHardwareMonitor SensorValueToString: OK')" 
python -c "import pythonnet; pythonnet.load('coreclr'); import clr; print('Python.NET: OK')"
python -c "import clr; clr.AddReference('System.Management'); print('System.Management: OK')"

# Test sensor implementations
python -c "
import asyncio
from app.sensors import HWSensor, LHMSensor, MockSensor
from app.core.config import AppSettings

async def test():
    settings = AppSettings()
    for name, cls in [('HW', HWSensor), ('LHM', LHMSensor), ('Mock', MockSensor)]:
        sensor = cls()
        await sensor.initialize(settings)
        available = await sensor.is_available()
        print(f'{name}: {\"✅\" if available else \"❌\"}')
        await sensor.close()

asyncio.run(test())
"
```

## 🆘 Troubleshooting

### Still Having Issues?

1. **Check Antivirus Software:**
   - Temporarily disable real-time protection
   - Add Python/project directory to exclusions

2. **Try Different Python Version:**
   - Consider Python 3.9-3.11 for best compatibility
   - Avoid very new or very old Python versions

3. **Clean Installation:**
   ```bash
   # Uninstall problematic packages
   pip uninstall pythonnet HardwareMonitor
   
   # Clear pip cache
   pip cache purge
   
   # Reinstall
   python dependency_installer.py
   ```

4. **Manual Downloads:**
   - Download .NET Framework 4.8 from Microsoft
   - Download LibreHardwareMonitorLib.dll manually
   - Place files in correct directories

### Get Help

- **Run diagnostics:** `python system_diagnostics.py`
- **Check logs:** Look for detailed error messages in console output
- **Verify environment:** Ensure 64-bit Python on 64-bit Windows

## ✅ Success Indicators

You'll know everything is working when:

- ✅ At least one sensor implementation shows as "Working"
- ✅ System diagnostics show minimal critical/high issues
- ✅ Hardware sensor data appears in your application
- ✅ No import errors in the logs

## 🚀 Next Steps

After successful fixes:

1. **Start the backend server:**
   ```bash
   python start_backend.py
   ```

2. **Monitor the logs** for sensor data collection

3. **Check the web interface** for real-time hardware monitoring

4. **Set up monitoring** for any ongoing issues

---

*This documentation covers comprehensive fixes for hardware monitoring dependencies. For additional support, refer to the diagnostic outputs and error messages for specific guidance.* 