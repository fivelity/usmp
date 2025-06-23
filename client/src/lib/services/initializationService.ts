/**
 * Service to handle application initialization with proper error handling
 */

import { configService } from "./configService";
import { apiService } from "./api";
import { websocketService } from "./websocket";
import { sensorStore as sensorUtils } from "$lib/stores/data/sensors.svelte";
import { addWidget } from "$lib/stores/data/widgets.svelte";
import { demoWidgets } from "$lib/demoData";
import type { WidgetConfig } from "$lib/types";

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
      // Connect to WebSocket for real-time updates (non-blocking)
      websocketService.connect();

      // Load available sensors
      const sensorsResponse = await apiService.getSensors();
      console.log("[DEBUG] Full sensor status response:", sensorsResponse);
      if (
        sensorsResponse.success &&
        sensorsResponse.data &&
        Array.isArray(sensorsResponse.data)
      ) {
        sensorUtils.updateSensorSources(sensorsResponse.data);
      } else {
        errors.push("Failed to load available sensors");
      }

      // Load hardware tree
      const hardwareResponse = await apiService.getHardwareTree();
      if (
        hardwareResponse.success &&
        hardwareResponse.data &&
        Array.isArray(hardwareResponse.data)
      ) {
        sensorUtils.updateHardwareTree(hardwareResponse.data);
      } else {
        warnings.push("Hardware tree not available");
      }

      // Load initial sensor data (optional, may not be available)
      try {
        const dataResponse = await apiService.getCurrentSensorData();
        if (
          dataResponse.success &&
          dataResponse.data &&
          Object.keys(dataResponse.data).length > 0
        ) {
          // Convert the nested structure from the API to a flat map of sensor readings
          const flatSensorData: Record<string, any> = {};
          Object.values(dataResponse.data).forEach((readings: any[]) => {
            if (Array.isArray(readings)) {
              readings.forEach((reading) => {
                if (reading && reading.sensor_id) {
                  flatSensorData[reading.sensor_id] = reading;
                }
              });
            }
          });
          sensorUtils.updateSensorData(flatSensorData);
        } else {
          warnings.push("No initial sensor data available");
        }
      } catch (error) {
        warnings.push("Initial sensor data endpoint not available");
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
          addWidget(widgetConfig);
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
