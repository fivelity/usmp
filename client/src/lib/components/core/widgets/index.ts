// Widget registry - exports all available widgets
export { default as TextGauge } from "../gauges/TextGauge.svelte"
export { default as RadialGauge } from "../gauges/RadialGauge.svelte"
export { default as LinearGauge } from "../gauges/LinearGauge.svelte"
export { default as GraphGauge } from "../gauges/GraphGauge.svelte"
export { default as ImageSequenceGauge } from "../gauges/ImageSequenceGauge.svelte"
export { default as GlassmorphicGauge } from "../gauges/GlassmorphicGauge.svelte"

// Custom widgets
export { default as SystemStatusWidget } from "./SystemStatusWidget.svelte"

// Widget inspectors
export { default as SystemStatusInspector } from "./SystemStatusInspector.svelte"

// Widget type registry
import type { ExtendedGaugeType, WidgetConfig, GaugeSettings, WidgetTypeDefinition } from "$lib/types/widgets"

export const widgetTypes: Record<ExtendedGaugeType, WidgetTypeDefinition> = {
  text: {
    id: "text",
    name: "Text Display",
    description: "Simple text display for sensor values",
    category: "basic",
    component: null, // Will be imported dynamically
    inspector: null, // Will be imported dynamically
    defaultConfig: {
      min_value: 0,
      max_value: 100,
      unit: "",
      format: "number",
      decimals: 2,
      show_value: true,
      show_min_max: false,
      show_unit: true,
      color_scheme: "default",
      animation_duration: 300,
      update_interval: 1000
    },
    icon: "text"
  },
  radial: {
    id: "radial",
    name: "Radial Gauge",
    description: "Circular gauge display",
    category: "basic",
    component: null,
    inspector: null,
    defaultConfig: {
      min_value: 0,
      max_value: 100,
      unit: "",
      format: "number",
      decimals: 2,
      show_value: true,
      show_min_max: true,
      show_unit: true,
      color_scheme: "default",
      animation_duration: 300,
      update_interval: 1000
    },
    icon: "radial"
  },
  linear: {
    id: "linear",
    name: "Linear Gauge",
    description: "Horizontal or vertical gauge display",
    category: "basic",
    component: null,
    inspector: null,
    defaultConfig: {
      min_value: 0,
      max_value: 100,
      unit: "",
      format: "number",
      decimals: 2,
      show_value: true,
      show_min_max: true,
      show_unit: true,
      color_scheme: "default",
      animation_duration: 300,
      update_interval: 1000
    },
    icon: "linear"
  },
  graph: {
    id: "graph",
    name: "Graph Display",
    description: "Time-series graph display",
    category: "advanced",
    component: null,
    inspector: null,
    defaultConfig: {
      min_value: 0,
      max_value: 100,
      unit: "",
      format: "number",
      decimals: 2,
      show_value: true,
      show_min_max: true,
      show_unit: true,
      color_scheme: "default",
      animation_duration: 300,
      update_interval: 1000
    },
    icon: "graph"
  },
  image: {
    id: "image",
    name: "Image Display",
    description: "Display images or icons",
    category: "basic",
    component: null,
    inspector: null,
    defaultConfig: {
      min_value: 0,
      max_value: 100,
      unit: "",
      format: "number",
      decimals: 2,
      show_value: true,
      show_min_max: false,
      show_unit: true,
      color_scheme: "default",
      animation_duration: 300,
      update_interval: 1000
    },
    icon: "image"
  },
  glassmorphic: {
    id: "glassmorphic",
    name: "Glassmorphic Display",
    description: "Modern glassmorphic style display",
    category: "advanced",
    component: null,
    inspector: null,
    defaultConfig: {
      min_value: 0,
      max_value: 100,
      unit: "",
      format: "number",
      decimals: 2,
      show_value: true,
      show_min_max: true,
      show_unit: true,
      color_scheme: "default",
      animation_duration: 300,
      update_interval: 1000
    },
    icon: "glassmorphic"
  },
  system_status: {
    id: "system_status",
    name: "System Status",
    description: "Display system status information",
    category: "advanced",
    component: null,
    inspector: null,
    defaultConfig: {
      layout: "compact",
      columns: 2,
      metrics: [],
      show_icons: true,
      show_labels: true,
      show_values: true,
      show_units: true,
      use_status_colors: true,
      warning_threshold: 80,
      critical_threshold: 90,
      animate_changes: true,
      update_animation: "fade"
    },
    icon: "system_status"
  }
}

// Helper function to get widget type definition
export function getWidgetType(type: ExtendedGaugeType): WidgetTypeDefinition {
  return widgetTypes[type]
}

// Helper function to get all widget types
export function getAllWidgetTypes(): WidgetTypeDefinition[] {
  return Object.values(widgetTypes)
}

// Helper function to get widget types by category
export function getWidgetTypesByCategory(category: "basic" | "advanced" | "custom"): WidgetTypeDefinition[] {
  return Object.values(widgetTypes).filter(widget => widget.category === category)
}

// Helper function to create a new widget config
export function createWidgetConfig(type: ExtendedGaugeType, x: number, y: number, width: number, height: number): WidgetConfig {
  const widgetType = getWidgetType(type)
  return {
    id: crypto.randomUUID(),
    type: type,
    pos_x: x,
    pos_y: y,
    width: width,
    height: height,
    is_locked: false,
    gauge_type: type,
    gauge_settings: widgetType.defaultConfig,
    z_index: 0,
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false
  }
}
