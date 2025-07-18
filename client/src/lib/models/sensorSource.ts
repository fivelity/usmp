import type { SensorSource } from "$lib/types/sensors";

export function createDefaultSensorSource(
  id: string,
  name: string,
  isActive: boolean,
  sensorCount: number,
): SensorSource {
  return {
    id: id,
    name: name,
    active: isActive,
    description: `Source for ${name}`,
    version: "1.0.0",
    connection_status: isActive ? "connected" : "disconnected",
    hardware_components: [],
    capabilities: {
      supports_real_time: true,
      supports_history: false,
      supports_alerts: false,
      supports_calibration: false,
      min_update_interval: 1000,
      max_update_interval: 5000,
      supported_hardware_types: [],
      supported_sensor_categories: [],
    },
    configuration: {
      update_interval: 1000,
      enable_auto_discovery: true,
      enable_hardware_acceleration: false,
      enable_detailed_logging: false,
      timeout_duration: 5000,
      retry_attempts: 3,
      buffer_size: 1000,
      compression_enabled: false,
      filter_inactive_sensors: true,
      hardware_filters: [],
      sensor_filters: [],
    },
    statistics: {
      total_sensors: sensorCount || 0,
      active_sensors: sensorCount || 0,
      update_count: 0,
      error_count: 0,
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
      average_update_time: 0,
    },
    last_update: new Date().toISOString(),
    error_message: undefined,
  };
}
