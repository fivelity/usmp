/**
 * Production-grade WebSocket client with automatic reconnection.
 * Robust WebSocket management with connection pooling and message queuing.
 */

import { writable, type Writable } from "svelte/store";
import { env, log, warn, error } from "$lib/config/environment";

export interface WebSocketMessage {
  type: string;
  timestamp: string;
  data?: any;
  content?: any;
  message?: string;
  id?: string;
}

export interface WebSocketConfig {
  url: string;
  reconnectInterval: number;
  maxReconnectAttempts: number;
  heartbeatInterval: number;
  messageQueueSize: number;
  enableCompression: boolean;
}

export type ConnectionStatus =
  | "connecting"
  | "connected"
  | "disconnected"
  | "error"
  | "reconnecting";

export interface ConnectionState {
  status: ConnectionStatus;
  lastConnected?: Date;
  reconnectAttempts: number;
  latency?: number;
  error?: string;
}

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private config: WebSocketConfig;
  private reconnectTimer: number | null = null;
  private heartbeatTimer: number | null = null;
  private isIntentionalClose = false;
  private messageQueue: WebSocketMessage[] = [];
  private messageHandlers = new Map<
    string,
    Set<(message: WebSocketMessage) => void>
  >();
  private connectionPromise: Promise<void> | null = null;

  // Reactive stores
  public connectionState: Writable<ConnectionState>;
  public lastMessage: Writable<WebSocketMessage | null>;
  public messageCount: Writable<number>;

  constructor(config?: Partial<WebSocketConfig>) {
    this.config = {
      url: env.WEBSOCKET_URL,
      reconnectInterval: env.WEBSOCKET_RECONNECT_INTERVAL,
      maxReconnectAttempts: env.MAX_RECONNECT_ATTEMPTS,
      heartbeatInterval: 30000,
      messageQueueSize: 1000,
      enableCompression: true,
      ...config,
    };

    // Initialize stores
    this.connectionState = writable<ConnectionState>({
      status: "disconnected",
      reconnectAttempts: 0,
    });

    this.lastMessage = writable<WebSocketMessage | null>(null);
    this.messageCount = writable(0);

    // Auto-connect in browser environment
    if (typeof window !== "undefined") {
      this.connect();
    }
  }

  /**
   * Connect to WebSocket server
   */
  async connect(): Promise<void> {
    if (this.connectionPromise) {
      return this.connectionPromise;
    }

    this.connectionPromise = this._connect();
    return this.connectionPromise;
  }

  private async _connect(): Promise<void> {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      return;
    }

    this.isIntentionalClose = false;
    this.updateConnectionState({ status: "connecting" });

    try {
      log(`Connecting to WebSocket: ${this.config.url}`);

      this.ws = new WebSocket(this.config.url);

      // Configure WebSocket
      if (this.config.enableCompression) {
        // Note: Compression is typically handled by the server
      }

      this.setupEventListeners();

      // Wait for connection to open
      await new Promise<void>((resolve, reject) => {
        if (!this.ws) {
          reject(new Error("WebSocket instance is null"));
          return;
        }

        const onOpen = () => {
          this.ws?.removeEventListener("open", onOpen);
          this.ws?.removeEventListener("error", onError);
          resolve();
        };

        const onError = (_event: Event) => {
          this.ws?.removeEventListener("open", onOpen);
          this.ws?.removeEventListener("error", onError);
          reject(new Error("WebSocket connection failed"));
        };

        this.ws.addEventListener("open", onOpen);
        this.ws.addEventListener("error", onError);
      });
    } catch (err) {
      error("WebSocket connection failed:", err);
      this.updateConnectionState({
        status: "error",
        error: err instanceof Error ? err.message : "Connection failed",
      });
      this.scheduleReconnect();
      throw err;
    } finally {
      this.connectionPromise = null;
    }
  }

  /**
   * Setup WebSocket event listeners
   */
  private setupEventListeners(): void {
    if (!this.ws) return;

    this.ws.onopen = () => {
      log("WebSocket connected");
      this.updateConnectionState({
        status: "connected",
        lastConnected: new Date(),
        reconnectAttempts: 0,
        error: undefined,
      });

      this.startHeartbeat();
      this.processMessageQueue();
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (err) {
        warn("Failed to parse WebSocket message:", event.data, err);
      }
    };

    this.ws.onclose = (event) => {
      log(`WebSocket closed: ${event.code} ${event.reason}`);
      this.stopHeartbeat();

      if (!this.isIntentionalClose) {
        this.updateConnectionState({ status: "disconnected" });
        this.scheduleReconnect();
      }
    };

    this.ws.onerror = (event) => {
      error("WebSocket error:", event);
      this.updateConnectionState({
        status: "error",
        error: "WebSocket error occurred",
      });
    };
  }

  /**
   * Handle incoming WebSocket message
   */
  private handleMessage(message: WebSocketMessage): void {
    log("WebSocket message received:", message.type);

    // Update stores
    this.lastMessage.set(message);
    this.messageCount.update((count) => count + 1);

    // Handle heartbeat response
    if (message.type === "heartbeat_response") {
      this.handleHeartbeatResponse(message);
      return;
    }

    // Notify message handlers
    const handlers = this.messageHandlers.get(message.type) || new Set();
    const globalHandlers = this.messageHandlers.get("*") || new Set();
    [...handlers, ...globalHandlers].forEach((handler) => {
      try {
        handler(message);
      } catch (err) {
        error("Error in message handler:", err);
      }
    });
  }

  /**
   * Handle heartbeat response and calculate latency
   */
  private handleHeartbeatResponse(message: WebSocketMessage): void {
    if (message.data?.timestamp) {
      const latency = Date.now() - new Date(message.data.timestamp).getTime();
      this.updateConnectionState({ latency });
    }
  }

  /**
   * Send message to WebSocket server
   */
  send(message: WebSocketMessage): boolean {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      // Queue message for later sending
      if (this.messageQueue.length < this.config.messageQueueSize) {
        this.messageQueue.push(message);
        log("Message queued for sending:", message.type);
        return true;
      } else {
        warn("Message queue full, dropping message:", message.type);
        return false;
      }
    }

    try {
      this.ws.send(JSON.stringify(message));
      log("Message sent:", message.type);
      return true;
    } catch (err) {
      error("Failed to send message:", err);
      return false;
    }
  }

  /**
   * Process queued messages
   */
  private processMessageQueue(): void {
    while (
      this.messageQueue.length > 0 &&
      this.ws?.readyState === WebSocket.OPEN
    ) {
      const message = this.messageQueue.shift();
      if (message) {
        this.send(message);
      }
    }
  }

  /**
   * Subscribe to messages of a specific type
   */
  subscribe(
    messageType: string,
    handler: (message: WebSocketMessage) => void,
  ): () => void {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, new Set());
    }

    this.messageHandlers.get(messageType)!.add(handler);

    // Return unsubscribe function
    return () => {
      const handlers = this.messageHandlers.get(messageType);
      if (handlers) {
        handlers.delete(handler);
        if (handlers.size === 0) {
          this.messageHandlers.delete(messageType);
        }
      }
    };
  }

  /**
   * Subscribe to all messages
   */
  subscribeAll(handler: (message: WebSocketMessage) => void): () => void {
    return this.subscribe("*", handler);
  }

  /**
   * Start heartbeat mechanism
   */
  private startHeartbeat(): void {
    this.stopHeartbeat();

    this.heartbeatTimer = window.setInterval(() => {
      this.send({
        type: "heartbeat",
        timestamp: new Date().toISOString(),
      });
    }, this.config.heartbeatInterval);
  }

  /**
   * Stop heartbeat mechanism
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  /**
   * Schedule reconnection attempt
   */
  private scheduleReconnect(): void {
    if (this.isIntentionalClose) {
      return;
    }

    this.connectionState.update((state) => {
      if (state.reconnectAttempts >= this.config.maxReconnectAttempts) {
        error("Max reconnection attempts reached");
        return {
          ...state,
          status: "error",
          error: "Max reconnection attempts reached",
        };
      }

      const nextAttempt = state.reconnectAttempts + 1;
      const delay = Math.min(
        this.config.reconnectInterval * Math.pow(2, nextAttempt - 1),
        30000,
      );

      log(`Scheduling reconnection attempt ${nextAttempt} in ${delay}ms`);

      this.reconnectTimer = window.setTimeout(() => {
        this.updateConnectionState({ status: "reconnecting" });
        this.connect().catch((err) => {
          error("Reconnection failed:", err);
        });
      }, delay);

      return { ...state, reconnectAttempts: nextAttempt };
    });
  }

  /**
   * Update connection state
   */
  private updateConnectionState(updates: Partial<ConnectionState>): void {
    this.connectionState.update((state) => ({ ...state, ...updates }));
  }

  /**
   * Disconnect WebSocket
   */
  disconnect(): void {
    this.isIntentionalClose = true;

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    this.stopHeartbeat();

    if (this.ws) {
      this.ws.close(1000, "Client disconnect");
      this.ws = null;
    }

    this.updateConnectionState({ status: "disconnected" });
    log("WebSocket disconnected");
  }

  /**
   * Reconnect WebSocket
   */
  async reconnect(): Promise<void> {
    this.disconnect();
    await new Promise((resolve) => setTimeout(resolve, 100));
    return this.connect();
  }

  /**
   * Get connection statistics
   */
  getStats(): {
    isConnected: boolean;
    reconnectAttempts: number;
    messageQueueSize: number;
    latency?: number;
  } {
    let currentState: ConnectionState;
    this.connectionState.subscribe((state) => (currentState = state))();

    return {
      isConnected: currentState!.status === "connected",
      reconnectAttempts: currentState!.reconnectAttempts,
      messageQueueSize: this.messageQueue.length,
      latency: currentState!.latency,
    };
  }

  /**
   * Clear message queue
   */
  clearMessageQueue(): void {
    this.messageQueue.length = 0;
  }

  /**
   * Destroy WebSocket client
   */
  destroy(): void {
    this.disconnect();
    this.messageHandlers.clear();
    this.clearMessageQueue();
  }
}

// Create singleton instance
export const websocketClient = new WebSocketClient();

// Convenience functions
export const websocket = {
  connect: () => websocketClient.connect(),
  disconnect: () => websocketClient.disconnect(),
  reconnect: () => websocketClient.reconnect(),
  send: (message: WebSocketMessage) => websocketClient.send(message),
  subscribe: (type: string, handler: (message: WebSocketMessage) => void) =>
    websocketClient.subscribe(type, handler),
  subscribeAll: (handler: (message: WebSocketMessage) => void) =>
    websocketClient.subscribeAll(handler),
  getStats: () => websocketClient.getStats(),

  // Reactive stores
  connectionState: websocketClient.connectionState,
  lastMessage: websocketClient.lastMessage,
  messageCount: websocketClient.messageCount,
};


