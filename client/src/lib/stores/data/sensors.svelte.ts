/**
 * Sensor Data Store (Svelte 5 Runes)
 * Manages sensor data, sources, and real-time updates
 */
import type { SensorReading, SensorSource } from "$lib/types/sensors";

// Internal state
const state = $state({
  sensorData: {} as Record<string, SensorReading>,
  sensorSources: [] as SensorSource[],
  availableSensors: [] as SensorReading[],
  hardwareTree: [] as Record<string, unknown>[],
  version: 0,
});

// Getter functions
export function getSensorData(): Record<string, SensorReading> {
  return { ...state.sensorData };
}

export function getSensorSources(): SensorSource[] {
  return [...state.sensorSources];
}

export function getAvailableSensors(): SensorReading[] {
  return [...state.availableSensors];
}

export function getHardwareTree(): Record<string, unknown>[] {
  return [...state.hardwareTree];
}

export function getSensorById(id: string): SensorReading | undefined {
  return state.sensorData[id];
}

// Mutation functions
export function updateSensorData(data: Record<string, SensorReading>): void {
  Object.assign(state.sensorData, data);
  state.version++;
}

export function updateSensorSources(sources: SensorSource[]): void {
  state.sensorSources = sources;
  state.version++;
}

export function updateAvailableSensors(sensors: SensorReading[]): void {
  state.availableSensors = sensors;
  state.version++;
}

export function updateHardwareTree(tree: Record<string, unknown>[]): void {
  state.hardwareTree = tree;
  state.version++;
}

// Legacy compatibility
export const sensorStore = {
  getSensorData,
  getSensorSources,
  getAvailableSensors,
  updateSensorData,
  updateSensorSources,
  updateAvailableSensors,
  updateHardwareTree,

  // Additional compatibility functions
  clearAllSensors(): void {
    state.sensorData = {};
    state.sensorSources = [];
    state.availableSensors = [];
    state.hardwareTree = [];
    state.version++;
  },

  updateMultipleSensors(data: Record<string, SensorReading>): void {
    Object.assign(state.sensorData, data);
    state.version++;
  },
};

// Export aliases for backwards compatibility
export const availableSensors = getAvailableSensors();
