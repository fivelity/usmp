import { PUBLIC_WS_URL } from '$env/static/public';

function createWebSocketStore() {
  let status = $state<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
  let socket: WebSocket | null = $state(null);
  let listeners: ((message: any) => void)[] = [];

  function connect() {
    if (socket) return;

    console.log('[WebSocket] Connecting to:', PUBLIC_WS_URL);
    status = 'connecting';
    const ws = new WebSocket(PUBLIC_WS_URL);

    ws.onopen = () => {
      console.log('[WebSocket] Connection established.');
      status = 'connected';
      socket = ws;
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        listeners.forEach(l => l(message));
      } catch (error) {
        console.error('[WebSocket] Error parsing message:', error);
      }
    };

    ws.onclose = () => {
      console.log('[WebSocket] Connection closed.');
      status = 'disconnected';
      socket = null;
    };

    ws.onerror = (error) => {
      console.error('[WebSocket] Connection error:', error);
      status = 'error';
      socket = null;
    };
  }

  function disconnect() {
    if (socket) {
      socket.close();
    }
  }

  function subscribe(callback: (message: any) => void) {
    listeners.push(callback);
    return () => {
      listeners = listeners.filter(l => l !== callback);
    };
  }
  
  function send(message: any) {
    if (socket?.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
    } else {
      console.warn('[WebSocket] Cannot send message, socket not open.');
    }
  }

  return {
    get status() { return status; },
    connect,
    disconnect,
    subscribe,
    send
  };
}

export const websocketStore = createWebSocketStore(); 