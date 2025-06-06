/**
 * Demo data for Ultimate Sensor Monitor Reimagined
 * Creates sample widgets and sensor data for showcasing functionality
 */

import type { WidgetConfig, SensorData, SensorSource } from './types/index';

export const demoSensorSources: Record<string, SensorSource> = {
  mock: {
    id: 'mock',
    name: 'Mock Hardware Sensors',
    active: true,
    last_update: new Date().toISOString(),
    sensors: [
      {
        id: 'cpu_temp',
        name: 'CPU Temperature',
        value: 67.5,
        unit: '°C',
        min_value: 30,
        max_value: 90,
        source: 'mock',
        category: 'temperature',
        timestamp: new Date().toISOString()
      },
      {
        id: 'cpu_usage',
        name: 'CPU Usage',
        value: 45.2,
        unit: '%',
        min_value: 0,
        max_value: 100,
        source: 'mock',
        category: 'usage',
        timestamp: new Date().toISOString()
      },
      {
        id: 'gpu_temp',
        name: 'GPU Temperature',
        value: 72.8,
        unit: '°C',
        min_value: 30,
        max_value: 95,
        source: 'mock',
        category: 'temperature',
        timestamp: new Date().toISOString()
      },
      {
        id: 'ram_usage',
        name: 'Memory Usage',
        value: 62.1,
        unit: '%',
        min_value: 0,
        max_value: 100,
        source: 'mock',
        category: 'usage',
        timestamp: new Date().toISOString()
      },
      {
        id: 'fan_speed',
        name: 'CPU Fan Speed',
        value: 1850,
        unit: 'RPM',
        min_value: 800,
        max_value: 3000,
        source: 'mock',
        category: 'fan',
        timestamp: new Date().toISOString()
      },
      {
        id: 'power_consumption',
        name: 'System Power',
        value: 185.5,
        unit: 'W',
        min_value: 50,
        max_value: 400,
        source: 'mock',
        category: 'power',
        timestamp: new Date().toISOString()
      },
      {
        id: 'cpu_frequency',
        name: 'CPU Frequency',
        value: 3.2,
        unit: 'GHz',
        min_value: 1.0,
        max_value: 4.5,
        source: 'mock',
        category: 'frequency',
        timestamp: new Date().toISOString()
      },
      {
        id: 'disk_usage',
        name: 'Disk Usage (C:)',
        value: 78.3,
        unit: '%',
        min_value: 0,
        max_value: 100,
        source: 'mock',
        category: 'usage',
        timestamp: new Date().toISOString()
      },
      {
        id: 'network_upload',
        name: 'Network Upload',
        value: 2.4,
        unit: 'MB/s',
        min_value: 0,
        max_value: 100,
        source: 'mock',
        category: 'network',
        timestamp: new Date().toISOString()
      },
      {
        id: 'network_download',
        name: 'Network Download',
        value: 15.7,
        unit: 'MB/s',
        min_value: 0,
        max_value: 100,
        source: 'mock',
        category: 'network',
        timestamp: new Date().toISOString()
      }
    ]
  }
};

export const demoSensorData: Record<string, SensorData> = {};
demoSensorSources.mock.sensors.forEach(sensor => {
  demoSensorData[sensor.id] = sensor;
});

export const demoWidgets: WidgetConfig[] = [
  {
    id: 'widget_cpu_temp_radial',
    sensor_id: 'cpu_temp',
    gauge_type: 'radial',
    pos_x: 50,
    pos_y: 50,
    width: 200,
    height: 200,
    rotation: 0,
    z_index: 1,
    is_locked: false,
    show_label: true,
    show_unit: true,
    gauge_settings: {
      start_angle: 0,
      end_angle: 270,
      color_primary: '#3b82f6',
      stroke_width: 8
    },
    style_settings: {}
  },
  {
    id: 'widget_cpu_usage_linear',
    sensor_id: 'cpu_usage',
    gauge_type: 'linear',
    pos_x: 300,
    pos_y: 50,
    width: 250,
    height: 100,
    rotation: 0,
    z_index: 1,
    is_locked: false,
    show_label: true,
    show_unit: true,
    gauge_settings: {
      orientation: 'horizontal',
      color_primary: '#10b981'
    },
    style_settings: {}
  },
  {
    id: 'widget_gpu_temp_text',
    sensor_id: 'gpu_temp',
    gauge_type: 'text',
    pos_x: 600,
    pos_y: 50,
    width: 180,
    height: 120,
    rotation: 0,
    z_index: 1,
    is_locked: false,
    show_label: true,
    show_unit: true,
    gauge_settings: {},
    style_settings: {}
  },
  {
    id: 'widget_ram_usage_graph',
    sensor_id: 'ram_usage',
    gauge_type: 'graph',
    pos_x: 50,
    pos_y: 300,
    width: 300,
    height: 200,
    rotation: 0,
    z_index: 1,
    is_locked: false,
    show_label: true,
    show_unit: true,
    gauge_settings: {
      time_range: 60,
      line_color: '#8b5cf6',
      fill_area: true,
      show_points: false
    },
    style_settings: {}
  },
  {
    id: 'widget_fan_speed_radial',
    sensor_id: 'fan_speed',
    gauge_type: 'radial',
    pos_x: 400,
    pos_y: 300,
    width: 180,
    height: 180,
    rotation: 0,
    z_index: 1,
    is_locked: false,
    show_label: true,
    show_unit: true,
    gauge_settings: {
      start_angle: 45,
      end_angle: 315,
      color_primary: '#f59e0b',
      stroke_width: 6
    },
    style_settings: {}
  },
  {
    id: 'widget_power_text',
    sensor_id: 'power_consumption',
    gauge_type: 'text',
    pos_x: 620,
    pos_y: 300,
    width: 160,
    height: 100,
    rotation: 0,
    z_index: 1,
    is_locked: false,
    show_label: true,
    show_unit: true,
    gauge_settings: {},
    style_settings: {}
  }
];

// Function to simulate live sensor data updates
export function updateDemoData(): Record<string, SensorData> {
  const updated = { ...demoSensorData };
  
  // Simulate realistic sensor value changes
  Object.keys(updated).forEach(sensorId => {
    const sensor = updated[sensorId];
    const variance = 0.02; // 2% variance
    const change = (Math.random() - 0.5) * 2 * variance;
    
    if (typeof sensor.value === 'number') {
      let newValue = sensor.value * (1 + change);
      
      // Keep within realistic bounds
      if (sensor.min_value !== undefined && sensor.max_value !== undefined) {
        newValue = Math.max(sensor.min_value, Math.min(sensor.max_value, newValue));
      }
      
      // Special handling for different sensor types
      switch (sensorId) {
        case 'cpu_temp':
        case 'gpu_temp':
          // Temperature fluctuates more slowly
          newValue = sensor.value + (Math.random() - 0.5) * 2;
          break;
        case 'cpu_usage':
        case 'ram_usage':
          // Usage can change more dramatically
          newValue = sensor.value + (Math.random() - 0.5) * 10;
          break;
        case 'fan_speed':
          // Fan speed changes in larger increments
          newValue = sensor.value + (Math.random() - 0.5) * 100;
          break;
        case 'network_upload':
        case 'network_download':
          // Network activity can be very volatile
          newValue = Math.max(0, sensor.value + (Math.random() - 0.5) * 5);
          break;
      }
      
      updated[sensorId] = {
        ...sensor,
        value: Math.round(newValue * 10) / 10, // Round to 1 decimal
        timestamp: new Date().toISOString()
      };
    }
  });
  
  return updated;
}
