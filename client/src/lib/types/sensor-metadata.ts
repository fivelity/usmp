/**
 * TypeScript interfaces for sensor metadata and configuration
 * Replaces usage of 'any' types throughout the sensor system
 */

/**
 * Sensor metadata configuration interface
 */
export interface SensorMetadata {
  /** Custom display name for the sensor */
  displayName?: string;
  /** Custom unit override for the sensor */
  customUnit?: string;
  /** Custom value range override */
  customRange?: SensorRange;
  /** Alert threshold configuration */
  alertThresholds?: AlertThresholds;
  /** Whether sensor is hidden from UI */
  hidden?: boolean;
  /** Additional custom properties */
  customProperties?: Record<string, string | number | boolean>;
}

/**
 * Sensor value range interface
 */
export interface SensorRange {
  /** Minimum expected value */
  min: number;
  /** Maximum expected value */
  max: number;
}

/**
 * Alert threshold configuration
 */
export interface AlertThresholds {
  /** Warning threshold value */
  warning: number;
  /** Critical threshold value */
  critical: number;
  /** Threshold type (above/below) */
  type?: 'above' | 'below';
}

/**
 * Alert status result
 */
export interface AlertStatus {
  /** Current alert level */
  level: 'normal' | 'warning' | 'critical';
  /** Optional alert message */
  message?: string;
  /** Threshold that was triggered */
  triggeredThreshold?: number;
}

/**
 * Sensor history data point
 */
export interface SensorHistoryPoint {
  /** Timestamp of the reading */
  timestamp: Date;
  /** Sensor value at this time */
  value: number;
}

/**
 * Sensor configuration export/import format
 */
export interface SensorConfigExport {
  /** Sensor metadata by sensor ID */
  metadata: Record<string, SensorMetadata>;
  /** Export timestamp */
  timestamp: string;
  /** Format version for compatibility */
  version: string;
}

/**
 * API payload for sensor source updates
 */
export interface SensorSourceApiPayload {
  /** Source identifier */
  source_id: string;
  /** Source display name */
  name: string;
  /** Whether source is currently active */
  is_active: boolean;
  /** Update interval in milliseconds */
  update_interval: number;
  /** Additional source properties */
  properties?: Record<string, unknown>;
}

/**
 * Configuration options for sensor system
 */
export interface SensorSystemConfig {
  /** Maximum number of history points to keep per sensor */
  maxHistoryPoints: number;
  /** Default update interval for sensors (ms) */
  defaultUpdateInterval: number;
  /** Default alert thresholds */
  defaultAlertThresholds: AlertThresholds;
  /** Whether to enable automatic cleanup of old data */
  enableHistoryCleanup: boolean;
  /** Performance monitoring settings */
  performance: {
    /** Maximum processing time warning threshold (ms) */
    maxProcessingTime: number;
    /** Enable performance logging */
    enableLogging: boolean;
  };
}
