import type { GaugeSettings } from "./index"

// Extend the existing GaugeType to include our custom widget
export type ExtendedGaugeType = "text" | "radial" | "linear" | "graph" | "image" | "glassmorphic" | "system_status"

// Export the GaugeSettings type
export type { GaugeSettings }

// Custom configuration for System Status Widget
export interface SystemStatusConfig extends GaugeSettings {
  // Layout options
  layout: "compact" | "detailed" | "minimal"
  columns: number

  // Metric selection
  metrics: SystemMetric[]

  // Visual options
  show_icons: boolean
  show_labels: boolean
  show_values: boolean
  show_units: boolean

  // Color coding
  use_status_colors: boolean
  warning_threshold: number
  critical_threshold: number

  // Animation
  animate_changes: boolean
  update_animation: "fade" | "slide" | "pulse" | "none"
}

export interface SystemMetric {
  id: string
  sensor_id: string
  label: string
  icon?: string
  unit?: string
  min_value?: number
  max_value?: number
  warning_threshold?: number
  critical_threshold?: number
  format?: "number" | "percentage" | "temperature" | "frequency" | "bytes"
}

// Status levels for color coding
export type StatusLevel = "normal" | "warning" | "critical" | "unknown"

export interface WidgetConfig {
  id: string
  type: ExtendedGaugeType
  pos_x: number
  pos_y: number
  width: number
  height: number
  is_locked: boolean
  gauge_type?: ExtendedGaugeType
  gauge_settings?: GaugeSettings
  group_id?: string
  z_index: number
  title?: string
  description?: string
  is_visible: boolean
  is_draggable: boolean
  is_resizable: boolean
  is_selectable: boolean
  is_grouped: boolean
  parent_id?: string
  children?: string[]
  style?: {
    background_color?: string
    border_color?: string
    border_width?: number
    border_radius?: number
    padding?: number
    margin?: number
    opacity?: number
    shadow?: string
  }
}

// Widget type definition
export interface WidgetTypeDefinition {
  id: ExtendedGaugeType
  name: string
  description: string
  category: "basic" | "advanced" | "custom"
  component: any
  inspector?: any
  defaultConfig: GaugeSettings | SystemStatusConfig
  icon: string
  preview?: string
}
