/**
 * Sensor Data Store (Svelte 5 Runes)
 * Manages sensor data, sources, and real-time updates in a centralized, reactive store.
 */
import type { SensorReading, SensorSource } from '$lib/types/sensors';
import { sensorDataManager as originalSensorDataManager } from '$lib/stores/sensorData';

/**
 * The reactive state object, serving as the single source of truth for sensor data.
 */
const state = $state({
  sensorData: {} as Record<string, SensorReading>,
  sensorSources: [] as SensorSource[],
  hardwareTree: [] as Record<string, unknown>[]
});

// Export availableSensors as a function for backward compatibility
// This follows Svelte 5 rules that derived state can't be directly exported
export function availableSensors() {
  return Object.values(state.sensorData);
}

// Re-export sensorDataManager for backward compatibility
export const sensorDataManager = originalSensorDataManager;

/**
 * The public interface for the sensor store.
 * It exports reactive state values (getters) and mutation functions to ensure controlled state updates.
 */
export const sensors = {
  // Reactive state accessors (runes)
  get data() {
    return state.sensorData;
  },
  get sources() {
    return state.sensorSources;
  },
  get tree() {
    return state.hardwareTree;
  },
  get available() {
    return Object.values(state.sensorData);
  },

  // Mutation functions to modify the state
  updateData(data: Record<string, SensorReading>): void {
    Object.assign(state.sensorData, data);
  },

  updateSources(sources: SensorSource[]): void {
    state.sensorSources = sources;
  },

  updateTree(tree: Record<string, unknown>[]): void {
    state.hardwareTree = tree;
  },

  clearAll(): void {
    state.sensorData = {};
    state.sensorSources = [];
    state.hardwareTree = [];
  }
};
