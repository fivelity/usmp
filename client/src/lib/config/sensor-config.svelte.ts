/**
 * Sensor system configuration management
 * Provides configurable defaults and settings for the sensor monitoring system
 */

import type { SensorSystemConfig, AlertThresholds } from '$lib/types/sensor-metadata';

/**
 * Default sensor system configuration
 */
export const DEFAULT_SENSOR_CONFIG: SensorSystemConfig = {
  maxHistoryPoints: 100,
  defaultUpdateInterval: 1000,
  defaultAlertThresholds: {
    warning: 80,
    critical: 95,
    type: 'above',
  },
  enableHistoryCleanup: true,
  performance: {
    maxProcessingTime: 100,
    enableLogging: false,
  },
};

/**
 * Sensor configuration store using Svelte 5 runes
 */
function createSensorConfigStore() {
  let config = $state<SensorSystemConfig>({ ...DEFAULT_SENSOR_CONFIG });

  return {
    /**
     * Get current configuration
     */
    get config() {
      return config;
    },

    /**
     * Update configuration with partial values
     * @param updates - Partial configuration updates
     */
    updateConfig(updates: Partial<SensorSystemConfig>) {
      config = { ...config, ...updates };
    },

    /**
     * Reset configuration to defaults
     */
    resetToDefaults() {
      config = { ...DEFAULT_SENSOR_CONFIG };
    },

    /**
     * Get maximum history points setting
     */
    getMaxHistoryPoints(): number {
      return config.maxHistoryPoints;
    },

    /**
     * Get default update interval setting
     */
    getDefaultUpdateInterval(): number {
      return config.defaultUpdateInterval;
    },

    /**
     * Get default alert thresholds
     */
    getDefaultAlertThresholds(): AlertThresholds {
      return { ...config.defaultAlertThresholds };
    },

    /**
     * Check if history cleanup is enabled
     */
    isHistoryCleanupEnabled(): boolean {
      return config.enableHistoryCleanup;
    },

    /**
     * Get performance monitoring settings
     */
    getPerformanceConfig() {
      return { ...config.performance };
    },
  };
}

export const sensorConfig = createSensorConfigStore();
