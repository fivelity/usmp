# Troubleshooting Guide

## Common Issues and Solutions

### Installation and Setup

#### LibreHardwareMonitor Integration Issues

**Problem**: "LibreHardwareMonitorLib.dll not found"
\`\`\`
Error: Could not load file or assembly 'LibreHardwareMonitorLib.dll'
\`\`\`

**Solutions**:
1. **Check DLL Location**:
   \`\`\`bash
   # Verify the DLL is in the correct location
   ls -la LibreHardwareMonitorLib.dll
   \`\`\`

2. **Run as Administrator**:
   \`\`\`bash
   # Windows: Right-click and "Run as Administrator"
   # Or use the admin batch files
   server/start_server_admin.bat
   \`\`\`

3. **Install .NET Framework**:
   - Download and install .NET Framework 4.7.2 or higher
   - Restart the system after installation

4. **Check Python Architecture**:
   \`\`\`python
   import platform
   print(platform.architecture())  # Should match DLL architecture (x64)
   \`\`\`

**Problem**: "Access Denied" when accessing hardware sensors

**Solutions**:
1. **Administrator Privileges**: Always run the server with administrator privileges
2. **Antivirus Exclusion**: Add the application folder to antivirus exclusions
3. **Windows Defender**: Disable real-time protection temporarily for testing

#### Python Environment Issues

**Problem**: Module import errors
\`\`\`
ModuleNotFoundError: No module named 'fastapi'
\`\`\`

**Solutions**:
1. **Verify Virtual Environment**:
   \`\`\`bash
   # Activate virtual environment
   conda activate sensor_monitor
   # or
   source venv/bin/activate
   
   # Verify packages
   pip list
   \`\`\`

2. **Reinstall Dependencies**:
   \`\`\`bash
   pip install -r server/requirements.txt
   \`\`\`

3. **Python Version Compatibility**:
   \`\`\`bash
   python --version  # Should be 3.8 or higher
   \`\`\`

#### Frontend Build Issues

**Problem**: Node.js build failures
\`\`\`
Error: Cannot resolve module '@/components/ui'
\`\`\`

**Solutions**:
1. **Clear Node Modules**:
   \`\`\`bash
   cd client
   rm -rf node_modules package-lock.json
   npm install
   \`\`\`

2. **Check Node Version**:
   \`\`\`bash
   node --version  # Should be 16 or higher
   npm --version
   \`\`\`

3. **TypeScript Errors**:
   \`\`\`bash
   # Check TypeScript configuration
   npx tsc --noEmit
   \`\`\`

### Runtime Issues

#### Sensor Data Problems

**Problem**: No sensor data appearing in the dashboard

**Diagnostic Steps**:
1. **Check Backend Logs**:
   \`\`\`bash
   # Look for sensor initialization messages
   tail -f server/logs/sensor_monitor.log
   \`\`\`

2. **Test Sensor Connection**:
   \`\`\`python
   # Run the test script
   python server/test_lhm_dll.py
   \`\`\`

3. **Verify Hardware Monitoring Service**:
   - Ensure LibreHardwareMonitor is not running separately
   - Check Windows Task Manager for conflicting processes

**Problem**: Sensor values are incorrect or outdated

**Solutions**:
1. **Refresh Sensor List**:
   \`\`\`javascript
   // In browser console
   fetch('/api/sensors/refresh', { method: 'POST' })
   \`\`\`

2. **Check Update Intervals**:
   \`\`\`python
   # In server configuration
   SENSOR_UPDATE_INTERVAL = 1.0  # seconds
   \`\`\`

3. **Verify Sensor IDs**:
   \`\`\`bash
   # Check available sensors
   curl http://localhost:8000/api/sensors
   \`\`\`

#### WebSocket Connection Issues

**Problem**: Real-time updates not working
\`\`\`
WebSocket connection failed: Error during WebSocket handshake
\`\`\`

**Solutions**:
1. **Check WebSocket URL**:
   \`\`\`javascript
   // Verify correct WebSocket endpoint
   const ws = new WebSocket('ws://localhost:8000/ws');
   \`\`\`

2. **Firewall Configuration**:
   - Allow port 8000 through Windows Firewall
   - Check corporate firewall settings

3. **Browser Developer Tools**:
   - Check Network tab for WebSocket connections
   - Look for error messages in Console

#### Widget Display Issues

**Problem**: Widgets not rendering correctly

**Diagnostic Steps**:
1. **Check Browser Console**:
   \`\`\`javascript
   // Look for JavaScript errors
   console.error
   \`\`\`

2. **Verify Widget Configuration**:
   \`\`\`javascript
   // Check widget settings in browser storage
   localStorage.getItem('dashboard_widgets')
   \`\`\`

3. **Test with Default Widgets**:
   - Create a new dashboard with default widgets
   - Check if the issue persists

**Problem**: Custom widgets not appearing in widget list

**Solutions**:
1. **Check Widget Registration**:
   \`\`\`typescript
   // Verify widget is in the registry
   import { widgetTypes } from '$lib/components/widgets'
   console.log(widgetTypes)
   \`\`\`

2. **Component Import Errors**:
   \`\`\`bash
   # Check for TypeScript compilation errors
   npm run check
   \`\`\`

### Performance Issues

#### Slow Dashboard Loading

**Diagnostic Steps**:
1. **Check Network Performance**:
   \`\`\`bash
   # Test API response times
   curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/sensors
   \`\`\`

2. **Monitor Memory Usage**:
   \`\`\`bash
   # Check Python process memory
   ps aux | grep python
   \`\`\`

3. **Browser Performance**:
   - Use Chrome DevTools Performance tab
   - Check for memory leaks in JavaScript

**Solutions**:
1. **Optimize Sensor Updates**:
   \`\`\`python
   # Reduce update frequency for non-critical sensors
   SENSOR_UPDATE_INTERVAL = 2.0
   \`\`\`

2. **Limit Historical Data**:
   \`\`\`javascript
   // Reduce graph time ranges
   time_range: 60  // seconds instead of 300
   \`\`\`

3. **Widget Optimization**:
   - Remove unused widgets
   - Use simpler widget types for non-critical data

#### High CPU Usage

**Problem**: Server consuming excessive CPU resources

**Solutions**:
1. **Optimize Sensor Polling**:
   \`\`\`python
   # Increase polling intervals
   HARDWARE_POLL_INTERVAL = 2.0  # seconds
   \`\`\`

2. **Reduce WebSocket Updates**:
   \`\`\`python
   # Batch sensor updates
   WEBSOCKET_BATCH_SIZE = 10
   \`\`\`

3. **Profile Python Code**:
   \`\`\`python
   # Use cProfile to identify bottlenecks
   python -m cProfile -o profile.stats server/app/main.py
   \`\`\`

### Configuration Issues

#### Theme and Styling Problems

**Problem**: Themes not applying correctly

**Solutions**:
1. **Clear Browser Cache**:
   \`\`\`bash
   # Hard refresh in browser
   Ctrl + Shift + R (Windows/Linux)
   Cmd + Shift + R (Mac)
   \`\`\`

2. **Check CSS Loading**:
   \`\`\`javascript
   // Verify CSS files are loaded
   document.styleSheets
   \`\`\`

3. **Theme Configuration**:
   \`\`\`javascript
   // Reset theme to default
   localStorage.removeItem('selected_theme')
   \`\`\`

#### Dashboard Layout Issues

**Problem**: Widgets overlapping or misaligned

**Solutions**:
1. **Reset Grid Settings**:
   \`\`\`javascript
   // Clear grid configuration
   localStorage.removeItem('grid_settings')
   \`\`\`

2. **Check Widget Positions**:
   \`\`\`javascript
   // Verify widget coordinates
   const widgets = JSON.parse(localStorage.getItem('dashboard_widgets'))
   console.log(widgets.map(w => ({ id: w.id, x: w.pos_x, y: w.pos_y })))
   \`\`\`

3. **Grid Snap Issues**:
   - Disable grid snapping temporarily
   - Manually adjust widget positions
   - Re-enable grid snapping

### Development Issues

#### Custom Widget Development

**Problem**: Custom widget not displaying

**Diagnostic Steps**:
1. **Check Component Registration**:
   \`\`\`typescript
   // Verify widget is properly exported
   export { default as CustomWidget } from './CustomWidget.svelte'
   \`\`\`

2. **TypeScript Errors**:
   \`\`\`bash
   # Check for type errors
   npm run check
   \`\`\`

3. **Component Props**:
   \`\`\`svelte
   &lt;!-- Verify required props are defined -->
   <script lang="ts">
     let { widget, isSelected = false } = $props();
   </script>
   \`\`\`

**Problem**: Widget inspector not working

**Solutions**:
1. **Inspector Registration**:
   \`\`\`typescript
   // Ensure inspector is registered with widget
   widgetTypes.custom_widget.inspector = CustomWidgetInspector
   \`\`\`

2. **Props Validation**:
   \`\`\`typescript
   // Check updateWidget function is called correctly
   function updateConfig(updates: Partial<CustomConfig>) {
     updateWidget({ gauge_settings: { ...config, ...updates } });
   }
   \`\`\`

### Deployment Issues

#### Production Build Problems

**Problem**: Build fails in production

**Solutions**:
1. **Environment Variables**:
   \`\`\`bash
   # Set production environment
   export NODE_ENV=production
   export API_URL=https://your-domain.com/api
   \`\`\`

2. **Static File Serving**:
   \`\`\`python
   # Ensure static files are served correctly
   app.mount("/static", StaticFiles(directory="static"), name="static")
   \`\`\`

3. **CORS Configuration**:
   \`\`\`python
   # Update CORS settings for production
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-domain.com"],
       allow_credentials=True,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   \`\`\`

## Diagnostic Tools

### Log Analysis

**Server Logs**:
\`\`\`bash
# View real-time logs
tail -f server/logs/sensor_monitor.log

# Search for specific errors
grep -i "error" server/logs/sensor_monitor.log

# Check sensor initialization
grep -i "sensor" server/logs/sensor_monitor.log
\`\`\`

**Browser Console**:
\`\`\`javascript
// Enable verbose logging
localStorage.setItem('debug_mode', 'true')

// Check WebSocket status
console.log(websocket.readyState)

// Monitor sensor data updates
window.addEventListener('sensor_update', console.log)
\`\`\`

### Health Check Endpoints

**API Health Check**:
\`\`\`bash
curl http://localhost:8000/health
\`\`\`

**Sensor Status Check**:
\`\`\`bash
curl http://localhost:8000/api/sensors/status
\`\`\`

**WebSocket Test**:
\`\`\`javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onopen = () => console.log('WebSocket connected');
ws.onerror = (error) => console.error('WebSocket error:', error);
\`\`\`

### Performance Monitoring

**Server Performance**:
\`\`\`bash
# Monitor CPU and memory usage
top -p $(pgrep -f "python.*main.py")

# Check network connections
netstat -an | grep :8000
\`\`\`

**Client Performance**:
\`\`\`javascript
// Monitor render performance
performance.mark('dashboard-start')
// ... dashboard rendering
performance.mark('dashboard-end')
performance.measure('dashboard-render', 'dashboard-start', 'dashboard-end')
console.log(performance.getEntriesByType('measure'))
\`\`\`

## Getting Help

### Community Support
- **GitHub Issues**: Report bugs and feature requests
- **Discord Server**: Real-time community support
- **Documentation**: Comprehensive guides and examples

### Professional Support
- **Enterprise Support**: Priority support for business users
- **Custom Development**: Professional customization services
- **Training**: Workshops and training sessions

### Reporting Issues

**Bug Report Template**:
\`\`\`markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows 10/11, Linux, macOS
- Python Version: 3.x.x
- Node.js Version: 16.x.x
- Browser: Chrome/Firefox/Safari version

## Logs
\`\`\`
Paste relevant log output here
\`\`\`

## Additional Context
Any other relevant information
\`\`\`

This troubleshooting guide covers the most common issues and provides systematic approaches to diagnosing and resolving problems with the Ultimate Sensor Monitor.
\`\`\`

\`\`\`md file="docs/USER_GUIDE.md"
[v0-no-op-code-block-prefix]## Custom Widgets

### System Status Widget
The System Status Widget is a powerful multi-metric display that shows multiple sensor values in a compact, organized layout.

#### Adding a System Status Widget
1. **Enter Edit Mode**: Click the "Edit" button in the top toolbar
2. **Add Widget**: Click the "+" button and select "System Status" from the widget gallery
3. **Position Widget**: Drag the widget to your desired location
4. **Configure Metrics**: Click the widget to open the inspector panel

#### Configuring Metrics
1. **Add Metrics**: Click "Add Metric" in the inspector
2. **Select Sensor**: Choose a sensor from the dropdown list
3. **Set Label**: Give your metric a descriptive name
4. **Choose Format**: Select how the value should be displayed:
   - **Number**: Raw numeric value
   - **Percentage**: Value with % symbol
   - **Temperature**: Value with °C
   - **Frequency**: Value in MHz
   - **Bytes**: Automatically formatted (KB, MB, GB)
5. **Add Icon**: Choose an emoji icon for visual identification
6. **Set Thresholds**: Configure warning and critical levels for color coding

#### Layout Options
- **Compact**: Dense layout with small metrics (default)
- **Detailed**: Larger metrics with more spacing
- **Minimal**: Values only, no labels or icons

#### Example Configuration
\`\`\`
Metric 1: CPU Usage (🔥) - Percentage format
Metric 2: GPU Temperature (🌡️) - Temperature format  
Metric 3: Memory Usage (💾) - Bytes format
Metric 4: Network Speed (🌐) - Bytes format
\`\`\`

#### Best Practices
- **Group Related Metrics**: Keep similar sensors together
- **Use Descriptive Labels**: Make metrics easy to understand at a glance
- **Set Appropriate Thresholds**: Configure warning levels based on your hardware
- **Choose Meaningful Icons**: Use emojis that represent the metric type
- **Consider Layout**: Use compact for overview dashboards, detailed for focused monitoring
