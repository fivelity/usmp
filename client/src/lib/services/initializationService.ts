/**
 * Service to handle application initialization with proper error handling
 */

import { configService } from "./configService";
import { apiService } from "./api";
import { websocketService } from "./websocket";
import { sensorUtils } from "$lib/stores/sensorData";
import { addWidget } from "$lib/stores/data/widgets";
import { demoWidgets } from "$lib/demoData";
import type { Widget } from "$lib/types";

export interface InitializationResult {
  success: boolean;
  mode: "demo" | "live" | "offline";
  errors: string[];
  warnings: string[];
}

class InitializationService {
  async initialize(): Promise<InitializationResult> {
    const result: InitializationResult = {
      success: false,
      mode: "offline",
      errors: [],
      warnings: [],
    };

    try {
      // Load configuration
      const config = await configService.loadConfig();
      console.log("Configuration loaded:", config);

      // Test backend connection
      const backendAvailable = await this.testBackendConnection();

      if (backendAvailable) {
        // Try to initialize live mode
        const liveResult = await this.initializeLiveMode();
        if (liveResult.success) {
          result.success = true;
          result.mode = "live";
          result.warnings = liveResult.warnings;
        } else {
          result.errors.push(...liveResult.errors);
          // Fall back to demo mode if configured
          if (config.data.useDemoData) {
            const demoResult = await this.initializeDemoMode();
            result.success = demoResult.success;
            result.mode = "demo";
            result.warnings.push("Backend unavailable, using demo data");
            result.errors.push(...demoResult.errors);
          }
        }
      } else {
        // Backend not available
        if (config.data.useDemoData) {
          const demoResult = await this.initializeDemoMode();
          result.success = demoResult.success;
          result.mode = "demo";
          result.warnings.push("Backend not available, using demo data");
          result.errors.push(...demoResult.errors);
        } else {
          result.errors.push("Backend not available and demo mode disabled");
        }
      }
    } catch (error) {
      result.errors.push(`Initialization failed: ${error}`);
    }

    return result;
  }

  private async testBackendConnection(): Promise<boolean> {
    try {
      return await apiService.testConnection();
    } catch (error) {
      console.warn("Backend connection test failed:", error);
      return false;
    }
  }

  private async initializeLiveMode(): Promise<{
    success: boolean;
    errors: string[];
    warnings: string[];
  }> {
    const errors: string[] = [];
    const warnings: string[] = [];

    try {
      // Connect to WebSocket for real-time updates
      await websocketService.connect();

      // Load available sensors
      const sensorsResponse = await apiService.getSensors();
      if (
        sensorsResponse.success &&
        sensorsResponse.data &&
        sensorsResponse.data.sources
      ) {
        const transformedSources: Record<
          string,
          import("$lib/types").SensorSourceFromAPI
        > = {};
        for (const sourceId in sensorsResponse.data.sources) {
          const source = sensorsResponse.data.sources[sourceId];
          if (source) {
            // Check if source is defined
            const sensorsRecord: Record<
              string,
              import("$lib/types").SensorData
            > = {};
            if (Array.isArray(source.sensors)) {
              source.sensors.forEach((sensor) => {
                sensorsRecord[sensor.id] = sensor;
              });
            }
            transformedSources[sourceId] = {
              id: source.id,
              name: source.name,
              active: source.active,
              last_update: source.last_update,
              sensors: sensorsRecord,
              // Optional properties
              ...(source.error_message && {
                error_message: source.error_message,
              }),
              ...(source.metadata && { metadata: source.metadata }),
            };
          }
        }
        sensorUtils.updateSensorSources(transformedSources);
      } else {
        errors.push("Failed to load available sensors");
      }

      // Load hardware tree
      const hardwareResponse = await apiService.getHardwareTree();
      if (
        hardwareResponse.success &&
        hardwareResponse.data &&
        hardwareResponse.data.hardware
      ) {
        sensorUtils.updateHardwareTree(hardwareResponse.data.hardware);
      } else {
        warnings.push("Hardware tree not available");
      }

      // Load initial sensor data
      const dataResponse = await apiService.getCurrentSensorData();
      if (
        dataResponse.success &&
        dataResponse.data &&
        dataResponse.data.data &&
        dataResponse.data.data.sources
      ) {
        // Convert nested source data to flat sensor data
        const flatSensorData: Record<string, any> = {};
        Object.entries(dataResponse.data.data.sources).forEach(
          ([_sourceId, sourceData]: [string, any]) => {
            if (sourceData.active && sourceData.sensors) {
              Object.assign(flatSensorData, sourceData.sensors);
            }
          },
        );
        sensorUtils.updateSensorData(flatSensorData);
      } else {
        warnings.push("No initial sensor data available");
      }

      return { success: errors.length === 0, errors, warnings };
    } catch (error) {
      errors.push(`Live mode initialization failed: ${error}`);
      return { success: false, errors, warnings };
    }
  }

  private async initializeDemoMode(): Promise<{
    success: boolean;
    errors: string[];
  }> {
    const errors: string[] = [];

    try {
      // Use imported demo widgets
      if (Array.isArray(demoWidgets)) {
        demoWidgets.forEach((widgetConfig) => {
          addWidget(widgetConfig as Widget);
        });
      }

      // Set demo sensor data (this would normally come from the demo data file)
      const demoSensorData = this.generateDemoSensorData();
      sensorUtils.updateSensorData(demoSensorData);

      return { success: true, errors };
    } catch (error) {
      errors.push(`Demo mode initialization failed: ${error}`);
      return { success: false, errors };
    }
  }

  private generateDemoSensorData(): Record<string, any> {
    // Generate some demo sensor data
    return {
      cpu_temp: {
        id: "cpu_temp",
        name: "CPU Temperature",
        value: 65,
        unit: "°C",
        category: "temperature",
        source: "demo",
        min_value: 30,
        max_value: 90,
        parent: "CPU",
        timestamp: new Date(),
      },
      gpu_temp: {
        id: "gpu_temp",
        name: "GPU Temperature",
        value: 72,
        unit: "°C",
        category: "temperature",
        source: "demo",
        min_value: 30,
        max_value: 95,
        parent: "GPU",
        timestamp: new Date(),
      },
      cpu_load: {
        id: "cpu_load",
        name: "CPU Load",
        value: 45,
        unit: "%",
        category: "load",
        source: "demo",
        min_value: 0,
        max_value: 100,
        parent: "CPU",
        timestamp: new Date(),
      },
      memory_usage: {
        id: "memory_usage",
        name: "Memory Usage",
        value: 68,
        unit: "%",
        category: "load",
        source: "demo",
        min_value: 0,
        max_value: 100,
        parent: "Memory",
        timestamp: new Date(),
      },
    };
  }
}

export const initializationService = new InitializationService();
