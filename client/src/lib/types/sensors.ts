/**
 * Enhanced sensor data types with real-time capabilities
 */

export interface SensorReading {
  id: string;
  name: string;
  value: number;
  unit: string;
  min_value?: number;
  max_value?: number;
  source: string;
  category: SensorCategory;
  hardware_type: HardwareType;
  parent_hardware?: string;
  timestamp: string;
  status: SensorStatus;
  quality: DataQuality;
  metadata?: SensorMetadata;
}

export type SensorCategory =
  | "temperature"
  | "voltage"
  | "clock"
  | "load"
  | "fan"
  | "flow"
  | "control"
  | "level"
  | "factor"
  | "power"
  | "data"
  | "throughput"
  | "energy"
  | "noise"
  | "unknown";

export type HardwareType =
  | "cpu"
  | "gpu"
  | "memory"
  | "motherboard"
  | "storage"
  | "network"
  | "controller"
  | "battery"
  | "unknown";

export type SensorStatus = "active" | "inactive" | "error" | "stale";

export type DataQuality = "excellent" | "good" | "fair" | "poor" | "unknown";

export interface SensorMetadata {
  hardware_name: string;
  sensor_type: string;
  identifier: string;
  description?: string;
  location?: string;
  vendor?: string;
  driver_version?: string;
  last_calibration?: string;
  accuracy?: number;
  resolution?: number;
  update_rate?: number;
}

export interface HardwareComponent {
  id: string;
  name: string;
  type: HardwareType;
  vendor?: string;
  model?: string;
  driver_version?: string;
  sensors: SensorReading[];
  sub_hardware: HardwareComponent[];
  status: "online" | "offline" | "error";
  last_update: string;
  metadata?: Record<string, any>;
}

export interface SensorSource {
  id: string;
  name: string;
  description: string;
  version: string;
  active: boolean;
  connection_status: ConnectionStatus;
  hardware_components: HardwareComponent[];
  capabilities: SourceCapabilities;
  configuration: SourceConfiguration;
  statistics: SourceStatistics;
  last_update: string;
  error_message?: string;
}

export type ConnectionStatus =
  | "connected"
  | "disconnected"
  | "connecting"
  | "error"
  | "initializing";

export interface SourceCapabilities {
  supports_real_time: boolean;
  supports_history: boolean;
  supports_alerts: boolean;
  supports_calibration: boolean;
  min_update_interval: number;
  max_update_interval: number;
  supported_hardware_types: HardwareType[];
  supported_sensor_categories: SensorCategory[];
}

export interface SourceConfiguration {
  update_interval: number;
  enable_auto_discovery: boolean;
  enable_hardware_acceleration: boolean;
  enable_detailed_logging: boolean;
  timeout_duration: number;
  retry_attempts: number;
  buffer_size: number;
  compression_enabled: boolean;
  filter_inactive_sensors: boolean;
  hardware_filters: HardwareType[];
  sensor_filters: SensorCategory[];
}

export interface SourceStatistics {
  total_sensors: number;
  active_sensors: number;
  update_count: number;
  error_count: number;
  average_update_time: number;
  data_throughput: number;
  uptime: number;
  last_error?: string;
  performance_metrics: PerformanceMetrics;
}

export interface PerformanceMetrics {
  cpu_usage: number;
  memory_usage: number;
  network_usage: number;
  update_latency: number;
  queue_size: number;
  dropped_updates: number;
}

export interface SensorAlert {
  id: string;
  sensor_id: string;
  type: AlertType;
  threshold: number;
  current_value: number;
  message: string;
  severity: AlertSeverity;
  timestamp: string;
  acknowledged: boolean;
  auto_resolve: boolean;
}

export type AlertType =
  | "threshold_high"
  | "threshold_low"
  | "rate_change"
  | "sensor_offline"
  | "data_quality";
export type AlertSeverity = "info" | "warning" | "error" | "critical";

export interface SensorHistory {
  sensor_id: string;
  readings: HistoryPoint[];
  aggregation_level: AggregationLevel;
  retention_period: number;
}

export interface HistoryPoint {
  timestamp: string;
  value: number;
  quality: DataQuality;
  metadata?: Record<string, any>;
}

export type AggregationLevel =
  | "raw"
  | "minute"
  | "hour"
  | "day"
  | "week"
  | "month";

export interface SensorCalibration {
  sensor_id: string;
  offset: number;
  scale: number;
  polynomial_coefficients?: number[];
  last_calibrated: string;
  calibrated_by: string;
  notes?: string;
}

export interface RealTimeConfig {
  polling_rate: number;
  adaptive_polling: boolean;
  burst_mode: boolean;
  priority_sensors: string[];
  background_polling: boolean;
  offline_caching: boolean;
  compression: boolean;
  batch_size: number;
  connection_timeout: number;
  reconnect_interval: number;
  max_reconnect_attempts: number;
  heartbeat_interval: number;
}

export interface WebSocketSensorMessage {
  type:
    | "sensor_data"
    | "sensor_update"
    | "hardware_change"
    | "connection_status"
    | "error"
    | "heartbeat";
  timestamp: string;
  source_id: string;
  data?: any;
  error?: string;
  sequence_number?: number;
  compression?: string;
}

export interface SensorDataBatch {
  batch_id: string;
  source_id: string;
  timestamp: string;
  sensors: Record<string, SensorReading>;
  hardware_changes?: HardwareComponent[];
  statistics?: Partial<SourceStatistics>;
  sequence_number: number;
}
