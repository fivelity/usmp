/**
 * Enhanced Sensor Service with LibreHardwareMonitor integration
 * Provides real-time sensor data with configurable polling and advanced features
 */

import { sensors } from '$lib/stores/data/sensors.svelte';
import { connectionStatus } from '$lib/stores/connectionStatus';
import { get } from 'svelte/store';
import type {
  SensorReading,
  SensorSource,
  RealTimeConfig,
  WebSocketSensorMessage
} from '$lib/types/sensors';
import { websocketService } from './websocket';

class SensorService {
  private config: RealTimeConfig = {
    polling_rate: 2000,
    adaptive_polling: true,
    burst_mode: false,
    priority_sensors: [],
    background_polling: true,
    offline_caching: true,
    compression: true,
    batch_size: 50,
    connection_timeout: 5000,
    reconnect_interval: 3000,
    max_reconnect_attempts: 5,
    heartbeat_interval: 30000
  };

  private heartbeatInterval: ReturnType<typeof setInterval> | null = null;

  constructor() {
    this.initializeService();
  }

  async initializeService(): Promise<void> {
    try {
      console.log('[SensorService] Initializing sensor service...');
      await this.loadConfiguration();
      this.setupWebSocketHandlers();
      await this.discoverSensorSources();
      websocketService.connect();
      this.startHeartbeat();
      console.log('[SensorService] Sensor service initialized successfully');
    } catch (error) {
      console.error('[SensorService] Failed to initialize:', error);
      throw error;
    }
  }

  private async loadConfiguration(): Promise<void> {
    try {
      const savedConfig = localStorage.getItem('sensor-realtime-config');
      if (savedConfig) {
        this.config = { ...this.config, ...JSON.parse(savedConfig) };
        console.log('[SensorService] Configuration loaded from storage');
      }
    } catch (error) {
      console.warn('[SensorService] Failed to load configuration:', error);
    }
  }

  /**
   * Update real-time configuration
   */
  async updateConfiguration(newConfig: Partial<RealTimeConfig>): Promise<void> {
    this.config = { ...this.config, ...newConfig };

    // Restart polling with new configuration
    this.stopHeartbeat();
    this.startHeartbeat();

    // Save configuration
    await this.saveConfiguration();

    console.log('[SensorService] Configuration updated:', this.config);
  }

  private async saveConfiguration(): Promise<void> {
    try {
      localStorage.setItem(
        "sensor-realtime-config",
        JSON.stringify(this.config),
      );
    } catch (error) {
      console.warn("[SensorService] Failed to save configuration:", error);
    }
  }

  private setupWebSocketHandlers(): void {
    // Subscribe to all incoming messages
    websocketService.subscribe((message: WebSocketSensorMessage) => {
      this.handleWebSocketMessage(message);
    });

    // Subscribe to connection status changes
    websocketService.onConnectionChange((status) => {
      connectionStatus.set(status);
      switch (status) {
        case 'connected':
          console.log('[SensorService] WebSocket connection established');
          this.discoverSensorSources();
          break;
        case 'disconnected':
          console.log('[SensorService] WebSocket connection closed');
          break;
        case 'error':
          console.error('[SensorService] WebSocket connection error.');
          break;
      }
    });
  }

  private handleWebSocketMessage(message: WebSocketSensorMessage): void {
    try {
      switch (message.type) {
        case "sensor_data":
          this.processSensorDataMessage(message);
          break;
        case "sensor_update":
          this.processSensorUpdate(message);
          break;
        case "hardware_change":
          this.processHardwareChange(message);
          break;
        // connection_status is now handled by onConnectionChange
        case "error":
          this.processError(message);
          break;
        case "heartbeat":
          this.processHeartbeat(message);
          break;
        default:
          console.warn(`[SensorService] Unknown message type: ${message.type}`);
      }
    } catch (error) {
      console.error("[SensorService] Error processing WebSocket message:", error);
    }
  }

  private processSensorDataMessage(message: WebSocketSensorMessage): void {
    if (message.data?.sensors) {
      const sensorReadings: Record<string, SensorReading> = {};
      for (const [sensorId, sensorData] of Object.entries(message.data.sensors)) {
        sensorReadings[sensorId] = this.normalizeSensorReading(sensorData, message.source_id);
      }
      sensors.updateData(sensorReadings);
    }
  }

  private processHardwareChange(message: WebSocketSensorMessage): void {
    if (message.data?.hardware_tree) {
      sensors.updateTree(message.data.hardware_tree);
    }
    if (message.data?.sources) {
      sensors.updateSources(Object.values(message.data.sources));
    }
  }

  private processSensorUpdate(message: WebSocketSensorMessage): void {
    if (message.data?.sensor) {
      const reading = this.normalizeSensorReading(message.data.sensor, message.source_id);
      sensors.updateData({ [reading.id]: reading });
    }
  }

  private processError(message: WebSocketSensorMessage): void {
    if (message.error) {
      console.error(
        `[SensorService] Received error from source ${message.source_id}: ${message.error}`,
      );
      // TODO: Re-implement alerting mechanism if needed. The 'sensors' store no longer has an 'addAlert' method.
    }
  }

  private processHeartbeat(message: WebSocketSensorMessage): void {
    // console.log(`[SensorService] Heartbeat from ${message.source_id}`);
    if (message.data?.performance_metrics) {
      // TODO: Re-implement performance metrics updates.
      // The 'sensors' store no longer has an 'updatePerformanceMetrics' method.
      // Performance metrics are part of the SourceStatistics on a SensorSource.
      // This would require finding the right source and updating its statistics.
      console.log('[SensorService] Received performance metrics, but update logic is not implemented yet.');
    }
  }

  private normalizeSensorReading(data: any, sourceId: string): SensorReading {
    return {
      id: data.id || `${sourceId}_${data.name}`,
      name: data.name || "Unknown Sensor",
      value: typeof data.value === "number" ? data.value : 0,
      unit: data.unit || "",
      min_value: data.min_value,
      max_value: data.max_value,
      source: sourceId,
      category: data.category || "unknown",
      hardware_type: data.hardware_type || "unknown",
      parent_hardware: data.parent,
      timestamp: data.timestamp || new Date().toISOString(),
      status: data.status || "active",
      quality: this.assessDataQuality(data),
      metadata: data.metadata,
    };
  }

  private assessDataQuality(
    data: any,
  ): "excellent" | "good" | "fair" | "poor" | "unknown" {
    // Assess data quality based on various factors
    const now = Date.now();
    const dataTime = new Date(data.timestamp || now).getTime();
    const age = now - dataTime;

    if (age < 5000) return "excellent";
    if (age < 15000) return "good";
    if (age < 30000) return "fair";
    if (age < 60000) return "poor";
    return "unknown";
  }

  private async discoverSensorSources(): Promise<void> {
    try {
      const response = await fetch("/api/sensors/sources");
      if (!response.ok) {
        throw new Error(
          `Failed to discover sensor sources: ${response.statusText}`,
        );
      }

      const data = await response.json();

      if (data.sources) {
        const normalizedSources: Record<string, SensorSource> = {};

        for (const [sourceId, sourceData] of Object.entries(data.sources)) {
          normalizedSources[sourceId] = this.normalizeSensorSource(
            sourceId,
            sourceData,
          );
        }

        sensors.updateSources(Object.values(normalizedSources));
        console.log(
          "[SensorService] Discovered sensor sources:",
          Object.keys(normalizedSources),
        );
      }
    } catch (error) {
      console.error(
        "[SensorService] Failed to discover sensor sources:",
        error,
      );
      throw error;
    }
  }

  private normalizeSensorSource(id: string, data: any): SensorSource {
    return {
      id,
      name: data.name || id,
      description: data.description || "",
      version: data.version || "1.0.0",
      active: data.active || false,
      connection_status: data.active ? "connected" : "disconnected",
      hardware_components: data.hardware || [],
      capabilities: data.capabilities || {
        supports_real_time: true,
        supports_history: false,
        supports_alerts: false,
        supports_calibration: false,
        min_update_interval: 500,
        max_update_interval: 10000,
        supported_hardware_types: [],
        supported_sensor_categories: [],
      },
      configuration: data.configuration || {
        update_interval: this.config.polling_rate,
        enable_auto_discovery: true,
        enable_hardware_acceleration: true,
        enable_detailed_logging: false,
        timeout_duration: 5000,
        retry_attempts: 3,
        buffer_size: 100,
        compression_enabled: true,
        filter_inactive_sensors: true,
        hardware_filters: [],
        sensor_filters: [],
      },
      statistics: data.statistics || {
        total_sensors: 0,
        active_sensors: 0,
        update_count: 0,
        error_count: 0,
        average_update_time: 0,
        data_throughput: 0,
        uptime: 0,
        performance_metrics: {
          cpu_usage: 0,
          memory_usage: 0,
          network_usage: 0,
          update_latency: 0,
          queue_size: 0,
          dropped_updates: 0,
        },
      },
      last_update: data.last_update || new Date().toISOString(),
      error_message: data.error_message,
    };
  }

  private startHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }

    this.heartbeatInterval = setInterval(() => {
      // Svelte 5 runes don't need `get()`
      if (get(connectionStatus) === 'connected') {
        websocketService.send({
          type: 'heartbeat',
          source_id: 'client',
          timestamp: new Date().toISOString()
        });
      }
    }, this.config.heartbeat_interval);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  /**
   * Cleanup resources
   */
  destroy(): void {
    this.stopHeartbeat();
    console.log('[SensorService] Service destroyed');
  }
}

// Create singleton instance
export const sensorService = new SensorService();
