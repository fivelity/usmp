/**
 * Enhanced Sensor Service with LibreHardwareMonitor integration
 * Provides real-time sensor data with configurable polling and advanced features
 */

import { get, writable, derived } from "svelte/store";
import type {
  SensorReading,
  SensorSource,
  RealTimeConfig,
  SensorDataBatch,
  WebSocketSensorMessage,
  SourceConfiguration,
  SensorAlert,
  PerformanceMetrics,
} from "$lib/types/sensors";
import { websocketService } from "./websocket";
import { configService } from "./configService";
import { storage } from "$lib/utils/storage";

class SensorService {
  private sources = writable<Record<string, SensorSource>>({});
  private currentData = writable<Record<string, SensorReading>>({});
  private alerts = writable<SensorAlert[]>([]);
  private isConnected = writable(false);
  private connectionStatus = writable<string>("disconnected");
  private performanceMetrics = writable<PerformanceMetrics>({
    cpu_usage: 0,
    memory_usage: 0,
    network_usage: 0,
    update_latency: 0,
    queue_size: 0,
    dropped_updates: 0,
  });

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
    heartbeat_interval: 30000,
  };

  private pollingInterval: number | null = null;
  private heartbeatInterval: number | null = null;
  private reconnectAttempts = 0;
  private lastUpdateTime = 0;
  private updateQueue: SensorDataBatch[] = [];
  private isProcessingQueue = false;

  constructor() {
    this.initializeService();
  }

  // ============================================================================
  // PUBLIC API
  // ============================================================================

  /**
   * Initialize the sensor service
   */
  async initializeService(): Promise<void> {
    try {
      console.log("[SensorService] Initializing sensor service...");

      // Load configuration
      await this.loadConfiguration();

      // Initialize WebSocket connection
      this.setupWebSocketHandlers();

      // Start discovery process
      await this.discoverSensorSources();

      // Start real-time polling
      this.startRealTimePolling();

      // Start heartbeat
      this.startHeartbeat();

      console.log("[SensorService] Sensor service initialized successfully");
    } catch (error) {
      console.error("[SensorService] Failed to initialize:", error);
      throw error;
    }
  }

  /**
   * Get all available sensor sources
   */
  getSources() {
    return derived(this.sources, ($sources) => Object.values($sources));
  }

  /**
   * Get current sensor data
   */
  getCurrentData() {
    return derived(this.currentData, ($data) => $data);
  }

  /**
   * Get sensor alerts
   */
  getAlerts() {
    return derived(this.alerts, ($alerts) => $alerts);
  }

  /**
   * Get connection status
   */
  getConnectionStatus() {
    return derived(
      [this.isConnected, this.connectionStatus],
      ([$connected, $status]) => ({
        connected: $connected,
        status: $status,
      }),
    );
  }

  /**
   * Get performance metrics
   */
  getPerformanceMetrics() {
    return derived(this.performanceMetrics, ($metrics) => $metrics);
  }

  /**
   * Update real-time configuration
   */
  async updateConfiguration(newConfig: Partial<RealTimeConfig>): Promise<void> {
    this.config = { ...this.config, ...newConfig };

    // Restart polling with new configuration
    this.stopRealTimePolling();
    this.startRealTimePolling();

    // Save configuration
    await this.saveConfiguration();

    console.log("[SensorService] Configuration updated:", this.config);
  }

  /**
   * Get current configuration
   */
  getConfiguration(): RealTimeConfig {
    return { ...this.config };
  }

  /**
   * Manually refresh sensor data
   */
  async refreshSensorData(): Promise<void> {
    try {
      console.log("[SensorService] Manual refresh requested");
      await this.fetchSensorData();
    } catch (error) {
      console.error("[SensorService] Manual refresh failed:", error);
      throw error;
    }
  }

  /**
   * Configure specific sensor source
   */
  async configureSensorSource(
    sourceId: string,
    config: Partial<SourceConfiguration>,
  ): Promise<void> {
    try {
      const response = await fetch(
        `/api/sensors/sources/${sourceId}/configure`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(config),
        },
      );

      if (!response.ok) {
        throw new Error(
          `Failed to configure sensor source: ${response.statusText}`,
        );
      }

      console.log(`[SensorService] Configured sensor source ${sourceId}`);
      await this.discoverSensorSources(); // Refresh sources
    } catch (error) {
      console.error(
        `[SensorService] Failed to configure source ${sourceId}:`,
        error,
      );
      throw error;
    }
  }

  /**
   * Enable/disable specific sensor source
   */
  async toggleSensorSource(sourceId: string, enabled: boolean): Promise<void> {
    try {
      const response = await fetch(`/api/sensors/sources/${sourceId}/toggle`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled }),
      });

      if (!response.ok) {
        throw new Error(
          `Failed to toggle sensor source: ${response.statusText}`,
        );
      }

      console.log(
        `[SensorService] ${enabled ? "Enabled" : "Disabled"} sensor source ${sourceId}`,
      );
      await this.discoverSensorSources(); // Refresh sources
    } catch (error) {
      console.error(
        `[SensorService] Failed to toggle source ${sourceId}:`,
        error,
      );
      throw error;
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private async loadConfiguration(): Promise<void> {
    try {
      const appConfig = await configService.loadConfig();

      // Merge with sensor-specific configuration
      this.config = {
        ...this.config,
        polling_rate: appConfig.sensors.updateInterval,
        connection_timeout: appConfig.sensors.connectionTimeout,
        max_reconnect_attempts: appConfig.sensors.maxRetryAttempts,
      };

      // Create a writable store for real-time configuration
      const realtimeConfig = writable<RealTimeConfig>({
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
        heartbeat_interval: 30000,
      });

      // Load saved config from localStorage
      const savedConfig = storage.getJSON<RealTimeConfig>(
        "sensor-realtime-config",
        {
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
          heartbeat_interval: 30000,
        },
      );

      // Initialize the store with saved config
      realtimeConfig.set(savedConfig);

      // Save config to localStorage when it changes
      realtimeConfig.subscribe((config) => {
        storage.setJSON("sensor-realtime-config", config);
      });
    } catch (error) {
      console.warn(
        "[SensorService] Failed to load configuration, using defaults:",
        error,
      );
    }
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
    websocketService.subscribe((message: WebSocketSensorMessage) => {
      this.handleWebSocketMessage(message);
    });

    websocketService.onConnectionChange((status) => {
      this.connectionStatus.set(status);
      this.isConnected.set(status === "connected");

      if (status === "connected") {
        this.reconnectAttempts = 0;
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
        case "connection_status":
          this.processConnectionStatus(message);
          break;
        case "error":
          this.processError(message);
          break;
        case "heartbeat":
          this.processHeartbeat(message);
          break;
        default:
          console.warn("[SensorService] Unknown message type:", message.type);
      }
    } catch (error) {
      console.error(
        "[SensorService] Error processing WebSocket message:",
        error,
      );
    }
  }

  private processSensorDataMessage(message: WebSocketSensorMessage): void {
    if (message.data && message.data.sources) {
      const batch: SensorDataBatch = {
        batch_id: `batch_${Date.now()}`,
        source_id: message.source_id || "unknown",
        timestamp: message.timestamp,
        sensors: {},
        sequence_number: message.sequence_number || 0,
      };

      // Process sensor data from all sources
      for (const [sourceId, sourceData] of Object.entries(
        message.data.sources,
      )) {
        if (sourceData.active && sourceData.sensors) {
          for (const [sensorId, sensorData] of Object.entries(
            sourceData.sensors,
          )) {
            batch.sensors[sensorId] = this.normalizeSensorReading(
              sensorData,
              sourceId,
            );
          }
        }
      }

      this.queueSensorUpdate(batch);
    }
  }

  private processSensorUpdate(message: WebSocketSensorMessage): void {
    // Handle individual sensor updates
    if (message.data && message.data.sensor_id) {
      const reading = this.normalizeSensorReading(
        message.data,
        message.source_id,
      );
      this.updateSensorReading(reading);
    }
  }

  private processHardwareChange(message: WebSocketSensorMessage): void {
    // Handle hardware component changes
    console.log("[SensorService] Hardware change detected:", message.data);
    this.discoverSensorSources(); // Refresh hardware discovery
  }

  private processConnectionStatus(message: WebSocketSensorMessage): void {
    if (message.data && message.data.status) {
      this.connectionStatus.set(message.data.status);
    }
  }

  private processError(message: WebSocketSensorMessage): void {
    console.error("[SensorService] Server error:", message.error);

    // Create alert for the error
    const alert: SensorAlert = {
      id: `error_${Date.now()}`,
      sensor_id: "",
      type: "sensor_offline",
      threshold: 0,
      current_value: 0,
      message: message.error || "Unknown sensor error",
      severity: "error",
      timestamp: message.timestamp,
      acknowledged: false,
      auto_resolve: true,
    };

    this.addAlert(alert);
  }

  private processHeartbeat(message: WebSocketSensorMessage): void {
    // Update performance metrics from heartbeat
    if (message.data && message.data.metrics) {
      this.performanceMetrics.set(message.data.metrics);
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

  private queueSensorUpdate(batch: SensorDataBatch): void {
    this.updateQueue.push(batch);

    if (!this.isProcessingQueue) {
      this.processUpdateQueue();
    }
  }

  private async processUpdateQueue(): Promise<void> {
    if (this.isProcessingQueue || this.updateQueue.length === 0) {
      return;
    }

    this.isProcessingQueue = true;

    try {
      while (this.updateQueue.length > 0) {
        const batch = this.updateQueue.shift()!;
        await this.processSensorBatch(batch);
      }
    } catch (error) {
      console.error("[SensorService] Error processing update queue:", error);
    } finally {
      this.isProcessingQueue = false;
    }
  }

  private async processSensorBatch(batch: SensorDataBatch): Promise<void> {
    // Update current data store
    this.currentData.update((current) => ({
      ...current,
      ...batch.sensors,
    }));

    // Check for alerts
    this.checkSensorAlerts(batch.sensors);

    // Update performance metrics
    this.updatePerformanceMetrics(batch);

    this.lastUpdateTime = Date.now();
  }

  private updateSensorReading(reading: SensorReading): void {
    this.currentData.update((current) => ({
      ...current,
      [reading.id]: reading,
    }));
  }

  private checkSensorAlerts(_sensors: Record<string, SensorReading>): void {
    // Implementation for checking sensor thresholds and generating alerts
    // This would be expanded based on user-defined alert rules
  }

  private addAlert(alert: SensorAlert): void {
    this.alerts.update((current) => [alert, ...current].slice(0, 100)); // Keep last 100 alerts
  }

  private updatePerformanceMetrics(batch: SensorDataBatch): void {
    const processingTime = Date.now() - new Date(batch.timestamp).getTime();

    this.performanceMetrics.update((current) => ({
      ...current,
      update_latency: processingTime,
      queue_size: this.updateQueue.length,
    }));
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

        this.sources.set(normalizedSources);
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

  private async fetchSensorData(): Promise<void> {
    try {
      const response = await fetch("/api/sensors/current");
      if (!response.ok) {
        throw new Error(`Failed to fetch sensor data: ${response.statusText}`);
      }

      const data = await response.json();

      if (data.sources) {
        const allSensors: Record<string, SensorReading> = {};

        for (const [sourceId, sourceData] of Object.entries(data.sources)) {
          if (sourceData.active && sourceData.sensors) {
            for (const [sensorId, sensorData] of Object.entries(
              sourceData.sensors,
            )) {
              allSensors[sensorId] = this.normalizeSensorReading(
                sensorData,
                sourceId,
              );
            }
          }
        }

        this.currentData.set(allSensors);
      }
    } catch (error) {
      console.error("[SensorService] Failed to fetch sensor data:", error);
      throw error;
    }
  }

  private startRealTimePolling(): void {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }

    if (this.config.polling_rate > 0) {
      this.pollingInterval = setInterval(() => {
        this.fetchSensorData().catch((error) => {
          console.error("[SensorService] Polling error:", error);
        });
      }, this.config.polling_rate);

      console.log(
        `[SensorService] Started real-time polling at ${this.config.polling_rate}ms intervals`,
      );
    }
  }

  private stopRealTimePolling(): void {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = null;
      console.log("[SensorService] Stopped real-time polling");
    }
  }

  private startHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }

    this.heartbeatInterval = setInterval(() => {
      if (get(this.isConnected)) {
        websocketService.send({
          type: "heartbeat",
          timestamp: new Date().toISOString(),
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
    this.stopRealTimePolling();
    this.stopHeartbeat();
    console.log("[SensorService] Service destroyed");
  }
}

// Create singleton instance
export const sensorService = new SensorService();

// Export stores for components to use
export const sensorSources = sensorService.getSources();
export const currentSensorData = sensorService.getCurrentData();
export const sensorAlerts = sensorService.getAlerts();
export const sensorConnectionStatus = sensorService.getConnectionStatus();
export const sensorPerformanceMetrics = sensorService.getPerformanceMetrics();
