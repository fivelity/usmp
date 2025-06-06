import { writable, derived } from 'svelte/store';
import type { SensorReading, SensorSource } from '$lib/types/sensors';
import type { HardwareNode } from '$lib/stores/hardwareTree';

// Create writable stores for the base data
const sensorDataStore = writable<Record<string, SensorReading>>({});
const sensorSourcesStore = writable<SensorSource[]>([]);
const availableSensorsStore = writable<SensorReading[]>([]);
const hardwareTreeStore = writable<HardwareNode[]>([]);

// Create derived stores
const activeSensors = derived(sensorDataStore, ($sensorData: Record<string, SensorReading>) => 
  Object.values($sensorData).filter((sensor: SensorReading) => sensor.value !== undefined)
);

const sensorCategories = derived(sensorDataStore, ($sensorData: Record<string, SensorReading>) => {
  const categories = new Set<string>();
  Object.values($sensorData).forEach((sensor: SensorReading) => {
    if (sensor.category) {
      categories.add(sensor.category);
    }
  });
  return Array.from(categories);
});

// Create utility functions
const sensorUtils = {
  updateSensorData(data: Record<string, SensorReading>) {
    sensorDataStore.set(data);
  },

  updateSensorSources(apiPayload: Record<string, any>) {
    const newAvailableSensors: SensorReading[] = [];
    const newSensorSources: SensorSource[] = [];

    if (apiPayload && typeof apiPayload === 'object') {
      const sourcesFromAPIArray = Object.values(apiPayload);
      
      for (const sourceAPI of sourcesFromAPIArray) {
        if (sourceAPI && sourceAPI.active && sourceAPI.hardware_components) {
          const currentSourceSensors: SensorReading[] = [];
          
          // Process hardware components and their sensors
          sourceAPI.hardware_components.forEach((component: any) => {
            if (component.sensors) {
              component.sensors.forEach((sensor: any) => {
                if (sensor) {
                  newAvailableSensors.push({
                    id: sensor.id,
                    name: sensor.name,
                    category: sensor.category,
                    unit: sensor.unit,
                    source: sourceAPI.id,
                    value: sensor.value,
                    min_value: sensor.min_value,
                    max_value: sensor.max_value,
                    hardware_type: sensor.hardware_type,
                    parent_hardware: component.id,
                    timestamp: sensor.timestamp,
                    status: sensor.status,
                    quality: sensor.quality,
                    metadata: sensor.metadata
                  });
                  currentSourceSensors.push(sensor);
                }
              });
            }
          });

          newSensorSources.push({
            id: sourceAPI.id,
            name: sourceAPI.name,
            description: sourceAPI.description || '',
            version: sourceAPI.version || '',
            active: sourceAPI.active,
            connection_status: sourceAPI.connection_status || 'disconnected',
            hardware_components: sourceAPI.hardware_components || [],
            capabilities: sourceAPI.capabilities || {
              supports_real_time: false,
              supports_history: false,
              supports_alerts: false,
              supports_calibration: false,
              min_update_interval: 1000,
              max_update_interval: 5000,
              supported_hardware_types: [],
              supported_sensor_categories: []
            },
            configuration: sourceAPI.configuration || {
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
              sensor_filters: []
            },
            statistics: sourceAPI.statistics || {
              total_sensors: 0,
              active_sensors: 0,
              update_count: 0,
              error_count: 0,
              last_successful_update: '',
              average_update_time: 0
            },
            last_update: sourceAPI.last_update || new Date().toISOString(),
            error_message: sourceAPI.error_message
          });
        } else if (sourceAPI) {
          newSensorSources.push({
            id: sourceAPI.id,
            name: sourceAPI.name,
            description: sourceAPI.description || '',
            version: sourceAPI.version || '',
            active: sourceAPI.active,
            connection_status: sourceAPI.connection_status || 'disconnected',
            hardware_components: [],
            capabilities: sourceAPI.capabilities || {
              supports_real_time: false,
              supports_history: false,
              supports_alerts: false,
              supports_calibration: false,
              min_update_interval: 1000,
              max_update_interval: 5000,
              supported_hardware_types: [],
              supported_sensor_categories: []
            },
            configuration: sourceAPI.configuration || {
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
              sensor_filters: []
            },
            statistics: sourceAPI.statistics || {
              total_sensors: 0,
              active_sensors: 0,
              update_count: 0,
              error_count: 0,
              last_successful_update: '',
              average_update_time: 0
            },
            last_update: sourceAPI.last_update || new Date().toISOString(),
            error_message: sourceAPI.error_message
          });
        }
      }
    }

    sensorSourcesStore.set(newSensorSources);
    availableSensorsStore.set(newAvailableSensors);
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
        (sensor) => sensor.category === category
      );
    })();
    return result;
  },

  getSensorsBySource(sourceId: string): SensorReading[] {
    let result: SensorReading[] = [];
    sensorDataStore.subscribe((state) => {
      result = Object.values(state).filter(
        (sensor) => sensor.source === sourceId
      );
    })();
    return result;
  }
};

// Export the stores and utilities
export {
  sensorDataStore as sensorData,
  sensorSourcesStore as sensorSources,
  availableSensorsStore as availableSensors,
  hardwareTreeStore as hardwareTree,
  activeSensors,
  sensorCategories,
  sensorUtils
};
