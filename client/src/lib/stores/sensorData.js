import { writable, derived } from "svelte/store";

// Core sensor data store
export const sensorData = writable({});

// Sensor sources (e.g., CPU, GPU, etc.)
export const sensorSources = writable([]);

// Full hardware tree retrieved from backend (if available)
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
  updateSensorData: (newData) => {
    sensorData.set(newData);
  },

  getSensorById: (id) => {
    let data;
    sensorData.subscribe((value) => (data = value))();
    return data[id] || null;
  },

  /**
   * Update the list of sensor sources (returned by /sensors/definitions).
   */
  updateSensorSources: (sources) => {
    sensorSources.set(sources ?? []);
  },

  /**
   * Update the hardware tree (device hierarchy) for advanced widgets.
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
