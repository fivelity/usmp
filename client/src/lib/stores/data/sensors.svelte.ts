import type { SensorReading, SensorSource, HardwareNode } from '$lib/types/sensors';
import { createDefaultSensorSource } from '$lib/models/sensorSource';

function createSensorState() {
  let data = $state<Record<string, SensorReading>>({});
  let sources = $state<SensorSource[]>([]);
  let tree = $state<HardwareNode[]>([]);

  const availableSensors = $derived(Object.values(data));
  const activeSensors = $derived(availableSensors.filter((s: SensorReading) => s.value !== undefined));
  const categories = $derived(
    Array.from(new Set(availableSensors.map((s: SensorReading) => s.category).filter((c): c is string => !!c)))
  );

  return {
    get data() {
      return data;
    },
    get sources() {
      return sources;
    },
    get tree() {
      return tree;
    },
    get availableSensors() {
      return availableSensors;
    },
    get activeSensors() {
      return activeSensors;
    },
    get categories() {
      return categories;
    },

    updateSensorData(newData: Record<string, SensorReading>) {
      data = newData;
    },

    updateSensorSources(apiPayload: Record<string, any>) {
      if (!apiPayload || typeof apiPayload !== 'object') {
        sources = [];
        return;
      }

      sources = Object.values(apiPayload).map((sourceAPI) => {
        return createDefaultSensorSource(
            sourceAPI.source_id,
            sourceAPI.name,
            sourceAPI.available,
            sourceAPI.sensor_count
        );
      });
    },

    updateHardwareTree(newTree: HardwareNode | HardwareNode[]) {
      tree = Array.isArray(newTree) ? newTree : newTree ? [newTree] : [];
    },

    getSensorById(id: string): SensorReading | undefined {
        return data[id];
    },

    getSensorsByCategory(category: string): SensorReading[] {
        return availableSensors.filter((sensor: SensorReading) => sensor.category === category);
    },

    getSensorsBySource(sourceId: string): SensorReading[] {
        return availableSensors.filter((sensor: SensorReading) => sensor.source === sourceId);
    }
  };
}

export const sensorState = createSensorState(); 