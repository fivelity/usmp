import { writable, derived, get } from "svelte/store";
import type { Writable } from "svelte/store";
import type {
  SensorReading,
  SensorSource,
  HardwareComponent,
  SensorCategory,
} from "$lib/types/sensors";

// Internal stores (not exported directly)
const _sensorData: Writable<Record<string, SensorReading>> = writable({});
const _sensorSources: Writable<SensorSource[]> = writable([]);
const _hardwareTree: Writable<HardwareComponent[]> = writable([]);

// Internal derived stores
const _sensorsByCategory = derived(
  _sensorData, // Use internal store
  ($_sensorData): Record<SensorCategory, SensorReading[]> => {
    const categories = {} as Record<SensorCategory, SensorReading[]>;
    Object.values($_sensorData).forEach((sensor: SensorReading) => {
      if (sensor && sensor.category) {
        const categoryKey = sensor.category;
        if (!categories[categoryKey]) {
          categories[categoryKey] = [];
        }
        categories[categoryKey].push(sensor);
      }
    });
    return categories;
  },
);

const _activeSensors = derived(
  _sensorData, // Use internal store
  ($_sensorData): SensorReading[] => {
    return Object.values($_sensorData).filter(
      (sensor: SensorReading) => sensor.status === "active",
    );
  },
);

// Single export object encapsulating stores (via getters) and methods
export const sensorDataManager = {
  // Expose stores via getters for reactivity
  get sensorDataStore() {
    return _sensorData;
  },
  get sensorSourcesStore() {
    return _sensorSources;
  },
  get hardwareTreeStore() {
    return _hardwareTree;
  },
  get sensorsByCategoryStore() {
    return _sensorsByCategory;
  },
  get activeSensorsStore() {
    return _activeSensors;
  },

  // Utility methods
  updateSensorData: (newData: Record<string, SensorReading>): void => {
    _sensorData.set(newData);
  },
  getSensorById: (id: string): SensorReading | null => {
    const currentSensorData = get(_sensorData);
    return currentSensorData[id] || null;
  },
  updateSensorSources: (sources: SensorSource[] | null): void => {
    _sensorSources.set(sources ?? []);
  },
  updateHardwareTree: (tree: HardwareComponent[] | null): void => {
    _hardwareTree.set(tree ?? []);
  },
  clearSensorData: (): void => {
    _sensorData.set({});
    _sensorSources.set([]);
    _hardwareTree.set([]);
  },
};

// Add missing exports that other files expect
export const updateSensorData = sensorDataManager.updateSensorData;
export const updateSensorSources = sensorDataManager.updateSensorSources;
export const updateHardwareTree = sensorDataManager.updateHardwareTree;
