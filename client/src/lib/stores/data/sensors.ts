import { writable, derived, get } from "svelte/store";
import type { SensorReading } from "$lib/types";

// Core sensor data store
export const sensorData = writable<Record<string, SensorReading>>({});

// Sensor metadata and configuration
export const sensorMetadata = writable<
  Record<
    string,
    {
      displayName?: string;
      customUnit?: string;
      customRange?: { min: number; max: number };
      alertThresholds?: { warning: number; critical: number };
      hidden?: boolean;
    }
  >
>({});

// Historical data for graphs and trends
export const sensorHistory = writable<
  Record<string, Array<{ timestamp: Date; value: number }>>
>({});

// Derived stores for organized access
export const sensorsByCategory = derived(sensorData, ($sensorData) => {
  const categories: Record<string, SensorReading[]> = {};

  Object.values($sensorData).forEach((sensor) => {
    if (!categories[sensor.category]) {
      categories[sensor.category] = [];
    }
    categories[sensor.category].push(sensor);
  });

  return categories;
});

export const sensorsBySource = derived(sensorData, ($sensorData) => {
  const sources: Record<string, SensorReading[]> = {};

  Object.values($sensorData).forEach((sensor) => {
    if (!sources[sensor.source]) {
      sources[sensor.source] = [];
    }
    sources[sensor.source].push(sensor);
  });

  return sources;
});

export const activeSensors = derived(sensorData, ($sensorData) => {
  return Object.values($sensorData).filter(
    (sensor) => sensor.value !== null && sensor.value !== undefined,
  );
});

// Derived store for filtered sensor data
export const filteredSensorData = derived(sensorData, ($sensorData) => {
  // Filter logic can be implemented here
  return $sensorData;
});

// Utility functions for sensor management
export const sensorUtils = {
  // Update sensor data
  updateSensorData: (newData: Record<string, SensorReading>) => {
    const currentTime = new Date();

    // Update main sensor data
    sensorData.set(newData);

    // Update historical data
    sensorHistory.update((history) => {
      const updatedHistory = { ...history };

      Object.entries(newData).forEach(([sensorId, sensor]) => {
        if (!updatedHistory[sensorId]) {
          updatedHistory[sensorId] = [];
        }

        // Add new data point
        updatedHistory[sensorId].push({
          timestamp: currentTime,
          value: sensor.value,
        });

        // Keep only last 100 data points for performance
        if (updatedHistory[sensorId].length > 100) {
          updatedHistory[sensorId] = updatedHistory[sensorId].slice(-100);
        }
      });

      return updatedHistory;
    });
  },

  // Get sensor by ID
  getSensorById: (id: string): SensorReading | null => {
    const data = get(sensorData);
    return data[id] || null;
  },

  // Get sensors by category
  getSensorsByCategory: (category: string): SensorReading[] => {
    const categories = get(sensorsByCategory);
    return categories[category] || [];
  },

  // Get sensor history
  getSensorHistory: (
    sensorId: string,
    maxPoints?: number,
  ): Array<{ timestamp: Date; value: number }> => {
    const history = get(sensorHistory);
    const sensorHistoryData = history[sensorId] || [];

    if (maxPoints && sensorHistoryData.length > maxPoints) {
      return sensorHistoryData.slice(-maxPoints);
    }

    return sensorHistoryData;
  },

  // Update sensor metadata
  updateSensorMetadata: (sensorId: string, metadata: any) => {
    sensorMetadata.update((current) => ({
      ...current,
      [sensorId]: {
        ...current[sensorId],
        ...metadata,
      },
    }));
  },

  // Get effective sensor display name
  getSensorDisplayName: (sensorId: string): string => {
    const sensor = sensorUtils.getSensorById(sensorId);
    const metadata = get(sensorMetadata)[sensorId];

    return metadata?.displayName || sensor?.name || sensorId;
  },

  // Get effective sensor unit
  getSensorUnit: (sensorId: string): string => {
    const sensor = sensorUtils.getSensorById(sensorId);
    const metadata = get(sensorMetadata)[sensorId];

    return metadata?.customUnit || sensor?.unit || "";
  },

  // Get effective sensor range
  getSensorRange: (sensorId: string): { min: number; max: number } | null => {
    const sensor = sensorUtils.getSensorById(sensorId);
    const metadata = get(sensorMetadata)[sensorId];

    if (metadata?.customRange) {
      return metadata.customRange;
    }

    if (sensor?.min_value !== null && sensor?.max_value !== null) {
      return { min: sensor.min_value, max: sensor.max_value };
    }

    return null;
  },

  // Check if sensor has alerts
  checkSensorAlerts: (
    sensorId: string,
  ): { level: "normal" | "warning" | "critical"; message?: string } => {
    const sensor = sensorUtils.getSensorById(sensorId);
    const metadata = get(sensorMetadata)[sensorId];

    if (!sensor || !metadata?.alertThresholds) {
      return { level: "normal" };
    }

    const { warning, critical } = metadata.alertThresholds;

    if (sensor.value >= critical) {
      return {
        level: "critical",
        message: `Critical: ${sensor.value}${sensor.unit} >= ${critical}${sensor.unit}`,
      };
    }

    if (sensor.value >= warning) {
      return {
        level: "warning",
        message: `Warning: ${sensor.value}${sensor.unit} >= ${warning}${sensor.unit}`,
      };
    }

    return { level: "normal" };
  },

  // Clear all sensor data
  clearSensorData: () => {
    sensorData.set({});
    sensorHistory.set({});
  },

  // Export sensor configuration
  exportSensorConfig: () => {
    return {
      metadata: get(sensorMetadata),
      timestamp: new Date().toISOString(),
    };
  },

  // Import sensor configuration
  importSensorConfig: (config: any) => {
    if (config.metadata) {
      sensorMetadata.set(config.metadata);
    }
  },
};

// Helper functions for sensor data management
export const sensorDataUtils = {
  updateSensor(id: string, data: SensorReading) {
    sensorData.update((sensors) => {
      return { ...sensors, [id]: data };
    });
  },

  updateMultipleSensors(updates: Record<string, SensorReading>) {
    sensorData.update((sensors) => {
      return { ...sensors, ...updates };
    });
  },

  removeSensor(id: string) {
    sensorData.update((sensors) => {
      const newSensors = { ...sensors };
      delete newSensors[id];
      return newSensors;
    });
  },

  clearAllSensors() {
    sensorData.set({});
  },
};
