/**
 * Type definitions for system status and events.
 */

export interface SystemEvent {
  id: string;
  type: "info" | "warning" | "error" | "success";
  message: string;
  timestamp: number;
  duration?: number;
}

export interface SystemState {
  events: SystemEvent[];
}
