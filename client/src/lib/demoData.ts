/**
 * Demo data for Ultimate Sensor Monitor Reimagined
 * Creates sample widgets and sensor data for showcasing functionality
 */

import type { WidgetConfig, SensorReading as SensorData, SensorSource, SensorReading } from "./types/index";
import { sensorStore } from "./stores/data/sensors.svelte";

export const demoSensorSources: Record<string, SensorSource> = {
  mock: {
    id: "mock",
    name: "Mock Hardware Sensors",
    description: "Simulated hardware sensors for demonstration purposes.",
    version: "1.0.0",
    active: true,
    connection_status: "connected",
    capabilities: {
      supports_real_time: true,
      supports_history: false,
      supports_alerts: false,
      supports_calibration: false,
      min_update_interval: 1000,
      max_update_interval: 5000,
      supported_hardware_types: ["cpu", "gpu", "memory", "motherboard", "storage", "network"],
      supported_sensor_categories: ["temperature", "voltage", "clock", "load", "fan", "power", "data", "throughput", "usage", "frequency", "energy", "noise"],
    },
    configuration: {
      update_interval: 1000,
      enable_auto_discovery: true,
      enable_hardware_acceleration: false,
      enable_detailed_logging: false,
      timeout_duration: 5000,
      retry_attempts: 3,
      buffer_size: 100,
      compression_enabled: false,
      filter_inactive_sensors: true,
      hardware_filters: [],
      sensor_filters: [],
    },
    statistics: {
      total_sensors: 10, // Update this count based on actual sensors
      active_sensors: 10, // Update this count
      update_count: 0,
      error_count: 0,
      average_update_time: 0,
      data_throughput: 0,
      uptime: 0,
      performance_metrics: {
        cpu_usage: 0,
        memory_usage: 0,
        network_usage: 0,
        update_latency: 0,
        queue_size: 0,
        dropped_updates: 0,
      },
    },
    last_update: new Date().toISOString(),
    hardware_components: [
      {
        id: "mock_system_main",
        name: "Mock System",
        type: "motherboard", // Or a general 'system' type if available/appropriate
        status: "online",
        last_update: new Date().toISOString(),
        sub_hardware: [],
        sensors: [
          {
            id: "cpu_temp",
            name: "CPU Temperature",
            value: 65,
            unit: "℃",
            min_value: 0,
            max_value: 100,
            source: "mock",
            category: "temperature",
            hardware_type: "cpu",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "cpu_usage",
            name: "CPU Usage",
            value: 45,
            unit: "%",
            min_value: 0,
            max_value: 100,
            source: "mock",
            category: "usage",
            hardware_type: "cpu",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "gpu_temp",
            name: "GPU Temperature",
            value: 72,
            unit: "℃",
            min_value: 0,
            max_value: 110,
            source: "mock",
            category: "temperature",
            hardware_type: "gpu",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "ram_usage",
            name: "Memory Usage",
            value: 62.1,
            unit: "%",
            min_value: 0,
            max_value: 100,
            source: "mock",
            category: "usage",
            hardware_type: "memory",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "fan_speed_cpu",
            name: "CPU Fan Speed",
            value: 1500,
            unit: "RPM",
            min_value: 0,
            max_value: 4000,
            source: "mock",
            category: "fan",
            hardware_type: "motherboard",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "psu_power_draw",
            name: "PSU Power Draw",
            value: 350,
            unit: "W",
            min_value: 0,
            max_value: 750,
            source: "mock",
            category: "power",
            hardware_type: "motherboard",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "cpu_frequency",
            name: "CPU Frequency",
            value: 3.5,
            unit: "GHz",
            min_value: 0.8,
            max_value: 4.5,
            source: "mock",
            category: "frequency",
            hardware_type: "cpu",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "disk_usage",
            name: "Disk Usage (C:)",
            value: 78.3,
            unit: "%",
            min_value: 0,
            max_value: 100,
            source: "mock",
            category: "usage",
            hardware_type: "storage",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "network_upload",
            name: "Network Upload",
            value: 1.5,
            unit: "Mbps",
            min_value: 0,
            max_value: 100,
            source: "mock",
            category: "throughput",
            hardware_type: "network",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
          {
            id: "network_download",
            name: "Network Download",
            value: 25.0,
            unit: "Mbps",
            min_value: 0,
            max_value: 500,
            source: "mock",
            category: "throughput",
            hardware_type: "network",
            status: "active",
            quality: "good",
            timestamp: new Date().toISOString(),
          },
        ],
      },
    ],
  },
};

export const demoSensorData: Record<string, SensorData> = {};
if (demoSensorSources.mock && demoSensorSources.mock.hardware_components[0]) {
  demoSensorSources.mock.hardware_components[0].sensors.forEach((sensor: SensorData) => {
    demoSensorData[sensor.id] = sensor;
  });
}

export const demoWidgets: WidgetConfig[] = [
  {
    id: "widget_cpu_temp_radial",
    sensor_id: "cpu_temp",
    type: "radial",
    gauge_type: "radial",
    pos_x: 50,
    pos_y: 50,
    width: 200,
    height: 200,
    z_index: 1,
    is_locked: false,
    gauge_settings: {
      start_angle: 0,
      end_angle: 270,
      color_primary: "#3b82f6",
      stroke_width: 8,
    },
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false,
    title: "CPU Temperature",
  },
  {
    id: "widget_cpu_usage_linear",
    sensor_id: "cpu_usage",
    type: "linear",
    gauge_type: "linear",
    pos_x: 300,
    pos_y: 50,
    width: 250,
    height: 100,
    z_index: 1,
    is_locked: false,
    gauge_settings: {
      orientation: "horizontal",
      color_primary: "#10b981",
    },
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false,
    title: "CPU Usage",
  },
  {
    id: "widget_gpu_temp_text",
    sensor_id: "gpu_temp",
    type: "text",
    gauge_type: "text",
    pos_x: 600,
    pos_y: 50,
    width: 180,
    height: 120,
    z_index: 1,
    is_locked: false,
    gauge_settings: {},
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false,
    title: "GPU Temperature",
  },
  {
    id: "widget_ram_usage_graph",
    sensor_id: "ram_usage",
    type: "graph",
    gauge_type: "graph",
    pos_x: 50,
    pos_y: 300,
    width: 300,
    height: 200,
    z_index: 1,
    is_locked: false,
    gauge_settings: {
      time_range: 60,
      line_color: "#8b5cf6",
      fill_area: true,
      show_points: false,
    },
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false,
    title: "RAM Usage",
  },
  {
    id: "widget_fan_speed_radial",
    sensor_id: "fan_speed_cpu",
    type: "radial",
    gauge_type: "radial",
    pos_x: 400,
    pos_y: 300,
    width: 180,
    height: 180,
    z_index: 1,
    is_locked: false,
    gauge_settings: {
      start_angle: 45,
      end_angle: 315,
      color_primary: "#f59e0b",
      stroke_width: 6,
    },
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false,
    title: "Fan Speed",
  },
  {
    id: "widget_power_text",
    sensor_id: "psu_power_draw",
    type: "text",
    gauge_type: "text",
    pos_x: 620,
    pos_y: 300,
    width: 160,
    height: 100,
    z_index: 1,
    is_locked: false,
    gauge_settings: {},
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false,
    title: "Power Consumption",
  },
];

// Function to simulate live sensor data updates
export function updateDemoData(): void {
  const updated: Record<string, Partial<SensorData>> = {};
  Object.keys(demoSensorData).forEach((sensorId) => {
    const sensor = demoSensorData[sensorId];
    if (!sensor) return;
    updated[sensorId] = { ...demoSensorData[sensorId] };

    // Simulate realistic sensor value changes
    const variance = 0.02; // 2% variance
    const change = (Math.random() - 0.5) * 2 * variance;

    if (typeof sensor.value === "number") {
      let newValue = sensor.value * (1 + change);

      // Keep within realistic bounds
      if (sensor.min_value !== undefined && sensor.max_value !== undefined) {
        newValue = Math.max(
          sensor.min_value,
          Math.min(sensor.max_value, newValue),
        );
      }

      // Special handling for different sensor types
      switch (sensorId) {
        case "cpu_temp":
        case "gpu_temp":
          // Temperature fluctuates more slowly
          newValue = sensor.value + (Math.random() - 0.5) * 2;
          break;
        case "cpu_usage":
        case "ram_usage":
          // Usage can change more dramatically
          newValue = sensor.value + (Math.random() - 0.5) * 10;
          break;
        case "fan_speed":
          // Fan speed changes in larger increments
          newValue = sensor.value + (Math.random() - 0.5) * 100;
          break;
        case "network_upload":
        case "network_download":
          // Network activity can be very volatile
          newValue = Math.max(0, sensor.value + (Math.random() - 0.5) * 5);
          break;
      }

      updated[sensorId] = {
        ...sensor,
        value: Math.round(newValue * 10) / 10, // Round to 1 decimal
        timestamp: new Date().toISOString(),
      };
    }
  });

  sensorStore.updateMultipleSensors(updated as Record<string, SensorReading>);
}
