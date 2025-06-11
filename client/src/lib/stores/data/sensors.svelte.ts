import type {
  SensorReading,
  SensorSource,
  HardwareNode,
  SensorCategory,
} from "$lib/types/sensors";
import { createDefaultSensorSource } from "$lib/models/sensorSource";

// Private state
let data = $state<Record<string, SensorReading>>({});
let sources = $state<SensorSource[]>([]);
let tree = $state<HardwareNode[]>([]);

// Derived state (exported)
export const availableSensors = $derived(Object.values(data));
export const activeSensors = $derived(
  availableSensors.filter((s) => s.value !== undefined),
);
export const sensorCategories = $derived(
  Array.from(
    new Set(
      availableSensors
        .map((s) => s.category)
        .filter((c): c is SensorCategory => !!c),
    ),
  ),
);
export const sensorSources = $derived(sources);
export const hardwareTree = $derived(tree);

// Updater functions (exported)
export function updateSensorData(newData: Record<string, SensorReading>) {
  data = newData;
}

export function updateSensorSources(apiPayload: Record<string, any>) {
  if (!apiPayload || typeof apiPayload !== "object") {
    sources = [];
    return;
  }
  sources = Object.values(apiPayload).map((sourceAPI) => {
    return createDefaultSensorSource(
      sourceAPI.source_id,
      sourceAPI.name,
      sourceAPI.is_active,
      sourceAPI.update_interval,
    );
  });
}

export function updateHardwareTree(newTree: HardwareNode | HardwareNode[]) {
  tree = Array.isArray(newTree) ? newTree : newTree ? [newTree] : [];
}

// Getter functions (exported)
export function getSensorById(id: string): SensorReading | undefined {
  return data[id];
}

export function getSensorsByCategory(category: string): SensorReading[] {
  return availableSensors.filter((s) => s.category === category);
}

export function getSensorsBySource(sourceId: string): SensorReading[] {
  return availableSensors.filter((s) => s.source === sourceId);
}
