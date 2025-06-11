import { PUBLIC_WS_URL } from "$env/static/public";

function createWebSocketStore() {
  let status = $state<"connecting" | "connected" | "disconnected" | "error">(
    "disconnected",
  );
  let socket: WebSocket | null = $state(null);
  let message = $state<any>(null); // The latest message received

  function connect() {
    if (socket) return;

    console.log("[WebSocket] Connecting to:", PUBLIC_WS_URL);
    status = "connecting";
    const ws = new WebSocket(PUBLIC_WS_URL);

    ws.onopen = () => {
      console.log("[WebSocket] Connection established.");
      status = "connected";
      socket = ws;
    };

    ws.onmessage = (event) => {
      try {
        message = JSON.parse(event.data);
      } catch (error) {
        console.error("[WebSocket] Error parsing message:", error);
      }
    };

    ws.onclose = () => {
      console.log("[WebSocket] Connection closed.");
      status = "disconnected";
      socket = null;
    };

    ws.onerror = (error) => {
      console.error("[WebSocket] Connection error:", error);
      status = "error";
      socket = null;
    };
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
