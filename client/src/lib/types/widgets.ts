import type { GaugeSettings, SystemStatusConfig, SystemMetric } from "./gauges";

// Extend the existing GaugeType to include our custom widget
export type ExtendedGaugeType =
  | "text"
  | "radial"
  | "linear"
  | "graph"
  | "image"
  | "glassmorphic"
  | "system_status"
  | "gauge"; // Add for backward compatibility

// Export the types from gauges.ts
export type { GaugeSettings, SystemStatusConfig, SystemMetric };

// Status levels for color coding
export type StatusLevel = "normal" | "warning" | "critical" | "unknown";

export interface WidgetConfig {
  id: string;
  type: ExtendedGaugeType;
  title: string; // Made required to match test expectations
  pos_x: number;
  pos_y: number;
  x?: number; // Alternative property name for compatibility
  y?: number; // Alternative property name for compatibility
  width: number;
  height: number;
  is_locked: boolean;
  locked?: boolean; // Alternative property name
  gauge_type: ExtendedGaugeType;
  gauge_settings: GaugeSettings;
  group_id?: string;
  z_index: number;
  description?: string;
  custom_label?: string;
  show_label?: boolean;
  show_unit?: boolean;
  is_visible: boolean;
  is_draggable: boolean;
  is_resizable: boolean;
  is_selectable: boolean;
  is_grouped: boolean;
  parent_id?: string;
  children?: string[];
  style?: {
    background_color?: string;
    border_color?: string;
    border_width?: number;
    border_radius?: number;
    padding?: number;
    margin?: number;
    opacity?: number;
    shadow?: string;
  };
  custom_unit?: string;
  sensor_id?: string;
}

// Widget type definition
export interface WidgetTypeDefinition {
  id: ExtendedGaugeType;
  name: string;
  description: string;
  category: "basic" | "advanced" | "custom";
  component: any;
  inspector?: any;
  defaultConfig: GaugeSettings | SystemStatusConfig;
  icon: string;
  preview?: string;
}

export interface WidgetGroup {
  id: string;
  name: string;
  widget_ids: string[];
  widgets: string[]; // Alternative property name for compatibility
  is_collapsed: boolean;
  layout?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  metadata?: {
    description?: string;
  };
}

export interface Widget {
  id: string;
  name: string;
  type: ExtendedGaugeType;
  pos_x: number;
  pos_y: number;
  x: number; // Alternative property name for compatibility
  y: number; // Alternative property name for compatibility
  width: number;
  height: number;
  is_locked: boolean;
  groupId?: string;
  group_id?: string; // Alternative property name
  config?: any;
  style?: Record<string, any>; // For custom CSS styles
}
