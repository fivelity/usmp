/**
 * WebSocket service for real-time sensor data communication
 */

import { get } from "svelte/store";
import { connectionStatus } from "../stores";
import { sensorUtils } from "../stores/sensorData.svelte";
import type { WebSocketSensorMessage, SensorReading } from "../types/sensors";

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private isIntentionalClose = false;
  private url: string | null = null;
  private messageHandlers: ((message: WebSocketSensorMessage) => void)[] = [];

  constructor() {
    // Don't auto-connect in constructor to avoid SSR issues
  }

  connect(url?: string): void {
    // Check if we're in a browser environment
    if (typeof window === "undefined") {
      console.warn("WebSocket service not available in SSR environment");
      return;
    }

    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      return;
    }

    let connectUrl: string;
    if (url) {
      connectUrl = url;
    } else {
      // Default URL pointing to backend server
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const host = window.location.host; // Use the current host, which is the Vite dev server
      const clientId = `client-${Math.random().toString(36).substring(7)}`;
      connectUrl = `${protocol}//${host}/ws/${clientId}`; // The /ws path will be proxied
    }

    this.url = connectUrl; // Store the url for reconnects

    connectionStatus.set("connecting");

    try {
      this.ws = new WebSocket(this.url);
      this.setupEventListeners();
    } catch (error) {
      console.error("Failed to create WebSocket connection:", error);
      connectionStatus.set("error");
      this.scheduleReconnect();
    }
  }

  private setupEventListeners(): void {
    if (!this.ws) return;

    this.ws.onopen = () => {
      console.log("WebSocket connected");
      connectionStatus.set("connected");
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketSensorMessage = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error("Failed to parse WebSocket message:", error);
      }
    };

    this.ws.onclose = (event) => {
      console.log("WebSocket closed:", event.code, event.reason);
      connectionStatus.set("disconnected");

      if (!this.isIntentionalClose) {
        this.scheduleReconnect();
      }
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      connectionStatus.set("error");
    };
  }

  private handleMessage(message: WebSocketSensorMessage): void {
    // Notify all registered handlers
    this.messageHandlers.forEach((handler) => handler(message));

    switch (message.type) {
      case "sensor_data":
        if (message.data) {
          // The actual sensor readings are nested inside message.data.sources
          const sensorReadings = (message.data as any).sources;
          if (sensorReadings) {
            // The data is a dictionary of sources, each with a 'sensors' object
            const flatData: Record<string, SensorReading> = {};
            for (const source of Object.values(sensorReadings as any)) {
              if ((source as any).sensors) {
                Object.assign(flatData, (source as any).sensors);
              }
            }
            sensorUtils.updateSensorData(flatData);
          }
        }
        break;

      case "sensor_update":
        console.log("[WebSocket] Received sensor_update message:", message);
        if (message.data) {
          sensorUtils.updateSensorData(
            message.data as Record<string, SensorReading>,
          );
        }
        break;

      case "hardware_change":
        console.log("[WebSocket] Received hardware_change message:", message);
        if (message.data) {
          sensorUtils.updateSensorSources(message.data);
        }
        break;

      case "connection_status":
        console.log("[WebSocket] Received connection_status message:", message);
        connectionStatus.set(message.data?.status || "disconnected");
        break;

      case "error":
        console.error("[WebSocket] Received error message:", message.error);
        break;

      case "heartbeat":
        // Handle heartbeat if needed
        break;

      default:
        console.log("Unknown message type:", message.type, message);
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("Max reconnection attempts reached");
      connectionStatus.set("error");
      return;
    }

    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
    this.reconnectAttempts++;

    console.log(
      `Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`,
    );

    setTimeout(() => {
      this.connect();
    }, delay);
  }

  send(message: WebSocketSensorMessage): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn("WebSocket is not connected");
    }
  }

  disconnect(): void {
    this.isIntentionalClose = true;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    connectionStatus.set("disconnected");
  }

  reconnect(): void {
    this.disconnect();
    this.isIntentionalClose = false;
    this.reconnectAttempts = 0;
    setTimeout(() => this.connect(), 100);
  }

  getConnectionState(): string {
    return get(connectionStatus);
  }

  // Method to subscribe to WebSocket messages
  subscribe(callback: (message: WebSocketSensorMessage) => void): () => void {
    this.messageHandlers.push(callback);
    return () => {
      this.messageHandlers = this.messageHandlers.filter((h) => h !== callback);
    };
  }

  // Method to handle connection status changes
  onConnectionChange(
    callback: (
      status: "connecting" | "connected" | "disconnected" | "error",
    ) => void,
  ): () => void {
    return connectionStatus.subscribe(callback);
  }
}

// Create singleton instance
export const websocketService = new WebSocketService();

// Auto-connect when the module is imported (only in browser)
if (typeof window !== "undefined") {
  // Connect when the page becomes visible
  document.addEventListener("visibilitychange", () => {
    if (
      !document.hidden &&
      websocketService.getConnectionState() === "disconnected"
    ) {
      websocketService.reconnect();
    }
  });

  // Connect when the page comes back online
  window.addEventListener("online", () => {
    if (websocketService.getConnectionState() !== "connected") {
      websocketService.reconnect();
    }
  });

  // Disconnect when going offline
  window.addEventListener("offline", () => {
    websocketService.disconnect();
  });
}
