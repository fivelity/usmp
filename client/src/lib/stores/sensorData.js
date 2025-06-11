import { writable, derived } from "svelte/store";

// eslint-disable-next-line spaced-comment
/**
 * Sensor data stores with explicit typings to satisfy TypeScript in a .js module.
 * Use JSDoc + generic parameters so that `noImplicitAny` checks pass without
 * converting the file to .ts yet.
 */

// Type imports (erased at compile-time)
/** @typedef {import("$lib/types/sensors").SensorReading} SensorReading */
/** @typedef {import("$lib/types/sensors").SensorSource}  SensorSource */
/** @typedef {import("$lib/types/sensors").HardwareComponent} HardwareComponent */

// Core sensor data store
/** @type {import("svelte/store").Writable<Record<string, SensorReading>>} */
export const sensorData = writable({});

// Sensor sources (e.g., CPU, GPU, etc.)
/** @type {import("svelte/store").Writable<SensorSource[]>} */
export const sensorSources = writable([]);

// Full hardware tree retrieved from backend (if available)
/** @type {import("svelte/store").Writable<HardwareComponent[]>} */
export const hardwareTree = writable([]);

// Derived stores for organized access
export const sensorsByCategory = derived(sensorData, ($sensorData) => {
  const categories = {};

  Object.values($sensorData).forEach((sensor) => {
    if (!categories[sensor.category]) {
      categories[sensor.category] = [];
    }
    categories[sensor.category].push(sensor);
  });

  return categories;
});

export const activeSensors = derived(sensorData, ($sensorData) => {
  return Object.values($sensorData).filter(
    (sensor) => sensor.value !== null && sensor.value !== undefined,
  );
});

// Utility functions
export const sensorUtils = {
  /**
   * Replace the entire sensor data map.
   * @param {Record<string, SensorReading>} newData
   */
  updateSensorData: (newData) => {
    sensorData.set(newData);
  },

  /**
   * Retrieve a single sensor by its unique ID.
   * @param {string} id
   * @returns {SensorReading | null}
   */
  getSensorById: (id) => {
    let data;
    sensorData.subscribe((value) => (data = value))();
    return data[id] || null;
  },

  /**
   * Update available sensor sources returned from the backend.
   * @param {SensorSource[] | null} sources
   */
  updateSensorSources: (sources) => {
    sensorSources.set(sources ?? []);
  },

  /**
   * Update hierarchy of hardware components.
   * @param {HardwareComponent[] | null} tree
   */
  updateHardwareTree: (tree) => {
    hardwareTree.set(tree ?? []);
  },

  clearSensorData: () => {
    sensorData.set({});
    sensorSources.set([]);
    hardwareTree.set([]);
  },
};
