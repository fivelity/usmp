/**
 * Shared type definitions between frontend and backend
 * This file ensures consistency in WebSocket message formats and sensor data structures
 */

export interface WebSocketMessage {
  type: 'sensor_data' | 'connection_established' | 'ping' | 'pong' | 'error' | 'ack';
  timestamp: string;
  data?: any;
  error?: string;
  client_id?: string;
  message?: string;
  server_info?: {
    version: string;
    capabilities: string[];
  };
}

export interface SensorReading {
  sensor_id: string;
  name: string;
  value: number;
  unit: string;
  category: 'temperature' | 'voltage' | 'current' | 'power' | 'fan' | 'clock' | 'load' | 'flow' | 'control' | 'level' | 'throughput' | 'data' | 'smalldata' | 'factor' | 'frequency' | 'unknown';
  hardware_type: string;
  parent_hardware?: string;
  timestamp: string;
  status: 'active' | 'inactive' | 'error';
  min_value?: number;
  max_value?: number;
  source?: string;
  quality?: 'excellent' | 'good' | 'fair' | 'poor' | 'unknown';
  metadata?: Record<string, any>;
}

export interface SensorDataBroadcast {
  sources: Record<string, SensorReading[]>;
  timestamp: string;
  total_sensors: number;
  active_sources: number;
  forced?: boolean;
}

export interface SensorSource {
  id: string;
  name: string;
  description: string;
  version: string;
  active: boolean;
  connection_status: 'connected' | 'disconnected' | 'connecting' | 'error';
  hardware_components: any[];
  last_update: string;
  error_message?: string;
}

export interface ConnectionMetadata {
  client_id: string;
  connected_at: Date;
  messages_sent: number;
  last_activity: Date;
  connection_errors: number;
  last_ping?: Date;
  user_agent: string;
}

export interface WebSocketStats {
  total_connections: number;
  total_messages_sent: number;
  connections: Array<{
    connected_at: string;
    messages_sent: number;
    last_activity: string;
  }>;
}

export interface RealTimeServiceStats {
  is_running: boolean;
  broadcast_interval: number;
  broadcasts_sent: number;
  last_broadcast_time: string | null;
  errors_count: number;
  connected_clients: number;
  active_connections: Array<{
    client_id: string;
    connected_at: string | null;
    messages_sent: number;
  }>;
}
