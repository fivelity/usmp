import { writable, derived } from "svelte/store";
import type { SensorReading, SensorSource } from "$lib/types/sensors";
import type { HardwareNode } from "$lib/stores/hardwareTree";

// Create writable stores for the base data
const sensorDataStore = writable<Record<string, SensorReading>>({});
const sensorSourcesStore = writable<SensorSource[]>([]);
const availableSensorsStore = writable<SensorReading[]>([]);
const hardwareTreeStore = writable<HardwareNode[]>([]);

// Create derived stores
const activeSensors = derived(
  sensorDataStore,
  ($sensorData: Record<string, SensorReading>) =>
    Object.values($sensorData).filter(
      (sensor: SensorReading) => sensor.value !== undefined,
    ),
);

const sensorCategories = derived(
  sensorDataStore,
  ($sensorData: Record<string, SensorReading>) => {
    const categories = new Set<string>();
    Object.values($sensorData).forEach((sensor: SensorReading) => {
      if (sensor.category) {
        categories.add(sensor.category);
      }
    });
    return Array.from(categories);
  },
);

// Create utility functions
const sensorUtils = {
  updateSensorData(data: Record<string, SensorReading>) {
    sensorDataStore.set(data);
    availableSensorsStore.set(Object.values(data));
  },

  updateSensorSources(apiPayload: Record<string, any>) {
    const newSensorSources: SensorSource[] = [];

    if (apiPayload && typeof apiPayload === "object") {
      const sourcesFromAPIArray = Object.values(apiPayload);

      for (const sourceAPI of sourcesFromAPIArray) {
        if (sourceAPI) {
          newSensorSources.push({
            id: sourceAPI.source_id,
            name: sourceAPI.name,
            active: sourceAPI.available,
            description: "",
            version: "1.0.0",
            connection_status: sourceAPI.available ? "connected" : "disconnected",
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
                total_sensors: sourceAPI.sensor_count || 0,
                active_sensors: sourceAPI.sensor_count || 0,
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
          });
        }
      }
    }
    sensorSourcesStore.set(newSensorSources);
  },

  updateHardwareTree(tree: HardwareNode | HardwareNode[]) {
    const treeArray = Array.isArray(tree) ? tree : tree ? [tree] : [];
    hardwareTreeStore.set(treeArray);
  },

  getSensorById(id: string): SensorReading | undefined {
    let result: SensorReading | undefined;
    sensorDataStore.subscribe((state) => {
      result = state[id];
    })();
    return result;
  },

  getSensorsByCategory(category: string): SensorReading[] {
    let result: SensorReading[] = [];
    sensorDataStore.subscribe((state) => {
      result = Object.values(state).filter(
        (sensor) => sensor.category === category,
      );
    })();
    return result;
  },

  getSensorsBySource(sourceId: string): SensorReading[] {
    let result: SensorReading[] = [];
    sensorDataStore.subscribe((state) => {
      result = Object.values(state).filter(
        (sensor) => sensor.source === sourceId,
      );
    })();
    return result;
  },
};

// Export the stores and utilities
export {
  sensorDataStore as sensorData,
  sensorSourcesStore as sensorSources,
  availableSensorsStore as availableSensors,
  hardwareTreeStore as hardwareTree,
  activeSensors,
  sensorCategories,
  sensorUtils,
};
