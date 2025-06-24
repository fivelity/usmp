import { PUBLIC_WS_URL } from "$env/static/public";

function createWebSocketStore() {
  let status = $state<"connecting" | "connected" | "disconnected" | "error">(
    "disconnected",
  );
  let socket: WebSocket | null = $state(null);
  let message = $state<any>(null); // The latest message received

  // Reconnection state management
  let reconnectAttempts = 0;
  const maxReconnectAttempts = 5;
let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  let isReconnecting = false;

  // Progressive backoff delays (in milliseconds)
  const backoffDelays = [1000, 2000, 5000, 10000, 30000]; // 1s, 2s, 5s, 10s, 30s

  function connect() {
    // Prevent multiple concurrent connection attempts
    if (socket?.readyState === WebSocket.CONNECTING || isReconnecting) {
      console.log("[WebSocket] Connection already in progress, skipping...");
      return;
    }

    if (socket?.readyState === WebSocket.OPEN) {
      console.log("[WebSocket] Already connected, skipping...");
      return;
    }

    console.log("[WebSocket] Connecting to:", PUBLIC_WS_URL);
    status = "connecting";
    const ws = new WebSocket(PUBLIC_WS_URL);

    ws.onopen = () => {
      console.log("[WebSocket] Connection established.");
      status = "connected";
      socket = ws;
      // Reset reconnection state on successful connection
      reconnectAttempts = 0;
      isReconnecting = false;
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
        reconnectTimeout = null;
      }
    };

    ws.onmessage = (event) => {
      try {
        message = JSON.parse(event.data);
      } catch (error) {
        console.error("[WebSocket] Error parsing message:", error);
      }
    };

    ws.onclose = (event) => {
      console.log(
        `[WebSocket] Connection closed. Code: ${event.code}, Reason: ${event.reason}`,
      );
      status = "disconnected";
      socket = null;

      // Only attempt reconnection if it wasn't a normal closure and we haven't exceeded max attempts
      if (event.code !== 1000 && reconnectAttempts < maxReconnectAttempts) {
        scheduleReconnect();
      } else if (reconnectAttempts >= maxReconnectAttempts) {
        console.error(
          "[WebSocket] Max reconnection attempts reached. Giving up.",
        );
        status = "error";
      }
    };

    ws.onerror = (error) => {
      console.error("[WebSocket] Connection error:", error);
      status = "error";
      socket = null;

      // Schedule reconnection on error
      if (reconnectAttempts < maxReconnectAttempts) {
        scheduleReconnect();
      }
    };
  }

  function scheduleReconnect() {
    if (isReconnecting || reconnectTimeout) {
      return; // Already scheduled
    }

    isReconnecting = true;
    const delay =
      backoffDelays[Math.min(reconnectAttempts, backoffDelays.length - 1)];

    console.log(
      `[WebSocket] Scheduling reconnection attempt ${reconnectAttempts + 1}/${maxReconnectAttempts} in ${delay}ms`,
    );

    reconnectTimeout = setTimeout(() => {
      reconnectAttempts++;
      reconnectTimeout = null;
      isReconnecting = false;
      connect();
    }, delay);
  }

  function disconnect() {
    if (socket) {
      socket.close();
    }
  }

  function send(data: any) {
    if (socket?.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(data));
    } else {
      console.warn("[WebSocket] Cannot send message, socket not open.");
    }
  }

  return {
    get status() {
      return status;
    },
    get message() {
      return message;
    },
    connect,
    disconnect,
    send,
  };
}

export const websocketStore = createWebSocketStore();
